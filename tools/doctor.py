#!/usr/bin/env python3
"""O'rnatish va Claude Code bilan shartnomani bitta buyruqda tekshiradi.

    python3 tools/doctor.py                                # repo settings.json
    python3 tools/doctor.py --settings ~/.claude/settings.json   # global
    python3 tools/doctor.py --proyekt <papka> --kun 30

Har band bir qator: `OK`, `OGOH` (ogohlantirish), `XATO` yoki `O'TK`
(tekshirib bo'lmadi, o'tkazildi). Kod 1 faqat XATO bo'lsa, aks holda 0.

Bandlar:
  1. `claude --version` SINALGAN_CLAUDE_CODE dan farq qilsa ogohlantirish.
     Hook payloadi, transkript tuzilishi va ruxsat xulqi versiyaga bog'liq,
     asboblar testi esa o'zi taxmin qilgan shartnomani sinaydi.
  2. Python: GENIUS_PYTHON (muhit yoki settings `env`), bo'lmasa python3.
  3. Klon: `.genius.json` dagi ildiz yoki shu klon, asboblari joyida.
  4. O'rnatilgan nusxa: `.genius.json` commiti klon HEAD i bilan.
  5. Har hook buyrug'i `|| exit N` siz, `tools/testdata/hooks/<event>.json`
     namunasi bilan yuradi: exit 0, bo'sh stderr, stdout bo'sh yoki
     to'g'ri `hookEventName` li JSON. `|| exit 0` olib tashlanadi, chunki
     u aynan shu xatolarni jim yutadi (klon ko'chgan, python3 yo'q).
  6. Oxirgi N kun transkriptidan aktyor -> model: frontmatter dagi alias
     (sonnet, opus, haiku) provayder va vaqtga qarab boshqa modelga
     bog'lanadi. Kutilgan oiladan farq qilsa ogohlantirish.

Hooklar vaqtinchalik holat papkasi bilan yuradi (GENIUS_STATE_DIR,
USAGE_STORE): tekshiruv budjet, sarf va sessiya holatiga tegmaydi.
Matcher li hook uchun namuna tool i mos kelmasa `<event>-<Tool>.json`
izlanadi (masalan `PreToolUse-Agent.json`).
"""

import argparse
import collections
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HOOKS_DIR = os.path.join(HERE, "testdata", "hooks")

# Asboblar va hook shartnomasi shu versiyada qo'lda sinalgan. Yangisida
# doctor qatorlari va install/README.md dagi tekshiruv qayta o'tkaziladi,
# keyin bu qiymat va README bitta commitda yangilanadi.
SINALGAN_CLAUDE_CODE = "2.1.289"

EXIT_SUFFIX = re.compile(r"\s*\|\|\s*exit\s+\d+\s*$")
SCRIPT = re.compile(r"([\w.-]+\.(?:py|sh))")
# hookSpecificOutput siz JSON da ruxsat etilgan umumiy maydonlar.
TOP_LEVEL = {"continue", "stopReason", "suppressOutput", "systemMessage",
             "decision", "reason"}
ALIASES = ("opus", "sonnet", "haiku")

OK, WARN, FAIL, SKIP = "OK", "OGOH", "XATO", "O'TK"


def line(status, band, text):
    return (status, "%-4s %s: %s" % (status, band, text))


def config_dir():
    return (os.environ.get("CLAUDE_CONFIG_DIR")
            or os.path.join(os.path.expanduser("~"), ".claude"))


def read_json(path):
    try:
        with open(path, encoding="utf-8-sig") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return None


# --- 1. Claude Code versiyasi -------------------------------------------

def parse_version(text):
    found = re.search(r"(\d+)\.(\d+)\.(\d+)", text or "")
    return tuple(int(x) for x in found.groups()) if found else None


def check_version(output, tested=SINALGAN_CLAUDE_CODE):
    """`claude --version` chiqishi (None: topilmadi) -> band qatori."""
    if output is None:
        return line(SKIP, "claude", "`claude` topilmadi, versiya tekshirilmadi")
    current = parse_version(output)
    if current is None:
        return line(WARN, "claude", "versiya o'qilmadi: %r" % output.strip()[:60])
    shown = ".".join(map(str, current))
    if current == parse_version(tested):
        return line(OK, "claude", "%s (sinalgan)" % shown)
    side = "eski" if current < parse_version(tested) else "yangi"
    return line(WARN, "claude", "%s, sinalgan %s dan %s: hook natijasi va "
                "transkript tuzilishini qayta tekshiring (install/README.md, "
                "'Claude Code versiyasi')" % (shown, tested, side))


def claude_version():
    exe = shutil.which("claude")
    if not exe:
        return None
    try:
        proc = subprocess.run([exe, "--version"], capture_output=True,
                              text=True, timeout=15)
    except (OSError, subprocess.SubprocessError):
        return None
    return proc.stdout if proc.returncode == 0 else None


# --- 2. Python ----------------------------------------------------------

def python_candidates(settings):
    out = []
    for source, value in (("GENIUS_PYTHON", os.environ.get("GENIUS_PYTHON")),
                          ("settings env.GENIUS_PYTHON",
                           ((settings or {}).get("env") or {}).get("GENIUS_PYTHON"))):
        if value:
            out.append((source, value))
    found = shutil.which("python3")
    out.append(("python3", found))
    return out


def check_python(settings):
    tried = []
    for source, exe in python_candidates(settings):
        if not exe:
            tried.append("%s yo'q" % source)
            continue
        try:
            proc = subprocess.run(
                [exe, "-c", "import sys; assert sys.version_info >= (3, 8); "
                            "print(sys.version.split()[0])"],
                capture_output=True, text=True, timeout=15)
        except (OSError, subprocess.SubprocessError) as exc:
            tried.append("%s: %s" % (source, exc.__class__.__name__))
            continue
        if proc.returncode == 0:
            return line(OK, "python", "%s (%s, %s)"
                        % (exe, proc.stdout.strip(), source))
        tried.append("%s: 3.8+ emas yoki ishlamadi" % source)
    return line(FAIL, "python", "ishlaydigan Python topilmadi (%s). Hooklar jim "
                "o'chadi: settings env.GENIUS_PYTHON ga to'liq yo'l yozing "
                "(install/README.md)" % "; ".join(tried))


# --- 3-4. Klon va o'rnatilgan nusxa -------------------------------------

def manifest_path():
    return os.path.join(config_dir(), "skills", "manguberdi", ".genius.json")


def check_clone(manifest):
    root = (manifest or {}).get("root") if isinstance(manifest, dict) else None
    root = root or ROOT
    missing = [rel for rel in ("tools/guard.py", "tools/usage.py",
                               "docs/manifest.json")
               if not os.path.isfile(os.path.join(root, rel))]
    if missing:
        return line(FAIL, "klon", "%s da yo'q: %s. Klon ko'chgan bo'lsa "
                    "install/README.md 'Klon o'chsa yoki ko'chsa'"
                    % (root, ", ".join(missing)))
    return line(OK, "klon", root)


def git_head(root):
    try:
        proc = subprocess.run(["git", "-C", root, "rev-parse", "HEAD"],
                              capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return ""
    return proc.stdout.strip() if proc.returncode == 0 else ""


def check_installed(manifest):
    if manifest is None:
        return line(SKIP, "o'rnatilgan", "%s yo'q (global o'rnatish emas)"
                    % manifest_path())
    if not isinstance(manifest, dict):
        return line(WARN, "o'rnatilgan", "%s buzuq" % manifest_path())
    installed = str(manifest.get("commit") or "")
    clone = git_head(manifest.get("root") or ROOT)
    text = "o'rnatilgan: %s, klon: %s" % (installed[:12] or "?", clone[:12] or "?")
    if installed and clone and installed != clone:
        return line(WARN, "o'rnatilgan", text + "; skill va aktyorlar eski "
                    "nusxa, o'rnatuvchini qayta yurgizing")
    return line(OK, "o'rnatilgan", text)


# --- 5. Hooklar ----------------------------------------------------------

def hook_entries(settings):
    hooks = (settings or {}).get("hooks") or {}
    for event, groups in hooks.items():
        for group in groups if isinstance(groups, list) else []:
            if not isinstance(group, dict):
                continue
            for hook in group.get("hooks") or []:
                if (isinstance(hook, dict) and hook.get("type") == "command"
                        and hook.get("command")):
                    yield event, group.get("matcher") or "", hook


def matches(matcher, tool):
    if not matcher or matcher == "*":
        return True
    try:
        return re.fullmatch(matcher, tool) is not None
    except re.error:
        return matcher == tool


def substitute(value, names):
    if isinstance(value, str):
        for name, real in names.items():
            value = value.replace("${%s}" % name, real)
        return value
    if isinstance(value, dict):
        return {k: substitute(v, names) for k, v in value.items()}
    if isinstance(value, list):
        return [substitute(v, names) for v in value]
    return value


def sample(event, matcher, hooks_dir=HOOKS_DIR):
    """Namunaviy payload yoki None. Matcher ga mos tool tanlanadi."""
    base = read_json(os.path.join(hooks_dir, event + ".json"))
    if isinstance(base, dict) and matches(matcher, str(base.get("tool_name") or "")):
        return base
    for tool in matcher.split("|") if matcher else []:
        alt = read_json(os.path.join(hooks_dir, "%s-%s.json" % (event, tool)))
        if isinstance(alt, dict):
            return alt
    return base if isinstance(base, dict) and "tool_name" not in base else None


def find_bash():
    """Git Bash: Claude Code Windows da hookni shu bilan yurgizadi.

    System32 va WindowsApps dagi bash.exe WSL ishga tushirgichi, u emas.
    """
    found = shutil.which("bash")
    if found and not re.search(r"system32|windowsapps", found, re.I):
        return found
    for base in (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)"),
                 os.path.join(os.environ.get("LOCALAPPDATA") or "", "Programs")):
        if base:
            candidate = os.path.join(base, "Git", "bin", "bash.exe")
            if os.path.isfile(candidate):
                return candidate
    return None


def judge(event, proc):
    """(holat, sabab): exit 0, bo'sh stderr, stdout bo'sh yoki to'g'ri JSON."""
    if proc.returncode != 0:
        first = (proc.stderr.strip().splitlines() or [""])[0][:120]
        return FAIL, "exit %d: %s" % (proc.returncode, first or "stderr bo'sh")
    if proc.stderr.strip():
        return FAIL, "stderr bo'sh emas: %s" % proc.stderr.strip().splitlines()[0][:120]
    out = proc.stdout.strip()
    if not out:
        return OK, "bo'sh chiqish"
    try:
        data = json.loads(out)
    except ValueError:
        return FAIL, "stdout JSON emas: %s" % out.splitlines()[0][:80]
    if not isinstance(data, dict):
        return FAIL, "stdout JSON obyekt emas"
    specific = data.get("hookSpecificOutput")
    if specific is not None:
        name = specific.get("hookEventName") if isinstance(specific, dict) else None
        if name != event:
            return FAIL, "hookEventName %r, kutilgan %r" % (name, event)
        return OK, "JSON, hookEventName %s" % event
    extra = sorted(set(data) - TOP_LEVEL)
    if extra:
        return FAIL, "noma'lum maydon: %s" % ", ".join(extra)
    return OK, "JSON"


def check_hooks(settings, project, hooks_dir=HOOKS_DIR):
    entries = list(hook_entries(settings))
    if not entries:
        return [line(WARN, "hook", "settings da command hook yo'q")]
    bash = find_bash()
    tmp = tempfile.mkdtemp(prefix="doctor_")
    env = dict(os.environ)
    for key, value in ((settings or {}).get("env") or {}).items():
        if isinstance(value, str):
            env[key] = value
    env.update(CLAUDE_PROJECT_DIR=project,
               GENIUS_STATE_DIR=os.path.join(tmp, "state"),
               USAGE_STORE=os.path.join(tmp, "usage"))
    env.pop("GENIUS_HOOK_DEBUG", None)
    names = {"HOOKS_DIR": hooks_dir.replace("\\", "/"),
             "CLAUDE_PROJECT_DIR": project.replace("\\", "/")}
    out = []
    try:
        for event, matcher, hook in entries:
            command = hook["command"]
            found = SCRIPT.search(command)
            label = "hook %s%s %s" % (event, "[%s]" % matcher if matcher else "",
                                      found.group(1) if found else command[:40])
            payload = sample(event, matcher, hooks_dir)
            if payload is None:
                out.append(line(WARN, label, "namunaviy payload yo'q: "
                                "tools/testdata/hooks/%s.json" % event))
                continue
            payload = substitute(payload, names)
            bare = EXIT_SUFFIX.sub("", command)
            argv = [bash, "-c", bare] if bash else bare
            started = time.time()
            try:
                proc = subprocess.run(
                    argv, input=json.dumps(payload), capture_output=True,
                    text=True, encoding="utf-8", errors="replace", env=env,
                    cwd=project, shell=not bash,
                    timeout=float(hook.get("timeout") or 60))
            except subprocess.TimeoutExpired:
                out.append(line(FAIL, label, "timeout %ss" % hook.get("timeout")))
                continue
            except OSError as exc:
                out.append(line(FAIL, label, "yurmadi: %s" % exc))
                continue
            status, reason = judge(event, proc)
            out.append(line(status, label, "%s (%.2f s)"
                            % (reason, time.time() - started)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return out


# --- 6. Aktyor -> model -------------------------------------------------

def expected_models():
    """{aktyor: model alias yoki id} repo va global agents/ frontmatter idan."""
    out = {}
    for folder in (os.path.join(config_dir(), "agents"),
                   os.path.join(ROOT, ".claude", "agents")):
        for path in sorted(glob.glob(os.path.join(glob.escape(folder), "*.md"))):
            try:
                with open(path, encoding="utf-8") as handle:
                    head = handle.read(2000)
            except OSError:
                continue
            front = re.match(r"---\s*\n(.*?)\n---", head, re.S)
            if not front:
                continue
            model = re.search(r"^model:\s*(\S+)", front.group(1), re.M)
            name = re.search(r"^name:\s*(\S+)", front.group(1), re.M)
            actor = name.group(1) if name else os.path.basename(path)[:-3]
            if model:
                out[actor] = model.group(1)   # repo nusxasi globaldan ustun
    return out


def first_model(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            for raw in handle:
                if '"model"' not in raw:
                    continue
                try:
                    row = json.loads(raw)
                except ValueError:
                    continue
                message = row.get("message") if isinstance(row, dict) else None
                model = message.get("model") if isinstance(message, dict) else None
                if model and model != "<synthetic>":
                    return model
    except OSError:
        return None
    return None


def actor_models(days, expected):
    """{aktyor: Counter(model)} oxirgi `days` kunlik subagent fayllaridan."""
    cutoff = time.time() - days * 86400
    found = collections.defaultdict(collections.Counter)
    pattern = os.path.join(glob.escape(os.path.join(config_dir(), "projects")),
                           "*", "*", "subagents", "**", "agent-*.meta.json")
    for meta in glob.glob(pattern, recursive=True):
        try:
            if os.path.getmtime(meta) < cutoff:
                continue
        except OSError:
            continue
        data = read_json(meta)
        actor = data.get("agentType") if isinstance(data, dict) else None
        if actor not in expected:
            continue
        model = first_model(meta[:-len(".meta.json")] + ".jsonl")
        if model:
            found[actor][model] += 1
    return found


def family_ok(expected, model):
    if expected in ALIASES:
        return expected in model
    if expected == "inherit":
        return True
    return expected == model


def check_models(days):
    expected = expected_models()
    found = actor_models(days, expected)
    if not found:
        return [line(SKIP, "aktyor modeli", "oxirgi %d kunda aktyor transkripti "
                     "yo'q" % days)]
    out = []
    for actor in sorted(found):
        want = expected[actor]
        models = found[actor]
        text = ", ".join("%s x%d" % item for item in models.most_common())
        wrong = [m for m in models if not family_ok(want, m)]
        if wrong:
            out.append(line(WARN, "model %s" % actor, "%s; kutilgan %s. Alias "
                            "provayder yoki versiyaga qarab boshqa modelga "
                            "bog'langan: ANTHROPIC_DEFAULT_%s_MODEL bilan pinlang "
                            "(install/README.md)" % (text, want, want.upper())
                            if want in ALIASES else
                            "%s; kutilgan %s" % (text, want)))
        else:
            out.append(line(OK, "model %s" % actor, "%s (kutilgan %s)" % (text, want)))
    return out


# --- Yig'ish -------------------------------------------------------------

def run(settings_path, project, days, version_output="auto"):
    settings = read_json(settings_path)
    results = []
    if version_output == "auto":
        version_output = claude_version()
    results.append(check_version(version_output))
    if not isinstance(settings, dict):
        results.append(line(FAIL, "settings", "%s %s" % (
            settings_path, "buzuq" if os.path.exists(settings_path) else "topilmadi")))
        settings = {}
    results.append(check_python(settings))
    manifest = read_json(manifest_path()) if os.path.exists(manifest_path()) else None
    results.append(check_clone(manifest))
    results.append(check_installed(manifest))
    results.extend(check_hooks(settings, project))
    results.extend(check_models(days))
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--settings",
                        default=os.path.join(ROOT, ".claude", "settings.json"))
    parser.add_argument("--proyekt", default=ROOT,
                        help="hook uchun CLAUDE_PROJECT_DIR (sukut: shu klon)")
    parser.add_argument("--kun", type=int, default=30)
    args = parser.parse_args(argv)
    results = run(os.path.expanduser(args.settings),
                  os.path.abspath(args.proyekt), args.kun)
    for _, text in results:
        print(text)
    counts = collections.Counter(status for status, _ in results)
    print("\ndoctor: %d OK, %d OGOH, %d XATO, %d o'tkazildi"
          % (counts[OK], counts[WARN], counts[FAIL], counts[SKIP]))
    return 1 if counts[FAIL] else 0


if __name__ == "__main__":
    sys.exit(main())
