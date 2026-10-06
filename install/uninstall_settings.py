#!/usr/bin/env python3
"""~/.claude/settings.json dan manguberdi yozuvlarini olib tashlaydi.

    python3 install/uninstall_settings.py <settings.json> --root <klon-yo'li>
    python3 install/uninstall_settings.py <settings.json> --root <klon> --yoz

Nega alohida skript: olib tashlash o'rnatishning teskarisi va "o'zniki"
qoidasi aynan bir xil bo'lishi kerak, aks holda o'rnatuvchi yozgan
yozuvning bir qismi qolib ketardi. Shuning uchun qoida ikki joyda
yozilmaydi: `is_own_hook` va `is_own_rule` merge_settings.py dan
olinadi.

Nega PowerShell da emas: PowerShell 5.1 da ConvertFrom-Json PSCustomObject
beradi, uni o'zgartirish uchun butun daraxt qayta qurilishi kerak va
bitta elementli massiv skalyarga aylanib ketadi. U qism agent sessiyasida
sinalmaydi ham. Bu yerda esa sinaladi: tools/test_uninstall_settings.py.

Nima olinadi:
- `hooks`: buyrug'ida `<root>/tools/` bor hooklar; shundan bo'shab qolgan
  guruh va bo'shab qolgan hodisa ham tushadi;
- `permissions.allow`, `ask` va `deny`: shu ildizga tegishli qoidalar
  (merge_settings bilan bir xil qoida);
- `permissions.additionalDirectories`: shu ildizning o'zi va `<root>/`
  ostidagi yozuvlar (`<root>/docs`, `<root>/memory`);
- `env.GENIUS_PYTHON`, va `env` shundan bo'shab qolsa `env` ham.

Begona yozuvlarga tegilmaydi: boshqa klonning (`<root>-eski`) hooki ham
begona, chunki `is_own_rule` ildizdan keyin yo'l davom etmasligini
talab qiladi.

Ildiz MAVJUD BO'LISHI SHART EMAS: klon o'chirilgan yoki ko'chirilgan
bo'lsa ham yozuvlar settings.json da qolgan bo'ladi. Shuning uchun yo'l
oddiy satr sifatida solishtiriladi, `realpath` qilinmaydi.
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from merge_settings import (RULE_LISTS, SozlamaXato, is_own_dir,  # noqa: E402
                            is_own_hook, is_own_rule, norm_root,
                            read_settings, render, section, write_atomic)


def strip_hooks(hooks, root, stats):
    """O'z hooklari olib tashlangan `hooks`. Bo'shab qolgani tushadi."""
    out = {}
    for event, groups in hooks.items():
        if not isinstance(groups, list):
            out[event] = groups          # notanish shakl: begona
            continue
        kept_groups = []
        for group in groups:
            inner = group.get("hooks") if isinstance(group, dict) else None
            if not isinstance(inner, list):
                kept_groups.append(group)
                continue
            kept = [h for h in inner if not is_own_hook(h, root)]
            stats["hook"] += len(inner) - len(kept)
            if inner and not kept:
                continue                 # faqat o'z hooklari bor edi
            kept_groups.append(dict(group, hooks=kept)
                               if len(kept) != len(inner) else group)
        if kept_groups:
            out[event] = kept_groups
    return out


def strip(data, root):
    """(yangi sozlama, sanoq). `data` o'zgarmaydi."""
    root = norm_root(root)
    stats = {"hook": 0, "ruxsat": 0, "papka": 0, "env": 0}
    hooks = strip_hooks(section(data, "hooks", dict, "mavjud"), root, stats)

    permissions = {}
    for key, value in section(data, "permissions", dict, "mavjud").items():
        if key in RULE_LISTS and isinstance(value, list):
            kept = [r for r in value if not is_own_rule(r, root)]
            stats["ruxsat"] += len(value) - len(kept)
            permissions[key] = kept
        elif key == "additionalDirectories" and isinstance(value, list):
            kept = [d for d in value if not is_own_dir(d, root)]
            stats["papka"] = len(value) - len(kept)
            permissions[key] = kept
        else:
            permissions[key] = value

    env = dict(section(data, "env", dict, "mavjud"))
    if "GENIUS_PYTHON" in env:
        del env["GENIUS_PYTHON"]
        stats["env"] = 1

    out = {}
    for key, value in data.items():
        if key == "hooks":
            if hooks:
                out[key] = hooks
        elif key == "permissions":
            if permissions:
                out[key] = permissions
        elif key == "env":
            if env:
                out[key] = env
        else:
            out[key] = value
    return out, stats


def summary(stats, existed):
    if not existed:
        return "settings.json yo'q, olib tashlashga narsa yo'q"
    parts = []
    if stats["hook"]:
        parts.append("%d hook" % stats["hook"])
    if stats["ruxsat"]:
        parts.append("%d ruxsat" % stats["ruxsat"])
    if stats["papka"]:
        parts.append("%d additionalDirectories yozuvi" % stats["papka"])
    if stats["env"]:
        parts.append("env.GENIUS_PYTHON")
    if not parts:
        return "shu ildizga tegishli yozuv topilmadi, fayl o'zgarmaydi"
    return ", ".join(parts) + " olib tashlandi, begona yozuvlar qoldi"


def main(argv=None):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("sozlama", help="~/.claude/settings.json")
    parser.add_argument("--root", required=True,
                        help="klon yo'li; mavjud bo'lishi shart emas")
    parser.add_argument("--yoz", action="store_true",
                        help="faylga yozadi; bersiz faqat xulosa")
    args = parser.parse_args(argv)

    # Bo'sh yoki faqat slashli ildiz hamma `/tools/` yo'lini o'zniki deb
    # o'qib, begona klonning hooklarini ham olib tashlardi.
    if not norm_root(args.root.strip()).strip("/"):
        print("olib tashlanmadi: --root bo'sh yoki faqat slash")
        return 1
    try:
        existed = os.path.exists(args.sozlama)
        data = read_settings(args.sozlama, must_exist=False)
        stripped, stats = strip(data, args.root)
    except SozlamaXato as exc:
        print("olib tashlanmadi: %s" % exc)
        return 1

    line = summary(stats, existed)
    if not args.yoz:
        print("settings.json (quruq, yozilmadi): %s" % line)
        return 0
    if not existed:
        print("settings.json: %s" % line)
        return 0
    try:
        write_atomic(args.sozlama, render(stripped))
    except OSError as exc:
        print("settings.json yozilmadi: %s (%s)" % (args.sozlama, exc))
        return 1
    print("settings.json: %s" % line)
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    sys.exit(main())
