import os
from datetime import datetime, timedelta
from auth import get_service
import json

STATE_FILE = 'email_tracker.json'
MILESTONES = [1, 5, 10, 15, 20]

def save_state(data):
    with open (STATE_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_state():
    with open (STATE_FILE, 'r') as f:
        return json.load(f)

def get_date(last_sprint=True):
    if last_sprint:
        query_date = (datetime.now() - timedelta(days=datetime.now().weekday() + 14)).strftime('%Y/%m/%d')
    else:
        query_date = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%Y/%m/%d')
    
    return query_date

def fresh_state():
    return {'sprints': {},
            'total_rejections': 0,
            'total_applications': 0,
            'cycle_rejections': 0,
            'completed_milestones': [],
            }

def check_milestone(total_rejections, completed):

    while total_rejections >= MILESTONES[-1]:    
        for milestone in MILESTONES:
            if milestone not in completed:
                print(f'New Milestone achieved!: {milestone}\n')
                completed.append(milestone)

        total_rejections = total_rejections - MILESTONES[-1]
        completed = []
        print(f'\nCycle Completed! Carrying over: {total_rejections} rejections')
    
    for milestone in MILESTONES:
        if total_rejections >= milestone and milestone not in completed:
            print(f'New Milestone achieved!: {milestone}\n')
            completed.append(milestone)

    print(f'Total remaining : {total_rejections}')
    print(f'Completed milestones: {completed}')

    return total_rejections, completed

def count_sprint_emails(date, label, after=None):

    query = (f'label:{label} after:{date}')
    service = get_service()
    result = service.users().messages().list(userId="me", q=query).execute()
    messages = result.get("messages", [])
    
    if not messages:
        return 0

    print(f'Total Emails for label {label}: {len(messages)}')

    return len(messages)

def run():

    #1) Loading or initialising state
    if os.path.exists(STATE_FILE):
        print("File Found, loading.....")
        state = load_state()
    else: 
        print("No File found, starting fresh...")
        state = fresh_state()

    print(f"\nCurrent Total Rejections : {state['total_rejections']}")
    print(f"Completed Milestones: {state['completed_milestones']}\n")

    #2) Current Sprint & Update / get new emails
    query_date =  get_date()
    
    #   For this date, update -  Job applications:
    applications = count_sprint_emails(date=query_date, label="Job Applications")

    #   For this date, update -  Job rejections:
    rejections = count_sprint_emails(date=query_date, label="Job Rejections")

    print(f'\nCurrent Sprint: {query_date}\n')
    
    #3) Assign new data
    if query_date not in state['sprints']:
        state["sprints"][query_date] = {"applications": 0, "rejections": 0}

    state["sprints"][query_date]["applications"] = applications
    state["sprints"][query_date]["rejections"] = rejections

    #4) tracking global emails across sprints

    # 4.1 Tracking rejections
    previous_total = state.get('total_rejections', 0)
    current_total = sum(s['rejections'] for s in state['sprints'].values())
    
    state['total_rejections'] = current_total
    new_rejections = current_total - previous_total

    # 4.2 TODO do the same for applications?
    state['total_applications'] = sum(s['applications'] for s in state['sprints'].values())

    #5) Check current milestones

    state['cycle_rejections'] += new_rejections

    state['cycle_rejections'], state['completed_milestones'] = check_milestone(
        total_rejections=state['cycle_rejections'],completed=state['completed_milestones'])
    
    #6) Save progress
    print("\nUpdating current Progress!")
    save_state(state)
    print(f"Updated Total Rejections: {state['total_rejections']}")
    print(f"Milestones: {state['completed_milestones']}")

if __name__ == "__main__":

    run()