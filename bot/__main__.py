import pyrogram, traceback, time, asyncio
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from .plugins.menu import menu
from bot import bot, Config, LOGS
from pyrogram import idle


## STARTUP ##
async def startup():
    await bot.start()
    LOGS.info(f'[Started]: @{(await bot.get_me()).username}')
    await idle()
    await bot.stop()

@bot.on_message(filters.incoming & filters.command(["start"]))
async def help_message(bot, message):
    if message.from_user.id not in Config.OWNER:
      return await message.reply_text("**You Are Not Authorised To Use This Bot**")
    await menu(bot, message) 
    
bot.loop.run_until_complete(startup())    
    
  
