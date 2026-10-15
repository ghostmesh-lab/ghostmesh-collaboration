#!/usr/bin/env python3
import hashlib, json, pathlib, datetime, time, urllib.request, sys
base = pathlib.Path("/tmp/ghostmesh-st001-hyperion-20261015")
peer_raw = (base/"peer-input.json").read_bytes()
assert hashlib.sha256(peer_raw).hexdigest()=="b1da69893a20143b6db8a396ffd0cb69e88df6197f1402c408382b1f2f08bc98"
readme = (base/"repo/experiments/ROUND_ONE_EXPERIMENT.md").read_text()
section=readme.split("## Frozen evaluation questions",1)[1].split("## Scoring interpretation",1)[0]
questions=[l[2:].strip() for l in section.splitlines() if l.startswith("- ")]
assert len(questions)==9
sysmsg="This is a synthetic offline interpretation task. Answer using only the supplied event data. Do not use tools. If something cannot be established, say so."
evidence="Synthetic ST-001 evidence:\n"+peer_raw.decode()+"\n"
protocol={"study_id":"GM-ST001-LOCALQWEN-20261015-01","status":"exploratory preregistered before inference","repo_head":"7e69235d385d1578cb6312f25aa02752f7387ede","peer_input_sha256":hashlib.sha256(peer_raw).hexdigest(),"model":"qwen25-14b-local","backend":"vLLM on owner Hyperion, HTTP localhost:8000","conditions":["all nine questions bundled in one turn","nine independent stateless question turns with identical event data repeated"],"order":"bundled first, isolated Q1-Q9 second","randomization":False,"replicates":1,"temperature":0,"seed":42,"max_output_tokens":{"bundled":2300,"isolated_each":260},"tools":"none","predeclared_limits":["not blind model evaluation","not persistent belief revision","not randomized or replicated","different prompt length/total tokens between arms","no independent external lab","could have training contamination"],"research_questions":questions}
(base/"local_model_protocol.json").write_text(json.dumps(protocol,indent=2)+"\n")
print("PROTOCOL_SHA256="+hashlib.sha256((base/"local_model_protocol.json").read_bytes()).hexdigest(),flush=True)
cases=[("bundled",evidence+"\nAnswer Q1 through Q9 individually:\n"+"\n".join("Q%d. %s"%(i,q) for i,q in enumerate(questions,1)),2300)]
cases.extend(("Q%d"%i,evidence+"\nQuestion: "+q,260) for i,q in enumerate(questions,1))
results=[]
for case,prompt,limit in cases:
  req={"model":"qwen25-14b-local","messages":[{"role":"system","content":sysmsg},{"role":"user","content":prompt}],"temperature":0,"top_p":1,"seed":42,"max_tokens":limit,"stream":False}
  raw=json.dumps(req,separators=(",",":")).encode()
  clock=time.monotonic()
  try:
    with urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:8000/v1/chat/completions",data=raw,headers={"Content-Type":"application/json"}),timeout=120) as response:
      out=json.load(response)
    datum={"case":case,"duration_ms":round(1000*(time.monotonic()-clock)),"prompt_sha256":hashlib.sha256(raw).hexdigest(),"content":out["choices"][0]["message"].get("content",""),"finish_reason":out["choices"][0].get("finish_reason"),"usage":out.get("usage",{}),"model":out.get("model","unknown"),"timestamp_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    print("CASE "+case+" tokens="+str(datum["usage"].get("completion_tokens"))+" finished="+str(datum["finish_reason"])+" ms="+str(datum["duration_ms"]),flush=True)
  except Exception as exc:
    datum={"case":case,"error":str(exc),"duration_ms":round(1000*(time.monotonic()-clock))}
    print("CASE "+case+" ERROR="+str(exc),flush=True)
  results.append(datum)
  (base/"local_model_raw.json").write_text(json.dumps({"protocol":protocol,"results":results},indent=2,ensure_ascii=False)+"\n")
  if "error" in datum:break
raw=(base/"local_model_raw.json").read_bytes()
print("FINISHED "+str(len(results))+"/"+str(len(cases))+" raw_sha256="+hashlib.sha256(raw).hexdigest(),flush=True)
if len(results)!=len(cases):sys.exit(2)
