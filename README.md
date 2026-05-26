[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wa7oHGos)

# ZeroMQ-Examples

Exemplos extraídos de Tanenbaum & van Steen (2025) para ilustrar três padrões diferentes de comunicação com ZeroMQ: **client-server**, **pub-sub** e **producer-consumer (pipeline)**.

Cada pasta contém um `const.py` com as configurações de rede (IP e porta) compartilhadas entre os processos daquele padrão.

---

## 1. [client-server/](client-server/) — Request/Reply (REQ/REP)

Padrão **síncrono de pergunta-resposta**: o cliente envia uma mensagem e fica bloqueado até o servidor responder.

- [server.py](client-server/server.py) — cria um socket `zmq.REP`, faz `bind` na porta e fica em loop recebendo mensagens. Para cada mensagem, anexa `"*"` no final e devolve. Se a mensagem for `"STOP"`, encerra o loop.
- [client.py](client-server/client.py) — cria um socket `zmq.REQ`, conecta ao servidor, envia `"Hello world"`, espera a resposta (`"Hello world*"`), envia `"STOP"` para encerrar o servidor e imprime o retorno.
- [const.py](client-server/const.py) — define `PORT` e `SERVER_IP`.

**Fluxo:** `client --REQ--> server --REP--> client`. Cada `send` do cliente deve ser seguido de um `recv`, e vice-versa no servidor (estrita alternância imposta pelo ZeroMQ).

---

## 2. [pub-sub/](pub-sub/) — Publisher/Subscriber (PUB/SUB)

Padrão **assíncrono de difusão por tópicos**: o publisher transmite mensagens sem saber quem está ouvindo; os subscribers escolhem quais tópicos receber.

- [server.py](pub-sub/server.py) — cria um socket `zmq.PUB`, faz `bind` na porta e, a cada 5 segundos, publica uma mensagem prefixada com `"TIME "` contendo o horário atual.
- [client.py](pub-sub/client.py) — cria um socket `zmq.SUB`, conecta ao servidor e usa `setsockopt(zmq.SUBSCRIBE, b"TIME")` para se inscrever apenas em mensagens que comecem com `"TIME"`. Recebe e imprime 5 mensagens, depois encerra.
- [const.py](pub-sub/const.py) — define `PORT` e `SERVER_IP`.

**Fluxo:** `publisher --PUB--> [tópico TIME] --SUB--> subscribers`. O publisher não bloqueia esperando ninguém; quem não estiver conectado no momento da publicação, **perde a mensagem** (sem buffer histórico).

---

## 3. [pipeline_producer-consumer/](pipeline_producer-consumer/) — Pipeline (PUSH/PULL)

Padrão de **divisão de trabalho em etapas**: o producer cria tarefas, os workers fazem as contas e o consumer junta os resultados. Quando existem vários workers, o producer reveza entre eles na hora de enviar as tarefas — cada tarefa vai para um worker diferente, de forma que o trabalho fique dividido por igual.

- [producer.py](pipeline_producer-consumer/producer.py) — cria um socket `zmq.PUSH`, faz `bind` em `PORT1` e gera continuamente tarefas aleatórias no formato `{"op", "a", "b"}` (operação: ADD/SUB/MUL/DIV com dois inteiros). Serializa com `pickle` e envia.
- [worker.py](pipeline_producer-consumer/worker.py) — atua como **intermediário**: tem um `zmq.PULL` conectado ao producer (recebe tarefas) e um `zmq.PUSH` conectado ao consumer (envia resultados). Usa o dicionário `OPERATIONS` para escolher a operação certa, calcula o resultado e repassa para o consumer.
- [consumer.py](pipeline_producer-consumer/consumer.py) — cria um socket `zmq.PULL`, faz `bind` em `PORT2` e recebe os resultados dos workers, imprimindo qual worker processou cada operação.
- [const.py](pipeline_producer-consumer/const.py) — define `SRC1`/`PORT1` (producer → worker) e `SRC2`/`PORT2` (worker → consumer).

**Fluxo:** `producer --PUSH--> [PORT1] --PULL--> workers --PUSH--> [PORT2] --PULL--> consumer`. Quem faz `bind` é sempre o ponto fixo (producer e consumer); os workers fazem `connect` nas duas pontas, ficando "no meio" do caminho.

---

## Resumo dos padrões

| Pasta | Padrão ZeroMQ | Característica |
|---|---|---|
| `client-server/` | REQ/REP | 1↔1, síncrono, alternância forçada |
| `pub-sub/` | PUB/SUB | 1→N, assíncrono, filtrado por tópico |
| `pipeline_producer-consumer/` | PUSH/PULL | N→M, assíncrono, tarefas divididas entre os workers |
