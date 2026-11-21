"""Public-source evidence API; no private intelligence access or surveillance."""
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from .physics import fspl_db, wavelength_m, photon_energy_ev
from .research import EVIDENCE, CLAIMS, analyze_claim, coverage

ROOT=Path(__file__).resolve().parent.parent
app=FastAPI(title='EvidenceChain Research API',version='1.0.0',description='Open-source evidence mapping and educational RF calculations. No operational SIGINT integration.')
app.mount('/assets',StaticFiles(directory=ROOT/'assets'),name='assets')

class RFRequest(BaseModel):
    frequency_mhz:float=Field(gt=0,le=100000,description='Educational input')
    distance_km:float=Field(gt=0,le=1000000,description='Educational input')

@app.get('/')
def home():
    return FileResponse(ROOT/'index.html')

@app.get('/api/health')
def health():
    return {'status':'ok','version':'1.0.0'}

@app.get('/api/evidence')
def evidence(status:str|None=None,domain:str|None=None,q:str|None=None):
    items=EVIDENCE
    if status:items=[e for e in items if e['status']==status]
    if domain:items=[e for e in items if e['domain']==domain]
    if q:items=[e for e in items if q.lower() in (e['title']+' '+e['summary']).lower()]
    return {'count':len(items),'items':items}

@app.get('/api/evidence/{evidence_id}')
def evidence_detail(evidence_id:str):
    item=next((e for e in EVIDENCE if e['id']==evidence_id),None)
    if item is None:raise HTTPException(404,'Evidence not found')
    return item

@app.get('/api/claims')
def claims():
    return {'items':CLAIMS}

@app.get('/api/claims/{claim_id}')
def claim_detail(claim_id:str):
    result=analyze_claim(claim_id)
    if result is None:raise HTTPException(404,'Claim not found')
    return result

@app.get('/api/summary')
def summary():
    return {'evidence_status_counts':coverage(),'claim_count':len(CLAIMS),'note':'Unverified dependencies prevent asserting an integrated operational capability.'}

@app.post('/api/models/rf')
def rf(request:RFRequest):
    return {'frequency_mhz':request.frequency_mhz,'distance_km':request.distance_km,'free_space_path_loss_db':round(fspl_db(request.frequency_mhz,request.distance_km),3),'wavelength_m':round(wavelength_m(request.frequency_mhz),9),'photon_energy_ev':photon_energy_ev(request.frequency_mhz),'limitations':['Idealized free-space model only','Does not predict biological effects','Does not establish feasibility of targeted audio or mind control']}

@app.get('/api/graph')
def graph():
    nodes=[{'id':e['id'],'type':'evidence','label':e['title'],'status':e['status']} for e in EVIDENCE]+[{'id':c['id'],'type':'claim','label':c['claim'],'status':c['assessment']} for c in CLAIMS]
    edges=[{'source':e,'target':c['id'],'relation':'cited_by'} for c in CLAIMS for e in c['evidence']]
    return {'nodes':nodes,'edges':edges}
