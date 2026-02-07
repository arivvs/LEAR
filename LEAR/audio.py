import pyaudiowpatch as pyaudio
import time


class AudioStream(object):
    def __init__(self):
        self.CHUNK = 4096
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 48000
        self.p = pyaudio.PyAudio()
        self.device_index = None

        print("АУДИО: Инициализация поиска Loopback...")

        try:
            wasapi_info = self.p.get_host_api_info_by_type(pyaudio.paWASAPI)

            default_speakers = self.p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
            print(f"АУДИО: Сейчас звук идет через: {default_speakers['name']}")

            if not default_speakers["isLoopbackDevice"]:
                found = False
                for loopback in self.p.get_loopback_device_info_generator():
                    # Если название совпадает с нашими наушниками
                    if default_speakers["name"] in loopback["name"]:
                        self.device_index = loopback["index"]
                        found = True
                        print(f"АУДИО: Успешно подключились к: {loopback['name']}")
                        break

                if not found:
                    print("АУДИО: Точное совпадение не найдено, берем системный поток...")
                    loopback = self.p.get_default_wasapi_loopback()
                    self.device_index = loopback["index"]
            else:
                self.device_index = default_speakers["index"]

        except Exception as e:
            print(f"АУДИО ОШИБКА: Не удалось найти устройство: {e}")

    def get_audio(self):
        if self.device_index is None:
            return

        stream = self.p.open(format=self.FORMAT,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             input=True,
                             input_device_index=self.device_index,
                             frames_per_buffer=self.CHUNK)

        while True:
            try:
                data = stream.read(self.CHUNK)
                yield data
            except Exception as e:
                pass