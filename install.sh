#!/usr/bin/env bash
# Bootstrap or refresh Opptra agent skills, local sdlc-resources cache, and pinned OpenSpec.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CACHE_DIR="${HOME}/.cache/opptra/sdlc-resources.git"

skills_only=0
if [ "${1:-}" = "--skills-only" ] && [ "$#" -eq 1 ]; then
  skills_only=1
elif [ "$#" -gt 0 ]; then
  echo "Usage: install.sh [--skills-only]" >&2
  exit 2
fi

mkdir -p "${HOME}/.claude/skills" "${HOME}/.codex/skills" "${HOME}/.cursor/skills" "${HOME}/.config/opencode/skills" "${HOME}/.local/bin"

if [ -f "${ROOT}/bin/odlc" ]; then
  chmod +x "${ROOT}/bin/odlc"
  ln -sfn "${ROOT}/bin/odlc" "${HOME}/.local/bin/odlc"
fi

# Remove only the old CLI symlink installed by Opptra; preserve unrelated commands.
legacy_cli="${HOME}/.local/bin/opptra"
if [ -L "$legacy_cli" ]; then
  legacy_target="$(readlink "$legacy_cli")"
  if [ "$legacy_target" = "${ROOT}/bin/opptra" ] || \
     grep -qF '# Unified Opptra SDLC CLI for both developers and AI agents.' "$legacy_cli" 2>/dev/null; then
    unlink "$legacy_cli"
  fi
fi

linked=()
for dir in "${ROOT}"/opptra/skills/*/; do
  [ -f "${dir}SKILL.md" ] || continue
  name="$(basename "$dir")"
  target="${dir%/}"
  ln -sfn "$target" "${HOME}/.claude/skills/${name}"
  ln -sfn "$target" "${HOME}/.codex/skills/${name}"
  ln -sfn "$target" "${HOME}/.cursor/skills/${name}"
  ln -sfn "$target" "${HOME}/.config/opencode/skills/${name}"
  linked+=("$name")
done

# Remove stale links owned by this checkout after a skill is removed or renamed.
for skill_home in "${HOME}/.claude/skills" "${HOME}/.codex/skills" "${HOME}/.cursor/skills" "${HOME}/.config/opencode/skills"; do
  for link in "$skill_home"/*; do
    [ -L "$link" ] || continue
    target="$(readlink "$link")"
    case "$target" in
      "${ROOT}/opptra/skills/"*)
        [ -f "$link/SKILL.md" ] || unlink "$link"
        ;;
    esac
  done
done

echo "Linked ${#linked[@]} Opptra skills: ${linked[*]}"

if [ "$skills_only" -eq 1 ]; then
  exit 0
fi

# Warm or refresh local bare cache of opptra/sdlc-resources for fast, offline-capable generator runs
mkdir -p "$(dirname "$CACHE_DIR")"
if [ -d "$CACHE_DIR" ]; then
  git -C "$CACHE_DIR" fetch --prune origin "+refs/heads/*:refs/heads/*" >/dev/null 2>&1 || true
else
  if [ -d "${ROOT}/../sdlc-resources/.git" ]; then
    git clone --bare "${ROOT}/../sdlc-resources" "$CACHE_DIR" >/dev/null 2>&1 || true
    git -C "$CACHE_DIR" remote set-url origin https://github.com/opptra/sdlc-resources.git >/dev/null 2>&1 || true
  else
    git clone --bare https://github.com/opptra/sdlc-resources.git "$CACHE_DIR" >/dev/null 2>&1 || true
  fi
fi

if [ -f "${ROOT}/opptra/pins.env" ]; then
  # shellcheck disable=SC1091
  source "${ROOT}/opptra/pins.env"
  if command -v npm >/dev/null 2>&1 && [ -n "${OPENSPEC_VERSION:-}" ]; then
    current_os="$(openspec --version 2>/dev/null || echo "")"
    if [ "$current_os" != "$OPENSPEC_VERSION" ]; then
      echo "Installing pinned @fission-ai/openspec@${OPENSPEC_VERSION}..."
      npm install -g "@fission-ai/openspec@${OPENSPEC_VERSION}" >/dev/null 2>&1 || true
    fi
  fi
fi

echo "Opptra setup complete (skills @ $(git -C "$ROOT" rev-parse --short HEAD 2>/dev/null || echo 'local'))."
