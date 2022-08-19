import pathlib
import shutil
import tempfile
from typing import Callable, Literal, cast

import click
import keepachangelog
import keepachangelog._versioning
import semver
import tomlkit


def change_version(
    version_transform: Callable[[semver.VersionInfo], semver.VersionInfo],
    dry_run: bool,
    project_dir: pathlib.Path,
    relax: bool,
):
    pyproject_path = project_dir / "pyproject.toml"
    with open(pyproject_path) as in_stream:
        pyproject_doc = tomlkit.load(in_stream)
    current_version = semver.VersionInfo.parse(
        cast(tomlkit.container.Container, pyproject_doc["project"])["version"]
    )

    new_version = version_transform(current_version)
    new_version_str = str(new_version)
    click.echo(f"Bump version {current_version} → {new_version}")

    changelog_path = project_dir / "CHANGELOG.md"
    if not changelog_path.exists():
        click.echo("Warning: no CHANGELOG.md file in this directory")
        if not relax:
            click.echo("Aborting")
            return 1
    else:
        changelog_dict = keepachangelog.to_dict(changelog_path, show_unreleased=True)
        _, current_semantic_version = keepachangelog._versioning.actual_version(changelog_dict)
        guessed_version = keepachangelog._versioning.guess_unreleased_version(changelog_dict, current_semantic_version)
        if guessed_version != new_version_str:
            click.echo(
                f"According to the changelog content, the new version should be {guessed_version} instead of {new_version}."
            )
            if not relax:
                click.echo("Aborting")
                return 1

    cast(tomlkit.container.Container, pyproject_doc["project"])["version"] = new_version_str

    if dry_run:
        click.echo("\n---pyproject.toml---\n")
        click.echo(pyproject_doc.as_string())
        click.echo("---end pyproject.toml---")
        if changelog_path.exists():
            click.echo("\n---changelog---\n")
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_changelog_path = pathlib.Path(temp_dir) / "CHANGELOG.md"
                shutil.copy(changelog_path, temp_changelog_path)
                keepachangelog.release(temp_changelog_path, new_version=new_version_str)
                click.echo(temp_changelog_path.read_text())
            click.echo("---end changelog---")
    else:
        with open(pyproject_path, "w") as out_stream:
            tomlkit.dump(pyproject_doc, out_stream)
        if changelog_path.exists():
            keepachangelog.release(changelog_path, new_version=new_version)


@click.group(help="Bump versions in changelogs and pyprojects")
def cli():
    pass

project_dir_arg = click.argument(
    "project_dir",
    default=pathlib.Path.cwd(),
    type=click.Path(
        exists=True,
        file_okay=False,
        path_type=pathlib.Path,
        writable=True,
    ),
)
dry_run_opt = click.option(
    "--dry-run",
    help="Don't actually modify the files and print their content in the terminal instead.",
    is_flag=True,
)
relax_opt = click.option(
    "--relax",
    help="Don't require a changelog file or fail if the bumped version is inconsistent with its content.",
    is_flag=True,
)


@cli.command(help="Increment a version segement")
@click.argument("segment", type=click.Choice(["major", "minor", "patch", "prerelease"]))
@click.option(
    "--pre-token",
    default="rc",
    help="The prefix to use for the pre-release segment, ignored for other segments.",
    show_default=True,
)
@project_dir_arg
@dry_run_opt
@relax_opt
def bump(
    dry_run: bool,
    pre_token: str,
    project_dir: pathlib.Path,
    relax: bool,
    segment: Literal["major", "minor", "patch", "prerelease"],
):
    def version_transform(current_version: semver.VersionInfo) -> semver.VersionInfo:
        match segment:
            case "major":
                return current_version.bump_major()
            case "minor":
                return current_version.bump_minor()
            case "patch":
                return current_version.bump_patch()
            case "prerelease":
                return current_version.bump_prerelease(token=pre_token)

    change_version(
        dry_run=dry_run,
        project_dir=project_dir,
        relax=relax,
        version_transform=version_transform,
    )


@cli.command(help="Set the version manually")
@click.argument("version")
@project_dir_arg
@dry_run_opt
@relax_opt
def set(
    dry_run: bool,
    project_dir: pathlib.Path,
    relax: bool,
    version: str,
):
    def version_transform(current_version: semver.VersionInfo) -> semver.VersionInfo:
       return semver.VersionInfo.parse(version)

    change_version(
        dry_run=dry_run,
        project_dir=project_dir,
        relax=relax,
        version_transform=version_transform,
    )