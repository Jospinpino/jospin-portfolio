"""File Organizer, a command line tool that sorts files into category folders.

Scans a target directory and moves files into subfolders (Images, Documents,
Videos, Audio, Archives, Code, Others) based on their extension. Supports a
dry run mode that reports planned moves without touching any file.
"""

import argparse
import shutil
import sys
from collections import Counter
from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".xlsx", ".pptx", ".csv"},
    "Videos": {".mp4", ".mov", ".avi", ".mkv", ".webm"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".html", ".css", ".json", ".java", ".c", ".cpp", ".php"},
}


def category_for(extension):
    extension = extension.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"


def unique_destination(destination):
    """Avoid overwriting an existing file by appending a counter."""
    if not destination.exists():
        return destination
    stem, suffix, parent = destination.stem, destination.suffix, destination.parent
    counter = 1
    while True:
        candidate = parent / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def organize(target_dir, dry_run=False, include_others=True):
    target_dir = Path(target_dir)
    if not target_dir.is_dir():
        raise NotADirectoryError(f"{target_dir} is not a valid directory")

    known_folders = set(CATEGORIES) | {"Others"}
    moved = Counter()
    plan = []

    for item in sorted(target_dir.iterdir()):
        if item.is_dir():
            continue
        if item.name.startswith("."):
            continue
        category = category_for(item.suffix)
        if category == "Others" and not include_others:
            continue
        if item.parent.name in known_folders:
            continue

        dest_folder = target_dir / category
        destination = unique_destination(dest_folder / item.name)
        plan.append((item, destination, category))

    for source, destination, category in plan:
        if not dry_run:
            destination.parent.mkdir(exist_ok=True)
            shutil.move(str(source), str(destination))
        moved[category] += 1

    return moved, plan


def main():
    parser = argparse.ArgumentParser(
        description="Sort files in a directory into category subfolders."
    )
    parser.add_argument("directory", help="Directory to organize")
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview the moves without touching any file"
    )
    parser.add_argument(
        "--skip-others",
        action="store_true",
        help="Leave unrecognized file types where they are, instead of moving them to Others",
    )
    args = parser.parse_args()

    try:
        moved, plan = organize(
            args.directory, dry_run=args.dry_run, include_others=not args.skip_others
        )
    except NotADirectoryError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if not plan:
        print("Nothing to organize, the directory is already tidy.")
        return

    verb = "Would move" if args.dry_run else "Moved"
    for source, destination, category in plan:
        print(f"{verb}: {source.name} -> {category}/{destination.name}")

    print()
    print("Summary:")
    for category, count in sorted(moved.items()):
        print(f"  {category}: {count} file(s)")

    if args.dry_run:
        print("\nThis was a dry run, no files were actually moved.")


if __name__ == "__main__":
    main()
