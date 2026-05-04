import multiprocessing #-
import zmq, time, pickle, sys, random #-

def worker(id):
  context = zmq.Context()
  socket  = context.socket(zmq.PULL)      # create a pull socket
  socket.connect("tcp://localhost:12345") # connect to the producer
  thisworker = format(id,'03d') #-

worker(1)