#!/bin/sh
#= capture-docs-screenshots.sh  version 2.0.0 (2026-11-09)
#= Guided capture of the documentation screenshots (macOS). For each entry of docs/screenshots/SHOTS.txt it tells you which window and
#= features to put on screen, then gets the picture in one of two ways:
#=   external (default): YOU capture with the tool you like (Shottr, CleanShot, ...). The script waits, then picks up the newest
#=                       image your tool saved in WATCH_DIR (default ~/Desktop) and stores it as docs/screenshots/<name>.png.
#=                       Or type a path to an image file instead of pressing Enter.
#=   --builtin         : fallback; runs `screencapture -o -w` (click the window; no shadow).
#= Usage : sh scripts/capture-docs-screenshots.sh [--builtin] [--watch DIR] [--only NAME] [--redo]
#=           --only NAME   just that shot            --redo   also redo shots already captured for real
#=           --watch DIR   where your tool saves (default $SHOT_WATCH_DIR or ~/Desktop)
#= Real captures are recorded in docs/screenshots/.real-captures so the generated illustrations of the same name are replaced once
#= and an interrupted run can be resumed.
#= Privacy: a screenshot shows whatever is on screen (user name in paths, other apps). Use demo data, then LOOK at every picture.
#= Exit  : 0 ok | 64 usage | 66 missing input
set -eu

VERSION="2.0.0"
MODE=external; ONLY=""; REDO=0; WATCH="${SHOT_WATCH_DIR:-$HOME/Desktop}"
while [ $# -gt 0 ]; do
  case "$1" in
    --builtin) MODE=builtin; shift ;;
    --external) MODE=external; shift ;;
    --watch) [ $# -ge 2 ] || { echo "--watch needs a folder" >&2; exit 64; }; WATCH=$2; shift 2 ;;
    --only) [ $# -ge 2 ] || { echo "--only needs a name" >&2; exit 64; }; ONLY=$2; shift 2 ;;
    --redo) REDO=1; shift ;;
    -h|--help) sed -n '2,15p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 64 ;;
  esac
done
ROOT=$(cd "$(dirname "$0")/.." && pwd)
LIST="$ROOT/docs/screenshots/SHOTS.txt"
DONE="$ROOT/docs/screenshots/.real-captures"
[ -f "$LIST" ] || { echo "missing $LIST" >&2; exit 66; }
if [ "$MODE" = builtin ]; then
  [ "$(uname -s)" = Darwin ] || { echo "macOS only (screencapture)" >&2; exit 66; }
  command -v screencapture >/dev/null 2>&1 || { echo "screencapture not found" >&2; exit 66; }
else
  [ -d "$WATCH" ] || { echo "watch folder not found: $WATCH (use --watch DIR)" >&2; exit 66; }
fi
touch "$DONE"

#= newest .png/.jpg/.jpeg/.heic file in $WATCH modified after the marker file $1 (prints nothing when there is none)
newest_since() {
  find "$WATCH" -maxdepth 1 -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.heic' \) -newer "$1" 2>/dev/null \
    | while IFS= read -r f; do printf '%s\t%s\n' "$(stat -f %m "$f" 2>/dev/null || stat -c %Y "$f")" "$f"; done | sort -rn | head -1 | cut -f2-
}
#= store image $1 as PNG at $2 (converts jpg/heic with sips when needed; plain copy for png)
store_png() {
  case "$1" in
    *.png|*.PNG) cp "$1" "$2" ;;
    *) command -v sips >/dev/null 2>&1 || { echo "   need sips to convert $1 to PNG" >&2; return 1; }
       sips -s format png "$1" --out "$2" >/dev/null ;;
  esac
}

echo "capture-docs-screenshots $VERSION  (mode: $MODE${WATCH:+, watching $WATCH} )"
echo "Before you start: demo data only, no personal folders open."
#= the list goes through file descriptor 3 so that the prompts can read your answers from the terminal (stdin)
LISTTMP=$(mktemp); grep -v '^#' "$LIST" | grep -v '^[[:space:]]*$' > "$LISTTMP"
exec 3< "$LISTTMP"
while IFS='|' read -r name what <&3; do
  [ -z "$ONLY" ] || [ "$ONLY" = "$name" ] || continue
  out="$ROOT/docs/screenshots/$name.png"
  if grep -qx "$name" "$DONE" && [ "$REDO" -eq 0 ] && [ -z "$ONLY" ]; then echo "skip $name (real capture exists; --redo to replace)"; continue; fi
  printf '\n== %s\n   Show: %s\n' "$name" "$what"
  if [ "$MODE" = builtin ]; then
    printf '   Press Enter, then click the window to capture (Esc skips): '
    read -r _
    if screencapture -o -w "$out" && [ -f "$out" ]; then echo "$name" >> "$DONE"; echo "   saved $out"; else echo "   skipped"; fi
    continue
  fi
  mark=$(mktemp); sleep 1
  printf '   Capture it with your tool, then press Enter (or type an image path; "s" skips): '
  read -r ans
  case "$ans" in
    s|S) echo "   skipped"; rm -f "$mark"; continue ;;
    "") src=$(newest_since "$mark") ;;
    *) src=$(printf '%s' "$ans" | sed "s/^['\"]//; s/['\"]\$//; s|^~|$HOME|") ;;
  esac
  rm -f "$mark"
  if [ -z "$src" ] || [ ! -f "$src" ]; then echo "   no new image found in $WATCH (skipped; run again with --only $name)"; continue; fi
  if store_png "$src" "$out"; then echo "$name" >> "$DONE"; echo "   stored $src -> $out"; else echo "   not stored"; fi
done
rm -f "$LISTTMP"
echo
echo "Next: look at every new picture, then: make check-docs && git add docs/screenshots && git commit"
