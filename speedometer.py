import math
import time
import readchar
import threading
import signal

wheel_size = 26


def speed_listener(state, stop_event):
    def speedometer():
        while not stop_event.is_set():
            r, p, s = state
            state[0] = 0
            state[1] = time.time() if r > 0 else p
            state[2] = current_speed(r, p, s)
            print('current speed:', state[2])
            time.sleep(0.01)
    return speedometer


def current_speed(r, p, s):
    real = calculate_speed(r, p) if r > 0 else s
    potential = calculate_speed(1, p)
    speed = min(real, potential)
    return math.floor(speed) if potential > 1.8 else 0  # jump to 0 early for aesthetics


def calculate_speed(r, p):
    t = (time.time() - p) / 60 / 60  # hours
    d = (wheel_size * math.pi) * r / 12 / 5280  # miles
    return d / t if t > 0 else 0


def input_listener(state, stop_event):
    def listen():
        while not stop_event.is_set():
            key = readchar.readkey()
            if key == ' ':
                state[0] += 1
            elif key == 'q':
                stop_event.set()
                exit(0)
            else:
                print(f"Key pressed: {key}")
    return listen


def main():
    p = time.time()
    r = 0
    state = [r, p, 0]
    stop_event = threading.Event()
    rev_listener = input_listener(state, stop_event)
    speedo_calc = speed_listener(state, stop_event)

    input_thread = threading.Thread(target=rev_listener, daemon=False)
    speedo_thread = threading.Thread(target=speedo_calc, daemon=False)

    speedo_thread.start()
    input_thread.start()

    def signal_handler(signum, frame):
        print("\nShutting down...")
        stop_event.set()
        input_thread.join(timeout=1)
        speedo_thread.join(timeout=1)
        exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        while not stop_event.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        stop_event.set()
        input_thread.join(timeout=1)
        speedo_thread.join(timeout=1)


main()
