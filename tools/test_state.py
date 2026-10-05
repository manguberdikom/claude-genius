#!/usr/bin/env python3
"""state.py uchun sinovlar.

    python3 tools/test_state.py

Eng muhimi parallel belgilash: bir vaqtda yurgan rules_for chaqiruvlari
bir-birining belgisini o'chirmasligi kerak. Avval hamma belgi bitta JSON
da edi va o'qish-o'zgartirish-yozish poygasida 20 jarayondan 14-20 tasining
belgisi yo'qolardi, check_code esa keyin yolg'on to'sardi.

Holat vaqtinchalik papkada: jonli sessiyaning belgilariga tegilmaydi.
"""

import multiprocessing
import os
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import state  # noqa: E402

WORKERS = 20


def use(folder):
    """state modulini shu papkaga yo'naltiradi (jarayon ichida)."""
    state.STATE_DIR = folder
    state.MARKS = os.path.join(folder, "rules_for")
    state.LEGACY_LOG = os.path.join(folder, "rules_for.json")


def worker(folder, path, barrier):
    use(folder)
    barrier.wait()
    state.mark([path], ["sinov"])


def report(rows):
    bad = 0
    for label, ok in rows:
        bad += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", label))
    return bad


def main():
    failures = total = 0
    folder = tempfile.mkdtemp(prefix="genius-state-")
    work = tempfile.mkdtemp(prefix="genius-work-")
    here = os.getcwd()
    try:
        use(folder)

        print("== Kalit ==")
        target = os.path.join(work, "src", "A.java")
        os.makedirs(os.path.dirname(target))
        open(target, "w").close()
        link = os.path.join(work, "havola")
        try:
            os.symlink(os.path.join(work, "src"), link)
        except (OSError, NotImplementedError):
            link = None   # Windows da symlink huquqi bo'lmasligi mumkin
        os.chdir(work)
        state.mark([os.path.join("src", "A.java")], ["tranzaksiya"])
        os.chdir(here)
        rows = [
            # rules_for boshqa proyektdan nisbiy yo'l bilan chaqiriladi,
            # hook esa mutlaq yo'l beradi: ikkalasi bitta belgi.
            ("nisbiy yo'l mutlaq yo'lga mos", state.was_marked(target)),
            ("symlink orqali ham mos",
             link is None or state.was_marked(os.path.join(link, "A.java"))),
            ("boshqa fayl belgilanmagan",
             not state.was_marked(os.path.join(work, "src", "B.java"))),
            ("belgilar saqlanadi", state.marked_labels(target) == {"tranzaksiya"}),
            ("belgisiz faylda None",
             state.marked_labels(os.path.join(work, "B.java")) is None),
        ]
        failures += report(rows)
        total += len(rows)

        print("\n== Muddat ==")
        old = time.time() - state.MAX_AGE - 60
        os.utime(state._marker(target), (old, old))
        expired = not state.was_marked(target)
        state.mark([os.path.join(work, "C.java")])
        rows = [
            ("eskirgan belgi amal qilmaydi", expired),
            ("eskirgan belgi keyingi mark da o'chadi",
             not os.path.exists(state._marker(target))),
        ]
        failures += report(rows)
        total += len(rows)

        print("\n== Parallel belgilash ==")
        paths = [os.path.join(work, "P%02d.java" % i) for i in range(WORKERS)]
        barrier = multiprocessing.Barrier(WORKERS)
        procs = [multiprocessing.Process(target=worker, args=(folder, p, barrier))
                 for p in paths]
        for proc in procs:
            proc.start()
        for proc in procs:
            proc.join(30)
        lost = [p for p in paths if not state.was_marked(p)]
        rows = [("%d jarayondan hech biri yo'qolmadi%s"
                 % (WORKERS, "" if not lost else " (yo'qoldi: %d)" % len(lost)),
                 not lost)]
        failures += report(rows)
        total += len(rows)

        print("\n== Tozalash va muhit ==")
        with open(state.LEGACY_LOG, "w") as handle:
            handle.write("{}")
        state.clear()
        probe = subprocess.run(
            [sys.executable, "-c", "import state; print(state.MARKS)"],
            capture_output=True, text=True, cwd=HERE,
            env=dict(os.environ, GENIUS_STATE_DIR=folder))
        rows = [
            ("clear belgilarni o'chiradi", not state.was_marked(paths[0])),
            ("clear eski JSON ni ham o'chiradi", not os.path.exists(state.LEGACY_LOG)),
            ("GENIUS_STATE_DIR holat papkasini almashtiradi",
             probe.stdout.strip() == os.path.join(folder, "rules_for")),
        ]
        failures += report(rows)
        total += len(rows)
    finally:
        os.chdir(here)
        shutil.rmtree(folder, ignore_errors=True)
        shutil.rmtree(work, ignore_errors=True)

    print("\n%d/%d o'tdi" % (total - failures, total))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
