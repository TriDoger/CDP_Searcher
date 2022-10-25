import ipaddress
import re

#Тест проверок IP
# def check_ip(*args):
#     return [ip for ip in args if check_ipaddress(ip)]
#
# def check_ipaddress(ip):
#     try:
#        ipaddress.ip_address(ip)
#     except ValueError:
#         return False
#     else:
#         return True
#
# ips='1.1.1.1'
# print(check_ip(ips))

macs=['01-23-45-67-89-AB','01:23:45:67:89:AB','0123.4567.89AB','01-23-45-67-89-AH','0123.4567.89ab']

#Тест проверка мака при помощи регулярок
def check_mac(mac):
    regex = ("^([0-9A-Fa-f]{2}[:-])" +
             "{5}([0-9A-Fa-f]{2})|" +
             "([0-9a-fA-F]{4}\\." +
             "[0-9a-fA-F]{4}\\." +
             "[0-9a-fA-F]{4})$")
    p = re.compile(regex)
    return (True if re.search(p,mac) else False)
for mac in macs:
    print (check_mac(mac))