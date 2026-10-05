#!/usr/bin/env bash
# docs/ ga tez kirish: indeks kerakli bo'limni topadi, sed faqat o'sha
# satrlarni chiqaradi. Bob fayllari 68k tokengacha boradi, bitta bo'lim esa
# ~700 token, shuning uchun qidiruv bob emas, bo'lim darajasida ishlaydi.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IDX="$ROOT/index"
SECTIONS="$IDX/sections.tsv"
CHAPTERS="$IDX/chapters.tsv"
ALIASES="$IDX/aliases.tsv"
DOCS="$IDX/docs.tsv"
RULES="$IDX/rules.tsv"
CHECKLIST="$IDX/checklist.tsv"
# build_index.py uni hamma fayldan keyin yozadi, vaqti build boshlangan payt.
STAMP="$IDX/.stamp"

# show uchun chegara: satr yoki bayt bo'yicha uzun blok tasodifan
# kontekstni to'ldirmasin. Bob satrlari uzun (1096 satrlik bob 138 KB),
# shuning uchun satr chegarasining o'zi deyarli hech qachon ishlamaydi.
# Eng katta bo'lim ~6 KB: bayt chegarasi faqat bobni to'sadi. Qiymat va
# o'zgaruvchi guard.py dagi Read chegarasi bilan bir xil.
MAX_LINES="${DOC_MAX_LINES:-1200}"
MAX_BYTES="${DOC_MAX_BYTES:-16000}"
LIMIT_DEFAULT=20
RULE_LIMIT=8

die() { printf '%s\n' "$*" >&2; exit 1; }

# Python nom bo'yicha emas, ishga tushirib tanlanadi: Windows da PATH dagi
# python3 ko'pincha WindowsApps stub'i, u bor, lekin hech narsa yurgizmaydi.
# Git Bash va python.org juftligida esa python3 umuman yo'q, faqat python.
# GENIUS_PYTHON ni o'rnatuvchi settings.json env ga yozadi.
pick_python() {
  local c
  for c in "${GENIUS_PYTHON:-}" python3 python py; do
    [ -n "$c" ] || continue
    if "$c" -c 'import sys' >/dev/null 2>&1; then
      printf '%s\n' "$c"
      return 0
    fi
  done
  return 1
}

rebuild() {
  local py
  py="$(pick_python)" || die "ishlaydigan Python topilmadi (GENIUS_PYTHON bilan ko'rsating)"
  "$py" "$ROOT/tools/build_index.py" >&2
}

# Indeks yo'q, chala yoki biror manbadan eski bo'lsa qayta yasaladi.
# Eskirgan indeks noto'g'ri satr raqami beradi, bu jim xato bo'lar edi.
# Manba build_index.py ning o'zi ham: unga yangi fayl yoki ustun qo'shilsa,
# eski klon pull dan keyin indeksni o'zi yangilaydi. Shart
# build_index.is_fresh() bilan bir xil.
ensure_index() {
  local f
  for f in "$STAMP" "$SECTIONS" "$CHAPTERS" "$ALIASES" "$DOCS" "$RULES" "$CHECKLIST"; do
    [ -f "$f" ] || { rebuild; return; }
  done
  if [ -n "$(find "$ROOT/docs" "$ROOT/tools/build_index.py" \
      \( -name '*.md' -o -name manifest.json -o -name build_index.py \) \
      -newer "$STAMP" -print -quit)" ]; then
    printf 'indeks eskirgan, qayta yasalmoqda...\n' >&2
    rebuild
  fi
}

# ---------------------------------------------------------------- find

cmd_find() {
  local full=0 limit=$LIMIT_DEFAULT
  local -a words=()
  # Bayroq so'rovdan oldin ham, keyin ham kelishi mumkin.
  while [ $# -gt 0 ]; do
    case "$1" in
      -f|--full)  full=1; shift ;;
      -n|--limit)
        [ $# -ge 2 ] || die "-n dan keyin raqam kerak"
        case "$2" in ''|*[!0-9]*) die "-n musbat butun son bo'lishi kerak: $2" ;; esac
        limit=$((10#$2))   # 10#: 08 oktal son deb o'qilmasin
        [ "$limit" -gt 0 ] || die "-n musbat butun son bo'lishi kerak: $2"
        shift 2 ;;
      --)         shift; words+=("$@"); break ;;
      -?*)        die "noma'lum bayroq: $1  (so'rov bo'lsa: doc.sh find -- $1)" ;;
      *)          words+=("$1"); shift ;;
    esac
  done
  [ ${#words[@]} -gt 0 ] || die "foydalanish: doc.sh find [-f] [-n N] [--] <so'rov>"
  local query="${words[*]}"
  # Korpus faqat ASCII apostrof ishlatadi, telefon va Word klaviaturasi esa
  # boshqasini qo'yadi. Har belgi alohida almashtiriladi: [...] ifodasi
  # locale ga bog'liq.
  local apos="'" a
  for a in 'ʻ' '’' '‘' 'ʼ'; do query="${query//"$a"/$apos}"; done
  [ -n "${query//[[:space:]]/}" ] || die "bo'sh so'rov: doc.sh find [-f] [-n N] [--] <so'rov>"

  # Uch bosqich: inglizcha taxalluslar (eng aniq urinish), bo'lim
  # sarlavhalari, bob sarlavhalari. Izoh shu yerda, chunki bash 3.2 (macOS
  # standarti) buyruq o'rnidagi izohni sintaksis deb o'qiydi. Kichik harfga
  # awk o'tkazadi: bash dagi kengaytmasi bash 4 talab qiladi. Ishora-yozuv
  # (sections.tsv 9-ustuni) to'liq yozuv raqami bilan belgilanadi.
  local raw
  raw="$(
    awk -F'\t' -v q="$query" 'BEGIN { q = tolower(q) }
      NR>1 && index(tolower($1), q) { print $2"\t"$4"\t"$1" [taxallus]" }' "$ALIASES"
    awk -F'\t' -v q="$query" 'BEGIN { q = tolower(q) }
      NR>1 && index(tolower($4), q) {
        print $1"\t"$2"\t"$4 ($9 != "" ? " [ishora: "$9"]" : "") }' "$SECTIONS"
    awk -F'\t' -v q="$query" 'BEGIN { q = tolower(q) }
      NR>1 && $2 != "" && index(tolower($3), q) { print $1"\t"$2"\t"$3 }' "$CHAPTERS"
  )"

  if [ "$full" -eq 1 ]; then
    raw="$raw
$(fulltext "$query")"
  fi

  local out
  out="$(printf '%s\n' "$raw" | awk -F'\t' 'NF && !seen[$1"\t"$2]++')"

  if [ -z "$out" ]; then
    printf 'topilmadi: %s\n' "$query" >&2
    [ "$full" -eq 1 ] || printf 'kengroq qidirish: doc.sh find -f %q\n' "$query" >&2
    return 1
  fi

  local total
  total="$(printf '%s\n' "$out" | wc -l)"
  # head emas: u N satrdan keyin chiqib ketadi, printf SIGPIPE oladi va
  # katta natijada (find -f spring) pipefail skriptni 141 bilan to'xtatadi.
  printf '%s\n' "$out" | awk -F'\t' -v n="$limit" 'NR <= n {
    printf "%-11s %-7s %s\n", $1, $2, $3
  }'
  if [ "$total" -gt "$limit" ]; then
    printf "... yana %d ta ('-n %d' bilan ko'proq)\n" \
      "$((total - limit))" "$((limit * 3))" >&2
  fi
  printf "> doc.sh show <hujjat> <raqam>\n" >&2
}

# To'liq matn qidiruvi: topilgan satrni egasi bo'lgan bo'limga bog'laydi.
# grep hech narsa topmasa 1 qaytaradi, bu xato emas, shuning uchun yutiladi.
fulltext() {
  local query="$1"
  # awk bloki single-quote ichida, shuning uchun u yerda apostrof ishlatilmaydi.
  # lo/hi: bir faylning bo'limlari indeksda ketma-ket turadi, shuning uchun
  # har topilgan satr uchun 3293 ta emas, faqat shu fayl bo'limlari ko'riladi.
  # Oxirgi sort: topilish soni ko'p bo'lim yuqorida turadi.
  { cd "$ROOT" && grep -rnFi --include='*.md' -- "$query" docs || true; } \
    | cut -d: -f1,2 \
    | awk -F'\t' '
        NR==FNR {
          if (FNR > 1) {
            n++; doc[n]=$1; num[n]=$2; title[n]=$4
            file[n]=$5; st[n]=$6; en[n]=$7
            if (!(file[n] in lo)) lo[file[n]] = n
            hi[file[n]] = n
          }
          next
        }
        {
          p = index($0, ":")
          f = substr($0, 1, p - 1)
          if (!(f in lo)) next
          l = substr($0, p + 1) + 0
          for (i = lo[f]; i <= hi[f]; i++)
            if (l >= st[i] && l <= en[i]) { hits[i]++; break }
        }
        END {
          for (i in hits)
            print hits[i]"\t"doc[i]"\t"num[i]"\t"title[i]
        }
      ' "$SECTIONS" - \
    | sort -t$'\t' -k1,1nr \
    | awk -F'\t' '{ print $2"\t"$3"\t"$4" ("$1" marta)" }'
}

# ---------------------------------------------------------------- show

cmd_show() {
  local force=0
  while [ $# -gt 0 ]; do
    case "$1" in
      --force) force=1; shift ;;
      *) break ;;
    esac
  done
  [ $# -eq 2 ] || die "foydalanish: doc.sh show [--force] <hujjat> <raqam>"
  local doc="$1" ref="$2" row
  # `2.*` (bobning hamma bo'limi) bob so'rovining o'zi: agentlar shunday yozadi.
  case "$ref" in *.\*) ref="${ref%.\*}" ;; esac

  # Bo'lim raqami satr sifatida solishtiriladi (r""): maydon ham, -v qiymat
  # ham son ko'rinishida, awk ularni son deb oladi va 24.10 == 24.1 chiqadi.
  # Bob raqami butun son, u yerda son solishtiruvi 01 ni ham qabul qiladi.
  if [[ "$ref" == *.* ]]; then
    row="$(awk -F'\t' -v d="$doc" -v r="$ref" \
      'NR>1 && $1==d && $2==r"" { print $5"\t"$6"\t"$7"\t"$4; exit }' "$SECTIONS")"
  else
    row="$(awk -F'\t' -v d="$doc" -v r="$ref" \
      'NR>1 && $1==d && $2==r { print $4"\t"$5"\t"$6"\t"$3; exit }' "$CHAPTERS")"
  fi
  [ -n "$row" ] || die "topilmadi: $doc $ref  (doc.sh toc $doc bilan tekshiring)"

  local file start end title
  IFS=$'\t' read -r file start end title <<< "$row"

  local span=$((end - start + 1))
  local bytes=$(( $(sed -n "${start},${end}p;${end}q" "$ROOT/$file" | wc -c) ))
  if { [ "$span" -gt "$MAX_LINES" ] || [ "$bytes" -gt "$MAX_BYTES" ]; } \
      && [ "$force" -eq 0 ]; then
    printf '%s %s - %s\n' "$doc" "$ref" "$title" >&2
    printf '%d satr, %d bayt (chegara %d satr, %d bayt). Ichidagi bo%slimlar:\n\n' \
      "$span" "$bytes" "$MAX_LINES" "$MAX_BYTES" "'" >&2
    cmd_outline "$doc" "$ref"
    printf "\nto'liq chiqarish: doc.sh show --force %s %s\n" "$doc" "$ref" >&2
    return 1
  fi
  sed -n "${start},${end}p;${end}q" "$ROOT/$file"
}

# ---------------------------------------------------------------- toc / outline / path

cmd_toc() {
  if [ $# -eq 0 ]; then
    awk -F'\t' 'NR>1 { printf "%-11s %3s bob %5s bo%slim  %s\n", $1, $5, $6, "'"'"'", $2 }' "$DOCS"
    return
  fi
  awk -F'\t' -v d="$1" 'NR>1 && $1==d { printf "%-7s %s\n", $2, $3 }' "$CHAPTERS" \
    | grep . || die "hujjat topilmadi: $1  (doc.sh toc bilan ro'yxatni ko'ring)"
}

cmd_outline() {
  [ $# -ge 1 ] || die "foydalanish: doc.sh outline <hujjat> [bob]"
  local doc="$1" chapter="${2:-}"
  awk -F'\t' -v d="$doc" -v c="$chapter" \
    'NR>1 && $1==d && (c=="" || $3==c) { printf "%-11s %-7s %s\n", $1, $2, $4 }' \
    "$SECTIONS" | grep . || die "topilmadi: $doc ${chapter:-}"
}

# Sonar qoida kalitidan uni tushuntirgan bo'limga. Kalit `java:S3776`,
# `S3776` yoki `3776` shaklida berilishi mumkin.
cmd_rule() {
  local all=0
  while [ $# -gt 0 ]; do
    case "$1" in
      --all) all=1; shift ;;
      *) break ;;
    esac
  done
  [ $# -eq 1 ] || die "foydalanish: doc.sh rule [--all] <kalit>   masalan java:S3776"
  local digits key
  digits="$(printf '%s' "$1" | tr -cd '0-9')"
  [ -n "$digits" ] || die "kalitda raqam yo'q: $1"
  key="java:S$digits"

  # Bo'lim ustuni bo'sh qator: kalit bob muqaddimasidagi katalog jadvalida.
  # Butun bob o'qilmasin, belgi outline ga yo'naltiradi.
  local out
  out="$(awk -F'\t' -v k="$key" '
    FILENAME ~ /sections\.tsv$/ { if (FNR > 1) st[$1"|"$2] = $4; next }
    FILENAME ~ /chapters\.tsv$/ { if (FNR > 1) ch[$1"|"$2] = $3; next }
    FNR > 1 && $1 == k {
      if ($4 != "") { ref = $4; title = st[$2"|"$4] }
      else          { ref = $3; title = ch[$2"|"$3] " [katalog: outline]" }
      printf "%-11s %-7s %5.2f  %s\n", $2, ref, $6, title
    }
  ' "$SECTIONS" "$CHAPTERS" "$RULES")"

  if [ -z "$out" ]; then
    printf '%s qo%sllanmada izohlanmagan.\n' "$key" "'" >&2
    printf "matn ichidan qidirish: doc.sh find -f '%s'\n" "$key" >&2
    return 1
  fi
  # Ro'yxat ko'zga tashlanish bo'yicha saralangan, boshidagilar yetadi:
  # ko'p bo'limda eslatilgan kalit (S3776) aks holda 29 qator beradi.
  # Katalog bobi (25-30) har doim ko'rinadi: kalit uning jadvalida
  # tuzatish bo'limiga bog'langan, bali esa past (S3776 da 29-o'rin).
  local total top shown
  total="$(printf '%s\n' "$out" | wc -l)"
  if [ "$all" -eq 0 ] && [ "$total" -gt "$RULE_LIMIT" ]; then
    top="$(printf '%s\n' "$out" | awk -v n="$RULE_LIMIT" 'NR <= n || /\[katalog: outline\]$/')"
    shown="$(printf '%s\n' "$top" | wc -l)"
    printf '%s\n' "$top"
    [ "$total" -gt "$shown" ] && printf "... yana %d ta (hammasi: doc.sh rule --all %s)\n" \
      "$((total - shown))" "$key"
  else
    printf '%s\n' "$out"
  fi
  printf "> doc.sh show <hujjat> <raqam>   (uchinchi ustun: ko'zga tashlanish)\n" >&2
}

# Bo'lim yoki bobning tekshiruv punktlari. Korpusda 2000 dan ortiq punkt
# yozilgan; ishdan oldin ro'yxatni o'ylab topish shart emas. Butun hujjat
# 28-47 KB, shuning uchun raqamsiz so'rov bob bo'yicha sanoq beradi,
# to'liq ro'yxat faqat --all bilan.
cmd_checklist() {
  local all=0
  local -a pos=()
  while [ $# -gt 0 ]; do
    case "$1" in
      --all) all=1; shift ;;
      *)     pos+=("$1"); shift ;;
    esac
  done
  { [ ${#pos[@]} -ge 1 ] && [ ${#pos[@]} -le 2 ]; } \
    || die "foydalanish: doc.sh checklist [--all] <hujjat> [bob yoki bo'lim]"
  local doc="${pos[0]}" ref="${pos[1]:-}"
  local out
  if [ -z "$ref" ] && [ "$all" -eq 0 ]; then
    out="$(awk -F'\t' -v d="$doc" '
      FILENAME ~ /chapters\.tsv$/ { if (FNR > 1 && $1 == d) t[$2] = $3; next }
      FNR > 1 && $1 == d { n[$2]++ }
      END { for (c in n) printf "%-4s %3d punkt  %s\n", c, n[c], t[c] }
    ' "$CHAPTERS" "$CHECKLIST" | sort -n)"
    [ -n "$out" ] || die "punkt topilmadi: $doc"
    printf '%s\n' "$out"
    printf "> doc.sh checklist %s <bob>   (hammasi: --all)\n" "$doc" >&2
    return
  fi
  # Bo'lim raqami satr sifatida (r ""): 1.1 so'ralganda 1.10 chiqmasin.
  out="$(awk -F'\t' -v d="$doc" -v r="$ref" '
    NR > 1 && $1 == d {
      if (r == "")                       keep = 1
      else if (index(r, ".") > 0)        keep = ($3 == (r ""))
      else                               keep = ($2 == r)
      if (!keep) next
      if ($3 != last) { if (last != "") print ""; print $3; last = $3 }
      print "  - [ ] " $4
    }
  ' "$CHECKLIST")"
  [ -n "$out" ] || die "punkt topilmadi: $doc ${ref:-}"
  printf '%s\n' "$out"
}

# Bo'limning fayli, satr oralig'i va markdown havolasi: skill yoki hujjat
# yozayotganda havolani qo'lda hisoblamaslik uchun. Raqam satr sifatida.
cmd_path() {
  [ $# -eq 2 ] || die "foydalanish: doc.sh path <hujjat> <raqam>"
  awk -F'\t' -v d="$1" -v r="$2" 'NR>1 && $1==d && $2==r"" {
    printf "%s:%s-%s\n%s#%s\n", $5, $6, $7, $5, $8; found=1; exit
  } END { exit !found }' "$SECTIONS" \
    || die "topilmadi: $1 $2"
}

# ---------------------------------------------------------------- main

[ $# -gt 0 ] || { sed -n '2,4p' "${BASH_SOURCE[0]}"; printf "
  doc.sh find [-f] [-n N] [--] <so'rov>   bo'lim qidirish (-f: matn ichidan ham)
  doc.sh show [--force] <hujjat> <raqam>  bo'lim yoki bob (katta bob o'rniga outline)
  doc.sh toc [hujjat]                     hujjatlar yoki boblar ro'yxati
  doc.sh outline <hujjat> [bob]           bo'limlar ro'yxati
  doc.sh path <hujjat> <raqam>            fayl, satr oralig'i va havola
  doc.sh rule [--all] <java:Sxxxx>        Sonar kalitini izohlagan bo'lim
  doc.sh checklist [--all] <hujjat> [bob] tekshiruv punktlari (bobsiz: sanoq)
  doc.sh rebuild                          indeksni qayta yasash

hujjatlar: patterns  testing  architect  sonarqube  clean-code  code-review
"; exit 0; }

cmd="$1"; shift
case "$cmd" in
  find)    ensure_index; cmd_find "$@" ;;
  show)    ensure_index; cmd_show "$@" ;;
  toc)     ensure_index; cmd_toc "$@" ;;
  outline) ensure_index; cmd_outline "$@" ;;
  path)    ensure_index; cmd_path "$@" ;;
  rule)    ensure_index; cmd_rule "$@" ;;
  checklist) ensure_index; cmd_checklist "$@" ;;
  rebuild) rebuild ;;
  *)       die "noma'lum buyruq: $cmd  (doc.sh yordam uchun argumentsiz)" ;;
esac
