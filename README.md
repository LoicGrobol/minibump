Minibump
=========

[![Latest PyPI version](https://img.shields.io/pypi/v/minibump.svg)](https://pypi.org/project/minibump)
[![Build Status](https://github.com/LoicGrobol/minibump/actions/workflows/ci.yml/badge.svg)](https://github.com/LoicGrobol/minibump/actions?query=workflow%3ACI)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Bump versions in changelogs and pyprojects and be minimalist about it:

- Only supports [semantic versioning](https://semver.org).
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
  nothing and fail (see the `--relax/--strict` option).

Options:

- `--dry-run`: don't modify the files in place and prints the result in the console instead
- `--relax/--strict`: in strict mode (default), inconsistencies between changes and version make
  minibump abort. in relax mode, this will simply result in a warning.

Alternatively you can set a version yourself directly (in that case the default mode is relax) with `set`:

```console
minibump bump [OPTIONS] VERSION [PROJECT DIR]
```

Where `VERSION` is the version to set, which still has to be semver-compatible.

## Inspirations and similar tools

Minibump is made to fit my own need as closely as possible. Although I would be glad to make evolve
to also suit other people's needs, you might also want to have a look at
[`bump2version`](https://pypi.org/project/bump2version/) and [the
alternatives](https://github.com/c4urself/bump2version/blob/master/RELATED.md) they suggest.

As it is, Minibump is mostly a wrapper around [semver](https://python-semver.readthedocs.io) and
[keep-a-changelog](https://github.com/Colin-b/keepachangelog), with
[tomlkit](https://github.com/sdispater/tomlkit) as a backend for metadata parsing.

## Licence

This software is released under the MIT Licence see [LICENCE.md](LICENCE.md) for the details.
