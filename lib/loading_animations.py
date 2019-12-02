import itertools
import threading
import time
import sys


class AnimationTask:

    def __init__(self, loadingMessage="loading", successMessage="Done!"):
        self._running = True
        self.loadingMessage = loadingMessage
        self.successMessage = successMessage

    def terminate(self):

        self._running = False

    def run(self):
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if not self._running:
                break
            sys.stdout.write('\r' + self.loadingMessage + ' ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.flush()
        sys.stdout.write('\r\r'+self.successMessage+'     \n')


class Animation:
    def __init__(self, loadingMessage="loading", successMessage="Done!"):
        self.animation_task = AnimationTask(loadingMessage, successMessage)
        self._thread = threading.Thread(target=self.animation_task.run)

    def start(self):
        self._thread.start()

    def stop(self):
        self.animation_task.terminate()
