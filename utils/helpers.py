import time

def wait_until(predicate, timeout=10, interval=0.2):
    start = time.time()
    while time.time() - start < timeout:
        if predicate():
            return True
        time.sleep(interval)
    return False
