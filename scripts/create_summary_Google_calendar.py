# Script to extract information from Google Calendar and compute how much time is spend weekly on different activities 
# determined by different calendar categories on Google calendar

# 0. IMPORT NECESSARY LIBRARIES
# Importing the necessary libraries
from googleapiclient.discovery import build # interacts with google calendar API
from google_auth_oauthlib.flow import InstalledAppFlow # handles the OAuth2 authentication
from google.auth.transport.requests import Request # handles the OAuth2 authentication
import pickle # saves and reloads authentication tokens to avoid logging in repeatedly
from google.auth.exceptions import RefreshError # handles token refresh errors
from datetime import datetime, timedelta # handles dates and times
import os # interacts with the operating system
import yaml # to save the markdown file with YAML front matter

# 1. MODIFY THE PARAMETERS SPECIFIC TO THE USER

# Enter path to your Obsidian vault
Obsidian_path = # WRITE HERE THE PATH TO THE FOLDER WHERE YOU WANT TO SAVE THE WEEKLY SUMMARY
print('Obsidian path is : ', Obsidian_path)

# Specify the calendars to include in the summary
include_list = ["Work", "Work out", "Learning", "Hobbies", "Social"]

# Get the current path, to load Google API credentials later, modify if they are not in the same folder as this script
script_dir = os.path.dirname(os.path.abspath(__file__)) # get folder containing this script
print('current path is : ', script_dir)

# -----------------------------------------------------------

# 2. DEFINE FUNCTION TO AUTHENTICATE GOOGLE CALENDAR API (access the data of your Google calendar)
def authenticate_google():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']  # Read-only permission
    creds = None
    token_path = os.path.join(script_dir, 'token.pickle') # assumes token.pickle is in the same directory as the script
    
    # Step 1: Load existing credentials
    if os.path.exists(token_path):  # Check if credentials are already saved
        with open(token_path, 'rb') as token:
            creds = pickle.load(token) # load credentials

    # Step 2: Handle missing or invalid credentials
    if not creds or not creds.valid: # check if the credentials are missing or invalid
        # Step 2a: Try refreshing the token if possible
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                print("Token expired. Deleting and reauthenticating...")
                os.remove(token_path)  # Remove the old token
                creds = None  # Force reauthentication

        # Step 2b: Trigger reauthentication if refresh is not possible
        if not creds:
            credentials_path = os.path.join(script_dir, 'credentials.json')  # Path to credentials.json
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)  # Open a browser for user login

        # Step 3: Save new credentials to token.pickle
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    # Step 4: Return the authenticated Google Calendar service
    return build('calendar', 'v3', credentials=creds)
                
# 3. DEFINE FUNCTION TO LIST CALENDARS
def list_calendars(service, include_calendars = None):
    calendars_result = service.calendarList().list().execute() # get list of calendars in Google Calendar
    calendars = calendars_result.get('items', []) # extract the items from the list
    calendars_info = {} # initialize dictionary to store calendar information
    for calendar in calendars:
        # extract the name and id of the calendar
        calendar_summary = calendar['summary']
        calendar_id = calendar['id']

        # check if the calendar is in the list of calendars to include
        if calendar_summary not in include_calendars:
            continue
        
        # add the calendar name and id to the dictionary of calendars
        calendars_info[calendar_summary] = calendar_id
    return calendars_info # return the dictionary of calendars

# 4. DEFINE FUNCTION TO FETCH EVENTS FROM CALENDARS
def fetch_events(service, calendars, start_date, end_date):
    all_events = [] # initialize list to store all calendar events
    for calendar_name, calendar_id in calendars.items(): # iterate over the calendar names and ids
        try:
            # get the events from the calendar within the specified time range
            events = service.events().list(
                calendarId=calendar_id,
                timeMin=start_date.isoformat() + 'Z',
                timeMax=end_date.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute().get('items', [])

            # Add calendar name to each event
            for event in events:
                event['calendar_name'] = calendar_name
            all_events.extend(events)

        except Exception as e:
            print(f"Error fetching events for calendar '{calendar_name}': {e}")
    return all_events # output all verified events

# 5. DEFINE FUNCTION TO CALCULATE TIME SPENT ON EVENTS
def calculate_time_spent(events):
    time_spent = {} # initialize dictionary to store time spent on each calendar
    for event in events: # iterate over all events
        # Handle timed events with 'dateTime'
        if 'dateTime' in event['start']: # extract the start and end times of the event
            start = datetime.fromisoformat(event['start']['dateTime'].replace('Z', '+00:00'))
            end = datetime.fromisoformat(event['end']['dateTime'].replace('Z', '+00:00'))
        # Handle all-day events with 'date'
        elif 'date' in event['start']: # extract the start and end dates of the event
            start = datetime.fromisoformat(event['start']['date'] + 'T00:00:00+00:00')
            end = datetime.fromisoformat(event['end']['date'] + 'T00:00:00+00:00')
        else:
            # Skip events without valid date information
            print(f"Skipping event without valid date: {event}")
            continue
        
        # Calculate duration of the event
        duration = (end - start).total_seconds() / 3600 
        
        # Identify calendar category (e.g., Work, Social)
        calendar = event.get('organizer', {}).get('displayName', event['calendar_name']) # Use organizer's name if available
        time_spent[calendar] = time_spent.get(calendar, 0) + duration # add the duration to the total time spent for each calendar category
    
    return time_spent # return dictionary with the total time spent on each calendar category

# 6. DEFINE FUNCTION TO GENERATE SUMMARY
def generate_summary(time_spent, weekly_label):
    # initialize dictionary with the label for that week
    weekly_data = {
        "week": weekly_label,
    }
    for calendar, hours in time_spent.items(): # iterate over the dictionary of total time spent on each category
        weekly_data[calendar] = f"{hours:.2f}" # extract hours and print out the total time spent on each category
    return weekly_data # output the dictionary with the weekly summary and weekly label

# -----------------------------------------------------------

# 7. MAIN FUNCTION TO EXECUTE THE STEPS
if __name__ == '__main__':
    # Step 1: Authenticate Google Calendar API and list calendars
    service = authenticate_google()  

    # Step 2: Get list of calendars, excluding specific ones
    calendars = list_calendars(service, include_calendars=include_list)

    # Step 3: Define time range (last week)
    start_date = datetime.utcnow() - timedelta(days=7)
    start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = datetime.utcnow()
    end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=0)
    print('start date is: ', start_date)
    print('end date is: ', end_date)

    # Step 4: Fetch events
    events = fetch_events(service, calendars, start_date, end_date)
 
    # Step 5: Calculate time spent
    time_spent = calculate_time_spent(events)

    # Step 6: Generate summary
    week_label = start_date.strftime('%Y-%m-%d') 
    summary = generate_summary(time_spent, week_label)

    # Step 7: Save weekly summary
    summary_path = os.path.join(Obsidian_path, f'Weekly_Tracker_{week_label}.md')
    with open(summary_path, "w") as f:
        f.write('---\n')  # YAML frontmatter start
        yaml.dump(summary, f)
        f.write('---\n')  # YAML frontmatter end

    print('Summary saved in ', summary_path)
