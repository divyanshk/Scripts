import time
import multiprocessing

class Task():

    # object of Task goes on the multiprocessing Queue,
    # this is what each worker does as per the main process's command
    def __init__(self, a , b):
        self.a = a
        self.b = b

    def __call__(self):
        time.sleep(1)
        return "%s * %s = %s" % (self.a, self.b, self.a * self.b)

    def __str__(self):
        return "%s * %s" % (self.a, self.b)

class Consumer(multiprocessing.Process):
    """ worker class which does what we ask it do """

    def __init__(
        self,
        name: str,
        task_queue: multiprocessing.JoinableQueue,
        result_queue: multiprocessing.Queue
    ):
        super(Consumer, self).__init__()
        self.name = name
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        process_name = self.name
        while True: # loop indefintely
            next_task = self.task_queue.get() # get the next action item
            if next_task is None: # aka main process wants you to shutdown
                print("%s: Exiting" % process_name)
                self.task_queue.task_done()
                break
            print("%s :%s" % (process_name, next_task))
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return

def main_process():
    """ main process which acts like everyone's parent """

    # Setup comm channels
    task_queue = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # Create Consumers
    print(multiprocessing.cpu_count())
    num_counsumers = multiprocessing.cpu_count() * 2
    print("Creating %d consumers" % num_counsumers)
    consumers = [Consumer(str(i), task_queue, results) for i in range(num_counsumers)]
    for w in consumers:
        w.start() # kick each one off

    # Enqueue jobs
    num_jobs = 10
    for i in range(num_jobs):
        task_queue.put(Task(i, i))

    # Enqueue stop tasks
    for i in range(num_counsumers):
        task_queue.put(None)

    # Wait for all of the tasks to finish
    task_queue.join()

    while(num_jobs):
        result = results.get()
        print("Result:", result)
        num_jobs -= 1

if __name__ == '__main__':
    main_process()
