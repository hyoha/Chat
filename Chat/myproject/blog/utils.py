# blog/utils.py

import subprocess
import re
import os
import threading
import time
import sys

def load_model_config():
    """
    모델과 파라미터(온도, top_p, system 메시지 등)를 딕셔너리 형태로 로드해서 반환합니다.
    필요하다면 별도 JSON 파일에서 읽어오거나, DB에서 불러올 수도 있습니다.
    """
    model_config = {
        "from": "hf.co/Bllossom/llama-3.2-Korean-Bllossom-3B-gguf-Q4_K_M",
        "system": "You are a helpful assistant providing answers in Korean.",
        "temperature": 0.1,
        "top_p": 0.8
    }
    return model_config

def remove_ansi_escape(text):
    """
    ANSI escape 코드를 제거하고, 앞뒤 공백을 정리한 문자열을 반환합니다.
    """
    ansi_escape = re.compile(r'\x1b\[[0-9;]*[mGKHJ]|\x1b\[[0-9;]*[@-~]')
    return ansi_escape.sub('', text).strip()

def run_model(question):
    """
    question(질문)에 대해 ollama 모델을 실행하고,
    line-by-line으로 읽은 stdout을 문자열로 누적 후 반환합니다.

    - load_model_config()로 모델 경로, system 메시지 등을 불러옴
    - data.txt(옵션) 읽어 prompt에 포함
    - 서브프로세스로 ollama CLI 실행
    - 모델이 답변을 생성 중일 때, 별도의 스레드에서 '무한 Progress Bar' 형태로 진행률을 표시
    - 최종적으로 모델 답변이 끝나면 Bar를 중단하고 결과를 반환
    """

    # 1. 모델 config 읽기
    config = load_model_config()
    model_path = config.get("from", "")
    system_message = config.get("system", "")

    # 2. data.txt 읽기 (선택)
    data_from_file = ""
    try:
        with open('data.txt', 'r', encoding='utf-8') as f:
            data_from_file = f.read().strip()
    except Exception as e:
        print("[DEBUG] data.txt 읽기 오류:", e)

    # 3. prompt 구성
    prompt = f"""
{system_message}
{data_from_file}

Question: {question}
Answer:
"""
    print("[DEBUG] 최종 prompt:", prompt)

    # 4. ollama 명령어 구성
    command = [
        "ollama", "run",
        model_path,
        prompt
    ]
    print("[DEBUG] 실행 명령어:", command)

    # --- 진행 상태 표시(Progress Bar)용 플래그 ---
    stop_progress_bar = False

    def progress_bar():
        """
        무한(불확정) 형태의 Progress Bar를 터미널에 표시하는 함수.
        stop_progress_bar가 True가 될 때까지 반복하며,
        간격(time.sleep)마다 bar를 업데이트해서 진행 중임을 표현한다.
        """
        bar_length = 20  # Progress bar 총 길이
        position = 0

        while not stop_progress_bar:
            # position이 bar_length보다 커지면 0으로 리셋
            position = (position + 1) % (bar_length + 1)
            # position만큼 '=' 채우고 나머지는 ' '로 채움
            bar_filled = '=' * position
            bar_empty = ' ' * (bar_length - position)
            # \r로 맨 앞으로 이동 후, 전체를 덮어쓰고 flush
            # ex) [===        ]
            sys.stdout.write(f"\r[DEBUG] [{bar_filled}>{bar_empty}] 모델 답변 생성 중...")
            sys.stdout.flush()
            time.sleep(0.1)

        # 중단 시 마지막으로 한 번 개행
        sys.stdout.write("\r[DEBUG] 모델 응답을 받았습니다.                       \n")
        sys.stdout.flush()

    try:
        # 서브프로세스 실행
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False  # 바이너리 모드, 필요시 decode
        )

        # 5. Progress Bar 스레드 시작
        bar_thread = threading.Thread(target=progress_bar)
        bar_thread.start()

        total_output = ""
        stderr_buffer = b""

        # 6. 모델 출력 & 에러 읽기
        while True:
            line = process.stdout.readline()
            err_line = process.stderr.readline()

            if not line and not err_line:
                # 더 이상 읽을 내용 없으면 종료
                break

            # stdout 처리
            if line:
                try:
                    decoded_line = line.decode('utf-8', errors='ignore')
                except UnicodeDecodeError:
                    decoded_line = line.decode('latin-1', errors='replace')
                cleaned_line = remove_ansi_escape(decoded_line)
                if cleaned_line:
                    total_output += cleaned_line

            # stderr 처리 (디버그)
            if err_line:
                try:
                    decoded_err = err_line.decode('utf-8', errors='ignore')
                except UnicodeDecodeError:
                    decoded_err = err_line.decode('latin-1', errors='replace')
                stderr_buffer += decoded_err.encode('utf-8')

        process.wait()

        # 7. Progress Bar 종료 신호 & 스레드 합류
        stop_progress_bar = True
        bar_thread.join()

        # 8. stderr 메시지 출력 (브라유 스피너 등 제거)
        if stderr_buffer:
            braille_pattern = re.compile(r'[\u2800-\u28FF]+')
            decoded_err = stderr_buffer.decode('utf-8', errors='ignore')
            decoded_err_no_spinner = braille_pattern.sub('', decoded_err)
            stderr_str = remove_ansi_escape(decoded_err_no_spinner).strip()
            if stderr_str:
                print("[DEBUG] stderr:", stderr_str)

        # 9. 최종 출력 확인
        result = total_output.strip()
        if result:
            return result
        else:
            return "모델에서 출력된 내용이 없습니다."

    except Exception as e:
        stop_progress_bar = True
        print("[DEBUG] 예외 발생:", e)
        return f"오류가 발생했습니다: {e}"

# 테스트용: 직접 실행 시 동작 확인
if __name__ == "__main__":
    test_question = "테스트 질문입니다. 안녕하세요?"
    answer = run_model(test_question)
    print("=== 테스트 질문 ===")
    print(test_question)
    print("=== 모델 답변 ===")
    print(answer)
