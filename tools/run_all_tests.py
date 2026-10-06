#!/usr/bin/env python3
"""Hamma `tools/test_*.py` suite ni parallel yurgizadi (CI va lokal).

    python3 tools/run_all_tests.py           # -j os.cpu_count()
    python3 tools/run_all_tests.py -j 1      # ketma-ket

Avval indeks bir marta yasaladi: CI da `index/` yo'q va bir nechta suite
uni bir vaqtda yasashga urinardi. Keyin suitelar ThreadPoolExecutor bilan
alohida jarayonlarda yuradi. Har suite chiqishi buferda yig'iladi va
fayl nomi tartibida chop etiladi, shuning uchun parallel yurish logni
aralashtirmaydi. Oxirida `yiqilgan:` qatori (bo'lsa) va eng sekin 5 suite.
Chiqish kodi: birorta suite yiqilsa 1.

GitHub Actions da (GITHUB_ACTIONS=true) har suite `::group::` ichida.
"""

import argparse
import concurrent.futures
import glob
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SLOWEST = 5


def build_index():
    """Indeks yo'q yoki eskirgan bo'lsa bir marta yasaydi: (ok, chiqish)."""
    sys.path.insert(0, HERE)
    try:
        import build_index as bi
        if bi.is_fresh():
            return True, b""
    except Exception:  # noqa: BLE001 - yasovchi o'zi xatoni aytadi
        pass
    proc = subprocess.run([sys.executable, os.path.join(HERE, "build_index.py")],
                          cwd=ROOT, stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode == 0, proc.stdout


def run_suite(path, timeout):
    """(rc, chiqish baytlari, soniya). stderr stdout ga qo'shiladi."""
    start = time.perf_counter()
    try:
        proc = subprocess.run([sys.executable, path], cwd=ROOT,
                              stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, timeout=timeout)
        rc, out = proc.returncode, proc.stdout
    except subprocess.TimeoutExpired as exc:
        rc = 124
        out = (exc.output or b"") + ("\nvaqt tugadi: %d s\n" % timeout).encode()
    return rc, out, time.perf_counter() - start


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("-j", type=int, default=os.cpu_count() or 2,
                        help="bir vaqtda nechta suite (standart: yadro soni)")
    parser.add_argument("--timeout", type=int, default=600,
                        help="bitta suite uchun soniya (standart 600)")
    opts = parser.parse_args(argv)

    out = sys.stdout.buffer
    group = os.environ.get("GITHUB_ACTIONS") == "true"
    started = time.perf_counter()
    failed = []

    ok, text = build_index()
    if not ok:
        out.write(b"build_index.py yiqildi:\n" + text)
        failed.append("tools/build_index.py")

    suites = sorted(glob.glob(os.path.join(HERE, "test_*.py")))
    timings = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, opts.j)) as pool:
        futures = [pool.submit(run_suite, path, opts.timeout) for path in suites]
        # Natija tartib bilan: oldingi suite tugamaguncha keyingisi kutadi,
        # lekin hammasi allaqachon parallel yurmoqda.
        for path, future in zip(suites, futures):
            rc, text, seconds = future.result()
            name = "tools/" + os.path.basename(path)
            timings.append((seconds, name))
            head = "::group::%s (%.1f s)" % (name, seconds) if group \
                else "== %s (%.1f s) ==" % (name, seconds)
            out.write(head.encode() + b"\n" + text)
            if text and not text.endswith(b"\n"):
                out.write(b"\n")
            if group:
                out.write(b"::endgroup::\n")
            if rc != 0:
                failed.append(name)
            out.flush()

    lines = ["", "%d suite, %.1f s (-j %d)" % (len(suites), time.perf_counter() - started,
                                              opts.j)]
    lines.append("eng sekin:")
    for seconds, name in sorted(timings, reverse=True)[:SLOWEST]:
        lines.append("  %6.1f s  %s" % (seconds, name))
    if failed:
        lines.append("yiqilgan: %s" % " ".join(failed))
    out.write(("\n".join(lines) + "\n").encode())
    out.flush()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
