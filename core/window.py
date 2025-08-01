import time
import win32gui
import win32con

def find_elite_window():
    def enum_callback(hwnd, results):
        title = win32gui.GetWindowText(hwnd)
        if "Elite - Dangerous" in title or "EliteDangerous64" in title:
            results.append(hwnd)
    results = []
    win32gui.EnumWindows(enum_callback, results)
    return results[0] if results else None

def focus_game_window():
    hwnd = find_elite_window()
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
        print("[Window] Fenêtre Elite Dangerous activée.")
        return True
    else:
        print("[Window] Impossible de trouver la fenêtre Elite Dangerous.")
        return False

if __name__ == "__main__":
    focus_game_window()
