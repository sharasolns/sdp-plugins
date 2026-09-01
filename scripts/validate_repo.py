#!/usr/bin/env python3
"""Validate the cross-platform SDP plugin without modifying the repository."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []

MCP_SERVERS = {
    "sdp-website-builder": "https://sdp-api.sdp-platform.com/mcp/website-builder",
    "sdp-products": "https://themes-production.sdp-platform.com/mcp/products",
    "sdp-listings": "https://themes-production.sdp-platform.com/mcp/listings",
    "sdp-custom-forms": "https://themes-production.sdp-platform.com/mcp/custom-forms",
}


def error(message: str) -> None:
    ERRORS.append(message)


def load_json(relative: str) -> dict:
    path = ROOT / relative
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        error(f"{relative}: invalid or unreadable JSON: {exc}")
        return {}


def check_path(owner: str, value: object) -> None:
    if not isinstance(value, str) or not value.startswith("./"):
        error(f"{owner}: expected a ./-prefixed relative path, got {value!r}")
        return
    target = (ROOT / value[2:]).resolve()
    try:
        target.relative_to(ROOT.resolve())
    except ValueError:
        error(f"{owner}: path escapes the plugin root")
        return
    if not target.exists():
        error(f"{owner}: referenced path does not exist: {value}")


for json_file in [
    ".agents/plugins/marketplace.json",
    ".claude-plugin/marketplace.json",
    ".mcp.json",
]:
    load_json(json_file)

manifest_paths = {
    "open": ".plugin/plugin.json",
    "claude": ".claude-plugin/plugin.json",
    "cursor": ".cursor-plugin/plugin.json",
    "codex": ".codex-plugin/plugin.json",
    "grok": ".grok-plugin/plugin.json",
}
manifests = {name: load_json(path) for name, path in manifest_paths.items()}

versions = {name: manifest.get("version") for name, manifest in manifests.items()}
if len(set(versions.values())) != 1 or None in versions.values():
    error(f"plugin manifest versions are not synchronized: {versions}")
else:
    version = next(iter(versions.values()))
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if f"## {version} " not in changelog:
        error(f"CHANGELOG.md has no entry for {version}")

for surface, manifest in manifests.items():
    if manifest.get("name") != "sdp":
        error(f"{surface} manifest name must be sdp")
    for field in ("skills", "mcpServers", "logo"):
        if field in manifest and isinstance(manifest[field], str):
            check_path(f"{surface}.{field}", manifest[field])
    interface = manifest.get("interface", {})
    if isinstance(interface, dict):
        for field in ("composerIcon", "logo", "logoDark"):
            if field in interface:
                check_path(f"{surface}.interface.{field}", interface[field])

skills_root = ROOT / "skills"
skill_dirs = sorted(path for path in skills_root.iterdir() if path.is_dir())
expected_skills = set(MCP_SERVERS)
found_skills = {path.name for path in skill_dirs}
if found_skills != expected_skills:
    error(f"skills directories must be {sorted(expected_skills)}, got {sorted(found_skills)}")

frontmatter_pattern = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
for skill_dir in skill_dirs:
    skill_file = skill_dir / "SKILL.md"
    openai_file = skill_dir / "agents" / "openai.yaml"
    if not skill_file.is_file():
        error(f"{skill_dir.name}: missing SKILL.md")
        continue
    if not openai_file.is_file():
        error(f"{skill_dir.name}: missing agents/openai.yaml")
        continue

    content = skill_file.read_text(encoding="utf-8")
    match = frontmatter_pattern.match(content)
    if not match:
        error(f"{skill_dir.name}: invalid YAML frontmatter boundary")
        continue

    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        key, separator, value = line.partition(":")
        if not separator:
            error(f"{skill_dir.name}: malformed frontmatter line: {line}")
            continue
        metadata[key.strip()] = value.strip().strip("\"'")

    if set(metadata) != {"name", "description"}:
        error(f"{skill_dir.name}: frontmatter must contain only name and description")
    if metadata.get("name") != skill_dir.name:
        error(f"{skill_dir.name}: frontmatter name does not match folder")
    if len(metadata.get("description", "")) < 40:
        error(f"{skill_dir.name}: description is too short for reliable discovery")

    openai = openai_file.read_text(encoding="utf-8")
    if f"${skill_dir.name}" not in openai:
        error(f"{skill_dir.name}: default_prompt must mention ${skill_dir.name}")
    expected_url = MCP_SERVERS.get(skill_dir.name)
    if expected_url and expected_url not in openai:
        error(f"{skill_dir.name}: missing hosted MCP URL {expected_url}")

markdown_link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
for markdown in ROOT.rglob("*.md"):
    if ".git" in markdown.parts:
        continue
    for target in markdown_link_pattern.findall(markdown.read_text(encoding="utf-8")):
        target = target.strip().strip("<>").split("#", 1)[0]
        if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
            continue
        resolved = (markdown.parent / target).resolve()
        if not resolved.exists():
            error(f"{markdown.relative_to(ROOT)}: broken local link {target}")

oauth_config = load_json(".mcp.json").get("mcpServers", {})
for name, url in MCP_SERVERS.items():
    entry = oauth_config.get(name)
    if entry != {"type": "http", "url": url}:
        error(f".mcp.json {name} must be {{\"type\": \"http\", \"url\": \"{url}\"}}")

if ERRORS:
    print("Repository validation failed:", file=sys.stderr)
    for item in ERRORS:
        print(f"- {item}", file=sys.stderr)
    raise SystemExit(1)

print(f"Repository validation passed: {len(manifests)} manifests, {len(skill_dirs)} skills")
