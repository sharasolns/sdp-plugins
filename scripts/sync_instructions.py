#!/usr/bin/env python3
"""Copy instruction docs from sibling SDP sources; --check detects drift."""
import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--backend', type=Path, default=ROOT.parent / 'sdp-cms-backend')
parser.add_argument('--themes', type=Path, default=ROOT.parent / 'sdp-themes')
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
# Instantiate the pure exporter without booting Laravel or touching databases.
php = r'''
require $argv[1].'/app/Services/Mcp/WebsiteBuilderInstructionCatalog.php';
require $argv[1].'/app/Services/Mcp/WebsiteBuilderInstructionDocs.php';
$docs = new App\Services\Mcp\WebsiteBuilderInstructionDocs(new App\Services\Mcp\WebsiteBuilderInstructionCatalog);
echo json_encode($docs->files(), JSON_THROW_ON_ERROR);
'''
files = json.loads(subprocess.check_output(['php', '-r', php, str(args.backend.resolve())], text=True))
# The shared backend exporter still labels its workflows with the legacy endpoint.
# Adapt routing for this plugin while preserving the catalog's workflow content.
manager_guidance = (
    'This plugin connects to Website Manager MCP (`/mcp/website-manager`). '
    'Use directly listed tools when available. Discover other tools with `search_tools`, '
    'then call `execute_tools` with the exact names and arguments returned by search. '
    'Do not assume workflow tool names are directly exposed. Follow the live server '
    'instructions and tool schemas when they differ from this source snapshot.\n\n'
)
for relative in list(files):
    files[relative] = files[relative].replace('/mcp/website-builder', '/mcp/website-manager').replace(
        'Server: `website-builder`', 'Server: `website-manager`')
    if relative.endswith('SKILL.md'):
        files[relative] = files[relative].replace('# SDP Website Builder\n\n', '# SDP Website Builder\n\n' + manager_guidance)
for skill, resource in [('products', 'Products'), ('listings', 'Listings'), ('courses', 'Courses'), ('custom-forms', 'CustomForms')]:
    source = args.themes / f'app/Mcp/Resources/{resource}InstructionsResource.php'
    match = re.search(r"<<<'MD'\n(.*?)\nMD\);", source.read_text(), re.S)
    if not match:
        raise SystemExit(f'Cannot extract Markdown from {source}')
    files[f'skills/sdp-{skill}/references/instructions.md'] = match[1].replace('/mcp/website-builder', '/mcp/website-manager') + '\n'

stale = []
for relative, contents in files.items():
    target = ROOT / relative
    if target.exists() and target.read_text() == contents:
        continue
    stale.append(relative)
    if not args.check:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(contents)
        print(f'Wrote {relative}')
if args.check and stale:
    raise SystemExit('Instruction docs are out of date: ' + ', '.join(stale))
print(f'Instruction docs synchronized: {len(files)} files')
