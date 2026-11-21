"""Evidence grading, provenance, and reproducible claim scoring."""
from collections import defaultdict

EVIDENCE = [
 {"id":"mkultra","title":"MKULTRA historical experimentation","status":"established","domain":"history","source":"https://www.intelligence.senate.gov/1977/08/03/hearings-joint-hearing-subcommittee-health-and-scientific-research-committee-human-resources-project/","summary":"Senate hearings document CIA behavioral experiments; no evidence here of satellite V2K."},
 {"id":"microwave-auditory","title":"Microwave auditory effect","status":"established","domain":"biophysics","source":"https://pmc.ncbi.nlm.nih.gov/articles/PMC8733248/","summary":"Pulsed RF can induce auditory sensations under studied conditions; does not establish covert speech delivery."},
 {"id":"directed-energy","title":"Directed energy research","status":"established","domain":"engineering","source":"https://www.jnlwp.defense.gov/","summary":"Government research into nonlethal directed energy exists; applications differ greatly."},
 {"id":"satcom","title":"Satellite communications and sensing","status":"established","domain":"space","source":"https://www.nasa.gov/","summary":"Satellites relay signals and collect remote sensing data; this does not establish brain targeting."},
 {"id":"ahi-assessment","title":"Intelligence community anomalous health incidents assessment","status":"assessed","domain":"intelligence","source":"https://www.dni.gov/files/ODNI/documents/assessments/NIC-Unclassified-ICA-Updated-Assessment-AHI-December2024.pdf","summary":"Agencies differ on RF capability assessments; no confirmation of satellite V2K."},
 {"id":"xkeyscore","title":"XKEYSCORE public reporting","status":"reported","domain":"sigint","source":"https://www.theguardian.com/world/2013/jul/31/nsa-top-secret-program-online-data","summary":"Public reporting describes signals-intelligence search and analysis, not a public API or neural interface."},
 {"id":"satellite-v2k","title":"Operational satellite voice-to-skull system","status":"unverified","domain":"hypothesis","source":None,"summary":"No independent replicable demonstration or authenticated operational evidence."},
 {"id":"remote-thoughts","title":"Satellite-based arbitrary thought decoding","status":"unverified","domain":"hypothesis","source":None,"summary":"No demonstrated ability to decode arbitrary mental content remotely from orbit."},
]
CLAIMS = [
 {"id":"c1","claim":"CIA conducted unethical behavioral experiments","evidence":["mkultra"],"assessment":"supported"},
 {"id":"c2","claim":"Pulsed RF can produce auditory sensations","evidence":["microwave-auditory"],"assessment":"supported"},
 {"id":"c3","claim":"Satellite-based covert intelligible speech delivery is operational","evidence":["satcom","microwave-auditory","satellite-v2k"],"assessment":"not established"},
 {"id":"c4","claim":"SIGINT databases can remotely decode thoughts","evidence":["xkeyscore","remote-thoughts"],"assessment":"not established"},
]
def analyze_claim(claim_id: str):
    claim = next((c for c in CLAIMS if c['id']==claim_id), None)
    if claim is None:
        return None
    items = [e for e in EVIDENCE if e['id'] in claim['evidence']]
    missing = [e['id'] for e in items if e['status']=='unverified']
    return {**claim,"sources":items,"unverified_dependencies":missing,"caution":"Evidence of component technologies does not prove an integrated system."}

def coverage():
    counts=defaultdict(int)
    for item in EVIDENCE:
        counts[item['status']]+=1
    return dict(counts)
