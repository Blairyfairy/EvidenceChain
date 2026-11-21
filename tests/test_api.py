from fastapi.testclient import TestClient
from app.main import app
from app.physics import fspl_db, wavelength_m
client=TestClient(app)

def test_health():
    assert client.get('/api/health').json()['status']=='ok'

def test_dashboard():
    assert 'EVIDENCE' in client.get('/').text

def test_evidence_filter():
    data=client.get('/api/evidence?status=unverified').json()
    assert data['count']>=1
    assert all(i['status']=='unverified' for i in data['items'])

def test_claim_missing_dependency():
    assert 'satellite-v2k' in client.get('/api/claims/c3').json()['unverified_dependencies']

def test_missing_returns_404():
    assert client.get('/api/claims/unknown').status_code==404

def test_rf_model():
    response=client.post('/api/models/rf',json={'frequency_mhz':1000,'distance_km':100})
    assert response.status_code==200
    assert abs(response.json()['free_space_path_loss_db']-132.44)<0.01

def test_invalid_rf():
    assert client.post('/api/models/rf',json={'frequency_mhz':0,'distance_km':100}).status_code==422

def test_physics():
    assert abs(wavelength_m(1000)-0.299792458)<1e-9
    assert abs(fspl_db(1000,100)-132.44)<1e-6

def test_graph():
    graph=client.get('/api/graph').json()
    assert graph['nodes'] and graph['edges']
