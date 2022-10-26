import argparse
import ipaddress
import re

#Проверка мака при помощи регулярок
#Поддерживает форматы записи '01-23-45-67-89-AB' '01:23:45:67:89:AB'
#0123.4567.89AB не зависит от регистра
def check_mac(mac, regex="^([0-9A-Fa-f]{2}[:-])" +
                         "{5}([0-9A-Fa-f]{2})|" +
                         "([0-9a-fA-F]{4}\\." +
                         "[0-9a-fA-F]{4}\\." +
                         "[0-9a-fA-F]{4})$"):
    if re.search(re.compile(regex), mac):
        return mac
    else:
        raise TypeError("Мак указан некоректно")



#Форматирование mac под формат сisco
#Можно подать свою регулярку для парсинга мака
def format_mac(mac, regex=r'[ .|:|-]'):
    str = ''
    if check_mac(mac):
        spl_mac = re.split(regex, mac.lower())
        for oktet in spl_mac:
            str = str + oktet
            if len(oktet) == 4 and len(str) != 14:
                str = str + '.'
            elif (len(str) == 4 or len(str) == 9) and len(str) != 14:
                str = str + '.'
    return str


#Получаем данные с ввода
parser=argparse.ArgumentParser(description='''Добавить какое-то умное описание''')

source_group=parser.add_mutually_exclusive_group(required=True)
source_group.add_argument('-si', dest='source_ip' ,action="store", default = '', type=ipaddress.ip_address, help='''Ip где искать''')
source_group.add_argument('-f',dest='source_file', action="store",
                          type=argparse.FileType('r', encoding='latin-1'), help='''Путь к файлу с Ip-шниками где искать, ''')

dest_group=parser.add_mutually_exclusive_group(required=True)
dest_group.add_argument('-di', dest='dest_ip' ,action="store", default = '', help='''Ip что нужно искать''')
dest_group.add_argument('-m',dest='dest_mac', action="store", default = '',type=format_mac, help='''Mac что нужно искать''')

parser.add_argument('-hp', action="store", dest = "hops", default = 10, type=int, help = '''Установка максимального 
количества редиректов, для страхование и избегания зацикливаний, по умолчанию 10''')

args=parser.parse_args()

print(args.dest_mac)
print(args.source_ip)

username=''
password=''
err_ip=0


#Основаная проверка ip возвращает в любом случае список
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


#Функция для создание хэндлеров
def form_handler(host,device_type='cisco_ios',username=username,password=password,port=22):\
    return  {
    'device_type': device_type,
    'host': host,
    'username': username,
    'password': password,
    'port': port,
}

#Просто чтение строк из файла
def read_file(filename):
    try:
        with open(filename) as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        raise ValueError("Файл не найден")

# if bool(check_ip(source_addres)):
#     print("Omogus")
# else:
#     print("betray")
#
# username=input('Username: ')
# password=getpass.getpass()












