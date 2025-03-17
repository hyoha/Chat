import multiprocessing
import time

def worker():
    print(f"Process {multiprocessing.current_process().name} started")
    time.sleep(1)
    print(f"Process {multiprocessing.current_process().name} finished")

if __name__ == '__main__':
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, name=f"Process-{i}")
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
