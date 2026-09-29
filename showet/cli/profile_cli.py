"""CLI for Showet configuration profiles.

Entry point: ``showet-profile`` (see pyproject.toml).

Commands
--------
create <name> <KEY=VAL>...   Create or overwrite a profile.
list                         List all profile names.
show <name>                Print a profile's variables (secrets masked).
delete <name>              Remove a profile.
run <name> -- <cmd>...     Execute <cmd> with the profile's env vars.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from showet.profile import (
    ProfileStore,
    profiles_dir,
    run_profile as _run_profile,
    run_profile,  # re-export for test imports
)

# Re-export command handlers under the names the test suite imports.
list_profiles = None  # type: ignore[assignment]
show_profile = None  # type: ignore[assignment]
delete_profile = None  # type: ignore[assignment]

# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------

def _cmd_list(store: ProfileStore) -> int:
    names = store.list_names()
    for n in names:
        print(n)
    return 0


def _cmd_show(store: ProfileStore, name: str) -> int:
    try:
        doc = store.load(name)
    except KeyError:
        print(f"Error: profile {name!r} not found")
        return 1
    from showet.profile import print_profile as _pp
    _pp(doc)
    return 0


def _cmd_delete(store: ProfileStore, name: str) -> int:
    if not store.delete(name):
        print(f"Error: profile {name!r} not found", file=sys.stderr)
        return 1
    print(f"Deleted profile {name!r}.")
    return 0


def _cmd_create(store: ProfileStore, name: str, variables: list[str], description: str) -> int:
    pairs: list[tuple[str, str]] = []
    for item in variables:
        if "=" not in item:
            print(f"Error: invalid variable format {item!r} (expected KEY=VALUE)", file=sys.stderr)
            return 2
        key, val = item.split("=", 1)
        pairs.append((key, val))
    try:
        store.create(name, pairs, description=description)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Created profile {name!r}.")
    return 0


def _cmd_run(store: ProfileStore, name: str, child_cmd: list[str]) -> int:
    rc, out, err = _run_profile(store, name, child_cmd)
    if out:
        sys.stdout.write(out)
    if err:
        sys.stderr.write(err)
    return rc


# Public aliases used by tests.
list_profiles = _cmd_list
show_profile = _cmd_show
delete_profile = _cmd_delete

# ---------------------------------------------------------------------------
# parser
# ---------------------------------------------------------------------------

def _examples() -> str:
    import textwrap
    return textwrap.dedent("""\
        Examples:
          showet-profile create dev SHOWET_DEBUG=true SHOWET_TIMEOUT=60
          showet-profile list
          showet-profile show dev
          showet-profile run dev -- showet 12345
          showet-profile delete dev
    """)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="showet-profile",
        description="Showet configuration profiles — manage named SHOWET_* env-var sets.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=_examples(),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_create = sub.add_parser("create", help="Create or overwrite a profile")
    p_create.add_argument("name", help="Profile name (alphanumeric, '.', '-', '_' only)")
    p_create.add_argument("variables", nargs="+", help="Variables as KEY=VALUE pairs")
    p_create.add_argument("--description", "-d", default="", help="Optional description")

    sub.add_parser("list", help="List all profile names")

    p_show = sub.add_parser("show", help="Show a profile's variables")
    p_show.add_argument("name", help="Profile name")

    p_del = sub.add_parser("delete", help="Delete a profile")
    p_del.add_argument("name", help="Profile name")

    p_run = sub.add_parser("run", help="Run a command with a profile's environment")
    p_run.add_argument("name", help="Profile name")
    p_run.add_argument("child", nargs=argparse.REMAINDER,
                       help="Command and arguments to run (use '--' to separate from options)")

    return parser


def _parse_run_args(args: argparse.Namespace) -> tuple[str, list[str]]:
    child = list(args.child) if args.child else []
    if child and child[0] == "--":
        child = child[1:]
    if not child:
        print("Error: run requires a command after '--'", file=sys.stderr)
        sys.exit(2)
    return args.name, child


def main(argv: list[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)

    store = ProfileStore(profiles_dir())

    if args.command == "create":
        return _cmd_create(store, args.name, args.variables, args.description)
    elif args.command == "list":
        return _cmd_list(store)
    elif args.command == "show":
        return _cmd_show(store, args.name)
    elif args.command == "delete":
        return _cmd_delete(store, args.name)
    elif args.command == "run":
        name, child = _parse_run_args(args)
        return _cmd_run(store, name, child)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
