import asyncio, sys, json
from playwright.async_api import async_playwright
APP="file:///Users/oskarklein/Documents/Obsidian%20Claude/Second%20Brain%20Claude/04%20Ressourcen/Sitzplan/Sitzplan.html"
OUT="/tmp/sp/shots/"
import os; os.makedirs(OUT,exist_ok=True)
NAMES="""Ahorn	Lena	w
Birke	Elias	m
Buche	Mia	w
Eibe	Noah	m
Erle	Sophie	w
Esche	Ben	m
Fichte	Emma	w
Hasel	Luca	m
Kiefer	Hannah	w
Linde	Elias	m
Pappel	Clara	w
Tanne	Jonas	m
Ulme	Lea	w
Weide	Finn	m
Zeder	Marie	w
Akazie	Paul	m
Bambus	Nele	w
Dattel	Leon	m
Eukalyptus	Ida	w
Farn	Felix	m
Ginster	Anna	w
Holunder	Tim	m
Jasmin	Ella	w
Kastanie	David	m"""
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    ctx=await b.new_context(viewport={"width":1400,"height":980},device_scale_factor=1.5,locale="de-DE")
    pg=await ctx.new_page()
    await pg.goto(APP); await pg.wait_for_timeout(500)
    # JS-Helfer für Markierungen
    await pg.evaluate("""()=>{
      window.__clr=()=>document.querySelectorAll('.__ring').forEach(e=>e.remove());
      window.__ring=(sel,n,pad=4,i=0)=>{
        const el=typeof sel==='string'?document.querySelectorAll(sel)[i]:sel; if(!el) {console.warn('kein Element',sel);return}
        const r=el.getBoundingClientRect(); const host=el.closest('dialog[open]')||document.body;
        const d=document.createElement('div'); d.className='__ring';
        d.style.cssText=`position:fixed;z-index:99999;pointer-events:none;left:${r.left-pad}px;top:${r.top-pad}px;width:${r.width+2*pad}px;height:${r.height+2*pad}px;border:2.5px solid #ff9500;border-radius:10px;box-shadow:0 0 0 3px rgba(255,149,0,.18)`;
        if(n){const s=document.createElement('span');s.textContent=n;s.style.cssText='position:absolute;left:-12px;top:-12px;min-width:22px;height:22px;border-radius:11px;background:#ff9500;color:#fff;font:700 13px/22px -apple-system,Helvetica;text-align:center;padding:0 4px;box-shadow:0 1px 3px rgba(0,0,0,.3)';d.appendChild(s)}
        host.appendChild(d);
      }}""")
    async def shot(name,clip=None,sel=None,pad=0):
      path=OUT+name+".png"
      if sel:
        sels=sel if isinstance(sel,list) else [sel]
        await pg.evaluate("(s)=>document.querySelector(s).scrollIntoView({block:'nearest'})",sels[0])
        await pg.wait_for_timeout(150)
        rs=[await pg.evaluate("(s)=>{const e=document.querySelector(s).getBoundingClientRect();return [e.left,e.top,e.right,e.bottom]}",x) for x in sels]
        x0=min(r[0] for r in rs);y0=min(r[1] for r in rs);x1=max(r[2] for r in rs);y1=max(r[3] for r in rs)
        clip={"x":max(0,x0-pad),"y":max(0,y0-pad),"width":min(1400,x1-x0+2*pad),"height":min(1300,y1-y0+2*pad)}
      await pg.screenshot(path=path,clip=clip) if clip else await pg.screenshot(path=path)
      await pg.evaluate("__clr()")
    # 1 Willkommen
    await pg.wait_for_selector("#dlgWelcome[open]")
    await pg.evaluate("__ring('.wtile',1,4,0);__ring('.wtile',2,4,1)")
    await shot("willkommen",sel="#dlgWelcome",pad=8)
    await pg.click(".wtile[value=full]"); await pg.wait_for_timeout(300)
    # 2 Import
    await pg.click("#bImport"); await pg.wait_for_selector("#dlgImport[open]")
    await pg.fill("#impText","Nachname\tVorname\tGeschlecht\n"+NAMES)
    await pg.wait_for_timeout(500)
    await pg.evaluate("__ring('#impFileBtn',1);__ring('#impText',2,3);__ring('#impOk',3)")
    await pg.evaluate("document.querySelector('#impText').scrollTop=0")
    await shot("import",sel="#dlgImport",pad=8)
    await pg.screenshot(path=OUT+"_dbg_import.png")
    await pg.click("#impOk"); await pg.wait_for_timeout(400)
    # 3 Anordnung
    await pg.set_viewport_size({"width":1400,"height":1300})
    await pg.click("#bTemplate"); await pg.wait_for_selector("#dlgTpl[open]")
    await pg.fill("#tplN","24")
    await pg.dispatch_event("#tplN","input")
    await pg.click("label.tile:has(input[value=gang])"); await pg.wait_for_timeout(300)
    await pg.evaluate("document.querySelector('#dlgTpl').scrollTop=0;document.querySelector('#dlgTpl .dlg').scrollTop=0")
    await pg.wait_for_timeout(200)
    await pg.evaluate("__ring('#tplN',1);__ring('label.tile:has(input[value=gang])',2);__ring('#aisleFields',3,2)")
    await shot("anordnung",sel="#dlgTpl",pad=8)
    await pg.click("#dlgTpl button.primary"); await pg.wait_for_timeout(500)
    await pg.set_viewport_size({"width":1400,"height":980})
    # 4 Raum-Dialog
    await pg.click("#bRoom"); await pg.wait_for_selector("#dlgRoom[open]")
    await pg.fill("#rKl","7c"); await pg.fill("#rNr","204"); await pg.fill("#rFach","Physik")
    await pg.evaluate("__ring('#rKl',1);__ring('#rW',2);__ring('#rWin',3)")
    await shot("raum",sel="#dlgRoom",pad=8)
    await pg.click("#dlgRoom button.primary"); await pg.wait_for_timeout(400)
    # 5 Verteilen
    await pg.evaluate("document.querySelector('#toast').style.display='none'")
    await pg.evaluate("document.querySelector('#dWish').closest('section').id='secVert';document.querySelector('#cOn').closest('section').id='secFarbe';document.querySelector('#bImport').closest('section').id='secKlasse'")
    await pg.click("#dRandom"); await pg.wait_for_timeout(800)
    await pg.evaluate("__ring('.side',1,-3);__ring('header.bar',2,-3);__ring('.canvasbar',3,0);__ring('#room',4,-3)")
    await shot("uebersicht")
    await pg.evaluate("__ring('#bAddSingle',1);__ring('#bAddDouble',2);__ring('#bTemplate',3);__ring('#bRotate',4);__ring('#bRoom',5);__ring('#bPrint',6);__ring('#bPdf',7);__ring('#bMore',8)")
    await shot("werkzeugleiste",clip={"x":0,"y":0,"width":1400,"height":50})
    await pg.evaluate("__ring('#mTische',1);__ring('#mSchueler',2);__ring('#vPult',3,3);__ring('#vKlasse',3,3)")
    await shot("modus",clip={"x":290,"y":58,"width":1010,"height":50})
    await pg.evaluate("__ring('#dWish',1);__ring('#dRandom',2);__ring('#dRest',3);__ring('#dAlpha',4);__ring('#dClear',5)")
    await shot("verteilen",sel="#secVert",pad=8)
    await pg.evaluate("__ring('#cOn',1);__ring('.colors',2);__ring('#bGender',3)")
    await shot("farben",sel="#secFarbe",pad=8)
    await pg.click("#bGender"); await pg.wait_for_selector("#dlgGender[open]")
        await shot("geschlecht",sel="#dlgGender",pad=8)
    await pg.click("#dlgGender button.primary"); await pg.wait_for_timeout(300)
    # Lasso
    rb=await pg.evaluate("(()=>{const r=document.querySelector('#room').getBoundingClientRect();return [r.left,r.top,r.width,r.height]})()")
    nm=await pg.evaluate("[...document.querySelectorAll('#room .name')].slice(0,12).map(e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom,e.textContent.trim()]})")
    print(nm[:4])
    # 6 Wünsche
    await pg.click("#bWishes"); await pg.wait_for_selector("#dlgWish[open]"); await pg.wait_for_timeout(400)
    async def wish_for(i,wishes,rowc=None):
      await pg.locator("#wList .wl").nth(i).click()
      for w in wishes: await pg.locator("#wEdit .sbox [data-wish]").nth(w).click()
      if rowc: await pg.locator(f"#wEdit .sbox [data-row='{rowc}']").click()
    # Liste alphabetisch nach Vorname: 0 Akazie? -> egal, deterministisch
    for i,(ws,rc) in enumerate([([3,7],None),([0,5],None),([9],None),([2,12],None),([15],None),([4,6],None),([20,21],None),([8,11],None),([1],None)]):
      await wish_for(i+3,ws,rc)
    # Hauptschüler für Screenshot: Anna (Index 1)
    await pg.locator("#wList .wl").nth(1).click()
    await pg.locator("#wEdit .sbox [data-wish]").nth(4).click()
    await pg.locator("#wEdit .sbox [data-wish]").nth(10).click()
    await pg.locator("#wEdit .sbox [data-row='1']").click()
    t=pg.locator("#wEdit .tbox [data-trule]")
    await t.nth(7).click(); await t.nth(7).click()
    await pg.locator("#wEdit .tbox [data-rowmust]").first.click()
    await pg.wait_for_timeout(300)
    await pg.evaluate("__ring('#wList',1,3);__ring('#wEdit .sbox',2,4);__ring('#wEdit .tbox',3,4)")
    await shot("wuensche",sel="#dlgWish",pad=8)
    await pg.click("#dlgWish button.primary"); await pg.wait_for_timeout(500)
    # 7 Regeln + Verteilen mit Wünschen
    await pg.check("[data-mix=noSingle]"); await pg.check("[data-mix=noLone]")
    await pg.click("#dWish"); await pg.wait_for_timeout(1500)
    await pg.evaluate("document.querySelector('#toast').style.display='none'")
    await pg.evaluate("document.querySelector('#secWish').id='secWish'; __ring('#secWish',1,3);__ring('#secRules',2,3)")
    await shot("regeln",sel=["#secWish","#secRules"],pad=8)
    await pg.screenshot(path=OUT+"_dbg_main2.png")
    await pg.evaluate("__ring('#room',1,-3)")
    await shot("wuensche-plan",sel="#room",pad=6)
    # 8 Tische stellen
    await pg.click("#mTische"); await pg.wait_for_timeout(300)
    cls=await pg.evaluate("[...new Set([...document.querySelectorAll('#room *')].map(e=>e.className&&e.className.baseVal===undefined?e.className:''))].filter(Boolean).slice(0,30)")
    print(cls)
    d=await pg.evaluate("(()=>{const e=document.querySelector('#room .desk.t-double');if(!e)return null;const r=e.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()")
    print("desk",d)
    if d:
      await pg.mouse.click(d[0],d[1]); await pg.wait_for_timeout(300)
    await pg.evaluate("__ring('#bRotate',2);__ring('#bRemove',3);__ring('#mTische',1)")
    await shot("tische")
    await pg.keyboard.press("Escape")
    # 9 Schüler setzen + Lasso
    await pg.click("#mSchueler"); await pg.wait_for_timeout(300)
    nm=await pg.evaluate("[...document.querySelectorAll('#room .name')].map(e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]})")
    top=min(n[1] for n in nm); 
    row1=[n for n in nm if abs(n[1]-top)<5]; rows2=[n for n in nm if n[1]<top+170]
    x0=min(n[0] for n in rows2)-12; x1=sorted(n[2] for n in rows2)[len(rows2)//2-1]+4
    await pg.mouse.move(x0,top-25); await pg.mouse.down(); await pg.mouse.move((x0+x1)/2,top+60,steps=8); await pg.mouse.move(x1,top+95,steps=8)
    await pg.wait_for_timeout(250)
    await pg.screenshot(path=OUT+"_dbg_lasso.png")
    await shot("lasso",sel="#room",pad=6)
    await pg.mouse.up(); await pg.wait_for_timeout(300)
    await pg.keyboard.press("Escape")
    # 10 Varianten + Vergleich
    await pg.click("[data-vadd]"); await pg.wait_for_timeout(400)
    await pg.evaluate("document.querySelector('#toast').style.display='none'")
    await pg.click("#dRandom"); await pg.wait_for_timeout(600)
    await pg.evaluate("document.querySelector('#toast').style.display='none'")
    await pg.click("#bCompare"); await pg.wait_for_timeout(600)
    await pg.evaluate("__ring('#varTabs',1,3);__ring('#bCompare',2);__ring('#cmpPanel',3,-3)")
    await shot("vergleich")
    await pg.click("#cmpClose")
    # 11 Wünsche ausblenden
    await pg.click("#bDiscreet"); await pg.wait_for_timeout(400)
    await pg.evaluate("__ring('#bDiscreet',1)")
    await shot("ausblenden")
    await pg.click("#bDiscreet"); await pg.wait_for_timeout(300)
    # Lehrer-/Schülersicht
    await pg.click("#vKlasse"); await pg.wait_for_timeout(400)
    await pg.evaluate("__ring('#vPult',1,3);__ring('#vKlasse',2,3)")
    await shot("sicht",clip={"x":0,"y":0,"width":1400,"height":980})
    await pg.click("#vPult"); await pg.wait_for_timeout(300)
    # 12 Menü
    await pg.click("#bMore"); await pg.wait_for_timeout(300)
    await pg.evaluate("__ring('#bExport',1);__ring('#bImportBackup',2);__ring('[data-lvl=simple]',3)")
    await shot("menue",clip={"x":900,"y":0,"width":500,"height":420})
    await pg.keyboard.press("Escape")
    await pg.mouse.click(700,25)
    # 13 Einfach
    await pg.click("#bMore"); await pg.click("[data-lvl=simple]"); await pg.wait_for_timeout(500)
    await pg.evaluate("document.querySelector('#toast').style.display='none'")
    await shot("einfach")
    await pg.click("#bMore"); await pg.click("[data-lvl=full]"); await pg.wait_for_timeout(400)
    # 14 Tipps
    await pg.evaluate("document.querySelector('.tipsbox').open=true")
    await shot("tipps",sel=".side-foot",pad=6)
    await pg.evaluate("document.querySelector('.tipsbox').open=false")
    # 15 Druckansicht
    await pg.emulate_media(media="print"); await pg.wait_for_timeout(400)
    await pg.pdf(path="/tmp/sp/druck.pdf",width="297mm",height="210mm",prefer_css_page_size=True,print_background=True)
    await pg.emulate_media(media="screen")
    await b.close()
asyncio.run(main())
