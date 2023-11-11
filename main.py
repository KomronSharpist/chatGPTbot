import asyncio
import json
import logging
import os
from collections import defaultdict
from datetime import datetime, date, timedelta, time, timezone
import openai
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ChatMemberStatus
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot, types

logging.basicConfig(level=logging.INFO)
# bot = Bot(token="5701012090:AAGRTr0XVls7yrfcyX1XaP1btLV4D9mWYjY")
bot = Bot(token="6440053728:AAFYsc0PcAicgsEOyYQysWi81ig7yYVG2WQ")
dp = Dispatcher()
api_keys = {"Komronapi": "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"}
api_names_iterator = iter(api_keys.keys())
api_add_session = {}
api_control_session = {}
chanel_add_session = {}
chanel_control_session = {}
admin_control_session = {}
admin_add_session = {}
chat_sessions = {}
admin_sessions = {}
owner_sessions = {}
user_reload_messages = {}
send_message_session = {}
inline_keyboard_session = {}
add_inline_keyboard_session = {}
logging.basicConfig(level=logging.INFO)
admin_userIds = {1052097431: "𝙺𝚘𝚖𝚛𝚘𝚗", 1232328054: "Cloud"}
today = datetime.now().date()
ownerId = [1232328054, 1052097431]
user_request_counts = defaultdict(int)
user_last_request = {}
reklam = ""
reklamBuilder = InlineKeyboardBuilder()
video_file_id = 0
chat_id = 0
user_states = {}
channel_usernames = []
sended_users = []
unsended_users = []

try:
    with open('all_users.json', 'r') as file:
        all_users = json.load(file)
except FileNotFoundError:
    all_users = []

try:
    with open('inactive_users.json', 'r') as file:
        inactive_users = json.load(file)
except FileNotFoundError:
    inactive_users = []

try:
    with open('active_users.json', 'r') as file:
        active_users = json.load(file)
except FileNotFoundError:
    active_users = []


try:
    with open('today_active_users.json', 'r') as file:
        today_active_users = json.load(file)
except FileNotFoundError:
    today_active_users = []


try:
    with open('today_logined_users.json', 'r') as file:
        today_logined_users = json.load(file)
except FileNotFoundError:
    today_logined_users = []



async def is_daily_limit_exceeded(user_id):
    today = date.today()
    if user_id in user_last_request and user_last_request[user_id] == today:
        if user_request_counts[user_id] >= 30:
            return True
    else:
        user_request_counts[user_id] = 0
        user_last_request[user_id] = today
        return False

async def increment_request_count(user_id):
    user_request_counts[user_id] += 1

async def get_current_api_key():
    if len(api_keys) > 1:
        current_api_name = next(api_names_iterator)
        return api_keys[current_api_name]
    else:
        return next(iter(api_keys.values()))
async def is_subscribed(user_id, channel_username):
    try:
        member = await bot.get_chat_member(channel_username, user_id)
        desired_statuses = {
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.CREATOR,
            ChatMemberStatus.ADMINISTRATOR,
        }
        if member.status in desired_statuses:
            return True
    except Exception as e:
        return False
async def check_user_reachability(user_id):
    try:
        send_message_session = await bot.send_message(chat_id=user_id,text="Botni block qilmaganingiz tekshirilmoqda, bu habarga etibor bermang. Tushunganingiz uchun raxmat 😇")
        await bot.delete_message(user_id, send_message_session.message_id)
    except Exception as e:
        active_users.remove(user_id)
        inactive_users.append(user_id)
        with open('inactive_users.json', 'w') as file:
            json.dump(inactive_users, file)
        with open('active_users.json', 'w') as file:
            json.dump(active_users, file)
async def periodic_user_check():
    while True:
        now_utc = datetime.now(timezone.utc)
        utc_plus_5 = timedelta(hours=5)
        now = now_utc + utc_plus_5
        next_midnight = datetime.combine(now.date() + timedelta(days=1), time(0, 0), timezone.utc)
        time_until_midnight = (next_midnight - now).total_seconds()

        await asyncio.sleep(time_until_midnight)

        today_active_users.clear()
        today_logined_users.clear()
        with open('today_logined_users.json', 'w') as file:
            json.dump(today_logined_users, file)
        with open('today_active_users.json', 'w') as file:
            json.dump(today_active_users, file)
def get_duplicates():
    seen = set()
    duplicates = set()
    for item in today_active_users:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    if user_id in user_states.keys():
        user_states[user_id]['awaiting_response'] = False
    else:
        user_states[user_id] = {'awaiting_response': False}
    channel_unsubscribed = []
    if user_id in api_control_session:
        del api_control_session[user_id]
    if user_id in api_add_session:
        del api_add_session[user_id]

    if user_id in admin_control_session:
        del admin_control_session[user_id]
    if user_id in admin_add_session:
        del admin_add_session[user_id]

    if user_id in chanel_control_session:
        del chanel_control_session[user_id]
    if user_id in chanel_add_session:
        del chanel_add_session[user_id]

    for channel_username in channel_usernames:
        if await is_subscribed(user_id, channel_username):
            continue
        else:
            channel_unsubscribed.append(channel_username)
    builder = InlineKeyboardBuilder()
    for channel in channel_unsubscribed:
        builder.add(types.InlineKeyboardButton(text=f"{channel}", url=f"https://t.me/{channel[1:]}"))
        builder.adjust(1, 1)
    if channel_unsubscribed:
        builder.add(types.InlineKeyboardButton(text=f"Tekshirish ✅", callback_data="checkSubscription"))
        builder.adjust(1, 1)
        await message.answer("• Botdan foydalanish uchun avval kanalga obuna bo’ling va <b>Tekshirish</b> tugmasini bosing! \n\n @TexnoAI - sun'iy intellektlar va texnologiyalar haqida eng so'nggi yangiliklarni berib boruvchi kanal",
                             reply_markup=builder.as_markup(), parse_mode="HTML")
        return
    else:
        keyboard = types.ReplyKeyboardRemove()
        await message.answer("<b>Salom! 👋\n\nMen istalgan mavzu yoki vazifalar bo'yicha ma'lumot va savolingizga javob topishda yordam beradigan chatbotman. Foydalanish uchun esa shunchaki savolni yozishingiz kifoya.\n\nChatbot nimalar qiloladi?</b>\n1. Savolga javob berish va matnni barcha tillarda tarjima qilish;\n2. Istalgan fanlarga oid informatsiyalar ba'zasi;\n3. Matematik misol va masalalarni yechish;\n4. Kod yozib, uni tahrirlash va texnologiya, dasturlash tillari, algoritmlar haqida ma'lumot berish;\n5. She'rlar, hikoyalar, insholar va ijodiy asarlar yozib berish;\n6. Sog'liq-salomatlik, to'g'ri ovqatlanish va fitnes bo'yicha to'g'ri ma'lumot berish.\n\n<b>Bot savollarga qanchalik tez javob beradi?</b>\nBir nech soniyadan bir necha daqiqagacha.\n\n<b>Buyruqlar:</b>\n/start - botni qayta ishga tushirish;\n/information - foydalanish qo'llanmasi", reply_markup=keyboard, parse_mode="HTML")

@dp.message(Command("information"))
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardRemove()
    await message.answer("🤖<b>Bot ChatGPT sun'iy intellektni qo'llab-quvvatlaydi. Foydalanish uchun esa shunchaki savolingizni botga yozing! \n\nFoydalanish qo'llanmasi:</b> \n• Bot sizning istalgan savolingizga suhbatdoshdek javob beradi va barcha tillarda so'zlashishingiz mumkin; \n• Bot faqat 2021-yilgi ma'lumotlarga ega;\n• Notog'ri javob qaytarsa, savolingizni qaytadan batafsilroq yozing.\n\n<b>Buyruqlar: </b>\n/start - botni qayta ishga tushirish;\n/information - foydalanish qo'llanmasi\n\n<b>Murojaat va takliflar uchun:</b>\n @Texno_GPTsupport", reply_markup=keyboard, parse_mode="HTML")

@dp.message(Command("myid"))
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardRemove()
    await message.answer(f"Sizning ID raqamingiz: {message.from_user.id}", reply_markup=keyboard)

@dp.message(Command("admin"))
async def cmd_start_admin(message: types.Message):
    user_id = message.from_user.id
    user = message.from_user
    if user_id in admin_userIds.keys():
        admin_sessions[user_id] = True
        if user_id in ownerId:
            owner_sessions[user_id] = True
            kb = [
                [
                    types.KeyboardButton(text="Xabar yuborish ✉️"),
                    types.KeyboardButton(text="Statistika 📊")
                ],
                [
                    types.KeyboardButton(text="APIni yangilash 🔄"),
                    types.KeyboardButton(text="Kanal qo'shish ➕")
                ],
                [types.KeyboardButton(text="Admin boshqaruvi 👤")],
                [types.KeyboardButton(text="Ertangi kunga otish 🔄")],
                [types.KeyboardButton(text="Orqaga qaytish 🔙")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer(f"Admin panelga xush kelibsiz. Menuni tanlang!", reply_markup=keyboard)
        elif user_id in admin_userIds.keys():
            kb = [
                [
                    types.KeyboardButton(text="Xabar yuborish ✉️"),
                    types.KeyboardButton(text="Statistika 📊")
                ],
                [types.KeyboardButton(text="Kanal qo'shish ➕")],
                [types.KeyboardButton(text="Orqaga qaytish 🔙")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await message.answer(f"Admin panelga xush kelibsiz. Menuni tanlang!", reply_markup=keyboard)

async def check_subcription(message: types.Message):
    user_id = message.from_user.id
    user = message.from_user

    channel_unsubscribed = []
    for channel_username in channel_usernames:
        if await is_subscribed(user_id, channel_username):
            continue
        else:
            channel_unsubscribed.append(channel_username)
    builder = InlineKeyboardBuilder()
    for channel in channel_unsubscribed:
        builder.add(types.InlineKeyboardButton(text=f"{channel}", url=f"https://t.me/{channel[1:]}"))
        builder.adjust(1, 1)
    if channel_unsubscribed:
        builder.add(types.InlineKeyboardButton(text=f"Tekshirish ✅", callback_data="checkSubscription"))
        builder.adjust(1, 1)
        await message.answer(
            "• Botdan foydalanish uchun avval kanalga obuna bo’ling va <b>Tekshirish</b> tugmasini bosing!",
            reply_markup=builder.as_markup(), parse_mode="HTML")
        return
    elif len(channel_unsubscribed) == 0:
        if user_id not in today_logined_users and user_id not in all_users:
            today_logined_users.append(user_id)
            with open('today_logined_users.json', 'w') as file:
                json.dump(today_logined_users, file)
        today_active_users.append(user_id)
        with open('today_active_users.json', 'w') as file:
            json.dump(today_active_users, file)
        if user_id not in all_users:
            all_users.append(user_id)
            with open('all_users.json', 'w') as file:
                json.dump(all_users, file)
        if user_id not in active_users:
            active_users.append(user_id)
            with open('active_users.json', 'w') as file:
                json.dump(active_users, file)
        if user_id in all_users:
            if user_id in inactive_users:
                inactive_users.remove(user_id)
                with open('inactive_users.json', 'w') as file:
                    json.dump(inactive_users, file)
        return True
@dp.message()
async def handle_message(message: types.Message):
    global new_api_key, last_api_key_update, video_file_id, reklam, reklamBuilder
    user_id = message.from_user.id
    user_message = message.text
    if user_id not in user_states.keys():
        user_states[user_id] = {'awaiting_response': False}

    if await check_subcription(message):
        if user_message == "Orqaga qaytish  🔙" or user_message == "Bekor qilish ❌" :
            reklam = ""
            reklamBuilder = InlineKeyboardBuilder()
            if user_id in send_message_session:
                del send_message_session[user_id]
            if user_id in add_inline_keyboard_session:
                del add_inline_keyboard_session[user_id]
            if user_id in inline_keyboard_session:
                del inline_keyboard_session[user_id]
            if user_id in api_control_session:
                del api_control_session[user_id]
            if user_id in api_add_session:
                del api_add_session[user_id]
            if user_id in admin_control_session:
                del admin_control_session[user_id]
            if user_id in admin_add_session:
                del admin_add_session[user_id]
            if user_id in chanel_control_session:
                del chanel_control_session[user_id]
            if user_id in chanel_add_session:
                del chanel_add_session[user_id]
            if user_id in ownerId:
                owner_sessions[user_id] = True
                kb = [
                    [
                        types.KeyboardButton(text="Xabar yuborish ✉️"),
                        types.KeyboardButton(text="Statistika 📊")
                    ],
                    [
                        types.KeyboardButton(text="APIni yangilash 🔄"),
                        types.KeyboardButton(text="Kanal qo'shish ➕")
                    ],
                    [types.KeyboardButton(text="Admin boshqaruvi 👤")],
                    [types.KeyboardButton(text="Ertangi kunga otish 🔄")],
                    [types.KeyboardButton(text="Orqaga qaytish 🔙")],
                ]
                keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
                await message.answer(f"Admin panelga xush kelibsiz. Menuni tanlang!", reply_markup=keyboard)
            elif user_id in admin_userIds.keys():
                kb = [
                    [
                        types.KeyboardButton(text="Statistika 📊")
                    ],
                    [types.KeyboardButton(text="Kanal qo'shish ➕")],
                    [types.KeyboardButton(text="Orqaga qaytish 🔙")],
                ]
                keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
                await message.answer(f"Admin panelga xush kelibsiz. Menuni tanlang!", reply_markup=keyboard)
        elif user_id in admin_control_session:
            await admin_control_session_service(message)
        elif user_id in inline_keyboard_session:
            if user_message == "Qo'shish ✅":
                add_inline_keyboard_session[user_id] = True
                kb = [
                    [
                        types.KeyboardButton(text="Bekor qilish ❌"),
                    ]
                ]
                keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
                await message.answer(
                    "Kanal nomi*Kanal sslikasi\nKanal nomi*Kanal sslikasi\n...\n\nIltimos shu ko`rinishda kiriting",
                    reply_markup=keyboard)
            elif user_message == "Tashlab o'tish ❌":
                kb = [
                    [
                        types.KeyboardButton(text="Yuborish ✅"),
                        types.KeyboardButton(text="Bekor qilish ❌"),
                    ]
                ]
                keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
                await message.answer(
                    "Xabaringiz to'g'rimi? Agarda to'g'ri bo'lsa \"Yuborish ✅\" tugmasini bosing aks holda \"Bekor qilish ❌\"ni bosing",
                    reply_markup=keyboard)
            elif user_message == "Yuborish ✅":
                if user_id in ownerId:
                    owner_sessions[user_id] = True
                    kb = [
                        [
                            types.KeyboardButton(text="Xabar yuborish ✉️"),
                            types.KeyboardButton(text="Statistika 📊")
                        ],
                        [
                            types.KeyboardButton(text="APIni yangilash 🔄"),
                            types.KeyboardButton(text="Kanal qo'shish ➕")
                        ],
                        [types.KeyboardButton(text="Admin boshqaruvi 👤")],
                        [types.KeyboardButton(text="Ertangi kunga otish 🔄")],
                        [types.KeyboardButton(text="Orqaga qaytish 🔙")],
                    ]
                    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
                    await message.answer(f"Admin panelga xush kelibsiz. Menuni tanlang!", reply_markup=keyboard)
                elif user_id in admin_userIds.keys():
                    kb = [
                        [
                            types.KeyboardButton(text="Xabar yuborish ✉️"),
                            types.KeyboardButton(text="Statistika 📊")
                        ],
                        [types.KeyboardButton(text="Kanal qo'shish ➕")],
                        [types.KeyboardButton(text="Orqaga qaytish 🔙")],
                    ]
                    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
                    await message.answer(f"Admin panelga xush kelibsiz. Menuni tanlang!", reply_markup=keyboard)
                await send_message_controller(message)
            elif user_id in add_inline_keyboard_session:
                keyboards = user_message.split("\n")
                for keyboard in keyboards:
                    name = keyboard.split("*")[0]
                    url = keyboard.split("*")[1]
                    reklamBuilder.add(types.InlineKeyboardButton(text=f"{name}", url=f"{url}"))
                    reklamBuilder.adjust(1, 1)
                if isinstance(reklam, types.Message) and reklam.video:
                    video = reklam.video
                    caption = reklam.caption

                    await bot.send_video(
                        chat_id=user_id,
                        video=video.file_id,
                        caption=caption,
                        disable_notification=True,
                        reply_markup=reklamBuilder.as_markup(),
                        parse_mode="HTML"
                    )
                elif isinstance(reklam, types.Message):
                    await bot.copy_message(
                        chat_id=user_id,
                        from_chat_id=reklam.chat.id,
                        message_id=reklam.message_id,
                        reply_markup=reklamBuilder.as_markup(),
                        parse_mode="HTML"
                    )
                kb = [
                    [
                        types.KeyboardButton(text="Yuborish ✅"),
                        types.KeyboardButton(text="Bekor qilish ❌"),
                    ]
                ]
                keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
                await message.answer(
                    "Xabaringiz to'g'rimi? Agarda to'g'ri bo'lsa \"Yuborish ✅\" tugmasini bosing aks holda \"Bekor qilish ❌\"ni bosing",
                    reply_markup=keyboard)
        elif user_id in send_message_session:
            await send_message_service(message)
        elif user_id in api_control_session:
            await api_control_session_service(message)
        elif user_id in chanel_control_session:
            await chanel_control_session_service(message)
        elif user_message == "Ertangi kunga o'tish ✅":
            # for user_id in active_users:
            #     await check_user_reachability(user_id)
            today_logined_users.clear()
            today_active_users.clear()
            with open('today_logined_users.json', 'w') as file:
                json.dump(today_logined_users, file)
            with open('today_active_users.json', 'w') as file:
                json.dump(today_active_users, file)
            await cmd_start_admin(message)
        elif user_id in admin_sessions:
            await admin_sessions_service(message)
        else:
            await chat_with_openai(message)

# async def chat_with_openai(message: types.Message):
#     user_id = message.from_user.id
#     user_message = message.text
#
#     if 'awaiting_response' in user_states[user_id] and user_states[user_id]['awaiting_response']:
#         builder = InlineKeyboardBuilder()
#         builder.add(types.InlineKeyboardButton(text=f"❌", callback_data=f"bekorqilish"))
#         await message.reply("⏳ Oldingi so'rovingiz bo'yicha javob tayyorlanmoqda, iltimos biroz kutib turing!", reply_markup=builder.as_markup())
#         return
#
#     user_states[user_id]['awaiting_response'] = True
#
#     response = await process_user_request(user_id, user_message)
#
#     user_states[user_id]['awaiting_response'] = False
#
#     await message.reply(response)

async def chat_with_openai(message: types.Message):
    user_id = message.from_user.id
    user_message = message.text

    if 'awaiting_response' in user_states[user_id] and user_states[user_id]['awaiting_response']:
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(text=f"❌", callback_data=f"bekorqilish"))
        await message.reply("⏳ Oldingi so'rovingiz bo'yicha javob tayyorlanmoqda, iltimos biroz kutib turing!", reply_markup=builder.as_markup())
        return

    user_states[user_id]['awaiting_response'] = True

    # Set a timeout task to reset the awaiting_response after 5 minutes
    timeout_seconds = 5 * 60
    timeout_task = asyncio.create_task(timeout_reset(user_id, timeout_seconds))

    try:
        response = await process_user_request(user_id, user_message)
        await message.reply(response)
    finally:
        # Cancel the timeout task if it hasn't completed
        timeout_task.cancel()

        # Reset the awaiting_response
        user_states[user_id]['awaiting_response'] = False

async def timeout_reset(user_id, timeout_seconds):
    await asyncio.sleep(timeout_seconds)
    user_states[user_id]['awaiting_response'] = False

async def is_text_message(message):
    return isinstance(message, str) and len(message.strip()) > 0

async def process_user_request(user_id, user_message):
    try:
        if await is_daily_limit_exceeded(user_id):
            await bot.send_message(user_id,
                                   f"😔 <b>Afsuski kunlik 30 ta so'rov limitiga yetdingiz! Limit har kuni yangilanadi.</b>",
                                   parse_mode="HTML")
        else:
            user_reload_messages[user_id] = await bot.send_message(user_id, "⏳ Javobni tayyorlayapman…")
            openai.api_key = await get_current_api_key()
            response = await asyncio.to_thread(openai.ChatCompletion.create,
                                               model="gpt-3.5-turbo-1106",
                                               messages=[
                                                   {"role": "system", "content": "You are a helpful assistant."},
                                                   {"role": "user", "content": user_message}
                                               ],
                                               max_tokens=1000
                                               )

            if response and response.choices and response.choices[0].message.content:
                bot_response = response['choices'][0]['message']['content']
                await bot.delete_message(user_id, user_reload_messages[user_id].message_id)
                await increment_request_count(user_id)
                return bot_response
    except Exception as e:
        await bot.delete_message(user_id, user_reload_messages[user_id].message_id)
        await bot.send_message(chat_id="@testchanellforbot13",
                               text=f"Botda nosozlik bor iltimos bartaraf eting:\n\n {e}\n\n\n {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        await bot.send_message(user_id,
                               f"🤖 Menda xatolik yuz berdi, havotirga o'rin yo'q meni tez orada tuzatishadi.\n\n• Iltimos ozroqdan so'ng urinib ko'ring yoki savolni batafsil va qisqaroq yozing.")

async def admin_control_session_service(message: types.Message):
    user_id = message.from_user.id
    user_message = message.text
    if user_message == "Adminlar royxati 📄":
        builder = InlineKeyboardBuilder()
        for item in list(admin_userIds.items()):
            builder.add(types.InlineKeyboardButton(text=f"{item[0]}", callback_data=f"nothing"))
            builder.add(types.InlineKeyboardButton(text=f"{item[1]}", callback_data=f"nothing"))
            builder.add(types.InlineKeyboardButton(text=f"🗑", callback_data=f"admin_delete_{item[0]}"))
            builder.adjust(3, 3)
        await message.answer(
            f"Adminlar royxati 📄",
            reply_markup=builder.as_markup())
    elif user_id in admin_add_session:
        del admin_add_session[user_id]
        userid = user_message.split(" ")
        admin_userIds[int(userid[0])] = userid[1]
        await message.answer("Admin qoshildi", )
    if user_message == "Admin qoshish ➕":
        admin_add_session[user_id] = True
        await message.answer("Admin qoshish ➕ uchun uning ID sini va Ismini yozing. Misol : 2479323 Ismi", )

async def admin_sessions_service(message: types.Message):
    user_id = message.from_user.id
    user_message = message.text
    if user_message == "APIni yangilash 🔄" and user_id in ownerId:
        api_control_session[user_id] = True
        kb = [
            [
                types.KeyboardButton(text="API qoshish ➕"),
                types.KeyboardButton(text="API royxati 📄"),
            ],
            [types.KeyboardButton(text="Orqaga qaytish  🔙")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(
            "APIni yangilash 🔄",
            reply_markup=keyboard)
    if user_message == "Ertangi kunga otish 🔄" and user_id in ownerId:
        kb = [
            [types.KeyboardButton(text="Ertangi kunga o'tish ✅")],
            [types.KeyboardButton(text="Orqaga qaytish  🔙")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(
            "Rostdan ham keyingi kunga o'tmoqchimisiz?",
            reply_markup=keyboard)
    if user_message == "Xabar yuborish ✉️":
        send_message_session[user_id] = True
        kb = [
            [types.KeyboardButton(text="Orqaga qaytish  🔙")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(f"Marhamat xabaringizni yuborishingiz mumkin", reply_markup=keyboard)
    if user_message == "Admin boshqaruvi 👤" and user_id in ownerId:
        admin_control_session[user_id] = True
        kb = [
            [
                types.KeyboardButton(text="Admin qoshish ➕"),
                types.KeyboardButton(text="Adminlar royxati 📄"),
            ],
            [types.KeyboardButton(text="Orqaga qaytish  🔙")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(
            "Admin boshqaruvi 👤",
            reply_markup=keyboard)
    if user_message == "Statistika 📊":
        await message.answer(f"📊 Jami a'zolar soni: {len(all_users)}\n"
                             f"📈 Aktiv a'zolar soni: {len(active_users)}\n"
                             f"📊 Bugungi ishlatganlar: {len(get_duplicates())}\n"
                             f"📉 Block qilganlar soni: {len(inactive_users)}\n"
                             f"📊 Bugungi a'zolar: {len(today_logined_users)}")
    if user_message == "Kanal qo'shish ➕":
        chanel_control_session[user_id] = True
        kb = [
            [
                types.KeyboardButton(text="Kanal qoshish ➕"),
                types.KeyboardButton(text="Kanallar royxati 📄"),
            ],
            [types.KeyboardButton(text="Orqaga qaytish  🔙")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(
            "Kanal qo'shish ➕",
            reply_markup=keyboard)
    if user_message == "Orqaga qaytish 🔙":
        if user_id in owner_sessions:
            del owner_sessions[user_id]
        del admin_sessions[user_id]
        keyboard = types.ReplyKeyboardRemove()
        await message.answer("<b>Salom! 👋\n\nMen istalgan mavzu yoki vazifalar bo'yicha ma'lumot va savolingizga javob topishda yordam beradigan chatbotman. Foydalanish uchun esa shunchaki savolni yozishingiz kifoya.\n\nChatbot nimalar qiloladi?</b>\n1. Savolga javob berish va matnni barcha tillarda tarjima qilish;\n2. Istalgan fanlarga oid informatsiyalar ba'zasi;\n3. Matematik misol va masalalarni yechish;\n4. Kod yozib, uni tahrirlash va texnologiya, dasturlash tillari, algoritmlar haqida ma'lumot berish;\n5. She'rlar, hikoyalar, insholar va ijodiy asarlar yozib berish;\n6. Sog'liq-salomatlik, to'g'ri ovqatlanish va fitnes bo'yicha to'g'ri ma'lumot berish.\n\n<b>Bot savollarga qanchalik tez javob beradi?</b>\nBir nech soniyadan bir necha daqiqagacha.\n\n<b>Buyruqlar:</b>\n/start - botni qayta ishga tushirish;\n/information - foydalanish qo'llanmasi", reply_markup=keyboard, parse_mode="HTML")

async def send_message_service(message: types.Message):
    global reklam
    reklam = message
    kb = [
        [
            types.KeyboardButton(text="Qo'shish ✅"),
            types.KeyboardButton(text="Tashlab o'tish ❌"),
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Xabaringiz saqlandi. Xabar tagiga keyboard reklama qo'shasizmi?", reply_markup=keyboard)
    inline_keyboard_session[message.from_user.id] = True

async def api_control_session_service(message: types.Message):
    user_id = message.from_user.id
    user_message = message.text
    if user_message == "API royxati 📄":
        builder = InlineKeyboardBuilder()
        for item in list(api_keys.items()):
            builder.add(types.InlineKeyboardButton(text=f"{item[0]}", callback_data=f"nothing"))
            builder.add(types.InlineKeyboardButton(text=f"{item[1]}", callback_data=f"nothing"))
            builder.add(types.InlineKeyboardButton(text=f"🗑", callback_data=f"api_delete_{item[0]}"))
            builder.adjust(3, 3)
        await message.answer(
            f"Siz qoshgan API lar royxati",
            reply_markup=builder.as_markup())
    elif user_id in api_add_session:
        del api_add_session[user_id]
        userid = user_message.replace("_", "").split(" ")
        api_keys[userid[0]] = userid[1]
        await message.answer("Api qoshildi", )
    if user_message == "API qoshish ➕":
        api_add_session[user_id] = True
        await message.answer("Qoshmoqchi bolgan API ingizni jonating. Misol : ApiNomi API", )

async def chanel_control_session_service(message: types.Message):
    user_id = message.from_user.id
    user_message = message.text
    if user_message == "Kanallar royxati 📄":
        builder = InlineKeyboardBuilder()
        for item in channel_usernames:
            builder.add(types.InlineKeyboardButton(text=f"{item}", callback_data=f"nothing"))
            builder.add(types.InlineKeyboardButton(text=f"🗑", callback_data=f"channel_delete_{item}"))
            builder.adjust(2, 2)
        await message.answer(
            f"Siz qoshgan kanallar lar royxati",
            reply_markup=builder.as_markup())
    elif user_id in chanel_add_session:
        if user_message.startswith("@"):
            del chanel_add_session[user_id]
            channel_usernames.append(f"{user_message}")
            await message.answer("Kanal qoshildi", )
        else: await message.answer("Iltimos kanal nomini tog'ri kiriting!")
    if user_message == "Kanal qoshish ➕":
        chanel_add_session[user_id] = True
        await message.answer("Qoshmoqchi bolgan kanalingizni jonating. Misol : @kanal", )

async def send_message_controller(message: types.Message):
    global reklam
    start_time = datetime.now()
    if isinstance(reklam, types.Message) and reklam.video:
        video = reklam.video
        caption = reklam.caption

        for user_id in active_users:
            try:
                sended_users.append(user_id)
                await bot.send_video(
                    chat_id=user_id,
                    video=video.file_id,
                    caption=caption,
                    disable_notification=True,
                    reply_markup=reklamBuilder.as_markup(),
                    parse_mode="HTML"
                )
            except Exception as e:
                unsended_users.append(user_id)
                active_users.remove(user_id)
                inactive_users.append(user_id)
                with open('inactive_users.json', 'w') as file:
                    json.dump(inactive_users, file)
                with open('active_users.json', 'w') as file:
                    json.dump(active_users, file)

    elif isinstance(reklam, types.Message):
        for user in active_users:
            try:
                sended_users.append(user)
                await bot.copy_message(
                    chat_id=user,
                    from_chat_id=reklam.chat.id,
                    message_id=reklam.message_id,
                    reply_markup=reklamBuilder.as_markup(),
                    parse_mode="HTML"
                )
            except Exception as e:
                unsended_users.append(user)
                active_users.remove(user)
                inactive_users.append(user)
                with open('inactive_users.json', 'w') as file:
                    json.dump(inactive_users, file)
                with open('active_users.json', 'w') as file:
                    json.dump(active_users, file)

    end_time = datetime.now()
    execution_time = (end_time - start_time)
    total_seconds = execution_time.total_seconds()
    minutes, seconds = divmod(total_seconds, 60)
    time_string = f"{int(minutes)} daqiqa {int(seconds)} sekund vaqt oralig'ida yuborildi."
    await message.answer(f"Xabaringiz yuborildi ✅\n\nYuborilmaganlar soni: {len(unsended_users)}\nYuborilganlar soni: {len(sended_users)}\n{time_string}")
    del send_message_session[message.from_user.id]

@dp.callback_query(lambda callback: callback.data.startswith("admin_delete_"))
async def admin_controller(callback: types.CallbackQuery):
    if callback.data.startswith("admin_delete_"):
        user_id = callback.data.split("_")
        admin = admin_userIds[int(user_id[2])]

        if admin:
            del admin_userIds[int(user_id[2])]
            builder = InlineKeyboardBuilder()
            for item in list(admin_userIds.items()):
                builder.add(types.InlineKeyboardButton(text=f"{item[0]}", callback_data=f"nothing"))
                builder.add(types.InlineKeyboardButton(text=f"{item[1]}", callback_data=f"nothing"))
                builder.add(types.InlineKeyboardButton(text=f"🗑", callback_data=f"admin_delete_{item[0]}"))
                builder.adjust(3, 3)
            await callback.message.answer(f"Adminlar royxati 📄", reply_markup=builder.as_markup())
            await callback.answer(f"Deleting admin: {admin}", show_alert=True)
        else:
            await callback.answer("Admin not found.", show_alert=True)

@dp.callback_query(lambda callback: callback.data.startswith("api_delete_"))
async def api_controller(callback: types.CallbackQuery):
    if callback.data.startswith("api_delete_"):
        api_name = callback.data.split("_")[2]

        if api_name in api_keys:
            del api_keys[api_name]
            builder = InlineKeyboardBuilder()
            for item in list(api_keys.items()):
                builder.add(types.InlineKeyboardButton(text=f"{item[0]}", callback_data=f"nothing"))
                builder.add(types.InlineKeyboardButton(text=f"{item[1]}", callback_data=f"nothing"))
                builder.add(types.InlineKeyboardButton(text=f"🗑", callback_data=f"api_delete_{item[0]}"))
                builder.adjust(3, 3)
            await callback.message.answer(f"Apilar royxati", reply_markup=builder.as_markup())
            await callback.answer(f"Deleting api: {api_name}", show_alert=True)
        else:
            await callback.answer("Api not found.", show_alert=True)

@dp.callback_query(lambda callback: callback.data == 'bekorqilish')
async def cancel_callback(callback: types.CallbackQuery):
    await callback.message.delete()

@dp.callback_query(lambda callback: callback.data.startswith("channel_delete_"))
async def channel_controller(callback: types.CallbackQuery):
    if callback.data.startswith("channel_delete_"):
        channel_name = callback.data.split("@")[1]
        if f"@{channel_name}" in channel_usernames:
            channel_usernames.remove(f"@{channel_name}")
            builder = InlineKeyboardBuilder()
            for item in channel_usernames:
                builder.add(types.InlineKeyboardButton(text=f"{item}", callback_data=f"nothing"))
                builder.add(types.InlineKeyboardButton(text=f"🗑", callback_data=f"channel_delete_{item}"))
                builder.adjust(2, 2)
            await callback.message.answer(f"Kanallar royxati 📄", reply_markup=builder.as_markup())
            await callback.answer(f"Deleting channel: {channel_name}", show_alert=True)
        else:
            await callback.answer("Chanel not found.", show_alert=True)

@dp.callback_query(lambda callback: callback.data.startswith("checkSubscription"))
async def channel_controller(callback: types.CallbackQuery):
    if callback.data.startswith("checkSubscription"):
        user_id = callback.from_user.id
        channel_unsubscribed = []
        for channel_username in channel_usernames:
            if await is_subscribed(user_id, channel_username):
                continue
            else:
                channel_unsubscribed.append(channel_username)
        builder = InlineKeyboardBuilder()
        for channel in channel_unsubscribed:
            builder.add(types.InlineKeyboardButton(text=f"{channel}", url=f"https://t.me/{channel[1:]}"))
            builder.adjust(1, 1)
        if channel_unsubscribed:
            await callback.answer("• Botdan foydalanish uchun avval kanalga obuna bo’ling.")
            return
        else:
            if user_id not in today_logined_users and user_id not in all_users:
                today_logined_users.append(user_id)
                with open('today_logined_users.json', 'w') as file:
                    json.dump(today_logined_users, file)
            today_active_users.append(user_id)
            with open('today_active_users.json', 'w') as file:
                json.dump(today_active_users, file)
            if user_id not in all_users:
                all_users.append(user_id)
                with open('all_users.json', 'w') as file:
                    json.dump(all_users, file)
            if user_id not in active_users:
                active_users.append(user_id)
                with open('active_users.json', 'w') as file:
                    json.dump(active_users, file)
            if user_id in all_users and user_id in inactive_users:
                inactive_users.remove(user_id)
                with open('inactive_users.json', 'w') as file:
                    json.dump(inactive_users, file)
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            await callback.answer("")
            await callback.message.answer(
                    "<b>Salom! 👋\n\nMen istalgan mavzu yoki vazifalar bo'yicha ma'lumot va savolingizga javob topishda yordam beradigan chatbotman. Foydalanish uchun esa shunchaki savolni yozishingiz kifoya.\n\nChatbot nimalar qiloladi?</b>\n1. Savolga javob berish va matnni barcha tillarda tarjima qilish;\n2. Istalgan fanlarga oid informatsiyalar ba'zasi;\n3. Matematik misol va masalalarni yechish;\n4. Kod yozib, uni tahrirlash va texnologiya, dasturlash tillari, algoritmlar haqida ma'lumot berish;\n5. She'rlar, hikoyalar, insholar va ijodiy asarlar yozib berish;\n6. Sog'liq-salomatlik, to'g'ri ovqatlanish va fitnes bo'yicha to'g'ri ma'lumot berish.\n\n<b>Bot savollarga qanchalik tez javob beradi?</b>\nBir nech soniyadan bir necha daqiqagacha.\n\n<b>Buyruqlar:</b>\n/start - botni qayta ishga tushirish;\n/information - foydalanish qo'llanmasi", parse_mode="HTML")

async def set_default_commands():
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Qayta ishga tushurish"),
        types.BotCommand(command="information", description="Foydalanish qo'llanmasi"),
    ])

async def main():
    await set_default_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.create_task(periodic_user_check())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(bot.close())