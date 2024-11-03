from datetime import datetime

def debug_msg_raw(req_lvl: int, cur_lvl: int, msg: str, log_dir: str = None):
    if cur_lvl < req_lvl:
        return
    
    raw_msg = f"[{req_lvl}] {msg}"
    
    print(raw_msg)
    
    # Check for logging to a file.
    if log_dir is not None:
        # Format message with date prepended.
        date_f = datetime.now().strftime("%y-%m-%d %H-%M:%S")
        
        log_msg = f"[{date_f}]{raw_msg}"
        
        # Format file name.
        date_f = datetime.now().strftime("%y-%m-%d")
        file_f = f"{date_f}.log"
        
        full_path = f"{log_dir}/{file_f}"
        
        with open(full_path, 'a+') as f:
            f.write(f"{log_msg}\n")
        
def debug_msg(req_lvl: int, cfg: any, msg: str):
    log_dir: str = None
    
    if cfg.debug.log_to_file:
        log_dir = cfg.debug.log_dir
        
    debug_msg_raw(req_lvl, cfg.debug.verbose, msg, log_dir)