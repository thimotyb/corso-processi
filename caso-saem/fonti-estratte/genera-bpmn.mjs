// Generazione deterministica dei BPMN dalle evidenze strutturate SAEM.
// I file esportati dal Modeler possono aggiungere informazioni di presentazione.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const base=path.dirname(fileURLToPath(import.meta.url));
const out=path.resolve(base,'../esempi-apqc/02-gestione-ordine');
const {views}=JSON.parse(fs.readFileSync(path.join(base,'estrazione-ordine.json'),'utf8'));
const esc=s=>String(s??"").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;");
const attr=o=>Object.entries(o).filter(([k,v])=>v!==undefined).map(([k,v])=>` ${k}="${esc(v)}"`).join("");
const tag=(name,a={},body="")=>`<${name}${attr(a)}>${body}</${name}>`;
const b=(name,a={},body="")=>tag("bpmn:"+name,a,body);
function geo(n){const t=n.type;let offset=n.y-(180+n.l*440);if(offset>0)offset=Math.max(200,offset);return {x:n.x,y:300+n.l*800+offset*1.6,w:t.includes("Gateway")?50:t.includes("Event")?36:t==="subProcess"?180:170,h:t.includes("Gateway")?50:t.includes("Event")?36:90};}
function routeY(y){const lane=Math.max(0,Math.floor((y+40)/440));return 300+lane*800+(y-(180+lane*440))*1.6;}
// Orthogonal A* routing around rendered shapes and labels (lane borders are traversable).
function orthogonal(a,z,obstacles,branch=0){
 const dir=z.x<a.x?-1:1;
 const side=branch===1?-dir:dir;
 const p=[a.x+side*a.w/2,a.y],q=[z.x-dir*z.w/2,z.y];
 const start=[p[0]+side*16,p[1]],end=[q[0]-dir*16,q[1]];
 const xs=[...new Set([start[0],end[0],...obstacles.flatMap(o=>[o.x-12,o.x+o.width+12])])].sort((a,b)=>a-b);
 const ys=[...new Set([start[1],end[1],...obstacles.flatMap(o=>[o.y-12,o.y+o.height+12])])].sort((a,b)=>a-b);
 const ny=ys.length, source=xs.indexOf(start[0])*ny+ys.indexOf(start[1]), target=xs.indexOf(end[0])*ny+ys.indexOf(end[1]);
 const point=id=>[xs[Math.floor(id/ny)],ys[id%ny]];
 const clear=(p,q)=>!obstacles.some(o=>p[0]===q[0]?
   p[0]>o.x-1&&p[0]<o.x+o.width+1&&Math.max(p[1],q[1])>o.y-1&&Math.min(p[1],q[1])<o.y+o.height+1:
   p[1]>o.y-1&&p[1]<o.y+o.height+1&&Math.max(p[0],q[0])>o.x-1&&Math.min(p[0],q[0])<o.x+o.width+1);
 const heap=[], push=(item)=>{heap.push(item);let i=heap.length-1;while(i){let p=(i-1)>>1;if(heap[p][0]<=item[0])break;heap[i]=heap[p];i=p;}heap[i]=item;};
 const pop=()=>{const r=heap[0],last=heap.pop();if(heap.length){let i=0;while(i*2+1<heap.length){let j=i*2+1;if(j+1<heap.length&&heap[j+1][0]<heap[j][0])j++;if(heap[j][0]>=last[0])break;heap[i]=heap[j];i=j;}heap[i]=last;}return r;};
 const distance=new Map([[source,0]]),previous=new Map();push([0,source]);
 const closed=new Set();let found=false;
 while(heap.length){const [,u]=pop();if(closed.has(u))continue;closed.add(u);if(u===target){found=true;break;}
 const ix=Math.floor(u/ny),iy=u%ny,up=point(u);
 for(const [vx,vy] of [[ix-1,iy],[ix+1,iy],[ix,iy-1],[ix,iy+1]]){
  if(vx<0||vx>=xs.length||vy<0||vy>=ys.length)continue;const k=vx*ny+vy;if(closed.has(k))continue;
  const vp=point(k);if(!clear(up,vp))continue;
  const old=previous.has(u)?point(previous.get(u)):null;
  const bend=old&&((old[0]===up[0])!==(vp[0]===up[0]))?24:0;
  const cost=distance.get(u)+Math.abs(up[0]-vp[0])+Math.abs(up[1]-vp[1])+bend;
  if(cost<(distance.get(k)??Infinity)){distance.set(k,cost);previous.set(k,u);push([cost+Math.abs(vp[0]-end[0])+Math.abs(vp[1]-end[1]),k]);}
 }
 }
 if(!found)throw new Error('No orthogonal route '+JSON.stringify({a,z}));
 const path=[];for(let k=target;k!==undefined;k=previous.get(k))path.push(point(k));path.reverse();
 const raw=[p,...path,q], result=[];
 for(const pt of raw){if(result.length&&pt[0]===result.at(-1)[0]&&pt[1]===result.at(-1)[1])continue;
  while(result.length>1&&((result.at(-2)[0]===result.at(-1)[0]&&result.at(-1)[0]===pt[0])||(result.at(-2)[1]===result.at(-1)[1]&&result.at(-1)[1]===pt[1])))result.pop();result.push(pt);}
 return result;
}
function generate(rootView,full=true){
const globals=new Map(),planes=[];
function build(v,id,isRoot=false){
const nodes=v.nodes.filter(n=>!["store","object"].includes(n.type));
const boxes=new Map(nodes.map(n=>[n.id,geo(n)]));
const graph=[],shapes=[],edges=[],obstacles=[],flowLabels=[];
const maxX=Math.max(...nodes.map(n=>n.x))+170, laneH=800;
const shape=(id,g,extra={},label)=>{
 if(!id.startsWith('Lane_')&&!id.startsWith('Participant_')){
  obstacles.push({x:g.x-g.w/2,y:g.y-g.h/2,width:g.w,height:g.h});
  if(label)obstacles.push(label);
 }
 const body=tag("dc:Bounds",{x:g.x-g.w/2,y:g.y-g.h/2,width:g.w,height:g.h})+(label?tag("bpmndi:BPMNLabel",{},tag("dc:Bounds",label)):"");
 shapes.push(tag("bpmndi:BPMNShape",{id:id+"_di_"+v.id,bpmnElement:id,...extra},body));
};
const edge=(id,pts,name="",labelPos)=>{
 let body=pts.map(p=>tag("di:waypoint",{x:p[0],y:p[1]})).join("");
 if(name){
  const width=name.length<12?70:125,height=name.length<26?28:44;
  const segs=pts.slice(1).map((p,i)=>({a:pts[i],b:p,len:Math.abs(p[0]-pts[i][0])+Math.abs(p[1]-pts[i][1])})).sort((a,b)=>b.len-a.len);
  const overlaps=r=>[...obstacles,...flowLabels].some(o=>r.x<o.x+o.width+4&&r.x+r.width>o.x-4&&r.y<o.y+o.height+4&&r.y+r.height>o.y-4);
  let pos;
  for(const s of segs){for(const ratio of [.5,.25,.75]){const x=s.a[0]+(s.b[0]-s.a[0])*ratio,y=s.a[1]+(s.b[1]-s.a[1])*ratio;
    for(const p of [{x:x-width/2,y:y-height-9,width,height},{x:x+9,y:y-height/2,width,height},{x:x-width/2,y:y+9,width,height}])if(!overlaps(p)){pos=p;break;}if(pos)break;}if(pos)break;}
  pos??={x:pts[0][0]+12,y:pts[0][1]-height-12,width,height};flowLabels.push(pos);
  body+=tag('bpmndi:BPMNLabel',{},tag('dc:Bounds',pos));
 }
 edges.push(tag("bpmndi:BPMNEdge",{id:id+"_di_"+v.id,bpmnElement:id},body));
};
const isMain=v.id==="Process_SAEM_Ordine";
let laneXML=b("laneSet",{id:"Lanes_"+v.id},v.lanes.map((name,i)=>{
const lid="Lane_"+v.id+"_"+i;
shape(lid,{x:(maxX+40)/2,y:i*laneH+laneH/2,w:maxX-40,h:laneH},{isHorizontal:"true"});
return b("lane",{id:lid,name},nodes.filter(n=>n.l===i).map(n=>b("flowNodeRef",{},n.id)).join(""));
}).join(""));
for(const node of nodes){
 const ns=[];const related=v.links.filter(l=>l.task===node.id);
 const doc=[
 `Scenario: ${v.scope}. Responsabilità: ${v.lanes[node.l]}.`,
 `Fonte: ${node.source||v.source}.`,
 `Evidenza: ${node.evidence||"Attività / relazione derivata dalla fonte; aggregazione e traduzione BPMN didattiche."}`,
 ...related.map(l=>{const data=v.nodes.find(d=>d.id===l.data);return `${l.crud} | ${data.name.replaceAll("\n"," ")} | ${l.detail} | Fonte ${l.source}`;}),
 related.length?"":"Entità/tabelle non specificate per questa decisione/evento.",
 node.type==="subProcess"?"Sottoprocesso completo: aprire il dettaglio con il pulsante di navigazione del Modeler.":"",
 node.multi?"Multi-istanza parallela: un'istanza per ogni consegna del piano. Astrazione didattica; non eseguibile.":""
 ].filter(Boolean).join("\n");
 ns.push(b("documentation",{},esc(doc)));
 v.flows.forEach((f,i)=>{if(f.b===node.id)ns.push(b("incoming",{},`Flow_${v.id}_${i}`));});
 v.flows.forEach((f,i)=>{if(f.a===node.id)ns.push(b("outgoing",{},`Flow_${v.id}_${i}`));});
 // Local references avoid long crossed data associations. They refer to the same logical archives.
 const groups=[["store",related.filter(l=>v.nodes.find(d=>d.id===l.data).type==="store")],...related.filter(l=>v.nodes.find(d=>d.id===l.data).type==="object").map(l=>["object",[l]])].filter(g=>g[1].length);
 const ioInputs=[],ioOutputs=[],assocs=[];
 for(let gi=0;gi<groups.length;gi++){
 const [kind,links]=groups[gi];const baseId="Data_"+node.id+"_"+kind+"_"+gi;
 const allStoreEmax=kind==="store"&&links.every(l=>v.nodes.find(d=>d.id===l.data).name.startsWith("Emaxgest5"));
 const names=[...new Set(links.map(l=>v.nodes.find(d=>d.id===l.data).name.replaceAll("\n"," ")))];
 const label=kind==="object"?(names.length===1?names[0]:names[0]+" + altri"):
 allStoreEmax?("Emaxgest5 · "+([...new Set(names.flatMap(n=>n.replace("Emaxgest5 · ","").split(/ \/ | · /)))].slice(0,2).join(" / "))+(names.length>1?" …":"")):
 (names.length===1?names[0].split("\n")[0]:"Archivi gestionali / documentali");
 const dataDoc=links.map(l=>`${l.crud}: ${v.nodes.find(d=>d.id===l.data).name}. ${l.detail} Fonte: ${l.source}`).join("\n");
 let refid=baseId+"_ref";
 if(kind==="store"){
 const dsid=allStoreEmax?"Store_Emaxgest5":baseId+"_store";
 if(!globals.has(dsid))globals.set(dsid,b("dataStore",{id:dsid,name:allStoreEmax?"Emaxgest5 · PostgreSQL":"Archivi logici dell'attività "+node.id},b("documentation",{},esc(allStoreEmax?"Database documentato dal caso SAEM. Ogni riferimento mostra una proiezione delle tabelle usate dal task.":"Raggruppamento grafico degli archivi consultati/prodotti; non identifica un nuovo database fisico. Vedere documentazione."))));
 graph.push(b("dataStoreReference",{id:refid,name:label,dataStoreRef:dsid},b("documentation",{},esc(dataDoc))));
 }else{graph.push(b("dataObject",{id:baseId}));graph.push(b("dataObjectReference",{id:refid,name:label,dataObjectRef:baseId},b("documentation",{},esc(dataDoc))));}
 const ng=boxes.get(node.id);const dg={x:ng.x+(gi-(groups.length-1)/2)*136,y:ng.y-155,w:kind==="store"?50:36,h:kind==="store"?48:50};
 shape(refid,dg,{}, {x:dg.x-(groups.length===1?100:67),y:dg.y+30,width:groups.length===1?200:134,height:65});
 const read=links.some(l=>l.crud.includes("R")||l.crud.includes("U")||l.crud.includes("D"));
 const write=links.some(l=>/[CUD]/.test(l.crud));
 if(read){
 const input=baseId+"_input";ioInputs.push(b("dataInput",{id:input,name:"Dati in ingresso"}));
 const aid=baseId+"_in";assocs.push(b("dataInputAssociation",{id:aid},b("sourceRef",{},refid)+b("targetRef",{},input)));
 edge(aid,[[dg.x-9,dg.y+dg.h/2],[dg.x-9,ng.y-ng.h/2]]);
 }
 if(write){
 const output=baseId+"_output";ioOutputs.push(b("dataOutput",{id:output,name:"Dati prodotti / modificati"}));
 const aid=baseId+"_out";assocs.push(b("dataOutputAssociation",{id:aid},b("sourceRef",{},output)+b("targetRef",{},refid)));
 edge(aid,[[dg.x+9,ng.y-ng.h/2],[dg.x+9,dg.y+dg.h/2]]);
 }
 }
 if(groups.length){
 ns.push(b("ioSpecification",{},ioInputs.join("")+ioOutputs.join("")+
 b("inputSet",{id:"Inputs_"+node.id},ioInputs.map(s=>b("dataInputRefs",{},/id="([^"]+)"/.exec(s)[1])).join(""))+
 b("outputSet",{id:"Outputs_"+node.id},ioOutputs.map(s=>b("dataOutputRefs",{},/id="([^"]+)"/.exec(s)[1])).join(""))));
 }
 // BPMN activities contain associations after ioSpecification.
 ns.push(...assocs.filter(s=>s.startsWith('<bpmn:dataInputAssociation')), ...assocs.filter(s=>s.startsWith('<bpmn:dataOutputAssociation')));
 if(node.multi)ns.push(b("multiInstanceLoopCharacteristics",{isSequential:"false"},b("loopCardinality",{"xsi:type":"bpmn:tFormalExpression"},"numeroConsegne")));
 if(node.view){
 const child=views.find(v=>v.id===node.view);
 const childResult=build(child,node.id,false);
 ns.push(childResult.content);
 }
 if(node.id==='Start_Main')ns.push(b('messageEventDefinition',{id:'Message_Start_Main'}));
 if(node.timer)ns.push(b("timerEventDefinition",{id:"Timer_"+node.id},b("timeDate",{"xsi:type":"bpmn:tFormalExpression"},node.timer)));
 const defaultFlow=node.type==="exclusiveGateway"?v.flows.findIndex(f=>f.a===node.id&&(f.name.startsWith("No")||f.name==="Rinuncia"||f.name==="Abbandonare")):-1;
 graph.push(b(node.type,{id:node.id,name:node.name,...(defaultFlow>=0?{default:`Flow_${v.id}_${defaultFlow}`}:{})},ns.join("")));
 const g=boxes.get(node.id);
 shape(node.id,g,node.type==="subProcess"?{isExpanded:"false"}:{},node.type.includes("Gateway")||node.type.includes("Event")?{x:g.x-65,y:g.y+g.h/2+9,width:130,height:55}:undefined);
 }
 for(let i=0;i<v.flows.length;i++){
 const f=v.flows[i],a=boxes.get(f.a),z=boxes.get(f.b),idFlow=`Flow_${v.id}_${i}`;
 let pts;
 if(f.viaY!==undefined){let y=routeY(f.viaY);pts=[[a.x,a.y+a.h/2],[a.x,y],[z.x,y],[z.x,z.y+z.h/2]];}
 else if(f.viaX!==undefined){let x=f.viaX;pts=[[a.x+a.w/2,a.y],[x,a.y],[x,z.y],[z.x+z.w/2,z.y]];}
 else if(a.y===z.y){pts=[[a.x+(z.x>a.x?a.w/2:-a.w/2),a.y],[z.x+(z.x>a.x?-z.w/2:z.w/2),z.y]];}
 else if(a.x===z.x){pts=[[a.x,a.y+(z.y>a.y?a.h/2:-a.h/2)],[z.x,z.y+(z.y>a.y?-z.h/2:z.h/2)]];}
 else {const x=(a.x+z.x)/2;pts=[[a.x+(z.x>a.x?a.w/2:-a.w/2),a.y],[x,a.y],[x,z.y],[z.x+(z.x>a.x?-z.w/2:z.w/2),z.y]];}
 pts=pts.filter((p,j)=>!j||p[0]!==pts[j-1][0]||p[1]!==pts[j-1][1]);
 const source=nodes.find(n=>n.id===f.a);
 const branchIndex=source.type==='exclusiveGateway'?v.flows.filter(ff=>ff.a===f.a).findIndex(ff=>ff===f):0;
 pts=orthogonal(a,z,obstacles,branchIndex);
 const defaultIdx=source.type==="exclusiveGateway"?v.flows.findIndex(ff=>ff.a===source.id&&(ff.name.startsWith("No")||ff.name==="Rinuncia"||ff.name==="Abbandonare")):-1;
 const cond=source.type==="exclusiveGateway"&&v.flows.filter(ff=>ff.a===f.a).length>1&&i!==defaultIdx?b("conditionExpression",{"xsi:type":"bpmn:tFormalExpression"},esc(f.name||"condizione documentata")):"";
 graph.push(b("sequenceFlow",{id:idFlow,sourceRef:f.a,targetRef:f.b,...(f.name?{name:f.name}:{})},cond));
 edge(idFlow,pts,f.name);
 }
 const content=laneXML+graph.join("");
 let planeElement=id;
 if(isRoot&&isMain){
 planeElement="Collaboration_SAEM";
 shape("Participant_SAEM",{x:maxX/2,y:v.lanes.length*laneH/2,w:maxX,h:v.lanes.length*laneH},{isHorizontal:"true"});
 shape("Participant_Cliente",{x:maxX/2,y:-170,w:maxX,h:70},{isHorizontal:"true"});
 // Separate channels, orthogonal and attached to the corresponding business interactions.
 for(const [mid,target,name] of [["Message_Richiesta","Start_Main","Richiesta"],["Message_Offerta","Sub_Offerta","Offerta"],["Message_Ordine","Sub_Ordine","Dati ordine"],["Message_Variazione","Sub_Modifica","Variazione"],["Message_Conferma","M_Conferma","Conferma"]]){
 const g=boxes.get(target),out=mid==="Message_Offerta"||mid==="Message_Conferma";
 const channel=g.x+(out?-110:110),top=[channel,-135],bottom=[g.x+(out?-g.w/2:g.w/2),g.y];
 edge(mid,out?[bottom,[channel,g.y],top]:[top,[channel,g.y],bottom],name);
 }
 }
 const plane=tag("bpmndi:BPMNDiagram",{id:"Diagram_"+v.id},tag("bpmndi:BPMNPlane",{id:"Plane_"+v.id,bpmnElement:planeElement},shapes.join("")+edges.join("")));
 planes.unshift(plane);
 return {content};
}
const root=build(rootView,rootView.id,true);
let collab="";
if(rootView.id==="Process_SAEM_Ordine")collab=b("collaboration",{id:"Collaboration_SAEM"},
b("participant",{id:"Participant_SAEM",name:"SAEM · ordine cliente · TO-BE MaxNet",processRef:rootView.id})+
b("participant",{id:"Participant_Cliente",name:"Cliente (partecipante esterno)"})+
[["Message_Richiesta","Start_Main","Richiesta",false],["Message_Offerta","Sub_Offerta","Offerta",true],["Message_Ordine","Sub_Ordine","Dati ordine",false],["Message_Variazione","Sub_Modifica","Variazione",false],["Message_Conferma","M_Conferma","Conferma",true]].map(([id,target,name,out])=>b("messageFlow",{id,name,sourceRef:out?target:"Participant_Cliente",targetRef:out?"Participant_Cliente":target})).join(""));
return '<?xml version="1.0" encoding="UTF-8"?>\n'+tag("bpmn:definitions",{
"xmlns:bpmn":"http://www.omg.org/spec/BPMN/20100524/MODEL","xmlns:bpmndi":"http://www.omg.org/spec/BPMN/20100524/DI","xmlns:dc":"http://www.omg.org/spec/DD/20100524/DC","xmlns:di":"http://www.omg.org/spec/DD/20100524/DI","xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",id:"Definitions_SAEM_"+rootView.id,targetNamespace:"https://saem.example/teaching",exporter:"SAEM course · MCP Camunda Modeler"
},[...globals.values()].join("")+collab+b("process",{id:rootView.id,name:rootView.name,isExecutable:"false"},b("documentation",{},esc(rootView.scope+". "+rootView.source+". Modello didattico completo nel perimetro ordine→spedizione→fatturazione; vedere processo.md per fonti e assunzioni."))+root.content)+planes.join(""))+"\n";
}
fs.mkdirSync(path.join(out,'dettagli'),{recursive:true});
for(const v of views){
 const name=v.id==='Process_SAEM_Ordine'?'processo.bpmn':'dettagli/'+v.id.toLowerCase()+'.bpmn';
 fs.writeFileSync(path.join(out,name),generate(v),'utf8');
}
console.log('Generati '+views.length+' BPMN.');
