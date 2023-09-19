import asyncio
import logging
import os
from datetime import datetime
import openai
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ChatMemberStatus
from aiogram.filters.command import Command
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

logging.basicConfig(level=logging.INFO)
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
send_message = {}
send_message_text = {}
send_message_rasm = {}
send_message_video = {}
sending_text_to_video = {}
logging.basicConfig(level=logging.INFO)
all_users = {}
active_users = {}
today_active_users = []
today_logined_users = []
inactive_users = []
today = datetime.now().date()
channel_usernames = []
admin_userIds = {1052097431: "𝙺𝚘𝚖𝚛𝚘𝚗", 1232328054: "Cloud"}
ownerId = 1232328054

video_file_id = 0
chat_id = 0

def get_current_api_key():
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
        sent_message = await bot.send_message(chat_id=user_id[0],text="Botni block qilmaganingiz tekshirilmoqda, bu habarga etibor bermang. Tushunganingiz uchun raxmat 😇")
        await bot.delete_message(user_id[0], sent_message.message_id)
    except Exception as e:
        del active_users[user_id[0]]
        inactive_users.append(user_id)
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
        builder.add(types.InlineKeyboardButton(text=f"Tekshirish", callback_data="checkSubscription"))
        builder.adjust(1, 1)
        await message.answer("• Botdan foydalanish uchun avval kanalga obuna bo’ling va Tekshirish tugmasini bosing! \n @TexoAI - sun''iy intellektlar va texnologiyalar haqida eng so''nggi yangiliklarni berib boruvchi kanal",
                             reply_markup=builder.as_markup())
        return

@dp.message(Command("information"))
async def cmd_start(message: types.Message):
    await message.answer("🤖Bot ChatGPT sun''iy intellektni qo''llab-quvvatlaydi. Foydalanish uchun esa shunchaki savolingizni botga yozing! \n Foydalanish qo'llanmasi: \n• Bot sizning istalgan savolingizga suhbatdoshdek javob beradi va barcha tillarda so'zlashishingiz mumkin; \n• Bot faqat 2021-yilgi ma'lumotlarga ega;\n• Notog''ri javob qaytarsa, savolingizni qaytadan batafsilroq yozing.\nBuyruqlar: \n/start - botni qayta ishga tushirish;\n/information - foydalanish qo''llanmasi\nMurojaat va takliflar uchun:\n @TexnoGPT_support")


@dp.message()
async def handle_message(message: types.Message):
    global new_api_key, last_api_key_update, video_file_id
    user_id = message.from_user.id
    user = message.from_user
    user_message = message.text
    today_active_users.append(user.id)

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
        builder.add(types.InlineKeyboardButton(text=f"Obuna boldim tekshirish", callback_data="checkSubscription"))
        builder.adjust(1, 1)
        await message.answer("Iltimos botdan foydalanish uchun kanallarga obuna bo'ling", reply_markup=builder.as_markup())
        return

    if user_message == "Orqaga qaytish ❌":
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

        if user_id == ownerId:
            owner_sessions[user_id] = True
            kb = [
                [
                    types.KeyboardButton(text="Xabar yuborish ✉️"),
                    types.KeyboardButton(text="Statistika 📊")
                ],
                [
                    types.KeyboardButton(text="API boshqaruvi ⚙️"),
                    types.KeyboardButton(text="Kanallarni boshqarish 🛠")
                ],
                [types.KeyboardButton(text="Adminlarni boshqarish")],
                [types.KeyboardButton(text="Admin paneldan chiqish ❌")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
            await message.answer(f"Admin panelga hush kelibsiz {user.first_name}", reply_markup=keyboard)
        elif user_id in admin_userIds.keys():
            kb = [
                [
                    types.KeyboardButton(text="Xabar yuborish ✉️"),
                    types.KeyboardButton(text="Statistika 📊")
                ],
                [types.KeyboardButton(text="Kanallarni boshqarish 🛠")],
                [types.KeyboardButton(text="Admin paneldan chiqish ❌")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
            await message.answer(f"Admin panelga hush kelibsiz {user.first_name}", reply_markup=keyboard)
    if user_message == "Admin panel ⚙️":
        if user.id in admin_userIds.keys():
            admin_sessions[user_id] = True
            if user_id == ownerId:
                owner_sessions[user_id] = True
                kb = [
                    [
                        types.KeyboardButton(text="Xabar yuborish ✉️"),
                        types.KeyboardButton(text="Statistika 📊")
                    ],
                    [
                        types.KeyboardButton(text="API boshqaruvi ⚙️"),
                        types.KeyboardButton(text="Kanallarni boshqarish 🛠")
                    ],
                    [types.KeyboardButton(text="Adminlarni boshqarish")],
                    [types.KeyboardButton(text="Admin paneldan chiqish ❌")],
                ]
                keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
                await message.answer(f"Admin panelga hush kelibsiz {user.first_name}", reply_markup=keyboard)
            elif user_id in admin_userIds.keys():
                kb = [
                    [
                        types.KeyboardButton(text="Xabar yuborish ✉️"),
                        types.KeyboardButton(text="Statistika 📊")
                    ],
                    [types.KeyboardButton(text="Kanallarni boshqarish 🛠")],
                    [types.KeyboardButton(text="Admin paneldan chiqish ❌")],
                ]
                keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
                await message.answer(f"Admin panelga hush kelibsiz {user.first_name}", reply_markup=keyboard)
    if user_id in admin_control_session:
        if user_id in admin_add_session:
            del admin_add_session[user_id]
            userid = user_message.split(" ")
            admin_userIds[int(userid[0])] = userid[1]
            await message.answer("Admin qoshildi", )
        if user_message == "Admin qoshish":
            admin_add_session[user_id] = True
            await message.answer("Admin qoshish uchun uning ID sini va Ismini yozing. Misol : 2479323 Ismi",)
        if user_message == "Adminlar royxati":
            builder = InlineKeyboardBuilder()
            for item in list(admin_userIds.items()):
                builder.add(types.InlineKeyboardButton(text=f"{item[0]}", callback_data=f"nothing"))
                builder.add(types.InlineKeyboardButton(text=f"{item[1]}", callback_data=f"nothing"))
                builder.add(types.InlineKeyboardButton(text=f"🗑", callback_data=f"admin_delete_{item[0]}"))
                builder.adjust(3, 3)
            await message.answer(f"|               ID                   |               NAME               |                🗑               |", reply_markup=builder.as_markup())
    if user_id in api_control_session:
        if user_id in api_add_session:
            del api_add_session[user_id]
            userid = user_message.replace("_","").split(" ")
            api_keys[userid[0]] = userid[1]
            await message.answer("Api qoshildi", )
        if user_message == "API qoshish":
            api_add_session[user_id] = True
            await message.answer("Qoshmoqchi bolgan API ingizni jonating. Misol : ApiNomi API", )
        if user_message == "API royxati":
            builder = InlineKeyboardBuilder()
            for item in list(api_keys.items()):
                builder.add(types.InlineKeyboardButton(text=f"{item[0]}", callback_data=f"nothing"))
                builder.add(types.InlineKeyboardButton(text=f"{item[1]}", callback_data=f"nothing"))
                builder.add(types.InlineKeyboardButton(text=f"🗑", callback_data=f"api_delete_{item[0]}"))
                builder.adjust(3, 3)
            await message.answer(
                f"Siz qoshgan API lar royxati",
                reply_markup=builder.as_markup())
    if user_id in chanel_control_session:
        if user_id in chanel_add_session:
            del chanel_add_session[user_id]
            channel_usernames.append(f"{user_message}")
            await message.answer("Kanal qoshildi", )
        if user_message == "Kanal qoshish":
            chanel_add_session[user_id] = True
            await message.answer("Qoshmoqchi bolgan kanalingizni jonating. Misol : @kanal", )
        if user_message == "Kanallar royxati":
            builder = InlineKeyboardBuilder()
            for item in channel_usernames:
                builder.add(types.InlineKeyboardButton(text=f"{item}", callback_data=f"nothing"))
                builder.add(types.InlineKeyboardButton(text=f"🗑", callback_data=f"channel_delete_{item}"))
                builder.adjust(2, 2)
            await message.answer(
                f"Siz qoshgan kanallar lar royxati",
                reply_markup=builder.as_markup())
    if user_id in send_message:
        for user in list(active_users.items()):
            await message.answer(user_id=user, text=user_message)
    if user_id in admin_sessions:
        if user_message == "API boshqaruvi ⚙️" and user_id == ownerId:
            api_control_session[user_id] = True
            kb = [
                [
                    types.KeyboardButton(text="API qoshish"),
                    types.KeyboardButton(text="API royxati"),
                ],
                [types.KeyboardButton(text="Orqaga qaytish ❌")]
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
            await message.answer(
                "API boshqarish",
                reply_markup=keyboard)
        if user_message == "Xabar yuborish ✉️":
            send_message[user_id] = True
            kb = [
                [
                    types.KeyboardButton(text="Text 📝"),
                    types.KeyboardButton(text="Rasm 🖼"),
                    types.KeyboardButton(text="Video 📹")
                ],
                [types.KeyboardButton(text="Orqaga qaytish ❌")]
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
            await message.answer(f"Qanday xabar yuborasiz?", reply_markup=keyboard)
        if user_message == "Adminlarni boshqarish" and user_id == ownerId:
            admin_control_session[user_id] = True
            kb = [
                [
                    types.KeyboardButton(text="Admin qoshish"),
                    types.KeyboardButton(text="Adminlar royxati"),
                ],
                [types.KeyboardButton(text="Orqaga qaytish ❌")]
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
            await message.answer(
                "Adminlarni boshqarish",
                reply_markup=keyboard)
        if user_message == "Statistika 📊":
            await message.answer(f"📊 Jami a'zolar soni: {len(all_users)}\n"
                                 f"📈 Aktiv a'zolar soni: {len(active_users)}\n"
                                 f"📊 Bugungi ishlatganlar: {len(get_duplicates())}\n"
                                 f"📉 Block qilganlar soni: {len(inactive_users)}\n"
                                 f"📊 Bugungi a'zolar: {len(today_logined_users)}")
        if user_message == "Kanallarni boshqarish 🛠":
            chanel_control_session[user_id] = True
            kb = [
                [
                    types.KeyboardButton(text="Kanal qoshish"),
                    types.KeyboardButton(text="Kanallar royxati"),
                ],
                [types.KeyboardButton(text="Orqaga qaytish ❌")]
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
            await message.answer(
                "Kanallarni boshqarish",
                reply_markup=keyboard)
        if user_message == "Admin paneldan chiqish ❌":
            if user_id in owner_sessions:
                del owner_sessions[user_id]
            del admin_sessions[user_id]
            kb = [
                [
                    types.KeyboardButton(text="ChatGPT bilan muloqot qilish 🤖"),
                    types.KeyboardButton(text="Mening ID raqamim 🔍")
                ],
            ]
            if user.id in admin_userIds:
                kb.append([types.KeyboardButton(text="Admin panel ⚙️")])

            keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
            await message.answer(
                "Xizmatlarni pasdan tanlashingiz mumkun 😇",
                reply_markup=keyboard)
    if user_message == "ChatGPT bilan muloqot qilish 🤖":
        chat_sessions[user_id] = True
        kb = [
            [types.KeyboardButton(text="Orqaga qaytish ❌")],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        await message.answer(
            "Bu bot sizga savollaringizga javob topishda yordam beradi. Foydalanish uchun shunchaki savolingizni botga yozish kifoya. 😇\n\n\n\n Boshqa xizmatlardan foydalanish uchun 'Orqaga qaytish ❌' ni bo'sing",
            reply_markup=keyboard)
    elif user_id in chat_sessions:
        if user_message == "Orqaga qaytish ❌":
            del chat_sessions[user_id]
            kb = [
                [
                    types.KeyboardButton(text="ChatGPT bilan muloqot qilish 🤖"),
                    types.KeyboardButton(text="Mening ID raqamim 🔍")
                ],
            ]
            if user.id in admin_userIds:
                kb.append([types.KeyboardButton(text="Admin panel ⚙️")])

            keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
            await message.answer("Xizmatlarni pasdan tanlashingiz mumkun 😇", reply_markup=keyboard)
        elif user_id in chat_sessions:
            try:
                openai.api_key = get_current_api_key()
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=user_message,
                    max_tokens=1000,
                    temperature=0.7,
                )
                if response and response.choices and response.choices[0].text:
                    generated_text = response.choices[0].text
                    await message.answer(generated_text)
                else:
                    await message.answer("Error in API response or no text generated.")
            except openai.error.OpenAIError as e:
                # await bot.send_message(chat_id="@testchanellforbot13", text=f"Botda nosozlik bor iltimos bartaraf eting:\n\n {e}\n\n\n {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                kb = [
                    [types.KeyboardButton(text="Orqaga qaytish ❌")],
                ]
                keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
                await message.answer(f"Botda afsuski nosozlik bor iltimos keyinroq urinib koring")
    if user_message == "Mening ID raqamim 🔍":
            await message.answer(f"Sizning ID raqamingiz: {user_id}")


async def send_video_with_question(user_id, video_filename):
    caption = "Do you want to add text to this video?"
    with open(video_filename, "rb") as video_file:
        await bot.send_video(user_id, InputFile(video_file), caption=caption)
    os.remove(video_filename)

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
            await callback.message.answer(f"Adminlar royxati", reply_markup=builder.as_markup())
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
            await callback.message.answer(f"Kanallar royxati", reply_markup=builder.as_markup())
            await callback.answer(f"Deleting channel: {channel_name}", show_alert=True)
        else:
            await callback.answer("Chanel not found.", show_alert=True)

@dp.callback_query(lambda callback: callback.data.startswith("checkSubscription"))
async def channel_controller(callback: types.CallbackQuery):
    if callback.data.startswith("checkSubscription"):
        channel_unsubscribed = []
        for channel_username in channel_usernames:
            if await is_subscribed(callback.message.from_user.id, channel_username):
                continue
            else:
                channel_unsubscribed.append(channel_username)
        builder = InlineKeyboardBuilder()
        for channel in channel_unsubscribed:
            builder.add(types.InlineKeyboardButton(text=f"{channel}", url=f"https://t.me/{channel[1:]}"))
            builder.adjust(1, 1)
        if channel_unsubscribed:
            builder.add(types.InlineKeyboardButton(text=f"Obuna boldim tekshirish", callback_data="checkSubscription"))
            builder.adjust(1, 1)
            await callback.answer("Iltimos botdan foydalanish uchun kanallarga obuna bo'ling",
                                 reply_markup=builder.as_markup())
            return
        else :
            await callback.answer("Tabrikliman siz hamma kanalga obuna boldingiz")
            user = callback.from_user
            if user.id not in all_users:
                all_users[user.id] = user.first_name
                active_users[user.id] = user.first_name
                today_logined_users.append(user.id)
            if user.id in all_users and user.id in inactive_users:
                active_users[user.id] = user.first_name
                inactive_users.remove(user.id)
            kb = [
                [
                    types.KeyboardButton(text="ChatGPT bilan muloqot qilish 🤖"),
                    types.KeyboardButton(text="Mening ID raqamim 🔍")
                ],
            ]
            if user.id in admin_userIds.keys():
                kb.append([types.KeyboardButton(text="Admin panel ⚙️")])

            keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
            await callback.answer(
                "Assalomu aleykum\n\nBu bot siz uchun ba'zi xizmatlar beradi. Xizmatlarni pasdan tanlashingiz mumkun 😇",
                reply_markup=keyboard)


async def main():
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