#! /usr/bin/env python3
import argparse
import os
import pathlib
from collections.abc import Generator
from datetime import datetime, timedelta
from os import path


def main(dir: pathlib.Path, age: int, recursive: bool):
    # Confirm valid path
    if not path.isdir(dir):
        raise NotADirectoryError(f"{dir} is not a valid directory")

    current_datetime = datetime.now()
    for entry in scantree(path=dir, recursive=recursive):
        modified = datetime.fromtimestamp(entry.stat().st_mtime)
        if current_datetime - modified > timedelta(days=age):
            print(f"Removing Filename: {entry.name}, Modified: {modified}, Path: {entry.path}")
            os.remove(entry.path)


def scantree(path: pathlib.Path, recursive: bool) -> Generator[os.DirEntry[str], None, None]:
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=True) and recursive:
            yield from scantree(path=pathlib.Path(entry.path), recursive=recursive)
        else:
            yield entry


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--dir", action="store", type=pathlib.Path, required=True, help="path of the directory to clean"
    )
    arg_parser.add_argument(
        "--age", action="store", type=int, default=180, help="minimum age in days of files to remove (default: 180)"
    )
    arg_parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="operate on files and directories recursively",
    )
    args = arg_parser.parse_args()
    main(dir=args.dir, age=args.age, recursive=args.recursive)
