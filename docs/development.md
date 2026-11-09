---
title: "Crescendo development guide"
description: "Repository layout, build and test commands, signing policy, continuous integration and releases, and the conventions used in this project."
slug: crescendo-development
author: "Clauiri (Claude Code session) for the repository owner"
type: how-to
date-created: 2026-11-09
date-modified: 2026-11-09
date-published:
source: "Makefile, .github/workflows, scripts/"
domain: macos-security
url:
draft: false
tags:
  - development
keywords:
  - make
  - CI
  - release
---

# Development

## Layout

| Path | What |
|---|---|
| `Crescendo/` | the macOS app (Swift, AppKit; the storyboard window plus programmatic views) |
| `CrescendoExtension/`, `libCrescendo/` | the original Endpoint Security system extension and framework (not part of the lite build) |
| `daemon/crescendo-esd.swift` | the event daemon (one file, built with `swiftc`) |
| `tools/cresc/` | the engine: standard-library Python 3.9+, tests in `tests/` |
| `scripts/` | build helpers: signing, daemon install, packaging, capture, checks |
| `docs/` | documentation; `docs/screenshots/` pictures and the shot list |
| `.github/workflows/` | CI, release, stale bot |

## Common commands

```bash
make help                 # all targets
make doctor               # tools and environment
make build-lite           # app + event daemon -> build/lite/Crescendo.app
make cresc-test           # engine tests (all platforms)
make check                # signing, personal-data, whitespace, lint, build
make check-pii            # HISTORY=1 also scans commits
make check-docs           # links, images, missing screenshots (STRICT=1 fails on them)
make screenshots          # guided capture (macOS)
make version              # Makefile, git, build number
```

## Signing policy

The repository only uses **"Sign to Run Locally"** (ad-hoc). No team id, certificate or provisioning profile is ever committed
(`scripts/check-signing.sh` enforces this, locally and in CI). The event daemon can be signed with your own identity at install time
(`SIGN_IDENTITY=auto|"name"`), read from the environment only.

## Tests

- Engine: `cd tools/cresc && python3 -m unittest discover -s tests -t .` (run on Linux and macOS, Python 3.9 and 3.13, in CI). Real eslogger captures in `tests/fixtures`.
- Swift: no automated tests yet; the app is built in CI and verified by hand (see [features.md](features.md)).
- Fixtures hold paths as `/Users/me`; `scripts/capture-file-events.sh` makes new ones with your home path redacted.

## Continuous integration and releases

- `ci.yml`: engine tests, hygiene (signing, personal data, shell syntax, docs), and a macOS build of the lite app (artifact kept 7 days).
- `release.yml` is **automatic**: every push to `main` (except documentation-only pushes, or a commit message containing `[skip release]`) runs the tests,
  builds on macOS, and publishes a **pre-release** tagged `v<MAJOR.MINOR>.<build>`. MAJOR.MINOR comes from the `VERSION` file (change it by hand for a new
  minor or major version); build = number of commits, so `0.1` becomes `v0.1.57`. Nothing is tagged by hand. The newest 10 pre-releases are kept.
  To publish a normal release, run the Release workflow by hand (Actions > Release > Run workflow) with **official** ticked: that marks the current `main` as the latest release.
  Assets: `Crescendo-lite-<tag>.zip`, `crescendo-esd-<tag>-<arch>`, `cresc-engine-<tag>.tar.gz`, `SHA256SUMS`, plus a build-provenance attestation.
  No secrets are used; artifacts are ad-hoc signed and not notarized.
- Build identity: version = `VERSION` + build number (commit count), plus the commit and UTC time, stamped into Info.plist (`make version`); local builds use the same rule.
- `dependabot.yml` keeps the actions up to date. For stricter supply-chain hygiene pin the actions to commit SHAs.

## Conventions

- Comments use the comment character followed by `= ` (`#= `, `//= `, `;= `) for real comments; commented-out code uses the plain character.
- Code is versioned in its header; user-visible changes update the docs and [features.md](features.md).
- Dark mode: attributed text always carries an explicit foreground colour (see the checklist in [future-feature-adds.md](future-feature-adds.md)).
- Personal data: use `/Users/me`, `/Users/alice`, documentation IP ranges; run `make check-pii` before pushing.
- Screenshots: `make screenshots`, demo data only, look at each picture before committing.

## Interfaces

- App <-> engine: JSON lines over a pipe, [PROTOCOL.md](../tools/cresc/PROTOCOL.md).
- Engine <-> daemon: Unix socket, [event-daemon.md](event-daemon.md).
- Files: [recording-format.md](recording-format.md), evidence bundles (`cresc.bundle/1`), schemas listed in `tools/cresc/cresc/__init__.py`.
