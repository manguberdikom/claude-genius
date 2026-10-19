#!/usr/bin/env python3
"""review_status.py --imzo uchun sinov: navbat boshidagi boblar imzolanadi,
qolgan qator va izohlar o'zgarmaydi.

    python3 tools/test_review_status.py
"""

import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import review_status as R  # noqa: E402

REVIEW = ("# izoh\nhujjat\tbob\tholat\tsana\ttekshiruvchi\tmanbalar\txatolar\tizoh\n"
          "testing\t1\ttekshirilmoqda\t2026-10-17\tsessiya\t3\t0\tx\n"
          "testing\t2\ttekshirilmoqda\t2026-10-17\tsessiya\t3\t0\tx\n"
          "testing\t3\tai-draft\t2026-10-17\tsessiya\t0\t0\tx\n")
QUEUE = ("# navbat\ntartib\tvazn\thujjat\tbob\tholat\n"
         "1\t5.0\ttesting\t2\ttekshirilmoqda\n2\t4.0\ttesting\t3\tai-draft\n"
         "3\t3.0\ttesting\t1\ttekshirilmoqda\n")


def main():
    tmp = tempfile.mkdtemp(prefix="review-status-")
    try:
        review, queue = os.path.join(tmp, "review.tsv"), os.path.join(tmp, "queue.tsv")
        for path, text in ((review, REVIEW), (queue, QUEUE)):
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text)
        keys = R.queue_head(2, queue)
        R.sign(set(keys), "2026-10-19", review)
        rows = R.read_review(review)
        with open(review, encoding="utf-8") as handle:
            text = handle.read()
        checks = [
            ("navbat tartibi bo'yicha", keys == [("testing", "2"), ("testing", "3")]),
            ("imzolangan: holat, sana, odam",
             all(rows[k]["holat"] == "tekshirilgan" and rows[k]["sana"] == "2026-10-19"
                 and rows[k]["tekshiruvchi"] == "odam" for k in keys)),
            ("navbatdan tashqaridagi bob tegilmadi",
             rows[("testing", "1")]["holat"] == "tekshirilmoqda"),
            ("izoh va oxirgi qator saqlandi", text.startswith("# izoh\n") and text.endswith("\n")),
        ]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    failures = 0
    for name, ok in checks:
        failures += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", name))
    print("\n%d/%d o'tdi" % (len(checks) - failures, len(checks)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
