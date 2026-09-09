<p align="center">
  <img src="assets/neofetch.svg" width="880" alt="neofetch-style card: dev-Blaze@homelab, DevOps / SRE / IT systems, 80+ compose stacks, Lucario palette">
</p>

I'm Blaze. I keep systems boring on purpose: backups that actually restore, deploys nobody has to babysit, and dashboards that are green because nothing is on fire, not because nobody is looking.

## What I run

Two sites plus a VPS, joined by a WireGuard mesh, with nothing listening on a public port. Everything is declarative Docker Compose, one directory per stack, prefixed by host.

| Concern | How it's handled |
| --- | --- |
| Ingress | Pangolin + Newt tunnels. Services attach to the tunnel network instead of publishing ports. Cloudflare DDNS covers the rest. |
| Network | NetBird (WireGuard) mesh between home, the VPS, and work sites. Gluetun VPN-gates the download stack. |
| Identity | Pocket ID as the OIDC provider. One login for every app that supports it. |
| Observability | Beszel hub + agents (including a GPU agent), CheckCle, Uptime Kuma. |
| Backups | Backrest (restic) to a NAS over SMB. n8n workflows exported to git nightly, with a written restore runbook. |
| Updates | Watchtower per host on a 02:00 cron, email on change. |
| Scheduling | Dagu for DAG jobs. Scriptorium for script cron with locks, timeouts, and missed-run detection. |
| Automation | Four n8n instances (two personal, two work) running AI agents that call MCP tools. |
| Apps | Immich, Paperless-ngx, Jellyfin + the \*arr stack, Vaultwarden, Outline, Forgejo, Open WebUI, Mealie, Audiobookshelf, and game servers (Crafty, Foundry VTT, AzerothCore). |

Hypervisor is Proxmox VE with TrueNAS SCALE and Ubuntu Server guests.

## Things I've built

- **[Scriptorium](https://github.com/yshah-aromatech/scriptorium)** — a single-binary Go TUI that runs PowerShell and Python scripts on a server. Per-script venvs and module dirs, cron in a managed crontab block, per-script locks and timeouts, CPU/RSS sampling from `/proc`, secret redaction, n8n webhook reporting with an on-disk retry queue, an MCP + REST server behind a bearer token, systemd install, GoReleaser releases, and a `curl | bash` installer that doubles as the updater.
- **[clavis](https://github.com/armtch-dev/clavis)** — SSH connection manager TUI with an age-encrypted vault, 15 s reachability probes with latency sparklines, Touch ID or FIDO2 unlock, and guarded encrypted git sync that refuses to push plaintext.
- **[asset-manager](https://github.com/armtch-dev/asset-manager)** — self-hosted IT asset management: lifecycle, assignments, licences, QR labels. FastAPI, multi-stage Dockerfile, non-root, healthcheck, multi-arch GHCR image, JumpCloud and Intune sync, TOTP.
- **[alfred](https://github.com/dev-Blaze/alfred)** + **[alfred-companion](https://github.com/dev-Blaze/alfred-companion)** — Android and Wear OS voice assistant that replaces the system assistant and talks to a self-hosted n8n AI agent. Kotlin, Jetpack Compose, credentials encrypted with the Android Keystore.
- **[azerothcore-docker](https://github.com/dev-Blaze/azerothcore-docker)** — AzerothCore with Playerbots and MySQL in one container, prebuilt on GHCR.
- **[homepage](https://github.com/dev-Blaze/homepage)** — fork of gethomepage/homepage with a Yahoo Finance widget (quote-only proxy, unit test) and my own GHCR build.
- **[powershell-scripts-tui](https://github.com/dev-Blaze/powershell-scripts-tui)** — the original pure-PowerShell 7 TUI that became Scriptorium. Same idea, no Go.

Smaller: [dropout-downloader](https://github.com/dev-Blaze/dropout-downloader) (Chromium extension), [rogers-monarch-converter](https://github.com/dev-Blaze/rogers-monarch-converter) (in-browser CSV converter that learns categories from your own export).

## Automation I lean on

n8n does the glue. A few flows that earn their keep:

- **Amazon ↔ NetSuite reconciliation** — a form upload kicks off an AI agent that calls Scriptorium over MCP to run the reconciliation script, checks the result, and emails the workbook (or the failure) through Outlook.
- **Run reporting** — every scheduled script POSTs exit code, duration, CPU/memory, and a log tail to a webhook. Failures get noticed. Successes get graphed.
- **Voice to task** — Alfred sends speech to a webhook. An agent decides whether it's a task, a note, or a conversation, and replies over TTS.
- **Invoices** — a Chrome extension turns any invoice page into a PDF and POSTs it to a header-authed webhook. Rolled out by MDM policy, updated from a self-hosted `updates.xml`.
- **Backups of the backups** — a Python job pulls every workflow from every n8n instance and commits the diffs to git, because native source control is enterprise-only and a backup workflow inside n8n dies with the instance.

## Day job

IT systems and automation for a company that manufactures and sells online. Internal apps ship as containers (multi-stage builds, non-root, healthchecks, OIDC + RBAC + audit logs) through a scripted release pipeline: lint, tests, buildx multi-arch, GHCR push, tag, release notes. The rest is Microsoft 365 and Google Workspace automation in PowerShell and Python: app-only Graph auth, Exchange Online, Teams transcript pipelines, JumpCloud onboarding, and offboarding that takes a Vault backup before it removes a licence. Anything that changes state gets a `--dry-run` and resumable state.

## Elsewhere

GitHub is the best place to find me.
<!-- add a site, email, or LinkedIn here -->
