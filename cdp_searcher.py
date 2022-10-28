import argparse
import ipaddress
import re
import getpass
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)


username=''
password=''
err_ip=0
SHOW_MAC_COMMAND=['show mac-address-table']
ERRORS_OUTPUT=['Invalid input detected at ''^'' marker.','for a list of subcommands']
ARP_COMMAND='show arp'

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


#Основаная проверка ip возвращает в любом случае список
def check_ip(*args):
    ips=[ip for ip in args if check_ipaddress(ip)]
    if ips:
        return ips
    else: raise ValueError("В файле нет правильных ip")

#Дефолтная проверка ip
def check_ipaddress(ip):
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        global err_ip
        err_ip+=1
        return False
    else:
        return True

#Просто чтение строк из файла
# def read_file(file):
#     try:
#         with open(file,'r') as f:
#             return [line.strip() for line in file]
#     except FileNotFoundError:
#         raise ValueError("Файл не найден")

def read_file(file):
    with file:
        return [line.strip() for line in file.readlines()]



#Получаем данные с ввода
parser=argparse.ArgumentParser(description='''Добавить какое-то умное описание''')

source_group=parser.add_mutually_exclusive_group(required=True)
source_group.add_argument('-si', dest='source_ip' ,action="store", type=ipaddress.ip_address, help='''Ip где искать''')
source_group.add_argument('-f',dest='source_file', action="store",
                          type=argparse.FileType('r', encoding='UTF-8'), help='''Путь к файлу с Ip-шниками где искать, ''')

dest_group=parser.add_mutually_exclusive_group(required=True)
dest_group.add_argument('-di', dest='dest_ip' ,action="store", help='''Ip что нужно искать''')
dest_group.add_argument('-m',dest='dest_mac', action="store",type=format_mac, help='''Mac что нужно искать''')

parser.add_argument('-hp', action="store", dest = "hops", default = 10, type=int, help = '''Установка максимального 
количества редиректов, для страхование и избегания зацикливаний, по умолчанию 10''')

args=parser.parse_args()
source_ips= check_ip(*read_file(args.source_file)) if args.source_ip is None else check_ip(str(args.source_ip))
dest_ip=args.dest_ip
dest_mac=args.dest_mac

print(source_ips)
print(dest_ip)
print(dest_mac)
print(err_ip)




#Функция для создание хэндлеров
def form_handler(host,device_type='cisco_ios',username=username,password=password,port=22):\
    return  {
    'device_type': device_type,
    'host': host,
    'username': username,
    'password': password,
    'port': port,
}

# if bool(source_ip is None):
#     print("Omogus")
# else:
#     print("betray")

#Проверка вывода команды на содержание ошибки
def check_error_output(answer, errors=ERRORS_OUTPUT): #TODO добавить эффективную проверку ошибочных выводов при некокректном задание команды
    for error in errors:
        if (answer.find(error)):
            return True
    return False

#Отправляет команды на оборудование и возвращает их в словаре пока возможно не будет использоваться
def send_show_command(device, commands):
    result = {}
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            for command in commands:
                output = ssh.send_command(command)
                result[command] = output
        return result
    except NetmikoTimeoutException:
        raise NetmikoTimeoutException('Что-то пошло не так, таймаут прошел')
    except NetmikoAuthenticationException:
        print('Пробуем ещё раз')




print(send_show_command(form_handler('172.18.226.3',username=input('Username: '),password=getpass.getpass()),['sh macaddress-table']))













