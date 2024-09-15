import time
import logging
import multiprocessing

class Worker(multiprocessing.Process):
    def __init__(self, id: int):
        self.id = id
        super(Worker, self).__init__()

    def run(self):
        """ worker function which does what we ask it do """
        print('Worker', self.id)
        if self.id % 5 == 0:
            time.sleep(10) # sleep for 10s
            # if running this process with a join
            # it will wait for 10s for child process 0, 5, 10, ...
        return

def main_process():
    """ main process which acts like everyone's parent """
    multiprocessing.log_to_stderr(logging.DEBUG)
    jobs = []
    for i in range(10):
        # unlike threading, the arg passed to a worker process
        # must be able to be serialized using pickle
        # p = multiprocessing.Process(target=worker_function, args=(i,))
        p = Worker(i)
        jobs.append(p) # track all child processes
        p.start() # kick off p
        p.join(100) # wait for p to complete, with timeout at 100


if __name__ == '__main__':
    main_process()