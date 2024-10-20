import httpx
import asyncio
import mimetypes
import os

from consts import DOWNLOAD_DELAY_API, WRITE_DESCRIPTION


class AsyncFileDownloader:
    def __init__(self, files_info, output_way):
        self.files_info = files_info
        self.output_way = output_way

        if not os.path.exists(output_way):
            os.makedirs(output_way)

    async def download_file(self, session: httpx.AsyncClient, url: str, base_filename: str, delay=0.0, description=None) -> None:
        await asyncio.sleep(delay)
        try:
            async with session.stream("GET", url) as resp:
                resp.raise_for_status()
                content_type = resp.headers.get('Content-Type')
                extension = mimetypes.guess_extension(content_type.split(';')[0].strip()) if content_type else '.bin'
                filename = f"{self.output_way}{base_filename}{extension}"

                total_size = int(resp.headers.get('Content-Length', 0))
                downloaded_size = 0
                with open(filename, 'wb') as f:
                    async for chunk in resp.aiter_bytes():
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        progress = int((downloaded_size / total_size) * 100)
                    if description and WRITE_DESCRIPTION:  # TODO: fix that
                        if "text" in description:
                            f.write(b"\xff\xfe" + bytes(f"{description['text']}", 'utf-8'))
                        if "orig_url_to_album" in description:
                            pass
        except Exception as e:
            print(f"При загрузке файла {base_filename} из {url} произошла ошибка: {str(e)}")

    async def run(self):
        async with httpx.AsyncClient() as session:
            tasks = [self.download_file(session, e.get_url(), e.get_filename(), i * DOWNLOAD_DELAY_API, e.get_description()) for i, e in enumerate(self.files_info)]
            await asyncio.gather(*tasks)


class FileInfo:
    def __init__(self, url: str, filename: str, description=None):
        if description is None:
            description = {}
        self.url = url
        self.filename = filename
        self.description = description

    def get_url(self):
        return self.url

    def get_filename(self):
        return self.filename

    def get_description(self):
        return self.description