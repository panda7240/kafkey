# -*- coding:utf-8 -*-


import socket

# 判断是否是ip:port
def is_ip_port(ip_port):
    ip_port_arr = ip_port.split(':')
    if len(ip_port_arr) != 2 or isinstance(ip_port_arr[1], int):
        return False
    return is_internal_ip(ip_port_arr[0])


# 判断是否是内网ip
def is_internal_ip(ip):
    if not check_ip(ip):
        return False
    ip = ip_into_int(ip)
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    return ip >> 24 == net_a or ip >> 20 == net_b or ip >> 16 == net_c


# 将ip转成int
def ip_into_int(ip):
    return reduce(lambda x, y: (x << 8) + y, map(int, ip.split('.')))


# 判断是否是ip
def check_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False
