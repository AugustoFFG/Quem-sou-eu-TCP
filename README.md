# Quem Sou Eu? — Multiplayer via Sockets TCP

Implementação do jogo "Quem sou eu?" para dois jogadores, com comunicação
cliente-servidor via sockets TCP e um protocolo de aplicação em texto
simples definido para este projeto.

## Tecnologias utilizadas

- **Python 3** (sem dependências externas — só biblioteca padrão)
- **`socket`** — comunicação via TCP/IP (`AF_INET`, `SOCK_STREAM`)
- **`re`** — extração de palpites das perguntas dos jogadores via expressões
  regulares
- Protocolo de aplicação próprio, baseado em mensagens de texto delimitadas
  por `\n`

## Estrutura

| Arquivo                    | Papel                                                          |
|-----------------------------|-----------------------------------------------------------------|
| `servidorquemsoueu.py`      | Servidor: gerencia a partida, os turnos e verifica os palpites |
| `clientequemsoueu.py`       | Cliente: conecta ao servidor e faz a interface com o jogador   |

## Requisitos

- Python 3.8+ instalado
- **Duas ou três máquinas na mesma rede** para demonstrar o funcionamento
  real via TCP/IP (não apenas em `localhost`). Como normalmente não se tem
  três computadores físicos disponíveis, o mais prático é usar **máquinas
  virtuais** (VirtualBox, VMware, etc.), cada uma com Python 3 instalado:
  - 1 VM (ou a máquina host) rodando o servidor
  - 1 VM para o Jogador 1
  - 1 VM para o Jogador 2
  - As VMs precisam estar na mesma rede (ex.: modo *Bridge* ou uma rede
    *Host-only*/interna compartilhada) para que os clientes consigam
    alcançar o IP do servidor.

  > Também é possível rodar tudo em `localhost` (servidor e os dois
  > clientes na mesma máquina, em terminais separados) só para testar a
  > lógica do jogo — mas isso não demonstra a comunicação em rede de fato.

## Como executar

### 1. Descobrir o IP do servidor

Na VM/máquina que vai rodar o servidor, descubra o IP na rede:

```bash
ip addr show   # Linux
# ou
ipconfig       # Windows
```

### 2. Iniciar o servidor

```bash
python3 servidorquemsoueu.py
```

Ele vai pedir uma porta (ex.: `5000`) e ficar aguardando os dois jogadores
se conectarem.

### 3. Conectar os dois clientes

Em cada VM de jogador, execute:

```bash
python3 clientequemsoueu.py
```

Informe o IP do servidor (obtido no passo 1) e a porta escolhida.

### 4. Jogar

1. Cada jogador escolhe um personagem para o **adversário** adivinhar.
2. Os jogadores se alternam fazendo perguntas de sim/não sobre o próprio
   personagem.
3. Para arriscar o palpite final, basta perguntar algo como:
   - "Eu sou o Batman?"
   - "Você é a Mulher Maravilha?"
   - "É o Coringa?"

   O servidor reconhece essas formas (com ou sem acento) e verifica se o
   palpite bate com o personagem sorteado.
4. Quem acertar primeiro vence a partida.

## Protocolo de comunicação (visão geral)

Todas as mensagens são texto simples terminado em `\n`. As principais
trocas entre servidor e cliente são:

- `Conectado como Jogador 1/2.` — confirmação de conexão
- `Selecione um personagem para o Jogador X adivinhar:` — pede o
  personagem que o cliente vai atribuir ao adversário
- `Faça uma pergunta:` — pede a próxima pergunta/palpite do jogador da vez
- `Responda sim ou não: <pergunta>` — repassa a pergunta ao adversário
- `Resposta do jogador X: <resposta>` — devolve a resposta a quem perguntou
- `Sim!!! Você venceu!` / `Jogador X acertou! Você perdeu.` — encerram a
  partida

## Possíveis melhorias futuras

- Tratar desconexão abrupta de um jogador no meio da partida
- Suportar mais de 2 jogadores ou uma fila de espera
- Migrar o protocolo de texto para JSON, facilitando extensões futuras
