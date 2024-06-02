#CARLOS LOZANO 
import json
import queue
import random
import threading
import time

my_queue = queue.Queue(maxsize=10)
lock = threading.Lock()
not_full = threading.Condition(lock)
not_empty = threading.Condition(lock)

PRODUCERS = 2
elements = 0
#Just one producer function because it can be used for each producer with his respective thread with the id
def producer(id):
    global elements
    while True:
        #Every producer has an id and a random value to push in the queue
        dictionary = {"id": id,"value": random.randint(1,10)}
        #Serializing data
        serialized_data = json.dumps(dictionary)
        with not_full:
            #A producer is locked while the queue is full
            while my_queue.full():
                print("            Producer is waiting...(full queue)")
                not_full.wait()
            #If is not full, producer pushes serialized data
            my_queue.put(serialized_data)
            elements = elements+1
            print("++++ Producer {} push data{}    NUM: {}".format(dictionary['id'], dictionary['value'], elements))
            #We unlock the consumer if is waiting for an element in the queue
            not_empty.notify()
        time.sleep(random.randint(1,15))

def consumer():
    global elements
    while True:
        with not_empty:
            #A consumer is locked while the queue is empty
            while my_queue.empty():
                print("            Consumer is waiting...(empty queue)")
                not_empty.wait()
            #If is not empty, consumer pops data and desserializes it
            data = my_queue.get()
            elements = elements-1
            desserialized_data = json.loads(data)
            print("---- Consumer pops data{}    NUM: {}".format(desserialized_data['value'], elements))
            #Consumer unlocks producer if is waiting for space in the queue to push data
            not_full.notify()
        time.sleep(random.randint(1,15))

def main():
    #This array will contain all the threads
    threads = []
    #Append the respective threads in the array, each one calling to his own function
    c = threading.Thread(target=consumer)
    threads.append(c)

    for i in range(PRODUCERS):
        p = threading.Thread(target=producer,args=[i,])
        threads.append(p)

    # Start all threads
    for t in threads:
        t.start()

    # acquire for all threads to complete
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
