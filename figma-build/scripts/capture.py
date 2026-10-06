#!/usr/bin/env python3
"""Send sections of a running page to Figma, one frame per section.

Usage:
    python3 capture.py jobs.json

jobs.json is a list of {"url": ..., "selector": ..., "id": ...}: one per section, where id is a
capture id from the Figma tool `generate_figma_design` (one call per section). Optional per job:
"width" (default 1440; 390 for phone, which also gets an 844 high phone viewport) and
"profile" (a folder from `shot.py --login`, for pages that need a signed-in account). The page must be
served locally (a production build, e.g. `next start -p 3107`, or `python3 -m http.server`).
Runs four headless Chromes at once through shot.py --eval (next to this file), which
injects Figma's capture script; no site source is touched.
"""
import json, os, queue, subprocess, sys, threading

SHOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shot.py')

def js(sel, cid):
    s = json.dumps(sel)
    return f"""(async()=>{{
document.querySelectorAll('img').forEach(i=>i.loading='eager');
for(let y=0;y<document.body.scrollHeight;y+=500){{scrollTo(0,y);await new Promise(r=>setTimeout(r,60));}}
scrollTo(0,0);
document.querySelectorAll('.anim').forEach(e=>e.classList.remove('anim'));
await Promise.all([...document.images].map(i=>i.decode().catch(()=>0))); await document.fonts.ready;
const el=document.querySelector({s});
let p=el,bg='rgba(0, 0, 0, 0)';while(p&&(bg=getComputedStyle(p).backgroundColor)==='rgba(0, 0, 0, 0)')p=p.parentElement;
if(p&&p!==el)el.style.backgroundColor=bg;
await new Promise(r=>setTimeout(r,800));
await new Promise((ok,bad)=>{{const t=document.createElement('script');t.src='https://mcp.figma.com/mcp/html-to-design/capture.js';t.onload=ok;t.onerror=()=>bad('noscript');document.head.appendChild(t);}});
await new Promise(r=>setTimeout(r,500));
window.figma.captureForDesign({{captureId:'{cid}',endpoint:'https://mcp.figma.com/mcp/capture/{cid}/submit?bindVariables=true',selector:{s}}});
await new Promise(r=>setTimeout(r,45000));return 'sent';}})()"""

jobs = json.load(open(sys.argv[1]))
q = queue.Queue()
for i, j in enumerate(jobs): q.put((i, j))

def worker(port):
    while True:
        try: i, j = q.get_nowait()
        except queue.Empty: return
        w = j.get('width', 1440)
        args = ['python3', SHOT, j['url'], '--wait', '3', '--width', str(w),
                '--height', '844' if w < 600 else '1200', '--port', str(port)]
        if j.get('profile'): args += ['--profile', j['profile']]
        p = subprocess.Popen(args + ['--eval', js(j['selector'], j['id'])],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        try: out = p.communicate(timeout=90)[0]
        except subprocess.TimeoutExpired: p.kill(); out = 'timeout'
        print(i + 1, j['selector'], j['id'][:8], out.strip()[-60:], flush=True)

ts = [threading.Thread(target=worker, args=(9401 + k,)) for k in range(4)]
[t.start() for t in ts]; [t.join() for t in ts]; print('done')
