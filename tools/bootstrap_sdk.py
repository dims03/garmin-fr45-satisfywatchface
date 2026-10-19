"""Fetch the unmodified Garmin compiler into a project-local tool directory."""
import json
import pathlib
import urllib.request
import zipfile
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEST = ROOT / '.tools'
DEST.mkdir(exist_ok=True)
BASE = 'https://developer.garmin.com/downloads/connect-iq/'

def get(url):
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read()

if '--manager' in sys.argv:
    archive = DEST / 'sdk-manager.zip'
    if not archive.exists():
        archive.write_bytes(get(BASE + 'sdk-manager/connectiq-sdk-manager-windows.zip'))
    with zipfile.ZipFile(archive) as z:
        z.extractall(DEST / 'sdk-manager')
        print('\n'.join(z.namelist()[:25]), flush=True)
    sys.exit(0)

if '--device' in sys.argv:
    endpoint = 'https://api.gcs.garmin.com/ciq-product-onboarding/devices'
    data = json.loads(get(endpoint + '?sdkManagerVersion=1.0.16'))
    matches = [x for x in data if x.get('name') == 'fr45']
    print(json.dumps(matches, indent=2), flush=True)
    for device in matches:
        if device.get('ciqInfoFileExists'):
            payload = get(endpoint + '/' + device['partNumber'] + '/ciqInfo')
            (DEST / 'fr45.zip').write_bytes(payload)
            with zipfile.ZipFile(DEST / 'fr45.zip') as z:
                print(z.namelist(), flush=True)
                z.extractall(DEST / 'Devices' / 'fr45')
            break
    sys.exit(0)

manifest = json.loads(get(BASE + 'sdks/sdks.json'))
(DEST / 'sdks.json').write_text(json.dumps(manifest, indent=2))
latest = manifest[-1]
if '--legacy' in sys.argv:
    latest = {'windows': 'connectiq-sdk-win-3.1.9-2020-06-24-1cc9d3a70.zip'}
archive = DEST / latest['windows']
sdk = DEST / ('sdk-3.1.9' if '--legacy' in sys.argv else 'sdk')
if not archive.exists():
    print('Downloading ' + latest['windows'], flush=True)
    url = BASE + ('' if '--legacy' in sys.argv else 'sdks/') + latest['windows']
    with urllib.request.urlopen(url, timeout=60) as response, archive.open('wb') as output:
        while data := response.read(1024 * 1024):
            output.write(data)
if not sdk.exists():
    print('Extracting official SDK', flush=True)
    with zipfile.ZipFile(archive) as z:
        z.extractall(sdk)
print('SDK ready at ' + str(sdk), flush=True)
for resource in ():
    try:
        data = get(BASE + resource)
        target = DEST / pathlib.Path(resource).name
        target.write_bytes(data)
        print(resource + ': ' + str(len(data)) + ' bytes', flush=True)
    except Exception as e:
        print(resource + ': ' + str(e), flush=True)
