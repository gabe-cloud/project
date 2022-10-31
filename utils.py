from pathlib import Path

from typing import Tuple


def main() -> None:
    """Main function"""
    new_file = Path.cwd() / "new_file.txt"
    new_file.touch()
    new_file.write_text("Test..")
    file_move(new_file)
    print(file_decompose(new_file))

def file_decompose(path: Path) -> Tuple[str, str]:
    """Return the file name and extension"""
    name = path.stem
    extension = path.suffix
    return (name, extension)

def file_move(path: Path) -> None:
    """Move the file to a specific folder"""
    root = Path.cwd()
    folder = Path("test/")
    name = path.name
    path.rename(root / folder / name)


if __name__ == "__main__":
    main()
