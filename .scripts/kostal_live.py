"""
Kostal Wechselrichter – Live-Daten Abruf
IP: 192.168.178.48
Verwendung: python3 .scripts/kostal_live.py
"""

import asyncio
import aiohttp
from pykoplenti import ApiClient
from datetime import datetime
from pathlib import Path

KOSTAL_IP = "192.168.178.48"

# Passwort außerhalb des Vaults gespeichert (nicht in iCloud)
_pw_file = Path.home() / ".config" / "kostal" / "password"
KOSTAL_PASSWORD = _pw_file.read_text().strip() if _pw_file.exists() else ""

def get_val(data, key, decimals=2):
    for item in data:
        if item["id"] == key:
            return round(item["value"], decimals)
    return None

async def fetch_kostal_data():
    async with aiohttp.ClientSession() as session:
        client = ApiClient(session, KOSTAL_IP)
        await client.login(key=KOSTAL_PASSWORD)
        token = client.session_id

        modules = [
            "devices:local",
            "devices:local:battery",
            "devices:local:pv1",
            "devices:local:pv2",
            "devices:local:powermeter"
        ]

        results = {}
        for mod in modules:
            async with session.get(
                f"http://{KOSTAL_IP}/api/v1/processdata/{mod}",
                headers={"authorization": f"Session {token}"}
            ) as resp:
                data = await resp.json()
                results[mod] = data[0]["processdata"]

        loc  = results["devices:local"]
        bat  = results["devices:local:battery"]
        pv1  = results["devices:local:pv1"]
        pv2  = results["devices:local:pv2"]
        meter = results["devices:local:powermeter"]

        now = datetime.now().strftime("%d.%m.%Y %H:%M")

        pv_str1  = get_val(pv1, "P")
        pv_str2  = get_val(pv2, "P")
        pv_total = round((pv_str1 or 0) + (pv_str2 or 0), 1)
        home_p   = get_val(loc, "Home_P")
        home_pv  = get_val(loc, "HomePv_P")
        home_bat = get_val(loc, "HomeBat_P")
        home_grid= get_val(loc, "HomeGrid_P")
        bat_soc  = get_val(bat, "SoC", 0)
        bat_p    = get_val(bat, "P")
        bat_cyc  = get_val(bat, "Cycles", 0)
        grid_p   = get_val(loc, "Grid_P")
        exp_e    = round((get_val(meter, "Exp_E") or 0) / 1000, 2)
        imp_e    = round((get_val(meter, "Imp_E") or 0) / 1000, 2)

        grid_str = f"Einspeisung {abs(grid_p)} W" if grid_p and grid_p < 0 else f"Bezug {grid_p} W"

        print(f"{'='*47}")
        print(f"  🌞 KOSTAL Live-Daten  –  {now}")
        print(f"{'='*47}")
        print(f"\n☀️  PV-Produktion")
        print(f"  Gesamt:          {pv_total} W")
        print(f"  String 1:        {pv_str1} W")
        print(f"  String 2:        {pv_str2} W")
        print(f"\n🏠 Hausverbrauch")
        print(f"  Gesamt:          {home_p} W")
        print(f"  Davon PV:        {home_pv} W")
        print(f"  Davon Batterie:  {home_bat} W")
        print(f"  Davon Netz:      {home_grid} W")
        print(f"\n🔋 Batterie")
        print(f"  Ladestand:       {bat_soc} %")
        print(f"  Leistung:        {bat_p} W")
        print(f"  Ladezyklen:      {bat_cyc}")
        print(f"\n⚡ Netz")
        print(f"  Aktuell:         {grid_str}")
        print(f"  Einspeisung Σ:   {exp_e} kWh")
        print(f"  Bezug Σ:         {imp_e} kWh")
        print(f"{'='*47}")

        return {
            "timestamp": now,
            "pv_total_w": pv_total,
            "pv_str1_w": pv_str1,
            "pv_str2_w": pv_str2,
            "home_p_w": home_p,
            "home_pv_w": home_pv,
            "home_bat_w": home_bat,
            "home_grid_w": home_grid,
            "bat_soc_pct": bat_soc,
            "bat_p_w": bat_p,
            "bat_cycles": bat_cyc,
            "grid_p_w": grid_p,
            "export_kwh": exp_e,
            "import_kwh": imp_e,
        }

if __name__ == "__main__":
    asyncio.run(fetch_kostal_data())
