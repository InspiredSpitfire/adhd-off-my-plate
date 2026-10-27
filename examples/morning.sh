#!/bin/sh
# Off My Plate: the unattended morning run.
#
# Reads mail and calendar, writes the Plate and the brief into the workspace,
# and sends nothing. `--permission-mode dontAsk` denies every tool that is not
# on the list below, so send, delete, RSVP, and pay tools never run. Reads are
# fenced to the workspace and this plugin; writes to the workspace; the only
# commands allowed are this plugin's three scripts, called by exact path.
#
# Copy to ~/plate/morning.sh, then schedule it (README: "Schedule it").
# Extra arguments pass straight to claude, e.g. --plugin-dir ~/dev/adhd-off-my-plate
# (then also set OFF_MY_PLATE_PLUGIN to that folder).

WS="${OFF_MY_PLATE_DIR:-$HOME/plate}"
CLAUDE="${CLAUDE_BIN:-$HOME/.local/bin/claude}"   # `command -v claude` tells you yours

# The installed plugin: ~/.claude/plugins/cache/<marketplace>/adhd-off-my-plate/<version>, newest version.
PLUGIN="${OFF_MY_PLATE_PLUGIN:-$(python3 - <<'PY'
import glob, os
def key(p):
    v = os.path.basename(p.rstrip("/"))
    return [int(x) if x.isdigit() else 0 for x in v.split(".")]
hits = sorted(glob.glob(os.path.expanduser("~/.claude/plugins/cache/*/adhd-off-my-plate/*/")), key=key)
print(hits[-1].rstrip("/") if hits else "")
PY
)}"
if [ -z "$PLUGIN" ] || [ ! -f "$PLUGIN/scripts/due.py" ]; then
  echo "Off My Plate: plugin not found; install it or set OFF_MY_PLATE_PLUGIN" >&2; exit 1
fi
case "$PLUGIN$WS" in *" "*)
  echo "Off My Plate: a space in the plugin or workspace path stops the script allow-list from matching; the brief will be UNLINTED" >&2;;
esac

mkdir -p "$WS/notes"
cd "$WS" || exit 1

"$CLAUDE" -p "/adhd-off-my-plate:morning $WS" \
  --permission-mode dontAsk \
  --allowedTools \
    "Read(/$WS/**)" "Read(/$PLUGIN/**)" "Edit(/$WS/**)" "Skill" "Agent" \
    "Bash(python3 $PLUGIN/scripts/plate_lint.py:*)" \
    "Bash(python3 $PLUGIN/scripts/due.py:*)" \
    "Bash(python3 $PLUGIN/scripts/surfaced.py:*)" \
    "mcp__claude_ai_Gmail__search_threads" "mcp__claude_ai_Gmail__get_thread" \
    "mcp__claude_ai_Google_Calendar__list_calendars" "mcp__claude_ai_Google_Calendar__list_events" \
  "$@" \
  < /dev/null > "$WS/notes/brief-$(date +%F).md" 2>&1
