from pyrogram import Client 
from pyrogram.types import Message, ReplyKeyboardRemove
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from util import Buttons
from util import Keyboards
from util import Values
from cache import Cache
from util import Keys

from language import fa as lang

from pyrogram.types import CallbackQuery

from wand.image import Image

import json # to display logs nicely

cache = Cache()

async def handle_updates(client: Client, message: Message):
    uid = message.from_user.id
    text = message.text
    media = message.media
    if media:
        await message.reply("You sent me a file. Do you want me to download it to server?", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text = "Download File", callback_data=Values.CONFIRM_DOWNLOAD)]
            ]
        ))
        
        cache.update_user_session(uid, Keys.MEDIA_MESSAGE, message)
        
        
    else:        
        match text:
            case "/start" | Buttons.home:
                await message.reply("Main Menu", reply_markup=Keyboards.MainMenu)
            case Buttons.settings:
                await message.reply("Setting Menu", reply_markup=Keyboards.SettingsMenu)
            case Buttons.admins:
                await message.reply("Admins Menu", reply_markup=Keyboards.AdminsMenu)
            case Buttons.remove_keyboard:
                confirm_inline_kb = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text = "Yes", callback_data=Values.CONFIRM_KB_REMOVAL), InlineKeyboardButton(text = "No", callback_data=Values.CANCEL_KB_REMOVAL)]
                ]
                )
                await message.reply("Are you sure you want to remove the keyboard?", reply_markup=confirm_inline_kb)
            case Buttons.make_inline_links:
                inline_kb = InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(text = "My Telegram Channel", url = "https://t.me/codewithmehdi")],
                        [InlineKeyboardButton(text = "My YouTube Channel", url = "https://youtube.com/mehdihaghgoo")],
                        [InlineKeyboardButton(text = "My GitHub Profile", url = "https://github.com/djnotes")]
                    ]
                )
                await message.reply(text = "My Links", reply_markup=inline_kb)
            
            # Handle Media
            case Buttons.media:
                await message.reply(text = "Media Menu", reply_markup= Keyboards.MediaMenu)
            case Buttons.send_photo:
                await client.send_photo(uid, "media/piano.jpg", "My Piano")
                await message.reply_photo("media/piano.jpg", "My Piano")
            case Buttons.send_sticker:
                await client.send_sticker(uid, "media/piano.webp")
            case Buttons.send_video:
                await client.send_video(uid, "media/piano.mp4", "Piano video")
            case Buttons.send_audio:
                await client.send_audio(uid, "media/piano.mp3", "A Nice Song")
            case Buttons.send_voice:
                await client.send_voice(uid, "media/piano.ogg", "A Nice Voice")
            case Buttons.send_document:
                await client.send_document(chat_id = uid, document = "media/piano.jpg", caption = "A Photo Sent as File")
            case Buttons.send_animation:
                await client.send_animation(uid, "media/blink.tgs", "A Nice Animation")
            case _:
                await message.reply("Unexpected input")


async def handle_callback_query(client: Client, query: CallbackQuery):
    uid = query.from_user.id
    match query.data:
        case Values.CONFIRM_KB_REMOVAL:
            await client.send_message(chat_id = query.from_user.id, text = "You removed the keyboard", reply_markup=ReplyKeyboardRemove())
        case Values.CANCEL_KB_REMOVAL:
            await client.send_message(chat_id = query.from_user.id, text = "You selected No")
        case Values.CONFIRM_DOWNLOAD:
            media_msg = cache.get_session_item(uid, Keys.MEDIA_MESSAGE)
            await query.message.reply("Download started")
            await client.download_media(media_msg)
            await client.send_message(chat_id = uid, text = "Download complete")

async def handle_image(client: Client, message: Message):
    if not message.photo and not message.document:
        return
    print(message)

    # Only image documents supported
    if message.document:
        if message.document.mime_type not in ['image/png', 'image/jpeg', 'image/webp', 'image/tiff']:
            return
    
    botmsg = await message.reply(lang.image_received + " " + lang.downloading_)
    img_file = await client.download_media(message)
    filename = img_file.split('/')[-1] # Last part is filename 
    
    img = Image(file = open(img_file, "rb"))
    height = img.height
    width = img.width

    # Reduce size until height <= 480
    while height > 480:
        height /= 2
        width  /= 2
    
    img.resize(width = int(width), height = int(height))
    await botmsg.edit("Image resized")
    filename = filename.lower().strip('.png').strip('.jpg').strip('.jpeg')
    of = "media/" + filename + ".webp"
    img.save(filename = of)
    await botmsg.edit("WebP image saved")
    
    # await message.reply_document(document= of, caption= message.caption if message.caption else "Your WebP Image")
    await message.reply_document(document = of , caption = message.caption if message.caption else "Here's your WebP image", force_document=True)
    