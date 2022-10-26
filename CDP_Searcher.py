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
#Поддерживает форматы записи '01-23-45-67-89-AB' '01:23:45:67:89:AB'
#0123.4567.89AB не зависит от регистра
def check_mac(mac):
    regex = ("^([0-9A-Fa-f]{2}[:-])" +
             "{5}([0-9A-Fa-f]{2})|" +
             "([0-9a-fA-F]{4}\\." +
             "[0-9a-fA-F]{4}\\." +
             "[0-9a-fA-F]{4})$")
    p = re.compile(regex)
    return (True if re.search(p,mac) else False)

#Форматирование mac под формат сisco
#Можно подать свою регулярку для парсинга мака
def format_mac(mac,regex=r'[ .|:|-]'):
    str=''
    if check_mac(mac):
        spl_mac=re.split(regex, mac.lower())
        for oktet in spl_mac:
            str = str + oktet
            if len(oktet)==4 and len(str)!=14:
                str=str+'.'
            elif (len(str)==4 or len(str)==9) and len(str)!=14:
                str=str+'.'
    return str



