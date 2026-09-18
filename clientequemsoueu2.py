import socket

def main():
    ip = input("IP do servidor: ")
    porta = int(input("Porta do servidor: "))

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((ip, porta))

    print("Conectado ao servidor.")

    while True:
        try:
            msg = cliente.recv(1024).decode('utf-8')
            if not msg:
                break

            print(msg, end='')

            # Precisamos enviar resposta para qualquer prompt
            if "Faça uma pergunta" in msg or "Responda sim ou não" in msg or "Selecione um personagem" in msg:
                texto = input()
                cliente.send((texto + "\n").encode('utf-8'))

        except (ConnectionError, OSError):
            break

    cliente.close()

if __name__ == "__main__":
    main()
    