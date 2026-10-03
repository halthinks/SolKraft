import json, sys
from pathlib import Path

STATES={"SELECTED","CONDITIONAL","BLOCKED","REOPENED","SUPERSEDED","REJECTED"}
REQUIRED={"selection_id","product","profile","revision","item","state","selection_reason","evidence","open_gaps","validation_gates"}

def main(path):
    data=json.loads(Path(path).read_text(encoding="utf-8"))
    rows=data.get("selections",data if isinstance(data,list) else [])
    errors=[]; ids=set()
    for i,row in enumerate(rows):
        missing=sorted(REQUIRED-set(row))
        if missing: errors.append(f"row {i}: missing {', '.join(missing)}")
        sid=row.get("selection_id")
        if sid in ids: errors.append(f"row {i}: duplicate selection_id {sid}")
        ids.add(sid)
        if row.get("state") not in STATES: errors.append(f"row {i}: invalid state {row.get('state')}")
        if row.get("state") in {"REOPENED","SUPERSEDED"} and not row.get("change_evidence"):
            errors.append(f"row {i}: {row.get('state')} requires change_evidence")
        if row.get("state")=="SUPERSEDED" and not row.get("successor_selection_id"):
            errors.append(f"row {i}: SUPERSEDED requires successor_selection_id")
    if errors:
        print("FAIL\n"+"\n".join(errors)); return 1
    print(f"PASS: {len(rows)} selections; unique IDs and state/change gates valid")
    return 0

if __name__=="__main__":
    raise SystemExit(main(sys.argv[1]))
