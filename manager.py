import multiprocessing

def worker(store, key, value):
    store[key] = value

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    store = manager.dict() # lists are also supported
    jobs = [multiprocessing.Process(target=worker, args=(store, i, i*3)) for i in range(10)]

    for j in jobs:
        j.start()
    for j in jobs:
        j.join()

    print("Results: ", store)