
## User Manual
---

### Prerequisites
- Ensure Python 3.7 or greater is installed.
- Install the `requests` library using pip:
  ```bash
  pip install requests
  ```

### Configuration File (`domains.config`)
Create a `domains.config` file with the following format:
```
# This is a comment line
example.com:api_key_for_example_com:optional_ip_address
anotherdomain.com:api_key_for_anotherdomain_com
```

### Running the Script
Save the script as `update_ddns.py` and run it using Python:
```bash
python update_ddns.py
```

### Scheduling the Script

#### Unix/Linux (cron)
1. Open the crontab editor:
   ```bash
   crontab -e
   ```
2. Add a cron job to run the script at a desired interval (e.g., Every 15 minutes):
   ```bash
   */15 * * * * /usr/bin/python3 /path/to/update_ddns.py
   ```
3. Save and exit the editor.

#### Unix/Linux (systemd)
1. Create a systemd service file `/etc/systemd/system/update_ddns.service`:
   ```ini
   [Unit]
   Description=Dynamic DNS Update Service

   [Service]
   ExecStart=/usr/bin/python3 /path/to/update_ddns.py
   ```
2. Create a systemd timer file `/etc/systemd/system/update_ddns.timer`:
   ```ini
   [Unit]
   Description=Run Dynamic DNS Update Daily

   [Timer]
   OnCalendar=*-*-* 03:00:00
   Persistent=true

   [Install]
   WantedBy=timers.target
   ```
3. Enable and start the timer:
   ```bash
   sudo systemctl enable update_ddns.timer
   sudo systemctl start update_ddns.timer
   ```

#### macOS (launchd)
1. Create a plist file `~/Library/LaunchAgents/com.example.update_ddns.plist`:
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.example.update_ddns</string>
       <key>ProgramArguments</key>
       <array>
           <string>/usr/bin/python3</string>
           <string>/path/to/update_ddns.py</string>
       </array>
       <key>StartCalendarInterval</key>
       <dict>
           <key>Hour</key>
           <integer>3</integer>
           <key>Minute</key>
           <integer>0</integer>
       </dict>
       <key>RunAtLoad</key>
       <true/>
   </dict>
   </plist>
   ```
2. Load the job:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.example.update_ddns.plist
   ```

#### Windows (Task Scheduler)
1. Open Task Scheduler and create a new task.
2. Set the trigger to run at a desired interval (e.g., daily at 3 AM).
3. Set the action to run the Python script:
   - Program/script: `python`
   - Add arguments: `C:\path\to\update_ddns.py`
4. Save the task.

### Logs
The script logs messages to `ddns_update.log` with timestamps. It also clips the log file to keep it under 25KB.

