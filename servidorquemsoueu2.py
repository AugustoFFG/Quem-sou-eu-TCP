import re
import socket

def receber(conn):
    return conn.recv(1024).decode("utf-8").strip()

def enviar(conn, msg):
    conn.send((msg + "\n").encode("utf-8"))

# Extrator de chute robusto
#
# Padrões ordenados do mais específico para o mais genérico: assim, uma frase
# como "você é o batman" tem a forma completa "você é o " removida de uma vez,
# em vez de cair primeiro no padrão genérico "o " (que sozinho cortaria uma
# pergunta comum como "o batman usa capa?" e a confundiria com um palpite).
_PADROES_CHUTE = [
    r"^(você|voce)\s+[eé]\s+o\s+",
    r"^(você|voce)\s+[eé]\s+a\s+",
    r"^(você|voce)\s+[eé]\s+",
    r"^ele\s+[eé]\s+o\s+",
    r"^ele\s+[eé]\s+a\s+",
    r"^ela\s+[eé]\s+o\s+",
    r"^ela\s+[eé]\s+a\s+",
    r"^eu\s+sou\s+o\s+",
    r"^eu\s+sou\s+a\s+",
    r"^eu\s+sou\s+",
    r"^sou\s+o\s+",
    r"^sou\s+a\s+",
    r"^sou\s+",
    r"^meu\s+personagem\s+[eé]\s+o\s+",
    r"^meu\s+personagem\s+[eé]\s+a\s+",
    r"^meu\s+personagem\s+[eé]\s+",
    r"^[eé]\s+o\s+",
    r"^[eé]\s+a\s+",
    r"^[eé]\s+",
    r"^o\s+",
    r"^a\s+",
]

def extrair_chute(pergunta):
    p = pergunta.lower().replace("?", "").strip()

    for padrao in _PADROES_CHUTE:
        nova = re.sub(padrao, "", p, count=1)
        if nova != p:
            p = nova.strip()
            break

    return p.strip()

def main():
    porta = int(input("Porta para o servidor escutar: "))

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(("0.0.0.0", porta))
    servidor.listen(2)

    print("Aguardando Jogador 1...")
    j1, end1 = servidor.accept()
    enviar(j1, "Conectado como Jogador 1.")
    print("Jogador 1 conectado:", end1)

    print("Aguardando Jogador 2...")
    j2, end2 = servidor.accept()
    enviar(j2, "Conectado como Jogador 2.")
    print("Jogador 2 conectado:", end2)

    # Coleta dos personagens
    enviar(j1, "Selecione um personagem para o Jogador 2 adivinhar:")
    personagem_j2 = receber(j1).lower().strip()

    enviar(j2, "Selecione um personagem para o Jogador 1 adivinhar:")
    personagem_j1 = receber(j2).lower().strip()

    print("Jogador 1 escolheu para J2:", personagem_j2)
    print("Jogador 2 escolheu para J1:", personagem_j1)

    turno = 1  # 1 = jogador 1 pergunta, 2 = jogador 2 pergunta

    while True:
        if turno == 1:
            # J1 PERGUNTA
            enviar(j1, "Faça uma pergunta:")
            pergunta = receber(j1)
            chute = extrair_chute(pergunta)

            # J2 RESPONDE
            enviar(j2, f"Responda sim ou não: {pergunta}")
            resposta = receber(j2)
            enviar(j1, f"Resposta do jogador 2: {resposta}")

            # Verifica chute (Jogador 1 tenta adivinhar personagem_j1)
            if chute == personagem_j1:
                enviar(j1, "Sim!!! Você venceu!")
                enviar(j2, "Jogador 1 acertou! Você perdeu.")
                break

            turno = 2

        else:
            # J2 PERGUNTA
            enviar(j2, "Faça uma pergunta:")
            pergunta = receber(j2)
            chute = extrair_chute(pergunta)

            # J1 RESPONDE
            enviar(j1, f"Responda sim ou não: {pergunta}")
            resposta = receber(j1)
            enviar(j2, f"Resposta do jogador 1: {resposta}")

            # Verifica chute (Jogador 2 tenta adivinhar personagem_j2)
            if chute == personagem_j2:
                enviar(j2, "Sim!!! Você venceu!")
                enviar(j1, "Jogador 2 acertou! Você perdeu.")
                break

            turno = 1

    # Encerrar sockets corretamente
    try:
        j1.close()
        j2.close()
        servidor.close()
    except OSError:
        pass

    print("Jogo encerrado.")

if __name__ == "__main__":
    main()