import ctypes
import os
from pathlib import Path

GENERIC_READ = 0x80000000
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
FILE_SHARE_DELETE = 0x00000004
OPEN_EXISTING = 3
FILE_ATTRIBUTE_NORMAL = 0x80

def copy_locked_file(src_path, dst_path):
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.CreateFileW(
        str(src_path),
        GENERIC_READ,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        None,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        None
    )
    
    if handle == -1 or handle == 0xFFFFFFFF:
        error = kernel32.GetLastError()
        print(f"Failed to open {src_path}, error code: {error}")
        return False
        
    try:
        # Get file size
        size_low = kernel32.GetFileSize(handle, None)
        print(f"Opened successfully! File size: {size_low} bytes")
        
        # Read file
        buffer = ctypes.create_string_buffer(size_low)
        bytes_read = ctypes.c_ulong(0)
        success = kernel32.ReadFile(handle, buffer, size_low, ctypes.byref(bytes_read), None)
        
        if success:
            with open(dst_path, "wb") as f_out:
                f_out.write(buffer.raw[:bytes_read.value])
            print(f"Copied {bytes_read.value} bytes to {dst_path}")
            return True
        else:
            print("ReadFile failed")
            return False
    finally:
        kernel32.CloseHandle(handle)

if __name__ == "__main__":
    cookie_src = Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Edge" / "User Data" / "Default" / "Network" / "Cookies"
    cookie_dst = Path("firm_environment/storage/edge_cookies_unlocked.sqlite")
    copy_locked_file(cookie_src, cookie_dst)
