import itertools
import socket
import sys

password_list = "passwords.txt"


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
        yield content[row].strip()


def connection(ip=None, port=None):
    if ip is None or port is None:
        ip, port = get_connection_data()

    gen = generate_from_file(password_list)

    response = ""
    with socket.socket() as sock:
        try:
            sock.connect((ip, port))
            for x in gen:
                for y in all_casings(x):
                    sock.send(y.encode())
                    response = sock.recv(1024).decode()
                    if "Connection success!" in response:
                        print(y)
                        break
        except ConnectionRefusedError:
            print(response)
        except ConnectionAbortedError:
            sys.exit("Connection aborted [Windows]")


if __name__ == "__main__":
    connection()
