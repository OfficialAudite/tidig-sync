# TIDIGTOGGLE Sync Tool

This tool is designed to export time tracking data from Toggl and format it for import into TIDIG, a time tracking and management tool used by Consid.

## Features

- Retrieve time entries from Toggl API
- Process data to match TIDIG import format
- Generate a CSV file ready for TIDIG import

## Installation

Before running this script, ensure you have Python installed on your system.
This script was written in Python 3.12, and compatibility with previous versions is not guaranteed.

### Set up the environment

1. Clone the repository (or download the ZIP):

    ```bash
    git clone https://github.com/OfficialAudite/tidig-sync.git
    cd tidig-sync
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the main script:

    ```bash
    python main.py
    ```

This command will start the script. Follow the on-screen prompts in the application to enter your Toggl credentials and retrieve the time tracking data.

After setting up the environment and running the script, follow any additional usage instructions provided within the application itself.