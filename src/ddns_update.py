import requests
import os
import datetime
import time

# Constants
CONFIG_FILE = 'domains.config'
LOG_FILE = 'ddns_update.log'
CACHE_FILE = 'ddns_update.cache'
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
        return None

# Function to update the DDNS for a domain
def update_ddns(host, domain, api_key, ip):
    url = f'https://dynamicdns.park-your-domain.com/update'
    params = {
        'host': host,
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

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - {message}"

    with open(LOG_FILE, 'a') as log_file:
        log_file.write(message + '\n')


# Function to clip the log file
def clip_log_file():
    with open(LOG_FILE, 'r') as log_file:
        lines = log_file.readlines()

    with open(LOG_FILE, 'w') as log_file:
        log_file.writelines(lines[LOG_CLIP_LINES:])

# Function to load the cached IP addresses
def load_cache():
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as cache_file:
            for line in cache_file:
                line = line.strip()
                if line:
                    parts = line.split(', ')
                    host_part, domain_part, ip_part = parts[0], parts[1], parts[2]
                    host = host_part.split(': ')[1]
                    domain = domain_part.split(': ')[1]
                    ip = ip_part.split(': ')[1]
                    cache[domain] = ip
    return cache

# Function to save the cached IP addresses
def save_cache(cache):
    with open(CACHE_FILE, 'w') as cache_file:
        for domain, ip in cache.items():
            cache_file.write(f"host: @, domain: {domain}, last_ip: {ip}\n")

# Function to read the config file and return a list of dicts
def read_config():
    config_list = []
    if not os.path.exists(CONFIG_FILE):
        print(f"Config file '{CONFIG_FILE}' not found.")
        return config_list

    with open(CONFIG_FILE, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split(':')
            if len(parts) < 3:
                log_message(f"Invalid config line: {line}")
                continue

            host = parts[0].strip()
            domain = parts[1].strip()
            api_key = parts[2].strip()
            ip_addr = parts[3].strip() if len(parts) > 3 else '127.0.0.1'

            config_list.append({
                'host': host,
                'domain': domain,
                'api_key': api_key,
                'ip_addr': ip_addr
            })

    return config_list

# Function to process each domain in the config file
def main():
    config_list = read_config()
    cache = load_cache()
    current_ip = get_external_ip()

    if not current_ip:
        log_message("Failed to get current external IP address.")
        return

    for entry in config_list:
        domain = entry['domain']
        api_key = entry['api_key']
        cached_ip = cache.get(domain)

        if cached_ip == current_ip:
            log_message(f"{domain}: No Change")
            continue

        response = update_ddns(domain, api_key, current_ip)
        if 'error' in response.lower():
            log_message(f"{domain}: Failure - {response}")
        else:
            log_message(f"{domain}: Success - {response}")
            cache[domain] = current_ip

    save_cache(cache)


if __name__ == '__main__':
    main()
