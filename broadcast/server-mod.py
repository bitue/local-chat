import socket
import threading
# init the socket package
# AF_INET for ip address and SOCK_STREAM for the tcp way
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('socket connected')
# server side is bind with port 9999 as well as ip address local host
server.bind((socket.gethostname(), 9999))

server.listen()

# this are the client list and nicknames list for the client to make visualize by server
clients = []
nickNames = []


def broadcast(massage):
    for client in clients:
        client.send(massage)


def handle(client):
    while True:
        try:
            massage = client.recv(1024)
            print(f"{nickNames[clients.index(client)]} says {massage}")
            broadcast(massage)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nickNames[index]
            nickNames.remove(nickname)
            break






def receive():
    while True:
        client, address = server.accept()
        # client is now connected with server with one ip and one port
        print(f"connected with {str(address)}!")
        # server send the massage to the server want to get nickname
        client.send('NICK'.encode('utf-8'))
        # need to append client to the clients list
        clients.append(client)
        # the response should get by the client as recv function by server
        nickName = client.recv(1024)
        print(f"nickname of {nickName} client is connected now!")
        # need to append this nickname associated with this thread by the client
        nickNames.append(nickName)
        broadcast(f"{nickName} connected to the server".encode('utf-8'))
        # server need to send msg to the client to confirm
        client.send(f"{nickName} you are now connected with server".encode('utf-8'))

        # as well as we need to make this one thread to make this client indevisual and target to handle function and args need the params of client as tuple
        thread = threading.Thread(target=handle, args=(client,))
        # thread now get handle function and client arg and is going to start
        thread.start()

print(f"server is running ....")
receive()
