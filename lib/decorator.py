#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from colorama import *
init(autoreset=True)

from functools import wraps
# from tabulate import tabulate

def decor_function_call(func):
    """
    Декоратор, оформляющий код принтами начала и конца
    """
    import time
    @wraps(func)
    def wrapper(*args, **kwargs):
        t = time.clock()
        fname = func.__name__
        print (Fore.GREEN + '################### Start {} ################').format(fname)
        print "Arguments: ", kwargs
        res = func(*args, **kwargs)

        print ( time.clock() - t)
        print (Fore.GREEN + '--------------------------------------------------------')
        return res
    return wrapper
