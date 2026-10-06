#!/usr/bin/env python3
"""Mavjud ~/.claude/settings.json ga yangi o'rnatish sozlamasini qo'shadi.

    python3 install/merge_settings.py <mavjud> <yangi> --root <klon>
    python3 install/merge_settings.py <mavjud> <yangi> --root <klon> --yoz

Nega kerak: `manguberdi.ps1 -Update` git pull dan keyin faqat o'z
birliklarini almashtiradi. settings.json da esa foydalanuvchining o'z
hooklari, ruxsatlari va boshqa kalitlari ham turadi: faylni butunligicha
yangisi bilan bosish ularni o'chirardi. Shuning uchun faqat shu klonning
`tools/` papkasiga ishora qilgan yozuvlar almashadi.

O'zniki: buyrug'i (teskari slash `/` ga, harflar kichikka o'girilgach)
`<root>/tools/` ni o'z ichiga olgan hook. Root ham xuddi shunday
normallanadi, oxirgi slash kesiladi. Ruxsat qoidasida root ning o'zi
yetadi, lekin `claude-genius-eski` kabi boshqa klon tutilmasligi uchun
root dan keyin yo'l davom etmasligi tekshiriladi.

Birlashtirish:
- `hooks`: har hodisada mavjud guruhlardan o'z hooklari olib tashlanadi,
  shundan bo'shab qolgan guruh tushadi, keyin yangi fayldagi shu hodisa
  guruhlari oxiriga qo'shiladi. Qolgani o'z tartibida turadi.
- `permissions.allow`, `ask` va `deny`: uchalasida bir xil qoida. O'z
  qoidalari tushadi, yangilari qo'shiladi, takror olib tashlanadi, tartib
  saqlanadi. Avval faqat `allow` shunday edi, `ask` va `deny` esa
  foydalanuvchida bo'lsa eski holicha qolardi: o'rnatuvchining yangi
  qoidasi -Update da jim tushib qolardi.
- `permissions.additionalDirectories`: root ning o'zi va `<root>/`
  ostidagi yozuvlar o'ziniki, ular tushadi, keyin yangilari qo'shiladi.
  Shunda butun klon yozuvi `<root>/docs` va `<root>/memory` ga
  almashganda eskisi qolib ketmaydi.
- `env`: yangi kalitlar ustun.
- Boshqa kalitlar joyida qoladi, faqat yangi faylda bo'lganlari qo'shiladi.

Migratsiya: `bashOutputMaxChars`. Avvalgi o'rnatuvchi bu kalitni yozardi,
lekin u Claude Code sozlama sxemasida yo'q va jim e'tiborsiz qoladi.
Qiymati aynan 12000 (o'rnatuvchi yozgan qiymat) bo'lsa olib tashlanadi va
xulosa qatorida aytiladi. Boshqa qiymat foydalanuvchiniki, unga
tegilmaydi: ehtimol u kalit kelajakda paydo bo'lishiga ishongan.

Quruq yurish (`--yoz` siz) bir qatorlik xulosa chiqaradi va hech narsa
yozmaydi. Mavjud fayl `utf-8-sig` bilan o'qiladi: PowerShell 5.1 dagi
eski o'rnatuvchi BOM yozgan. Fayl yo'q bo'lsa `{}`. Buzuq JSON yoki obyekt
bo'lmagan fayl: sabab aytiladi, 1 qaytadi, hech narsa yozilmaydi.
`--yoz` BOM siz UTF-8, indent 2 bilan, shu papkadagi vaqtinchalik fayl
va `os.replace` orqali yozadi: yarim yozilgan settings.json qolmaydi.

Bu mantiq shu yerda, Python da turadi: PowerShell qismi agent sessiyasida
sinalmaydi, bu esa `tools/test_merge_settings.py` da sinaladi.
"""

import argparse
import json
import os
import re
import sys
import tempfile


class SozlamaXato(Exception):
    """settings.json ni birlashtirib bo'lmaydi: sabab matnda."""


def norm(text):
    return text.replace("\\", "/").lower()


def norm_root(root):
    return norm(root).rstrip("/")


def is_own_hook(hook, root):
    command = hook.get("command") if isinstance(hook, dict) else None
    return isinstance(command, str) and (root + "/tools/") in norm(command)


def is_own_rule(rule, root):
    """Root dan keyin yo'l nomi davom etmasa: `<root>-eski` boshqa klon."""
    if not isinstance(rule, str) or not root:
        return False
    return re.search(re.escape(root) + r"(?![\w.-])", norm(rule)) is not None


def is_own_dir(entry, root):
    """additionalDirectories yozuvi: root ning o'zi yoki uning ostida.

    `<root>-eski` boshqa klon: root dan keyin `/` kelishi shart."""
    if not isinstance(entry, str) or not root:
        return False
    path = norm_root(entry)
    return path == root or path.startswith(root + "/")


def read_settings(path, must_exist):
    """settings.json ni obyekt qilib o'qiydi. Yo'q fayl: {} yoki xato."""
    if not os.path.exists(path):
        if must_exist:
            raise SozlamaXato("fayl yo'q: %s" % path)
        return {}
    try:
        with open(path, encoding="utf-8-sig") as handle:
            data = json.load(handle)
    except ValueError as exc:
        raise SozlamaXato("JSON buzuq: %s (%s)" % (path, exc)) from exc
    except OSError as exc:
        raise SozlamaXato("o'qilmadi: %s (%s)" % (path, exc)) from exc
    if not isinstance(data, dict):
        raise SozlamaXato("JSON obyekt emas: %s" % path)
    return data


def section(data, key, kind, path):
    """data[key] yo'q bo'lsa bo'sh, turi boshqa bo'lsa xato."""
    value = data.get(key)
    if value is None:
        return kind()
    if not isinstance(value, kind):
        raise SozlamaXato("%s: '%s' %s emas" % (
            path, key, "obyekt" if kind is dict else "ro'yxat"))
    return value


def merge_hooks(old, new, root, stats):
    merged = {}
    for event in list(old) + [e for e in new if e not in old]:
        old_groups = old.get(event, [])
        new_groups = new.get(event, [])
        if not isinstance(old_groups, list) or not isinstance(new_groups, list):
            raise SozlamaXato("hooks.%s ro'yxat emas" % event)
        groups = []
        for group in old_groups:
            hooks = group.get("hooks") if isinstance(group, dict) else None
            if not isinstance(hooks, list):
                groups.append(group)  # notanish shakl: begona, tegilmaydi
                continue
            kept = [h for h in hooks if not is_own_hook(h, root)]
            stats["eski"] += len(hooks) - len(kept)
            if hooks and not kept:
                continue  # faqat o'z hooklari bor edi
            if len(kept) != len(hooks):
                group = dict(group, hooks=kept)
            groups.append(group)
        for group in new_groups:
            hooks = group.get("hooks") if isinstance(group, dict) else None
            stats["yangi"] += len(hooks) if isinstance(hooks, list) else 0
            groups.append(group)
        if groups or (event in old and not old_groups):
            merged[event] = groups
    return merged


def dedupe(items):
    seen, out = set(), []
    for item in items:
        key = json.dumps(item, sort_keys=True, ensure_ascii=False)
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


# Ruxsat ro'yxatlari: uchalasi bir xil qoida bilan birlashadi.
RULE_LISTS = ("allow", "ask", "deny")


def merge_permissions(old, new, root, stats, path):
    lists = {}
    for key in RULE_LISTS:
        rules_old = section(old, key, list, path + " permissions")
        rules_new = section(new, key, list, "yangi permissions")
        kept = [r for r in rules_old if not is_own_rule(r, root)]
        stats["ruxsat_eski"] += len(rules_old) - len(kept)
        stats["ruxsat_yangi"] += len(rules_new)
        lists[key] = dedupe(kept + rules_new)
    dirs_old = section(old, "additionalDirectories", list, path + " permissions")
    dirs_new = section(new, "additionalDirectories", list, "yangi permissions")
    dirs = dedupe([d for d in dirs_old if not is_own_dir(d, root)] + dirs_new)

    merged = {}
    for key in list(old) + [k for k in new if k not in old]:
        if key in lists:
            merged[key] = lists[key]
        elif key == "additionalDirectories":
            merged[key] = dirs
        else:
            merged[key] = old[key] if key in old else new[key]
    return merged


# Avvalgi o'rnatuvchi yozgan, sxemada yo'q kalitlar: (nom, o'rnatuvchi
# yozgan qiymat). Faqat aynan shu qiymat olib tashlanadi.
LEGACY = (("bashOutputMaxChars", 12000),)


def drop_legacy(merged, stats):
    """O'rnatuvchi yozgan, lekin sxemada yo'q kalitlarni oladi.

    Boshqa qiymat foydalanuvchiniki: qoldiriladi. `merged` joyida
    o'zgaradi, olib tashlanganlar nomi stats ga yoziladi.
    """
    for name, written in LEGACY:
        if name in merged and merged[name] == written:
            del merged[name]
            stats["eskirgan"].append(name)


def merge(old, new, root, path="mavjud"):
    """(birlashgan sozlama, sanoq). old va new o'zgarmaydi."""
    root = norm_root(root)
    stats = {"eski": 0, "yangi": 0, "ruxsat_eski": 0, "ruxsat_yangi": 0,
             "eskirgan": []}
    hooks = merge_hooks(section(old, "hooks", dict, path),
                        section(new, "hooks", dict, "yangi"), root, stats)
    permissions = merge_permissions(
        section(old, "permissions", dict, path),
        section(new, "permissions", dict, "yangi"), root, stats, path)
    env = dict(section(old, "env", dict, path))
    env.update(section(new, "env", dict, "yangi"))

    merged = {}
    for key in list(old) + [k for k in new if k not in old]:
        if key == "hooks":
            merged[key] = hooks
        elif key == "permissions":
            merged[key] = permissions
        elif key == "env":
            merged[key] = env
        else:
            merged[key] = old[key] if key in old else new[key]
    drop_legacy(merged, stats)
    return merged, stats


def summary(stats, existed):
    if not existed:
        return ("settings.json yo'q edi: %d hook va %d ruxsat bilan yangisi"
                % (stats["yangi"], stats["ruxsat_yangi"]))
    swapped = min(stats["eski"], stats["yangi"])
    parts = ["%d hook almashdi" % swapped,
             "%d qo'shildi" % (stats["yangi"] - swapped)]
    if stats["eski"] > stats["yangi"]:
        parts.append("%d olib tashlandi" % (stats["eski"] - stats["yangi"]))
    rules = min(stats["ruxsat_eski"], stats["ruxsat_yangi"])
    parts.append("%d ruxsat almashdi" % rules)
    if stats["ruxsat_yangi"] > rules:
        parts.append("%d ruxsat qo'shildi" % (stats["ruxsat_yangi"] - rules))
    if stats["ruxsat_eski"] > rules:
        parts.append("%d ruxsat olib tashlandi" % (stats["ruxsat_eski"] - rules))
    for name in stats.get("eskirgan", ()):
        parts.append("%s olib tashlandi (sozlama sxemasida yo'q)" % name)
    return ", ".join(parts) + ", boshqa yozuvlar saqlandi"


def render(data):
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def write_atomic(path, text):
    """Shu papkadagi vaqtinchalik fayl va os.replace: yarim fayl qolmaydi."""
    folder = os.path.dirname(os.path.abspath(path))
    os.makedirs(folder, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".settings-", suffix=".tmp", dir=folder)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(text.encode("utf-8"))
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("mavjud", help="hozirgi settings.json (yo'q bo'lsa {})")
    parser.add_argument("yangi", help="toza o'rnatishning to'liq settings.json i")
    parser.add_argument("--root", required=True, help="claude-genius klonining yo'li")
    parser.add_argument("--yoz", action="store_true",
                        help="mavjud faylga yozadi; bersiz faqat xulosa")
    args = parser.parse_args(argv)

    try:
        existed = os.path.exists(args.mavjud)
        old = read_settings(args.mavjud, must_exist=False)
        new = read_settings(args.yangi, must_exist=True)
        merged, stats = merge(old, new, args.root, args.mavjud)
    except SozlamaXato as exc:
        print("settings.json birlashtirilmadi: %s" % exc)
        return 1

    line = summary(stats, existed)
    if not args.yoz:
        print("settings.json (quruq, yozilmadi): %s" % line)
        return 0
    try:
        write_atomic(args.mavjud, render(merged))
    except OSError as exc:
        print("settings.json yozilmadi: %s (%s)" % (args.mavjud, exc))
        return 1
    print("settings.json: %s" % line)
    return 0


if __name__ == "__main__":
    # Windows konsoli cp1252 bo'lsa yo'ldagi notanish harf xulosani
    # yiqitmasin: almashtirib chiqariladi.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    sys.exit(main())
