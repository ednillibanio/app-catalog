English | [Português](dev-environment.pt-BR.md)

# Local development environment

This standard applies to the local development environment of an application repository: the tools a contributor installs, the services started on their machine, the configuration that differs between machines and the commands they run every day. It sets how an application supports several operating systems without one environment breaking another, and how each environment's guide states whether it was validated. An application records its supported environments, services, ports, variables, exact versions and stricter rules in its own repository, as described in [Using these standards](README.md#using-these-standards).

The examples use the neutral `inventory` vocabulary of the [Java/Quarkus backend](java-quarkus-backend.md) standard, Make as the task runner and Docker Compose for services. Make and Compose are examples, not requirements. Snippets marked "illustrative" show a shape and are not meant to run on their own; the others were run when this standard changed, as recorded in its iteration evidence.

## 1. Supported environments

Each application declares the environments it supports, in its agent instructions and in its development guide. It chooses from this reference set and names the exact operating system versions and tools itself:

| Environment | Typical setup |
| --- | --- |
| macOS | A container runtime such as Colima with the Docker CLI, or Docker Desktop; tools from a package manager such as Homebrew |
| Linux virtual machine | A VM managed by a tool such as Vagrant, with Docker or Podman inside it |
| Linux | Native Docker or Podman |
| WSL2 | A Linux distribution under Windows, with Docker or Podman |
| Windows | PowerShell with Docker Desktop |

Every supported environment has a guide (§11), a setup script (§5), a doctor check (§6) and the common commands (§8). An environment that lacks one of them is an exception and records the owner, reason, scope, expiry or review date and tracking issue required by the [standards index](README.md); its guide documents the manual steps that replace what is missing and its validation state is `Not validated` (§11). This standard grants no standing exception to any environment.

## 2. Repository files

| File | Role |
| --- | --- |
| `.env.example` | Versioned. Lists every variable that may differ between machines, with its default |
| `.env` | Local and ignored by Git. Holds this machine's values |
| Compose file (for example `compose.yaml`) | Versioned. Defines the development services |
| Task runner file (for example `Makefile`) | Versioned. Defines the common commands (§8) |
| `scripts/<environment>/` | Versioned. Setup, doctor and bootstrap scripts of one environment |
| Version pin files (for example `.nvmrc`, `.sdkmanrc`, `packageManager` in `package.json`, build tool wrapper) | Versioned. The single source of each tool version (§4) |
| `.gitattributes` | Versioned. Line endings for scripts (§9) |
| `docs/operations/` (or the application's equivalent) | One guide per environment and one shared guide (§11) |

## 3. Configuration and `.env`

1. Differences between environments and machines live only in the local `.env`. Versioned files keep values that work everywhere, and environment-specific choices are variables with a default.
2. `.env` is never committed. `.gitignore` excludes it, and the repository's hooks reject it.
3. `.env.example` documents every variable: purpose, default, when to change it and which commands read it. A variable that is read but missing from `.env.example` is a defect.
4. The project works without `.env`: every variable has a development default in the file that reads it.
5. `.env` uses a portable subset that Compose and a POSIX shell sourcing the file read the same way: one `NAME=value` per line, with a name made of letters, digits and underscores that does not start with a digit, and `#` comments on their own lines. A value is either unquoted and made only of letters, digits and the characters `_ . - / : , @ + =`, or wrapped whole in single or double quotes, with no `$`, backslash, backtick, quote character or line break inside. There is no variable expansion, command substitution, escape sequence or multi-line value. `.env.example` and `.env` use LF line endings, because a shell keeps a carriage return in the value: `.gitattributes` enforces it for `.env.example` (§9), and the doctor check reports a `.env` that contains carriage returns (§6).
6. The task runner and the Compose file read the same `.env`. A value derived from other variables (for example, a URL built from a port) is computed in one place, usually the task runner.
7. The application documents precedence when a variable is already set in the shell. In the example below, a command run through the task runner takes the `.env` value, because it sources `.env` before calling Compose, while a direct Compose call lets the shell value win.
8. A direct command that bypasses the task runner (for example, the build tool run from a subfolder) needs the variables it reads set in the shell. The shared guide lists them.

```dotenv
# -----------------------------------------------------------------------------
# Compose (read by the Makefile)
# -----------------------------------------------------------------------------
# Default: Docker. For Podman, uncomment both lines.
# Some podman-compose versions do not support the --wait flag used by `make up`.
# COMPOSE=podman-compose
# COMPOSE_UP_FLAGS=-d

# Address where services publish their ports. Keep 127.0.0.1 unless a guide
# says otherwise for its environment.
# BIND_ADDRESS=127.0.0.1

# -----------------------------------------------------------------------------
# PostgreSQL (development credentials only)
# -----------------------------------------------------------------------------
POSTGRES_DB=inventory
POSTGRES_USER=inventory
POSTGRES_PASSWORD=inventory-dev
# Published host port. Change it when the default port is occupied.
POSTGRES_PORT=5432
```

## 4. Tool versions

1. Each tool version is pinned once, in a file the repository already uses for that tool: a runtime version file, the `packageManager` field enforced through Corepack, the build tool wrapper, or an image tag in the Compose file.
2. Setup scripts, doctor checks and CI read those files; they do not repeat the versions.
3. The build tool runs through its wrapper (for example `mvnw`), so contributors do not install it separately.
4. Images use fully qualified names and a tag (for example `docker.io/library/postgres:<tag>`). Podman does not resolve short names the way Docker does.
5. Selecting the pinned runtime does not depend on a shell hook being enabled; the task runner sets it explicitly when it can.

## 5. Setup

Each supported environment has a setup script that installs or configures what that environment needs.

1. It is idempotent: each step checks before acting, and a second run changes nothing.
2. It supports `--dry-run`, which prints what it would do without changing anything.
3. It never deletes data, `.env` or volumes, and never replaces a file it did not create.
4. It does not install the base package manager or SDK manager of the operating system; it tells the contributor how to install it and stops.
5. On the contributor's own machine it does not escalate privileges and does not silently change global defaults (default runtime, global container context, shell profile). When a change is needed, it says so and asks or prints the command.
6. A provisioner that runs inside a disposable VM may use privileged steps and set the VM's defaults; its header says so.
7. It ends by pointing to the doctor check (§6).

Illustrative: a check-before-install step with dry-run support.

```bash
install_if_missing() {
  local command_name="$1"
  shift
  if command -v "$command_name" >/dev/null 2>&1; then
    echo "[ OK ] $command_name already installed"
  elif [[ "${DRY_RUN:-0}" == 1 ]]; then
    echo "[PLAN] would run: $*"
  else
    "$@"
  fi
}

install_if_missing colima brew install colima
```

## 6. Doctor

Each supported environment has a doctor check.

1. It only reads; it installs and changes nothing.
2. It checks each prerequisite: container runtime and Compose, each pinned runtime version, the package manager version, the build tool wrapper and anything else the environment needs.
3. It prints one line per check and, for each failure, the command or step that fixes it.
4. It exits with a non-zero status when a required check fails, so scripts and contributors can rely on it. Optional findings are warnings and do not change the exit status.

A partial example: a real doctor check also covers the package manager, the build tool wrapper and the other prerequisites of its environment.

```bash
#!/usr/bin/env bash
# Read-only environment check. Exits 1 when a required check fails.
set -euo pipefail

failures=0

check() {
  local description="$1" fix="$2"
  shift 2
  if "$@" >/dev/null 2>&1; then
    echo "[ OK ] $description"
  else
    echo "[FAIL] $description -> $fix" >&2
    failures=$((failures + 1))
  fi
}

# Accepts a numeric pin such as 26, 26.13 or v26.13.0 in .nvmrc.
node_matches_nvmrc() {
  local pin current
  pin="$(tr -d '[:space:]v' < .nvmrc)"
  current="$(node --version)"
  [[ "$current" == "v$pin" || "$current" == "v$pin."* ]]
}

check "container runtime responds" "start the container runtime" docker info
check "Compose is available" "install the Compose plugin" docker compose version
env_has_lf_endings() {
  [[ -e .env || -L .env ]] || return 0
  [[ -f .env && -r .env ]] || return 1
  local status=0
  grep -q $'\r' .env || status=$?
  # grep exits 1 when no carriage return is found; 0 or an error fails.
  [[ "$status" -eq 1 ]]
}

check "Node matches .nvmrc" "run the setup command" node_matches_nvmrc
check ".env uses LF line endings" "convert .env to LF line endings" env_has_lf_endings

if ((failures > 0)); then
  echo "$failures check(s) failed." >&2
  exit 1
fi
echo "All checks passed."
```

## 7. Bootstrap

A bootstrap command is recommended: one command that takes a fresh clone to a working environment.

1. It runs setup, starts the services, prepares what the tests need (for example, a test database) and ends with the doctor check.
2. It creates `.env` from `.env.example` only when `.env` is absent. It keeps an existing `.env` and existing data volumes.
3. It may adjust the values of a `.env` it has just created (for example, choosing a free port when a default port is occupied); it does not rewrite an existing `.env`, and it reports the variable to change instead.
4. A change to global state that it needs (for example, a container context) applies only to its own commands, or is restored when it exits.

```bash
if [[ ! -e .env ]]; then
  cp .env.example .env
  chmod 600 .env
  echo "Created .env from .env.example."
else
  echo "Keeping the existing .env."
fi
```

## 8. Common commands

Every supported environment offers the same minimum command set, with the same names and the same effect, through a task runner or a wrapper script that runs there. Direct commands written in a guide document what a command does; they do not replace it.

| Command | Effect |
| --- | --- |
| `help` | Lists the available commands with a one-line description |
| `setup` | Installs missing tools; idempotent (§5) |
| `doctor` | Checks the environment without changing it (§6) |
| `up` | Starts the development services and waits for their health checks, or tells how to check readiness when the Compose implementation cannot wait |
| `down` | Stops the services and keeps their data volumes |
| `test` | Runs the test suites |
| `dev` | Runs the development servers |
| `check` | Runs the build, lint and test checks that CI also runs, and states which CI jobs it does not cover |

1. An application with several components may split `test` and `dev` per component (for example `backend-test` and `frontend-dev`), as long as the names are the same in every environment.
2. A command that deletes data, such as removing volumes, has its own explicit name and its description says that it is destructive. No command in the minimum set deletes data.
3. A `smoke` command, which checks the running application end to end (for example, a real sign-in in a browser), is recommended.
4. `help` is the default command.

Illustrative: part of a Makefile.

```make
# .env is read by the shell, not by Make, so quoted values keep shell meaning.
LOAD_ENV := $(if $(wildcard .env),set -a && . ./.env && set +a &&)
COMPOSE_CMD := $${COMPOSE:-docker compose}

.DEFAULT_GOAL := help
.PHONY: help up ps down clean-data

help: ## List the available commands
	@grep -hE '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*## "}; {printf "  %-12s %s\n", $$1, $$2}'

up: ## Start the services; wait for health checks when the flags include --wait
	$(LOAD_ENV) flags="$${COMPOSE_UP_FLAGS:--d --wait}" && \
		$(COMPOSE_CMD) up $$flags && \
		case " $$flags " in *" --wait "*) ;; \
		*) echo "Not waiting for health checks: run 'make ps' until every service is healthy." ;; esac

ps: ## Show the services and their health
	$(LOAD_ENV) $(COMPOSE_CMD) ps

down: ## Stop the services and keep their data volumes
	$(LOAD_ENV) $(COMPOSE_CMD) down

clean-data: ## DESTRUCTIVE: stop the services and delete their data volumes
	$(LOAD_ENV) $(COMPOSE_CMD) down -v
```

## 9. Compatibility across environments

1. The Compose file works with Docker and Podman: fully qualified image names (§4), the `z` option on bind mounts for SELinux hosts, health checks on every service, and readiness that does not depend only on `--wait`.
2. Services publish their ports on `127.0.0.1` by default. Wider binding is opt-in through a `.env` variable and documented with its risk (§13).
3. Ports are variables with defaults (§3), so a contributor can move a service off an occupied port without editing versioned files.
4. A setting that one environment needs and the others tolerate stays in the versioned file, with a comment that names the environment and the reason. It is not removed by a contributor in another environment.
5. For a VM, the application documents where the working tree lives. A clone inside the VM is the option when shared folders cause problems with symlinks, permissions or performance. Under WSL2, keep the working tree in the Linux file system rather than under `/mnt/c`, as Microsoft's WSL documentation recommends for performance.
6. Shell scripts, the task runner file and other files run inside Linux keep LF line endings on every checkout, including Windows; `.gitattributes` enforces it.
7. A POSIX shell script that is run directly, such as a setup or doctor script or a build tool's Unix wrapper (`mvnw`), starts with a shebang and is stored in Git with mode `100755`. A shell library that other scripts load with `source` has no shebang and keeps mode `100644`. PowerShell and batch scripts do not use a shebang or the executable mode. Git on Windows usually runs with `core.fileMode=false` and does not record the mode by itself, so a contributor there sets it with `git update-index --chmod=+x <file>`. The repository's hooks check the modes.

```yaml
services:
  postgres:
    image: docker.io/library/postgres:<tag>
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-inventory}
      POSTGRES_USER: ${POSTGRES_USER:-inventory}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-inventory-dev}
    ports:
      - "${BIND_ADDRESS:-127.0.0.1}:${POSTGRES_PORT:-5432}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./infra/postgres/init:/docker-entrypoint-initdb.d:ro,z
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

`<tag>` is a placeholder for the tag that each application pins in this file (§4).

```gitattributes
* text=auto
*.sh text eol=lf
.env.example text eol=lf
Makefile text eol=lf
mvnw text eol=lf
*.cmd text eol=crlf
*.bat text eol=crlf
```

Illustrative: a setting kept for one environment.

```ini
# Required by the <environment> guide: its shared folders do not support symlinks.
node-linker=hoisted
symlink=false
```

## 10. Tooling language

1. Scripts, the task runner file, Compose files, `.env.example` and CI workflows are written in English: the names they own, their messages and their comments. Their commands and tools are in English, whatever language the application uses for its product and documentation.
2. A file, or a set of scripts that work together, never mixes languages.
3. Product and domain identifiers that appear in tooling, such as a service, database or command named after a domain concept, keep the vocabulary the application chose.
4. The application lists these choices in its language map, as described in [Documentation](documentation.md#languages).

## 11. Environment guides

1. Each supported environment has its own guide in the application's operations documentation.
2. Content that is the same in every environment (daily workflow, services, tests, test users, troubleshooting that does not depend on the environment) lives in one shared guide. An environment guide holds only what differs and links to the shared guide.
3. An environment guide covers prerequisites, preparation, the `.env` values that environment changes, how to verify it (doctor and, if present, smoke) and troubleshooting specific to that environment.
4. Each guide starts with its validation state:
   - `Validated`: the date, the repository revision, who validated it and the commands run, at least setup or bootstrap, doctor, `check` and `smoke` when present.
   - `Not validated`: the guide was reviewed against the repository only; it names the tracking issue and who can validate it, for example a contributor who uses that environment.
5. An environment is claimed validated only with that evidence. A change to a shared file (§12) leaves the other environments not validated for that change until someone runs them there.

Illustrative: the first lines of two guides.

```markdown
> **Validation state:** `Validated` on 2026-11-14 at revision `abc1234` by the maintainer.
> Commands run: `make bootstrap`, `make doctor`, `make check`, `make smoke`.
```

```markdown
> **Validation state:** `Not validated`. Reviewed against the repository at revision `abc1234`;
> not run on this environment. Tracking issue: #123. Can be validated by a contributor using
> Windows with Docker Desktop.
```

## 12. Changing an environment

1. Test a change in the environment you are using, and record which environment that was in the pull request.
2. Do not remove or break what another environment relies on (§9 rule 4). When a shared file changes (the Compose file, the task runner file, `.env.example`, version pins), review the other environments' guides and scripts against the change.
3. The pull request states which environments were run and which were only reviewed. For each environment not run, it links the tracking issue or opens one for a contributor who uses it.
4. A change that adds or renames a variable updates `.env.example` and the guides that mention it in the same pull request.

## 13. Security

1. `.env.example` and versioned files contain development credentials only, recognizable as such. Real credentials never enter the repository, `.env.example` or a guide.
2. Generated local secrets, such as development certificates and private keys, live in a directory ignored by Git.
3. Publishing a service beyond `127.0.0.1` is opt-in, limited to trusted networks and documented with the services it exposes. Services that hold data stay local unless a guide states why they must not.
4. The private key of a local certificate authority stays on the machine that created it and is never shared or committed. Devices that need to trust it receive only its public certificate.
5. Setup scripts download tools only from the official source of each tool or from the operating system's package manager.

## 14. Anti-patterns

| Do not use | Use |
| --- | --- |
| A machine-specific value in a versioned file | A variable with a default and a `.env` value |
| A variable read by a command but missing from `.env.example` | An entry in `.env.example` with purpose and default |
| A version repeated in a script | The version pin file (§4) |
| A short image name | A fully qualified image name with a tag |
| A setup step that reinstalls or overwrites every time | A check before each step |
| A setup script that deletes `.env` or volumes | A separate, explicitly destructive command |
| A doctor check that fixes things | A read-only check that prints the fix |
| A command name that exists in only one environment | The common command set (§8) |
| `down` that deletes volumes | `down` that keeps them, plus a destructive command |
| Removing a setting another environment needs | A comment naming the environment and the reason |
| A guide that claims an environment works without a run | The validation state (§11) |
| Scripts in two languages | English tooling, one language per file (§10) |
| A shell script run directly but stored without the executable mode | Mode `100755` in Git, set with `git update-index --chmod=+x` on Windows (§9) |
| Services published on every interface by default | `127.0.0.1` by default, opt-in wider binding |

## 15. Pull request checklist

Every pull request that changes the development environment follows the sections that apply. A deviation is an exception and records the owner, reason, scope, expiry or review date and tracking issue required by the [standards index](README.md), whether it is written in the pull request or in the application's local rules.

- [ ] New or changed variables are in `.env.example` with purpose and default, and `.env` is not committed (§3).
- [ ] Versions come from the pin files (§4).
- [ ] Setup steps are idempotent and support `--dry-run`, and the doctor check stays read-only (§5, §6).
- [ ] The common commands keep the same names and effects in every environment (§8).
- [ ] Settings needed by another environment were kept, and new shell scripts have the right mode in Git (§9).
- [ ] Tooling files are in English, one language per file (§10).
- [ ] The pull request says which environments were run and which were only reviewed, with tracking issues (§12).
- [ ] The guides and their validation state match the change (§11).
- [ ] No real credential or private key was added (§13).
