import pathlib
from typing import Literal, cast

import click
import semver
import tomlkit


@click.group(help="Bump versions in changelogs and pyprojects")
def cli():
    pass


@cli.command(help="Increment a version segement")
@click.argument("segment", type=click.Choice(["major", "minor", "patch", "prerelease"]))
@click.argument(
    "project_dir",
    default=pathlib.Path.cwd(),
    type=click.Path(
        exists=True,
        file_okay=False,
        path_type=pathlib.Path,
        writable=True,
    ),
)
@click.option("--dry-run", help="Don't actually modify the files and print their content in the terminal instead.", is_flag=True)
@click.option(
    "--pre-token",
    default="rc",
    help="The prefix to use for the pre-release segment, ignored for other segments.",
    show_default=True,
)
def bump(
    dry_run: bool,
    pre_token: str,
    project_dir: pathlib.Path,
    segment: Literal["major", "minor", "patch", "prerelease"],
):
    pyproject_path = project_dir / "pyproject.toml"
    with open(pyproject_path) as in_stream:
        pyproject_doc = tomlkit.load(in_stream)
    current_version = semver.VersionInfo.parse(
        cast(tomlkit.container.Container, pyproject_doc["project"])["version"]
    )
    match segment:
        case "major":
            new_version = current_version.bump_major()
        case "minor":
            new_version = current_version.bump_minor()
        case "patch":
            new_version = current_version.bump_patch()
        case "prerelease":
            new_version = current_version.bump_prerelease(token=pre_token)
    cast(tomlkit.container.Container, pyproject_doc["project"])["version"] = str(new_version)

    if dry_run:
        click.echo(pyproject_doc.as_string())
    else:
        with open(pyproject_path, "w") as out_stream:
            tomlkit.dump(pyproject_doc, out_stream)