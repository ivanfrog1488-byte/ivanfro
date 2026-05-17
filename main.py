# =========================================
# TELEGRAM AUTO TEMPLATE BOT (STABLE VERSION)
# =========================================

print("SCRIPT LOADED")

from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os

# =========================================
# CONFIG
# =========================================

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

client = TelegramClient(
    StringSession(SESSION),
    API_ID,
    API_HASH
)

# =========================================
# CHANNELS
# =========================================

SOURCE_CHANNELS = -1003837148064   # твій канал-джерело

TARGET_CHANNEL = "boyovyy_sokil"   # або заміни на -100ID (краще)

# =========================================
# КЕШ (антидубль)
# =========================================

recent_messages = set()

# =========================================
# ВИЗНАЧЕННЯ ТИПУ (ГНУЧКЕ)
# =========================================

def detect_attack_type(text: str):
    t = text.lower()

    # ударні БпЛА
    if (
        "бпла" in t or
        "герань" in t or
        "шахед" in t or
        "ударн" in t
    ):
        return "пуски ударних"

    # балістика
    if (
        "баліст" in t or
        "ракета" in t
    ):
        return "балістика"

    return None

# =========================================
# ВИЗНАЧЕННЯ ЛОКАЦІЇ (ГНУЧКЕ)
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

    for key in locations:
        if key in t:
            return locations[key]

    return None

# =========================================
# ТРИГЕР ШАБЛОНУ
# =========================================

def get_template(text: str):

    attack_type = detect_attack_type(text)
    location = detect_location(text)

    if not attack_type or not location:
        return None

    # нормалізація (щоб з великої букви)
    location = location.strip()

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

    # антидубль
    if text in recent_messages:
        return

    recent_messages.add(text)
    if len(recent_messages) > 300:
        recent_messages.clear()

    template = get_template(text)

    if not template:
        return

    try:
        await client.send_message(TARGET_CHANNEL, template)
        print("[+] SENT:", template)

    except Exception as e:
        print("[ERROR SEND]:", e)

# =========================================
# START
# =========================================

print("BEFORE START")
client.start()
print("BOT STARTED")

client.run_until_disconnected()
