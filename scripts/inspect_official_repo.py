#!/usr/bin/env python
"""扫描官方克隆：列出入口、依赖、可能的数据下载与 CLI。不改仓库。"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "__pycache__", "data", ".venv", "node_modules", "wandb"}
KEY_FILES = [
    "README.md", "ReadMe.md", "readme.md", "README.rst",
    "requirements.txt", "environment.yml", "environment.yaml",
    "setup.py", "setup.cfg", "pyproject.toml", "Pipfile",
    "Makefile", "LICENSE",
]
ENTRY_GLOBS = [
    "main.py", "train.py", "run.py", "exp.py", "evaluate.py",
    "**/main.py", "**/train.py", "**/run.py", "scripts/*.sh",
    "*.sh", "**/train_*.py", "**/run_*.py",
]


def git_head(repo: Path) -> dict:
    def run(*args):
        return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()
    return {
        "head": run("rev-parse", "HEAD"),
        "branch": run("rev-parse", "--abbrev-ref", "HEAD"),
        "n_commits_shallow": run("rev-list", "--count", "HEAD"),
        "subject": run("log", "-1", "--format=%s"),
        "date": run("log", "-1", "--format=%ci"),
    }


def list_top(repo: Path) -> list[str]:
    return sorted(p.name + ("/" if p.is_dir() else "") for p in repo.iterdir() if p.name != ".git")


def read_text(path: Path, limit=4000) -> str:
    try:
        data = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    return data[:limit]


def find_files(repo: Path, names) -> list[str]:
    found = []
    for n in names:
        p = repo / n
        if p.exists():
            found.append(n)
    return found


def glob_rel(repo: Path, pattern: str, cap=40) -> list[str]:
    out = []
    for p in repo.glob(pattern):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        out.append(str(p.relative_to(repo)))
        if len(out) >= cap:
            break
    return out


def inspect(name: str) -> dict:
    repo = ROOT / "repro" / name
    if not (repo / ".git").exists():
        return {"name": name, "error": "missing clone"}
    info = {"name": name, "path": str(repo), "git": git_head(repo), "top": list_top(repo)}
    info["key_files"] = find_files(repo, KEY_FILES)
    readmes = [f for f in info["key_files"] if f.lower().startswith("readme")]
    info["readme_head"] = read_text(repo / readmes[0], 6000) if readmes else ""
    reqs = [f for f in info["key_files"] if "require" in f.lower() or f.startswith("environment") or f == "pyproject.toml"]
    info["deps_text"] = {f: read_text(repo / f, 3000) for f in reqs}
    entries = []
    for g in ENTRY_GLOBS:
        entries.extend(glob_rel(repo, g))
    info["entry_candidates"] = sorted(set(entries))[:60]
    info["sh_scripts"] = glob_rel(repo, "**/*.sh", 30)
    info["yml"] = glob_rel(repo, "**/*.{yml,yaml}", 30)
    info["n_py"] = sum(1 for _ in repo.rglob("*.py") if ".git" not in _.parts)
    return info


def main():
    names = sys.argv[1:]
    if not names:
        names = [line.split("\t")[1] for line in (ROOT / "repro" / "PREP_REGISTRY.tsv").read_text().splitlines()[1:] if line.strip()]
    out_dir = ROOT / "results" / "prep"
    out_dir.mkdir(parents=True, exist_ok=True)
    all_info = []
    for name in names:
        info = inspect(name)
        all_info.append(info)
        (out_dir / f"{name}_inspect.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"=== {name} ===")
        if "error" in info:
            print(info["error"])
            continue
        print("HEAD", info["git"]["head"], info["git"]["branch"], info["git"]["subject"])
        print("top", " ".join(info["top"][:25]))
        print("key", info["key_files"])
        print("entries", info["entry_candidates"][:20])
        print()
    (out_dir / "all_inspect.json").write_text(json.dumps(all_info, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
