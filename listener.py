import time 
import sys
import stomp
import json

from tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter as tk

"""
Cria objeto "Tkinter"/"Tk"
"""
root = tk.Tk()
root.withdraw()

text_area_topicos = ScrolledText()
text_area_filas = ScrolledText()

class Listener(stomp.ConnectionListener):
# Override the methods on_error and on_message provides by the
# parent class
    def on_error(self, message):
        print('ERROR: "%s"' % message)
# Print out the message received
    def on_message(self, message):
        print(message)    
        header_message = message.headers['destination'] 
        if "topic" in header_message:
            topico = header_message.replace("/topic/", "")
            text_area_topicos.insert(tk.INSERT, f'{topico} : {message.body}!\n', 'msg')
            text_area_topicos.tag_config('msg', foreground='blue')
        
        if "queue" in header_message:
            queue = header_message.replace("/queue/", "")
            text_area_filas.insert(tk.INSERT, f'{queue} : {message.body}!\n', 'msg')
            text_area_filas.tag_config('msg', foreground='blue')            
    
    def subscribe_topic(self, topic, toplevel):
        global text_area_topicos
        text_area_topicos.insert(tk.INSERT, f'Inscrito no tópico: {topic}!\n', 'msg')
        text_area_topicos.tag_config('msg', foreground='blue')
        conn.subscribe(destination='/topic/{}'.format(topic), id=1, ack='auto')
        self.fecha_tela(toplevel)

    def subscribe_queue(self, queue):
        print('Subscribe queue: "%s"' % queue)
        global text_area_filas
        text_area_filas.insert(tk.INSERT, f'Fila criada: {queue}!\n', 'msg')
        text_area_filas.tag_config('msg', foreground='blue')
        conn.subscribe(destination='/queue/{}'.format(queue), id=1, ack='auto')

    def send_message_topic(self, topic, message, toplevel):
        conn.send(body='{}'.format(message), destination='/topic/{}'.format(topic))
        self.fecha_tela(toplevel)

    def send_message_queue(self, queue, message, toplevel):
        print('Send queue: "%s"' % message)
        global text_area_filas
        text_area_filas.insert(tk.INSERT, f'Enviando mensagem: {queue}!\n', 'msg')
        text_area_filas.tag_config('msg', foreground='blue')
        conn.send(body='{}'.format(message), destination='/queue/{}'.format(queue))
        self.fecha_tela(toplevel)

    def disconnect(self):
        conn.disconnect()


    # TELAS DA APLICAÇÃO
    def conexao_cliente(self):
        newWindow = Toplevel(root)
        newWindow.title("INICIAR")
        newWindow.geometry("300x150")
        newWindow.config(bg="#4F4F4F")

        #newWindow.protocol("WM_DELETE_WINDOW", lambda: fecha_janela(newWindow))

        # BG cor de fundo  FG cor da letra
        label = Label(newWindow, text="DIGITE SEU NOME:", font=('Ivy 15 bold'), fg="#FFFFFF", bg="#4F4F4F")
        label.place(x=40, y=20)

        jogador_name_input = Entry(newWindow, width=27)
        jogador_name_input.place(x=40, y=60)

        # https://python-forum.io/thread-26854.html <--- Como fazer o texto de um botão do tkinter ficar em Negrito
        jogar_button = Button(newWindow, text='INICIAR', font='sans 11 bold', width=12, height=int(1.5),
                                command=lambda: self.janela_principal(str(jogador_name_input.get()), newWindow))
        jogar_button.place(x=80, y=95)


    def janela_principal(self, jogador_name_input, toplevel):
        global text_area_topicos, text_area_filas
        newWindow = Toplevel(root)
        newWindow.title("Confirma!")
        newWindow.geometry("730x400")

        newWindow.protocol("WM_DELETE_WINDOW", lambda: self.fecha_janela(newWindow))

        label_peca = Label(newWindow, text= 'Cliente: ' + str(jogador_name_input), height=0, padx=0, relief="flat", anchor="center",
                        font=('Ivy 10 bold'),
                            fg="#000000")
        label_peca.place(x=20, y=5)

        label_peca = Label(newWindow, text= 'Menu Tópico', height=0, padx=0, relief="flat", anchor="center",
                        font=('Ivy 10 bold'),fg="#000000")
        label_peca.place(x=20, y=30)

        button_inscricao_topic = Button(newWindow, text='Increver-se', width=12, command=lambda:self.inscricao_topico(newWindow))
        button_inscricao_topic.place(x=20, y=60)

        button_inscricao_topic = Button(newWindow, text='Envia Msg', width=12, command=lambda:self.mensagem_topico(newWindow))
        button_inscricao_topic.place(x=20, y=100)

        label_peca = Label(newWindow, text= 'Menu Filas', height=0, padx=0, relief="flat", anchor="center",
                        font=('Ivy 10 bold'),fg="#000000")
        label_peca.place(x=20, y=200)

        button_mensagem_fila = Button(newWindow, text='Enviar Msg', width=12, command=lambda:self.mensagem_fila(newWindow))
        button_mensagem_fila.place(x=20, y=230)


        label_name = Label(newWindow, text="TOPICOS:", font=('Ivy 10 bold'), fg="#4F4F4F")
        label_name.place(x=240, y=5)
        text_area_topicos = ScrolledText(newWindow, wrap=WORD, width=35, height=20, font=("Callibri", 8))
        text_area_topicos.place(x=150, y=40)
        text_area_topicos.focus()

        label_name = Label(newWindow, text="FILAS:", font=('Ivy 10 bold'), fg="#4F4F4F")
        label_name.place(x=550, y=5)
        text_area_filas = ScrolledText(newWindow, wrap=WORD, width=35, height=20, font=("Callibri", 8))
        text_area_filas.place(x=450, y=40)
        text_area_filas.focus()

        self.subscribe_queue(jogador_name_input)
        self.fecha_tela(toplevel)

    def inscricao_topico(self, toplevel):
        newWindow = Toplevel(root)
        newWindow.title("TOPICO!")
        newWindow.geometry("300x150")
        newWindow.config(bg="#4F4F4F")

        newWindow.protocol("WM_DELETE_WINDOW", lambda: self.fecha_tela(newWindow))

        # BG cor de fundo  FG cor da letra
        label = Label(newWindow, text="NOME DO TOPICO:", font=('Ivy 15 bold'), fg="#FFFFFF", bg="#4F4F4F")
        label.place(x=40, y=20)

        topic_name_input = Entry(newWindow, width=27)
        topic_name_input.place(x=40, y=60)

        jogar_button = Button(newWindow, text='JOGAR', font='sans 11 bold', width=12, height=int(1.5),
                                command=lambda: self.subscribe_topic(str(topic_name_input.get()), newWindow))
        jogar_button.place(x=80, y=95)

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

    

    def fecha_janela(self, Toplevel):
        Toplevel.destroy()
        Toplevel.quit()
        self.disconnect()
        root.destroy()
        # os._exit(1)


    def fecha_tela(self, Toplevel):
        Toplevel.destroy()


if __name__ == "__main__":
    #PORTA PADRÂO STOMP (61613)
    hosts = [('localhost', 61613)]
    conn = stomp.Connection(host_and_ports=hosts)
    conn.set_listener('', Listener())
    conn.connect('admin', 'admin', wait=True)
    pub = Listener()
    pub.conexao_cliente()
    root.mainloop()