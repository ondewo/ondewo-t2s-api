import multiprocessing
import requests
from typing import List

ONDEWO_T2S_URL: str = "http://0.0.0.0:40015/text2speech"
TEXTS_FILE: str = "responses.txt"
NUM_PROC: int = 5


def send_to_ondewo_t2s(text: str) -> None:
    print(f"Sending text: {text}")
    ans = requests.post(ONDEWO_T2S_URL, data={'text': text})
    if ans.status_code != 200:
        print(f"Server returned status {ans.status_code}!")


def main() -> None:
    with open(TEXTS_FILE) as rfile:
        texts: List[str] = rfile.read().splitlines()

    pool = multiprocessing.Pool(1)
    pool.map(send_to_ondewo_t2s, texts)


if __name__ == "__main__":
    main()
