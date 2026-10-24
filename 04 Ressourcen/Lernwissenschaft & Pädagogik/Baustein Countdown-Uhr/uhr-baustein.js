  /* Countdown-Uhr: läuft weiter, auch wenn die Folie gewechselt wird */
  var uhr=document.createElement('div'); uhr.id='uhr';
  uhr.innerHTML='<span class="ut">0:00</span><button class="pri" data-u="go">Start</button><button data-u="rs" title="Zurücksetzen">↺</button><span class="upre"></span><button data-u="m" title="eine Minute weniger">−1</button><button data-u="p" title="eine Minute mehr">+1</button>';
  stage.appendChild(uhr);
  uhr.addEventListener('click',e=>e.stopPropagation());
  var uSec=0, uEnd=0, uRun=false, uBase=0, uTick=null;
  const uq=s=>uhr.querySelector(s);
  function uRest(){ return uRun ? Math.max(0,Math.ceil((uEnd-Date.now())/1000)) : uSec; }
  function uDraw(){
    const r=uRest(); uq('.ut').textContent=Math.floor(r/60)+':'+String(r%60).padStart(2,'0');
    uhr.classList.toggle('knapp', r>0&&r<=60&&(uRun||r<uBase)); uhr.classList.toggle('aus', r===0&&uBase>0);
    uq('[data-u=go]').textContent=uRun?'Pause':(r===0?'Fertig':'Start');
    uhr.style.display=(slides[i].dataset.timer||uRun||(uBase>0&&r===0))?'flex':'none';
  }
  function uBeep(){ try{ const ac=new (window.AudioContext||window.webkitAudioContext)(); [0,.35,.7].forEach(d=>{ const o=ac.createOscillator(), g=ac.createGain(); o.frequency.value=880; g.gain.value=.15; o.connect(g); g.connect(ac.destination); o.start(ac.currentTime+d); o.stop(ac.currentTime+d+.2); }); }catch(e){} }
  function uStop(){ uRun=false; clearInterval(uTick); }
  function uSet(min){ uStop(); uBase=min*60; uSec=uBase; uMarks(); uDraw(); }
  function uMarks(){ uhr.querySelectorAll('.upre button').forEach(b=>b.classList.toggle('on',+b.dataset.min*60===uBase)); }
  function uToggle(){
    if(uRun){ uSec=uRest(); uStop(); }
    else if(uSec>0){ uEnd=Date.now()+uSec*1000; uRun=true; uTick=setInterval(()=>{ if(uRest()===0){ uSec=0; uStop(); uBeep(); } uDraw(); },250); }
    uDraw();
  }
  function uSlide(){
    const a=slides[i].dataset.timer;
    if(a && !uRun){
      const p=a.split(',').map(Number), box=uq('.upre'); box.innerHTML='';
      if(p.length>1) p.forEach(m=>{ const b=document.createElement('button'); b.dataset.min=m; b.textContent=m+' Min.'; b.addEventListener('click',()=>uSet(m)); box.appendChild(b); });
      uSet(p[0]);
    }
    uDraw();
  }
  uq('[data-u=go]').addEventListener('click',uToggle);
  uq('[data-u=rs]').addEventListener('click',()=>{ const m=uBase/60; if(m) uSet(m); });
  uq('[data-u=m]').addEventListener('click',()=>{ if(uRun) uEnd-=60000; else uSec=Math.max(0,uSec-60); uDraw(); });
  uq('[data-u=p]').addEventListener('click',()=>{ if(uRun) uEnd+=60000; else uSec+=60; uDraw(); });
