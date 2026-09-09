<p align="center">
  <img src="assets/neofetch.svg" width="880" alt="neofetch-style card: dev-Blaze@homelab, DevOps / SRE / IT systems, 80+ compose stacks, Lucario palette">
</p>

I'm Blaze. I keep systems boring on purpose: backups that actually restore, deploys nobody has to babysit, and dashboards that are green because nothing is on fire, not because nobody is looking.

## What I run

Two sites plus a VPS, joined by a WireGuard mesh, with nothing listening on a public port. Everything is declarative Docker Compose, one directory per stack, prefixed by host, versioned in git.

| Concern | How it's handled |
| --- | --- |
| Ingress | Pangolin + Newt tunnels. Services attach to the tunnel network instead of publishing ports. Cloudflare DDNS covers the rest. |
| Network | NetBird (WireGuard) mesh between home, the VPS, and work sites. Gluetun VPN-gates the download stack. |
| Identity | Pocket ID as the OIDC provider. One login for every app that supports it. |
| Observability | Beszel hub + agents (including a GPU agent), CheckCle, Uptime Kuma. |
| Backups | Backrest (restic) to a NAS over SMB. Automation workflows exported to git nightly, with a written restore runbook. |
| Updates | Watchtower per host on a 02:00 cron, email on change. |
| Scheduling | Dagu for DAG jobs. A self-built script runner for cron with locks, timeouts, and missed-run detection. |
| Automation | Four n8n instances (two personal, two work) running AI agents that call MCP tools. |
| Apps | Immich, Paperless-ngx, Jellyfin + the \*arr stack, Vaultwarden, Outline, Forgejo, Open WebUI, Mealie, Audiobookshelf, and a few game servers. |

Hypervisor is Proxmox VE with TrueNAS SCALE and Ubuntu Server guests.

## What I do

- **Ship containers properly** — multi-stage Dockerfiles, non-root users, `HEALTHCHECK`s, `depends_on: service_healthy`, migrations at container start, multi-arch (amd64/arm64) images on GHCR via buildx, and single static Go binaries with GoReleaser when a container is overkill.
- **Release without ceremony** — scripted pipelines that lint, test, build, push, tag, and write release notes in one command. GitHub Actions for CI (`go test -race`, golangci-lint, Pester, PSScriptAnalyzer). `curl | bash` installers that double as updaters and verify checksums. Self-hosted browser-extension distribution with MDM force-install and an `updates.xml` feed.
- **Keep the network closed** — WireGuard mesh instead of port forwards, tunnel-based ingress, DDNS, VPN-gated egress, OIDC in front of everything, RBAC with audit logs, TOTP.
- **Handle secrets like they matter** — age-encrypted vaults unlocked by Touch ID or FIDO2, keys that never touch disk, redaction in logs and webhook payloads, `.env` files at mode 600, git sync that refuses to push plaintext.
- **Make failure survivable** — restic backups to a NAS, config-as-code with diff-only commits, written restore runbooks, retry queues for outbound webhooks, per-job locks and timeouts, missed-run detection, `--dry-run` and resumable state on anything that changes the world.
- **Watch the fleet** — host and container metrics, uptime probes, GPU agents, `/proc` CPU and RSS sampling per job, run history with sparklines, and every scheduled job reporting exit code, duration, and a log tail to a webhook.
- **Glue the business together** — n8n workflows with AI agents that call MCP tools, then hand results to people over email. Microsoft Graph with app-only certificate auth, Exchange Online, Teams, SharePoint, Intune, JumpCloud, Google Workspace with domain-wide delegation, Google Vault, Shopify Admin GraphQL, Amazon SP-API, NetSuite SuiteQL over OAuth 2.0 M2M.
- **Automate the tenant** — onboarding that creates the user, MFA, groups, device binding, and licence in one run. Offboarding that takes a Vault backup and verifies it before it removes anything. Mailbox, calendar, and transcript pipelines that run unattended and page only on non-zero exit.
- **Build the tooling I wish existed** — terminal UIs in Go (Bubble Tea, Lip Gloss) and PowerShell 7, MCP and REST servers behind bearer tokens, systemd units, FastAPI apps with SQLAlchemy and Alembic, Android and Wear OS apps that talk to self-hosted automation, Chrome extensions that POST to webhooks.

## Toolbox

| | |
| --- | --- |
| Languages | Go, Python, PowerShell 7, Kotlin, TypeScript, Bash |
| Platforms | Proxmox VE, TrueNAS SCALE, Ubuntu Server, Hetzner and RackNerd VPS, macOS |
| Containers | Docker, Compose, buildx, GHCR, Watchtower, Portainer-style stack envs |
| Network | WireGuard, NetBird, Pangolin/Newt, Cloudflare, Gluetun |
| Identity | OIDC (Pocket ID, Authlib), RBAC, TOTP, FIDO2, age, Android Keystore |
| Data | PostgreSQL, SQLite, Redis/Valkey, MariaDB, restic, S3/B2 |
| Observability | Beszel, CheckCle, Uptime Kuma, webhook run reporting |
| Automation | n8n, MCP, cron, systemd timers, Dagu, GitHub Actions, GoReleaser |
| Microsoft 365 | Graph API, Exchange Online, Teams, SharePoint, Intune, JumpCloud |
| Google | Workspace Admin, Vault, domain-wide delegation |
| Commerce | Shopify Admin GraphQL, Amazon SP-API, NetSuite SuiteQL |

## Elsewhere

GitHub is the best place to find me.
<!-- add a site, email, or LinkedIn here -->
