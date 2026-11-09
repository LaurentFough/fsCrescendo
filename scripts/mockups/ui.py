#= ui.py  version 0.1.0 (2026-11-09)
#= Design system for the documentation mockups: HTML/CSS pieces that imitate the Crescendo windows (macOS look, light and dark).
#= These are ILLUSTRATIONS drawn from the real layout (same columns, controls and wording as the app), not screenshots.
from __future__ import annotations

import html

esc = html.escape

CSS = """
:root{--bg:#ececee;--panel:#ffffff;--text:#1d1d1f;--sub:#6e6e73;--line:#d8d8dd;--zebra:#f6f6f8;--bar:#e4e4e8;--ctl:#ffffff;--ctl-line:#c6c6cc;
--sel:#0a60e0;--accent:#0a84ff;--ins:#fafafb;--banner:#fff4cf;--banner-line:#e2c458;--red:#e5382f;--green:#2fb344;--orange:#f5a000;--blue:#2d7cf6;--gray:#8e8e93;
--wall1:#dfe6f2;--wall2:#c9d3e6;--shadow:0 22px 60px rgba(20,30,60,.35),0 0 0 1px rgba(0,0,0,.18)}
.dark{--bg:#2c2c2f;--panel:#1d1d20;--text:#f2f2f6;--sub:#9d9da6;--line:#3a3a40;--zebra:#242427;--bar:#38383c;--ctl:#4a4a50;--ctl-line:#5d5d64;
--sel:#0a58c8;--accent:#2f8bff;--ins:#252528;--banner:#3a3320;--banner-line:#7d6c2b;--red:#ff5a52;--green:#35c759;--orange:#ffab1a;--blue:#4b93ff;--gray:#98989f;
--wall1:#23283a;--wall2:#171a26;--shadow:0 22px 60px rgba(0,0,0,.6),0 0 0 1px rgba(255,255,255,.12)}
*{box-sizing:border-box}
html,body{margin:0}
body{font:13px/1.35 Inter,-apple-system,"Helvetica Neue",Arial,sans-serif;color:var(--text);background:linear-gradient(135deg,var(--wall1),var(--wall2));-webkit-font-smoothing:antialiased}
.stage{display:inline-block;padding:44px 48px;position:relative}
.win{background:var(--bg);border-radius:12px;box-shadow:var(--shadow);overflow:hidden;position:relative}
.title{height:38px;display:flex;align-items:center;padding:0 14px;position:relative;background:var(--bar);border-bottom:1px solid var(--line)}
.tl{display:flex;gap:8px}.tl i{width:12px;height:12px;border-radius:50%;display:block}
.tl i:nth-child(1){background:#ff5f57}.tl i:nth-child(2){background:#febc2e}.tl i:nth-child(3){background:#28c840}
.title b{position:absolute;left:0;right:0;text-align:center;font-weight:600;font-size:13px;pointer-events:none}
.row{display:flex;align-items:center;gap:8px}
.bar{display:flex;align-items:center;gap:8px;padding:8px 14px;flex-wrap:nowrap;white-space:nowrap}
.btn,.pop{display:inline-flex;align-items:center;gap:5px;height:24px;padding:0 11px;border-radius:6px;border:1px solid var(--ctl-line);background:var(--ctl);font-size:12px;color:var(--text)}
.pop::after{content:"\\25BE";font-size:9px;color:var(--sub);margin-left:4px}
.btn.red{color:var(--red);font-weight:500}
.btn.dis{opacity:.45}
.seg{display:inline-flex;border:1px solid var(--ctl-line);border-radius:7px;overflow:hidden;background:var(--ctl)}
.seg span{padding:3px 12px;font-size:12px;border-right:1px solid var(--ctl-line)}.seg span:last-child{border-right:0}
.seg .on{background:var(--accent);color:#fff}
.chk{display:inline-flex;align-items:center;gap:6px;font-size:12px}.chk .box{width:14px;height:14px;border-radius:4px;border:1px solid var(--ctl-line);background:var(--ctl);display:inline-flex;align-items:center;justify-content:center;font-size:10px;color:#fff}
.chk .box.on{background:var(--accent);border-color:var(--accent)}
.search{display:inline-flex;align-items:center;gap:6px;height:24px;width:230px;padding:0 9px;border-radius:12px;border:1px solid var(--ctl-line);background:var(--ctl);color:var(--sub);font-size:12px}
.grow{flex:1}.sub{color:var(--sub)}.mono{font-family:"JetBrains Mono","SF Mono",Menlo,"DejaVu Sans Mono",monospace}
.status{color:var(--sub);font-size:12px}
.panel{background:var(--panel)}
.split{display:flex;border-top:1px solid var(--line)}
.left{flex:1;min-width:0;background:var(--panel)}
.insp{width:300px;background:var(--ins);border-left:1px solid var(--line);padding:12px 14px;font-size:12px;overflow:hidden}
.insp h4{margin:12px 0 4px;font-size:12px;font-weight:700}.insp h4:first-of-type{margin-top:0}
.insp .kv{display:flex;gap:6px;margin:1px 0}.insp .k{color:var(--sub);white-space:nowrap}.insp .v{word-break:break-all}
.insp .big{text-align:center;margin:2px 0 8px}.insp .big small{display:block;color:var(--sub);margin-top:2px}
.tbl{width:100%}
.th,.tr{display:grid;align-items:center;height:24px;padding:0 4px;white-space:nowrap}
.th{font-size:11px;font-weight:600;color:var(--sub);border-bottom:1px solid var(--line);background:var(--panel);height:22px}
.tr:nth-child(odd){background:var(--zebra)}
.tr.sel{background:var(--sel)!important;color:#fff}.tr.sel .sub{color:#d6e4ff}
.tr.del .p{color:var(--red)}.tr.sel.del .p{color:#ffd4d1}
.cell{overflow:hidden;text-overflow:ellipsis;padding:0 4px}
.num{text-align:right;font-variant-numeric:tabular-nums}
.p{display:flex;align-items:center;gap:6px;overflow:hidden}.p span{overflow:hidden;text-overflow:ellipsis}
.legend{display:flex;gap:16px;padding:8px 18px;font-size:11px;border-top:1px solid var(--line);background:var(--panel);color:var(--text)}
.legend span{display:inline-flex;align-items:center;gap:4px}
.banner{display:flex;align-items:center;gap:12px;margin:0 14px 8px;padding:8px 12px;border-radius:8px;background:var(--banner);border:1px solid var(--banner-line);font-size:12px}
.fpanel{margin:0 14px 8px;border:1px solid var(--line);border-radius:7px;padding:8px 10px;background:var(--panel)}
.rule{display:flex;align-items:center;gap:6px;margin-top:6px}
.field{height:24px;display:inline-flex;align-items:center;padding:0 8px;border:1px solid var(--ctl-line);border-radius:5px;background:var(--ctl);min-width:150px;font-size:12px}
.small{font-size:11px}
.ill{position:absolute;right:56px;bottom:14px;font-size:10px;letter-spacing:.04em;color:var(--sub);opacity:.8;text-transform:uppercase}
.menu{position:absolute;background:var(--panel);border:1px solid var(--line);border-radius:8px;box-shadow:0 10px 30px rgba(0,0,0,.35);padding:5px;font-size:12px;min-width:210px;z-index:5}
.menu div{padding:4px 12px;border-radius:5px}.menu .hi{background:var(--accent);color:#fff}.menu hr{border:0;border-top:1px solid var(--line);margin:4px 2px}.menu .off{color:var(--sub)}
.tabs{display:flex;justify-content:center;padding:6px 0}
.log{background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:8px 10px;font-size:11px;line-height:1.5;overflow:hidden}
.hint{color:var(--sub);font-size:11px}
.form{display:grid;grid-template-columns:96px 1fr;gap:8px 10px;align-items:start;padding:10px 14px}
.form .l{text-align:right;padding-top:4px;color:var(--text)}
.list{border:1px solid var(--line);border-radius:4px;background:var(--panel);font-size:12px}.list div{padding:2px 8px;height:20px}.list div:nth-child(odd){background:var(--zebra)}
.btns{display:flex;flex-direction:column;gap:4px}
svg text{font-family:Inter,-apple-system,Arial,sans-serif}
"""

TL = '<div class="tl"><i></i><i></i><i></i></div>'


def page(theme: str, body: str, label: bool = True, width: int | None = None) -> str:
    cls = "dark" if theme == "dark" else ""
    ill = '<div class="ill">illustration - not a screenshot</div>' if label else ""
    style = f' style="width:{width}px"' if width else ""
    return (f'<!doctype html><html class="{cls}"><head><meta charset="utf-8"><title>mockup</title><style>{CSS}</style></head>'
            f'<body class="{cls}"><div class="stage"{style}>{body}{ill}</div></body></html>')


def window(title: str, inner: str, width: int) -> str:
    return f'<div class="win" style="width:{width}px"><div class="title">{TL}<b>{esc(title)}</b></div>{inner}</div>'


#= ---- icons -----------------------------------------------------------------------------------------------------------
def icon(kind: str, size: int = 16) -> str:
    s = size
    if kind == "folder":
        return (f'<svg width="{s}" height="{s}" viewBox="0 0 16 16"><path d="M1 4c0-.7.5-1.2 1.2-1.2h3.4l1.4 1.6h6.8c.7 0 1.2.5 1.2 1.2v6.8c0 .7-.5 1.2-1.2 1.2H2.2C1.5 13.6 1 13.1 1 12.4z" fill="#4aa3f5"/>'
                f'<path d="M1 6.2h14v6.2c0 .7-.5 1.2-1.2 1.2H2.2C1.5 13.6 1 13.1 1 12.4z" fill="#79bcf9"/></svg>')
    colors = {"plist": "#46b06a", "db": "#7a7ae6", "img": "#e57fb0", "zip": "#c9a14a", "txt": "#aeb4bd", "csv": "#46b06a", "app": "#7a7ae6",
              "log": "#aeb4bd", "json": "#f0a030", "pkg": "#c9a14a", "md": "#aeb4bd", "xlsx": "#46b06a", "tmp": "#c3c3c8", "partial": "#c3c3c8"}
    c = colors.get(kind, "#aeb4bd")
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 16 16"><path d="M3 1.5h6.2L13 5.3v8.4c0 .5-.4.8-.8.8H3.8c-.4 0-.8-.3-.8-.8V2.3c0-.4.4-.8 0-.8z" fill="#fff" stroke="#b9b9c0" stroke-width=".8"/>'
            f'<path d="M9.2 1.5v3.1c0 0.4 0.3 0.7 0.7 0.7H13" fill="#e6e6ea" stroke="#b9b9c0" stroke-width=".8"/><rect x="4.5" y="8.4" width="7" height="3.6" rx=".8" fill="{c}"/></svg>')


KIND = {"created": ("#2fb344", "+"), "deleted": ("#e5382f", "✕"), "modified": ("#f5a000", "✎"), "attributes": ("#8e8e93", "⚙"),
        "moved_from": ("#2d7cf6", "↗"), "moved_to": ("#2d7cf6", "↘"), "meta": ("#8e8e93", "…")}
KIND_LABEL = {"created": "Created", "deleted": "Deleted", "modified": "Content Modified", "attributes": "Attributes Modified",
              "moved_from": "Moved From", "moved_to": "Moved To", "meta": "Meta Event"}


def kind_icon(cat: str, size: int = 16) -> str:
    color, glyph = KIND[cat]
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 16 16"><circle cx="8" cy="8" r="7.2" fill="{color}"/>'
            f'<text x="8" y="11.4" font-size="9.5" font-weight="700" text-anchor="middle" fill="#fff">{glyph}</text></svg>')


def legend() -> str:
    cats = ["created", "deleted", "modified", "attributes", "moved_from", "moved_to", "meta"]
    return '<div class="legend">' + "".join(f'<span>{kind_icon(c, 14)}{KIND_LABEL[c]}</span>' for c in cats) + "</div>"


def ext_kind(path: str, is_dir: bool = False) -> str:
    if is_dir:
        return "folder"
    e = path.rsplit(".", 1)[-1].lower() if "." in path.rsplit("/", 1)[-1] else ""
    return {"plist": "plist", "db": "db", "json": "json", "csv": "csv", "txt": "txt", "md": "md", "zip": "zip", "pkg": "pkg", "log": "log",
            "tmp": "tmp", "partial": "partial", "xlsx": "xlsx", "png": "img", "jpg": "img"}.get(e, "txt")


#= ---- controls --------------------------------------------------------------------------------------------------------
def seg(items, on: str) -> str:
    return '<div class="seg">' + "".join(f'<span class="{"on" if i == on else ""}">{esc(i)}</span>' for i in items) + "</div>"


def chk(label: str, on: bool = True) -> str:
    return f'<span class="chk"><span class="box {"on" if on else ""}">{"✓" if on else ""}</span>{esc(label)}</span>'


def pop(label: str, extra: str = "") -> str:
    return f'<span class="pop {extra}">{esc(label)}</span>'


def btn(label: str, extra: str = "") -> str:
    return f'<span class="btn {extra}">{label}</span>'


def search(text: str = "Search") -> str:
    return f'<span class="search">⌕ {esc(text)}</span>'


def main_toolbar(selected: str = "File", capturing: bool = True) -> str:
    segs = ["All Events", "File", "Process", "Network", "Unsigned", "Exclude Apple"]
    first = ('<div class="bar">' + (btn("Stop") if capturing else btn("Start")) + btn("Clear") + btn("\U0001F4BE") + chk("Auto-scroll") +
             '<span class="grow"></span>' + btn("Settings") + search() + "</div>")
    second = '<div class="bar" style="padding-top:0;justify-content:center">' + seg(segs, selected) + "</div>"
    return first + second
