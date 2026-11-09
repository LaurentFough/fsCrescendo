#= views.py  version 0.1.0 (2026-11-09)
#= Builders for the pieces of the Files view and the console, combined by build.py into the mockup pages.
from __future__ import annotations

from typing import Dict, List, Optional

from scenario import H, INSPECTOR, PATHS, ROWS, Row
from ui import (btn, chk, esc, icon, kind_icon, legend, main_toolbar, pop, search, seg, ext_kind, window, KIND_LABEL)

LIST_COLS = "46px 66px 150px 1fr 108px 112px"


def files_bar(mode: str = "List", status: str = "capturing - 24 of 24 rows", record: str = "Record", filter_on: bool = False,
              inspector: bool = True, replay: bool = False) -> str:
    items = [seg(["List", "Text", "Tree", "Graph"], mode)]
    if not replay:
        items += [pop("Prune Redundant Events" if filter_on else "No Cleanup"), btn("Pause")]
        items += [btn('<span style="color:var(--red)">●</span> ' + record, "red"), pop("Include last 5 min")]
    items += [chk("Filter", filter_on), chk("Inspector", inspector), f'<span class="status">{esc(status)}</span>']
    return '<div class="bar" style="padding-top:2px;padding-bottom:6px">' + "".join(items) + "</div>"


def path_cell(r: Row) -> str:
    ic = kind_icon("deleted", 15) if r.cat == "deleted" else icon(ext_kind(r.path, r.is_dir), 15)
    text = esc(r.path) + (f'  <span class="sub">← {esc(r.src)}</span>' if r.cat == "moved_to" and r.src else "")
    return f'<div class="p">{ic}<span>{text}</span></div>'


def list_view(rows: List[Row], selected: int = -1, cols: str = LIST_COLS, height: Optional[int] = None) -> str:
    head = (f'<div class="th" style="grid-template-columns:{cols}"><div class="cell">Kind</div><div class="cell">PID</div><div class="cell">Process</div>'
            f'<div class="cell">Path</div><div class="cell">Inode</div><div class="cell">Date</div></div>')
    body = []
    for i, r in enumerate(rows):
        cls = ("sel " if i == selected else "") + ("del" if r.cat == "deleted" else "")
        body.append(f'<div class="tr {cls}" style="grid-template-columns:{cols}"><div class="cell" style="display:flex;justify-content:center">{kind_icon(r.cat)}</div>'
                    f'<div class="cell">{r.pid}</div><div class="cell">{esc(r.proc)}</div><div class="cell">{path_cell(r)}</div>'
                    f'<div class="cell">{r.inode}</div><div class="cell">{r.t}</div></div>')
    h = f' style="height:{height}px;overflow:hidden"' if height else ""
    return f'<div class="tbl"{h}>{head}{"".join(body)}</div>'


def text_view(rows: List[Row], height: Optional[int] = None) -> str:
    tags = {"created": "CRE ", "deleted": "DEL ", "modified": "MOD ", "attributes": "ATR ", "moved_from": "MVF ", "moved_to": "MVT "}
    lines = []
    for r in rows:
        color = "var(--red)" if r.cat == "deleted" else ("var(--blue)" if r.cat.startswith("moved") else "var(--text)")
        path = r.path + (f"  <-  {r.src}" if r.cat == "moved_to" and r.src else "")
        lines.append(f'<div style="color:{color}">2026-11-09 {r.t}  {tags[r.cat]}  {str(r.pid):<7} {r.proc[:18]:<18} {r.inode:<20} {esc(path)}</div>')
    h = f' style="height:{height}px;overflow:hidden"' if height else ""
    return f'<div class="mono" style="padding:6px 10px;font-size:11.5px;line-height:1.6"{h}>{"".join(lines)}</div>'


def inspector(i: Dict[str, str] = INSPECTOR) -> str:
    def kv(k, v):
        return f'<div class="kv"><span class="k">{k}:</span><span class="v">{esc(v)}</span></div>'
    return ('<div class="insp"><div class="big">' + icon("plist", 56) + f'<small>{i["type"]}</small></div>'
            '<h4>Current Status</h4>' + kv("Path", i["path"]) + kv("Created", i["created"]) + kv("Modified", i["modified"]) +
            '<h4>Event Information</h4>' + kv("Category", i["category"]) + kv("Event Type", i["event"]) + kv("Time", i["time"]) +
            kv("Owner uid", i["owner_uid"]) + kv("Owner gid", i["owner_gid"]) + kv("Mode", i["mode"]) + kv("Size", i["size"]) +
            kv("Inode", i["inode"]) + kv("Device", i["device"]) +
            '<h4>Process Information</h4>' + kv("PID", i["pid"]) + kv("PPID", i["ppid"]) + kv("Name", i["pname"]) + kv("Path", i["ppath"]) +
            kv("Signing id", i["sign"]) + kv("UID", i["puid"]) + kv("GID", i["pgid"]) + "</div>")


def filter_panel(hidden: bool = True) -> str:
    def rule(field, op, val):
        return (f'<div class="rule"><span class="field" style="min-width:150px;justify-content:space-between">{field}<span class="sub">▾</span></span>'
                f'<span class="field" style="min-width:140px;justify-content:space-between">{op}<span class="sub">▾</span></span>'
                f'<span class="field" style="min-width:260px">{esc(val)}</span>{btn("−")}{btn("+")}</div>')
    top = (f'<div class="row">{pop("Apply Filter Template")}<span>Match</span>{pop("All")}<span>of the following rules</span>'
           f'<span class="grow"></span>{btn("Clear Filter")}</div>')
    hid = ''
    if hidden:
        hid = (f'<div class="row small sub" style="margin-top:8px"><span>Hidden folders (1): {H}/Library/Caches</span>'
               f'<span class="grow"></span>{btn("Restore All")}</div>')
    return ('<div class="fpanel">' + top + rule("Process Name", "is not", "kernel_task") + rule("Path", "begins with", H + "/") +
            rule("Category", "is not", "Attributes Modified") + hid + "</div>")


#= ---- tree -----------------------------------------------------------------------------------------------------------------
class Node:
    def __init__(self, name: str, path: str):
        self.name, self.path = name, path
        self.kids: Dict[str, "Node"] = {}
        self.own = 0
        self.total = 0
        self.last = ""
        self.counts: Dict[str, int] = {}


def build_tree(paths=PATHS) -> Node:
    root = Node("/", "/")
    for path, (own, last) in paths.items():
        node = root
        node.total += own
        cur = ""
        for part in [p for p in path.split("/") if p]:
            cur += "/" + part
            node = node.kids.setdefault(part, Node(part, cur))
            node.total += own
            node.counts[last] = node.counts.get(last, 0) + own
        node.own += own
        node.last = last
    return root


def tree_view(expanded_depth: int = 4, rows_limit: int = 28, selected: Optional[str] = None) -> str:
    cols = "1fr 74px 64px 64px 70px 56px 58px 108px"
    head = (f'<div class="th" style="grid-template-columns:{cols}"><div class="cell">Path</div><div class="cell num">Changes</div><div class="cell num">Created</div>'
            f'<div class="cell num">Deleted</div><div class="cell num">Modified</div><div class="cell num">Attr.</div><div class="cell num">Moved</div><div class="cell">Last Change</div></div>')
    root = build_tree()
    out: List[str] = []

    def walk(node: Node, depth: int):
        for name in sorted(node.kids):
            k = node.kids[name]
            if len(out) >= rows_limit:
                return
            is_dir = bool(k.kids)
            tri = ("▾" if depth < expanded_depth else "▸") if is_dir else ""
            ic = kind_icon("deleted", 15) if (not is_dir and k.last == "deleted") else icon(ext_kind(k.path, is_dir), 15)

            def n(c):
                v = k.counts.get(c, 0)
                return str(v) if v else ""
            sel = "sel " if selected and k.path == selected else ""
            out.append(f'<div class="tr {sel}" style="grid-template-columns:{cols}"><div class="cell p" style="padding-left:{6 + depth * 18}px">'
                       f'<span style="width:10px;color:var(--sub)">{tri}</span>{ic}<span>{esc(name)}</span></div>'
                       f'<div class="cell num">{k.total}</div><div class="cell num">{n("created")}</div><div class="cell num">{n("deleted")}</div>'
                       f'<div class="cell num">{n("modified")}</div><div class="cell num">{n("attributes")}</div>'
                       f'<div class="cell num">{(k.counts.get("moved_from", 0) + k.counts.get("moved_to", 0)) or ""}</div><div class="cell">21:42:{30 + (k.total % 11):02d}.{(k.total * 37) % 1000:03d}</div></div>')
            if is_dir and depth < expanded_depth:
                walk(k, depth + 1)
    walk(root, 0)
    bar = f'<div class="bar" style="padding:4px 10px">{btn("Expand All")}{btn("Collapse All")}{pop("Sort by Name")}</div>'
    return bar + f'<div class="tbl">{head}{"".join(out)}</div>'


def activity_summary_inspector() -> str:
    def kv(k, v):
        return f'<div class="kv"><span class="k">{k}:</span><span class="v">{esc(v)}</span></div>'
    return ('<div class="insp"><h4>Activity Under This Path</h4>' + kv("Path", H + "/Library/Application Support/NotesSync") + kv("Changes", "32") +
            kv("Created", "3") + kv("Deleted", "3") + kv("Content modified", "23") + kv("Attributes modified", "1") + kv("Moved from", "1") + kv("Moved to", "1") +
            kv("First change", "2026-11-09 21:42:31.866") + kv("Last change", "2026-11-09 21:42:40.112") +
            kv("Busiest processes", "notes-sync (29), cfprefsd (3)") + "</div>")
