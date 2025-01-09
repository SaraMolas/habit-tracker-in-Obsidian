# Setting Up the Cron Job to run the habit tracker weekly

This guide explains how to set up a cron job to run the Python script to extract the Google Calendar summary
every Sunday at 23:59.

## **For Mac and Linux**

### 1. **Open the Crontab Editor**
To edit the crontab, open a terminal and type:
```bash
crontab -e
```

### 2. **Add a New Cron Job**
Add the following line to the crontab file:
```bash
59 23 * * 0 /path/to/python3 /path/to/your/script.py
```

- **59 23 \* \* 0**: Runs the script at 23:59 every Sunday.
- **/path/to/python3**: Replace with the path to your Python executable (e.g., `/usr/bin/python3`).
- **/path/to/your/script.py**: Replace with the full path to your Python script (`path/create_summary_Google_calendar.py`).

### 3. **Save and Exit**
- If using `nano` as the editor: Press `Ctrl+O` to save and `Ctrl+X` to exit.

## **For Windows**

Windows does not use cron but has a similar feature called **Task Scheduler**. Follow these steps:

### 1. **Open Task Scheduler**
1. Press `Win + R` and type `taskschd.msc` to open Task Scheduler.
2. Click **Create Basic Task** from the right-hand panel.

### 2. **Create a New Task**
1. **Name the Task:** Enter a descriptive name like "Run Habit Tracker Script."
2. **Set the Trigger:**
   - Choose **Weekly** and specify Sunday at 23:59.
3. **Set the Action:**
   - Select **Start a Program** and specify:
     - **Program/script:** Path to your Python executable (e.g., `C:\Python39\python.exe`).
     - **Add arguments:** Path to your script (e.g., `C:\path\to\your\script.py`).

4. **Finish and Save:**
   - Review your settings and click **Finish**.

--- 

## **Verify the Setup**
- For Mac/Linux: Run `crontab -l` to see your cron jobs.
- For Windows: Open Task Scheduler and check that your task is listed.

### Notes:
- Ensure the Python script and required dependencies (e.g., libraries) are properly installed and accessible from the specified paths.
- Logs for cron jobs on Mac/Linux can usually be found in `/var/log/syslog` or `/var/log/cron`.
