"""tools/ uchun umumiy yordamchilar: `run_git`, `atomic_write_text`,
`clone_root` va `state_dir`.

Avval bu ikki amal tools/ dagi o'nga yaqin faylda alohida yozilgan edi
(audit/2026-10-05 R7.5): har nusxa o'z timeout i, o'z xato qaytarishi
bilan, ba'zisida tmp faylni tozalash yo'q. Endi bitta joyda, chaqiruvchining
farqlari parametr bilan: timeout, cwd, matn yoki bayt, xatoda nima bo'lishi,
encoding, fsync.

Faqat standart kutubxona, Python 3.8: hook yo'lidagi modullar ham
import qiladi. Yangi yordamchi bu yerga faqat tegadigan fayl ko'chganda
qo'shiladi, hammasi birdan emas.
"""

import os
import re
import subprocess

# Global o'rnatishda o'rnatuvchi settings.json `env` ga klon yo'lini shu
# nom bilan yozadi (R7.8 XV-Y1). Pin qilingan snapshotdan yuradigan hook
# yoziladigan narsani (memory, holat) klonga yo'naltirish uchun shuni o'qiydi.
CLONE_ENV = "GENIUS_CLONE"


def run_git(args, cwd=None, timeout=20, text=True, input=None, env=None,
            strict=False):
    """`git <args>` ni yurgizadi va CompletedProcess qaytaradi.

    git yo'q (OSError) yoki timeout (SubprocessError) bo'lsa `None`:
    chaqiruvchi o'zi hal qiladi (bo'sh qator, False). Chiqish kodi
    tekshirilmaydi, uni chaqiruvchi o'qiydi (`proc.returncode`).

    cwd:     jarayon papkasi; `-C <papka>` kerak bo'lsa args ga yoziladi.
    timeout: soniya, `None` bo'lsa cheksiz.
    text:    True bo'lsa stdout/stderr str, False bo'lsa bytes.
    input:   stdin (text rejimiga mos tur).
    env:     os.environ ustiga qo'shiladigan o'zgaruvchilar.
    strict:  True bo'lsa OSError va SubprocessError `None` bo'lmay ko'tariladi.
    """
    try:
        return subprocess.run(
            ["git"] + list(args), capture_output=True, text=text, cwd=cwd,
            input=input, timeout=timeout,
            env=dict(os.environ, **env) if env else None)
    except (OSError, subprocess.SubprocessError):
        if strict:
            raise
        return None


def atomic_write_text(path, text, encoding="utf-8", newline=None,
                      fsync=False, mtime=None):
    """`text` ni `path` ga atomik yozadi: avval tmp, keyin `os.replace`.

    O'quvchi har doim eski yoki yangi faylni to'liq ko'radi, yarimini
    hech qachon. tmp nomida pid bor: parallel jarayonlar bir tmp faylga
    yozmaydi. Yozish yoki almashtirish yiqilsa tmp o'chiriladi va istisno
    (odatda OSError) o'zgarishsiz ko'tariladi; eski fayl o'z holicha qoladi.
    Papka yaratilmaydi: kerak bo'lsa chaqiruvchi `os.makedirs` qiladi.

    encoding: fayl kodlashi (sukut UTF-8).
    newline:  `open(newline=...)` ga o'tadi; `"\\n"` Windows da CRLF ni
              oldini oladi, `None` bo'lsa platforma sukuti.
    fsync:    True bo'lsa almashtirishdan oldin diskka yoziladi (elektr
              uzilishida ham fayl butun).
    mtime:    berilsa almashtirishdan oldin tmp ga qo'yiladi (indeks
              mtime i manba bilan tengligi uchun).
    """
    tmp = "%s.%d.tmp" % (path, os.getpid())
    try:
        with open(tmp, "w", encoding=encoding, newline=newline) as handle:
            handle.write(text)
            if fsync:
                handle.flush()
                os.fsync(handle.fileno())
        if mtime is not None:
            os.utime(tmp, (mtime, mtime))
        os.replace(tmp, path)
    except BaseException:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


SNAPSHOT_NAME = re.compile(r"^[0-9a-f]{12}\Z")


def is_snapshot(root):
    """`root` pin qilingan snapshotmi: `<claude-dir>/genius/<12 hex>`.

    O'rnatuvchi snapshotni aynan shu joyda yasaydi (install/snapshot.py).
    Klonning o'zi va uning worktree lari (`.claude/worktrees/genius-<id>`)
    shu shaklga tushmaydi."""
    path = os.path.abspath(root).replace("\\", "/").rstrip("/")
    parts = path.split("/")
    return (len(parts) >= 3 and bool(SNAPSHOT_NAME.match(parts[-1]))
            and parts[-2] == "genius" and parts[-3] == ".claude")


def clone_root(root):
    """Yoziladigan narsalar turadigan klon: `GENIUS_CLONE`, aks holda `root`.

    Global o'rnatishda hooklar klonning ishchi daraxtidan emas, aniq commit
    dagi snapshotdan (`~/.claude/genius/<sha12>/`) yuradi, shuning uchun
    asbobning `ROOT` i snapshot. Snapshot faqat o'qiladi (docs, index,
    GLOSSARY, tools) va yangilashda almashadi; memory (klon reposi bilan
    push qilinadi) va holat papkasi esa shu yerdan, klondan olinadi.
    `GENIUS_CLONE` faqat `root` snapshot bo'lsa (`is_snapshot`) olinadi:
    global o'rnatilgan mashinada u hamma sessiya muhitida turadi, klonning
    o'zida yoki uning worktree sida ishlayotgan hook esa o'z daraxtini
    `root` deb bilishi va holat bilan memoryni asosiy klonga yozmasligi shart.
    Qiymat mavjud mutlaq papka bo'lmasa ham e'tiborga olinmaydi: buzuq qiymat
    hookni yiqitmasin. Har chaqiruvda o'qiladi, import paytida emas.
    """
    given = os.environ.get(CLONE_ENV, "").strip()
    if (given and is_snapshot(root) and os.path.isabs(given)
            and os.path.isdir(given)):
        return os.path.normpath(given)
    return root


def state_dir(root):
    """Holat papkasi: `GENIUS_STATE_DIR`, aks holda klondagi `.claude/.state`.

    Klon (`clone_root`) snapshot almashganda yo'qolmaydi, shuning uchun
    budjet, belgilar va jurnal yangilashdan keyin ham qoladi.
    """
    return (os.environ.get("GENIUS_STATE_DIR")
            or os.path.join(clone_root(root), ".claude", ".state"))
