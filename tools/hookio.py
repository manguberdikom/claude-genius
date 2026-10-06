"""Hook kirishi va hookning qayerda ishlashi.

Kirish: Claude Code stdin ga UTF-8 JSON beradi.

Matnli `sys.stdin` Windows da ANSI kod sahifasi (cp1252) bilan o'qiydi,
o'zbekcha `ʻ` yoki ruscha harfli prompt buzilib keladi. Windows
PowerShell 5.1 esa native buyruqqa pipe qilganda boshiga BOM qo'yishi
mumkin: `json.load` undan yiqiladi va hook jim qoladi. Shuning uchun
baytlar o'qiladi va `utf-8-sig` bilan ochiladi.
"""

import json
import os
import sys
import time


def read_text(stream=None):
    """stdin matni. Terminal, yopiq yoki o'qilmaydigan oqimda ""."""
    stream = sys.stdin if stream is None else stream
    try:
        if stream is None or stream.isatty():
            return ""
        raw = getattr(stream, "buffer", None)
        data = raw.read() if raw is not None else stream.read()
    except (OSError, ValueError):
        return ""
    if isinstance(data, bytes):
        return data.decode("utf-8-sig", errors="replace")
    return data.lstrip("\ufeff")


def read_payload(stream=None, blank=None):
    """JSON obyekt. Bo'sh kirishda `blank`, buzuq yoki obyekt emasda None.

    Terminal ham None: hook qo'lda yurgizilganda EOF kutib qotmaydi.
    """
    stream = sys.stdin if stream is None else stream
    try:
        if stream is None or stream.isatty():
            return None
    except (OSError, ValueError):
        return None
    text = read_text(stream)
    if not text.strip():
        return blank
    try:
        payload = json.loads(text)
    except ValueError:
        return None
    return payload if isinstance(payload, dict) else None


# --- Hook qayerda ishlaydi ----------------------------------------------

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Java proyekti belgisi. Faqat yig'uvchi fayllar: `src/` yoki `.java`
# borligi yetarli emas, chunki boshqa tilli repoda ham shunday papka
# uchraydi.
MARKERS = ("pom.xml", "build.gradle", "build.gradle.kts",
           "settings.gradle", "settings.gradle.kts")

# GENIUS_HOOKS shu qiymatlardan biri bo'lsa hooklar o'chadi. Hujjatdagi
# nomi `off`, qolganlari odatiy "yo'q" yozilishlari.
OFF = ("off", "0", "false", "no")
# `on` esa markerdan qat'i nazar yoqadi: Spring moduli ikkinchi darajada
# turgan monorepo (`backend/services/orders/pom.xml`) uchun. Chuqur skan
# o'rniga shu: har Read va Bash da papka aylanish narxi to'lanmaydi.
ON = ("on", "1", "true", "yes")

# Ildizda shulardan biri bo'lsa repo mobil yoki JS ilova: React Native,
# Expo, Capacitor, Cordova (package.json, app.json) yoki Flutter
# (pubspec.yaml). Ularning `android/build.gradle` i Java proyekti belgisi
# emas, Gradle u yerda faqat mobil yig'uvchi.
MOBILE_ROOT = ("package.json", "pubspec.yaml", "app.json")
MOBILE_DIRS = ("android",)


def _same(left, right):
    """Ikki yo'l bitta papkani ko'rsatadimi.

    realpath symlink ni yechadi, normcase esa Windows da registr va
    ajratgich farqini olib tashlaydi: `C:\\Users\\x` va `c:/users/x`
    bitta papka.
    """
    try:
        return (os.path.normcase(os.path.realpath(left))
                == os.path.normcase(os.path.realpath(right)))
    except OSError:
        return False


def _marked(folder):
    """Papkada Java yig'uvchisining fayli bormi."""
    for name in MARKERS:
        if os.path.isfile(os.path.join(folder, name)):
            return True
    return False


def project_root(payload=None):
    """Hook ishlayotgan proyekt ildizi yoki None.

    CLAUDE_PROJECT_DIR ni Claude Code hook jarayoniga beradi. U bo'lmasa
    payload dagi `cwd` olinadi: Stop va UserPromptSubmit payloadlarida u
    bor. Ikkisi ham yo'q bo'lsa None, ya'ni "bilmadim".
    """
    root = os.environ.get("CLAUDE_PROJECT_DIR") or ""
    if not root and isinstance(payload, dict):
        cwd = payload.get("cwd")
        root = cwd if isinstance(cwd, str) else ""
    root = root.strip()
    return root if root and os.path.isdir(root) else None


def active(payload=None):
    """Hook shu proyektda ishlashi kerakmi.

    Global o'rnatishda hooklar HAR proyektda yuradi. Python yoki JS
    proyektida ularning qoidalari o'rinsiz: docker va psql to'siladi,
    Java bo'limlari taklif qilinadi, har Read va Bash ga Python ishga
    tushishi qo'shiladi. Shuning uchun hook faqat ikki joyda ishlaydi:

    - qo'llanma klonining o'zida (asbob va hujjat shu yerda);
    - Java proyektida, ya'ni ildizida yoki birinchi darajali papkasida
      Maven yoki Gradle yig'uvchisi bo'lgan repoda (ko'p modulli repoda
      `pom.xml` ildizda emas, `backend/pom.xml` da turishi mumkin).

    Istisnolar: Android ilova (`_android`) nofaol; ildizda MOBILE_ROOT
    bo'lsa `android/` dagi marker sanalmaydi (React Native, Flutter),
    lekin `backend/pom.xml` sanaladi. `GENIUS_HOOKS=on` hammasidan ustun.

    Ildiz aniqlanmasa NOFAOL: hook o'z noaniqligi tufayli hech qachon
    to'smaydi. docref.in_clone() bu yerda yaramaydi, u JORIY papkaga
    qaraydi, hook jarayonining papkasi esa proyekt ildizi bo'lishi shart
    emas.
    """
    flag = os.environ.get("GENIUS_HOOKS", "").strip().lower()
    if flag in OFF:
        return False
    if flag in ON:
        return True
    root = project_root(payload)
    if root is None:
        return False
    if _same(root, ROOT):
        return True
    try:
        with os.scandir(root) as entries:
            subs = [e.path for e in entries if e.is_dir()]
    except OSError:
        return False
    if _android(root, subs):
        return False
    if _marked(root):
        return True
    if any(os.path.isfile(os.path.join(root, n)) for n in MOBILE_ROOT):
        subs = [s for s in subs
                if os.path.basename(s).lower() not in MOBILE_DIRS]
    return any(_marked(sub) for sub in subs)


# --- Hook xatosi izi ----------------------------------------------------

ERRORS_LOG = "hook_errors.log"
ERRORS_KEEP = 200


def state_dir():
    """Holat papkasi: GENIUS_STATE_DIR, aks holda klondagi `.claude/.state`
    (budget, state va handoff bilan bir xil). Har chaqiruvda o'qiladi."""
    return (os.environ.get("GENIUS_STATE_DIR")
            or os.path.join(ROOT, ".claude", ".state"))


def fail_open(name, exc):
    """Hook kutilmagan xatoda jim o'tadi (fail-open), lekin iz qoldiradi.

    Holat papkasidagi `hook_errors.log` ga bitta qator: vaqt, hook nomi,
    istisno turi va xabari. Fayl oxirgi ERRORS_KEEP qatorda kesiladi.
    Hook stderr i hech kimga ko'rinmaydi, shuning uchun usiz buzilgan
    hook oylar davomida sezilmasdi. Yozib bo'lmasa ham jim: bu funksiya
    hookni hech qachon yiqitmaydi.
    """
    try:
        message = " ".join(str(exc).split())[:300]
        line = "%s\t%s\t%s: %s\n" % (time.strftime("%Y-%m-%dT%H:%M:%S"), name,
                                      type(exc).__name__, message)
        folder = state_dir()
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, ERRORS_LOG)
        try:
            with open(path, encoding="utf-8", errors="replace") as handle:
                lines = handle.readlines()
        except OSError:
            lines = []
        lines = (lines + [line])[-ERRORS_KEEP:]
        tmp = "%s.%d.tmp" % (path, os.getpid())
        with open(tmp, "w", encoding="utf-8") as handle:
            handle.writelines(lines)
        os.replace(tmp, path)
    except Exception:  # noqa: BLE001 - iz yozilmasa ham hook o'tadi
        pass


def _android(root, subs):
    """Android ilova: qo'llanma server tomoni uchun, maslahati o'rinsiz.

    Ikki belgi. Modulda `src/main/AndroidManifest.xml` (AGP tuzilishi),
    yoki version catalog da `com.android` plagini: yangi Android Studio
    shabloni build faylida `alias(libs.plugins.android.application)`
    yozadi va `com.android` matni faqat catalog da qoladi.
    """
    manifest = os.path.join("src", "main", "AndroidManifest.xml")
    if any(os.path.isfile(os.path.join(d, manifest)) for d in [root] + subs):
        return True
    catalog = os.path.join(root, "gradle", "libs.versions.toml")
    try:
        with open(catalog, encoding="utf-8", errors="replace") as handle:
            return "com.android" in handle.read(65536)
    except OSError:
        return False
