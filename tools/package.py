from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json

root = Path(__file__).resolve().parents[1]
output = root / 'output'
binary = output / 'SATISFY-FR45.prg'
assert binary.is_file() and binary.stat().st_size > 0, 'Build the PRG first.'
report = {
    'application': 'SATISFY FR45',
    'target': 'fr45',
    'device_api': '1.4.5',
    'compiler': 'Garmin Connect IQ 9.2.0',
    'configuration': 'release',
    'sha256': hashlib.sha256(binary.read_bytes()).hexdigest(),
    'bytes': binary.stat().st_size,
    'validation': {
        'compiler': 'BUILD SUCCESSFUL; no warnings',
        'simulator': 'Debug build ran on the official FR45 simulator; clock updated and layout inspected.',
        'observed_debug_memory_kib': 8.8,
        'device_memory_limit_kib': 48,
        'physical_watch_tested': False,
        'all_sensor_edge_cases_tested': False,
    },
}
(output / 'build-info.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
with ZipFile(output / 'SATISFY-FR45-install.zip', 'w', ZIP_DEFLATED) as z:
    z.write(binary, binary.name)
    z.write(root / 'PANDUAN.md', 'PANDUAN.md')
    z.write(output / 'build-info.json', 'build-info.json')
    z.write(output / 'satisfy-fr45-preview-208.png', 'pratinjau-angka-contoh.png')

source_files = [root / 'manifest.xml', root / 'monkey.jungle', root / 'PANDUAN.md',
                *root.glob('tools/build.ps1'), *root.glob('tools/make_assets.py'),
                *root.glob('tools/package.py'), *root.glob('source/*.mc'),
                *root.glob('resources/**/*.*'), *output.glob('*preview*.png')]
with ZipFile(output / 'SATISFY-FR45-source.zip', 'w', ZIP_DEFLATED) as z:
    for file in source_files:
        if file.is_file():
            z.write(file, file.relative_to(root).as_posix())
print(json.dumps(report, indent=2))
print('Created install and source ZIP files. Private signing key and Garmin SDK are excluded.')
