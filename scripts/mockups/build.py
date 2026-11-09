#= build.py  version 0.1.0 (2026-11-09)
#= Writes the 17 documentation mockup pages (HTML) into docs/mockups/. render.mjs then turns them into docs/screenshots/*.png.
#= These are ILLUSTRATIONS of the layout with made-up data, not screenshots (each image says so). Real captures from `make screenshots`
#= replace them by file name.
#= Usage : python3 scripts/mockups/build.py [OUT_DIR]        (Python 3.12+: the modules use nested f-string quotes)
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scenario import H, INSPECTOR, ROWS  # noqa: E402
from ui import (btn, chk, esc, icon, kind_icon, legend, main_toolbar, page, pop, seg, window, KIND, KIND_LABEL)  # noqa: E402
from views import (Node, activity_summary_inspector, build_tree, files_bar, filter_panel, inspector, list_view, text_view,  # noqa: E402
                   tree_view)

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "mockups")
W = 1240


#= ---- main window ----------------------------------------------------------------------------------------------------------
def main_window(left: str, mode: str = "List", insp: str | None = "", status: str = "capturing - 24 of 24 rows", record: str = "Record",
                filter_on: bool = False, extra: str = "", width: int = W, title: str = "Crescendo", banner: str = "",
                replay: bool = False, capturing: bool = True) -> str:
    insp_html = inspector() if insp == "" else (insp or "")
    split = f'<div class="split"><div class="left">{left}</div>{insp_html}</div>'
    inner = (main_toolbar("File", capturing) + banner + files_bar(mode, status, record, filter_on, bool(insp_html), replay) + extra + split + legend())
    return window(title, inner, width)


def hero() -> str:
    return main_window(list_view(ROWS, selected=0))


#= ---- graph geometry -------------------------------------------------------------------------------------------------------
def compress(n: Node) -> Node:
    #= merge single-child chains into one label ("Users/me"), as the app does for readability
    while len(n.kids) == 1 and n.own == 0:
        (k,) = n.kids.values()
        k.name = (n.name.rstrip("/") + "/" + k.name).lstrip("/") if n.name != "/" else k.name
        n = k
    n.kids = {name: compress(k) for name, k in n.kids.items()}
    return n


def cat_color(cat: str) -> str:
    return KIND.get(cat, ("#8e8e93", ""))[0]


def tree_svg(selected: str | None = None) -> str:
    root = build_tree()
    root.name = "/"
    root = compress(root)
    leaf_h, col_w, x0 = 27, 215, 24
    pos: dict = {}
    counter = [0]

    def layout(n: Node, d: int):
        kids = [layout(k, d + 1) for _, k in sorted(n.kids.items())]
        if kids:
            y = sum(pos[id(k)][1] for k in kids) / len(kids)
        else:
            y = 30 + counter[0] * leaf_h
            counter[0] += 1
        pos[id(n)] = (x0 + d * col_w, y, d)
        return n
    layout(root, 0)
    maxd = max(p[2] for p in pos.values())
    width = x0 + (maxd + 1) * col_w + 150
    height = 30 + counter[0] * leaf_h + 20
    edges, nodes = [], []

    def draw(n: Node):
        x, y, _ = pos[id(n)]
        for _, k in sorted(n.kids.items()):
            kx, ky, _ = pos[id(k)]
            mx = (x + kx) / 2
            edges.append(f'<path d="M{x + 8},{y} C{mx},{y} {mx},{ky} {kx - 8},{ky}" fill="none" stroke="var(--line)" stroke-width="1.4"/>')
            draw(k)
        leaf = not n.kids
        r = 5 + min(9, math.sqrt(n.total) * 1.3)
        col = cat_color(n.last) if leaf else "var(--gray)"
        lab = esc(n.name if len(n.name) < 26 else n.name[:24] + "…")
        if leaf and n.last == "deleted":
            nodes.append(f'<circle cx="{x}" cy="{y}" r="8" fill="none" stroke="var(--red)" stroke-width="1.5"/><path d="M{x - 4},{y - 4}L{x + 4},{y + 4}M{x + 4},{y - 4}L{x - 4},{y + 4}" stroke="var(--red)" stroke-width="2"/>')
        else:
            nodes.append(f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="{col}" fill-opacity="{1 if leaf else .55}" stroke="{col}"/>')
        txt = "var(--red)" if (leaf and n.last == "deleted") else "var(--text)"
        sel = ' font-weight="700"' if selected and n.path == selected else ""
        nodes.append(f'<text x="{x + r + 6}" y="{y + 4}" font-size="12" fill="{txt}"{sel}>{lab}</text>')
        nodes.append(f'<g><rect x="{x + r + 6 + len(lab) * 6.6 + 4:.0f}" y="{y - 8}" width="{14 + 6 * len(str(n.total))}" height="16" rx="8" fill="var(--bar)"/>'
                     f'<text x="{x + r + 6 + len(lab) * 6.6 + 11 + 3 * len(str(n.total)):.0f}" y="{y + 4}" font-size="10" text-anchor="middle" fill="var(--sub)">{n.total}</text></g>')
    draw(root)
    return f'<svg width="100%" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">{"".join(edges)}{"".join(nodes)}</svg>'


PALETTE = ["#4b93ff", "#35c759", "#ffab1a", "#b06af0", "#18b5c7", "#ef6aa0", "#9aa64b", "#f2765a"]


def arc(cx, cy, r0, r1, a0, a1) -> str:
    def pt(r, a):
        return cx + r * math.cos(a), cy + r * math.sin(a)
    large = 1 if a1 - a0 > math.pi else 0
    x0, y0 = pt(r1, a0)
    x1, y1 = pt(r1, a1)
    x2, y2 = pt(r0, a1)
    x3, y3 = pt(r0, a0)
    return f"M{x0:.1f},{y0:.1f} A{r1},{r1} 0 {large} 1 {x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f} A{r0},{r0} 0 {large} 0 {x3:.1f},{y3:.1f} Z"


def sunburst_svg(size: int = 600) -> str:
    root = compress(build_tree())
    cx = cy = size / 2
    centre_r, outer = 62, size / 2 - 14
    depth = [0]

    def maxdepth(n: Node, d: int):
        depth[0] = max(depth[0], d)
        for k in n.kids.values():
            maxdepth(k, d + 1)
    maxdepth(root, 0)
    ring = (outer - centre_r) / max(1, depth[0])
    parts, labels = [], []

    def draw(n: Node, d: int, a0: float, a1: float, hue: str):
        if d > 0:
            r0, r1 = centre_r + (d - 1) * ring, centre_r + d * ring
            leaf = not n.kids
            fill = cat_color(n.last) if (leaf and n.last == "deleted") else hue
            op = .95 if leaf else max(.45, .85 - d * .1)
            parts.append(f'<path d="{arc(cx, cy, r0, r1 - 1.5, a0, a1 - 0.004)}" fill="{fill}" fill-opacity="{op:.2f}" stroke="var(--panel)" stroke-width="1.5"/>')
            if (a1 - a0) * (r0 + r1) / 2 > 80:
                am = (a0 + a1) / 2
                rm = (r0 + r1) / 2
                deg = math.degrees(am)
                flip = 90 < deg % 360 < 270
                rot = deg + 180 if flip else deg
                nm = n.name if len(n.name) < 15 else n.name[:13] + "…"
                labels.append(f'<text transform="translate({cx + rm * math.cos(am):.1f},{cy + rm * math.sin(am):.1f}) rotate({rot:.1f})" font-size="10.5" '
                              f'text-anchor="middle" dominant-baseline="middle" fill="#fff" font-weight="600">{esc(nm)}</text>')
        kids = sorted(n.kids.values(), key=lambda k: -k.total)
        sub = n.total - n.own
        a = a0
        for i, k in enumerate(kids):
            span = (a1 - a0) * (k.total / n.total) if n.own == 0 else (a1 - a0) * (k.total / n.total)
            draw(k, d + 1, a, a + span, PALETTE[i % len(PALETTE)] if (d == 0 or (d == 1 and len(n.kids) > 2)) else hue)
            a += span
    draw(root, 0, -math.pi / 2, 1.5 * math.pi, "var(--gray)")
    centre = (f'<circle cx="{cx}" cy="{cy}" r="{centre_r - 4}" fill="var(--panel)" stroke="var(--line)"/>'
              f'<text x="{cx}" y="{cy - 2}" font-size="26" font-weight="700" text-anchor="middle" fill="var(--text)">{root.total}</text>'
              f'<text x="{cx}" y="{cy + 16}" font-size="11" text-anchor="middle" fill="var(--sub)">changes</text>')
    return f'<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">{"".join(parts)}{"".join(labels)}{centre}</svg>'


def graph_bar(layout: str) -> str:
    return (f'<div class="bar" style="padding:4px 12px;background:var(--panel);border-bottom:1px solid var(--line)">{pop(layout)}{pop("Cap: 200 busiest paths")}'
            f'{pop("User: all")}{chk("Hide Apple operations")}<span class="grow"></span>{btn("−")}{btn("+")}{btn("Fit")}{btn("100%")}{btn("Center")}{btn("Save…")}</div>')


def graph_status(text: str) -> str:
    return f'<div class="status" style="padding:5px 14px;background:var(--panel);border-top:1px solid var(--line)">{esc(text)}</div>'


def graph_tree_page() -> str:
    svg = tree_svg(selected=H + "/work/final.txt")
    left = graph_bar("Horizontal Tree") + f'<div style="padding:8px 8px;background:var(--panel)">{svg}</div>' + graph_status(
        "22 paths shown of 22 · 129 changes · Horizontal Tree · scroll or drag to pan, pinch or ± to zoom")
    return main_window(left, "Graph", insp=activity_summary_inspector(), status="graph - 22 paths")


def graph_sunburst_page() -> str:
    left = graph_bar("Sunburst") + f'<div style="padding:10px;display:flex;justify-content:center;background:var(--panel)">{sunburst_svg(600)}</div>' + graph_status(
        "22 paths shown of 22 · 129 changes · Sunburst · double-click zooms in at the pointer (Option: out)")
    return main_window(left, "Graph", insp=activity_summary_inspector(), status="graph - 22 paths")


#= ---- other Files-view pages -----------------------------------------------------------------------------------------------
def list_page() -> str:
    return main_window(list_view(ROWS, selected=7))


def text_page() -> str:
    return main_window(text_view(ROWS), "Text", insp=None)


def tree_page() -> str:
    return main_window(tree_view(4, 28, selected=H + "/Library/Application Support/NotesSync"), "Tree", insp=activity_summary_inspector(), status="tree - 22 paths")


def filter_page() -> str:
    return main_window(list_view([r for r in ROWS if not r.path.startswith(H + "/Library/Caches")][:19], selected=0), filter_on=True,
                       extra=filter_panel(True), status="capturing - 19 of 24 rows (5 filtered)")


def record_page() -> str:
    menu = ('<div class="menu" style="left:520px;top:132px"><div>Off</div><div>Include last 1 min</div><div class="hi">Include last 5 min</div>'
            '<div>Include last 15 min</div><hr><div class="off">Rows kept in memory: 50,000</div></div>')
    page_html = main_window(list_view(ROWS[:20], selected=-1), record="Stop recording", status="recording - 00:42 - 1,204 events")
    return page_html.replace('<div class="split">', menu + '<div class="split">', 1)


def player_page() -> str:
    bar = (f'<div class="bar">{btn("Pause")}{btn("Restart")}{pop("Speed 1×")}{chk("Compress idle gaps")}{chk("Follow newest")}<span class="grow"></span>'
           f'<span class="status">00:14.2 / 00:42.0</span></div>'
           f'<div style="padding:2px 18px 10px"><div style="height:6px;border-radius:3px;background:var(--bar);position:relative"><div style="width:34%;height:6px;border-radius:3px;background:var(--accent)"></div>'
           f'<div style="position:absolute;left:34%;top:-4px;width:14px;height:14px;margin-left:-7px;border-radius:50%;background:#fff;border:1px solid var(--ctl-line);box-shadow:0 1px 3px rgba(0,0,0,.3)"></div></div></div>')
    head = f'<div class="bar" style="padding-top:0"><span class="sub small">notes-sync-session.crescrec · 1,204 events · recorded 2026-11-09 21:42 · sha256 verified</span></div>'
    return window("notes-sync-session.crescrec", bar + head + f'<div class="split"><div class="left">{list_view(ROWS[:16], 6)}</div></div>' + legend(), 980)


#= ---- Cresc Console --------------------------------------------------------------------------------------------------------
def console(tab: str, body: str, width: int = 1060) -> str:
    tabs = '<div class="tabs">' + seg(["Sessions", "Denials", "Profile", "Events"], tab) + "</div>"
    return window("Cresc Console", f'<div class="bar" style="padding-bottom:0"><span class="status">engine: ready · protocol 1</span></div>{tabs}{body}', width)


def logbox(lines, h=150) -> str:
    return f'<div class="log mono" style="margin:0 14px 14px;height:{h}px">' + "".join(f"<div>{esc(x)}</div>" for x in lines) + "</div>"


def console_sessions() -> str:
    form = ('<div class="form"><div class="l">Profile</div><div>' + pop("notes-sync (v4)") + '</div>'
            '<div class="l">Program</div><div class="row"><span class="field" style="min-width:560px">' + H + '/bin/notes-sync</span>' + btn("Choose…") + '</div>'
            '<div class="l">Write folders</div><div class="row"><div class="list" style="width:560px"><div>' + H + '/Library/Application Support/NotesSync</div><div>' + H + '/work</div></div>'
            '<div class="btns">' + btn("Add…") + btn("Remove") + '</div></div>'
            '<div class="l">Arguments</div><div><span class="field" style="min-width:560px">--sync --verbose</span></div></div>')
    buttons = f'<div class="bar" style="padding-left:110px">{btn("Start")}{btn("Stop", "dis")}{btn("Restart")}</div>'
    log = logbox(["21:40:02 profile notes-sync v4 loaded (sandbox-exec)", "21:40:02 started /Users/me/bin/notes-sync --sync --verbose (pid 5301)",
                  "21:40:09 denial: file-write-create /Users/me/Library/Caches/ca.example.updater/lock", "21:40:31 program exited with status 0",
                  "21:40:31 run saved: 1 candidate denial, 3 benign"], 120)
    return console("Sessions", form + buttons + log)


def console_denials() -> str:
    cols = "70px 80px 60px 110px 150px 1fr 50px"
    head = "".join(f'<div class="cell">{c}</div>' for c in ["Change", "Class", "Risk", "Process", "Operation", "Target", "Count"])
    data = [("new", "candidate", "low", "notes-sync", "file-write-create", H + "/Library/Caches/ca.example.updater/lock", 1),
            ("new", "candidate", "medium", "notes-sync", "network-outbound", "api.example.com:443", 4),
            ("persisting", "candidate", "low", "notes-sync", "file-read-data", H + "/Documents/notes", 12),
            ("persisting", "benign", "low", "notes-sync", "mach-lookup", "com.apple.system.opendirectoryd", 3),
            ("persisting", "path-search", "low", "bash", "file-read-metadata", "/usr/local/bin/python3", 2)]
    rows = "".join(f'<div class="tr {"sel" if i == 1 else ""}" style="grid-template-columns:70px 80px 60px 110px 150px 1fr 50px">' + "".join(
        f'<div class="cell {"num" if j == 6 else ""}">{esc(str(v))}</div>' for j, v in enumerate(r)) + "</div>" for i, r in enumerate(data))
    top = f'<div class="bar">Run: {pop("2026-11-09 21:40 · notes-sync")}{btn("Reload")}{seg(["Candidates", "All"], "Candidates")}<span class="grow"></span><span class="status">1 resolved since the previous run</span></div>'
    table = f'<div class="panel" style="margin:0 14px;border:1px solid var(--line)"><div class="th" style="grid-template-columns:{cols}">{head}</div>{rows}</div>'
    detail = ('<div class="log mono" style="margin:10px 14px;height:96px"><div>process:   notes-sync (pid 5301)</div><div>operation: network-outbound</div>'
              '<div>target:    api.example.com:443</div><div>rule:      (allow network-outbound (remote tcp "api.example.com:443"))</div><div>risk:      medium - reaches a remote host</div></div>')
    foot = f'<div class="bar" style="padding-top:0">{btn("Grant selected")}{btn("Grant all low-risk")}{btn("Add rule by hand…")}<span class="grow"></span>{btn("Export evidence bundle…")}</div>'
    return console("Denials", top + table + detail + foot)


def console_profile() -> str:
    cols = "60px 180px 80px 1fr 70px"
    hist = [("v4", "2026-11-09 21:38:50", "grant", "g-9f31 file-write-create ~/work", "low"), ("v3", "2026-11-09 21:12:07", "grant", "g-7c20 network-outbound api.example.com", "medium"),
            ("v2", "2026-11-09 20:51:33", "revoke", "g-4410 file-read-data ~/Documents", "low"), ("v1", "2026-11-09 20:40:01", "create", "initial deny-default profile", "low")]
    head = "".join(f'<div class="cell">{c}</div>' for c in ["Version", "When", "Action", "Grant id", "Risk"])
    rows = "".join(f'<div class="tr {"sel" if i == 0 else ""}" style="grid-template-columns:{cols}">' + "".join(f'<div class="cell">{esc(v)}</div>' for v in r) + "</div>" for i, r in enumerate(hist))
    prof = ['(version 1)', '(deny default)', '(allow process-exec* (literal "/Users/me/bin/notes-sync"))', '(allow file-read* (subpath "/usr/lib") (subpath "/System/Library"))',
            '(allow file-write* (subpath "/Users/me/Library/Application Support/NotesSync"))', '(allow file-write-create (subpath "/Users/me/work"))  ; g-9f31']
    top = f'<div class="bar">Profile: {pop("notes-sync")}<span class="sub small">4 versions · current v4</span><span class="grow"></span>{btn("Refresh")}{btn("Diff with previous")}{btn("Revoke selected grant")}</div>'
    return console("Profile", top + f'<div class="panel" style="margin:0 14px;border:1px solid var(--line)"><div class="th" style="grid-template-columns:{cols}">{head}</div>{rows}</div>' + logbox(prof, 130).replace("margin:0 14px 14px", "margin:10px 14px 14px"))


def console_events() -> str:
    scope = f'<div class="bar">Scope: {pop("Folder")}<span class="field" style="min-width:380px">{H}/work</span>{btn("Choose…")}{btn("Start capture")}<span class="grow"></span><span class="status">daemon ready · Full Disk Access ok</span></div>'
    return console("Events", scope + f'<div class="panel" style="margin:0 0 14px">{list_view([r for r in ROWS if "/work/" in r.path or "Downloads" in r.path] + ROWS[19:21])}</div>')


#= ---- small crops -----------------------------------------------------------------------------------------------------------
def setup_banner() -> str:
    b = ('<div class="banner"><span style="font-size:15px">⚠</span><span class="grow">The event daemon has no Full Disk Access yet. Open the setup in the Cresc Console (Events tab).</span>'
         + btn("Open setup") + "</div>")
    return window("Crescendo", b + files_bar("List", "needs Full Disk Access"), 940)


def menu_bar() -> str:
    bar = ('<div style="display:flex;justify-content:flex-end;gap:18px;align-items:center;height:26px;padding:0 14px;background:var(--bar);border-radius:8px 8px 0 0;font-size:12px">'
           '<span>Fri 21:42</span><span style="background:var(--accent);color:#fff;padding:1px 7px;border-radius:5px">◉</span></div>')
    menu = ('<div class="menu" style="position:relative;float:right;margin:2px 4px 0 0;width:300px"><div class="off small">Crescendo 0.1.3 · build 3 · 81d642e</div><hr>'
            '<div>Show App Window</div><div class="hi">Cresc Console…</div><div>Open Recording…</div><hr><div>Run in Background</div><div>Run in Dock</div><hr><div>Quit Crescendo</div></div>')
    return f'<div style="width:560px;height:260px;background:var(--panel);border-radius:8px;box-shadow:var(--shadow);overflow:hidden">{bar}{menu}</div>'


def graph_controls() -> str:
    return window("Crescendo", graph_bar("Horizontal Tree").replace("padding:4px 12px", "padding:8px 12px"), 1100)


#= ---- list of pages ---------------------------------------------------------------------------------------------------------
def pages():
    return [
        ("hero-dark", "dark", hero()), ("hero-light", "light", hero()), ("files-list", "light", list_page()), ("files-text", "light", text_page()),
        ("files-tree", "light", tree_page()), ("files-graph-tree", "light", graph_tree_page()), ("files-graph-sunburst", "light", graph_sunburst_page()),
        ("files-filter", "light", filter_page()), ("files-record", "light", record_page()), ("player", "light", player_page()),
        ("console-sessions", "light", console_sessions()), ("console-denials", "light", console_denials()), ("console-profile", "light", console_profile()),
        ("console-events", "light", console_events()), ("setup-banner", "light", setup_banner()), ("menu-bar", "light", menu_bar()),
        ("graph-controls", "light", graph_controls()),
    ]


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    for name, theme, body in pages():
        with open(os.path.join(OUT, name + ".html"), "w", encoding="utf-8") as f:
            f.write(page(theme, body))
    print(f"build.py: wrote {len(pages())} pages to {os.path.normpath(OUT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
