from pathlib import Path

def ensure_folder(folder_path):
    path = Path(folder_path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_latest_file(folder, pattern):
    files = list(Path(folder).glob(pattern))
    if not files:
        return None
    return max(files, key=lambda f: f.stat().st_mtime)
