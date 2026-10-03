"""Create a portable download of the Codex plugin from its authoritative folder."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


def main():
    root = Path(__file__).resolve().parents[1]
    folder = root / "plugins/solkraft"
    output = root / "docs/downloads/solkraft-plugin.zip"
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(folder.rglob("*")):
            if path.is_file():
                archive.write(path, "solkraft/" + path.relative_to(folder).as_posix())
        archive.write(root / "LICENSE", "solkraft/LICENSE")
    print(output.name)


if __name__ == "__main__":
    main()
