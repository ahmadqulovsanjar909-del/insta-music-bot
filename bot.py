import os
import telebot
import yt_dlp

TOKEN = "9256042725:AAFuoaCoVaqDnBF1w0Q2G01KvnzXlpw2w00"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(bot_message):
  bot.reply_to(
      bot_message,
      "Salom! Menga Instagram video havolasini yoki izlayotgan musiqangiz"
      " nomini yuboring, men uni yuklab beraman! 📥",
  )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  text = message.text.strip()

  if "instagram.com" in text:
    bot.reply_to(
        message, "⏳ Instagram dan video yuklab olinmoqda, biroz kuting..."
    )
    try:
      ydl_opts = {
          "format": "mp4",
          "outtmpl": "downloads/%(id)s.%(ext)s",
      }
      os.makedirs("downloads", exist_ok=True)
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(text, download=True)
        filename = ydl.prepare_filename(info)

      with open(filename, "rb") as video_file:
        bot.send_video(message.chat.id, video_file)
      os.remove(filename)
    except Exception as e:
      bot.reply_to(message, f"❌ Xatolik yuz berdi: {str(e)}")
  else:
    bot.reply_to(message, f"🔍 '{text}' bo'yicha musiqa qidirilmoqda...")
    try:
      ydl_opts = {
          "format": "bestaudio/best",
          "postprocessors": [{
              "key": "FFmpegExtractAudio",
              "preferredcodec": "mp3",
              "preferredquality": "192",
          }],
          "outtmpl": "downloads/%(id)s.%(ext)s",
      }
      os.makedirs("downloads", exist_ok=True)
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        query = f"ytsearch1:{text}"
        info = ydl.extract_info(query, download=True)
        if "entries" in info:
          info = info["entries"][0]
        filename = ydl.prepare_filename(info)
        audio_filename = filename.rsplit(".", 1)[0] + ".mp3"

      with open(audio_filename, "rb") as audio_file:
        bot.send_audio(
            message.chat.id,
            audio_file,
            title=info.get("title", "Musiqa"),
            performer=info.get("uploader", "Unknown"),
        )
      os.remove(audio_filename)
    except Exception as e:
      bot.reply_to(message, f"❌ Xatolik yuz berdi: {str(e)}")


if name == "main":
  bot.infinity_polling()
