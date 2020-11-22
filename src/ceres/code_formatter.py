import argparse
import pathlib
import black
import os


def find_top_dir() -> pathlib.Path:
    top_dir = None
    for dir_path in pathlib.Path(__file__).resolve().parents:
        if dir_path.stem == "src":
            top_dir = dir_path

    if top_dir is None:
        raise FileNotFoundError("Cannot find top directory (looking for 'src')")

    return top_dir


def format_all_files(top_directory: pathlib.Path) -> None:
    for file_dir, _, files in os.walk(top_dir):
        for file in files:
            file = pathlib.Path(file_dir) / file
            if file.suffix != ".py":
                continue
            if black.format_file_in_place(
                file, fast=True, mode=black.FileMode(), write_back=black.WriteBack.YES
            ):
                print(f"Reformatted {file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Formats all python files in a directory."
    )
    parser.add_argument(
        "-d", "--dir", metavar="directory", required=False, help="The top directory"
    )
    args = parser.parse_args()

    top_dir = find_top_dir() if args.dir is None else args.dir
    format_all_files(top_dir)
