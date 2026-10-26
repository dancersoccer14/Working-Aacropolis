(async()=>{
const assetBase=new URL('.',document.currentScript.src);
const locations=await fetch(new URL('locations.json',assetBase)).then(r=>{if(!r.ok)throw Error('Locations unavailable');return r.json()});
let current='alberta';
const map=L.map('map',{scrollWheelZoom:false,zoomControl:false,minZoom:6,maxZoom:14,zoomSnap:.25,zoomDelta:.75}).setView([53.52,-113.54],10);
L.control.zoom({position:'topright'}).addTo(map);
map.attributionControl.setPrefix('<a href="https://leafletjs.com">Leaflet</a>');
const tiles=L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',{attribution:'Tiles &copy; Esri &mdash; Esri, HERE, Garmin, OpenStreetMap contributors',maxZoom:16}).addTo(map);
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Reference/MapServer/tile/{z}/{y}/{x}',{maxZoom:16,interactive:false}).addTo(map);
let loaded=false;tiles.on('tileload',()=>{loaded=true;document.querySelector('.map-warning').hidden=true});tiles.on('tileerror',()=>{if(!loaded)document.querySelector('.map-warning').hidden=false});
const layer=L.layerGroup().addTo(map);
const emblem='<span class="mini-emblem" aria-hidden="true"><img src="'+new URL('emblem.svg',assetBase).href+'" alt=""></span>';
const label={new:'NEW NEIGHBOURHOOD',infill:'EDMONTON INFILL',acreage:'ACREAGE BUILDS',beyond:'ACROSS ALBERTA'};
const copies={new:'New beginnings.<br>Lasting neighbourhoods.',infill:'Fresh possibilities.<br>Established communities.',acreage:'More room to imagine.<br>More space to call home.',alberta:'Our roots in Edmonton.<br>Our reach across Alberta.'};
const visible=()=>locations.filter(p=>p.point&&(current==='alberta'||p.kind===current));
function bounds(points){return L.latLngBounds(points.map(p=>p.point))}
function fit(points){const narrow=map.getSize().x<600;map.fitBounds(bounds(points),{paddingTopLeft:narrow?[35,175]:[275,55],paddingBottomRight:[45,50],maxZoom:11.5,animate:false})}
function popup(p){return `<div class="popup-label">${label[p.kind]}</div><div class="popup-name">${p.name}</div><div class="popup-region">${p.kind==='acreage'?'Alberta':p.region}</div>`}
function render(){
 layer.clearLayers();const groups=[];
 for(const p of visible()){
  const pixel=map.latLngToContainerPoint(p.point);let group=groups.find(g=>g.pixel.distanceTo(pixel)<25);
  if(group){group.items.push(p);group.pixel=L.point((group.pixel.x*(group.items.length-1)+pixel.x)/group.items.length,(group.pixel.y*(group.items.length-1)+pixel.y)/group.items.length)}else groups.push({pixel,items:[p]});
 }
 for(const g of groups){
  const items=g.items,isCluster=items.length>1,pos=map.containerPointToLatLng(g.pixel);
  const names=items.map(p=>p.name).join(' · ');
  const icon=L.divIcon({className:'brand-pin'+(isCluster?' cluster':''),html:`<div class="pin">${emblem}</div>`,iconSize:[29,29],iconAnchor:[14.5,14.5],popupAnchor:[0,-14]});
  const marker=L.marker(pos,{icon,title:names,alt:names,keyboard:true}).addTo(layer);
  marker.bindTooltip(isCluster?`${items.length} communities · select to explore`:items[0].name,{direction:'top',offset:[0,-18],permanent:!isCluster&&current==='alberta'&&items[0].kind==='beyond'});
  if(isCluster){marker.on('click',()=>{if(map.getZoom()<13.5)map.fitBounds(bounds(items),{padding:[75,75],maxZoom:Math.min(14,map.getZoom()+2)});else marker.bindPopup(items.map(popup).join('<hr style="border:0;border-top:1px solid #e1d9cd;margin:15px 0">')).openPopup()})}else marker.bindPopup(popup(items[0]));
 }
}
function setView(view){current=view;map.closePopup();document.querySelectorAll('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.filter===view)));document.querySelector('#view-copy').innerHTML=copies[view];fit(current==='alberta'?visible().filter(p=>p.kind==='new'||p.kind==='infill'):visible());render()}
map.on('zoomend moveend',render);
document.querySelectorAll('[data-filter]').forEach(b=>b.onclick=()=>setView(b.dataset.filter));document.querySelector('.reset').onclick=()=>setView(current);
setView('alberta');
let resizeTimer;const resizeObserver=new ResizeObserver(()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{map.invalidateSize();setView(current)},120)});resizeObserver.observe(document.querySelector('#map'));
})().catch(()=>{document.querySelector('#map').innerHTML='<p style="padding:30px">The map couldn’t load. Please refresh to try again.</p>'});
