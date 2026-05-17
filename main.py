print("SCRIPT LOADED")

from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os
import asyncio

# =========================================
# CONFIG
# =========================================

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")
TARGET_CHANNEL_ID = -1002363149346

client = TelegramClient(
    StringSession(SESSION),
    API_ID,
    API_HASH,
    connection_retries=-1,
    retry_delay=5,
    auto_reconnect=True
)

# =========================================
# CHANNELS
# =========================================

SOURCE_CHANNELS = [-1003837148064]  # список, не int

# =========================================
# КЕШ (антидубль)
# =========================================

recent_messages = set()

# =========================================
# ВИЗНАЧЕННЯ ТИПУ
# =========================================

def detect_attack_type(text: str):
    t = text.lower()

    if any(w in t for w in ["бпла", "герань", "шахед", "ударн"]):
        return "пуски ударних"

    if any(w in t for w in ["баліст", "ракета"]):
        return "балістика"

    return None

# =========================================
# ВИЗНАЧЕННЯ ЛОКАЦІЇ
# =========================================

def detect_location(text: str):
    t = text.lower()

    locations = {
        "навля": "навля",
        "цимбулова": "цимбулова",
        "приморськ": "приморськ-ахтарськ",
        "гвардій": "гвардійське",
        "міллер": "міллерово",
        "халіно": "халіно",
        "шатал": "шаталово",
        "чауда": "чауда",
        "донецьк": "донецьк",
        "орел": "орла",
        "брян": "брянська",
        "курсь": "курська",
        "крим": "криму",
        "луган": "луганська",
        "ліпець": "ліпецька",
        "воронеж": "воронежа",
        "таганрог": "таганрога",
        "бєлгород": "бєлгорода",
        "ростов": "ростовської області",
    }

    for key, value in locations.items():
        if key in t:
            return value

    return None

# =========================================
# ТРИГЕР ШАБЛОНУ
# =========================================

def get_template(text: str):
    attack_type = detect_attack_type(text)
    location = detect_location(text)

    if not attack_type or not location:
        return None

    if attack_type == "пуски ударних":
        return f"Пуски ударних БпЛА з району: {location}"

    if attack_type == "балістика":
        return f"Загроза балістики з {location}"

    return None

# =========================================
# HANDLER
# =========================================

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    text = event.raw_text
    print("RAW:", text)

    if not text:
        return

    if text in recent_messages:
        return

    recent_messages.add(text)
    if len(recent_messages) > 300:
        recent_messages.clear()

    template = get_template(text)

    if not template:
        print("[-] No template match")
        return

    try:
        await client.send_message(TARGET_CHANNEL_ID, template)
        print("[+] SENT:", template)
    except Exception as e:
        print("[ERROR SEND]:", e)

# =========================================
# START
# =========================================

async def main():
    print("BEFORE START")
    await client.start()
    print("BOT STARTED")
    await client.run_until_disconnected()

asyncio.run(main())
