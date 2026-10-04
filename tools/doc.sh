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

# show uchun chegara: bundan uzun blok tasodifan kontekstni to'ldirmasin.
MAX_LINES="${DOC_MAX_LINES:-1200}"
LIMIT_DEFAULT=20

die() { printf '%s\n' "$*" >&2; exit 1; }

rebuild() { python3 "$ROOT/tools/build_index.py" >&2; }

# Biror bob fayli indeksdan yangiroq bo'lsa, indeks qayta yasaladi.
# Eskirgan indeks noto'g'ri satr raqami beradi, bu jim xato bo'lar edi.
ensure_index() {
  if [ ! -f "$SECTIONS" ]; then
    rebuild
    return
  fi
  if [ -n "$(find "$ROOT/docs" -name '*.md' -newer "$SECTIONS" -print -quit)" ]; then
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
      -n|--limit) [ $# -ge 2 ] || die "-n dan keyin raqam kerak"; limit="$2"; shift 2 ;;
      --)         shift; words+=("$@"); break ;;
      -?*)        die "noma'lum bayroq: $1" ;;
      *)          words+=("$1"); shift ;;
    esac
  done
  [ ${#words[@]} -gt 0 ] || die "foydalanish: doc.sh find [-f] [-n N] <so'rov>"
  local query="${words[*]}"

  local raw
  raw="$(
    # 1) inglizcha taxalluslar - eng aniq urinish
    awk -F'\t' -v q="${query,,}" 'NR>1 && index(tolower($1), q) {
      print $2"\t"$4"\t"$1" [taxallus]"
    }' "$ALIASES"
    # 2) bo'lim sarlavhalari
    awk -F'\t' -v q="${query,,}" 'NR>1 && index(tolower($4), q) {
      print $1"\t"$2"\t"$4
    }' "$SECTIONS"
    # 3) bob sarlavhalari
    awk -F'\t' -v q="${query,,}" 'NR>1 && $2 != "" && index(tolower($3), q) {
      print $1"\t"$2"\t"$3
    }' "$CHAPTERS"
  )"

  if [ "$full" -eq 1 ]; then
    raw="$raw
$(fulltext "$query")"
  fi

  local out
  out="$(printf '%s\n' "$raw" | awk -F'\t' 'NF && !seen[$1"\t"$2]++')"

  if [ -z "$out" ]; then
    printf 'topilmadi: %s\n' "$query" >&2
    [ "$full" -eq 1 ] || printf "kengroq qidirish: doc.sh find -f '%s'\n" "$query" >&2
    return 1
  fi

  local total
  total="$(printf '%s\n' "$out" | wc -l)"
  printf '%s\n' "$out" | head -n "$limit" | awk -F'\t' '{
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
  { cd "$ROOT" && grep -rnFi --include='*.md' -- "$query" docs || true; } \
    | cut -d: -f1,2 \
    | awk -F'\t' '
        NR==FNR {
          if (FNR > 1) {
            n++; doc[n]=$1; num[n]=$2; title[n]=$4
            file[n]=$5; st[n]=$6; en[n]=$7
          }
          next
        }
        {
          p = index($0, ":")
          f = substr($0, 1, p - 1)
          l = substr($0, p + 1) + 0
          for (i = 1; i <= n; i++)
            if (file[i] == f && l >= st[i] && l <= en[i]) { hits[i]++; break }
        }
        END {
          for (i in hits)
            print doc[i]"\t"num[i]"\t"title[i]" ("hits[i]" marta)"
        }
      ' "$SECTIONS" -
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

  if [[ "$ref" == *.* ]]; then
    row="$(awk -F'\t' -v d="$doc" -v r="$ref" \
      'NR>1 && $1==d && $2==r { print $5"\t"$6"\t"$7"\t"$4; exit }' "$SECTIONS")"
  else
    row="$(awk -F'\t' -v d="$doc" -v r="$ref" \
      'NR>1 && $1==d && $2==r { print $4"\t"$5"\t"$6"\t"$3; exit }' "$CHAPTERS")"
  fi
  [ -n "$row" ] || die "topilmadi: $doc $ref  (doc.sh toc $doc bilan tekshiring)"

  local file start end title
  IFS=$'\t' read -r file start end title <<< "$row"

  local span=$((end - start + 1))
  if [ "$span" -gt "$MAX_LINES" ] && [ "$force" -eq 0 ]; then
    printf '%s %s - %s\n' "$doc" "$ref" "$title" >&2
    printf '%d satr (chegara %d). Ichidagi bo%slimlar:\n\n' \
      "$span" "$MAX_LINES" "'" >&2
    cmd_outline "$doc" "$ref"
    printf "\nto'liq chiqarish: doc.sh show --force %s %s\n" "$doc" "$ref" >&2
    return 1
  fi
  sed -n "${start},${end}p" "$ROOT/$file"
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

# Bo'limning fayli, satr oralig'i va markdown havolasi: skill yoki hujjat
# yozayotganda havolani qo'lda hisoblamaslik uchun.
cmd_path() {
  [ $# -eq 2 ] || die "foydalanish: doc.sh path <hujjat> <raqam>"
  awk -F'\t' -v d="$1" -v r="$2" 'NR>1 && $1==d && $2==r {
    printf "%s:%s-%s\n%s#%s\n", $5, $6, $7, $5, $8; found=1; exit
  } END { exit !found }' "$SECTIONS" \
    || die "topilmadi: $1 $2"
}

# ---------------------------------------------------------------- main

[ $# -gt 0 ] || { sed -n '2,4p' "${BASH_SOURCE[0]}"; printf "
  doc.sh find [-f] [-n N] <so'rov>        bo'lim qidirish (-f: matn ichidan ham)
  doc.sh show [--force] <hujjat> <raqam>  bo'lim yoki bobni chiqarish
  doc.sh toc [hujjat]                     hujjatlar yoki boblar ro'yxati
  doc.sh outline <hujjat> [bob]           bo'limlar ro'yxati
  doc.sh path <hujjat> <raqam>            fayl, satr oralig'i va havola
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
  rebuild) rebuild ;;
  *)       die "noma'lum buyruq: $cmd  (doc.sh yordam uchun argumentsiz)" ;;
esac
