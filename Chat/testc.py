import threading
import multiprocessing
import time

def thread_worker(iteration):
    print(f"쓰레드 {iteration}: 시작")
    time.sleep(1)
    print(f"쓰레드 {iteration}: 종료")

def process_worker(iteration):
    print(f"프로세스 {iteration}: 시작")
    time.sleep(1)
    print(f"프로세스 {iteration}: 종료")

if __name__ == '__main__':
    # === 쓰레드 실행 (동시 실행) ===
    print("=== 쓰레드 실행 (동시 실행) ===")
    threads = []
    for i in range(5):
        t = threading.Thread(target=thread_worker, args=(i+1,))
        threads.append(t)
        t.start()  # 쓰레드는 모두 동시에 시작

    for t in threads:
        t.join()  # 모든 쓰레드가 종료될 때까지 기다림

    # === 프로세스 실행 (순차 실행) ===
    print("\n=== 프로세스 실행 (순차 실행) ===")
    for i in range(5):
        p = multiprocessing.Process(target=process_worker, args=(i+1,))
        p.start()  # 프로세스 시작
        p.join()   # 각 프로세스가 종료될 때까지 기다림 => 순차적으로 실행됨
