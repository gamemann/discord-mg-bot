import os

def safe_write(path: str, contents: str, remove_temp: bool = True):
    tmp = f"{path}.tmp"
    
    with open(tmp, 'w') as f:
        f.write(contents)
        
    os.replace(tmp, path)
    
    if remove_temp:
        os.remove(tmp)