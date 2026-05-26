import zmq, pickle, random
from const import *

OPERATIONS = {
  "ADD": lambda a, b: a + b,
  "SUB": lambda a, b: a - b,
  "MUL": lambda a, b: a * b,
  "DIV": lambda a, b: a / b if b != 0 else float("inf"),
}

def worker(id):
  context = zmq.Context()
  pull = context.socket(zmq.PULL)         # consumer side
  pull.connect(f"tcp://{SRC1}:{PORT1}")   # connect to the producer

  push = context.socket(zmq.PUSH)         # producer side
  push.connect(f"tcp://{SRC2}:{PORT2}")   # connect to the consumer

  me = format(id, '03d')
  while True:
    task = pickle.loads(pull.recv())      # receive task from producer
    op, a, b = task["op"], task["a"], task["b"]
    value = OPERATIONS[op](a, b)
    result = {"worker": me, "op": op, "a": a, "b": b, "value": value}
    print(f"[worker {me}] {op} {a} {b} = {value}")
    push.send(pickle.dumps(result))       # forward result to consumer

worker(random.randint(1, 10000))
