import echo_util
import threading
import urllib3
import facebook
import requests

HOST = echo_util.HOST
PORT = echo_util.PORT

def handle_client(sock, addr): #modificat a.i sa putem lua id si alte comenzi din client.py
    """ Receive data from the client via sock and echo it back """
    while True:
        try:
            msg = echo_util.recv_msg(sock) # Blocks until received
            # complete message
            print('{}: {}'.format(addr, msg))
            echo_util.send_msg(sock, msg) # Blocks until sent
        except (ConnectionError, BrokenPipeError):
            print('Closed connection to {}'.format(addr))
            sock.close()
            break


if __name__ == '__main__':
    listen_sock = echo_util.create_listen_socket(HOST, PORT)
    addr = listen_sock.getsockname()
    print('Listening on {}'.format(addr))

    while True:
        client_sock, addr = listen_sock.accept()
        # Thread will run function handle_client() autonomously
        # and concurrently to this while loop
        thread = threading.Thread(target = handle_client, args = [client_sock, addr], daemon=True)
        thread.start()
        print('Connection from {}'.format(addr))
