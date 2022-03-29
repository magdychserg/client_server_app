
from tabulate import tabulate
from dz1_2 import host_range_ping

def host_range_ping_tab():
    dict= host_range_ping(True)
    print()
    print(tabulate([dict], headers='keys', tablefmt='pipe', stralign='center'))

if __name__=='__main__':
    host_range_ping_tab()