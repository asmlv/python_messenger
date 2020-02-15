from datetime import datetime
from time import sleep
from colorama import init
from util import *


def print_current_online(online_users):
    """
        Напечатать на экран пользователей, которые сейчас онлайн
    """
    online = len(online_users)
    print(Fore.LIGHTBLUE_EX + f"Current online ({online})", end='')
    if online != 0:
        print(": ", end='')
        online = ""
        for online_user in online_users:
            online += online_user + ', '
        print(online[:-2], end='')
    print(Style.RESET_ALL)


# Очистка экрана
clear_screen()

# Инициализация библиотеки для цветного вывода в консоль
init()

# Запоминаем время последнего принятого сообщения
last_message_time = 0

# Отправляем запрос серверу, чтобы выяснить, кто сейчас в сети
response = requests.get(
        SERVER_ADDR + '/check_users'
    )
data = response.json()
print_current_online(data['online'])

while True:
    # Отправляем запрос, чтобы получить историю сообщений
    # старше последнего принятого сообщения
    response = requests.get(
        SERVER_ADDR + '/history',
        params={'after': last_message_time}
    )

    data = response.json()

    # Печатаем новые сообщения на экан
    for message in data['messages']:
        # float -> datetime
        beauty_time = datetime.fromtimestamp(message['time'])
        beauty_time = beauty_time.strftime('%H:%M:%S')
        sender_name = message['username']
        print(Fore.CYAN + beauty_time + ' ' + Fore.GREEN + sender_name, end=': ')
        print(Fore.WHITE + message['text'])
        last_message_time = message['time']

    # Проверяем состояние пользователей
    # чтобы напечатать в общий чат,
    # если произошли какие-то изменения состояния пользователей
    response = requests.get(
        SERVER_ADDR + '/check_users'
    )

    data = response.json()

    # Если кто-то недавно отключился,
    # и об этом ещё не было напечатано в общий чат,
    # тогда печатаем имя пользователя, который отключился, и время отключения
    disconnected_users = data['disconnected']
    for disconnected_user in disconnected_users:
        beauty_time = datetime.now()
        beauty_time = beauty_time.strftime('%H:%M:%S')
        print(Fore.CYAN + beauty_time + " " +
              Fore.LIGHTRED_EX + disconnected_user + " has left" +
              Style.RESET_ALL)

    # Если кто-то недавно подключился,
    # и об этом ещё не было оповещения в общем чате,
    # тогда печатаем имя и время подключения
    connected_users = data['connected']
    for connected_user in connected_users:
        beauty_time = datetime.now()
        beauty_time = beauty_time.strftime('%H:%M:%S')
        print(Fore.CYAN + beauty_time + " " +
              Fore.LIGHTRED_EX + connected_user + " has joined" +
              Style.RESET_ALL)

    # Если были подключенные и отключенные пользователи,
    # то необходимо обновить список пользователей, которые сейчас в сети
    if len(disconnected_users) != 0 or len(connected_users) != 0:
        print_current_online(data['online'])

    # Ждём секунду, чтобы снова повторить все действия выше
    sleep(1)
