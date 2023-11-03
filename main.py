import requests, re, os
from base64 import b64encode
import PySimpleGUI as sg
from datetime import datetime, timedelta
import pickle

pattern = re.compile(r'\((.*?)\)')

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
        sg.Text('Toggl export for import into tidig @ consid!', font='_ 13 bold', size=(40,2), justification='c', expand_x=True)
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
    ]
]

window = sg.Window('TIDIGTOGGLE', layout=layout, font="Helvetica 12")

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