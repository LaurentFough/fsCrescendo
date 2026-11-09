---
title: Documentation images
description: How the pictures in docs/screenshots are made and how to replace them with real captures
slug: docs-screenshots
author: fsCrescendo contributors
type: note
date-created: 2026-11-09
date-modified: 2026-11-09
draft: false
tags: [docs, screenshots]
keywords: [mockups, screenshots]
---

# Documentation images

> **The pictures here are illustrations, not screenshots.** They are drawn from HTML mockups (`scripts/mockups/`) that copy the
> layout, controls and wording of the app, with made-up data (a fictional user `/Users/me`). Each image says
> "illustration - not a screenshot". Details such as fonts and spacing differ from the real app.

- Regenerate the illustrations: `make mockups` (Python 3.12+, Node with `playwright`).
- Replace them with real captures: `make screenshots` (macOS). It shows, one shot at a time, which window and features to put on screen;
  you capture with your own tool (Shottr, CleanShot, ...) and the script picks up the newest image from `~/Desktop` (`WATCH=dir` to
  change it) or a path you type, and stores it as PNG. `make screenshots-builtin` is the fallback that uses macOS `screencapture`.
  `ONLY=name` does one shot, `REDO=1` redoes shots already captured. Real captures are listed in `.real-captures`. A real capture overwrites the illustration of the same name; the
  shot list is in `SHOTS.txt`. Look at every picture before committing it.
