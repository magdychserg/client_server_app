"""Пинг ресурса"""

import platform
import subprocess
import threading
from ipaddress import ip_address

result = {'Доступные узлы':'', 'Недоступные узлы':''}
def check_ipadress(value):
    try:
        ipv4= ip_address(value)
    except ValueError:
        raise Exception('Неккоректный ip адрес')
    return ipv4


def ping(ipv4,result, get_list):
    param = "-n" if platform.system().lower() == 'windows' else "-c"
    command = ["ping", param, "1", '-w', '1', str(ipv4)]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    code = process.wait()
    if code == 0:
        result['Доступные узлы'] += f'{ipv4}\n'
        res_string = f'{ipv4}- Узел доступен'
        if not get_list:
            print(res_string)
        return res_string
    else:
        result['Недоступные узлы'] += f'{ipv4}\n'
        res_string = f'{ipv4}- Узел недоступен'
        if not get_list:
            print(res_string)
        return res_string


def host_ping(host_list, get_list=False):
    threads = []

    for host in host_list:
        try:
            ipv4= check_ipadress(host)
        except Exception:
            ipv4 = host

        thread =  threading.Thread(target=ping, args=(ipv4, result, get_list), daemon=True)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    if get_list:
        return result

if __name__ == '__main__':

    host_list=['8.8.8.8', 'ya.ru', '1.1.1.1', 'google.com']
    host_ping(host_list)




