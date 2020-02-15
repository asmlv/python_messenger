from getpass import getpass
from os import name, system
import requests
from colorama import Fore, Style

# Вспомогательная константа, чтобы не печатать каждый раз адрес сервера
SERVER_ADDR = "http://127.0.0.1:5000"


def clear_screen():
    """
        Очистка экрана
    """
    # for windows
    if name == 'nt':
        _ = system('cls')
        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def log_in():
    """
        Окно для ввода логина и пароля

        Если авторизация неуспешна,
        то пользователю предлагается повторить попытку,
        вернуться в меню или выйти из чата
    """
    clear_screen()
    print(Fore.LIGHTRED_EX + "Logging in")
    print(Fore.YELLOW + Style.DIM + 30 * "*")
    print(Fore.YELLOW + 'Username:', end=' ')
    username = input()
    password = getpass()
    print(Fore.YELLOW + 30 * "*")

    # Отправляем введённые данные на сервер для проверки
    response = requests.post(
        SERVER_ADDR + '/connect',
        json={"username": username, "password": password}
    )

    # Если вход не разрешён, то предупреждаем пользователя
    # и отклоняем авторизацию
    if not response.json()['ok']:
        print()
        print(Fore.RED + 'Access denied' + Style.BRIGHT)
        print()
        print("[1] Try again")
        print("[2] Back")
        print("[q] Quit")

        option = input()
        if option == '1':
            log_in()
        if option == '2':
            user_initialization()
        if option.lower() == 'q':
            exit(0)

    # Если всё ок, возвращаем имя пользователя,
    # чтобы он мог начать общение в чате
    return username


def register():
    """
        Окно для регистрации нового пользователя

        Если такой пользователь уже существует,
        то регистрация отклоняется,
        а пользователю предлагается повторить попытку,
        вернуться в меню или выйти из чата
    """
    clear_screen()
    print(Fore.LIGHTRED_EX + "Registration")
    print(Fore.YELLOW + Style.DIM + 30 * "*")
    print(Fore.YELLOW + 'New username:', end=' ')
    username = input()
    password = getpass()
    print(Fore.YELLOW + 30 * "*")
    response = requests.post(
        SERVER_ADDR + '/register',
        json={"username": username, "password": password}
    )
    if not response.json()['ok']:
        print()
        print(Fore.RED + 'Such username already exists!' + Style.BRIGHT)
        print()
        print("[1] Try again")
        print("[2] Back")
        print("[q] Quit")
        option = input()
        if option == '1':
            log_in()
        if option == '2':
            user_initialization()
        if option.lower() == 'q':
            exit(0)
    else:
        response = requests.post(
            SERVER_ADDR + '/connect',
            json={"username": username, "password": password}
        )

    return username


def user_initialization():
    """
        Инициализация пользователя

        После запуска чата пользователю предоставляется возможность
        войти в чат под своим именем и паролем,
        зарегистрировать новое имя
        или выйти из чата
    """
    clear_screen()
    print(Fore.LIGHTRED_EX + "Welcome to our chat!")
    print(Fore.YELLOW + Style.DIM + 30 * "*")
    print("[1] Log in");
    print("[2] Register");
    print("[q] Quit");
    print(Fore.YELLOW + Style.DIM + 30 * "*" + Style.RESET_ALL)
    username = ""
    option = input();
    if option == '1':
        username = log_in()
    elif option == '2':
        username = register()
    if option.lower() == 'q':
        exit(0)

    return username
