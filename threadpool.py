import threading
import queue
import time
import contextlib


class ThreadPool():

    StopEvent = object()

    def __init__(self, max_thread_num=10):

        self._que = queue.Queue()
        self._max_num = max_thread_num
        self.terminal = False
        self._generate_list = []
        self._free_list = []

    def push(self, func, args, kw, callback=None):

        """
        # push func to thread pool
        #
        # Parameters:
        # func : function | user function
        # args : tuple | function parameters
        # kw : dict | function parameters
        # callback : function | hander return result
        """

        if len(self.free_list) == 0 and len(self.generate_list) < self.max_num:
            self._generate_thread()
        w = (func, args, kw, callback)
        self._que.put(w)

    def _generate_thread(self):

        thread = threading.Thread(target=self._call)
        thread.start()

    def _call(self):

        cthread = threading.currentThread
        self._generate_list.append(cthread)

        event = self._que.get()

        while event != StopEvent:

            func, args, kw, callback = event

            try:
                result = func(*args, **kw)
                status = True
            except Exception as e:
                status = False
                result = e

            if callback is not None:
                try:
                    callback(status, result)
                except Exception as e:
                    pass

            with self._work_state():
                event = self._que.get()

        else:
            self._generate_list.remove(cthread)

    def close(self):

        """
        # close and clear thread pool
        # wait until all process done
        """

        for i in range(len(self._generate_list)):
            self._que.put(StopEvent)

    def terminate(self):

        self.terminal = True
        while self.generate_list:
            self._que.put(StopEvent)
        self._que.empty()

        return self.terminal

    def _work_state(self):

        self._free_list.append(threading.currentThread)
        try:
            yield
        finally:
            self._free_list.remove(threading.currentThread)
