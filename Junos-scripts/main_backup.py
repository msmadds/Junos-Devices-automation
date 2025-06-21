from jnpr.junos import Device
from jnpr.junos.exception import *
from lxml import etree
from datetime import datetime
import os
import time
import random
import logging


#  Configuration 
HOST_FILE = "hosts.txt"
LOG_FILE = "junos_config_backup.log"

# Logging Setup 
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#  Helper Functions 
def save_config(data, hostname):
    """This function will save the config file to a dated folder with hostname in filename."""
    date_str = datetime.now().strftime('%Y-%m-%d')
    folder_path = os.path.join(os.getcwd(), date_str)
    os.makedirs(folder_path, exist_ok=True)
    config_file = os.path.join(folder_path, f"{hostname}_{date_str}.txt")
    with open(config_file, "w") as f:
        f.write(etree.tostring(data, encoding="unicode", pretty_print=True))
    logging.info(f"Saved config for {hostname} to {config_file}")

def get_hostname(dev):
    """This function will extract hostname from Junos device facts."""
    try:
        return dev.facts["hostname"]
    except Exception:
        return dev.hostname or "unknown"

def get_host_port(line):
    """This function will parse host and port from a line provided from host file like '66.29.201.210:36009'."""
    if ':' in line:
        host, port = line.strip().split(':')
        return host.strip(), int(port.strip())
    else:
        return line.strip(), 22  # if no port was provided with the host IP use default SSH port 22

def config_check(host, port, username, password):
    """This function will Connect to a JUNOS device and fetch config.Format can be set, xml or JSON """
    try:
        with Device(host=host, user=username, password=password, port=port) as dev:
            data = dev.rpc.get_config(options={"format": "set"})
            hostname = get_hostname(dev)
            save_config(data, hostname)
    except ConnectAuthError:
        logging.error(f"Authentication failed for {host}:{port}")
    except RpcTimeoutError:
        wait = random.randint(1, 5)
        logging.warning(f"RPC timeout on {host}:{port}, retrying in {wait}s")
        time.sleep(wait)
        config_check(host, port, username, password)
    except Exception as e:
        logging.error(f"Error on {host}:{port}: {str(e)}")

#  Main Function 
def main():
    if not os.path.exists(HOST_FILE):
        logging.error(f"{HOST_FILE} not found.")
        return
    
    #get login info from environment variables
    username = os.getenv("Junos_Username")
    password = os.getenv("Junos_Password")
    
    if not username or not password:
        logging.error("Missing username or Password environment variable.")
        exit(1)

    with open(HOST_FILE, "r") as f:
        for line in f:
            if line.strip():
                host, port = get_host_port(line)
                config_check(host, port, username, password)

if __name__ == "__main__":
    main()
