# update_script.py
import requests
import os
import subprocess
import time

def update_application():
    try:
        # Fetch latest release information from GitHub API
        api_url = 'https://api.github.com/repos/Dyst0rti0n/autodork/releases/latest'
        response = requests.get(api_url)
        release_info = response.json()

        # Check if 'assets' key exists in the release info
        if 'assets' in release_info and release_info['assets']:
            # Extract download URL for the script file
            download_url = release_info['assets'][0]['browser_download_url']

            # Download the latest script file
            script_response = requests.get(download_url)

            # Generate a timestamp string
            timestamp = str(int(time.time()))  # Using Unix timestamp
            
            # Create the filename with the timestamp appended
            new_script_filename = f'autodork_{timestamp}.py'

            # Save the updated script with the timestamp-appended filename
            with open(new_script_filename, 'wb') as file:
                file.write(script_response.content)

            # Execute the updated script
            subprocess.Popen(['python', new_script_filename])

            # No need to delete the old script immediately

        else:
            print("No assets found for the latest release.")
    except Exception as e:
        print(f"Failed to update application: {str(e)}")

if __name__ == "__main__":
    update_application()
