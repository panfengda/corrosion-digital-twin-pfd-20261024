import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="PFD | Offshore Wind Digital Twin",
    page_icon="🌊",
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
<title>PFD Offshore Wind Digital Twin</title>
<style>
:root{
 --bg:#071321;--panel:rgba(9,29,46,.91);--line:rgba(119,180,202,.23);
 --cyan:#5de0e7;--muted:#91adbf;--text:#edf7ff;--orange:#ffb86b;--red:#ff5e70;
}
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:var(--bg);
 color:var(--text);font-family:Inter,"Microsoft YaHei",Arial,sans-serif}
#app{position:relative;width:100%;height:100vh;min-height:650px;overflow:hidden;background:#8fbac5}
#scene{position:absolute;inset:0}
#topbar{position:absolute;top:0;left:0;right:0;height:76px;padding:15px 22px;
 display:flex;align-items:center;gap:15px;background:linear-gradient(180deg,rgba(4,17,29,.94),rgba(4,17,29,.18));z-index:4}
.logo{height:40px;width:46px;border:1px solid #58dbe4;border-radius:9px;background:#12364a;
 display:flex;align-items:center;justify-content:center;color:#72edf0;font-weight:900;letter-spacing:1px}
.brand{font-weight:800;letter-spacing:1.4px;font-size:14px}
.subbrand{color:#8faabb;font-size:10px;letter-spacing:1.4px;margin-top:4px}
.topright{margin-left:auto;display:flex;gap:8px;align-items:center}
.pill{border:1px solid var(--line);border-radius:7px;padding:8px 11px;background:rgba(10,33,50,.75);
 color:#d5eaf3;font-size:12px}
.pill.live{color:#75edc4;border-color:#286a58;background:rgba(9,59,47,.8)}
.panel{position:absolute;z-index:3;background:var(--panel);border:1px solid var(--line);
 box-shadow:0 12px 35px rgba(0,0,0,.15);backdrop-filter:blur(9px);border-radius:12px}
#left{left:18px;top:94px;width:235px;padding:15px 15px 14px}
#right{right:18px;top:94px;width:275px;padding:15px}
.section{font-size:13px;font-weight:800;letter-spacing:.4px;margin:0 0 12px}
.kicker{font-size:9px;letter-spacing:1.8px;color:var(--cyan);font-weight:800;margin-bottom:7px}
.control{margin:14px 0}
.control label{display:flex;justify-content:space-between;gap:8px;font-size:11px;color:#bdd2df;margin-bottom:8px}
.control output{color:var(--cyan);font-weight:800}
input[type=range]{width:100%;accent-color:#ff6672;cursor:pointer}
button{cursor:pointer;border:1px solid #426a7d;background:#17384d;color:#e5f5fc;border-radius:7px;
 padding:8px 10px;font-size:11px;font-weight:700}
button:hover{background:#20536a}
button.primary{background:#218e8b;border-color:#43c4bd}
.btnrow{display:flex;gap:7px;flex-wrap:wrap}
.note{font-size:10px;color:#91aebe;line-height:1.55}
.divider{height:1px;background:var(--line);margin:13px 0}
.metric{display:flex;justify-content:space-between;align-items:baseline;padding:9px 0;border-bottom:1px solid rgba(119,180,202,.12)}
.metric:last-child{border:0}
.metric span{font-size:11px;color:#a8c0cf}
.metric strong{font-size:18px;color:#eaf8ff}
.metric small{font-size:10px;color:#94b4c6;font-weight:500}
.status{padding:10px 11px;border:1px solid rgba(255,184,107,.25);border-radius:8px;background:rgba(92,54,24,.23)}
.status strong{display:block;color:var(--orange);font-size:14px;margin-bottom:4px}
.status span{font-size:10px;color:#c3d1d9;line-height:1.5}
#bottom{position:absolute;left:18px;right:18px;bottom:15px;z-index:3;display:flex;align-items:end;gap:12px;pointer-events:none}
#bottom .legend,#bottom .hint{pointer-events:auto;background:rgba(7,24,39,.78);border:1px solid var(--line);
 border-radius:8px;padding:9px 12px;font-size:10px;color:#c2d8e4}
.gradient{height:7px;width:170px;border-radius:5px;margin:7px 0 4px;
 background:linear-gradient(90deg,#2dc8bd,#dce7a4,#ffbd69,#ff596b)}
#bottom .hint{margin-left:auto}
#toast{position:absolute;top:85px;left:50%;transform:translateX(-50%);z-index:5;
 background:rgba(8,30,46,.9);border:1px solid var(--line);padding:8px 12px;border-radius:7px;
 color:#dff6fa;font-size:11px;display:none}
#hotspot{position:absolute;left:50%;bottom:94px;transform:translateX(-50%);z-index:2;
 color:#d9f1f7;font-size:11px;text-shadow:0 1px 5px #082031;pointer-events:none}
@media(max-width:900px){
 #app{min-height:720px}
 #left{left:10px;top:82px;width:185px;padding:11px}
 #right{right:10px;top:82px;width:205px;padding:11px}
 #topbar{padding:10px 12px;height:65px}
 .brand{font-size:12px}.subbrand{font-size:8px}
 .metric strong{font-size:15px}
}
@media(max-width:620px){
 #app{height:100dvh;min-height:700px}
 #left{top:auto;bottom:70px;left:8px;width:48%;max-height:245px;overflow:auto}
 #right{top:auto;bottom:70px;right:8px;width:46%;max-height:245px;overflow:auto}
 #topbar{height:62px;padding:8px}
 .logo{width:37px;height:36px;font-size:12px}
 .brand{font-size:11px}.subbrand{display:none}
 .pill{font-size:9px;padding:6px}
 #bottom{left:8px;right:8px;bottom:8px}
 #bottom .legend{padding:7px;font-size:9px}
 #bottom .hint{display:none}
 .gradient{width:110px}
 .control{margin:9px 0}
 .control label{font-size:10px}
 .section{font-size:11px}
}
</style>
</head>
<body>
<div id="app">
 <div id="scene"></div>
 <header id="topbar">
  <div class="logo">PFD</div>
  <div><div class="brand">OFFSHORE WIND · DIGITAL TWIN</div>
   <div class="subbrand">海上风电叶片涂层监测与损伤演化</div></div>
  <div class="topright"><span class="pill live">● 演示运行中</span><span class="pill" id="clock">DEMO</span></div>
 </header>

 <section id="left" class="panel">
  <div class="kicker">01 / OPERATION</div><h3 class="section">风机运行控制</h3>
  <div class="control"><label>叶轮转速 <output id="rpmOut">12 rpm</output></label>
   <input id="rpm" type="range" min="0" max="28" value="12"></div>
  <div class="btnrow"><button id="toggle" class="primary">Ⅱ 暂停旋转</button><button id="reset">↺ 重置视角</button></div>
  <div class="divider"></div>
  <div class="control"><label>风速 <output id="windOut">12.3 m/s</output></label>
   <input id="wind" type="range" min="0" max="35" step=".1" value="12.3"></div>
  <div class="control"><label>有效波高 <output id="waveOut">2.1 m</output></label>
   <input id="wave" type="range" min="0" max="10" step=".1" value="2.1"></div>
  <div class="control"><label>涂层损伤演示值 <output id="damageOut">28%</output></label>
   <input id="damage" type="range" min="0" max="100" value="28"></div>
  <div class="control"><label>涂层显示</label>
   <div class="btnrow"><button id="coatBtn" class="primary">✓ 显示涂层</button><button id="heatBtn">隐藏损伤热图</button></div></div>
  <div class="divider"></div>
  <div class="note">数据为程序生成的演示值。叶片涂层和损伤颜色用于展示交互逻辑，不代表真实检测结论。</div>
 </section>

 <section id="right" class="panel">
  <div class="kicker">02 / BLADE INTEGRITY</div><h3 class="section">叶片涂层状态</h3>
  <div class="status"><strong id="statusTitle">建议检查</strong><span id="statusText">外段前缘出现模拟涂层磨蚀区域，建议查看分区趋势。</span></div>
  <div class="divider"></div>
  <div class="metric"><span>当前风速</span><strong id="windMetric">12.3 <small>m/s</small></strong></div>
  <div class="metric"><span>波浪高度</span><strong id="waveMetric">2.1 <small>m</small></strong></div>
  <div class="metric"><span>损伤演示值</span><strong id="damageMetric">28 <small>%</small></strong></div>
  <div class="metric"><span>重点分区</span><strong id="segmentMetric">S08 <small>外段</small></strong></div>
  <div class="divider"></div>
  <div class="kicker">03 / MAINTENANCE</div><h3 class="section">维护提示</h3>
  <div class="note" id="advice">建议对叶片前缘开展目视复核，并结合实际检测数据确认损伤范围。</div>
  <div class="divider"></div>
  <div class="btnrow"><button id="inspect">查看叶片分区</button><button id="full">全景视角</button></div>
 </section>

 <div id="toast"></div>
 <div id="hotspot">拖动旋转视角 · 滚轮缩放 · 叶片持续旋转</div>
 <div id="bottom">
  <div class="legend">涂层 / 损伤映射<div class="gradient"></div><div style="display:flex;justify-content:space-between"><span>完好</span><span>过渡</span><span>损伤</span></div></div>
  <div class="hint">演示模型 · 非真实设备扫描 · 非工程安全评估</div>
 </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script>
(function(){
 const host=document.getElementById('scene');
 if(!window.THREE){host.innerHTML='<div style="color:white;padding:30px">三维库加载失败，请检查网络后刷新。</div>';return;}
 const THREE=window.THREE;
 const scene=new THREE.Scene();
 scene.background=new THREE.Color(0x789eac);
 scene.fog=new THREE.Fog(0x789eac,24,78);
 const camera=new THREE.PerspectiveCamera(43,1,0.1,180);
 camera.position.set(10,8,14);
 const renderer=new THREE.WebGLRenderer({antialias:true,alpha:false});
 renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
 renderer.setSize(host.clientWidth,host.clientHeight);
 renderer.outputEncoding=THREE.sRGBEncoding;
 renderer.toneMapping=THREE.ACESFilmicToneMapping;
 renderer.toneMappingExposure=0.82;
 renderer.shadowMap.enabled=true;
 renderer.shadowMap.type=THREE.PCFSoftShadowMap;
 host.appendChild(renderer.domElement);
 const controls=new THREE.OrbitControls(camera,renderer.domElement);
 controls.target.set(0,4.1,0); controls.enableDamping=true; controls.dampingFactor=.06;
 controls.minDistance=6;controls.maxDistance=34;controls.maxPolarAngle=Math.PI*.49;

 scene.add(new THREE.HemisphereLight(0xd6eaf2,0x284653,0.82));
 const sun=new THREE.DirectionalLight(0xfff4df,1.15);sun.position.set(-8,15,10);sun.castShadow=true;scene.add(sun);
 const fill=new THREE.DirectionalLight(0x62b8ce,.28);fill.position.set(8,7,-10);scene.add(fill);

 // Ocean with gentle vertex waves
 const oceanGeo=new THREE.PlaneGeometry(180,180,100,100);
 oceanGeo.rotateX(-Math.PI/2);
 const oceanMat=new THREE.MeshPhongMaterial({color:0x176b87,shininess:32,specular:0x376f80,side:THREE.DoubleSide});
 const ocean=new THREE.Mesh(oceanGeo,oceanMat);ocean.position.y=-.18;ocean.receiveShadow=true;scene.add(ocean);
 const basePositions=oceanGeo.attributes.position.array.slice();
 const grid=new THREE.GridHelper(65,52,0x75c3d0,0x5da9b9);grid.position.y=-.145;
 grid.material.transparent=true;grid.material.opacity=.14;scene.add(grid);

 // Soft distant island silhouettes
 function makeIsland(x,z,sx,sz){
   const g=new THREE.SphereGeometry(1,24,12);
   const m=new THREE.MeshStandardMaterial({color:0x557e78,roughness:1});
   const o=new THREE.Mesh(g,m);o.position.set(x,.15,z);o.scale.set(sx,.45,sz);scene.add(o);
 }
 makeIsland(-17,-24,8,3);makeIsland(-7,-28,6,2.4);makeIsland(17,-31,9,3.2);makeIsland(28,-22,7,2.5);

 // Main turbine tower: tapered, multi-section surface
 const towerMat=new THREE.MeshStandardMaterial({color:0xcbd8df,roughness:.58,metalness:.06});
 const towerGeo=new THREE.CylinderGeometry(.19,.39,6.0,32,12,false);
 const tower=new THREE.Mesh(towerGeo,towerMat);tower.position.set(0,2.82,0);tower.castShadow=true;scene.add(tower);
 // Dark tower door
 const door=new THREE.Mesh(new THREE.BoxGeometry(.13,.65,.035),new THREE.MeshStandardMaterial({color:0x536b78,roughness:.8}));
 door.position.set(0,1.05,.37);scene.add(door);

 // Three-legged offshore support and yellow service caps
 const supportMat=new THREE.MeshStandardMaterial({color:0x326f80,metalness:.35,roughness:.42});
 const capMat=new THREE.MeshStandardMaterial({color:0xf2cf62,metalness:.25,roughness:.38});
 const legs=[];
 for(let i=0;i<3;i++){
   const a=i*2*Math.PI/3+.25,x=Math.cos(a)*.72,z=Math.sin(a)*.72;
   const leg=new THREE.Mesh(new THREE.CylinderGeometry(.13,.16,1.35,20),supportMat);
   leg.position.set(x,-.25,z);leg.castShadow=true;scene.add(leg);legs.push(leg);
   const cap=new THREE.Mesh(new THREE.CylinderGeometry(.16,.16,.12,20),capMat);
   cap.position.set(x,.46,z);scene.add(cap);
   const cable=new THREE.Mesh(new THREE.CylinderGeometry(.012,.012,3.2,8),new THREE.MeshStandardMaterial({color:0x365b68,roughness:1}));
   cable.position.set(x*.9,-1.65,z*.9);cable.rotation.z=.23*Math.sign(x||1);scene.add(cable);
 }

 // Nacelle and hub
 const nacelle=new THREE.Mesh(new THREE.BoxGeometry(.95,.43,.55),new THREE.MeshStandardMaterial({color:0xcbd8df,roughness:.55,metalness:.06}));
 nacelle.position.set(0,6.08,-.23);nacelle.castShadow=true;scene.add(nacelle);
 const hub=new THREE.Group();hub.position.set(0,6.08,.16);scene.add(hub);
 const hubBody=new THREE.Mesh(new THREE.SphereGeometry(.28,32,24),new THREE.MeshStandardMaterial({color:0xd7e2e8,roughness:.48,metalness:.05}));
 hub.add(hubBody);
 const hubNose=new THREE.Mesh(new THREE.SphereGeometry(.17,24,18),new THREE.MeshStandardMaterial({color:0xd8e5eb,roughness:.25}));
 hubNose.position.z=.22;hub.add(hubNose);

 // Blade mesh with aerodynamic tapered/chord/thickness profile, per-vertex coating colors.
 const bladeRoot=new THREE.Group();bladeRoot.position.copy(hub.position);scene.add(bladeRoot);
 const blades=[];
 let damage=28,heatOn=true,coatOn=true;
 function bladeProfile(t){
   const chord=.58*Math.pow(1-t,.72)+.055;
   const sweep=-.13*t*t;
   const thick=.105*Math.pow(1-t,.72)+.012;
   return {chord,sweep,thick};
 }
 function makeBlade(index){
   const group=new THREE.Group();
   const stations=48, across=12;
   const verts=[],colors=[],indices=[];
   const colorGood=new THREE.Color(0xcbd7df);
   const colorCoat=new THREE.Color(0x8edbd4);
   const colorWarn=new THREE.Color(0xffbd69);
   const colorBad=new THREE.Color(0xf0445d);
   for(let i=0;i<=stations;i++){
     const t=i/stations, p=bladeProfile(t), length=4.0;
     for(let j=0;j<=across;j++){
       const u=j/across*2-1;
       const x=p.sweep+u*p.chord*.5;
       const z=p.thick*Math.sqrt(Math.max(0,1-u*u));
       // Upper surface, leading edge gets pale aqua coating stripe.
       verts.push(x,t*length,z);
       let col=colorGood.clone();
       const leading=Math.abs(u+0.72)<.18;
       const trailing=t>.9;
       if(coatOn && leading) col.lerp(colorCoat,.75);
       const damageStart=0.82-damage/150;
       const inDamageBand=(u>-.98 && u<.22);
       if(heatOn && damage>0 && t>damageStart && inDamageBand){
         const q=Math.max(0,Math.min(1,(t-damageStart)/Math.max(.001,1-damageStart)));
         const edgeFactor=Math.max(0,Math.min(1,(.24-u)/1.15));
         col.lerp(colorWarn,Math.min(.96,.35+q*.65)*edgeFactor);
         if(q>.22) col.lerp(colorBad,Math.min(.98,(q-.22)*1.7)*edgeFactor);
       }
       if(trailing && heatOn && damage>55) col.lerp(colorWarn,.35);
       colors.push(col.r,col.g,col.b);
     }
   }
   const row=across+1;
   for(let i=0;i<stations;i++){
     for(let j=0;j<across;j++){
       const a=i*row+j,b=a+row;
       indices.push(a,b,a+1,b,b+1,a+1);
     }
   }
   // Lower surface
   const upperCount=verts.length/3;
   for(let i=0;i<=stations;i++){
     const t=i/stations,p=bladeProfile(t),length=4.0;
     for(let j=0;j<=across;j++){
       const u=j/across*2-1;
       verts.push(p.sweep+u*p.chord*.5,t*length,-p.thick*Math.sqrt(Math.max(0,1-u*u)));
       const col=colorGood.clone();
       if(coatOn && Math.abs(u+0.72)<.18) col.lerp(colorCoat,.6);
       if(heatOn && t>1-damage/125 && u<-.45) col.lerp(colorBad,.65);
       colors.push(col.r,col.g,col.b);
     }
   }
   for(let i=0;i<stations;i++){
     for(let j=0;j<across;j++){
       const a=upperCount+i*row+j,b=a+row;
       indices.push(upperCount+a,upperCount+a+1,upperCount+b,upperCount+b,upperCount+a+1,upperCount+b+1);
     }
   }
   const geo=new THREE.BufferGeometry();
   geo.setAttribute('position',new THREE.Float32BufferAttribute(verts,3));
   geo.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));
   geo.setIndex(indices);geo.computeVertexNormals();
   const mat=new THREE.MeshStandardMaterial({vertexColors:true,side:THREE.DoubleSide,roughness:.3,metalness:.04});
   const mesh=new THREE.Mesh(geo,mat);mesh.castShadow=true;mesh.receiveShadow=true;group.add(mesh);

   // Leading-edge protective coating ribbon on the visible surface.
   const stripVerts=[],stripColors=[],stripIdx=[];
   for(let i=0;i<=stations;i++){
     const t=i/stations,p=bladeProfile(t),length=4.0;
     const u=-.72;
     const x=p.sweep+u*p.chord*.5;
     const z=p.thick*Math.sqrt(Math.max(0,1-u*u))+.008;
     stripVerts.push(x-.018,t*length,z,x+.018,t*length,z);
     const c=(heatOn && t>1-damage/125)?colorBad:colorCoat;
     for(let k=0;k<2;k++)stripColors.push(c.r,c.g,c.b);
   }
   for(let i=0;i<stations;i++){const a=i*2;stripIdx.push(a,a+2,a+1,a+1,a+2,a+3);}
   const sg=new THREE.BufferGeometry();
   sg.setAttribute('position',new THREE.Float32BufferAttribute(stripVerts,3));
   sg.setAttribute('color',new THREE.Float32BufferAttribute(stripColors,3));
   sg.setIndex(stripIdx);sg.computeVertexNormals();
   const strip=new THREE.Mesh(sg,new THREE.MeshStandardMaterial({vertexColors:true,side:THREE.DoubleSide,roughness:.28,metalness:.02}));
   group.add(strip);
   // Rounded root collar
   const collar=new THREE.Mesh(new THREE.CylinderGeometry(.22,.29,.34,24),new THREE.MeshStandardMaterial({color:0xdde8ed,roughness:.28}));
   collar.rotation.x=Math.PI/2;collar.position.set(0,.23,0);group.add(collar);
   group.rotation.z=index*2*Math.PI/3;
   bladeRoot.add(group);blades.push(group);
 }
 for(let i=0;i<3;i++)makeBlade(i);

 // Distant turbines reuse the same detailed aerodynamic blade geometry and materials.
 const distantRotors=[];
 function addDistantTurbine(x,z,s){
   const g=new THREE.Group();g.position.set(x,0,z);g.scale.setScalar(s);scene.add(g);
   const farTower=tower.clone(true);farTower.position.set(0,2.82,0);farTower.castShadow=false;farTower.receiveShadow=false;g.add(farTower);
   const farNacelle=nacelle.clone(true);farNacelle.position.set(0,6.08,-.23);farNacelle.castShadow=false;g.add(farNacelle);
   const farHub=new THREE.Group();farHub.position.set(0,6.08,.16);g.add(farHub);
   farHub.add(hubBody.clone());farHub.add(hubNose.clone());
   const rotor=new THREE.Group();rotor.position.set(0,6.08,.16);g.add(rotor);
   for(let k=0;k<3;k++){
     const detailedBlade=blades[k].clone(true);
     detailedBlade.traverse(o=>{if(o.isMesh){o.castShadow=false;o.receiveShadow=false;}});
     rotor.add(detailedBlade);
   }
   for(let k=0;k<3;k++){
     const a=k*2*Math.PI/3+.25,px=Math.cos(a)*.72,pz=Math.sin(a)*.72;
     const leg=new THREE.Mesh(new THREE.CylinderGeometry(.13,.16,1.35,16),supportMat);
     leg.position.set(px,-.25,pz);g.add(leg);
     const cap=new THREE.Mesh(new THREE.CylinderGeometry(.16,.16,.12,16),capMat);
     cap.position.set(px,.46,pz);g.add(cap);
   }
   distantRotors.push(rotor);
 }
 [[-10,-14,.75],[-16,-20,.55],[12,-18,.65],[19,-24,.5],[-4,-25,.48]].forEach(p=>addDistantTurbine(...p));

 function recolorBlades(){
   const good=new THREE.Color(0xcbd7df);
   const coat=new THREE.Color(0x58cfc4);
   const warn=new THREE.Color(0xffa34d);
   const bad=new THREE.Color(0xf0445d);
   for(const group of blades){
     for(const obj of group.children){
       if(!obj.isMesh || !obj.geometry.attributes.position || !obj.geometry.attributes.color) continue;
       const pos=obj.geometry.attributes.position, col=obj.geometry.attributes.color;
       const isStrip=pos.count===98;
       for(let i=0;i<pos.count;i++){
         const y=pos.getY(i),t=Math.max(0,Math.min(1,y/4));
         let c=good.clone();
         if(isStrip){
           c=coat.clone();
           const start=0.82-damage/150;
           if(heatOn && damage>0 && t>start){
             const q=(t-start)/Math.max(.001,1-start);
             c.copy(q>.48?bad:warn);
           } else if(!coatOn) c.copy(good);
         } else {
           const x=pos.getX(i),p=bladeProfile(t);
           const u=(x-p.sweep)/Math.max(.001,p.chord*.5);
           const leading=Math.abs(u+.72)<.3;
           if(coatOn && leading)c.lerp(coat,.8);
           const start=0.82-damage/150;
           if(heatOn && damage>0 && t>start && u>-.98 && u<.22){
             const q=Math.max(0,Math.min(1,(t-start)/Math.max(.001,1-start)));
             const edgeFactor=Math.max(0,Math.min(1,(.24-u)/1.15));
             c.lerp(warn,Math.min(.98,.35+q*.65)*edgeFactor);
             if(q>.22)c.lerp(bad,Math.min(.99,(q-.22)*1.7)*edgeFactor);
           }
         }
         col.setXYZ(i,c.r,c.g,c.b);
       }
       col.needsUpdate=true;
     }
   }
 }

 function toast(msg){const t=document.getElementById('toast');t.textContent=msg;t.style.display='block';clearTimeout(toast.timer);toast.timer=setTimeout(()=>t.style.display='none',2200);}
 let rpm=12,paused=false,last=performance.now(),elapsed=0;
 const $=id=>document.getElementById(id);
 $('rpm').addEventListener('input',e=>{rpm=+e.target.value;$('rpmOut').textContent=rpm+' rpm';});
 $('wind').addEventListener('input',e=>{$('windOut').textContent=(+e.target.value).toFixed(1)+' m/s';$('windMetric').innerHTML=(+e.target.value).toFixed(1)+' <small>m/s</small>';});
 $('wave').addEventListener('input',e=>{$('waveOut').textContent=(+e.target.value).toFixed(1)+' m';$('waveMetric').innerHTML=(+e.target.value).toFixed(1)+' <small>m</small>';});
 $('damage').addEventListener('input',e=>{
   damage=+e.target.value;$('damageOut').textContent=damage+'%';$('damageMetric').innerHTML=damage+' <small>%</small>';
   $('statusTitle').textContent=damage<20?'涂层状态良好':damage<55?'建议检查':'重点复核';
   $('statusTitle').style.color=damage<20?'#72e3bd':damage<55?'#ffbd69':'#ff6475';
   $('statusText').textContent=damage<20?'当前模拟损伤程度较低，可继续观察。':damage<55?'叶片外段前缘出现模拟涂层磨蚀区域，建议查看分区趋势。':'模拟损伤程度较高，建议优先复核对应叶片分区。';
   $('segmentMetric').innerHTML=(damage>65?'S11':damage>35?'S08':'S04')+' <small>外段</small>';
   $('advice').textContent=damage<20?'按计划开展巡检并持续记录涂层状态。':damage<55?'建议对叶片前缘开展目视复核，并结合实际检测数据确认损伤范围。':'建议优先复核外段前缘区域；不得仅凭模拟值决定停机或维修。';
   recolorBlades();
 });
 $('toggle').addEventListener('click',()=>{paused=!paused;$('toggle').textContent=paused?'▶ 启动旋转':'Ⅱ 暂停旋转';$('toggle').classList.toggle('primary',!paused);});
 $('reset').addEventListener('click',()=>{camera.position.set(10,8,14);controls.target.set(0,4.1,0);controls.update();toast('已重置三维视角');});
 $('coatBtn').addEventListener('click',()=>{coatOn=!coatOn;$('coatBtn').textContent=coatOn?'✓ 显示涂层':'○ 隐藏涂层';recolorBlades();});
 $('heatBtn').addEventListener('click',()=>{heatOn=!heatOn;$('heatBtn').textContent=heatOn?'隐藏损伤热图':'显示损伤热图';recolorBlades();});
 $('inspect').addEventListener('click',()=>toast('已选中叶片外段分区 S08（演示数据）'));
 $('full').addEventListener('click',()=>{camera.position.set(10,8,14);controls.target.set(0,3.5,0);controls.update();});
 $('clock').textContent=new Date().toLocaleTimeString('zh-CN',{hour12:false});
 setInterval(()=>$('clock').textContent=new Date().toLocaleTimeString('zh-CN',{hour12:false}),1000);

 // Click on main blades to display a demo segment label.
 const raycaster=new THREE.Raycaster(),mouse=new THREE.Vector2();
 renderer.domElement.addEventListener('click',e=>{
   const r=renderer.domElement.getBoundingClientRect();
   mouse.x=((e.clientX-r.left)/r.width)*2-1;mouse.y=-((e.clientY-r.top)/r.height)*2+1;
   raycaster.setFromCamera(mouse,camera);
   const hits=raycaster.intersectObjects(blades,true);
   if(hits.length)toast('叶片分区 S08 · 涂层损伤演示值 '+damage+'%');
 });

 function resize(){
   const w=host.clientWidth,h=host.clientHeight;
   camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h);
 }
 window.addEventListener('resize',resize);
 function animate(now){
   requestAnimationFrame(animate);
   const dt=Math.min(.05,(now-last)/1000);last=now;elapsed+=dt;
   if(!paused){const spin=rpm*2*Math.PI/60*dt;bladeRoot.rotation.z+=spin;for(const rotor of distantRotors)rotor.rotation.z+=spin;}
   const p=oceanGeo.attributes.position;
   for(let i=0;i<p.count;i++){
     const x=basePositions[i*3],z=basePositions[i*3+2];
     p.setY(i,basePositions[i*3+1]+.035*Math.sin(x*.55+elapsed*1.25)*Math.cos(z*.42+elapsed*.85));
   }
   p.needsUpdate=true;oceanGeo.computeVertexNormals();
   controls.update();renderer.render(scene,camera);
 }
 requestAnimationFrame(animate);
})();
</script>
</body>
</html>
"""

components.html(html, height=920, scrolling=False)
