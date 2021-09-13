import socket
# init the socket package
s = socket.socket()
print('socket connected')
# server side is binded with port 9999 as well as ip address local host
s.bind(('localhost', 9999))

s.listen(3)
print(bytes('waiting for the connection', 'utf-8').decode())

while True:
    # accept the data and get two params always
    c, add = s.accept()
    name = c.recv(1024).decode()
    print('you are always connected with my heart', add, name)
    c.send(bytes('i love you ', 'utf-8'))
    c.close()
