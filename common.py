from pytube import YouTube
import moviepy.editor
from pathlib import Path
import os, platform
from shazamio import Shazam
# import datetime
from datetime import datetime



telegram_bot_token = "YT_Bot_Token"
user_id = []

# Каталог для сохранения файлов
WORK_FOLDER = 'data'
# Максимальный размер файла для передачи через бот (поставил примерно)
MAX_SIZE_AUDIO = 51380224

# Максимальный размер файла для прогонки через Shazam
MAX_SAHAZAM_FILE =10485760 
# https://www.thepythoncode.com/article/make-a-youtube-video-downloader-in-python

HISTORY_FILE = 'history.txt'
ENV_FILE = 'app.env'

async def a_video_downloader(video_url : str):
    """
    # the function takes the video url as an argument
    """
    # print("Вызов функции скачивания видео")
    my_video = YouTube(url=video_url)
    result = my_video.streams.get_lowest_resolution().download(WORK_FOLDER)
    # print(result)
    return {'title' : my_video.title, 'file' : result}

async def a_audio_decoder(videofile : str):
    """
    the function takes the audio track from video file
    """
    # input(f"Извлекаем аудио из {videofile } ")
    video_file = Path(videofile)
    # input(video_file)
    video = moviepy.editor.VideoFileClip(f'{video_file}')
    audio = video.audio
    audiofile = WORK_FOLDER + os.sep+ f"{video_file.stem}.mp3"
    # input(audiofile)
    audio.write_audiofile(audiofile)
    video.close()
    audio.close()
    # Удаляем видеофайл
    os.remove(videofile)
    return audiofile


async def recognize_track(input_file : str):
    """
    у меня функция заработала под Линуксом, и то только после
    установки пакета ffmpeg
    Под виндой что-то пошло не так - вероятно дело в моей криворукости
    """
    # Определяем платформу, где запущен скрипт
    host = platform.system().lower()
    if host == 'linux':
        shazam = Shazam()
        trackinfo = await shazam.recognize_song(input_file)
        if trackinfo.get('track') != None:
            result = {
                'title' : trackinfo['track']['title'], 
                'subtitle' : trackinfo['track']['subtitle'],
                }
            try:    # Ишем картинку
                result['image'] = trackinfo['track']['images']['background']
            except KeyError:
                result['image'] = None
            try:    # Ищем текст песни
                result['text'] = trackinfo['track']['sections'][1]['text']
            except KeyError:
                result['text'] = None
            return result
        else: return None
    else: return None

    
def read_user_history(users : list):
        """
        Считываем истрорию юзверей из файла HISTORY_FILE
        """
        if os.path.exists(HISTORY_FILE): 
            f = open(file=HISTORY_FILE, mode="rt")
            try:
                for word in [str(item).replace("\n", "") for item in f.readlines() if len(item.strip()) > 0]:
                    users.append(int(word.split(":")[0]))
            finally: f.close()

            # for word in lst: users.append(int(word.split(":")[0]))
                # newlst = item.split(":")
                # users.append(int(newlst[0])) 
                

def write_user_history(userid : int, username: str, users : list):
    users.append(userid)
    try:
        f = open(file=HISTORY_FILE, mode="at")
        f.write(f"{userid}:{username}:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    finally: f.close()

# if __name__ == "__main__":
#     read_user_history(user_id)
#     print(__file__)
#     print(user_id)





