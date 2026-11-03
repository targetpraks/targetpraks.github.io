#!/usr/bin/env python3
"""CI twin of `pages-link-check` lenses 1 and 2 — run by .github/workflows/pages-link-guard.yml.

Why this exists at all: the checkout's own hooks (`tools/pages_commit_guard.py`) only see a commit
made *on this Mac*. A pull request merged on github.com never runs them, and that is exactly how a
published page was renamed out from under a live link on 2026-11-02 — commit 83d1afda, authored as
Ricardo on the web, renamed `…-aac-supply-and-install-…-business-2.html` and rewrote its ledger row
in the same commit, so the local ledger went on reporting a complete site while the held URL 404'd.
This runs where the merge happens, so the same accident fails a build within a minute.

Two checks, and neither touches the vault (CI cannot see it; the local tool checks that lens):

  1. every row in .publish-ledger.tsv answers HTTP 200
  2. every page name that EVER held a ledger row still exists in the checkout — a name that was
     published is a link somebody holds, so it may be *aliased* away but never simply deleted

The local tool remains the full audit: python3 ~/.config/maio-stack/tools/pages_link_check.py check
"""

import concurrent.futures
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

LEDGER = ".publish-ledger.tsv"
WORKERS = 12
TIMEOUT = 20
UA = "maio-pages-link-guard/1.0 (+github actions)"


def ledger_rows():
    rows = []
    try:
        with open(LEDGER, encoding="utf-8", errors="replace") as f:
            for line in f:
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                parts = line.rstrip("\n").split("\t")
                if len(parts) >= 2 and parts[0].strip():
                    rows.append((parts[0].strip(), parts[1].strip()))
    except OSError:
        pass
    return rows


def status(url):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method,
                                         headers={"User-Agent": UA, "Cache-Control": "no-cache"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.status
        except urllib.error.HTTPError as e:
            if e.code == 405 and method == "HEAD":
                continue
            return e.code
        except Exception:                                   # noqa: BLE001
            return None
    return None


def ever_published():
    """{name: the commit that last dropped it} from the ledger's whole patch history."""
    try:
        out = subprocess.run(["git", "log", "-p", "--format=%H", "--", LEDGER],
                             capture_output=True, text=True, timeout=180)
    except subprocess.TimeoutExpired:
        return {}
    removed, sha = {}, None
    for line in (out.stdout or "").splitlines():
        if re.fullmatch(r"[0-9a-f]{40}", line.strip()):
            sha = line.strip()
            continue
        if line.startswith("---") or line.startswith("+++"):
            continue
        if not line.startswith(("-", "+")):
            continue
        cell = line[1:].split("\t")[0].strip()
        if cell.endswith(".html"):
            removed[cell] = sha if line.startswith("-") else removed.get(cell, sha)
    return removed


def main():
    dead, gone = [], []
    rows = ledger_rows()
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for (name, url), code in zip(rows, ex.map(lambda r: status(r[1]), rows)):
            if code != 200:
                dead.append((name, url, code))
    for name, sha in sorted(ever_published().items()):
        if not os.path.exists(name):
            gone.append((name, sha))
    if dead:
        print("::error title=Published page is dead::{} of {} published URLs do not answer 200"
              .format(len(dead), len(rows)))
        for name, url, code in dead:
            print("::error file={}::{} returns {} — repair with `pages-link-check restore {} "
                  "--from <the document>` or `alias {} --to <the page it moved to>`"
                  .format(name, url, code, name, name))
    if gone:
        print("::error title=A published name was deleted::{} published page name(s) no longer "
              "exist in the checkout".format(len(gone)))
        for name, sha in gone:
            print("::error file={}::the ledger row for {} went in commit {} and the page is not "
                  "in this checkout — alias it to where the document lives now".format(
                      name, name, (sha or "")[:8]))
    if dead or gone:
        return 1
    print("ok — {} published URLs answer 200 and every published name still exists"
          .format(len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
