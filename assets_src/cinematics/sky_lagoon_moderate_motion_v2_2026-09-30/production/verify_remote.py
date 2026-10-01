"""Anonymous HTTPS verification of the complete exact GitHub revision."""
import argparse
import concurrent.futures
import hashlib
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REL = 'assets_src/cinematics/sky_lagoon_moderate_motion_v2_2026-09-30'


def sha(data): return hashlib.sha256(data).hexdigest()


def fetch(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'SkyLagoonReferenceByteVerifier/2.0'}), timeout=45) as response:
                assert response.status == 200
                return response.read()
        except Exception:
            if attempt == 2: raise
            time.sleep(attempt + 1)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('revision');parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    assert len(args.revision)==40 and all(c in '0123456789abcdef' for c in args.revision)
    base='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+args.revision+'/'+REL+'/'
    data=fetch(base+'MANIFEST.json');manifest=json.loads(data)
    assert data==(ROOT/'MANIFEST.json').read_bytes(), 'Manifest bytes differ from staged archive'

    def verify(row):
        assert not row['path'].startswith('/') and '..' not in Path(row['path']).parts
        body=fetch(base+urllib.parse.quote(row['path'],safe='/'))
        assert len(body)==row['bytes'] and sha(body)==row['sha256'],row['path']
        return {'path':row['path'],'bytes':len(body),'sha256':sha(body),'http_status':200}

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(verify,manifest['files']))
    payload=sha(''.join(r['path']+'\t'+r['sha256']+'\n' for r in sorted(rows,key=lambda r:r['path'])).encode())
    assert payload==manifest['packet_payload_sha256']
    receipt={'status':'PASS','ARCHIVE_COMPLETE':True,'GENERATION_READY':False,'DELIVERY_ACCEPTED':False,
             'repository':'https://github.com/Ebonyks/mermaid-roshan-reef','branch':manifest['branch'],
             'packet_revision':args.revision,'entry_link':'https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+manifest['branch']+'/'+REL,
             'immutable_tree_link':'https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+args.revision+'/'+REL,
             'direct_manifest_link':base+'MANIFEST.json','manifest_sha256':sha(data),'packet_payload_sha256':payload,
             'access_mode':'Anonymous HTTPS GET; no credentials, cookies or authenticated GitHub session. Existing public recipient access.',
             'checked_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'files_verified':len(rows),'files':rows,
             'limits':'Published reference-byte delivery only. Six-key animation polish, new owner selection, runtime/device/child and cinematic acceptance remain open. Receipt excluded from payload to avoid circular hashing.'}
    args.output.write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    print('ANONYMOUS EXACT-REVISION PASS: '+str(len(rows))+' files; '+payload, flush=True)


if __name__=='__main__':main()
