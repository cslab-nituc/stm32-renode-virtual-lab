'use strict';
const $=id=>document.getElementById(id);
let queue=Promise.resolve(),connected=false,angle=0,direction=0,previous=0;
const masks=[63,6,91,79,102,109,125,39,127,111,119,124,88,94,121,113];
const controls=[$('adc-slider0'),...Array.from({length:4},(_,i)=>[$(`sw${i}-on`),$(`sw${i}-off`),$(`sw${i}-toggle`)]).flat()];
function offline(){connected=false;direction=0;document.body.classList.add('disconnected');$('status-text').textContent='未接続';$('motor-state').textContent='—';controls.forEach(x=>x.disabled=true);for(let i=0;i<4;i++)$(`psw${i}-status`).textContent='—';}
function render(s){connected=true;document.body.classList.remove('disconnected');$('status-text').textContent='connected';controls.forEach(x=>x.disabled=false);
for(let i=0;i<8;i++)$(`led${i}`).classList.toggle('led-on',!!(s.leds&(1<<i)));
$('adc-value0').textContent=s.adc;if(document.activeElement!==$('adc-slider0'))$('adc-slider0').value=s.adc;
for(let i=0;i<4;i++){$(`psw${i}-status`).textContent=s.switches[`PSW${i}`]?'ON':'OFF';$(`sw${i}-toggle`).checked=s.switches[`TSW${i}`];const v=s.digits[i];[...'abcdefg'].forEach((name,j)=>$(`7seg-${i}`).querySelector(`.seg-${name}`).classList.toggle('on',v!==null&&!!(masks[v]&(1<<j))));}
direction=s.motor==='forward'?1:s.motor==='reverse'?-1:0;$('motor-state').textContent={forward:'正転',reverse:'逆転',stop:'停止'}[s.motor];}
async function request(path,options){try{const r=await fetch(path,options);const d=await r.json();if(!r.ok||!d.connected)throw Error();render(d.state);}catch(e){offline();}}
function input(signal,value){queue=queue.then(()=>request('/api/input',{method:'POST',headers:{'Content-Type':'application/json','X-Virtual-Lab':'1'},body:JSON.stringify({signal,value})}));}
for(let i=0;i<4;i++){$(`sw${i}-on`).addEventListener('click',()=>input(`PSW${i}`,true));$(`sw${i}-off`).addEventListener('click',()=>input(`PSW${i}`,false));$(`sw${i}-toggle`).addEventListener('change',e=>input(`TSW${i}`,e.target.checked));}
$('adc-slider0').addEventListener('input',()=>{$('adc-value0').textContent=$('adc-slider0').value;});
$('adc-slider0').addEventListener('change',()=>input('AnalogInput0',Number($('adc-slider0').value)));
window.addEventListener('blur',()=>{if(connected)for(let i=0;i<4;i++)input(`PSW${i}`,false);});
function animate(now){if(previous)angle=(angle+direction*Math.min(now-previous,100)*.2)%360;previous=now;$('motor').style.transform=`rotate(${angle}deg)`;requestAnimationFrame(animate);}
offline();requestAnimationFrame(animate);
async function poll(){queue=queue.then(()=>request('/api/state'));await queue;setTimeout(poll,200);}poll();
