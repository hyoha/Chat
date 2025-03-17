import threading
import time

def worker():
    print(f"Thread {threading.current_thread().name} started")
    time.sleep(1)
    print(f"Thread {threading.current_thread().name} finished")

threads = []
for i in range(5):
    t = threading.Thread(target=worker, name=f"Worker-{i}")
    threads.append(t)
    t.start()

for t in threads:
    t.join()
