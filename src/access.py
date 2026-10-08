"""Read-only access probes. Never acquire or log credentials."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import subprocess
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from inventory import load_bom, write_si

ROOT=Path(__file__).resolve().parents[1]
TARGETS={
 'assignment':'https://tiangong-lca-decision-lab.ecodino73.chatgpt.site/',
 'original_bom':'https://tiangong-lca-decision-lab.ecodino73.chatgpt.site/classroom/kettle-bom.csv',
 'uslci':'https://www.lcacommons.gov/lca-collaboration/National_Renewable_Energy_Laboratory/USLCI_Database_Public/datasets',
}

def probe(url):
    try:
        with urlopen(Request(url,headers={'User-Agent':'KettleLCA-Research/1.0'}),timeout=20) as r:
            body=r.read(4_000_001)
            if len(body)>4_000_000: return {'status':'response-too-large'},None
            return {'status':'retrieved','http_status':r.status,
                    'sha256':hashlib.sha256(body).hexdigest(),'bytes':len(body)},body
    except HTTPError as e:
        return {'status':'http-error','http_status':e.code},None
    except (URLError,TimeoutError,OSError):
        # Exception messages may contain infrastructure URLs; retain only safe status.
        return {'status':'network-or-proxy-error'},None

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--cli',default='/workspace/lca-tools/node_modules/.bin/tiangong-lca')
    args=ap.parse_args()
    run_id=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out=ROOT/'data/provenance'/run_id
    out.mkdir(parents=True,exist_ok=False)
    report={'run_id':run_id,'urls':{},'database_access_confirmed':False,
            'environment':{},'credentials':{},'baseline_status':'not calculated'}
    for executable in ('python3','node'):
        p=subprocess.run([executable,'--version'],capture_output=True,text=True)
        report['environment'][executable]=p.stdout.strip()
    for name in sorted(os.environ):
        if name.startswith('TIANGONG_'):
            report['credentials'][name]='present' if os.environ[name] else 'empty'
    for name,url in TARGETS.items():
        status,body=probe(url)
        report['urls'][name]={'url':url,**status}
        if name=='original_bom' and body is not None:
            candidate=out/'downloaded-bom.csv'
            candidate.write_bytes(body)
            try:
                rows,totals=load_bom(candidate)
                report['urls'][name]['schema_and_mass_valid']=True
                # Preserve each retrieval; do not silently replace the supplied BOM.
                write_si(rows,out/'downloaded-bom-si.csv')
            except (ValueError,UnicodeError,KeyError):
                report['urls'][name]['schema_and_mass_valid']=False
    env=os.environ.copy()
    env['XDG_STATE_HOME']='/workspace/lca-tools/state'
    env['XDG_CONFIG_HOME']='/workspace/lca-tools/config'
    try:
        p=subprocess.run([args.cli,'--version'],env=env,capture_output=True,text=True,timeout=30)
        report['environment']['tiangong_cli']=p.stdout.strip()
        p=subprocess.run([args.cli,'auth','status','--json'],env=env,capture_output=True,text=True,timeout=30)
        report['tiangong_auth']=json.loads(p.stdout)
        p=subprocess.run([args.cli,'search','process','--input',str(ROOT/'data/mapping/requests/04.json'),'--json'],
                         env=env,capture_output=True,text=True,timeout=30)
        report['tiangong_search_exit_code']=p.returncode
        if p.returncode:
            try:
                obj=json.loads(p.stdout or p.stderr)
                report['tiangong_search_error_code']=obj.get('error',{}).get('code','unknown')
            except ValueError: report['tiangong_search_error_code']='unparsed-error'
        else:
            # Search results are not provider closure or permission to redistribute.
            (out/'process-search.json').write_text(p.stdout)
            report['tiangong_search_status']='response received; requires review'
    except (OSError,subprocess.TimeoutExpired,ValueError):
        report['tiangong_status']='tool-unavailable-or-invalid-response'
    (out/'access_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
