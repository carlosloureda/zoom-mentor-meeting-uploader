import itertools
import threading
import time
import sys

# show_animation = True


# def _animate(loadingMessage="loading", successMessage="Done!"):
#     global show_animation
#     for c in itertools.cycle(['|', '/', '-', '\\']):
#         if not show_animation:
#             break
#         sys.stdout.write('\r' + loadingMessage + ' ' + c)
#         sys.stdout.flush()
#         time.sleep(0.1)
#     sys.stdout.write('\n'+successMessage+'     \n')


# def show_loading_animation(loadingMessage, successMessage):
#     t = threading.Thread(target=_animate, args=(
#         loadingMessage, successMessage))
#     t.start()


# def hide_loading_animation():
#     global show_animation
#     show_animation = False


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
        sys.stdout.write('\r'+self.successMessage+'     \n')


class Animation:
    def __init__(self, loadingMessage="loading", successMessage="Done!"):
        self.animation_task = AnimationTask(loadingMessage, successMessage)
        self._thread = threading.Thread(target=self.animation_task.run)

    def start(self):
        self._thread.start()

    def stop(self):
        self.animation_task.terminate()

# animation = Animation("Downloading webdriver",
#                       "Finished Downloading webdriver!")
# animation.start()
# time.sleep(3)
# animation.stop()
