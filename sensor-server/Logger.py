import threading

class DataLogger():
    def __init__(self):
        self.stdout = b''
        self.lock = threading.Lock()

    # Is logs reading and writting function needed to be locked due to access in two thread?, I do not see any issues as I check partial_packet while reading. 
    def write(self,message):
        #with self.lock:
        self.stdout += message
        print("Message writing length as of now: ", len(self.stdout))


    def read(self):
        #with self.lock:
        print("Message reading as of now: ", len(self.stdout))
        return self.stdout