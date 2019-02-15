import socket
import logging as L

def main():
    s = socket.socket()
    s.bind(('', 1234))
    s.listen(256)

    while True:
        sock, addr = s.accept()
        L.debug(f'connection from {addr} using socket {sock}')


if __name__ == '__main__':
    main()
