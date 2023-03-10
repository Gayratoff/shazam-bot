from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import CommandStart, CommandHelp, Command
from aiogram.utils import executor
from pytube import YouTube
from shazamio import Shazam, Serialize
import pytube
from os import remove, rename

ADMINS = ['ID','ID VAHOKAZO']

bot=Bot(token="TOKEN",parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(CommandStart())
async def MistrUz(message: types.Message):
    await message.reply(f"Salom {message.from_user.full_name}!")



@dp.message_handler(content_types=['audio'])
async def MistrUz(message: types.Message):
    msg = await message.reply("🔎")
    file_id = message.audio.file_id
    file =  await bot.get_file(file_id)
    path = file.file_path
    await bot.download_file(path,f"{message.message_id}.mp3")
    shazam = Shazam()
    out = await shazam.recognize_song(f"{message.message_id}.mp3")
    print(out)
    r = out['matches']
    if r == []:
        await msg.delete()
        await message.answer("Musiqa topilmadi")
        remove(f"{message.message_id}.mp3")
    elif r !=[]:
        track = out['track']
        title  = track['title']
        subtitle = track['subtitle']
        await message.reply(f"<b>{title} - {subtitle}</b> Siz qidirgan musiqa...")
        remove(f"{message.message_id}.mp3")
        data = Serialize.full_track(data=out)
        yt = await shazam.get_youtube_data(link=data.track.youtube_link)
        url =yt['actions'][0]['uri']
        print(url)
        if url != 'No result':
            ytb =  YouTube(url)
            audio =ytb.streams.filter(only_audio=True)[1]
            out_audio = audio.download(output_path=".")
            new_music =f"{title} - {subtitle}.mp3"
            rename(out_audio,new_music)
            with open(f"{new_music}",'rb') as music:
                await  message.reply_audio(audio=music,caption=f"{title} - {subtitle}")



@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam")

    await message.answer("\n".join(text))

async def on_startup_notifiy(dp:Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "<b>Bot ishga tushdi...</b>")
        except:
            pass

async def on_startup(dispatcher):
    await on_startup_notifiy(dispatcher)

if __name__ =="__main__":
    executor.start_polling(dp,on_startup=on_startup,skip_updates=True)