#!/usr/bin/env python3
"""Sonar serverdan issue, quality gate, coverage va hotspot olish (faqat o'qish).

    python3 tools/sonar_fetch.py issues  [--loyiha KEY] [--chiqish fayl.tsv]
    python3 tools/sonar_fetch.py gate    [--loyiha KEY]
    python3 tools/sonar_fetch.py coverage [--loyiha KEY]
    python3 tools/sonar_fetch.py hotspots [--loyiha KEY]

issues    - ochiq issue lar TSV: kalit, daraja, tur, fayl, qator, xabar.
gate      - quality gate holati va har shart (metrika, taqqoslash, chegara, qiymat).
coverage  - fayl bo'yicha uncovered_lines va uncovered_conditions (TSV), eng
            ko'pidan boshlab; qoplanmagani yo'q fayl chiqmaydi.
hotspots  - TO_REVIEW holatdagi security hotspot lar TSV.

Sozlama (qiymat kodda yo'q, muhitdan):

    GENIUS_SONAR_URL         sukut https://sonar.mbabm.uz
    GENIUS_SONAR_PROJECT     project key (yoki --loyiha)
    GENIUS_SONAR_TOKEN_FILE  token fayli yo'li, sukut ~/.sonar-token.txt

Token QIYMATI hech qayerga chop etilmaydi, logga va xatoga tushmaydi: fayl
birinchi qatori o'qiladi va `-u token:` (Basic, parolsiz) sifatida yuboriladi.
Asbob hech narsani o'zgartirmaydi: hotspot ni SAFE qilish va issue ni
Accept/won't fix qilish bu yerda yo'q va foydalanuvchi roziligisiz bajarilmaydi.
Chiqish kodi: 0 yaxshi, 2 sozlama yo'q (token, loyiha), 3 tarmoq yoki server xatosi.
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_URL = "https://sonar.mbabm.uz"
PAGE = 500
MAX_PAGES = 40   # Sonar o'zi 10 000 elementdan oshirmaydi


class Config(Exception):
    pass


class Network(Exception):
    pass


def token_path():
    given = os.environ.get("GENIUS_SONAR_TOKEN_FILE", "").strip()
    return os.path.expanduser(given or "~/.sonar-token.txt")


def read_token(path=None):
    path = path or token_path()
    try:
        with open(path, encoding="utf-8") as handle:
            token = handle.readline().strip()
    except OSError:
        raise Config("token fayli o'qilmadi: %s (GENIUS_SONAR_TOKEN_FILE)" % path)
    if not token:
        raise Config("token fayli bo'sh: %s" % path)
    return token


def base_url():
    return os.environ.get("GENIUS_SONAR_URL", "").strip().rstrip("/") or DEFAULT_URL


def http_get(url, token):
    """JSON javob (dict). Token faqat Authorization sarlavhasida."""
    auth = base64.b64encode((token + ":").encode("utf-8")).decode("ascii")
    request = urllib.request.Request(url, headers={"Authorization": "Basic " + auth})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        raise Network("HTTP %d: %s" % (err.code, url.split("?")[0]))
    except (urllib.error.URLError, OSError, ValueError) as err:
        raise Network("%s: %s" % (type(err).__name__, url.split("?")[0]))


def pages(path, params, token, key):
    """Sahifalab `key` ro'yxatini yig'adi."""
    out = []
    for number in range(1, MAX_PAGES + 1):
        query = dict(params, p=number, ps=PAGE)
        data = http_get("%s%s?%s" % (base_url(), path, urllib.parse.urlencode(query)),
                        token)
        out.extend(data.get(key, []))
        total = (data.get("paging") or {}).get("total", data.get("total", len(out)))
        if len(out) >= total or not data.get(key):
            break
    return out


def clean(text):
    return " ".join(str(text).split())


def file_of(component):
    return component.split(":", 1)[1] if ":" in component else component


def issues(project, token):
    rows = pages("/api/issues/search",
                 {"componentKeys": project, "resolved": "false",
                  "statuses": "OPEN,CONFIRMED,REOPENED"}, token, "issues")
    lines = ["kalit\tdaraja\ttur\tfayl\tqator\txabar"]
    for item in sorted(rows, key=lambda i: (i.get("rule", ""), i.get("component", ""),
                                            i.get("line") or 0)):
        lines.append("\t".join([
            item.get("rule", ""), item.get("severity", ""), item.get("type", ""),
            file_of(item.get("component", "")), str(item.get("line") or ""),
            clean(item.get("message", ""))]))
    return lines


def gate(project, token):
    data = http_get("%s/api/qualitygates/project_status?%s" % (
        base_url(), urllib.parse.urlencode({"projectKey": project})), token)
    status = data.get("projectStatus", {})
    lines = ["holat\t%s" % status.get("status", "?"),
             "metrika\tshart\tchegara\tqiymat\tnatija"]
    for cond in status.get("conditions", []):
        lines.append("\t".join([
            cond.get("metricKey", ""), cond.get("comparator", ""),
            str(cond.get("errorThreshold", "")), str(cond.get("actualValue", "")),
            cond.get("status", "")]))
    return lines


def coverage(project, token):
    rows = pages("/api/measures/component_tree",
                 {"component": project, "qualifiers": "FIL", "strategy": "leaves",
                  "metricKeys": "uncovered_lines,uncovered_conditions"},
                 token, "components")
    found = []
    for comp in rows:
        values = {m["metric"]: int(float(m.get("value", 0)))
                  for m in comp.get("measures", [])}
        lines_, conds = values.get("uncovered_lines", 0), values.get("uncovered_conditions", 0)
        if lines_ or conds:
            found.append((lines_, conds, comp.get("path") or file_of(comp.get("key", ""))))
    found.sort(key=lambda r: (-r[0], -r[1], r[2]))
    return ["fayl\tuncovered_lines\tuncovered_conditions"] + [
        "%s\t%d\t%d" % (path, a, b) for a, b, path in found]


def hotspots(project, token):
    rows = pages("/api/hotspots/search",
                 {"projectKey": project, "status": "TO_REVIEW"}, token, "hotspots")
    lines = ["kalit\tximoya\tfayl\tqator\txabar"]
    for item in sorted(rows, key=lambda h: (h.get("component", ""), h.get("line") or 0)):
        lines.append("\t".join([
            item.get("ruleKey", ""), item.get("vulnerabilityProbability", ""),
            file_of(item.get("component", "")), str(item.get("line") or ""),
            clean(item.get("message", ""))]))
    return lines


COMMANDS = {"issues": issues, "gate": gate, "coverage": coverage, "hotspots": hotspots}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("buyruq", choices=sorted(COMMANDS))
    parser.add_argument("--loyiha", help="project key (sukut GENIUS_SONAR_PROJECT)")
    parser.add_argument("--chiqish", help="natijani shu faylga yozish")
    args = parser.parse_args(argv)
    try:
        project = args.loyiha or os.environ.get("GENIUS_SONAR_PROJECT", "").strip()
        if not project:
            raise Config("project key yo'q: --loyiha yoki GENIUS_SONAR_PROJECT")
        lines = COMMANDS[args.buyruq](project, read_token())
    except Config as err:
        print("sonar_fetch: %s" % err, file=sys.stderr)
        return 2
    except Network as err:
        print("sonar_fetch: tarmoq/server xatosi (%s)" % err, file=sys.stderr)
        return 3
    text = "\n".join(lines) + "\n"
    if args.chiqish:
        with open(args.chiqish, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        print("sonar_fetch: %d qator -> %s" % (len(lines) - 1, args.chiqish))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
