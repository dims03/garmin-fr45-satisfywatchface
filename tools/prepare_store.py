"""Prepare the already-delivered v1 sources for a separate Store export.

The main workspace also contains an unshipped HR experiment. Export the source
archive matching the version installed by the user, without changing that work.
"""
from pathlib import Path
from zipfile import ZipFile
import hashlib

root = Path(__file__).resolve().parents[1]
destination = root / 'publishing' / 'source-v1'
destination.mkdir(parents=True, exist_ok=True)
with ZipFile(root / 'output' / 'SATISFY-FR45-install.zip') as z:
    release = z.read('SATISFY-FR45.prg')
assert hashlib.sha256(release).hexdigest() == 'bae4f744aacb13e51752f7b9b337c5afed79b6135e2773f055fb9b7c0e813618'
with ZipFile(root / 'output' / 'SATISFY-FR45-source.zip') as archive:
    for name in archive.namelist():
        if name not in ('manifest.xml', 'monkey.jungle') and not name.startswith(('source/', 'resources/')):
            continue
        target = (destination / name).resolve()
        assert target.is_relative_to(destination.resolve()), 'Unsafe archive path'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(archive.read(name))
print('Prepared the delivered v1 sources for Store export at ' + str(destination))
