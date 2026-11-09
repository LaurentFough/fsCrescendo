#= scenario.py  version 0.1.0 (2026-11-09)
#= Made-up activity used by every mockup: a note-taking app syncing, an updater downloading, a script writing a report, a few shell
#= commands. All paths are under /Users/me; nothing here comes from a real machine.
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Row:
    t: str            # local time, HH:MM:SS.mmm
    cat: str          # created | deleted | modified | attributes | moved_from | moved_to
    pid: int
    proc: str
    inode: int
    path: str
    src: str = ""
    is_dir: bool = False
    count: int = 1


H = "/Users/me"
APP = H + "/Library/Application Support/NotesSync"
UPD = H + "/Library/Caches/ca.example.updater"

ROWS: List[Row] = [
    Row("21:42:31.204", "modified", 621, "cfprefsd", 23980611, H + "/Library/Preferences/ca.example.notes.plist"),
    Row("21:42:31.866", "created", 4182, "notes-sync", 23980640, APP + "/cache/blob-7f3a.tmp"),
    Row("21:42:31.871", "modified", 4182, "notes-sync", 23980640, APP + "/cache/blob-7f3a.tmp"),
    Row("21:42:32.012", "moved_from", 4182, "notes-sync", 23980640, APP + "/cache/blob-7f3a.tmp"),
    Row("21:42:32.012", "moved_to", 4182, "notes-sync", 23980640, APP + "/cache/index.db", src=APP + "/cache/blob-7f3a.tmp"),
    Row("21:42:32.340", "modified", 4182, "notes-sync", 23980655, APP + "/state.json"),
    Row("21:42:33.118", "created", 5120, "UpdateAgent", 23980702, UPD + "/download.partial"),
    Row("21:42:33.502", "modified", 5120, "UpdateAgent", 23980702, UPD + "/download.partial", count=7),
    Row("21:42:34.025", "modified", 5120, "UpdateAgent", 23980710, UPD + "/manifest.json"),
    Row("21:42:34.771", "deleted", 5120, "UpdateAgent", 23980702, UPD + "/download.partial"),
    Row("21:42:35.208", "created", 83266, "touch", 23980731, H + "/work/draft.txt"),
    Row("21:42:35.640", "modified", 83290, "Python", 23980744, H + "/work/report.csv", count=5),
    Row("21:42:36.115", "moved_from", 83298, "mv", 23980731, H + "/work/draft.txt"),
    Row("21:42:36.115", "moved_to", 83298, "mv", 23980731, H + "/work/final.txt", src=H + "/work/draft.txt"),
    Row("21:42:36.902", "attributes", 83308, "chmod", 23980731, H + "/work/final.txt"),
    Row("21:42:37.384", "created", 83331, "installer-helper", 23980760, H + "/Downloads/tool.zip"),
    Row("21:42:37.390", "modified", 83331, "installer-helper", 23980760, H + "/Downloads/tool.zip", count=4),
    Row("21:42:37.911", "attributes", 407, "fseventsd", 23980792, H + "/.Trash"),
    Row("21:42:38.256", "modified", 83390, "Pages", 23980801, H + "/Documents/notes/todo.md", count=3),
    Row("21:42:38.804", "created", 83402, "bash", 23980809, H + "/.local/state/crescendo/sandbox/out.log"),
    Row("21:42:39.327", "modified", 83402, "bash", 23980809, H + "/.local/state/crescendo/sandbox/out.log", count=9),
    Row("21:42:39.950", "deleted", 83439, "rm", 23980731, H + "/work/final.txt"),
    Row("21:42:40.470", "attributes", 621, "kernel_task", 23980611, H + "/Library/Preferences/ca.example.notes.plist"),
    Row("21:42:41.016", "modified", 83390, "Pages", 23980813, H + "/Documents/budget.xlsx"),
]

#= paths for the tree and the graphs: path -> (own changes, last category, is_dir)
PATHS: Dict[str, tuple] = {
    APP + "/cache/index.db": (14, "modified"),
    APP + "/cache/blob-7f3a.tmp": (3, "deleted"),
    APP + "/state.json": (9, "modified"),
    APP + "/NotesSync.log": (6, "modified"),
    H + "/Library/Preferences/ca.example.notes.plist": (6, "attributes"),
    UPD + "/download.partial": (9, "deleted"),
    UPD + "/manifest.json": (2, "modified"),
    H + "/work/report.csv": (8, "modified"),
    H + "/work/draft.txt": (2, "moved_from"),
    H + "/work/final.txt": (3, "deleted"),
    H + "/Documents/budget.xlsx": (3, "modified"),
    H + "/Documents/notes/ideas.md": (4, "modified"),
    H + "/Documents/notes/todo.md": (7, "modified"),
    H + "/Downloads/installer.pkg": (2, "created"),
    H + "/Downloads/tool.zip": (5, "modified"),
    "/private/var/folders/xy/T/TemporaryItems/tmp-1a2b": (4, "deleted"),
    H + "/.local/state/crescendo/sandbox/out.log": (11, "modified"),
    H + "/.local/state/crescendo/sandbox/result.json": (2, "created"),
    H + "/Pictures/screenshot-0412.png": (1, "created"),
    H + "/Pictures/screenshot-0413.png": (1, "created"),
    H + "/Library/Mail/V10/index.sqlite": (12, "modified"),
    H + "/Library/Mail/V10/attachments/offer.pdf": (2, "created"),
}

#= inspector content for the hero row (the plist modified by cfprefsd)
INSPECTOR = {
    "type": "Property List", "path": H + "/Library/Preferences/ca.example.notes.plist", "created": "2026-11-02 09:14:08.221",
    "modified": "2026-11-09 21:42:31.204", "category": "Content Modified", "event": "Content Modified", "time": "2026-11-09 21:42:31.204",
    "owner_uid": "501", "owner_gid": "20", "mode": "-rw-------", "size": "4,812 bytes", "inode": "23980611", "device": "16777234",
    "pid": "621", "ppid": "1", "pname": "cfprefsd", "ppath": "/usr/sbin/cfprefsd", "sign": "com.apple.cfprefsd.daemon", "puid": "501", "pgid": "20",
}
