from multiprocessing import Process
from server import run_server
from bot import run_bot


if __name__ == '__main__':
    Process(target=run_bot).start()
    Process(target=run_server).start()
    