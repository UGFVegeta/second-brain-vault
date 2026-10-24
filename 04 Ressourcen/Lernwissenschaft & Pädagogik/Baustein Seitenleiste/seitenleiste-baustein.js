  /* Seitenleiste: Abschnitte aus data-tab und data-group der Folien, Punkte = Folien im Abschnitt */
  const side=document.getElementById('side'), present=document.getElementById('present');
  const tabs=[];
  slides.forEach((s,k)=>{ const n=s.dataset.tab||'Folien'; let t=tabs[tabs.length-1]; if(!t||t.name!==n){ t={name:n,group:s.dataset.group||'',idx:[]}; tabs.push(t); } t.idx.push(k); s._tab=tabs.length-1; });
  const sideTitle=document.createElement('h2'); sideTitle.textContent=(document.querySelector('.slide h1')||{}).textContent||'Folien'; side.appendChild(sideTitle);
  const tabBtns2=[]; let lastG='';
  tabs.forEach(t=>{
    if(t.group && t.group!==lastG){ const g=document.createElement('div'); g.className='grp'; g.textContent=t.group; side.appendChild(g); }
    lastG=t.group;
    const b=document.createElement('button'); b.className='tab'+(t.group?' sub':'');
    const l=document.createElement('span'); l.textContent=t.name; b.appendChild(l);
    const p=document.createElement('span'); p.className='punkte';
    if(t.idx.length>1) t.idx.forEach(k=>{ const d=document.createElement('i'); d.addEventListener('click',ev=>{ ev.stopPropagation(); show(k,false); }); p.appendChild(d); });
    b.appendChild(p); b.addEventListener('click',()=>{ show(t.idx[0],false); b.blur(); }); side.appendChild(b); tabBtns2.push(b);
  });
  const sideHint=document.createElement('div'); sideHint.className='hinweis';
  sideHint.innerHTML='<kbd>←</kbd> <kbd>→</kbd> Schritt<br><kbd>↑</kbd> <kbd>↓</kbd> Abschnitt<br><kbd>T</kbd> Leiste aus/ein<br><kbd>F</kbd> Vollbild<br><kbd>M</kbd> Mindmap, <kbd>G</kbd> Gruppen';
  side.appendChild(sideHint);
  function updSide(){
    const ti=slides[i]._tab;
    tabBtns2.forEach((b,k)=>{
      b.classList.toggle('aktiv',k===ti);
      const pos=tabs[k].idx.indexOf(i);
      b.querySelectorAll('i').forEach((d,j)=>{ d.className=(k===ti&&j<=pos)?'an':''; });
      if(k===ti && (b.offsetTop<side.scrollTop || b.offsetTop+b.offsetHeight>side.scrollTop+side.clientHeight)) side.scrollTop=Math.max(0,b.offsetTop-60);
    });
  }
  function tabStep(d){ const ti=Math.max(0,Math.min(tabs.length-1,slides[i]._tab+d)); show(tabs[ti].idx[0],false); }
