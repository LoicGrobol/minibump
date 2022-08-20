Minibump
=========

[![Latest PyPI version](https://img.shields.io/pypi/v/zeldarose.svg)](https://pypi.org/project/zeldarose)
[![Build Status](https://github.com/LoicGrobol/zeldarose/actions/workflows/ci.yml/badge.svg)](https://github.com/LoicGrobol/zeldarose/actions?query=workflow%3ACI)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Bump versions in changelogs and pyprojects and be minimalist about it:

- Only supports [semnatic versioning](https://semver.org).
- Only supports standard tool-independent version fields in `pyproject.toml`.
- Only supports the [Keep a changelog](https://keepachangelog.com) format, in Markdown and with
  `CHANGELOG.md` as a file name.
- Doesn't interact with git at all, either by inferring changelog entries from commits or making
  commits or tags for you.
- Warns you if you try to set a version that is inconsistent with your changelog entries.

## Installation

Installation with [pipx](https://pypa.github.io/pipx/) is recommended. You might have to [install
pipx itself](https://pypa.github.io/pipx/installation/) first.

```console
pipx install minibump
```

## Usage

Increment one of the semantic versioning segments using `bump`:

```console
minibump bump [OPTIONS] SEGMENT [PROJECT DIR]
```

Where

- `SEGMENT` is `major`, `minor`, `patch` or `prerelease`
- `PROJECT DIR` is an optional path to the root of the Python project to update

This will

- Change the version in `pyproject.toml` in the standard `project.version` field, incrementing the
  relevant part.
- Make a new release in your changelog (if present) from the content of the Unreleased section, with
  the appropriate version number, link and date.
- If the segment you were asking to bump is inconsistent with the entries of your changelog, do
  nothing (see the `--relax` option).

Options:

- `--dry-run`: don't modify the files in place and prints the result in the console instead
- `--relax`: ignore inconsistencies between the contents of the changelog and the segment you asked
  to increment.
