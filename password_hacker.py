import socket
import sys


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
        ip, port, message = sys.argv[1], sys.argv[2], sys.argv[3]
    return ip, int(port), message


def connection(ip=None, port=None, message=None):
    if ip is None or port is None or message is None:
        ip, port, message = get_connection_data()
    response = ""
    try:
        with socket.socket() as sock:
            sock.connect((ip, port))
            sock.send(message.encode())
            response = sock.recv(1024)
    except ConnectionRefusedError:
        print(response.decode())

    if response:
        print(response.decode())


if __name__ == "__main__":
    connection()
