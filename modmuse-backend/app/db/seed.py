import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from openai import AsyncOpenAI

from app.db.session import Base, SessionLocal, engine
from app.db.models import (
    Game,
    Tag,
    Mod,
    ModTag,
    Dependency,
    Incompatibility,
)
from app.db.models import *

client = AsyncOpenAI()

# ======================================================
# MAIN SEED FUNCTION
# ======================================================

async def seed_data():
    print("🌱 Starting database seed...")

    async with engine.begin() as conn:
        # Wipe ALL tables (development only!)
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        # Creation (games, tags, mods, etc.)
        await create_games(session)
        await create_tags(session)
        await create_mods(session)
        await create_mod_tags(session)
        await create_dependencies(session)
        await create_incompatibilities(session)

        await session.commit()
        print("✔️ Base data inserted.")

        # Embeddings step
        await generate_mod_embeddings(session)
        await session.commit()

        print("🌱 Database fully seeded with embeddings!")


# ======================================================
# 1. GAMES
# ======================================================

async def create_games(session: AsyncSession):
    games = [
        Game(game_id=1, name="Skyrim", genre="RPG", engine="Creation Engine", platform="PC"),
        Game(game_id=2, name="Minecraft", genre="Sandbox", engine="Custom", platform="Java"),
        Game(game_id=3, name="Fallout 4", genre="RPG", engine="Creation Engine", platform="PC"),
    ]
    session.add_all(games)


# ======================================================
# 2. TAGS
# ======================================================

async def create_tags(session: AsyncSession):
    tags = [
        Tag(tag_id=1, name="survival"),
        Tag(tag_id=2, name="immersion"),
        Tag(tag_id=3, name="magic"),
        Tag(tag_id=4, name="overhaul"),
        Tag(tag_id=5, name="UI"),
        Tag(tag_id=6, name="graphics"),
        Tag(tag_id=7, name="performance"),
        Tag(tag_id=8, name="exploration"),
    ]
    session.add_all(tags)


# ======================================================
# 3. MODS
# ======================================================

async def create_mods(session: AsyncSession):
    mods = [
        # Skyrim
        Mod(mod_id=1, name="Frostfall", description="Hypothermia survival mechanics",
            source_url="https://www.nexusmods.com/skyrim/mods/11163", version="3.4.1", game_id=1),
        Mod(mod_id=2, name="Campfire", description="Camping system and resource management",
            source_url="https://www.nexusmods.com/skyrim/mods/64798", version="1.12", game_id=1),
        Mod(mod_id=3, name="iNeed", description="Adds hunger, thirst, and sleep requirements",
            source_url="https://www.nexusmods.com/skyrim/mods/51473", version="2.0", game_id=1),
        Mod(mod_id=4, name="Ordinator", description="Overhauls the perk system",
            source_url="https://www.nexusmods.com/skyrim/mods/68425", version="9.30", game_id=1),
        Mod(mod_id=5, name="Wet and Cold", description="Weather-based immersion effects",
            source_url="https://www.nexusmods.com/skyrim/mods/27563", version="2.2", game_id=1),
        Mod(mod_id=6, name="RASS", description="Breath, snow, wetness, and immersion visuals",
            source_url="https://www.nexusmods.com/skyrim/mods/103486", version="1.0", game_id=1),
        Mod(mod_id=7, name="SkyUI", description="Modernized UI with MCM menu",
            source_url="https://www.nexusmods.com/skyrim/mods/3863", version="5.2", game_id=1),
        Mod(mod_id=8, name="Hunterborn", description="Overhauls hunting, skinning, gathering",
            source_url="https://www.nexusmods.com/skyrim/mods/33201", version="1.6", game_id=1),

        # Minecraft
        Mod(mod_id=9, name="OptiFine", description="Performance + graphics enhancements",
            source_url="https://optifine.net/", version="HD U G9", game_id=2),
        Mod(mod_id=10, name="JEI", description="Recipe browser and item lookup",
            source_url="https://www.curseforge.com/minecraft/mc-mods/jei", version="12.0.0", game_id=2),
        Mod(mod_id=11, name="Biomes O’ Plenty", description="Adds 80+ new biomes",
            source_url="https://www.curseforge.com/minecraft/mc-mods/biomes-o-plenty", version="17.0.1", game_id=2),

        # Fallout 4
        Mod(mod_id=12, name="Sim Settlements", description="Dynamic settlement overhaul",
            source_url="https://www.nexusmods.com/fallout4/mods/21872", version="4.2.9", game_id=3),
        Mod(mod_id=13, name="Armorsmith Extended", description="Craft and customize armor fully",
            source_url="https://www.nexusmods.com/fallout4/mods/2228", version="4.6", game_id=3),
        Mod(mod_id=14, name="Vivid Fallout", description="Texture + graphics overhaul",
            source_url="https://www.nexusmods.com/fallout4/mods/25714", version="2.2", game_id=3),
    ]
    session.add_all(mods)


# ======================================================
# 4. MOD TAGS
# ======================================================

async def create_mod_tags(session: AsyncSession):
    mappings = [
        # Skyrim tags
        ModTag(mod_id=1, tag_id=1), ModTag(mod_id=1, tag_id=2),
        ModTag(mod_id=2, tag_id=1),
        ModTag(mod_id=3, tag_id=1),
        ModTag(mod_id=4, tag_id=3),
        ModTag(mod_id=5, tag_id=2),
        ModTag(mod_id=6, tag_id=2),
        ModTag(mod_id=7, tag_id=5),
        ModTag(mod_id=8, tag_id=1), ModTag(mod_id=8, tag_id=8),

        # Minecraft
        ModTag(mod_id=9, tag_id=7), ModTag(mod_id=9, tag_id=6),
        ModTag(mod_id=10, tag_id=5),
        ModTag(mod_id=11, tag_id=8),

        # Fallout 4
        ModTag(mod_id=12, tag_id=4),
        ModTag(mod_id=13, tag_id=4),
        ModTag(mod_id=14, tag_id=6),
    ]
    session.add_all(mappings)


# ======================================================
# 5. DEPENDENCIES
# ======================================================

async def create_dependencies(session: AsyncSession):
    session.add_all([
        Dependency(mod_id=1, depends_on_mod_id=2),  # Frostfall requires Campfire
    ])


# ======================================================
# 6. INCOMPATIBILITIES
# ======================================================

async def create_incompatibilities(session: AsyncSession):
    session.add_all([
        Incompatibility(mod_id_a=3, mod_id_b=4),  # iNeed conflicts with Ordinator
    ])


# ======================================================
# 7. GENERATE EMBEDDINGS (OPENAI)
# ======================================================

async def generate_mod_embeddings(session: AsyncSession):
    print("🧠 Generating embeddings for mods...")

    result = await session.execute(select(Mod))
    mods = result.scalars().all()

    for mod in mods:
        if mod.embedding is not None:
            print(f"  ➜ Skipping {mod.name} (already embedded)")
            continue

        text = f"{mod.name}: {mod.description or ''}"

        print(f"  ➜ Embedding: {mod.name}")

        try:
            response = await client.embeddings.create(
                model="text-embedding-3-small",
                input=text,
            )
            embedding = response.data[0].embedding
            mod.embedding = embedding # type: ignore[assignment]

        except Exception as e:
            print(f"❌ Failed embedding {mod.name}: {e}")
            continue

    print("✔️ Finished generating embeddings.")


# ======================================================
# ENTRY
# ======================================================

if __name__ == "__main__":
    asyncio.run(seed_data())
