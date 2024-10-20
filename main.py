from tabulate import tabulate
import asyncio
from modules.vk import VkApi
from threading import Thread

from consts import *
from useful import *
from modules.downloader import AsyncFileDownloader, FileInfo


if __name__ == "__main__":
    vk = VkApi(token=TOKEN)
    username = input("Введите юзернейм: ").strip()
    user_resp = vk.request("users.get", {"user_ids": username}).json()
    try:
        if not user_resp["response"]:
            raise Exception("Пользователь не найден")
        user_id = user_resp["response"][0]["id"]
        album_resp = vk.request("photos.getAlbums", {"owner_id": user_id}).json()["response"]
        if album_resp["count"] == 0:
            print("У пользователя нет альбомов")
        else:
            table = [(i + 1, e["title"], e["size"]) for i, e in enumerate(album_resp["items"])]
            print(tabulate(table, headers=("№", "Название", "Шт.")))
            num = int(input("Введите № альбома: "))
            if num > len(table) or num <= 0:
                raise ValueError("Неверный номер альбома")
            num -= 1
            print(f"Выбран альбом '{table[num][1]}', кол-во фото: {table[num][2]}")
            print(f"Описание: {album_resp['items'][num]['description'] if album_resp['items'][num]['description'] else '---'}")
            print(f"Создан: {time_convert(album_resp['items'][num]['created'])}\tОбновлён: {time_convert(album_resp['items'][num]['updated'])}")
            count = int(input('Введите количество фото, которое надо загрузить ("0", если хотите скачать все фото): '))
            rev = bool(int(input('Введите, в каком порядке загрузить (0 - хронологический, 1 - антихронологический): ')))
            size = table[num][2]
            left = 0
            if count != 0:
                offset_input = int(input('Введите номер фото, с которого начать загрузку ("0", если загрузить с начала альбома): '))
                if offset_input < 0 or offset_input >= size:
                    raise ValueError("Неправильное значение")
                left = offset_input
            elif count == 0:
                count = size

            folder_name = f'{user_resp["response"][0]["first_name"]}_{user_resp["response"][0]["last_name"]}/{table[num][1]}/'

            print("Загрузка началась!")
            while count != 0:
                photo_params = {
                    "owner_id": user_id,
                    "album_id": album_resp['items'][num]['id'],
                    "offset": left,
                    "count": min(MAX_PHOTO_COUNT_PER_REQUEST, count),
                    "rev": rev
                }
                #print(left, count, photo_params)
                photo_resp = vk.request("photos.get", photo_params).json()["response"]
                files_info = [FileInfo(
                    e["orig_photo"]["url"],
                    str(left + i + 1),
                    {
                        "text": e["text"]
                    }) for i, e in enumerate(photo_resp["items"])]
                left += min(MAX_PHOTO_COUNT_PER_REQUEST, count)
                count -= min(MAX_PHOTO_COUNT_PER_REQUEST, count)
                async_downloader = AsyncFileDownloader(files_info, CONFIG["CONSTS"]["output"] + folder_name)

                download_thread = Thread(target=lambda: asyncio.run(async_downloader.run()))
                download_thread.run()
                time.sleep(DOWNLOAD_GROUP_DELAY)
            print("Загрузка завершена!")
    except Exception as e:
        print(e)