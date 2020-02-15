from colorama import init
from util import *

# Инициализация библиотеки для цветного вывода в консоль
init()

# Инициализация пользователя
# (вход или регистрация)
username = user_initialization()

# Очистка экрана
clear_screen()

# Приветствие после входа в чат
print(Fore.LIGHTRED_EX + 30*"*")
print("Please, be polite and behave.")
print(Fore.LIGHTRED_EX + 30*"*")
print()
print("Type '/q' to quit")
print()

try:
    while True:
        print(Fore.BLACK + Style.BRIGHT + 'Say:' + Style.RESET_ALL, end=' ')
        text = input()

        # Если пользователь печатает служебную команду /q или /Q,
        # то происходит выход из чата
        if text.lower() == '/q':
            break

        response = requests.post(
            SERVER_ADDR + '/send',
            json={"username": username, "text": text}
        )

except KeyboardInterrupt:
    # Если пользователь аварийно завершает работу,
    # то перед завершением посылаем запрос серверу на отключение
    pass

# Запрос на отключение от сервера
requests.post(
      SERVER_ADDR + '/disconnect',
      json={"username": username}
    )

# Прощание с пользователем
print()
print(Fore.LIGHTRED_EX + "You're leaving. Bye!")

