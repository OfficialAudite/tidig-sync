import requests, re, os
from base64 import b64encode
import PySimpleGUI as sg
from datetime import datetime, timedelta
import pickle

pattern = re.compile(r'\((.*?)\)')
ICON = b"iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAMAAACdt4HsAAADAFBMVEVHcEz19vcTExMXFxcVFRUAAAD19fUeHh4lJSUCAgImJibu7u4QEBDy8vJEREQ0NDQxMTHOzs6cnJxra2slJSUTExNkZGRzc3OdnZ1ISEhYWFjS0tLg4OCKioqbm5urq6t1dXVoaGihoaHGxsZra2tdXV24uLi9vb1eXl6kpKS2tranp6eFhYWVlZXR0dHb29u9vb3n5+fDw8OBgYGsrKzIyMi+vr7h4eF2dnZ0dHRfX18EBij+/v7////9/f4DChMDESECBQsEFCgDDBcDDx4DEyYEGjMFGC4DCA8DDRoEFisEHTgBAgYJJkUFHzwGDx0RLk36+vsGEyUNK0oIEyEOFiEQK0cOJkITKUIPHCz4+fkJIj4KIDoTM1T8/PwPITYHIkEOJT4PHzEuSWQMExwZNVQdPFwXN1gLGy8LFycfNk4KGSshRWoUHSkbLUIRM1gWMlAMLlEnTHEoOk4mSGsYJDIaKj0fMEMJHTUSMFB5eoMPIzoXLUYhOVMHDBTs7e6BkJ8AAAIHGzIWL0suRF0hNEkIJ0opRWIJEBkkQF2Ai5cUJjsvUXPd3d3MycpfcYK/vL7X1dXQ1dqXlJkmPVUfOlcMMFcfLT0bMUnx8vLh4eJqf5FxjKOCh5Hm5eZ7g46IhotyhJUTPGYZJjbo6eoPNFt8gIlYdI4pQFiPkZd5h5Sdmp+CgolthJqsqKvS2N+3trkyTmscQGUWIS0qUXhqeolIW2/T0tTHxMYkMkSIi5NmeIpOZ3+AladWaXrHz9ezu8PCxso/TV0hQmMfSnUqQlszQlI2S2JzgI4+WneAfYQ9RlASOF+cqrk5Y4wwVntFVWUuP1BifZVCcqDPzs+joqZlg556j6M7UmuFi5bh5OiPmaMjKjLY3eJsdoIvWoUWQ3AsNkKstsCcpa8/YYO6w8xVgqw3XYIjV4lGa49MYnZ7jJySjpKMiI3ByNDh6PCYnaQzZ5peaHJrjrAsXo88aZSin6O4vsVyd32prrRTbYeNn7KDoLpHcEz1AwYXBQCmL02RAAABAHRSTlMA/x81ChL9AQUPQPQa+G5MWdW8KCYsUXqjOXvp71l2q5JDrtCSb7rAi5bTvmal2t7a8N6qzdnV5KCeiv//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////AP81hAyXlQAACsxJREFUWMO0VmlUk2cWLiqEZTweq7U6Z3TsdKrHM5329Edn/rxZyPZlIftO9oQkJCQkgZCAEOAkhB1F1kQWFVBAtOwiCIqySUWtVuu+a9U6tS4dp+38mTeJVpl2nHbOmfsn+fK998ldnufe9403/r+Ggva/ukYvW71mw++hbVizeln0r4RBLVuzLg6g0SBk8DNu3ZplvxwjevV6RcgTg1FwOAoMJvTAWb86+pe5v/9h6HxgS+UnXdWdndVdn1RuCYQQP3z/v0Og3lkKTyryKrsu5I+N7Q3ajnNjpU3VlXlBjKXvvD4R1KKV8Bin4mxTaePp+7Plw1Na7VSqVjs72pjf9KyCA6E3LHpt7T6AiTc/u7Dj4LCv6KS5xGnqKHJrSsR+p2Om/VxTVzMsx9LXVHNFHAARPU27R4cFSbnuAYc73VSgLYEAZdn6Mn/56Lk9PREAfPSf0kCtiAKgrbr04HCGL8GSkDORVqM1dfQWldWKytgGsVjnLWrPr24DYPEK1M/7RwDMlpHd0/Df6y1JxUbdZIm2o6a8N1UnVkJ/uVqUXTL6YHsFBkT9HAJq1WKAGbowmC6Ij08S1FAyKF7zRFFNyUB5ji5HLc8Wy2XZYpPv/rk9QxiweNVPEFALfgf9Rw50FPOxCblJznpBcbahr8TtSEvz64QiebZXJFLr/NpebcOeLRjw19/8hD7rAdg6MjgsUGJTKPEC41RxPyurRVdb7nCYdGIeW5wlU3tNHbddFlfDnq0ArPs3SqHeBiCv8+gpSzFLk5scT5GUuY3FBXuP3zl06M6thvQ5tVCkFulM92ssucaSxq8DALw9P4nliwHn7IPppH4Li59c7KEUa4q+q4IqChuoGrTJpF7TbW1GLp9uvzv2jAPiFsxL4A8AnLmwr1+Q29+axE8RZFKutqHn2cXNIlv5ydZcHLNwp/mHpjMArHw1iVUKEOhs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"

def save_to_csv(data, filename="output.csv"):
    header = "Datum,Artikel,Tid (timmar),Kund,Projekt,Aktivitet,Ärendenummer,Beskrivning\n"
    with open(filename, "w", encoding="utf-8", newline='') as f:
        f.write(header)
        f.write(data)
    sg.popup(f"Data saved to {filename} successfully!", title='Success')

def round_to_half_hour(seconds):
    hours = int(seconds) / 3600
    rounded_hours = round(hours * 2) / 2
    return int(rounded_hours) if rounded_hours.is_integer() else round(rounded_hours, 1)

def create_auth_header(email, password):
    encoded_credentials = b64encode(f"{email}:{password}".encode('utf-8')).decode('ascii')
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {encoded_credentials}'
    }

def get_data_from_api(url, headers):
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code} {response.text}")
        return None

def construct_data(email, password, datefrom, dateto):
    headers = create_auth_header(email, password)
    # is datefrom and dateto empty
    if not datefrom or not dateto:
        timedata = get_data_from_api('https://api.track.toggl.com/api/v9/me/time_entries', headers)
    else:
        timedata = get_data_from_api(f'https://api.track.toggl.com/api/v9/me/time_entries?start_date={datefrom}&end_date={dateto}', headers)
    
    if not timedata:
        return None
    
    workspaceid = timedata[0]['workspace_id']
    clientdata = get_data_from_api(f'https://api.track.toggl.com/api/v9/workspaces/{workspaceid}/clients', headers)
    projectdata = get_data_from_api(f'https://api.track.toggl.com/api/v9/workspaces/{workspaceid}/projects', headers)
    
    if not clientdata or not projectdata:
        return None
    
    clients_dict = {client['id']: client['name'] for client in clientdata}
    projects_dict = {project['id']: (project['name'], project['client_id']) for project in projectdata}

    formatted_data = []
    
    for time in timedata:
        dt = datetime.strptime(time['start'], '%Y-%m-%dT%H:%M:%S%z')
        formatted_date = dt.strftime('%Y-%m-%d')
        
        description_without_task = pattern.sub("", time['description']).strip()
        task_match = pattern.search(time['description'])
        task = task_match.group(1) if task_match else ' '

        project_name, client_id = projects_dict.get(time['project_id'], ("Unknown Project", None))
        client_name = clients_dict.get(client_id, "Unknown Client")
        
        first_tag = time['tags'][0] if time['tags'] else 'Programmering'

        formatted_string = f"{formatted_date},Normal,{round_to_half_hour(time['duration'])},{client_name},{project_name},{first_tag},{task},{description_without_task}"
        formatted_data.append(formatted_string)

    return '\n'.join(formatted_data)

def ColumnFixedSize(layout, size=(None, None), *args, **kwargs):
    return sg.Column([[sg.Column([[sg.Sizer(0,size[1]-1), sg.Column([[sg.Sizer(size[0]-2,0)]] + layout, *args, **kwargs, pad=(0,0))]], *args, **kwargs)]],pad=(0,0))

credentials_file = 'credentials.dat'
if os.path.exists(credentials_file):
    with open(credentials_file, 'rb') as f:
        account_data = pickle.load(f)
    email = account_data.get('email', '')
    password = account_data.get('password', '')
else:
    email = ''
    password = ''

sg.theme("DarkGrey13")

buttons = [
    [sg.Button('Get Data'), sg.Button('Cancel')]
]

layout = [  
    [
        sg.Image(data=ICON, pad=(0,0), expand_x=True)
    ],
    [
        sg.Text('TIDIGTOGGLE', font='_ 13 bold', size=(40,2), justification='c', expand_x=True)
    ],
    [
        sg.Text('Email', expand_x=True), 
        sg.InputText(default_text=email)
    ],
    [
        sg.Text('Password', expand_x=True), 
        sg.InputText(default_text=password,password_char='*')
    ],
    [
        sg.Text('Date From', expand_x=True), 
        sg.InputText(key='date_from', readonly=True, size=(20,1), disabled_readonly_text_color="#000"),  # This field will hold the date from the calendar
        sg.CalendarButton('Select Date', no_titlebar=False, title="Select Date", close_when_date_chosen=True, target='date_from', format='%Y-%m-%d')
    ],
    [
        sg.Text('Date To', expand_x=True), 
        sg.InputText(key='date_to', readonly=True, size=(20,1), disabled_readonly_text_color="#000"),  # This field will hold the date to from the calendar
        sg.CalendarButton('Select Date', no_titlebar=False, title="Select Date", close_when_date_chosen=True, target='date_to', format='%Y-%m-%d')
    ],
    [
        ColumnFixedSize(buttons, size=(500, 70), element_justification='c')
    ],
    [
        sg.Text('Created by: @officialaudite', font='_ 10', size=(40,1), justification='c', expand_x=True)
    ]
]

window = sg.Window('TIDIGTOGGLE', layout=layout, font="Helvetica 12", icon=ICON)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    if event == 'Get Data':        
        email, password = values[0], values[1]
        datefrom, dateto = values['date_from'], values['date_to']
        
        if not email or not password:
            sg.popup_error('You need to specify both an email and password.', title='Login Error')
            continue
        
        with open(credentials_file, 'wb') as f:
            pickle.dump({'email': email, 'password': password}, f)
        
        if not datefrom or not dateto:
            sg.popup_error('You need to specify both a start and end date.', title='Date Error')
            continue
        
        date_format = "%Y-%m-%d"
        dateto_datetime = datetime.strptime(dateto, date_format)
        dateto_datetime += timedelta(days=1)
        dateto = dateto_datetime.strftime(date_format)
        
        try:
            data = construct_data(email, password, datefrom, dateto)
            
            if data:
                save_to_csv(data)
                sg.popup_scrolled(data, title='Retrieved Data')
            else:
                sg.popup_error('No data to display.')
        except ValueError:
            sg.popup_error('Invalid date format. Please use YYYY-MM-DD format.', title='Date Format Error')
        except Exception as e:
            sg.popup_error(f'An error occurred: {e}', title='Error')

window.close()