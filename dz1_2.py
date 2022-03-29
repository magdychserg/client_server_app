from dz1 import check_ipadress, host_ping

def host_range_ping(get_list=False):

    while True:
        start_ip= input('Enter start ip: ')
        try:
            ipv4_start =check_ipadress(start_ip)
            last_octet = int(start_ip.split('.')[3])
            break
        except Exception:
            print(Exception)

    while True:
        end_ip = input('How many addresses to check: ')
        if not end_ip.isnumeric():
            print('Enter numeric')
        else:
            if (last_octet + int(end_ip))> 255+1:
                print(f'max amount host {255+1 - last_octet}')
            else:
                break
    host_list = []
    [host_list.append(str(ipv4_start+x)) for x in range(int(end_ip))]
    if not get_list:
        host_ping(host_list)
    else:
        return host_ping(host_list, True)

if __name__=='__main__':
    host_range_ping()