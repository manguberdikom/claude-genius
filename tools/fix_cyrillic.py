#!/usr/bin/env python3
"""Lotin so'zlari ichiga tasodifan tushgan kirill harflarini tuzatadi.

Aralash token (lotin + kirill) -> kirill homoglif lotinga almashtiriladi.
To'liq kirill token -> avtomatik tuzatilmaydi, ogohlantirish sifatida chiqariladi.
"""
import re, sys

HOMO = {
    'а':'a','е':'e','о':'o','р':'p','с':'c','у':'y','х':'x','і':'i','ј':'j',
    'ѕ':'s','һ':'h','ԛ':'q','ԝ':'w','ё':'e','и':'i','н':'h','к':'k','м':'m',
    'т':'t','в':'b','г':'r','д':'d','з':'z','л':'l','п':'n','ф':'f','ь':"'",
    'А':'A','В':'B','Е':'E','К':'K','М':'M','Н':'H','О':'O','Р':'P','С':'C',
    'Т':'T','У':'Y','Х':'X','І':'I','Ј':'J','Ѕ':'S','Ё':'E','И':'I','Г':'R',
    'Д':'D','З':'Z','Л':'L','П':'N','Ф':'F','Б':'B','Я':'Ya','Ю':'Yu',
}
CYR = re.compile(r'[Ѐ-ӿԀ-ԯ]')
LAT = re.compile(r'[A-Za-z]')
TOKEN = re.compile(r"[\wЀ-ӿ'’ʻʼ-]+", re.UNICODE)

def fix_text(text):
    fixed = 0
    warn = []
    def repl(m):
        nonlocal fixed
        tok = m.group(0)
        if not CYR.search(tok):
            return tok
        if LAT.search(tok):
            out = ''.join(HOMO.get(ch, ch) for ch in tok)
            if CYR.search(out):
                warn.append(tok)
                return tok
            fixed += 1
            return out
        warn.append(tok)
        return tok
    return TOKEN.sub(repl, text), fixed, warn

def main(paths):
    total_fixed = 0
    all_warn = []
    for p in paths:
        src = open(p, encoding='utf-8').read()
        out, n, warn = fix_text(src)
        if n:
            open(p, 'w', encoding='utf-8').write(out)
            total_fixed += n
            print("%s: %d token tuzatildi" % (p, n))
        for w in warn:
            all_warn.append("%s: %s" % (p, w))
    if all_warn:
        print("\nQO'LDA TEKSHIRISH KERAK (to'liq kirill token):")
        for w in sorted(set(all_warn)):
            print("  " + w)
    print("\nJami tuzatilgan token: %d, ogohlantirish: %d" % (total_fixed, len(set(all_warn))))
    return 1 if all_warn else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
