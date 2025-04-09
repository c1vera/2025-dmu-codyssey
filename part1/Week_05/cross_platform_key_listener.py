import sys
import platform
import time

def is_q_pressed():
    current_os = platform.system()

    if current_os == 'Windows':
        import msvcrt
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            return key == 'q'
        return False

    elif current_os in ('Linux', 'Darwin'):
        import tty
        import termios
        import select

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setcbreak(fd)  # set raw mode (non-blocking)
            dr, _, _ = select.select([sys.stdin], [], [], 0)
            if dr:
                key = sys.stdin.read(1).lower()
                return key == 'q'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return False

    else:
        raise OSError("Unsupported OS: " + current_os)
