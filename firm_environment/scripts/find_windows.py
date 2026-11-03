import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32

def enum_windows_callback(hwnd, extra):
    if user32.IsWindowVisible(hwnd):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            extra.append((hwnd, buff.value))
    return True

EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, ctypes.POINTER(ctypes.c_void_p))
windows = []
user32.EnumWindows(EnumWindowsProc(enum_windows_callback), ctypes.byref(ctypes.py_object(windows)))

print("Visible Windows:")
for hwnd, title in windows:
    if any(k in title.lower() for k in ["rutube", "mail", "edge", "chrome", "браузер", "вход", "виталий"]):
        print(f"HWND: {hwnd} | Title: {title}")
