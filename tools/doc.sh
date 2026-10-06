#!/usr/bin/env bash
# docs/ ga tez kirish: indeks kerakli bo'limni topadi, sed faqat o'sha
# satrlarni chiqaradi. Bob fayllari 68k tokengacha boradi, bitta bo'lim esa
# ~700 token, shuning uchun qidiruv bob emas, bo'lim darajasida ishlaydi.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IDX="$ROOT/index"
SECTIONS="$IDX/sections.tsv"
CHAPTERS="$IDX/chapters.tsv"
# Bob tekshiruvi holati. Indeksda emas, chunki u hosila emas: odam yozadi.
REVIEW="$ROOT/docs/review.tsv"
ALIASES="$IDX/aliases.tsv"
DOCS="$IDX/docs.tsv"
RULES="$IDX/rules.tsv"
CHECKLIST="$IDX/checklist.tsv"
# Inglizcha-o'zbekcha jadval (find varianti), suggest_sections ham o'qiydi.
SYNONYMS="$ROOT/tools/synonyms.tsv"
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
      \( -name '*.md' -o -name manifest.json -o -name build_index.py \
         -o -name aliases.tsv -o -name OWNERS.tsv \) \
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

  # Nom bo'yicha qidiruv (name_hits), kerak bo'lsa matn ichidan ham.
  # Izoh shu yerda, chunki bash 3.2 (macOS standarti) buyruq o'rnidagi
  # izohni sintaksis deb o'qiydi.
  local raw
  raw="$(name_hits "$query")"

  if [ "$full" -eq 1 ]; then
    raw="$raw
$(fulltext "$query")"
  fi

  local out
  out="$(printf '%s\n' "$raw" | awk -F'\t' 'NF && !seen[$1"\t"$2]++')"

  # Ibora hech qayerda aynan yo'q, lekin so'zlari bor bo'lishi mumkin:
  # "optimistic locking" -> 18.8 "Optimistik va pessimistik lock".
  # Faqat uy-bob topilgan bo'lsa ham shunday: qolgan hujjatlarning nuqtai
  # nazari so'zlar bo'yicha qo'shiladi. Naqshga to'liq mos uy-bob
  # birinchi qoladi, qisman mos kelgani (4-ustun `qisman`: "N+1 testda")
  # so'zlar natijasidan keyin, chunki ortiqcha so'z mavzuni toraytiradi.
  # Python topilmasa yoki yiqilsa, avvalgidek "topilmadi".
  local py extra
  if [ -z "$(printf '%s\n' "$out" | cut -f3 | grep -v '\[uy-bob\]$' || true)" ] \
      && [ "$(printf '%s\n' "$query" | awk '{ print NF }')" -ge 2 ] \
      && py="$(pick_python)"; then
    extra="$("$py" "$ROOT/tools/findlib.py" "$query" 2>/dev/null || true)"
    if [ -n "$extra" ]; then
      [ -n "$out" ] || printf "ibora topilmadi, so'zlar bo'yicha:\n" >&2
      out="$( { printf '%s\n' "$out" | awk -F'\t' '$4 != "qisman"'
                printf '%s\n' "$extra"
                printf '%s\n' "$out" | awk -F'\t' '$4 == "qisman"'; } \
              | awk -F'\t' 'NF && !seen[$1"\t"$2]++')"
    fi
  fi

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

# Nom bo'yicha qidiruv: taxallus, bo'lim va bob sarlavhasi bitta
# o'tishda. Har mos qatorga daraja beriladi: 4 aniq moslik (taxallus,
# sarlavha, ikki nuqtagacha qism, qavsdagi nom yoki backtick ichidagi
# identifikatorning o'zi), 3 butun so'z, 2 so'z boshi, 1 so'z ichida.
# So'z ichidagi moslik olib tashlanmaydi (find Lock ReentrantLock ni ham
# topsin), faqat pastga tushadi: "kesh" da Bikeshedding birinchi emas.
# Bir daraja ichida tartib avvalgidek: taxallus, bo'lim, bob (NR).
# Kichik harfga awk o'tkazadi: bash dagi kengaytmasi bash 4 talab qiladi.
# Ishora-yozuv (sections.tsv 9-ustuni) to'liq yozuv raqami bilan belgilanadi.
# Uy-bob (aliases.tsv kind=uy, docs/OWNERS.tsv dan): alias ustunidagi
# naqsh so'rovga qo'llanadi. To'liq mos kelsa daraja 5, ya'ni hammadan
# oldin; qisman mos kelsa 3 va o'sha daraja oxirida: "Idempotent
# Consumer" taxallusi o'z bo'limini idempotentlik uy-bobidan oldin beradi.
# Bitta so'zli ASCII so'rovga transliteratsiya varianti (tools/findlib.py
# translit bilan bir xil) va synonyms.tsv [inglizcha] bloki qo'shiladi:
# migration -> migratsiya, isolation -> izolyatsiya.
# Faqat POSIX awk: mawk va macOS awk da regex interval va gawk
# kengaytmalari yo'q, shuning uchun so'z chegarasi index/substr bilan.
# awk bloki single-quote ichida, u yerda apostrof ishlatilmaydi.
name_hits() {
  local syn="$SYNONYMS" tab
  tab="$(printf '\t')"
  [ -f "$syn" ] || syn=/dev/null
  awk -F'\t' -v q="$1" -v syn="$syn" -v al="$ALIASES" -v se="$SECTIONS" \
      -v ch="$CHAPTERS" '
    function wordch(c) { return c != "" && index("abcdefghijklmnopqrstuvwxyz0123456789_", c) > 0 }
    function tier(s, x,    p, off, b, a, t, best) {
      best = 0; off = 0
      while ((p = index(substr(s, off + 1), x)) > 0) {
        p += off
        b = (p > 1) ? substr(s, p - 1, 1) : ""
        a = substr(s, p + length(x), 1)
        t = wordch(b) ? 1 : (wordch(a) ? 2 : 3)
        if (t > best) best = t
        if (best == 3) break
        off = p
      }
      return best
    }
    function bare(w) { sub(/^@/, "", w); return w }
    function exact(s, x,    t, i, j, w, rest) {
      if (s == x) return 1
      t = s
      sub(/^[0-9][0-9.]* /, "", t)
      if (t == x) return 1
      i = index(t, ": ")
      if (i > 1 && substr(t, 1, i - 1) == x) return 1
      if (match(t, / \([^()]*\)$/)) {
        if (substr(t, 1, RSTART - 1) == x) return 1
        if (substr(t, RSTART + 2, RLENGTH - 3) == x) return 1
      }
      rest = t
      while ((i = index(rest, "`")) > 0) {
        rest = substr(rest, i + 1)
        j = index(rest, "`")
        if (j == 0) break
        w = substr(rest, 1, j - 1)
        if (w == x || bare(w) == bare(x)) return 1
        rest = substr(rest, j + 1)
      }
      return 0
    }
    function score(s,    k, t, best) {
      s = tolower(s); best = 0
      for (k = 1; k <= nv; k++) {
        if (index(s, v[k]) == 0) continue
        t = exact(s, v[k]) ? 4 : tier(s, v[k])
        if (t > best) best = t
      }
      return best
    }
    function emit(t, line) { if (t > 0) print t "\t" NR "\t" line }
    function owner(re,    t) {
      if (match(q, "^(" re ")$")) return 5
      if (match(q, re)) return 3
      return 0
    }
    BEGIN {
      q = tolower(q); nv = 1; v[1] = q
      if (q ~ /^[a-z]+$/) {
        single = 1; t = q
        gsub(/ction/, "ksiya", t); gsub(/tion/, "tsiya", t); gsub(/sion/, "siya", t)
        sub(/ic$/, "ik", t); gsub(/c/, "k", t)
        if (t != q) v[++nv] = t
      }
    }
    FILENAME == syn {
      if (index($0, "# [inglizcha]") == 1) inside = 1
      else if (index($0, "# [/inglizcha]") == 1) inside = 0
      else if (inside && single && $1 == q) {
        n = split($2, parts, " ")
        for (i = 1; i <= n; i++) v[++nv] = parts[i]
      }
      next
    }
    FNR == 1 { next }
    FILENAME == al && $3 == "uy" {
      t = owner($1)
      if (t > uy[$2 "\t" $4]) uy[$2 "\t" $4] = t
      next
    }
    FILENAME == al { emit(score($1), $2 "\t" $4 "\t" $1 " [taxallus]"); next }
    FILENAME == se {
      if (($1 "\t" $2) in uy) uytitle[$1 "\t" $2] = $4
      emit(score($4), $1 "\t" $2 "\t" $4 ($9 != "" ? " [ishora: " $9 "]" : "")); next
    }
    FILENAME == ch && $2 != "" {
      if (($1 "\t" $2) in uy) uytitle[$1 "\t" $2] = $3
      emit(score($3), $1 "\t" $2 "\t" $3)
    }
    END {
      for (k in uy) if (uy[k] > 0)
        print uy[k] "\t" (uy[k] == 5 ? 0 : 999999999) "\t" k "\t" uytitle[k] \
          " [uy-bob]" (uy[k] == 5 ? "" : "\tqisman")
    }
  ' "$syn" "$ALIASES" "$SECTIONS" "$CHAPTERS" \
    | sort -t "$tab" -k1,1nr -k2,2n | cut -f3-
}

# To'liq matn qidiruvi: topilgan satrni egasi bo'lgan bo'limga bog'laydi.
# grep hech narsa topmasa 1 qaytaradi, bu xato emas, shuning uchun yutiladi.
fulltext() {
  local query="$1"
  # awk bloki single-quote ichida, shuning uchun u yerda apostrof ishlatilmaydi.
  # lo/hi: bir faylning bo'limlari indeksda ketma-ket turadi, shuning uchun
  # har topilgan satr uchun 3293 ta emas, faqat shu fayl bo'limlari ko'riladi.
  # Oxirgi sort: topilish soni ko'p bo'lim yuqorida turadi.
  # LC_ALL: Git for Windows dagi grep 3.0 C locale da -F va -i birga
  # kelsa har safar qulaydi (Aborted), `|| true` esa buni yashirardi.
  # env orqali: locale yo'q tizimda bash ogohlantirish chiqarmasin.
  { cd "$ROOT" && env LC_ALL=C.UTF-8 grep -rnFi --include='*.md' -- "$query" docs || true; } \
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

# Bobning tekshiruv holati, bitta qator. Tekshirilgan bobda jim turadi:
# ogohlantirish faqat ishonib bo'lmaydigan holat uchun chiqadi, aks holda
# u har chaqiruvda shovqin bo'lardi.
review_note() {
  local doc="$1" ref="$2" chapter holat
  chapter="${ref%%.*}"
  [ -f "$REVIEW" ] || return 0
  holat="$(awk -F'\t' -v d="$doc" -v c="$chapter" \
    '$1==d && $2==c { print $3; exit }' "$REVIEW")"
  case "$holat" in
    ai-draft)
      printf '[%s %s: tekshirilmagan bob (AI yozgan). Texnik da%svoni\n' \
        "$doc" "$chapter" "'" >&2
      printf ' birlamchi manbaga solishtiring.]\n' >&2 ;;
    tekshirilmoqda)
      printf '[%s %s: tekshirilmoqda, da%svolar hali tasdiqlanmagan.]\n' \
        "$doc" "$chapter" "'" >&2 ;;
  esac
}

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
  review_note "$doc" "$ref"
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
  # 7-ustun `qoida`: bo'lim "Qoida: `java:S1192`" bilan boshlanadi, ya'ni
  # katalogdagi tuzatish retsepti. U birinchi turadi va uchinchi ustunda
  # ulush o'rniga `qoida` yoziladi, qolgani ulush tartibida (sort -s
  # barqaror).
  local out tab
  tab="$(printf '\t')"
  out="$(awk -F'\t' -v k="$key" '
    FILENAME ~ /sections\.tsv$/ { if (FNR > 1) st[$1"|"$2] = $4; next }
    FILENAME ~ /chapters\.tsv$/ { if (FNR > 1) ch[$1"|"$2] = $3; next }
    FNR > 1 && $1 == k {
      if ($4 != "") { ref = $4; title = st[$2"|"$4] }
      else          { ref = $3; title = ch[$2"|"$3] " [katalog: outline]" }
      share = ($7 + 0) ? "qoida" : sprintf("%5.2f", $6)
      printf "%d\t%-11s %-7s %5s  %s\n", $7 + 0, $2, ref, share, title
    }
  ' "$SECTIONS" "$CHAPTERS" "$RULES" | sort -s -t "$tab" -k1,1nr | cut -f2-)"

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
  printf "> doc.sh show <hujjat> <raqam>   (uchinchi ustun: ko'zga tashlanish yoki qoida)\n" >&2
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
