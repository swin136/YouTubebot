from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import hide_link
from dotenv import load_dotenv

from common import *

ENV_FILE

if os.path.exists(ENV_FILE):
    load_dotenv('app.env')
else: 
    print(f'Отсутствует файл конфигурации {ENV_FILE}!!')
    quit()
    
bot = Bot(token=os.environ.get('yt_token'), parse_mode="HTML")
dp = Dispatcher(bot)

@dp.message_handler(commands=["start", "help"])
async def start_command(message : types.Message):
    await message.reply("Привет! Отправь мне ссылку на видеоролик YouTube и я пришлю тебе звуковую дорожку.")
    if message.from_user.id not in user_id: write_user_history(userid=message.from_user.id, username=(message.from_user.full_name).strip(), users=user_id) 

    # if is_tlg_user_allow(testuser=message.chat.id, username=message.from_user.username): 
    #     await message.reply("Привет! Отправь мне ссылку на видеоролик YouTube и я пришлю тебе звуковую дорожку.")
    # else: await bot.send_message(message.from_user.id, f'Уважаемый {message.from_user.full_name} для работы с данным сервисом пожалуйста обратитесь к администратору.')


@dp.message_handler()
async def send_audio(message : types.Message):
    # print(message.from_user.username)
    # if is_tlg_user_allow(testuser=message.chat.id, username=message.from_user.username): 
    #     # await bot.send_message(message.from_user.id, message.text)
    if message.from_user.id not in user_id: write_user_history(userid=message.from_user.id, username=(message.from_user.full_name).strip(), users=user_id) 
    if "youtu" not in message.text:
        await bot.send_message(message.from_user.id, 'Нет ссылки на ролик YouTube!')
    else: 
        # Кажется это хрень
        track_title = await a_video_downloader(video_url=message.text)
        await bot.send_message(message.chat.id, text=f"Видеофайл <b>'{track_title['title']}'</b> с YouTube успешно загружен! Приступаем к извлечению звуковой дорожки.")
        # Кажется это хрень
        audio_file = await a_audio_decoder(videofile=track_title['file'])
        file_size = os.path.getsize(audio_file)
        if file_size < MAX_SIZE_AUDIO:
            # Загоняем трек в Shazam
            if file_size < MAX_SAHAZAM_FILE: track_definition = await recognize_track(input_file=audio_file)
            with open(audio_file, 'rb') as audio:
                await bot.send_audio(message.from_user.id, audio, caption=f"Аудиофайл видеоролика <b>'{track_title['title']}'</b>.")
                # Отправляем пользователю автора песни и название трека из Shazam-а
            if  track_definition != None:
                user_text = f"Вы скачали видеоролик <b>'{track_title['title']}'</b>\n" + f"Название ролика - <b>{track_definition['title']}</b>\n" + f"Артист (группа) - <b>{track_definition['subtitle']}</b>"

                if track_definition['image'] != None:
                    await message.answer(
                        f"{hide_link(track_definition['image'])}" + user_text
                        )
                else: await message.answer(user_text)
                # Отправка текста песни - при наличии в Shazam-е
                if track_definition['text'] != None:
                    song_text = f"<b>{track_definition['subtitle']} - {track_definition['title']}</b>\n"
                    for item in track_definition['text']:
                        song_text += f"{item}\n" 
                    await message.answer(song_text) 
                                      
        else: await bot.send_message(message.from_user.id, f"Аудиофайл видеоролика <b>'{track_title['title']}</b> имеет слишком большой размер для передачи! Попробуйте другой видеоролик.")


if __name__ == "__main__":
    read_user_history(user_id)
    executor.start_polling(dp)