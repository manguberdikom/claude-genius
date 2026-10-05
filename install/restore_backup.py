#!/usr/bin/env python3
"""Eski o'rnatuvchi o'chirgan sozlamalarni zaxiradan qaytaradi.

    python3 install/restore_backup.py <zaxira-papkasi>
    python3 install/restore_backup.py <zaxira-papkasi> --yoz
    python3 install/restore_backup.py <zaxira-papkasi> --claude <papka>

Nega kerak: o'rnatuvchining avvalgi versiyasi `-Update` siz `-Apply`
berilganda ~/.claude dagi settings.json, settings.local.json, CLAUDE.md,
skills, agents, commands, plugins, hooks, rules va output-styles ni
o'chirardi. Hammasi zaxiraga tushgan, lekin zaxirada birliklar
`<ota>--<nom>` nomi bilan yotadi (`~/.claude/settings.json` ->
`.claude--settings.json`, `skills\\` -> `.claude--skills`), shuning uchun
butun papkani `~/.claude` ga ko'chirish hech narsani tiklamaydi.

Qoida: faqat HOZIR yo'q bo'lgan narsa qaytariladi. Yangi o'rnatish
qo'shuvchi, ya'ni o'z birliklaridan boshqasiga tegmaydi: shuning uchun
hozir turgan fayl foydalanuvchining joriy holati va u ustidan
yozilmaydi.

- CLAUDE.md, commands, plugins, hooks, rules, output-styles: butunligicha,
  faqat hozir yo'q bo'lsa.
- skills va agents: ichidagi faqat yo'q bo'lgan bolalar. manguberdi
  skilli va olti aktyor fayli ataylab tashlanadi: ularni o'rnatuvchi
  boshqaradi, zaxiradagisi esa eski versiya.
- settings.json: birlashtiriladi. Zaxiradagi foydalanuvchi yozuvlari
  qaytadi, HOZIRGI fayldagi yozuvlar ustun turadi, ya'ni yangi
  o'rnatishning hooklari va ruxsatlari yo'qolmaydi.
- settings.local.json: faqat hozir yo'q bo'lsa.

Default quruq yurish: nima qaytishini aytadi, hech narsa yozmaydi.
`--yoz` bilan yozadi.
"""

import argparse
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from merge_settings import (SozlamaXato, read_settings, render,  # noqa: E402
                            write_atomic)

# Zaxirada birlik nomi: `<ota papka nomi>--<birlik nomi>`.
SEP = "--"

# Butunligicha qaytariladigan birliklar.
WHOLE = ("CLAUDE.md", "settings.local.json", "commands", "plugins", "hooks",
         "rules", "output-styles")
# Ichidagi bolalar bo'yicha qaytariladigan papkalar.
MERGED_DIRS = ("skills", "agents")
# O'rnatuvchi boshqaradigan birliklar: zaxiradagisi eski versiya.
OWN_SKILL = "manguberdi"
OWN_AGENTS = ("qidiruv", "tahlil", "review", "arxitektor", "test-muhandis",
              "rejalashtiruvchi")


def backup_entries(folder):
    """Zaxiradagi `<ota>--<nom>` birliklari: {nom: yo'l}.

    Ota nomi tekshirilmaydi: eski zaxirada u `.claude`, proyekt zaxirasida
    esa proyekt papkasining nomi bo'lishi mumkin. Nom ichida `--` bo'lsa
    oxirgi ajratgich olinadi, chunki ota nomi `my--repo` bo'lishi mumkin.
    """
    found = {}
    if not os.path.isdir(folder):
        return found
    for name in sorted(os.listdir(folder)):
        if SEP not in name:
            continue
        unit = name.rsplit(SEP, 1)[1]
        if unit:
            found.setdefault(unit, os.path.join(folder, name))
    return found


def plan_children(src, dst, skip=()):
    """Papka ichidagi, nishonda yo'q bolalar: [(nom, manba, nishon)]."""
    rows = []
    if not os.path.isdir(src):
        return rows
    for child in sorted(os.listdir(src)):
        if child in skip:
            continue
        target = os.path.join(dst, child)
        if not os.path.exists(target):
            rows.append((child, os.path.join(src, child), target))
    return rows


def plan(backup, claude):
    """Qaytariladigan ishlar ro'yxati va o'tkazib yuborilganlar sababi."""
    units = backup_entries(backup)
    jobs, skipped = [], []

    for name in WHOLE:
        src = units.get(name)
        if src is None:
            continue
        dst = os.path.join(claude, name)
        if os.path.exists(dst):
            skipped.append((name, "hozir bor, tegilmaydi"))
        else:
            jobs.append(("butun", name, src, dst))

    for name in MERGED_DIRS:
        src = units.get(name)
        if src is None:
            continue
        skip = {OWN_SKILL} if name == "skills" else {
            "%s.md" % a for a in OWN_AGENTS}
        for child, child_src, child_dst in plan_children(
                src, os.path.join(claude, name), skip):
            jobs.append(("bola", "%s/%s" % (name, child), child_src, child_dst))
        for child in sorted(os.listdir(src)) if os.path.isdir(src) else []:
            if child in skip:
                skipped.append(("%s/%s" % (name, child),
                                "o'rnatuvchi boshqaradi"))
            elif os.path.exists(os.path.join(claude, name, child)):
                skipped.append(("%s/%s" % (name, child), "hozir bor"))

    if "settings.json" in units:
        jobs.append(("sozlama", "settings.json", units["settings.json"],
                     os.path.join(claude, "settings.json")))
    return jobs, skipped


def merge_settings_json(backup_path, current_path):
    """Zaxiradagi va hozirgi sozlamani birlashtiradi; hozirgisi ustun.

    `hooks` va `permissions` ichida ham hozirgisi ustun: yangi o'rnatish
    yozgan hook va ruxsat yo'qolmaydi. Zaxiradan faqat HOZIR YO'Q
    bo'lgan kalitlar, hodisalar va ro'yxat elementlari qaytadi.
    """
    old = read_settings(backup_path, must_exist=True)
    now = read_settings(current_path, must_exist=False)

    merged = dict(old)
    merged.update(now)

    old_hooks = old.get("hooks") if isinstance(old.get("hooks"), dict) else {}
    now_hooks = now.get("hooks") if isinstance(now.get("hooks"), dict) else {}
    if old_hooks or now_hooks:
        hooks = {}
        for event in list(now_hooks) + [e for e in old_hooks if e not in now_hooks]:
            hooks[event] = now_hooks.get(event, old_hooks.get(event))
        merged["hooks"] = hooks

    old_perm = old.get("permissions") if isinstance(old.get("permissions"), dict) else {}
    now_perm = now.get("permissions") if isinstance(now.get("permissions"), dict) else {}
    if old_perm or now_perm:
        perm = {}
        for key in list(now_perm) + [k for k in old_perm if k not in now_perm]:
            current, previous = now_perm.get(key), old_perm.get(key)
            if isinstance(current, list) and isinstance(previous, list):
                seen = {json.dumps(i, sort_keys=True) for i in current}
                extra = [i for i in previous
                         if json.dumps(i, sort_keys=True) not in seen]
                perm[key] = current + extra
            else:
                perm[key] = current if key in now_perm else previous
        merged["permissions"] = perm

    old_env = old.get("env") if isinstance(old.get("env"), dict) else {}
    now_env = now.get("env") if isinstance(now.get("env"), dict) else {}
    if old_env or now_env:
        env = dict(old_env)
        env.update(now_env)
        merged["env"] = env
    return merged


def copy(src, dst):
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)


def main(argv=None):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("zaxira", help="zaxira papkasi (.claude-backup-<vaqt>)")
    parser.add_argument("--claude", default="",
                        help="nishon papka, sukut ~/.claude")
    parser.add_argument("--yoz", action="store_true",
                        help="qaytaradi; bersiz faqat ro'yxat")
    args = parser.parse_args(argv)

    if not os.path.isdir(args.zaxira):
        print("zaxira papkasi topilmadi: %s" % args.zaxira)
        return 1
    claude = args.claude or os.path.join(os.path.expanduser("~"), ".claude")

    try:
        jobs, skipped = plan(args.zaxira, claude)
    except OSError as exc:
        print("zaxira o'qilmadi: %s" % exc)
        return 1

    if not jobs:
        print("qaytariladigan narsa yo'q: zaxiradagi birliklar allaqachon joyida")
        for name, why in skipped:
            print("  o'tkazildi: %s (%s)" % (name, why))
        return 0

    for kind, name, _, _ in jobs:
        print("  %s: %s" % ("birlashtiriladi" if kind == "sozlama"
                            else "qaytariladi", name))
    for name, why in skipped:
        print("  o'tkazildi: %s (%s)" % (name, why))

    if not args.yoz:
        print("\n%d birlik (quruq yurish, hech narsa yozilmadi). "
              "Qaytarish uchun --yoz qo'shing." % len(jobs))
        return 0

    for kind, name, src, dst in jobs:
        try:
            if kind == "sozlama":
                merged = merge_settings_json(src, dst)
                write_atomic(dst, render(merged))
            else:
                copy(src, dst)
        except (OSError, SozlamaXato) as exc:
            print("\n%s qaytarilmadi: %s" % (name, exc))
            return 1
    print("\n%d birlik qaytarildi -> %s" % (len(jobs), claude))
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    sys.exit(main())
