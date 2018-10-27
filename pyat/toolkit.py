from pyat.adb import ADB
from pyat import binder
from pyat.extras import *


class PYAToolkit(object):
    def __init__(self, device_id, need_log=None):
        self.device_id = device_id
        self.need_log = bool(need_log)
        self.adb = ADB(device_id)

    @classmethod
    def bind_cmd(cls, func_name, command):
        return binder.add(func_name, command)

    @classmethod
    def bind_func(cls, real_func):
        return binder.add(real_func.__name__, real_func)

    def __getattr__(self, item):
        if not binder.is_existed(item):
            raise AttributeError('function {} not found'.format(item))
        command = binder.get(item)

        # is real function
        if callable(command):
            return lambda *args, **kwargs: command(*args, toolkit=self, **kwargs)
        # is command
        return lambda: self.adb.run(command)


# build-in functions bind here
PYAToolkit.bind_func(real_func=download_and_install)
