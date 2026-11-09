---
title: Notice and attribution
description: Where fsCrescendo comes from, what is original, and how to follow the upstream project
slug: notice
author: fsCrescendo contributors
type: note
date-created: 2026-11-09
date-modified: 2026-11-09
draft: false
tags: [license, attribution]
keywords: [fork, upstream, Crescendo, MIT]
---

# Notice and attribution

fsCrescendo is a **fork of [Crescendo](https://github.com/SuprHackerSteve/Crescendo)** by Stephen Davis (originally published
by FireEye, Inc.), used and modified under the MIT licence. The licence texts, including the original copyright notices, are in
[LICENSE](LICENSE) and must stay with any copy or derivative of this repository.

## What comes from upstream

- The Endpoint Security system extension, framework, command-line client and the original app code (`CrescendoExtension/`,
  `CrescendoFramework.xcodeproj/`, `libCrescendo/`, `Crescendo-cli/`, and the base of `Crescendo/`).
- The original project name, icon assets and the idea of a file/process/network event viewer.

## What this fork adds

The "lite" build that needs no Endpoint Security entitlement: the root event daemon (`daemon/`), the `cresc` engine (`tools/cresc/`),
the Cresc Console, the Files view (list, text, tree, graph), recordings and the player, plus the build, CI and release tooling.

## Git history

This repository was started from a clean tree (a single first commit) so that no personal data from earlier working copies is
published. It therefore does **not** share git history with upstream, and GitHub does not show it as a "fork" in its network graph.
To compare with upstream, add it as a remote:

```sh
git remote add upstream https://github.com/SuprHackerSteve/Crescendo.git
git fetch upstream
git log --oneline upstream/master      # check the upstream default branch name first
```

Upstream changes cannot be merged automatically (unrelated histories); port them by hand or with `git cherry-pick` after review.
