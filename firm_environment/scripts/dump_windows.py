import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32

windows = []
def enum_windows_callback(hwnd, extra):
    if user32.IsWindowVisible(hwnd):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            windows.append((hwnd, buff.value))
    return True

EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, ctypes.c_void_p)
user32.EnumWindows(EnumWindowsProc(enum_windows_callback), 0)

with open("windows_list.txt", "w", encoding="utf-8") as f:
    for hwnd, title in windows:
        f.write(f"{hwnd}: {title}\n")

print(f"Total windows found: {len(windows)}")
