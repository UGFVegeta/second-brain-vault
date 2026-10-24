  /* Gruppen-Generator: Zufall aus der Klassenliste. Die Namen bleiben im Browser (localStorage), nicht in dieser Datei. */
  const GRP_KEY='klasse-namen-v1';
  const GRP_COL=['#2f6f4f','#c2531e','#2457a6','#8a3d9a','#8a6a14','#0f7b8a','#a33a54','#5a6b1f'];
  let grpOpen=false, grpN=5, grpNums=24, grpState={};
  const grpEl=document.createElement('div'); grpEl.id='grp';
  grpEl.innerHTML='<div class="gtop"><h3>Gruppen auslosen</h3>'
    +'<span class="cnt">Gruppen <button data-d="-1">−</button><b id="gn">5</b><button data-d="1">+</button></span>'
    +'<span class="cnt" id="gnumwrap">Nummern bis <button data-nd="-1">−</button><b id="gnum">24</b><button data-nd="1">+</button></span>'
    +'<button id="gmix" class="pri">Neu mischen (N)</button><button id="glist">Klassenliste</button><button id="gback">Zurück (G)</button></div>'
    +'<div class="gpanel" id="gpanel"><b>Klassenliste</b>: einmal die Namensspalte aus Excel kopieren und hier einfügen, eine Zeile pro Person. Es werden nur Vornamen angezeigt. Die Namen bleiben nur in diesem Browser auf diesem Gerät, sie stehen nicht in der Datei.'
    +'<textarea id="gtext" placeholder="Eine Person pro Zeile"></textarea>'
    +'<div class="row"><label>In der Liste steht zuerst der <select id="gord"><option value="nv">Nachname</option><option value="vn">Vorname</option></select></label><span id="gprev" class="ghint"></span></div>'
    +'<div class="row"><button id="gsave" class="pri">Speichern</button><label><button id="gfilebtn" type="button">Aus Textdatei laden (.txt, .csv)</button><input id="gfile" type="file" accept=".txt,.csv,text/plain,text/csv" hidden></label><button id="gclear">Liste löschen</button><span id="gcount" class="ghint"></span></div>'
    +'<div class="ghint">Ohne Liste werden Nummern gemischt.</div></div>'
    +'<div class="gbody" id="gbody"></div>';
  stage.appendChild(grpEl);
  grpEl.addEventListener('click',e=>e.stopPropagation());
  const gq=s=>grpEl.querySelector(s);
  const GRP_KEY2='klasse-namen-v2', GRP_ORD='klasse-reihenfolge';
  function grpRaw(){ try{ let a=JSON.parse(localStorage.getItem(GRP_KEY2)||'null'); if(!Array.isArray(a)) a=JSON.parse(localStorage.getItem(GRP_KEY)||'[]'); return Array.isArray(a)?a:[]; }catch(e){ return []; } }
  function grpOrder(){ try{ return localStorage.getItem(GRP_ORD)||'nv'; }catch(e){ return 'nv'; } }
  /* eine Zeile der Liste in Vorname und Nachname zerlegen: ord 'nv' = Nachname zuerst, 'vn' = Vorname zuerst */
  function splitName(raw,ord){
    const parts=raw.split(/[\t;]/).map(x=>x.trim()).filter(Boolean); let v,n;
    if(parts.length>=2){ if(ord==='nv'){ n=parts[0]; v=parts[1]; } else { v=parts[0]; n=parts[1]; } }
    else{
      const s=parts[0]||'';
      if(s.includes(',')){ const q=s.split(',').map(x=>x.trim()).filter(Boolean); if(ord==='nv'){ n=q[0]; v=q.slice(1).join(' '); } else { n=q[q.length-1]; v=q.slice(0,-1).join(' '); } }
      else{ const w=s.split(/\s+/); if(w.length<2){ v=s; n=''; } else if(ord==='nv'){ n=w[0]; v=w.slice(1).join(' '); } else { n=w[w.length-1]; v=w.slice(0,-1).join(' '); } }
    }
    return {v:v||'',n:n||''};
  }
  /* angezeigt werden nur Vornamen; bei doppelten Vornamen kommt der Anfangsbuchstabe des Nachnamens dazu */
  function grpNames(){
    const o=grpOrder(), L=grpRaw().map(r=>splitName(r,o)).filter(x=>x.v), cnt={};
    L.forEach(x=>{ cnt[x.v]=(cnt[x.v]||0)+1; });
    return L.map(x=>cnt[x.v]>1&&x.n ? x.v+' '+x.n[0]+'.' : x.v);
  }
  function grpPool(){ const n=grpNames(); return n.length?n:Array.from({length:grpNums},(_,k)=>String(k+1)); }
  function rnd(n){ const b=new Uint32Array(1), lim=Math.floor(4294967296/n)*n; let x; do{ crypto.getRandomValues(b); x=b[0]; }while(x>=lim); return x%n; }
  function grpMix(){
    const p=grpPool().slice();
    for(let k=p.length-1;k>0;k--){ const j=rnd(k+1); [p[k],p[j]]=[p[j],p[k]]; }
    const g=Array.from({length:grpN},()=>[]);
    p.forEach((x,k)=>g[k%grpN].push(x));
    g.forEach(a=>a.sort((x,y)=>x.localeCompare(y,'de',{numeric:true})));
    grpState[grpN]={g,size:p.length};
    grpDraw();
  }
  function grpDraw(){
    const names=grpRaw().length>0;
    gq('#gn').textContent=grpN; gq('#gnum').textContent=grpNums;
    gq('#gnumwrap').style.display=names?'none':'';
    const s=grpState[grpN];
    if(!s||s.size!==grpPool().length){ grpMix(); return; }
    const body=gq('#gbody');
    body.style.setProperty('--gc', grpN<=2?grpN:grpN<=4?2:grpN<=6?3:4);
    const mx=Math.max(...s.g.map(a=>a.length));
    body.style.setProperty('--gf', (mx>8?1.6:mx>6?1.8:2)+'cqw');
    body.innerHTML=s.g.map((a,k)=>`<div class="gc" style="--gcol:${GRP_COL[k%GRP_COL.length]};animation-delay:${k*70}ms"><h4>Gruppe ${k+1}</h4><ul>${a.map(x=>'<li>'+x.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))+'</li>').join('')}</ul></div>`).join('');
  }
  function grpToggle(n){
    grpOpen=!grpOpen; grpEl.classList.toggle('on',grpOpen);
    if(grpOpen){ gq('#gpanel').classList.remove('on'); if(n) grpN=n; grpDraw(); } else stage.focus();
  }
  document.querySelectorAll('.grpbtn').forEach(b=>b.addEventListener('click',e=>{ e.stopPropagation(); grpToggle(+b.dataset.grp); }));
  gq('#gback').addEventListener('click',()=>grpToggle());
  gq('#gmix').addEventListener('click',grpMix);
  grpEl.querySelectorAll('[data-d]').forEach(b=>b.addEventListener('click',()=>{ grpN=Math.min(10,Math.max(2,grpN+(+b.dataset.d))); grpDraw(); }));
  grpEl.querySelectorAll('[data-nd]').forEach(b=>b.addEventListener('click',()=>{ grpNums=Math.min(40,Math.max(4,grpNums+(+b.dataset.nd))); grpState={}; grpDraw(); }));
  function grpPrev(){ const n=grpNames(); gq('#gprev').textContent=n.length?'Vorschau: '+n.slice(0,4).join(', ')+(n.length>4?' …':''):''; gq('#gcount').textContent=n.length?n.length+' Namen gespeichert':''; }
  gq('#glist').addEventListener('click',()=>{ const p=gq('#gpanel'); p.classList.toggle('on'); if(p.classList.contains('on')){ gq('#gtext').value=grpRaw().join('\n'); gq('#gord').value=grpOrder(); grpPrev(); } });
  gq('#gord').addEventListener('change',e=>{ try{ localStorage.setItem(GRP_ORD,e.target.value); }catch(x){} grpState={}; grpPrev(); grpDraw(); });
  function parseList(txt){ return txt.split(/\r?\n/).map(l=>l.trim()).filter(Boolean); }
  gq('#gsave').addEventListener('click',()=>{ const a=parseList(gq('#gtext').value); try{ localStorage.setItem(GRP_KEY2,JSON.stringify(a)); localStorage.removeItem(GRP_KEY); }catch(e){} grpState={}; gq('#gpanel').classList.remove('on'); grpDraw(); });
  gq('#gclear').addEventListener('click',()=>{ try{ localStorage.removeItem(GRP_KEY); localStorage.removeItem(GRP_KEY2); }catch(e){} gq('#gtext').value=''; grpState={}; gq('#gprev').textContent=''; gq('#gcount').textContent='Liste gelöscht'; grpDraw(); });
  gq('#gfilebtn').addEventListener('click',()=>gq('#gfile').click());
  gq('#gfile').addEventListener('change',e=>{ const f=e.target.files[0]; if(!f) return; const r=new FileReader(); r.onload=()=>{ gq('#gtext').value=parseList(String(r.result)).join('\n'); }; r.readAsText(f); });

