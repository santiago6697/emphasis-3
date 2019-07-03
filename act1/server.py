import sys
import socket
import threading

server_ip_address = sys.argv[1]
server_port = int(sys.argv[2])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def accept(client_socket):
    client_socket.sendall("ok".encode('utf-8'))
    return

print ("Server: " + socket.gethostname())

server_socket.bind((server_ip_address, server_port))
server_socket.listen(32000)

while 1:
    (client_socket, address) = server_socket.accept() 
    print ("Connected client: {}".format(address))
    t = threading.Thread(target = accept, args=(client_socket,))
    t.start()
    t.join()
