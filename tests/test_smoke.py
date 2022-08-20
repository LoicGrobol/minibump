import filecmp
import pathlib
import shutil

from semver import VersionInfo
import freezegun
import pytest_console_scripts

from minibump.main import change_version


# TODO: this could all been made much more fun using hypothesis and generating chanagelogs on the fly
# using keepachangelog directly instead of files

@freezegun.freeze_time("2022-08-19")
def test_change_version(
    shared_datadir: pathlib.Path,
):
    """Test that setting the version manually works"""
    change_version(
        version_transform=lambda v: VersionInfo(0, 7, 0),
        dry_run=False,
        project_dir=shared_datadir / "before",
        relax=True,
    )
    assert filecmp.cmp(
        shared_datadir / "before" / "pyproject.toml",
        shared_datadir / "after" / "pyproject.toml",
        shallow=False,
    )
    assert filecmp.cmp(
        shared_datadir / "before" / "CHANGELOG.md",
        shared_datadir / "after" / "CHANGELOG.md",
        shallow=False,
    )


def test_bump(
    script_runner: pytest_console_scripts.ScriptRunner,
    shared_datadir: pathlib.Path,
):
    """Test that the entry point works and succesfully bumps the minor version"""
    ret = script_runner.run(
        "minibump",
        "bump",
        "minor",
        str(shared_datadir / "before"),
        "--relax",
    )
    assert ret.success
    assert filecmp.cmp(
        shared_datadir / "before" / "pyproject.toml",
        shared_datadir / "after" / "pyproject.toml",
        shallow=False,
    )
    # Not comparing changelogs here because the date changes and mocking it is annoying


def test_bump_dry_run(
    script_runner: pytest_console_scripts.ScriptRunner,
    shared_datadir: pathlib.Path,
):
    """Test that files don't change when in dry run mode"""
    shutil.copy(
        shared_datadir / "before" / "pyproject.toml",
        shared_datadir / "before" / "pyproject_orig.toml",
    )
    shutil.copy(
        shared_datadir / "before" / "CHANGELOG.md",
        shared_datadir / "before" / "CHANGELOG_orig.md",
    )
    ret = script_runner.run(
        "minibump",
        "bump",
        "minor",
        str(shared_datadir / "before"),
        "--relax",
        "--dry-run",
    )
    assert ret.success
    assert filecmp.cmp(
        shared_datadir / "before" / "pyproject.toml",
        shared_datadir / "before" / "pyproject_orig.toml",
        shallow=False,
    )
    assert filecmp.cmp(
        shared_datadir / "before" / "CHANGELOG.md",
        shared_datadir / "before" / "CHANGELOG_orig.md",
        shallow=False,
    )
