  /* Mindmap: Excalidraw, lazy geladen, eine Fläche für Folie 4 und 5 */
  const MM_KEY='kluge-mindmap-v1';
  let mmOpen=false, mmApi=null, mmLoading=false;
  const mmEl=document.createElement('div');
  mmEl.id='mm';
  mmEl.innerHTML='<div class="mmhost"></div><div class="mmbar"><button class="zurueck">Zurück zur Folie (M)</button><button data-g="a">Spontan / Grundsätzlich</button><button data-g="b">Kleidung</button></div>';
  stage.appendChild(mmEl);
  ['click','mousedown','mouseup','pointerdown'].forEach(t=>mmEl.addEventListener(t,e=>e.stopPropagation()));
  const mmSeed=()=>ExcalidrawLib.convertToExcalidrawElements([
    {type:'text',id:'a-t1',x:-420,y:-200,text:'Spontan',fontSize:44,strokeColor:'#1f4f3a'},
    {type:'text',id:'a-t2',x:140,y:-200,text:'Grundsätzlich',fontSize:44,strokeColor:'#9a5a1a'},
    {type:'text',id:'a-t3',x:-420,y:-140,text:'nach Lust und Laune',fontSize:24,strokeColor:'#6b7280'},
    {type:'text',id:'a-t4',x:140,y:-140,text:'gilt für längere Zeit',fontSize:24,strokeColor:'#6b7280'},
    {type:'line',id:'a-l',x:0,y:-220,points:[[0,0],[0,640]],strokeWidth:3,strokeColor:'#9a9488'},
    {type:'ellipse',id:'b-e',x:2600,y:-70,width:380,height:150,label:{text:'Kleidung',fontSize:44},strokeColor:'#1f4f3a'}
  ]);
  function mmGo(g){
    if(!mmApi) return;
    const els=mmApi.getSceneElements().filter(e=>!e.isDeleted && (g==='b' ? e.x>=1500 : e.x<1500));
    mmApi.updateScene({appState:{zoom:{value:1}}});
    if(els.length) mmApi.scrollToContent(els,{fitToContent:false,animate:false});
  }
  function mmLoad(src){ return new Promise((ok,err)=>{ const x=document.createElement('script'); x.src=src; x.onload=ok; x.onerror=()=>err(new Error(src)); document.head.appendChild(x); }); }
  async function mmInit(g){
    if(mmLoading) return; mmLoading=true;
    const host=mmEl.querySelector('.mmhost');
    host.innerHTML='<div class="mmmsg">Zeichenfläche wird geladen ...</div>';
    try{
      window.EXCALIDRAW_ASSET_PATH='./_excalidraw/';
      window.process=window.process||{env:{IS_PREACT:'false'}};
      await mmLoad('_excalidraw/react.production.min.js');
      await mmLoad('_excalidraw/react-dom.production.min.js');
      await mmLoad('_excalidraw/excalidraw.production.min.js');
      let els=null;
      try{ const t=localStorage.getItem(MM_KEY); if(t) els=JSON.parse(t); }catch(e){}
      if(!els||!els.length) els=mmSeed();
      host.innerHTML='';
      let tm=null;
      const el=React.createElement(ExcalidrawLib.Excalidraw,{
        langCode:'de-DE',
        initialData:{elements:els, appState:{viewBackgroundColor:'#fffdf7', currentItemFontSize:36, zoom:{value:1}}},
        excalidrawAPI:api=>{ mmApi=api; setTimeout(()=>mmGo(g),150); },
        onChange:els2=>{ clearTimeout(tm); tm=setTimeout(()=>{ try{ localStorage.setItem(MM_KEY, JSON.stringify(els2.filter(e=>!e.isDeleted))); }catch(e){} },600); },
        UIOptions:{canvasActions:{loadScene:false, saveToActiveFile:false}}
      });
      ReactDOM.createRoot(host).render(el);
    }catch(e){
      host.innerHTML='<div class="mmmsg">Die Zeichenfläche konnte nicht geladen werden. Liegt der Ordner _excalidraw neben dieser Datei?</div>';
    }
    mmLoading=false;
  }
  function mmToggle(g){
    mmOpen=!mmOpen;
    mmEl.classList.toggle('on',mmOpen);
    if(mmOpen){
      g=g||(i===4?'b':'a');
      if(mmApi) mmGo(g); else mmInit(g);
    }else{
      stage.focus();
    }
  }
  document.querySelectorAll('.mmbtn').forEach(b=>b.addEventListener('click',e=>{ e.stopPropagation(); mmToggle(b.dataset.mm); }));
  mmEl.querySelector('.zurueck').addEventListener('click',()=>mmToggle());
  mmEl.querySelectorAll('[data-g]').forEach(b=>b.addEventListener('click',()=>mmGo(b.dataset.g)));

