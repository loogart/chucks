from pathlib import Path
import xml.etree.ElementTree as E
import math,re
N='http://www.w3.org/2000/svg';E.register_namespace('',N)
def el(tag,attrs={},parent=None):
 x=E.Element('{'+N+'}'+tag,{k:str(v) for k,v in attrs.items()})
 if parent is not None:parent.append(x)
 return x
BASE=Path(__file__).resolve().parent.parent
src=E.parse(BASE/'assets/chef-original.svg').getroot();parts=list(src.find('.//{'+N+'}g[@id="final"]/{'+N+'}g'))
r=el('svg',{'viewBox':'-25 -90 180 325','role':'img','aria-labelledby':'chef-title chef-desc'})
el('title',{'id':'chef-title'},r).text='Chuck, le chef qui a du swing'
el('desc',{'id':'chef-desc'},r).text='Deux pas, une petite préparation, un burger lancé en arc, puis rattrapé. Une boucle de 6,4 secondes.'
el('style',{},r).text='.motion{display:inline}.still{display:none}@media(prefers-reduced-motion:reduce){.motion{display:none}.still{display:inline}}'
# Explicit fills preserve the original palette; no overwritten class can turn gray limbs black.
colors={'cls-1':'#231f20','cls-2':'#fff','cls-3':'#939598','cls-4':'#ef4136','cls-5':'#a7a9ac'}
for p in parts:
 for c in p.iter():
  if c.get('class') in colors:c.set('fill',colors[c.get('class')]);c.attrib.pop('class',None)
import copy
# The open palm fits the logo’s flat grey geometry and supports the burger.
parts[18].set('points','103.97 69.56 103.97 61 86.87 61 84.05 64.02 103.97 69.56')
def add_hand(parent):
 hand=el('g',{'id':'serving-hand-still' if parent.get('class')=='still' else 'serving-hand'},parent)
 el('path',{'fill':'#a7a9ac','d':'M85 55L82 51Q80 49 78.5 51Q77 52.5 79 55L84 60Q85 61 88 62L88 65H104V61Q109 60 112 56Q114 53 111 52L87 53Z'},hand)
 el('path',{'fill':'none','stroke':'#939598','stroke-width':'1.1','stroke-linecap':'round','d':'M98 57.5H109M98 60.5H105'},hand)
 return hand
still=el('g',{'class':'still'},r)
for p in parts[:-1]:still.append(copy.deepcopy(p))
add_hand(still)
still.append(copy.deepcopy(parts[-1]))
motion=el('g',{'class':'motion'},r)
body=el('g',{'id':'chuck-body'},motion)
legs=[]
for name,d in [('left','M24.49 170h35.63v53.43H3.96c0-4.82 9.19-8.73 20.53-8.73Z'),('right','M73.88 170h35.63v44.82c9.71.7 17.13 4.28 17.13 8.61H73.88Z')]:
 g=el('g',{'id':'leg-'+name},body);el('path',{'fill':'#231f20','d':d},g);legs.append(g)
upper=el('g',{'id':'torso'},body)
# Torso and raised arm are now independent articulated shapes.
el('path',{'fill':'#231f20','d':'M126.64 160.78C126.64 137.79 118.13 116.8 104.1 100.76L80.59 81.51C67.27 73.91 51.86 69.56 35.43 69.56H17.79V160.78Z'},upper)
arm=el('g',{'id':'throw-arm'},upper)
el('path',{'fill':'#231f20','d':'M80.59 81.51L84.05 64.02L103.97 69.56L104.1 100.76L91 108Z'},arm)
arm.append(copy.deepcopy(parts[18]))
add_hand(arm)
head=el('g',{'id':'head'},upper)
for i in [2,3,4,5]:head.append(copy.deepcopy(parts[i]))
brows=[]
for i in [6,7]:
 b=el('g',{'id':'eyebrow-'+str(i)},head);b.append(copy.deepcopy(parts[i]));brows.append(b)
hat=el('g',{'id':'hat'},head);hat.append(copy.deepcopy(parts[9]))
for i in [8,11,12,13,14]:upper.append(copy.deepcopy(parts[i]))
free=el('g',{'id':'free-arm'},upper);free.append(copy.deepcopy(parts[15]))
burger=el('g',{'id':'burger'},upper);burger.append(copy.deepcopy(parts[-1]))
# A single sampled timeline synchronizes every joint and the ballistic flight.
D=6.4;count=385;times=[i*D/(count-1) for i in range(count)]
def smooth(x):return x*x*(3-2*x)
def interp(t,keys):
 for (a,x),(b,y) in zip(keys,keys[1:]):
  if a<=t<=b:return x+(y-x)*smooth((t-a)/(b-a))
 return keys[0][1] if t<keys[0][0] else keys[-1][1]
def stride(t):
 for a,b in [(0,1.6),(4.8,6.4)]:
  if a<=t<=b:
   u=(t-a)/(b-a); return math.sin(u*4*math.pi)*math.sin(u*math.pi)**.5
 return 0
armkeys=[(0,0),(1.9,0),(2.26,13),(2.52,-14),(2.75,-6),(3.42,0),(3.7,0),(3.82,8),(4.05,-3),(4.3,0),(6.4,0)]
army=[(0,0),(1.9,0),(2.26,5),(2.52,-9),(2.8,-1),(3.42,0),(3.7,0),(3.82,4),(4.08,-1),(4.3,0),(6.4,0)]
bodyy=[(0,0),(1.9,0),(2.26,2),(2.52,-3),(2.85,0),(3.7,0),(3.82,3),(4.05,-1),(4.3,0),(6.4,0)]
def armpos(t):
 a=math.radians(interp(t,armkeys));dy=interp(t,army);x,y=95.49,33.43;px,py=89,99
 return (px+math.cos(a)*(x-px)-math.sin(a)*(y-py)-x,py+math.sin(a)*(x-px)+math.cos(a)*(y-py)-y+dy)
launch=armpos(2.52);land=armpos(3.7)
def flight(t):
 if 2.52<t<3.7:
  u=(t-2.52)/1.18
  return (launch[0]+(land[0]-launch[0])*u, launch[1]+(land[1]-launch[1])*u-4*76*u*(1-u),-14+374*u)
 x,y=armpos(t);return(x,y,interp(t,armkeys)+(360 if t>=3.7 else 0))
def animate(node,fn):
 vals=[fn(t) for t in times]
 parsed=[re.findall(r'(translate|rotate)\(([^)]+)\)',v) for v in vals]
 for i,(kind,_) in enumerate(parsed[0]):
  if i:
   inner=el('g')
   for c in list(node):
    if not c.tag.endswith('animateTransform'):node.remove(c);inner.append(c)
   node.append(inner);node=inner
  el('animateTransform',{'attributeName':'transform','type':kind,'dur':'6.4s','repeatCount':'indefinite','calcMode':'linear','keyTimes':';'.join(f'{j/(count-1):.6f}' for j in range(count)),'values':';'.join(v[i][1] for v in parsed)},node)
fmt=lambda x:f'{x:.3f}'
animate(body,lambda t:'translate('+fmt(1.2*stride(t))+' '+fmt(interp(t,bodyy)-1.8*abs(stride(t)))+')')
animate(legs[0],lambda t:f'translate(0 {fmt(-2*max(0,stride(t)))}) rotate({fmt(8*stride(t))} 43 183)')
animate(legs[1],lambda t:f'translate(0 {fmt(-2*max(0,-stride(t)))}) rotate({fmt(-8*stride(t))} 92 183)')
animate(upper,lambda t:f'rotate({fmt(-1.2*stride(t))} 65 184)')
animate(free,lambda t:f'rotate({fmt(-7*stride(t)+interp(t,[(0,0),(2.2,0),(2.6,3),(3.7,0),(3.82,-2),(4.3,0),(6.4,0)]))} 27 138)')
animate(arm,lambda t:f'translate(0 {fmt(interp(t,army))}) rotate({fmt(interp(t,armkeys))} 89 99)')
animate(burger,lambda t:f'translate({fmt(flight(t)[0])} {fmt(flight(t)[1])}) rotate({fmt(flight(t)[2])} 95.49 33.43)')
animate(head,lambda t:f'rotate({fmt(interp(t,[(0,0),(2.2,0),(2.78,3),(3.1,4),(3.7,0),(4, -1),(4.35,0),(6.4,0)]))} 34 87)')
animate(hat,lambda t:f'rotate({fmt(interp(t,[(0,0),(2.26,1),(2.58,-2),(2.88,1),(3.1,0),(3.87,2),(4.12,-1),(4.4,0),(6.4,0)]))} 34 39)')
for i,b in enumerate(brows):
 animate(b,lambda t,i=i:f'translate(0 {fmt(interp(t,[(0,0),(2.25,1),(2.7,-3-i),(3.15,-4-i),(3.7,0),(4.38,0),(4.47,2),(4.58,0),(6.4,0)]))})')
E.ElementTree(r).write(BASE/'assets/chef-animated.svg',encoding='unicode',xml_declaration=True)
# Manual pause and reduced-motion fallback includes the same hand.
static=copy.deepcopy(r)
for child in list(static):
 if child.get('class')=='motion' or child.tag=='{'+N+'}style':static.remove(child)
static.find('{'+N+'}title').text='Chuck tient son burger dans la main'
static.find('{'+N+'}desc').text='Le chef Chuck présente son burger sur la paume de sa main ouverte.'
static.find('{'+N+'}g').attrib.pop('class',None)
static.find('.//{'+N+'}g[@id="serving-hand-still"]').set('id','serving-hand')
E.ElementTree(static).write(BASE/'assets/chef-still.svg',encoding='unicode',xml_declaration=True)
print('Synchronized SVG rig: 385 poses, 6.4 seconds, 12 articulated channels. Original fills preserved.')

# Footer variant: only the two burger buns change to white on the red section.
for name in ['animated', 'still']:
 variant=copy.deepcopy(r if name=='animated' else static)
 for group in variant.findall('.//{'+N+'}g[@id="burger"]'):
  for node in group.iter():
   if node.get('fill')=='#ef4136':node.set('fill','#fff')
 # The static group and reduced-motion layer contain the original burger paths.
 for group in variant.findall('.//{'+N+'}g'):
  if len(group)==4 and sum(x.get('fill')=='#ef4136' for x in group)==2:
   for node in group:
    if node.get('fill')=='#ef4136':node.set('fill','#fff')
 variant.set('viewBox','-25 -90 180 313.43')
 E.ElementTree(variant).write(BASE/('assets/chef-'+name+'-footer.svg'),encoding='unicode',xml_declaration=True)
