
## Developer Document
---

### Overview
The Python script `update_ddns.py` is designed to update dynamic DNS records using Namecheap's DDNS API. It reads a configuration file (`domains.config`), retrieves the current external IP address, and updates the DNS records if the IP address has changed. The script logs the results of these operations to a log file (`ddns_update.log`).

### Files and Directories
- `update_ddns.py`: The main Python script.
- `domains.config`: Configuration file containing domain names, API keys, and optional IP addresses.
- `ddns_update.log`: Log file to record the outcomes of DDNS updates.
- `last_ip.cache`: Cache file to store the last known IP addresses for domains.

### Dependencies
- Python 3.7 or greater
- `requests` library: Install via pip (`pip install requests`)

### Script Components
1. **Constants**:
   - Configuration and log file paths.
   - Maximum log file size and clipping lines.
   
2. **Functions**:
   - `load_last_ips()`: Loads the last known IPs from the cache file.
   - `save_last_ips()`: Saves the current IPs to the cache file.
   - `get_external_ip()`: Retrieves the current external IP address.
   - `update_ddns(domain, api_key, ip)`: Updates the DDNS for a domain using Namecheap's API.
   - `log_message(message)`: Logs messages with a timestamp to the log file.
   - `clip_log_file()`: Clips the first 10 lines of the log file if it exceeds the maximum size.
   - `process_config_file()`: Processes each domain in the config file, checks if the IP has changed, and updates the DDNS if necessary.

### Execution Flow
1. Load last known IPs from the cache.
2. Get the current external IP address.
3. Read and process each line in the configuration file.
4. For each domain, if the IP address has changed, update the DDNS record.
5. Log the results and update the cache file with the current IPs.

### Error Handling
- The script handles exceptions when making HTTP requests and logs errors accordingly.
- It skips invalid lines in the configuration file and logs a message for each skipped line.
