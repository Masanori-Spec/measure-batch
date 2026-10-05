"""Pinned native consumer gate. Run within an isolated Xvfb session, not a shared display."""
from pathlib import Path
from decimal import Decimal
import os, sys, json, re, subprocess, hashlib, math, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts'/'native'; OUT.mkdir(parents=True,exist_ok=True)
BIN=Path(os.environ['SEAMLY_BIN_DIR']).resolve()
REPORT={'status':'running','release':'v2026.10.5.154','consumer_sha256':'9ab9e43e21637e166507c34a87174f81d01ccb663d5a32a7dc51668915680e7c','checks':[]}
def save(): (OUT/'native-report.json').write_text(json.dumps(REPORT,indent=2))
def run(tool,args,label,expect=0):
 p=subprocess.run([str(BIN/tool),*map(str,args)],cwd=ROOT,text=True,capture_output=True,timeout=90)
 text=p.stdout+'\n'+p.stderr
 (OUT/(label+'.log')).write_text(text)
 REPORT['checks'].append({'check':label,'exit_code':p.returncode})
 save()
 if expect==0: assert p.returncode==0,(label,p.returncode,text)
 else: assert p.returncode!=0,(label,'Invalid formula was accepted by native consumer',text)
 return text
# Basic affine SVG support. Physical scale comes from the SVG's width/height + viewBox,
# not from assuming DPI or measuring page bounds.
I=(1.,0.,0.,1.,0.,0.)
def mul(a,b):
 return (a[0]*b[0]+a[2]*b[1],a[1]*b[0]+a[3]*b[1],a[0]*b[2]+a[2]*b[3],a[1]*b[2]+a[3]*b[3],a[0]*b[4]+a[2]*b[5]+a[4],a[1]*b[4]+a[3]*b[5]+a[5])
NUM=r'[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?'
def numbers(s): return [float(x) for x in re.findall(NUM,s)]
def transform(s):
 t=I
 for name,content in re.findall(r'(\w+)\(([^)]*)\)',s):
  a=numbers(content)
  if name=='matrix': n=tuple(a); assert len(n)==6
  elif name=='translate': n=(1,0,0,1,a[0],a[1] if len(a)>1 else 0)
  elif name=='scale': n=(a[0],0,0,a[1] if len(a)>1 else a[0],0,0)
  elif name=='rotate':
   v=math.radians(a[0]); n=(math.cos(v),math.sin(v),-math.sin(v),math.cos(v),0,0)
   if len(a)>1:n=mul(mul((1,0,0,1,a[1],a[2]),n),(1,0,0,1,-a[1],-a[2]))
  else: raise AssertionError('Unsupported native SVG transform '+name)
  t=mul(t,n)
 return t
def physical(s):
 m=re.fullmatch(r'('+NUM+')(mm|cm|in|pt|px)?',s.strip());assert m,('SVG unit',s)
 return float(m[1])*{'mm':1,'cm':10,'in':25.4,'pt':25.4/72,'px':25.4/96,None:25.4/96}[m[2]]
def linear_path(s):
 # A deliberately narrow rectangle witness parser, independent of fixture coordinates.
 if re.search(r'[ACHQSTVachqstv]',s):return []
 toks=re.findall(r'[MLZmlz]|'+NUM,s); out=[]; i=0; mode='';p=(0,0)
 while i<len(toks):
  if toks[i] in 'MLZmlz':
   mode=toks[i];i+=1
   if mode in 'Zz':
    if out:out.append(out[0])
    continue
  if i+1>=len(toks):break
  q=(float(toks[i]),float(toks[i+1]));i+=2
  if mode.islower():q=(q[0]+p[0],q[1]+p[1])
  p=q;out.append(p)
  if mode=='M':mode='L'
  if mode=='m':mode='l'
 return out

def rectangles(file):
 root=ET.parse(file).getroot();vb=numbers(root.attrib['viewBox']);sx=physical(root.attrib['width'])/vb[2];sy=physical(root.attrib['height'])/vb[3];assert abs(sx-sy)<0.005
 found=[]
 def walk(e,t):
  t=mul(t,transform(e.get('transform',''))); tag=e.tag.split('}')[-1]; pts=[]
  if tag in ('polygon','polyline'):
   ns=numbers(e.get('points',''));pts=list(zip(ns[::2],ns[1::2]));
   if tag=='polygon' and pts:pts.append(pts[0])
  elif tag=='path':pts=linear_path(e.get('d',''))
  if len(pts)>=4:
   pts=[((t[0]*x+t[2]*y+t[4])*sx,(t[1]*x+t[3]*y+t[5])*sy) for x,y in pts]
   clean=[]
   for p in pts:
    if not clean or math.dist(p,clean[-1])>0.001:clean.append(p)
   if len(clean)==5 and math.dist(clean[0],clean[-1])<0.01:
    edges=[math.dist(clean[i],clean[i+1]) for i in range(4)]
    if all(abs((clean[(i+1)%4][0]-clean[i][0])*(clean[(i+2)%4][0]-clean[(i+1)%4][0])+(clean[(i+1)%4][1]-clean[i][1])*(clean[(i+2)%4][1]-clean[(i+1)%4][1]))<0.1 for i in range(4)):
     found.append({'width_mm':edges[0],'height_mm':edges[1],'points_mm':clean})
  for child in e:walk(child,t)
 walk(root,I);return found
try:
 run('seamlyme',['--version'],'seamlyme-version')
 run('seamly2d',['--version'],'seamly2d-version')
 helptext=run('seamly2d',['--help'],'seamly2d-help')
 # Read the format number from this pinned binary's help, never assume it.
 svg=re.search(r'(?im)^.*\bsvg\b[^\n]*?=\s*(\d+)\s*$',helptext)
 assert svg, 'Could not identify SVG export format from pinned native --help'
 fmt=svg.group(1); REPORT['svg_format']=fmt
 T=(ROOT/'fixtures/anonymous.smis').read_text()
 inputs=[('A','cm','80','50','80','50',22,25),('B','mm','900','600','90','60',24.5,30),('C','inch','40','24','101.6','60.96',27.4,30.48)]
 files=[]
 # The first spike is fixture generation. The production gate will consume JS/browser outputs too.
 for row,unit,girth,length,g,l,w,h in inputs:
  dst=OUT/(row+'.smis');dst.write_text(T.replace('value="80"','value="'+g+'"').replace('value="50"','value="'+l+'"'));files.append(dst)
  run('seamlyme',['--test',dst],row+'-measurements')
 bad=OUT/'invalid-formula.smis';bad.write_text(T.replace('@girth/4+@ease','@missing_dependency/4+@ease'))
 run('seamlyme',['--test',bad],'invalid-formula',expect=1)
 for row,unit,girth,length,g,l,w,h in inputs:
  dest=OUT/row;dest.mkdir(exist_ok=True)
  run('seamly2d',['--measurefile',OUT/(row+'.smis'),'--basename',row,'--destination',dest,'--format',fmt,'--exportonlydetails',ROOT/'fixtures/rectangle.sm2d'],row+'-export')
  svgs=list(dest.glob('*.svg')); assert svgs,(row,'no native SVG output')
  candidates=[r for f in svgs for r in rectangles(f)]
  REPORT['checks'].append({'check':row+'-rectangle','expected_cm':[w,h],'candidates':candidates});save()
  assert any(abs(r['width_mm']-w*10)<0.08 and abs(r['height_mm']-h*10)<0.08 for r in candidates),(row,'native rectangle has wrong dimensions',candidates)
 REPORT['status']='passed';save();print(json.dumps(REPORT,indent=2))
except Exception as exc:
 REPORT['status']='failed';REPORT['error']=repr(exc);save();raise
