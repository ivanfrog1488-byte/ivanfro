# =========================================
# TELEGRAM AUTO TEMPLATE BOT (FIXED)
# =========================================
print("SCRIPT LOADED")

from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os

# =========================================
# API
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
# КАНАЛИ
# =========================================

SOURCE_CHANNELS = [ "strategicontrol"]

TARGET_CHANNEL = ["boyovyy_sokil"]

# =========================================
# ШАБЛОНИ (ВСЕ В LOWERCASE КЛЮЧАХ)
# =========================================

TEMPLATES = {

    "пуски ударних": {

        "навля": "Пуски ударних БпЛА з локації: Навля",
        "цимбулова": "Пуски ударних БпЛА з локації: Цимбулова",
        "приморськ-ахтарськ": "Пуски ударних БпЛА з локації: Приморськ-Ахтарськ",
        "гвардійське": "Пуски ударних БпЛА з локації: Гвардійське",
        "міллерово": "Пуски ударних БпЛА з локації: Міллерово",
        "халіно": "Пуски ударних БпЛА з локації: Халіно",
        "шаталово": "Пуски ударних БпЛА з локації: Шаталово",
        "чауда": "Пуски ударних БпЛА з локації: Чауда",
        "донецьк": "Пуски ударних БпЛА з локації: Донецьк",
        "орла": "Пуски ударних БпЛА з локації: Орла"

    },

    "балістика": {

        "курська": "Загроза балістики з Курської області",
        "брянська": "Загроза балістики з Брянської області",
        "криму": "Загроза балістики з Криму",
        "луганська": "Загроза балістики з Луганська",
        "ліпецька": "Загроза балістики з Ліпецька",
        "воронежа": "Загроза балістики з Воронежа",
        "таганрога": "Загроза балістики з Таганрога",
        "бєлгорода": "Загроза балістики з Бєлгорода",
        "ростовської області": "Загроза балістики з Ростовської області"

    }
}

# =========================================
# КЕШ
# =========================================

recent_messages = set()

# =========================================
# ВИЗНАЧЕННЯ ТИПУ
# =========================================

def detect_attack_type(text: str):

    text = text.lower()

    if "пуски ударних" in text:
        return "пуски ударних"

    if "баліст" in text:
        return "балістика"

    return None

# =========================================
# ВИЗНАЧЕННЯ ЛОКАЦІЇ
# =========================================

def detect_location(text: str):

    text = text.lower()

    locations = [
        "навля",
        "цимбулова",
        "приморськ-ахтарськ",
        "гвардійське",
        "міллерово",
        "халіно",
        "шаталово",
        "чауда",
        "донецьк",
        "орла",
        "курська",
        "брянська",
        "криму",
        "луганська",
        "ліпецька",
        "воронежа",
        "таганрога",
        "бєлгорода",
        "ростовської області"
    ]

    text_lower = text.lower()

    for loc in locations:
        if loc in text_lower:
            return loc

    return None

# =========================================
# ОТРИМАННЯ ШАБЛОНУ
# =========================================

def get_template(text: str):

    attack_type = detect_attack_type(text)
    location = detect_location(text)

    if not attack_type or not location:
        return None

    return TEMPLATES.get(attack_type, {}).get(location)

# =========================================
# ОБРОБКА ПОВІДОМЛЕНЬ
# =========================================

@client.on(events.NewMessage())
async def handler(event):
    print(event.chat_id)
    print(event.raw_text)

    try:

        text = event.raw_text

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

        await client.send_message(
            TARGET_CHANNEL,
            template
        )

        print(f"[+] SENT: {text}")

    except Exception as e:
        print(f"[ERROR] {e}")

# =========================================
# START
# =========================================


print("BEFORE START")
client.start()
client.run_until_disconnected()
print("BOT STARTED")
