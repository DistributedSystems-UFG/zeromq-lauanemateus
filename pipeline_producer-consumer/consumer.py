import zmq, pickle
from const import *

def consumer():
  context = zmq.Context()
  socket  = context.socket(zmq.PULL)      # create a pull socket
  socket.bind(f"tcp://*:{PORT2}")         # workers connect here

  while True:
    result = pickle.loads(socket.recv())  # receive result from worker
    print(
      f"[consumer] worker={result['worker']} "
      f"{result['op']} {result['a']} {result['b']} = {result['value']}"
    )

consumer()
