import pyrogram, asyncio, os, re
from pyrogram import Client
from bot import bot, Config, LOGS
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram import filters
from .classes import functions, ffmpeg
from .devtools import progress_for_pyrogram
import time

async def menu(bot, message):
  await bot.send_message(
    chat_id=message.from_user.id,
    text="Select Any Option To Continue",
    reply_markup=InlineKeyboardMarkup(remark)
  )

vid_menu = [
  [
    InlineKeyboardButton('Convert To MP4', callback_data="mp4"),
    InlineKeyboardButton('Convert To MKV', callback_data="mkv"),
  ],
  [
    InlineKeyboardButton('Convert To File', callback_data="file"),
    InlineKeyboardButton('Convert To Video', callback_data="video"),
  ],
  [
    InlineKeyboardButton('BACK', callback_data="back"),
  ]
]

back =[
  [
    InlineKeyboardButton('BACK', callback_data="back")
  ]
]

# remark = [
#     [InlineKeyboardButton('Media Information', callback_data="info")],
#     [InlineKeyboardButton('Sample', callback_data="sample")]
# ]
remark = [
  [
    InlineKeyboardButton('Media Information', callback_data="info"),
    InlineKeyboardButton('Sample', callback_data="sample")
  ],
  [
    InlineKeyboardButton('Video Converter', callback_data="vid_menu")
  ],
]

@bot.on_callback_query()
async def get_info(bot: Client, m: CallbackQuery):
 if "info" == m.data:
  Y = await m.edit_message_text(
        text="**Send Video**",
        reply_markup=InlineKeyboardMarkup(back)
  )
  Input1 = await bot.listen(m.from_user.id)
  await Y.delete(True)
  if Input1.video:
   Msg = await bot.send_message(m.from_user.id, "**📥 Trying To Downloading 📥**")
   try:
    d_start = time.time()
    filepath = await bot.download_media(
        message=Input1,  
        file_name=Config.DOWNLOAD_DIR,
        progress=progress_for_pyrogram,
        progress_args=(
          bot,
          "**📥 Trying To Downloading 📥**",
          Msg,
          d_start
        )
    )
    await Msg.delete(True) 
    link = await functions.mediainfo(filepath=filepath)
    await bot.send_message(m.from_user.id, text="Here Is The Mediainfo", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('MEDIAINFO', url=link)]]))
    os.remove(filepath)
   except Exception as e:
    LOGS.info(e)
    
 if "back" == m.data:
  await m.edit_message_text(
    text="Select Any Option To Continue",
    reply_markup=InlineKeyboardMarkup(remark)
  )
  
 if "sample" == m.data:
  Y = await m.edit_message_text(
        text="**Send Video**",
        reply_markup=InlineKeyboardMarkup(back)
  )
  Input1 = await bot.listen(m.from_user.id)
  await Y.delete(True)
  if Input1.video:
   Msg = await bot.send_message(m.from_user.id, "**📥 Trying To Downloading 📥**")
   try:
    d_start = time.time()
    filepath = await bot.download_media(
        message=Input1,  
        file_name=Config.DOWNLOAD_DIR,
        progress=progress_for_pyrogram,
        progress_args=(
          bot,
          "**📥 Trying To Downloading 📥**",
          Msg,
          d_start
        )
    )
    await Msg.edit("Generating Sample")
    sample = await functions.sample(filepath=filepath)
    duration = await ffmpeg.duration(filepath=sample)
    thumb = await functions.screenshot(filepath=sample)
    width, height = await ffmpeg.resolution(filepath=sample)
    await Msg.edit("Starting To Upload")
    u_start = time.time()
    await bot.send_video(
      video=sample,
      chat_id=m.from_user.id, 
      supports_streaming=True,
      file_name=sample, 
      thumb=thumb, 
      duration=duration, 
      width=width, 
      height=height, 
      caption="**SAMPLE**",
      progress=progress_for_pyrogram,
      progress_args=(
        bot,
        "**⬆️ Trying To Upload ⬆️**",
        Msg,
        u_start
      )
    )
    os.remove(sample)
    os.remove(filepath)
    os.remove(thumb)
    await msg.delete(True)
   except Exception as e:
    LOGS.info(e)
 if "vid_menu" == m.data:
  Y = await m.edit_message_text(
        text="__Choose Your Appropriate Action 👍__",
        reply_markup=InlineKeyboardMarkup(vid_menu)
   )
 if "mp4" == m.data:
  Y = await m.edit_message_text(
        text="Send Your Video 👍",
        reply_markup=InlineKeyboardMarkup(back)
  )
  input1 = await bot.listen(m.from_user.id)
  await Y.delete(True)
  if input1.video:
    msg = await bot.send_message(m.from_user.id, "**📥 Trying To Downloading 📥**")
    d_start = time.time()
    filepath = await bot.download_media(
      message=input1,
      file_name=Config.DOWNLOAD_DIR,
      progress=progress_for_pyrogram,
      progress_args=(bot, "Trying To Download", msg, d_start)
    )
    await msg.edit("Converting To MP4")
    mp4 = await ffmpeg.mp4(filepath=filepath)
    duration = await ffmpeg.duration(filepath=mp4)
    thumb = await functions.screenshot(filepath=mp4)
    width, height = await ffmpeg.resolution(filepath=mp4)
    base, extension = os.path.split(mp4)
    await msg.edit("Starting To Upload")
    u_start = time.time()
    await bot.send_video(
      video=mp4,
      chat_id=input1.from_user.id,
      supports_streaming=True,
      file_name=extension,
      thumb=thumb,
      duration=duration,
      width=width,
      height=height,
      caption=extension,
      progress=progress_for_pyrogram,
      progress_args=(bot, "Trying To Upload", msg, u_start)
    )
    await msg.delete(True)
    os.remove(thumb)
    os.remove(filepath)
    os.remove(mp4)
