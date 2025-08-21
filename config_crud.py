from pathlib import Path

CONFIG_FILE = Path.home() / ".mycli_config"

def save_config(data: dict):  # set multiple kvpair in dict format 
    """Save a whole dictionary to the config file"""
    lines = []
    for k, v in data.items():
        safe_value = str(v).replace("\n", "\\n")  # escape newlines first
        lines.append(f"{k}={safe_value}")
    CONFIG_FILE.write_text("\n".join(lines))


def load_config():   # fetching the entire dict 
    """Load the config file into a dictionary"""
    if not CONFIG_FILE.exists():
        print("file not found error")
        return {}

    data = {}
    for line in CONFIG_FILE.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            if v == "None":
                data[k] = None
            else:
                data[k] = v.replace("\\n", "\n")  # unescape back to real newlines
    return data



def get_config(key, default=None): # fetch a value by its key 
    """Get a single config value by key"""
    return load_config().get(key, default)


def set_config(key, value):  # set a kv pair
    """Update one config key without touching others"""
    data = load_config()
    data[key] = value
    save_config(data)
    
def flush_config():
    """empty the config file , clean sweeping """
    save_config({})
    
if __name__=="__main__":
    # run this directly form here to simple flush 
    print(load_config())
    flush_config()
