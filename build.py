#!/usr/bin/env python3
"""Generate the Lucario-coloured SVGs used by README.md: title, headings, and the technologies table."""
import re, textwrap
from pathlib import Path
from xml.sax.saxutils import escape

NAVY, INK, MUTED, DARK = "#2b3e50", "#f8f8f2", "#8a9bb0", "#252d38"
PALETTE = ["#d85740", "#67af5e", "#f4d858", "#6a97c9", "#c296f9", "#9fdefa"]  # red green yellow blue magenta cyan
FONT = "SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
ASSETS = Path("assets")

CATEGORIES = [
    ("Networking", ["WireGuard", "NetBird", "Pangolin", "Cloudflare", "UniFi", "Meraki", "Sophos", "Fortinet", "OPNsense/pfSense"]),
    ("Identity & security", ["OIDC", "SAML", "Pocket ID", "Authlib", "Entra ID", "JumpCloud", "SentinelOne", "RBAC", "audit logs", "MFA/TOTP", "FIDO2", "age", "Android Keystore"]),
    ("Backups & storage", ["restic", "Backrest", "S3", "Backblaze B2", "ZFS", "nightly DB dumps", "config-as-code", "restore runbooks"]),
    ("Containers", ["Docker", "Compose", "buildx", "multi-arch", "Portainer", "healthchecks"]),
    ("Platforms", ["Proxmox VE", "TrueNAS SCALE", "Ubuntu Server", "Windows Server", "Hetzner", "RackNerd"]),
    ("Observability & alerting", ["Zabbix", "Beszel", "CheckCle", "Uptime Kuma", "/proc sampling", "webhook run notifications", "Gotify", "ntfy", "Slack", "SMTP"]),
    ("Automation & CI", ["n8n", "MCP", "cron", "systemd", "Dagu", "GitHub Actions", "GoReleaser", "Forgejo"]),
    ("AI tooling", ["Claude Code", "OpenCode", "NanoClaw", "n8n AI agents", "MCP servers", "OpenRouter", "Open WebUI"]),
    ("Data", ["PostgreSQL", "SQLite", "Redis", "Valkey", "MariaDB", "Alembic"]),
    ("Languages", ["Python", "PowerShell 7", "Bash", "SQL"]),
    ("Microsoft 365 & Google Workspace", ["Graph API", "Exchange Online", "Teams", "SharePoint", "Intune", "Workspace Admin", "Google Vault"]),
    ("Commerce & ERP", ["Shopify Admin GraphQL", "Shopify Admin REST", "Shopify Storefront", "Amazon SP-API", "Amazon MWS", "Salesforce REST", "Salesforce SOAP", "Salesforce Bulk", "NetSuite SuiteQL", "SuiteTalk REST"]),
]
HEADINGS = [("what-i-do", "What I do", PALETTE[1]), ("technologies", "Technologies I know well", PALETTE[3])]

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def table():
    w, pad, cat_w, lh, rp = 880, 20, 244, 19, 11
    fs, cw = 13, 9.2                      # worst-case monospace glyph width (0.7em) so wrapped lines fit in any renderer
    cat_wrap = int((cat_w - pad) / cw)    # 28 chars
    tech_wrap = int((w - pad - cat_w - pad) / cw) - 2   # 72 chars
    rows, y = [], 0
    for i, (cat, techs) in enumerate(CATEGORIES):
        cl = textwrap.wrap(cat, cat_wrap); tl = textwrap.wrap(", ".join(techs), tech_wrap)
        rh = rp * 2 + lh * max(len(cl), len(tl))
        rows.append((cl, tl, PALETTE[i % len(PALETTE)], y, rh)); y += rh
    h = y
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Technologies I know well">',
           f'<clipPath id="c"><rect width="{w}" height="{h}" rx="8"/></clipPath><g clip-path="url(#c)">',
           f'<rect width="{w}" height="{h}" fill="{NAVY}"/>']
    def text(x, y, line, fill, bold=False):
        weight = ' font-weight="700"' if bold else ""
        return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{fs}"{weight} fill="{fill}">{escape(line)}</text>'
    for i, (cl, tl, color, y0, rh) in enumerate(rows):
        if i % 2: out.append(f'<rect y="{y0}" width="{w}" height="{rh}" fill="#30455a"/>')
        out.append(f'<rect y="{y0}" width="5" height="{rh}" fill="{color}"/>')
        ty = y0 + rp + 14
        out += [text(pad, ty + j * lh, line, color, bold=True) for j, line in enumerate(cl)]
        out += [text(pad + cat_w, ty + j * lh, line, INK) for j, line in enumerate(tl)]
    out.append('</g></svg>')
    return "\n".join(out)

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
            f'<text x="28" y="44" font-family="{FONT}" font-size="26" font-weight="700" fill="{PALETTE[1]}">dev-Blaze</text>'
            f'<text x="28" y="72" font-family="{FONT}" font-size="14" fill="{MUTED}">DevOps / SRE / IT systems</text>'
            f'<g clip-path="url(#c)">{strip}</g></svg>')

# write each SVG as <name>.<content-hash>.svg (GitHub's image caches ignore query strings,
# so a changed file needs a new filename), drop stale versions, and point README.md at the new names
import hashlib
readme = Path("README.md").read_text()
outputs = {"title": title(), "technologies": table(), **{f"h-{k}": heading(t, c) for k, t, c in HEADINGS}}
for name, svg in outputs.items():
    v = hashlib.md5(svg.encode()).hexdigest()[:8]
    for old in ASSETS.glob(f"{name}.*.svg"):
        if old.name != f"{name}.{v}.svg": old.unlink()
    (ASSETS / f"{name}.{v}.svg").write_text(svg)
    readme = re.sub(rf'src="assets/{name}(\.[0-9a-f]{{8}})?\.svg(\?v=[0-9a-f]+)?"', f'src="assets/{name}.{v}.svg"', readme)
Path("README.md").write_text(readme)
print("wrote", ", ".join(sorted(x.name for x in ASSETS.glob("*.svg"))))
