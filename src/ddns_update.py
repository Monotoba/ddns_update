import requests
import os

# Constants
CONFIG_FILE = 'domains.config'
LOG_FILE = 'ddns_update.log'
MAX_LOG_SIZE = 25 * 1024  # 25KB
LOG_CLIP_LINES = 10


# Function to get the current external IP address
def get_external_ip():
    try:
        response = requests.get('http://ipecho.net/plain')
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        log_message("Failed to get external IP address: " + str(e))
        return None


# Function to update the DDNS for a domain
def update_ddns(domain, api_key, ip):
    url = f'https://dynamicdns.park-your-domain.com/update'
    params = {
        'host': '@',
        'domain': domain,
        'password': api_key,
        'ip': ip
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return "Error: " + str(e)


# Function to log messages to the log file
def log_message(message):
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > MAX_LOG_SIZE:
        clip_log_file()

    with open(LOG_FILE, 'a') as log_file:
        log_file.write(message + '\n')


# Function to clip the log file
def clip_log_file():
    with open(LOG_FILE, 'r') as log_file:
        lines = log_file.readlines()

    with open(LOG_FILE, 'w') as log_file:
        log_file.writelines(lines[LOG_CLIP_LINES:])


# Function to read the config file and process each domain
def process_config_file():
    if not os.path.exists(CONFIG_FILE):
        print(f"Config file '{CONFIG_FILE}' not found.")
        return

    with open(CONFIG_FILE, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split(':')
            if len(parts) < 2:
                log_message(f"Invalid config line: {line}")
                continue

            domain = parts[0]
            api_key = parts[1]
            ip = parts[2] if len(parts) > 2 else get_external_ip()

            if not ip:
                log_message(f"Failed to get IP address for {domain}")
                continue

            response = update_ddns(domain, api_key, ip)
            if 'error' in response.lower():
                log_message(f"{domain}: Failure - {response}")
            else:
                log_message(f"{domain}: Success - {response}")


if __name__ == '__main__':
    process_config_file()
