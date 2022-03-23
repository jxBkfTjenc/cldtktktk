from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters
)
import requests
import os
import logging

# ◇─────────────────────────────────────────────────────────────────────────────────────◇

# TikTok Downloader API
API = 'https://single-developers.up.railway.app/tiktok?url='

# Your BOT Token
BOT_TOKEN = os.getenv("BOT_TOKEN")
UPDATES_CHANNEL = os.getenv("UPDATES_CHANNEL")
GROUP_SUPPORT = os.getenv("GROUP_SUPPORT")
BOT_NAME = os.getenv("BOT_NAME")

# TikTok Video URL Types , You Can Add More to This :)
TikTok_Link_Types= ['https://m.tiktok.com','https://vt.tiktok.com','https://tiktok.com','https://www.tiktok.com']

# ParseMode Type For All Messages
_ParseMode=ParseMode.MARKDOWN


# ◇─────────────────────────────────────────────────────────────────────────────────────◇

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ◇─────────────────────────────────────────────────────────────────────────────────────◇

def start_handler(update, context):
    update.message.reply_text(
        f"""👋 Hai! Saya adalah bot telegram yang bisa membantu anda Mengunduh video tiktok\n
🔗 Kirim tautan video TikTok ke BOT ini
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("👥 Support Group", url=f"https://t.me/{GROUP_SUPPORT}"),
                    InlineKeyboardButton("📣 Support Channel", url=f"https://t.me/{UPDATES_CHANNEL}")
                ],
            ]
        ),parse_mode=_ParseMode)

# ◇─────────────────────────────────────────────────────────────────────────────────────◇

# Download Task
def Download_Video(Link,update, context):
    message=update.message
    req=None
    no_watermark=None

    status_msg=message.reply_text('🔄sedang mendownload ....')

    # Getting Download Links Using API
    try:
       req=requests.get(API+Link).json()
       no_watermark=req['no_watermark']
       print('Download Links Generated \n\n\n'+str(req)+'\n\n\n')
    except:
        print('Download Links Generate Error !!!')
        status_msg.edit_text('⁉️ TikTok Downloader API Error !!! Report To Developer : @STM_Developers')
        return
    
    caption_text= f"📥 Download Video TikTok {} Sukses
    🤖 @{BOT_NAME}
"
    
    # Uploading Downloaded Videos to Telegram
    print('Uploading Videos')
    status_msg.edit_text('🔄sedang mengupload....')
    message.reply_video(video=no_watermark,supports_streaming=True,caption=caption_text.format('No Watermark'),parse_mode=_ParseMode)

    # Task Done ! So, Deleteing Status Messages
    status_msg.delete()

# ◇─────────────────────────────────────────────────────────────────────────────────────◇

def incoming_message_action(update, context):
    message=update.message
    if any(word in str(message.text) for word in TikTok_Link_Types):
        context.dispatcher.run_async(Download_Video,str(message.text),update,context)

# ◇─────────────────────────────────────────────────────────────────────────────────────◇

def main() -> None:
    """Run the bot."""
  
    updater = Updater(BOT_TOKEN)

    dispatcher = updater.dispatcher


    # Commands Listning
    dispatcher.add_handler(CommandHandler('start', start_handler, run_async=True))


    # Message Incoming Action
    dispatcher.add_handler( MessageHandler(Filters.text, incoming_message_action,run_async=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main() # 😁 Start

# ◇─────────────────────────────────────────────────────────────────────────────────────◇

# Example For https://github.com/Single-Developers/API/blob/main/tiktok/Note.md

# https://t.me/STMDevelopers
# https://t.me/STM_Developers

# ◇─────────────────────────────────────────────────────────────────────────────────────◇
