import asyncio
import logging
import os
from collections import defaultdict
from datetime import datetime, date
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
user_states = {}
owner_sessions = {}
send_message_session = {}
inline_keyboard_session = {}
add_inline_keyboard_session = {}
logging.basicConfig(level=logging.INFO)
all_users = {}
active_users = {}
today_active_users = []
today_logined_users = []
user_reload_messages = {}
inactive_users = {}
today = datetime.now().date()
channel_usernames = []
admin_userIds = {1052097431: "𝙺𝚘𝚖𝚛𝚘𝚗", 1232328054: "Cloud"}
ownerId = [1232328054, 1052097431]
user_request_counts = defaultdict(int)
user_last_request = {}
reklam = ""
reklamBuilder = InlineKeyboardBuilder()
video_file_id = 0
chat_id = 0


async def is_daily_limit_exceeded(user_id):
    today = date.today()
    if user_id in user_last_request and user_last_request[user_id] == today:
        if user_request_counts[user_id] >= 40:
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
        send_message_session = await bot.send_message(chat_id=user_id[0],text="Botni block qilmaganingiz tekshirilmoqda, bu habarga etibor bermang. Tushunganingiz uchun raxmat 😇")
        await bot.delete_message(user_id[0], send_message_session.message_id)
    except Exception as e:
        del active_users[user_id[0]]
        inactive_users[user_id[0]] = True
async def periodic_user_check():
    while True:
        for user_id in list(all_users.items()):
            await check_user_reachability(user_id)
        today_active_users.clear()
        today_logined_users.clear()
        await asyncio.sleep(24 * 60 * 60)
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
    await message.answer("🤖<b>Bot ChatGPT sun'iy intellektni qo'llab-quvvatlaydi. Foydalanish uchun esa shunchaki savolingizni botga yozing! \n\nFoydalanish qo'llanmasi:</b> \n• Bot sizning istalgan savolingizga suhbatdoshdek javob beradi va barcha tillarda so'zlashishingiz mumkin; \n• Bot faqat 2021-yilgi ma'lumotlarga ega;\n• Notog'ri javob qaytarsa, savolingizni qaytadan batafsilroq yozing.\n\n<b>Buyruqlar: </b>\n/start - botni qayta ishga tushirish;\n/information - foydalanish qo'llanmasi\n\n<b>Murojaat va takliflar uchun:</b>\n @TexnoGPT_support", reply_markup=keyboard, parse_mode="HTML")

@dp.message(Command("myid"))
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardRemove()
    await message.answer(f"Sizning ID raqamingiz: {message.from_user.id}", reply_markup=keyboard)


@dp.message(Command("admin"))
async def cmd_start(message: types.Message):
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
        today_active_users.append(user_id)
        if user_id not in all_users:
            all_users[user_id] = user.first_name
        if user_id not in active_users:
            active_users[user_id] = user.first_name
        if user_id in all_users.keys():
            if user_id in inactive_users.keys():
                active_users[user_id] = user.first_name
                del inactive_users[user_id]
        return True
@dp.message()
async def handle_message(message: types.Message):
    global new_api_key, last_api_key_update, video_file_id, reklam, reklamBuilder
    user_id = message.from_user.id
    user_message = message.text

    if await check_subcription(message):
        if user_message == "Orqaga qaytish  🔙":
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
                await send_message_controller(user_id)
                kb = [
                    [
                        types.KeyboardButton(text="Orqaga qaytish  🔙"),
                    ]
                ]
                keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
                await message.answer(
                    "Xabaringiz yuborildi ✅",
                    reply_markup=keyboard)
            elif user_message == "Bekor qilish ❌":
                kb = [
                    [
                        types.KeyboardButton(text="Orqaga qaytish  🔙"),
                    ]
                ]
                keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
                await message.answer(
                    "Xabaringiz ochirildi 😕",
                    reply_markup=keyboard)
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
                        reply_markup=reklamBuilder.as_markup()
                    )
                elif isinstance(reklam, types.Message):
                    await bot.copy_message(
                        chat_id=user_id,
                        from_chat_id=reklam.chat.id,
                        message_id=reklam.message_id,
                        reply_markup=reklamBuilder.as_markup()
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
        elif user_id in admin_sessions:
            await admin_sessions_service(message)
        else:
            await chat_with_openai(message)



async def chat_with_openai(message: types.Message):
    user_id = message.from_user.id
    user_message = message.text

    try:
        if 'awaiting_response' in user_states[user_id] and user_states[user_id]['awaiting_response']:
            await message.reply("⏳ Oldingi savolingiz uchun javobni tayyorlayapman iltimos kutib turing.")
            return
    except:
        await message.reply("Iltimos botdan foydalanish uchun qayta /start bosib yuboring.")

    user_states[user_id]['awaiting_response'] = True

    response = await process_user_request(user_id, user_message)

    user_states[user_id]['awaiting_response'] = False

    await message.reply(response)


async def process_user_request(user_id, user_message):
    try:
        if await is_daily_limit_exceeded(user_id):
            await bot.send_message(user_id,
                                   f"😔 <b>Afsuski kunlik 40 ta so'rov limitiga yetdingiz! Limit har kuni yangilanadi.</b>",
                                   parse_mode="HTML")
        else:
            user_reload_messages[user_id] = await bot.send_message(user_id, "⏳ Javobni tayyorlayapman…")
            openai.api_key = await get_current_api_key()
            response = await asyncio.to_thread(openai.ChatCompletion.create,
                                               model="gpt-3.5-turbo",
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
    except openai.error.OpenAIError as e:
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

async def send_message_controller(userId):
    global reklam
    if isinstance(reklam, types.Message) and reklam.video:
        video = reklam.video
        caption = reklam.caption

        for user_id in active_users:
            await bot.send_video(
                chat_id=user_id,
                video=video.file_id,
                caption=caption,
                disable_notification=True,
                reply_markup=reklamBuilder.as_markup()
            )
    elif isinstance(reklam, types.Message):
        for user in list(active_users.items()):
            await bot.copy_message(
                chat_id=user[0],
                from_chat_id=reklam.chat.id,
                message_id=reklam.message_id,
                reply_markup=reklamBuilder.as_markup()
            )
    del send_message_session[userId]


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

        if api_name in api_keys.keys():
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
            user = callback.from_user
            if user.id not in today_logined_users and user.id not in all_users:
                today_logined_users.append(user.id)
            today_active_users.append(user.id)
            if user.id not in all_users:
                all_users[user.id] = user.first_name
            if user.id not in active_users:
                active_users[user.id] = user.first_name
            if user.id in all_users and user.id in inactive_users:
                active_users[user.id] = user.first_name
                del inactive_users[user.id]
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