#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Guard PreToolUse - ga-zone-engine. Registrato in .claude/settings.json (sede CLI e Web).

Enforcement MECCANICO di FORMA (mai di sostanza) per 4 protezioni:
  1. Quarantena impianto B : nessun Read/Edit/Write/Glob/Grep dentro
     'Business Spec/OLD_NOT_USE_NOT_READ_FILES_MODEL_4_CANALI/' (decisione AC 11/06/2026).
  2. Protezione governance : nessun Write/Edit su '.claude/agents/' senza il flag
     '.claude/AGENTS_UNLOCK' (file vuoto, untracked, creato/rimosso solo su autorizzazione
     esplicita del supervisore).
  3. RM-1 (forma)          : un commit che aggiunge righe 'verificat*' in file .md non esenti
     e' bloccato se il file non contiene il blocco VERIFICA/PROVE/ALTERNATIVE
     (cfr. tasks/METODO.md:28-33).
  4. RM-4 (forma)          : un commit che introduce nuovi tasks/{HANDOFF,PROBE,INDAGINE,RIPRESA}_*
     o script di parsing in scripts/ e' bloccato se manca sia il blocco 'Self-review RM-1..RM-3'
     nel file sia una reviews/PROBE_REVIEW_<base>_*.md (cfr. tasks/METODO.md par. RM-4).

LIMITE DICHIARATO (cfr. finding F4 audit 4-canali): il guard verifica la PRESENZA dei blocchi,
non la loro verita'. Guard verde != "verificato davvero". La sostanza di RM-1..RM-4 resta in
carico al gatekeeping dell'Orchestratore e alle review. Residui noti non coperti: Grep
project-wide puo' restituire contenuto della quarantena; redirezioni shell dirette non sono
intercettate.

Override (solo su autorizzazione esplicita del supervisore, da motivare nel commit message):
aggiungere [RM-HOOK-OVERRIDE] al comando git.

Protocollo hook: legge il JSON dell'evento da stdin. Exit 0 = consenti; exit 2 = blocca
(lo stderr viene mostrato a Claude). Qualunque errore interno = exit 0 (fail-open, mai
bloccare il lavoro per un bug del guard).
"""
import fnmatch
import json
import os
import re
import subprocess
import sys

QUAR = "OLD_NOT_USE_NOT_READ_FILES_MODEL_4_CANALI"
UNLOCK_FLAG = os.path.join(".claude", "AGENTS_UNLOCK")

# RM-1: il gatekeeping di forma vale per i commit non-CAP (cfr. .claude/CLAUDE.md).
# Esenti: file di stato (sintetizzano esiti gia' verificati altrove), reviews/ e reports/
# (coperti dal ciclo di review pieno), capitoli metodologia (idem), e la quarantena.
RM1_EXEMPT_FILES = {
    "tasks/STATO_CORRENTE.md", "tasks/CARRYOVER.md", "tasks/ACTIVE_TASK.md",
    "tasks/DEV_STATUS.md", "tasks/QUESTIONS.md",
}
RM1_EXEMPT_PREFIXES = ("reviews/", "reports/", "docs/methodology_v2/")

RM4_NAME_PATTERNS = ("tasks/HANDOFF_*", "tasks/PROBE_*", "tasks/INDAGINE_*", "tasks/RIPRESA_*")
RM4_EXEMPT_PREFIXES = ("scripts/claude_hooks/",)
PARSER_HINT = re.compile(r"\b(parse|decod\w*|payload|DAPI|CANDLE|BOOK_5|telegram)\b", re.I)

VERIF = re.compile(r"verificat", re.I)
RM1_BLOCK_MARKER = re.compile(r"ALTERNATIVE", re.I)
SELF_REVIEW = re.compile(r"self.?review", re.I)
QUAR_READ_CMD = re.compile(
    r"\b(cat|type|Get-Content|gc|less|more|head|tail|Copy-Item|copy|cp|Move-Item|mv|Select-String|grep)\b",
    re.I)
GIT_COMMIT = re.compile(r"\bgit\b[\s\S]*\bcommit\b")
GIT_ADD = re.compile(r"\bgit\b[^\n|;&]*\badd\b")


def deny(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(2)


def root():
    return os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          errors="replace", cwd=root())


def norm(p):
    return str(p or "").replace("\\", "/")


def staged_content(path):
    r = git("show", ":" + path)
    return r.stdout if r.returncode == 0 else ""


def disk_content(path):
    try:
        with open(os.path.join(root(), path), encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def rm1_exempt(path):
    p = norm(path)
    return (p in RM1_EXEMPT_FILES or QUAR in p
            or any(p.startswith(pre) for pre in RM1_EXEMPT_PREFIXES))


def check_rm1(path, added_lines, content, problems):
    if rm1_exempt(path) or not norm(path).lower().endswith(".md"):
        return
    hits = [l.strip() for l in added_lines if VERIF.search(l)]
    if hits and not RM1_BLOCK_MARKER.search(content):
        problems.append(
            "RM-1 (forma) - '%s': aggiunge dichiarazioni 'verificato' (es. \"%s\") ma il file non "
            "contiene il blocco VERIFICA/PROVE/ALTERNATIVE ESCLUSE/NON ESCLUSE "
            "(tasks/METODO.md:28-33)." % (path, hits[0][:90]))


def is_rm4_target(path, content):
    p = norm(path)
    if QUAR in p or any(p.startswith(pre) for pre in RM4_EXEMPT_PREFIXES):
        return False
    if any(fnmatch.fnmatch(p, pat) for pat in RM4_NAME_PATTERNS):
        return True
    return p.startswith("scripts/") and p.endswith(".py") and bool(PARSER_HINT.search(content))


def probe_review_exists(base):
    rdir = os.path.join(root(), "reviews")
    if not os.path.isdir(rdir):
        return False
    b = base.lower()
    return any(f.lower().startswith("probe_review_") and b in f.lower()
               for f in os.listdir(rdir))


def check_rm4(path, content, problems):
    if SELF_REVIEW.search(content) and "RM-1" in content:
        return
    base = os.path.splitext(os.path.basename(norm(path)))[0]
    if probe_review_exists(base):
        return
    problems.append(
        "RM-4 (forma) - '%s': output non-CAP determinante NUOVO senza blocco "
        "'Self-review RM-1..RM-3' nel file ne' reviews/PROBE_REVIEW_%s_*.md "
        "(tasks/METODO.md par. RM-4: opzione A o B obbligatoria prima del commit)."
        % (path, base))


def added_lines_by_file(diff_args):
    r = git("diff", *diff_args, "-U0")
    out, cur = {}, None
    for line in r.stdout.splitlines():
        if line.startswith("+++ b/"):
            cur = line[6:]
        elif cur and line.startswith("+") and not line.startswith("+++"):
            out.setdefault(cur, []).append(line[1:])
    return out


def handle_commit(cmd):
    problems = []
    seen = set()

    # 1) Stato gia' staged al momento dell'hook.
    for path, lines in added_lines_by_file(["--cached"]).items():
        seen.add(path)
        check_rm1(path, lines, staged_content(path), problems)
    for line in git("diff", "--cached", "--name-status").stdout.splitlines():
        if line.startswith("A"):
            path = line.split("\t")[-1]
            content = staged_content(path)
            if is_rm4_target(path, content):
                check_rm4(path, content, problems)

    # 2) Comando combinato 'git add ...; git commit ...': lo staging avviene DOPO questo hook,
    #    quindi analizza in superset prudente anche working tree e untracked citati nel comando.
    if GIT_ADD.search(cmd):
        for path, lines in added_lines_by_file(["HEAD"]).items():
            if path not in seen:
                check_rm1(path, lines, disk_content(path), problems)
        cmd_n = norm(cmd)
        for path in git("ls-files", "--others", "--exclude-standard").stdout.splitlines():
            p = norm(path)
            if p in seen:
                continue
            if p not in cmd_n and os.path.basename(p) not in cmd_n:
                continue
            content = disk_content(p)
            check_rm1(p, content.splitlines(), content, problems)
            if is_rm4_target(p, content):
                check_rm4(p, content, problems)

    if problems:
        deny("COMMIT BLOCCATO - guard RM (controllo di FORMA, non di sostanza):\n- "
             + "\n- ".join(problems)
             + "\nRimedio: aggiungi al file il blocco richiesto. Override (solo su autorizzazione "
               "esplicita del supervisore, da motivare nel commit message): aggiungi "
               "[RM-HOOK-OVERRIDE] al comando.")


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    tool = data.get("tool_name") or ""
    ti = data.get("tool_input") or {}

    if tool in ("Read", "Edit", "Write", "NotebookEdit", "Glob", "Grep"):
        path = norm(ti.get("file_path") or ti.get("notebook_path") or ti.get("path"))
        if QUAR in path:
            deny("BLOCCATO - quarantena impianto B: '%s' sta in OLD_NOT_USE_NOT_READ_FILES_"
                 "MODEL_4_CANALI/ e per decisione AC (11/06/2026) non va letto, citato ne' "
                 "copiato. Decision-record legittimo: 'Business Spec/FINDING "
                 "AUDIT_GOVERNANCE_4CANALI.md'." % path)
        if tool in ("Edit", "Write", "NotebookEdit") and ".claude/agents/" in path.lower():
            if not os.path.exists(os.path.join(root(), UNLOCK_FLAG)):
                deny("BLOCCATO - '.claude/agents/' e' governance protetta: la modifica dei ruoli "
                     "e' ammessa solo su autorizzazione esplicita del supervisore. Procedura: "
                     "creare il file '.claude/AGENTS_UNLOCK' (vuoto, untracked), eseguire la "
                     "modifica autorizzata, rimuovere il file.")
        sys.exit(0)

    if tool in ("Bash", "PowerShell"):
        cmd = str(ti.get("command") or "")
        if "RM-HOOK-OVERRIDE" in cmd:
            sys.exit(0)
        if QUAR in cmd and QUAR_READ_CMD.search(cmd):
            deny("BLOCCATO - il comando legge/copia file della quarantena impianto B (%s): "
                 "vietato da decisione AC 11/06/2026." % QUAR)
        if GIT_COMMIT.search(cmd):
            handle_commit(cmd)
        sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # fail-open: un bug del guard non deve fermare il lavoro
        sys.stderr.write("rm_guard: errore interno non bloccante: %r\n" % (exc,))
        sys.exit(0)
