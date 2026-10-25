import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="PFD | 2 MW DFIG Digital Twin",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
.stApp { background:#071321; color:#eaf4fb; }
[data-testid="stHeader"], footer, #MainMenu { visibility:hidden; }
.block-container { max-width:100%; padding:0 !important; }
iframe { border:0 !important; }
</style>
""", unsafe_allow_html=True)

html = r"""
<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{--bg:#071321;--panel:rgba(8,27,43,.94);--line:rgba(105,169,194,.25);--cyan:#59dce5;--muted:#91adbf;--text:#edf7ff;--amber:#ffbd69;--red:#ff6577;--green:#63e0ba}
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:var(--bg);color:var(--text);font-family:Inter,"Microsoft YaHei",Arial,sans-serif}
#app{position:relative;width:100%;height:100vh;min-height:690px;overflow:hidden;background:#102b3b}
#scene{position:absolute;inset:0}
#top{position:absolute;z-index:5;left:0;right:0;top:0;height:72px;padding:12px 20px;display:flex;align-items:center;gap:13px;background:linear-gradient(180deg,rgba(3,14,25,.96),rgba(3,14,25,.55))}
.logo{height:42px;width:48px;border:1px solid #4dcbd8;border-radius:9px;display:flex;align-items:center;justify-content:center;background:#12394c;color:#66e4ec;font-weight:900;letter-spacing:1px}
.brand{font-size:14px;font-weight:850;letter-spacing:1.2px}.sub{font-size:10px;color:#8eabba;margin-top:4px;letter-spacing:.6px}
.topright{margin-left:auto;display:flex;gap:8px;align-items:center}.pill{font-size:11px;padding:8px 10px;border-radius:7px;background:#112b3e;border:1px solid var(--line);color:#cde2ed}.pill.live{color:var(--green);background:#0c302c;border-color:#1f6656}
.panel{position:absolute;z-index:4;background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:14px;box-shadow:0 12px 35px rgba(0,0,0,.2);backdrop-filter:blur(10px)}
#left{left:14px;top:86px;width:250px;max-height:calc(100% - 155px);overflow:auto}
#right{right:14px;top:86px;width:285px;max-height:calc(100% - 155px);overflow:auto}
.kicker{font-size:9px;letter-spacing:1.8px;color:var(--cyan);font-weight:850;margin-bottom:7px}.section{font-size:13px;font-weight:800;margin:0 0 12px}
.control{margin:12px 0}.control label{display:flex;justify-content:space-between;gap:8px;font-size:11px;color:#b7ccd9;margin-bottom:7px}.control output{color:var(--cyan);font-weight:800}
input[type=range]{width:100%;accent-color:#57dce5;cursor:pointer}
button{border:1px solid #3a6278;background:#15374b;color:#e4f4fb;border-radius:7px;padding:8px 9px;font-size:10px;font-weight:750;cursor:pointer}
button:hover{background:#20536a}button.active{background:#176e72;border-color:#3bbbc0}
.row{display:flex;gap:6px;flex-wrap:wrap}.divider{height:1px;background:var(--line);margin:12px 0}
.metric{display:flex;align-items:baseline;justify-content:space-between;gap:8px;padding:8px 0;border-bottom:1px solid rgba(120,173,193,.12)}.metric:last-child{border-bottom:0}
.metric span{font-size:10px;color:#a6bfce}.metric strong{font-size:17px}.metric small{font-size:9px;color:#93afbf;font-weight:500}
.status{border:1px solid rgba(255,189,105,.25);border-radius:8px;background:rgba(91,58,24,.2);padding:10px}.status strong{display:block;font-size:13px;color:var(--amber);margin-bottom:5px}.status span{font-size:10px;color:#c5d4de;line-height:1.5}
.note{font-size:9px;color:#91adbf;line-height:1.55}.badge{display:inline-block;padding:3px 6px;border-radius:4px;background:#173c50;color:#8bdfe6;font-size:9px}
#bottom{position:absolute;z-index:4;left:14px;right:14px;bottom:12px;display:flex;gap:8px;align-items:end;pointer-events:none}
#bottom>*{pointer-events:auto}.bottomcard{background:rgba(5,20,33,.88);border:1px solid var(--line);border-radius:7px;padding:8px 10px;font-size:9px;color:#bcd2df}.bottomright{margin-left:auto}
#toast{position:absolute;z-index:8;top:82px;left:50%;transform:translateX(-50%);display:none;padding:9px 12px;border:1px solid var(--line);background:#092238;color:#e8f8fc;border-radius:7px;font-size:11px}
#viewlabel{position:absolute;z-index:3;left:50%;top:84px;transform:translateX(-50%);padding:7px 10px;border:1px solid rgba(126,203,218,.24);border-radius:7px;background:rgba(5,23,37,.55);font-size:10px;color:#c4e4ed;white-space:nowrap}
#legend{display:flex;gap:8px;align-items:center}.dot{width:7px;height:7px;border-radius:50%;display:inline-block;margin-right:4px}
@media(max-width:900px){#left{left:8px;width:215px;padding:10px}#right{right:8px;width:235px;padding:10px}.metric strong{font-size:14px}.brand{font-size:12px}}
@media(max-width:620px){#app{height:100dvh;min-height:740px}#top{height:60px;padding:7px 9px}.logo{width:36px;height:36px;font-size:12px}.brand{font-size:10px}.sub{display:none}.pill{font-size:9px;padding:6px}#left{left:7px;bottom:64px;top:auto;width:48%;max-height:290px}#right{right:7px;bottom:64px;top:auto;width:47%;max-height:290px}#viewlabel{top:65px;font-size:9px}#bottom{left:7px;right:7px;bottom:6px}.bottomcard{padding:6px;font-size:8px}.bottomright{display:none}.control{margin:8px 0}.section{font-size:11px}}
</style>
</head>
<body>
<div id="app">
 <div id="scene"></div>
 <header id="top">
  <div class="logo">PFD</div>
  <div><div class="brand">2 MW DFIG · DIGITAL TWIN</div><div class="sub">双馈感应发电机组 · 状态监测与故障诊断演示</div></div>
  <div class="topright"><span class="pill live">● SIMULATION</span><span class="pill" id="clock">--:--:--</span></div>
 </header>
 <div id="viewlabel">三维机组总览 · 点击“机舱剖视”查看传动链与双馈发电机</div>

 <section id="left" class="panel">
  <div class="kicker">01 / OPERATING CONDITIONS</div><h3 class="section">运行工况控制</h3>
  <div class="control"><label>风速 <output id="windOut">11.5 m/s</output></label><input id="wind" type="range" min="3" max="25" step=".1" value="11.5"></div>
  <div class="control"><label>发电机转速 <output id="speedOut">1500 rpm</output></label><input id="speed" type="range" min="900" max="1900" step="10" value="1500"></div>
  <div class="control"><label>有功功率 <output id="powerOut">1.55 MW</output></label><input id="power" type="range" min="0" max="2" step=".01" value="1.55"></div>
  <div class="control"><label>发电机轴承温度 <output id="tempOut">68 °C</output></label><input id="temp" type="range" min="35" max="115" value="68"></div>
  <div class="control"><label>机组振动 RMS <output id="vibOut">2.1 mm/s</output></label><input id="vib" type="range" min=".2" max="12" step=".1" value="2.1"></div>
  <div class="row"><button id="pause" class="active">Ⅱ 暂停转动</button><button id="cutaway">机舱剖视</button><button id="reset">↺ 重置视角</button></div>
  <div class="divider"></div>
  <div class="kicker">05D / TWIN DIMENSIONS</div>
  <div class="row"><button class="dim active" data-dim="physical">物理实体</button><button class="dim" data-dim="virtual">虚拟模型</button><button class="dim" data-dim="data">数据</button><button class="dim" data-dim="service">服务</button><button class="dim" data-dim="connection">连接</button></div>
  <p class="note" id="dimText">物理实体：2 MW 级风轮、传动链、齿轮箱、双馈发电机与变流器的示意模型。</p>
 </section>

 <section id="right" class="panel">
  <div class="kicker">02 / CONDITION MONITORING</div><h3 class="section">关键状态量</h3>
  <div class="metric"><span>有功功率</span><strong id="powerMetric">1.55 <small>MW</small></strong></div>
  <div class="metric"><span>发电机转速</span><strong id="speedMetric">1500 <small>rpm</small></strong></div>
  <div class="metric"><span>轴承温度</span><strong id="tempMetric">68 <small>°C</small></strong></div>
  <div class="metric"><span>振动 RMS</span><strong id="vibMetric">2.1 <small>mm/s</small></strong></div>
  <div class="metric"><span>转子侧电流（模拟）</span><strong id="currentMetric">126 <small>A</small></strong></div>
  <div class="divider"></div>
  <div class="kicker">03 / FAULT DIAGNOSIS</div><h3 class="section">初始故障诊断</h3>
  <div class="status"><strong id="diagTitle">运行正常 · 继续监测</strong><span id="diagText">当前模拟参数未触发演示阈值。诊断结果仅用于展示规则逻辑。</span></div>
  <div class="divider"></div>
  <div class="kicker">04 / MAINTENANCE SERVICE</div><h3 class="section">维护建议</h3>
  <div class="note" id="advice">持续监测轴承温度、振动和发电机运行参数；结合历史趋势与检修记录进一步判断。</div>
  <div class="divider"></div>
  <div class="row"><button id="faultBearing">模拟轴承故障</button><button id="faultVibration">模拟振动异常</button><button id="clearFault">清除异常</button></div>
  <p class="note" style="margin-top:9px">所有数值均为模拟数据，不连接真实风机，不用于实际保护、停机或安全决策。</p>
 </section>
 <div id="toast"></div>
 <div id="bottom">
  <div class="bottomcard"><b>机组结构</b>　风轮 → 主轴/齿轮箱 → DFIG → 变流器</div>
  <div class="bottomcard" id="legend"><span><i class="dot" style="background:#62dfbd"></i>正常</span><span><i class="dot" style="background:#ffbd69"></i>关注</span><span><i class="dot" style="background:#ff6577"></i>异常</span></div>
  <div class="bottomcard bottomright">演示原型 · 5D 维度为本项目的工程组织方式</div>
 </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script>
(function(){
const host=document.getElementById('scene');
if(!window.THREE){host.innerHTML='<div style="color:white;padding:30px">Three.js 加载失败，请检查网络/CDN。</div>';return;}
const T=THREE, scene=new T.Scene();scene.background=new T.Color(0x7896a5);scene.fog=new T.Fog(0x7896a5,28,85);
const camera=new T.PerspectiveCamera(42,1,.1,200);camera.position.set(12,9,15);
const renderer=new T.WebGLRenderer({antialias:true,alpha:false});renderer.setPixelRatio(Math.min(devicePixelRatio||1,2));renderer.setSize(host.clientWidth,host.clientHeight);renderer.outputEncoding=T.sRGBEncoding;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=.88;renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.PCFSoftShadowMap;host.appendChild(renderer.domElement);
const controls=new T.OrbitControls(camera,renderer.domElement);controls.target.set(0,4,0);controls.enableDamping=true;controls.maxPolarAngle=Math.PI*.49;controls.minDistance=5;controls.maxDistance=36;
scene.add(new T.HemisphereLight(0xd9edf5,0x243f50,.95));const sun=new T.DirectionalLight(0xfff0d9,1.35);sun.position.set(-9,16,10);sun.castShadow=true;scene.add(sun);const fill=new T.DirectionalLight(0x5bc9df,.35);fill.position.set(9,7,-8);scene.add(fill);
const seaGeo=new T.PlaneGeometry(180,180,90,90);seaGeo.rotateX(-Math.PI/2);const sea=new T.Mesh(seaGeo,new T.MeshPhongMaterial({color:0x176b87,shininess:28,specular:0x376f80,side:T.DoubleSide}));sea.position.y=-.25;sea.receiveShadow=true;scene.add(sea);const seaBase=seaGeo.attributes.position.array.slice();
const grid=new T.GridHelper(70,56,0x65bdcc,0x468da1);grid.position.y=-.20;grid.material.transparent=true;grid.material.opacity=.14;scene.add(grid);
function island(x,z,sx,sz){const o=new T.Mesh(new T.SphereGeometry(1,22,12),new T.MeshStandardMaterial({color:0x486e70,roughness:1}));o.position.set(x,.2,z);o.scale.set(sx,.45,sz);scene.add(o)}
island(-18,-27,8,3);island(17,-32,11,3.5);island(28,-24,6,2.4);

// Main tower and offshore foundation
const towerMat=new T.MeshStandardMaterial({color:0xcbd7df,roughness:.48,metalness:.12});
const steel=new T.MeshStandardMaterial({color:0x688797,roughness:.38,metalness:.55});
const darkSteel=new T.MeshStandardMaterial({color:0x264d60,roughness:.42,metalness:.4});
const yellow=new T.MeshStandardMaterial({color:0xe8c35e,roughness:.4,metalness:.15});
const tower=new T.Mesh(new T.CylinderGeometry(.22,.42,6.2,32,10),towerMat);tower.position.y=2.85;tower.castShadow=true;scene.add(tower);
for(let i=0;i<3;i++){const a=i*Math.PI*2/3+.2,x=Math.cos(a)*.75,z=Math.sin(a)*.75;const leg=new T.Mesh(new T.CylinderGeometry(.15,.19,1.45,20),darkSteel);leg.position.set(x,-.28,z);leg.castShadow=true;scene.add(leg);const cap=new T.Mesh(new T.CylinderGeometry(.18,.18,.12,20),yellow);cap.position.set(x,.5,z);scene.add(cap)}

// Nacelle, gearbox, DFIG components built as a detailed exploded/cutaway group
const nacelleGroup=new T.Group();nacelleGroup.position.set(0,6.25,0);scene.add(nacelleGroup);
const nacelleBody=new T.Mesh(new T.BoxGeometry(2.5,.95,1.12),new T.MeshStandardMaterial({color:0xb9cbd5,roughness:.5,metalness:.1,transparent:true,opacity:.88}));nacelleBody.position.set(0,.15,-.45);nacelleBody.castShadow=true;nacelleGroup.add(nacelleBody);
const nacelleRoof=new T.Mesh(new T.BoxGeometry(2.55,.09,1.16),new T.MeshStandardMaterial({color:0xe2ebef,roughness:.42,metalness:.1}));nacelleRoof.position.set(0,.66,-.45);nacelleGroup.add(nacelleRoof);
// Main low-speed shaft
const shaft=new T.Mesh(new T.CylinderGeometry(.14,.14,1.85,24),steel);shaft.rotation.x=Math.PI/2;shaft.position.set(0,.05,.55);nacelleGroup.add(shaft);
// Gearbox block with multiple stage cylinders/gears
const gearbox=new T.Group();gearbox.position.set(0,.05,-.05);nacelleGroup.add(gearbox);
const gbBody=new T.Mesh(new T.BoxGeometry(.78,.62,.72),new T.MeshStandardMaterial({color:0x6d8796,roughness:.48,metalness:.35}));gearbox.add(gbBody);
for(let i=0;i<3;i++){const gear=new T.Mesh(new T.CylinderGeometry(.19-i*.025,.19-i*.025,.12,24),new T.MeshStandardMaterial({color:i===1?0xb4c6ce:0x8fa7b4,metalness:.65,roughness:.3}));gear.rotation.x=Math.PI/2;gear.position.set(-.22+i*.22,.02,.4);gearbox.add(gear);}
// DFIG generator body, end caps, stator ribs and rotor axis
const generator=new T.Group();generator.position.set(0,.05,-.72);nacelleGroup.add(generator);
const genBody=new T.Mesh(new T.CylinderGeometry(.34,.34,.95,36,1,true),new T.MeshStandardMaterial({color:0x357f91,metalness:.48,roughness:.34,side:T.DoubleSide}));genBody.rotation.x=Math.PI/2;generator.add(genBody);
for(let z of [-.5,.5]){const cap=new T.Mesh(new T.CylinderGeometry(.36,.36,.08,32),new T.MeshStandardMaterial({color:0x9db2bd,metalness:.55,roughness:.28}));cap.rotation.x=Math.PI/2;cap.position.z=z;generator.add(cap);}
for(let i=0;i<20;i++){const a=i*Math.PI*2/20;const rib=new T.Mesh(new T.BoxGeometry(.035,.58,.78),new T.MeshStandardMaterial({color:i%2?0x6eb8c4:0x8ba6b2,metalness:.4,roughness:.38}));rib.position.set(Math.cos(a)*.33,Math.sin(a)*.33,0);rib.rotation.z=a;generator.add(rib);}
const rotorCore=new T.Mesh(new T.CylinderGeometry(.12,.12,1.3,24),new T.MeshStandardMaterial({color:0xd1a85c,metalness:.7,roughness:.25}));rotorCore.rotation.x=Math.PI/2;generator.add(rotorCore);
// Converter cabinet and cable links
const converter=new T.Mesh(new T.BoxGeometry(.45,.58,.36),new T.MeshStandardMaterial({color:0x244e63,roughness:.5,metalness:.25}));converter.position.set(.72,-.08,-.65);nacelleGroup.add(converter);
for(let i=0;i<5;i++){const vent=new T.Mesh(new T.BoxGeometry(.24,.025,.018),new T.MeshStandardMaterial({color:0x72b9c8,metalness:.25}));vent.position.set(.72,.08-i*.075,-.46);nacelleGroup.add(vent);}
const bearingGroup=new T.Group();bearingGroup.position.set(0,.05,.35);nacelleGroup.add(bearingGroup);
for(let z of [-.18,.18]){const ring=new T.Mesh(new T.TorusGeometry(.2,.045,12,28),new T.MeshStandardMaterial({color:0xe0b75c,metalness:.7,roughness:.25}));ring.rotation.x=Math.PI/2;ring.position.z=z;bearingGroup.add(ring);}
const hub=new T.Group();hub.position.set(0,6.25,.95);scene.add(hub);const hubMat=new T.MeshStandardMaterial({color:0xdce7ec,roughness:.35,metalness:.08});const hubBall=new T.Mesh(new T.SphereGeometry(.3,28,20),hubMat);hub.add(hubBall);
const hubNose=new T.Mesh(new T.SphereGeometry(.18,24,16),new T.MeshStandardMaterial({color:0xbacbd4,roughness:.35}));hubNose.position.z=.2;hub.add(hubNose);

// Aerodynamic 3D blades: tapered, thickness-bearing meshes with light coating and damage stripe.
const rotor=new T.Group();rotor.position.copy(hub.position);scene.add(rotor);
const bladeMeshes=[];let damageLevel=22,heatmapOn=true,cutawayOn=false,rotating=true;
function profile(t){return {chord:.52*Math.pow(1-t,.72)+.055,sweep:-.14*t*t,thick:.095*Math.pow(1-t,.72)+.012};}
function makeBlade(idx){
 const group=new T.Group(),N=42,M=10,verts=[],cols=[],ids=[],rows=M+1;
 const good=new T.Color(0xcbd7df),coat=new T.Color(0x57cfc5),amber=new T.Color(0xffbd69),red=new T.Color(0xff4d65);
 for(let side=0;side<2;side++){
  const offset=verts.length/3;
  for(let i=0;i<=N;i++){const t=i/N,p=profile(t);for(let j=0;j<=M;j++){const u=j/M*2-1;verts.push(p.sweep+u*p.chord*.5,t*3.9,(side===0?1:-1)*p.thick*Math.sqrt(Math.max(0,1-u*u)));let c=good.clone();if(Math.abs(u+.7)<.22)c.lerp(coat,.75);if(heatmapOn&&t>1-damageLevel/120&&u<-.35){const q=(t-(1-damageLevel/120))/Math.max(.01,damageLevel/120);c.lerp(amber,Math.min(.9,q*1.4));if(q>.48)c.lerp(red,Math.min(.95,(q-.48)*2.1));}cols.push(c.r,c.g,c.b);}}
  for(let i=0;i<N;i++)for(let j=0;j<M;j++){const a=offset+i*rows+j,b=a+rows;if(side===0)ids.push(a,b,a+1,b,b+1,a+1);else ids.push(a,a+1,b,b,b===undefined?b:a+1,b+1);}
 }
 const geo=new T.BufferGeometry();geo.setAttribute('position',new T.Float32BufferAttribute(verts,3));geo.setAttribute('color',new T.Float32BufferAttribute(cols,3));geo.setIndex(ids);geo.computeVertexNormals();
 const mesh=new T.Mesh(geo,new T.MeshStandardMaterial({vertexColors:true,side:T.DoubleSide,roughness:.42,metalness:.04}));mesh.castShadow=true;group.add(mesh);
 const rootCollar=new T.Mesh(new T.CylinderGeometry(.22,.27,.3,24),new T.MeshStandardMaterial({color:0xd5e0e6,roughness:.38}));rootCollar.rotation.x=Math.PI/2;rootCollar.position.y=.2;group.add(rootCollar);
 group.rotation.z=idx*2*Math.PI/3;rotor.add(group);bladeMeshes.push(mesh);
}
for(let i=0;i<3;i++)makeBlade(i);

function refreshHeatmap(){
 bladeMeshes.forEach(mesh=>{
  const pos=mesh.geometry.attributes.position,col=mesh.geometry.attributes.color;
  for(let i=0;i<pos.count;i++){
   const y=pos.getY(i),t=Math.max(0,Math.min(1,y/3.9)),x=pos.getX(i),p=profile(t),u=(x-p.sweep)/(p.chord*.5);
   let c=new T.Color(0xcbd7df);if(Math.abs(u+.7)<.22)c.lerp(new T.Color(0x57cfc5),.75);
   if(heatmapOn&&t>1-damageLevel/120&&u<-.35){const q=(t-(1-damageLevel/120))/Math.max(.01,damageLevel/120);c.lerp(new T.Color(0xffbd69),Math.min(.9,q*1.4));if(q>.48)c.lerp(new T.Color(0xff4d65),Math.min(.95,(q-.48)*2.1));}
   col.setXYZ(i,c.r,c.g,c.b);
  }col.needsUpdate=true;
 });
}

// Background turbines use the same blade mesh generator with reduced scale and identical blade material detail.
const distantRotors=[];
function addDistantTurbine(x,z,s){
 const group=new T.Group();group.position.set(x,0,z);group.scale.setScalar(s);scene.add(group);
 const t=new T.Mesh(new T.CylinderGeometry(.045,.085,3.3,16),towerMat);t.position.y=1.55;group.add(t);
 const nac=new T.Mesh(new T.BoxGeometry(.42,.2,.34),nacelleRoof.material);nac.position.set(0,3.22,-.08);group.add(nac);
 const h=new T.Group();h.position.set(0,3.2,.15);group.add(h);
 const miniRotor=new T.Group();miniRotor.position.copy(h.position);group.add(miniRotor);
 for(let i=0;i<3;i++){
  const m=bladeMeshes[i].clone();m.geometry=bladeMeshes[i].geometry;m.material=bladeMeshes[i].material;const g=new T.Group();g.add(m);g.scale.setScalar(.82);g.rotation.z=i*2*Math.PI/3;miniRotor.add(g);
 }
 distantRotors.push(miniRotor);
}
addDistantTurbine(-10,-14,.72);addDistantTurbine(-16,-20,.52);addDistantTurbine(13,-18,.63);addDistantTurbine(21,-25,.48);

// Interaction / diagnosis logic
const $=id=>document.getElementById(id);let wind=11.5,speed=1500,power=1.55,temp=68,vib=2.1;
function toast(msg){const el=$('toast');el.textContent=msg;el.style.display='block';clearTimeout(toast.timer);toast.timer=setTimeout(()=>el.style.display='none',2300);}
function diagnose(){
 let title='运行正常 · 继续监测',txt='当前模拟参数未触发演示阈值。诊断结果仅用于展示规则逻辑。',advice='持续监测轴承温度、振动和发电机运行参数；结合历史趋势与检修记录进一步判断。',color='var(--green)';
 if(temp>=90&&vib>=7){title='高风险：温升与振动同时异常';txt='温度与振动同时超过演示阈值，可能存在轴承润滑、磨损或对中问题。';advice='优先核查轴承温度传感器、润滑状态、振动频谱和检修记录；实际处置应依据制造商规程。';color='var(--red)';}
 else if(temp>=90){title='关注：发电机轴承温度偏高';txt='温度超过本演示阈值 90 °C。可能原因需结合负载、润滑与传感器状态复核。';advice='检查负载变化、润滑状态、温度传感器和轴承历史趋势。';color='var(--red)';}
 else if(vib>=7){title='关注：机组振动异常';txt='振动 RMS 超过本演示阈值 7 mm/s。需要进一步分析频谱和转速关联。';advice='检查不平衡、对中、轴承、齿轮啮合及安装松动等可能原因。';color='var(--red)';}
 else if(temp>=78||vib>=4.5){title='预警：参数出现上升趋势';txt='至少一个参数进入关注区间，建议观察连续趋势，避免只依据单点值判断。';advice='查看过去一段时间的温度与振动趋势，并与功率、转速及工况对照。';color='var(--amber)';}
 $('diagTitle').textContent=title;$('diagTitle').style.color=color;$('diagText').textContent=txt;$('advice').textContent=advice;
}
function update(){
 $('windOut').textContent=wind.toFixed(1)+' m/s';$('speedOut').textContent=speed+' rpm';$('powerOut').textContent=power.toFixed(2)+' MW';$('tempOut').textContent=temp+' °C';$('vibOut').textContent=vib.toFixed(1)+' mm/s';
 $('powerMetric').innerHTML=power.toFixed(2)+' <small>MW</small>';$('speedMetric').innerHTML=speed+' <small>rpm</small>';$('tempMetric').innerHTML=temp+' <small>°C</small>';$('vibMetric').innerHTML=vib.toFixed(1)+' <small>mm/s</small>';
 $('currentMetric').innerHTML=Math.round(45+power*52+vib*2)+' <small>A</small>';
 diagnose();
}
$('wind').addEventListener('input',e=>{wind=+e.target.value;update()});
$('speed').addEventListener('input',e=>{speed=+e.target.value;update()});
$('power').addEventListener('input',e=>{power=+e.target.value;update()});
$('temp').addEventListener('input',e=>{temp=+e.target.value;update()});
$('vib').addEventListener('input',e=>{vib=+e.target.value;update()});
$('pause').addEventListener('click',()=>{rotating=!rotating;$('pause').textContent=rotating?'Ⅱ 暂停转动':'▶ 启动转动';$('pause').classList.toggle('active',rotating)});
$('cutaway').addEventListener('click',()=>{cutawayOn=!cutawayOn;nacelleBody.material.opacity=cutawayOn?.22:.88;nacelleRoof.visible=!cutawayOn;gearbox.visible=true;generator.visible=true;converter.visible=true;$('cutaway').classList.toggle('active',cutawayOn);$('viewlabel').textContent=cutawayOn?'机舱剖视 · 主轴 / 齿轮箱 / 双馈发电机 / 变流器':'三维机组总览 · 点击“机舱剖视”查看传动链与双馈发电机';controls.target.set(0,4.4,0);});
$('reset').addEventListener('click',()=>{camera.position.set(12,9,15);controls.target.set(0,4,0);controls.update();toast('视角已重置')});
$('faultBearing').addEventListener('click',()=>{temp=96;vib=8.1;$('temp').value=temp;$('vib').value=vib;update();toast('已注入模拟轴承异常')});
$('faultVibration').addEventListener('click',()=>{vib=8.5;$('vib').value=vib;update();toast('已注入模拟振动异常')});
$('clearFault').addEventListener('click',()=>{temp=68;vib=2.1;$('temp').value=temp;$('vib').value=vib;update();toast('模拟异常已清除')});
const dims={
 physical:'物理实体：2 MW 级风轮、主轴、齿轮箱、双馈感应发电机、变流器和支撑结构的示意模型。',
 virtual:'虚拟模型：以三维结构、部件状态和简化运动逻辑映射机组，不等同于经校准的多物理场模型。',
 data:'数据：风速、功率、转速、轴承温度、振动与转子侧电流均为模拟数据，可后续替换为传感器/SCADA数据。',
 service:'服务：规则阈值预警、故障提示、维护建议与分区状态展示；当前为初始规则算法，不是已验证诊断模型。',
 connection:'连接：当前为浏览器本地演示；后续可通过 API/MQTT/数据库接入真实 SCADA 或状态监测系统。'
};
document.querySelectorAll('.dim').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('.dim').forEach(x=>x.classList.remove('active'));b.classList.add('active');$('dimText').textContent=dims[b.dataset.dim]}));
$('clock').textContent=new Date().toLocaleTimeString('zh-CN',{hour12:false});setInterval(()=>$('clock').textContent=new Date().toLocaleTimeString('zh-CN',{hour12:false}),1000);
const base=seaGeo.attributes.position.array.slice();let last=performance.now(),elapsed=0;
function resize(){const w=host.clientWidth,h=host.clientHeight;camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h)}
window.addEventListener('resize',resize);
function animate(now){requestAnimationFrame(animate);const dt=Math.min(.05,(now-last)/1000);last=now;elapsed+=dt;if(rotating){rotor.rotation.z+=speed/1500*.35*dt;distantRotors.forEach((r,i)=>r.rotation.z+=speed/1500*(.35-i*.025)*dt);generator.rotation.z+=speed/1500*.18*dt;}
 const p=seaGeo.attributes.position;for(let i=0;i<p.count;i++){const x=base[i*3],z=base[i*3+2];p.setY(i,base[i*3+1]+.035*Math.sin(x*.42+elapsed)*Math.cos(z*.37+elapsed*.7));}p.needsUpdate=true;seaGeo.computeVertexNormals();controls.update();renderer.render(scene,camera);}
update();requestAnimationFrame(animate);
})();
</script>
</body>
</html>
"""
components.html(html, height=940, scrolling=False)
