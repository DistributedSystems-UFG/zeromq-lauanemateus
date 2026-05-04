import multiprocessing #-
import zmq, time, pickle, sys, random #-
#-
NWORKERS = 2 #-
#-
def producer():
  context = zmq.Context()              
  socket  = context.socket(zmq.PUSH)      # create a push socket
  socket.bind("tcp://127.0.0.1:12345")    # bind socket to address
  
  while True:
    workload = random.randint(1, 100)     # compute workload
    print("Produced workload", format(workload,'03d')) #-
    socket.send(pickle.dumps(workload))   # send workload to worker
    time.sleep(workload/NWORKERS)         # balance production by waiting 

producer()