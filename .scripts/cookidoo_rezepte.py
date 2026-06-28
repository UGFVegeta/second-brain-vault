#!/usr/bin/env python3
"""
Cookidoo Rezept-Browser für Claudian
Zeigt alle Rezepte aus Julias Cookidoo-Account an.
Credentials: ~/.config/claude-cookidoo/cookidoo.env
"""

import asyncio
import aiohttp
import ssl
import certifi
import json
import sys
from dotenv import dotenv_values
from cookidoo_api import Cookidoo, CookidooConfig, CookidooLocalizationConfig

CREDS_PATH = "/Users/oskarklein/.config/claude-cookidoo/cookidoo.env"


def format_time(seconds: int) -> str:
    if not seconds:
        return "?"
    mins = seconds // 60
    if mins < 60:
        return f"{mins} Min"
    h = mins // 60
    m = mins % 60
    return f"{h}h {m}min" if m else f"{h}h"


async def get_all_recipes(mode: str = "list") -> dict:
    creds = dotenv_values(CREDS_PATH)
    loc = CookidooLocalizationConfig(
        country_code="de",
        language="de-DE",
        url="https://cookidoo.de/foundation/de-DE"
    )
    cfg = CookidooConfig(
        email=creds["EMAIL"],
        password=creds["PASSWORD"],
        localization=loc
    )
    ssl_ctx = ssl.create_default_context(cafile=certifi.where())
    connector = aiohttp.TCPConnector(ssl=ssl_ctx)

    async with aiohttp.ClientSession(connector=connector) as session:
        c = Cookidoo(session, cfg)
        await c.login()

        result = {"collections": [], "calendar": [], "shopping": []}

        # Sammlungen (Kochbücher)
        collections = await c.get_managed_collections()
        for col in collections:
            col_data = {
                "name": col.name,
                "id": col.id,
                "recipes": []
            }
            if hasattr(col, "chapters") and col.chapters:
                for chapter in col.chapters:
                    for recipe in chapter.recipes:
                        col_data["recipes"].append({
                            "id": recipe.id,
                            "name": recipe.name,
                            "time": format_time(recipe.total_time),
                            "collection": col.name
                        })
            result["collections"].append(col_data)

        # Einkaufsliste
        shopping = await c.get_shopping_list_recipes()
        for r in shopping:
            result["shopping"].append({
                "id": r.id,
                "name": r.name,
                "time": format_time(getattr(r, "total_time", 0))
            })

        return result


def print_all_recipes():
    data = asyncio.run(get_all_recipes())

    total = 0
    for col in data["collections"]:
        count = len(col["recipes"])
        total += count
        print(f"\n📚 {col['name']} ({count} Rezepte)")
        print("-" * 50)
        for r in col["recipes"]:
            print(f"  [{r['id']}] {r['name']} — {r['time']}")

    if data["shopping"]:
        print(f"\n🛒 Auf der Einkaufsliste ({len(data['shopping'])} Rezepte)")
        print("-" * 50)
        for r in data["shopping"]:
            print(f"  [{r['id']}] {r['name']} — {r['time']}")

    print(f"\n✅ Gesamt: {total} Rezepte in {len(data['collections'])} Sammlungen")


def export_json():
    data = asyncio.run(get_all_recipes())
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if "--json" in sys.argv:
        export_json()
    else:
        print_all_recipes()
