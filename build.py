#!/usr/bin/env python3
"""Generate the Lucario-coloured SVG headings and tags used by README.md, then rewrite the tag lines in README.md."""
import re
from pathlib import Path
from xml.sax.saxutils import escape

NAVY, INK, MUTED, DARK = "#2b3e50", "#f8f8f2", "#8a9bb0", "#252d38"
PALETTE = ["#d85740", "#67af5e", "#f4d858", "#6a97c9", "#c296f9", "#9fdefa"]  # red green yellow blue magenta cyan
FONT = "SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
ASSETS = Path("assets"); TAGS = ASSETS / "tags"

CATEGORIES = [
    ("Networking", ["WireGuard", "NetBird", "Pangolin", "Newt", "Cloudflare DNS", "DDNS", "SMB/CIFS"]),
    ("Identity & security", ["OIDC", "SAML", "Pocket ID", "Authlib", "Entra ID", "JumpCloud", "SentinelOne", "RBAC", "audit logs", "MFA/TOTP", "FIDO2", "age", "Android Keystore"]),
    ("Backups & storage", ["restic", "Backrest", "S3", "Backblaze B2", "ZFS", "nightly DB dumps", "config-as-code", "restore runbooks"]),
    ("Containers", ["Docker", "Compose", "buildx", "multi-arch", "GHCR", "Watchtower", "Portainer", "non-root images", "healthchecks"]),
    ("Platforms", ["Proxmox VE", "TrueNAS SCALE", "Ubuntu Server", "Windows Server", "Hetzner", "RackNerd"]),
    ("Observability & alerting", ["Zabbix", "Beszel", "CheckCle", "Uptime Kuma", "/proc sampling", "webhook run notifications", "Gotify", "ntfy", "Slack", "SMTP"]),
    ("Automation & CI", ["n8n", "MCP", "cron", "systemd", "Dagu", "GitHub Actions", "GoReleaser", "Forgejo"]),
    ("AI tooling", ["Claude Code", "OpenCode", "NanoClaw", "n8n AI agents", "MCP servers", "OpenRouter", "Open WebUI"]),
    ("Data", ["PostgreSQL", "SQLite", "Redis", "Valkey", "MariaDB", "Alembic"]),
    ("Languages", ["Python", "PowerShell 7", "Bash", "SQL"]),
    ("Microsoft 365 & Google Workspace", ["Graph API", "Exchange Online", "Teams", "SharePoint", "Intune", "Workspace Admin", "Google Vault"]),
    ("Commerce & ERP", ["Shopify Admin GraphQL", "Shopify Admin REST", "Shopify Storefront", "Amazon SP-API", "Amazon MWS", "Salesforce REST", "Salesforce SOAP", "Salesforce Bulk", "NetSuite SuiteQL", "SuiteTalk REST"]),
]
HEADINGS = [("technologies", "Technologies I know well", PALETTE[1]), ("what-i-do", "What I do", PALETTE[3])]

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def tag(text, fg, bg, bold=False):
    fs, cw, pad, h = 12, 7.3, 9, 22
    tw = round(len(text) * cw, 1); w = round(tw + pad * 2)
    weight = ' font-weight="700"' if bold else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(text)}">'
            f'<rect width="{w}" height="{h}" rx="4" fill="{bg}"/>'
            f'<text x="{pad}" y="15.5" font-family="{FONT}" font-size="{fs}"{weight} fill="{fg}" textLength="{tw}" lengthAdjust="spacingAndGlyphs">{escape(text)}</text></svg>')

def heading(text, color):
    fs, cw, h = 20, 12.1, 34
    tw = round(len(text) * cw, 1); w = round(tw + 36)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(text)}">'
            f'<text x="0" y="25" font-family="{FONT}" font-size="{fs}" font-weight="700" fill="{MUTED}">#</text>'
            f'<text x="24" y="25" font-family="{FONT}" font-size="{fs}" font-weight="700" fill="{color}" textLength="{tw}" lengthAdjust="spacingAndGlyphs">{escape(text)}</text></svg>')

def title():
    w, h = 880, 96
    strip = "".join(f'<rect x="{i*110}" y="{h-6}" width="110" height="6" fill="{c}"/>' for i, c in enumerate([DARK] + PALETTE + [INK]))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="dev-Blaze, DevOps / SRE / IT systems">'
            f'<clipPath id="c"><rect width="{w}" height="{h}" rx="8"/></clipPath>'
            f'<rect width="{w}" height="{h}" rx="8" fill="{NAVY}"/>'
            f'<text x="28" y="44" font-family="{FONT}" font-size="26" font-weight="700" fill="{PALETTE[1]}">dev-Blaze<tspan fill="{INK}">@</tspan><tspan fill="{PALETTE[1]}">homelab</tspan></text>'
            f'<text x="28" y="72" font-family="{FONT}" font-size="14" fill="{MUTED}">DevOps / SRE / IT systems</text>'
            f'<g clip-path="url(#c)">{strip}</g></svg>')

TAGS.mkdir(parents=True, exist_ok=True)
(ASSETS / "title.svg").write_text(title())
for key, text, color in HEADINGS:
    (ASSETS / f"h-{key}.svg").write_text(heading(text, color))

lines = []
for i, (cat, techs) in enumerate(CATEGORIES):
    color = PALETTE[i % len(PALETTE)]
    (TAGS / f"cat-{slug(cat)}.svg").write_text(tag(cat, DARK, color, bold=True))
    imgs = [f'<img src="assets/tags/cat-{slug(cat)}.svg" alt="{escape(cat)}:">']
    for t in techs:
        (TAGS / f"{slug(t)}.svg").write_text(tag(t, color, NAVY))
        imgs.append(f'<img src="assets/tags/{slug(t)}.svg" alt="{escape(t)}">')
    lines.append(" ".join(imgs))
block = "\n\n".join(lines)

readme = Path("README.md").read_text()
readme = re.sub(r"<!-- tags:start -->.*<!-- tags:end -->", f"<!-- tags:start -->\n{block}\n<!-- tags:end -->", readme, flags=re.S)
Path("README.md").write_text(readme)
print(f"wrote {len(list(TAGS.iterdir()))} tags, {len(HEADINGS)} headings, title")
