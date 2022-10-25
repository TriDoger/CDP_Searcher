import argparse
import ipaddress
import re

parser=argparse.ArgumentParser(description='''Добавить какое-то умное описание
''')

parser.add_argument('source_ip', action="store", default = '', help='''Ip где искать''')
parser.add_argument('-f', action="store", dest = "source_file", default = '', help = '''Подключение файла с ip 
адресами назначения если необходима проверка на множествах устройств''')
parser.add_argument('-hp', action="store", dest = "hops", default = 10, type=int, help = '''Установка максимального 
количества редиректов, для страхование и избегания зацикливаний, по умолчанию 10''')
parser.add_argument('dest_addres', action="store", help='''Ip или mac что искать''')

args=parser.parse_args()

source_ip=args.source_ip
source_file=args.source_file
hops=args.hops
dest_address=args.dest_addres

print(source_ip)
print(source_file)
print(hops)
print(dest_address)



#Основаная проверка возвращает в любом случае список
def check_ip(*args):
    return [ip for ip in args if check_ipaddress(ip)]

#Дефолтная проверка ip
def check_ipaddress(ip):
    try:
       ipaddress.ip_address(ip)
    except ValueError:
        return False
    else:
        return True

#Проверка мака при помощи регулярок
def check_mac(mac):
    regex = ("^([0-9A-Fa-f]{2}[:-])" +
             "{5}([0-9A-Fa-f]{2})|" +
             "([0-9a-fA-F]{4}\\." +
             "[0-9a-fA-F]{4}\\." +
             "[0-9a-fA-F]{4})$")
    p = re.compile(regex)
    return (True if re.search(p,mac) else False)