import itertools
import socket
import sys


def password_generator(length):
    """
    Generate a password
    """
    chars = [x for x in "abcdefghijklmnopqrstuvwxyz0123456789"]

    possibilities = itertools.product(chars, repeat=length)

    return possibilities


def get_connection_data():
    """
    Get the connection data from the user
    """
    ip, port, message = "", "", ""
    # use for terminal input
    # try:
    #     ip, port, message = str(input()).split(" ")
    # except ValueError:
    #     print("Invalid input")
    #     sys.exit(1)

    # use for command line arguments
    if len(sys.argv) >= 3:
        ip, port = sys.argv[1], sys.argv[2]
    return ip, int(port)


def connection(ip=None, port=None):
    if ip is None or port is None:
        ip, port = get_connection_data()
    response = ""
    file = open("password.txt", "w")
    with socket.socket() as sock:
        try:
            sock.connect((ip, port))
            # password length range
            for x in range(1, 6):
                for password in password_generator(x):
                    password = "".join(password)
                    sock.send(password.encode())
                    response = sock.recv(1024).decode()
                    print(password, response, file=file)
                    if response == "Connection success!":
                        print(password)
                        sys.exit(0)

        except ConnectionRefusedError:
            print(response)


if __name__ == "__main__":
    connection()