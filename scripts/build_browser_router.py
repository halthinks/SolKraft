"""Package public production Python inputs for the GitHub Pages WebAssembly worker."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def build_runtime(output=None):
    output = Path(output or ROOT / 'docs/assets/router-runtime.zip')
    package = ROOT / 'solkraft'
    paths = sorted(path for path in package.rglob('*') if path.is_file()
                   and '__pycache__' not in path.parts and path.suffix != '.pyc'
                   and (path.parent == package or 'skillpacks' in path.parts or 'schemas' in path.parts))
    digest = hashlib.sha256()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in paths:
            name = path.relative_to(ROOT).as_posix()
            data = path.read_bytes()
            digest.update(name.encode('utf-8') + b'\0' + data)
            info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
    return {'file_count': len(paths), 'production_inputs_sha256': digest.hexdigest(),
            'archive_sha256': hashlib.sha256(output.read_bytes()).hexdigest()}


if __name__ == '__main__':
    print(json.dumps(build_runtime(), indent=2))
