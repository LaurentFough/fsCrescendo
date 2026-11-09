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
- Replace them with real captures: `make screenshots` (macOS). A real capture overwrites the illustration of the same name; the
  shot list is in `SHOTS.txt`. Look at every picture before committing it.
