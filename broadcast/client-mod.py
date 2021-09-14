import threading
import socket
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
HOST='127.0.0.1'
PORT=9090



class Client:
    def __init__(self, host, port):
        # init our client with socket with server and port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        # gui interface pop up and send mas
        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring('Nickname', 'please enter your nickname', parent=msg)
        self.gui_done = False
        self.running = True
        gui_thread =threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.config(bg='lightgray')

        self.chat_level=tkinter.Label(self.win, text='chat', bg='lightgray')
        self.chat_level.config(font=('Arial', 12))
        self.chat_level.pack(padx=20, pady=5)

        self.text_area=tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_level = tkinter.Label(self.win, text='Massage', bg='lightgray')
        self.msg_level.config(font=('Arial', 12))
        self.msg_level.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text='send', comand=self.write)
        self.send_button.config(font=('Arial',12))
        self.send_button.pack(padx=20, pady=5)
        self.gui_done=True
        self.win.protocol('WM_DELETE_WINDOW', self.stop)
        self.win.mainloop()


    def write(self):
        massage= f"{self.nickname}: {self.input_area('1.0', 'end')}"
        self.sock.send(massage.encode('utf-8'))
        self.input_area.delete()


    def stop(self):
        self.running=False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                massage = self.sock.recv(1024).decode('utf-8')
                if massage =="NICK":
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end')
                        self.text_area.config(state='disabled')


            except ConnectionAbortedError:
                break
            except:
                print('error')
                self.sock.close()
                break


client = Client(HOST, PORT)





















