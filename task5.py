'''5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового
 в строковый тип на кириллице.'''
import platform
import subprocess

import chardet
import locale

default_encoding = locale.getpreferredencoding()

def ping_sites(ping_site):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ['ping', param, '2', ping_site]
    result = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in result.stdout:
        result = chardet.detect(line)
        print('result = ', result)
        line = line.decode(result['encoding']).encode(default_encoding)
        print(line.decode(default_encoding))


ping_sites('yandex.ru')
ping_sites('youtube.com')