import time 
import sys
import stomp
import requests
from http.client import HTTPConnection
from base64 import b64encode
import json

from tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter as tk

"""
Cria objeto "Tkinter"/"Tk"
"""
root = tk.Tk()
root.withdraw()

#http://localhost:8161/admin/topics.jsp

class Publisher(stomp.ConnectionListener):
    # Override the methods on_error and on_message provides by the
    # parent class
    def on_error(self, message):
        print('Received an error "%s"' % message)

    # Print out the message received
    def on_message(self, message):
        print('Received a message "%s"' % message)

    def send_message_topic(self, topic, message, toplevel):
        conn.send(body='{}'.format(message), destination='/topic/{}'.format(topic))
        self.fecha_tela(toplevel)
    
    def send_message_queue(self, queue, message, toplevel):
        conn.send(body='{}'.format(message), destination='/queue/{}'.format(queue))
        self.fecha_tela(toplevel)

    def disconnect(self):
         conn.disconnect()
        

    def delete_queue(self, queue, toplevel):
        host = "localhost:8161"
        url = "http://hostname:8161/api/jolokia/exec/org.apache.activemq:type=Broker,brokerName=localhost/removeQueue/{}".format(queue)
        headers = {'Origin': 'localhost', 'Authorization': 'Basic {}'.format(b64encode(b'admin:admin').decode('ascii'))}
        conn = HTTPConnection(host)
        conn.request('GET', url=url, headers=headers)
        self.fecha_tela(toplevel)

    def delete_topic(self, topic, toplevel):
        host = "localhost:8161"
        url = "http://hostname:8161/api/jolokia/exec/org.apache.activemq:type=Broker,brokerName=localhost/removeTopic/{}".format(topic)
        headers = {'Origin': 'localhost', 'Authorization': 'Basic {}'.format(b64encode(b'admin:admin').decode('ascii'))}
        conn = HTTPConnection(host)
        conn.request('GET', url=url, headers=headers)
        self.fecha_tela(toplevel)



    # TELAS DA APLICAÇÃO
    def conexao_cliente(self):
        newWindow = Toplevel(root)
        newWindow.title("INICIAR")
        newWindow.geometry("300x150")
        newWindow.config(bg="#4F4F4F")

        newWindow.protocol("WM_DELETE_WINDOW", lambda: self.fecha_janela(newWindow))

        # BG cor de fundo  FG cor da letra
        label_nome_cliente = Label(newWindow, text="DIGITE SEU NOME:", font=('Ivy 15 bold'), fg="#FFFFFF", bg="#4F4F4F")
        label_nome_cliente.place(x=40, y=20)

        jogador_name_input = Entry(newWindow, width=27)
        jogador_name_input.place(x=40, y=60)

        jogar_button = Button(newWindow, text='CONECTAR', font='sans 11 bold', width=12, height=int(1.5),
                                command=lambda: self.janela_principal(str(jogador_name_input.get()), newWindow))
        jogar_button.place(x=80, y=95)


    def janela_principal(self, jogador_name_input, toplevel):
        self.fecha_tela(toplevel)
        newWindow = Toplevel(root)
        newWindow.title("Confirma!")
        newWindow.geometry("360x400")

        newWindow.protocol("WM_DELETE_WINDOW", lambda: self.fecha_janela(newWindow))

        label_peca = Label(newWindow, text= 'Publicador: ' + str(jogador_name_input), height=0, padx=0, relief="flat", anchor="center",
                        font=('Ivy 10 bold'),
                            fg="#000000")
        label_peca.place(x=110, y=5)

        label_peca = Label(newWindow, text= 'Tópico', height=0, padx=0, relief="flat", anchor="center",
                        font=('Ivy 10 bold'),fg="#000000")
        label_peca.place(x=110, y=30)

        button = Button(newWindow, text='Enviar Msg', width=12, command=lambda:self.mensagem_topico(newWindow))
        button.place(x=110, y=60)

        button = Button(newWindow, text='Deletar', width=12, command=lambda:self.deletar_topico(newWindow))
        button.place(x=110, y=100)

        label_peca = Label(newWindow, text= 'Fila', height=0, padx=0, relief="flat", anchor="center",
                        font=('Ivy 10 bold'),fg="#000000")
        label_peca.place(x=110, y=200)

        nao_button = Button(newWindow, text='Enviar Msg', width=12, command=lambda:self.mensagem_fila(newWindow))
        nao_button.place(x=110, y=230)

        nao_button = Button(newWindow, text='Deletar', width=12, command=lambda:self.deletar_fila(newWindow))
        nao_button.place(x=110, y=270)

    def mensagem_topico(self, toplevel):
        newWindow = Toplevel(root)
        newWindow.title("TOPICO!")
        newWindow.geometry("310x360")
        newWindow.config(bg="#4F4F4F")

        newWindow.protocol("WM_DELETE_WINDOW", lambda: self.fecha_tela(newWindow))

        label_name = Label(newWindow, text="NOME DO TOPICO:", font=('Ivy 10 bold'), fg="#FFFFFF", bg="#4F4F4F")
        label_name.place(x=40, y=20)
        topic_name_input = Entry(newWindow, width=27)
        topic_name_input.place(x=40, y=50)

        label_name = Label(newWindow, text="MENSAGEM:", font=('Ivy 10 bold'), fg="#FFFFFF", bg="#4F4F4F")
        label_name.place(x=40, y=90)
        text_area_chat = ScrolledText(newWindow, wrap=WORD, width=29, height=12, font=("Callibri", 8))
        text_area_chat.place(x=40, y=120)
        text_area_chat.focus()


        jogar_button = Button(newWindow, text='ENVIAR', font='sans 11 bold', width=12, height=int(1.5),
                                command=lambda: self.send_message_topic(str(topic_name_input.get()), str(text_area_chat.get("1.0",'end-1c')), newWindow))
        jogar_button.place(x=80, y=300)

    def mensagem_fila(self, toplevel):
        newWindow = Toplevel(root)
        newWindow.title("FILA!")
        newWindow.geometry("310x360")
        newWindow.config(bg="#4F4F4F")

        newWindow.protocol("WM_DELETE_WINDOW", lambda: self.fecha_tela(newWindow))

        # NOME DA FILA
        label_name = Label(newWindow, text="NOME DA FILA:", font=('Ivy 10 bold'), fg="#FFFFFF", bg="#4F4F4F")
        label_name.place(x=40, y=20)
        queue_name_input = Entry(newWindow, width=27)
        queue_name_input.place(x=40, y=50)

        label_name = Label(newWindow, text="MENSAGEM:", font=('Ivy 10 bold'), fg="#FFFFFF", bg="#4F4F4F")
        label_name.place(x=40, y=90)
        text_area_chat = ScrolledText(newWindow, wrap=WORD, width=29, height=12, font=("Callibri", 8))
        text_area_chat.place(x=40, y=120)
        text_area_chat.focus()

        jogar_button = Button(newWindow, text='ENVIAR', font='sans 11 bold', width=12, height=int(1.5),
                                command=lambda: self.send_message_queue(str(queue_name_input.get()), str(text_area_chat.get("1.0",'end-1c')), newWindow))
        jogar_button.place(x=80, y=300)

    def deletar_topico(self, toplevel):
        newWindow = Toplevel(root)
        newWindow.title("DELETAR TOPICO")
        newWindow.geometry("300x150")
        newWindow.config(bg="#4F4F4F")

        newWindow.protocol("WM_DELETE_WINDOW", lambda: self.fecha_tela(newWindow))

        # BG cor de fundo  FG cor da letra
        label = Label(newWindow, text="NOME DO TOPICO:", font=('Ivy 15 bold'), fg="#FFFFFF", bg="#4F4F4F")
        label.place(x=40, y=20)

        topic_name_input = Entry(newWindow, width=27)
        topic_name_input.place(x=40, y=60)

        jogar_button = Button(newWindow, text='DELETAR', font='sans 11 bold', width=12, height=int(1.5),
                                command=lambda: self.delete_topic(str(topic_name_input.get()), newWindow))
        jogar_button.place(x=80, y=95)

    def deletar_fila(self, toplevel):
        newWindow = Toplevel(root)
        newWindow.title("DELETAR TOPICO")
        newWindow.geometry("300x150")
        newWindow.config(bg="#4F4F4F")

        newWindow.protocol("WM_DELETE_WINDOW", lambda: self.fecha_tela(newWindow))

        # BG cor de fundo  FG cor da letra
        label = Label(newWindow, text="NOME DA FILA:", font=('Ivy 15 bold'), fg="#FFFFFF", bg="#4F4F4F")
        label.place(x=40, y=20)

        fila_name_input = Entry(newWindow, width=27)
        fila_name_input.place(x=40, y=60)

        jogar_button = Button(newWindow, text='DELETAR', font='sans 11 bold', width=12, height=int(1.5),
                                command=lambda: self.delete_queue(str(fila_name_input.get()), newWindow))
        jogar_button.place(x=80, y=95)

    def fecha_janela(self, Toplevel):
        Toplevel.destroy()
        Toplevel.quit()
        self.disconnect()
        root.destroy()


    def fecha_tela(self, Toplevel):
        Toplevel.destroy()


if __name__ == "__main__":
    #PORTA PADRÂO STOMP (61613) OPENWIRE (61616)
    hosts = [('localhost', 61613)]
    conn = stomp.Connection(host_and_ports=hosts)
    conn.set_listener('', Publisher())
    conn.connect('admin', 'admin', wait=True)
    pub = Publisher()
    pub.conexao_cliente()
    root.mainloop()
    

