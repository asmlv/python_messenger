import time
from datetime import datetime
from flask import Flask, request
from colorama import init

# Инициализация библиотеки для цветного вывода в консоль
init()

# Инициализация Flask
app = Flask(__name__)

# БД сообщений
# {'username': "str", 'text': "str", 'time': float}
messages = [
    {'username': 'jack', 'text': 'Hello', 'time': time.time()},
    {'username': 'mary', 'text': 'Hi, jack!', 'time': time.time()}
]

# БД пользователей ({'name' : 'password'})
users = {
    # username: password
    'jack': 'black',
    'mary': '12345'
}

# БД пользователей, которые сейчас в сети
online = set()

# БД пользователей, которые недавно отключились из чата
disconnected = set()

# БД пользователей, которые недавно подклбчились к чату
connected = set()


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/status")
def status():
    return {
        'status': True,
        'time': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        'registered_users': len(users),
        'messages_amount': len(messages)
    }


@app.route("/history")
def history():
    """
    request: ?after=1234567890.4567
    response: {
        "messages": [
            {"username": "str", "text": "str", "time": float},
            ...
        ]
    }
    """
    after = float(request.args['after'])
    filtered_messages = [m for m in messages if after < m['time']]
    return {'messages': filtered_messages}


@app.route("/send", methods=['POST'])
def send():
    """
    request: {"username": "str", "text": "str"}
    response: {"ok": true}
    """
    data = request.json  # JSON -> dict
    username = data['username']
    text = data['text']

    new_message = {'username': username, 'text': text, 'time': time.time()}
    messages.append(new_message)

    return {"ok": True}


@app.route("/connect", methods=['POST'])
def connect():
    """
       request: {"username": "str", "password": "str"}
       response: {"ok": true}
    """

    data = request.json  # JSON -> dict
    username = data['username']
    password = data['password']

    # если такой пользователь существует -> проверим пароль
    # иначе отказ
    if username not in users:
        return {"ok": False}
    else:
        real_password = users[username]
        if real_password != password:
            return {"ok": False}

    online.add(username)
    connected.add(username)

    return {
        'ok': True,
        'time': datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    }


@app.route("/disconnect", methods=['POST'])
def disconnect():
    """
       request: {"username": "str"}
       response: {"ok": true}
    """

    data = request.json  # JSON -> dict
    username = data['username']
    online.remove(username)
    disconnected.add(username)

    return {
        'ok': True,
        'time': datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    }


@app.route("/register", methods=['POST'])
def register():
    """
       request: {"username": "str", "password" : "str"}
       response: {"ok": true}
    """
    data = request.json  # JSON -> dict
    username = data['username']
    if username not in users:
        users[username] = data['password']
    else:
        return {"ok": False}

    return {
        'ok': True,
        'time': datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    }


@app.route("/check_users")
def check_users():
    """
          request: -
          response: {"connected": [], "disconnected" : [], "online" : []}
    """
    _disconnected = list(disconnected)
    _connected = list(connected)
    disconnected.clear()
    connected.clear()
    return {
        'connected': _connected,
        'disconnected': _disconnected,
        'online': list(online),
    }

app.run()
