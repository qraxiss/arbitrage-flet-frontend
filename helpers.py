from threading import Thread

def thread(func):
    def inner(*args, **kwargs):
        obj = Thread(target=func,args=args,kwargs=kwargs)
        obj.start()
        return obj
    return inner