import time 
import queue
import random
import logging
import threading
from concurrent.futures import ThreadPoolExecutor

def consumer(queue, event):
    while not event.is_set():
        message = random.randint(1, 101)
        logging.info("Producer got message: %s", message)
        queue.put(message)
    logging.info("Producer received event. Exiting")

def producer(queue, event):
    while not event.is_set() or not queue.empty():
        message = queue.get()
        logging.info(
            "Consumer storing message: %s (size=%d)", message, queue.qsize()
        )
    logging.info("Consumer received event. Exiting")


if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    work_task = queue.Queue(maxsize=10)
    event = threading.Event()
    with ThreadPoolExecutor(max_workers=2) as thread_pool:
        logging.info("Submit producer and consumer")
        thread_pool.submit(producer, work_task, event)
        thread_pool.submit(consumer, work_task, event)

        time.sleep(0.1)
        # set event
        logging.info("Setting event")
        event.set()