import time


def percentage(part, whole):
    p = 100 * float(part) / float(whole)
    return int(p)


def show_timed_progress(t, callback, hault=lambda: False):
    start = time.time()
    end = time.time()

    while end - start < t:
        if hault():
            break
        p = percentage(end - start, t)
        callback(p)
        time.sleep(0.5)
        end = time.time()

    callback(100)
