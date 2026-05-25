import multiprocessing #-
import zmq, time, pickle, sys, random #-

def worker(id):
  context = zmq.Context()
  socket  = context.socket(zmq.PULL)      # create a pull socket
  socket.connect(f"tcp://{SRC1}:{PORT1}") # connect to the producer
  thisworker = format(id,'03d') #-

worker(random.randint(1, 10000))