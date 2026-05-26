import zmq, time, pickle, random
from const import *

OPS = ["ADD", "SUB", "MUL", "DIV"]

def producer():
  context = zmq.Context()
  socket  = context.socket(zmq.PUSH)      # create a push socket
  socket.bind(f"tcp://*:{PORT1}")         # bind socket to address

  time.sleep(1)                           # give workers time to connect

  while True:
    task = {
      "op": random.choice(OPS),
      "a":  random.randint(1, 100),
      "b":  random.randint(1, 100),
    }
    print(f"Produced task: {task['op']} {task['a']} {task['b']}")
    socket.send(pickle.dumps(task))       # send task to worker
    time.sleep(random.uniform(0.3, 1.0))  # pace production

producer()
