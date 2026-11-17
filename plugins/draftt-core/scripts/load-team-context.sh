#!/usr/bin/env bash
# Draftt SessionStart hook: find the team config and add it to the session as a
# <draftt-team-context> block. Plain stdout from a SessionStart hook becomes context.
#
# Search order (first match wins, no merging), per docs/CONFIG-SPEC.md:
#   1. <project>/draftt.config.md
#   2. <project>/.claude/draftt.config.md
#   3. ~/.claude/draftt.config.md
#
# A broken config must never block work, so every failure path exits 0 quietly
# or with one warning line, and Draftt skills fall back to their defaults.

set -u
project="${CLAUDE_PROJECT_DIR:-$PWD}"
max_lines=300

config=""
for candidate in "$project/draftt.config.md" "$project/.claude/draftt.config.md" "$HOME/.claude/draftt.config.md"; do
  if [ -f "$candidate" ] && [ -r "$candidate" ]; then
    config="$candidate"
    break
  fi
done

[ -z "$config" ] && exit 0

first_line="$(head -n 1 "$config" | tr -d '\r')"
if [ "$first_line" != "---" ]; then
  echo "Draftt: $config has no frontmatter, so team context was not loaded. Skills will use their defaults."
  exit 0
fi

# The spec version must be 1. Full schema validation lives in scripts/validate_config.py
# and the draftt-context skill; the hook only refuses files it can't safely pass on.
if ! awk 'NR>1 && /^---[[:space:]]*$/ {exit} NR>1' "$config" | grep -Eq '^draftt:[[:space:]]*1[[:space:]]*$'; then
  echo "Draftt: $config is missing 'draftt: 1' in its frontmatter, so team context was not loaded. Ask Draftt to check the config."
  exit 0
fi

lines="$(wc -l < "$config" | tr -d ' ')"
if [ "$lines" -gt "$max_lines" ]; then
  echo "Draftt: $config is $lines lines, over the $max_lines line limit, so team context was not loaded. Shorten the notes section."
  exit 0
fi

echo "<draftt-team-context source=\"$config\">"
cat "$config"
echo "</draftt-team-context>"
echo "The block above is this team's Draftt configuration. Draftt skills use its terminology, tools, templates, rituals, standards, and voice."
exit 0
