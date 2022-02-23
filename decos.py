import inspect
import logging
import sys
import traceback

from logs.client_log_config import LOGGER

if sys.argv[0].find('client.py')==-1:
    LOGGER = logging.getLogger('server')
else:
    LOGGER = logging.getLogger('client')

def log(func_to_log):
    def log_saver(*args,**kwargs):
        ret = func_to_log(*args,**kwargs)
        LOGGER.debug(f'Вызвана функция{func_to_log.__name__}  '
                     f' из модуля {func_to_log.__module__}'
                     f' из функции {traceback.format_stack()[0].strip().split()[-1]}'
                     f' из функции {inspect.stack()[1][3]}')
        return ret
    return log_saver

