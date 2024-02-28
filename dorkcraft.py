import tkinter as tk
from tkinter import ttk, messagebox 
import webbrowser
import random
import requests
import os

filetype_radio_buttons = []  # List to hold the Radiobutton variables for filetypes

def generate_random_dork(parameters):
    dork_query = ''
    selected_site_domains = [domain.cget("text") for domain, var in zip(domain_checkboxes, domain_vars) if var.get()]
    if selected_site_domains:
        dork_query += 'site:' + '+'.join(selected_site_domains) + ' '

    selected_filetype = get_selected_filetype()
    if selected_filetype:
        dork_query += 'filetype:' + selected_filetype + ' '

    for parameter in parameters:
        if parameter.startswith('intext:') or parameter.startswith('intitle:'):
            selected_options = [option for var, option in advanced_vars if var.get()]
            if selected_options:
                dork_query += random.choice(selected_options) + ' '

    return dork_query.strip()

def get_selected_filetype():
    for var in filetype_radio_buttons:
        if var.get():
            return var.get()
    return None

# Function to perform a Google search with the generated dork query
def search_google_with_dork(query):
    base_url = 'https://www.google.com/search?q='
    search_url = base_url + '+'.join(query.split())

    # Specify the full path to the Firefox executable
    firefox_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

    # Open Firefox and perform the search
    webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))
    webbrowser.get('firefox').open(search_url)

def run_search():
    selected_parameters = []
    if servers_var.get():
        selected_parameters.append('site:')
    selected_filetype = get_selected_filetype()
    if selected_filetype:
        selected_parameters.append('filetype:')
        selected_parameters.append(selected_filetype)
    selected_domains = [domain.cget("text") for domain, var in zip(domain_checkboxes, domain_vars) if var.get()]
    if selected_domains:
        selected_parameters.extend(['site:' + domain for domain in selected_domains])
    for var, option in advanced_vars:
        if var.get():
            selected_parameters.append(option)  # Append selected option string
    
    random_dork = generate_random_dork(selected_parameters)
    search_google_with_dork(random_dork)
    print("Google Dork Query:", random_dork)

# Function to update the application
def update_application():
    try:
        # Fetch latest release information from GitHub API
        api_url = 'https://api.github.com/repos/Dys0rti0n/autodork/releases/latest'
        response = requests.get(api_url)
        release_info = response.json()

        # Check if 'assets' key exists in the release info
        if 'assets' in release_info and release_info['assets']:
            # Extract download URL for the script file
            download_url = release_info['assets'][0]['browser_download_url']

            # Download the latest script file
            script_response = requests.get(download_url)
            with open('updated_script.py', 'wb') as file:
                file.write(script_response.content)

            # Replace existing script file with the updated one
            os.replace('updated_script.py', 'your_script.py')

            # Optional: Restart the application
            # app.quit()
            # os.execv(sys.executable, ['python'] + sys.argv)
            # or provide a message to restart manually
            
            messagebox.showinfo("Update", "Application updated successfully. Please restart the application.")
        else:
            messagebox.showinfo("No Assets", "No assets found for the latest release.")
    except Exception as e:
        messagebox.showerror("Update Error", f"Failed to update application: {str(e)}")


# Create GUI
app = tk.Tk()
app.title("Google Dorking Crafter")

# Get the screen width
screen_width = app.winfo_screenwidth()

# Set window width based on screen resolution
app.geometry("1000x500")

# Option tabs for different categories
notebook = ttk.Notebook(app)

# Servers tab
servers_frame = tk.Frame(notebook)
servers_frame.pack(fill="both", expand=True)
servers_var = tk.BooleanVar()
servers_checkbox = tk.Checkbutton(servers_frame, text="Servers", variable=servers_var)
servers_checkbox.pack(pady=5)


# Filetypes tab
filetypes_frame = tk.Frame(notebook)
filetypes_frame.pack(fill="both", expand=True)
filetypes_var = tk.StringVar()  # Variable to hold the selected filetype

filetypes_label = tk.Label(filetypes_frame, text="Filetypes", font=("Helvetica", 14, "bold"))
filetypes_label.pack(pady=5)

file_types = {
    "Text Documents": ['txt', 'docx', 'doc', 'pdf', 'rtf', 'odt'],
    "Images": ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tif', 'tiff', 'svg'],
    "Audio": ['mp3', 'wav', 'aac', 'flac', 'ogg', 'm4a'],
    "Video": ['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv'],
    "Spreadsheets and Databases": ['xlsx', 'xls', 'csv', 'db', 'sqlite', 'mdb'],
    "Presentations": ['pptx', 'ppt', 'key', 'odp'],
    "Archives and Compression": ['zip', 'rar', 'tar.gz', '7z'],
    "Programming and Script Files": ['cpp', 'c', 'h', 'java', 'py', 'html', 'css', 'js'],
    "Miscellaneous": ['exe', 'app', 'apk', 'iso', 'torrent', 'xml']
}

# Create a canvas for the filetypes frame
filetypes_canvas = tk.Canvas(filetypes_frame)
filetypes_canvas.pack(side="left", fill="both", expand=True)

# Create a frame to contain the filetypes widgets
filetypes_inner_frame = tk.Frame(filetypes_canvas)
filetypes_inner_frame.pack(fill="both", expand=True)

# Add the frame to the canvas
filetypes_canvas.create_window((0, 0), window=filetypes_inner_frame, anchor="nw")

# Configure scrollbar for the canvas
filetypes_scroll = ttk.Scrollbar(filetypes_frame, orient="vertical", command=filetypes_canvas.yview)
filetypes_scroll.pack(side="right", fill="y")
filetypes_canvas.configure(yscrollcommand=filetypes_scroll.set)

# Function to get the selected filetype
def get_selected_filetype():
    return filetypes_var.get()

# Append the Radiobuttons variable to a list if needed elsewhere
filetype_radio_buttons.append(filetypes_var)

# Create Radiobuttons for different filetypes
for category, types in file_types.items():
    category_label = tk.Label(filetypes_inner_frame, text=category, font=("Helvetica", 12, "bold"))
    category_label.pack(anchor="w")
    for file_type in types:
        var = tk.StringVar(value=file_type)  # Initially set value
        radio_button = tk.Radiobutton(filetypes_inner_frame, text=file_type, variable=filetypes_var, value=file_type)
        radio_button.pack(anchor="w")
        filetype_radio_buttons.append(var)

# Update the scroll region when the size of the inner frame changes
def on_frame_configure(event):
    filetypes_canvas.configure(scrollregion=filetypes_canvas.bbox("all"))

filetypes_inner_frame.bind("<Configure>", on_frame_configure)

# Site Domains tab
site_domains_frame = tk.Frame(notebook)
site_domains_frame.pack(fill="both", expand=True)
site_domains_var = tk.BooleanVar()
site_domains_label = tk.Label(site_domains_frame, text="Site Domains", font=("Helvetica", 14, "bold"))
site_domains_label.pack(pady=5)

# Define domain categories and their respective domains
domain_categories = {
    "General Domains": ['.com', '.org', '.net', '.info', '.biz', '.io', '.domains'],
    "Country Code Domains": ['.us', '.uk', '.de', '.fr', '.jp', '.cn', '.ru', '.au'],
    "Educational Domains": ['.edu', '.ac', '.sch'],
    "Governmental Domains": ['.gov', '.mil'],
}

domain_vars = []
domain_checkboxes = []

for category, domains in domain_categories.items():
    category_frame = tk.Frame(site_domains_frame)
    category_frame.pack(side="left", padx=10, pady=5, fill="y")
    category_label = tk.Label(category_frame, text=category, font=("Helvetica", 12, "bold"))
    category_label.pack(anchor="w")
    for domain in domains:
        var = tk.BooleanVar(value=False)  # Initially unticked
        checkbox = tk.Checkbutton(category_frame, text=domain, variable=var)
        checkbox.pack(anchor="w")
        domain_vars.append(var)
        domain_checkboxes.append(checkbox)

# Advanced Dorking tab
advanced_frame = ttk.Frame(notebook)
advanced_frame.pack(fill="both", expand=True)
advanced_scroll = ttk.Scrollbar(advanced_frame, orient="vertical")
advanced_scroll.pack(side="right", fill="y")
advanced_canvas = tk.Canvas(advanced_frame, yscrollcommand=advanced_scroll.set)
advanced_canvas.pack(side="left", fill="both", expand=True)
advanced_inner_frame = ttk.Frame(advanced_canvas)
advanced_canvas.create_window((0, 0), window=advanced_inner_frame, anchor="nw")

advanced_vars = []

advanced_categories = [
    ("Webcams", [
        'allintitle:"Network Camera NetworkCamera"',
        'intitle:"EvoCam" inurl:"webcam.html"',
        'intitle:"Live View / - AXIS"',  # maybe without spaces...
        'inurl:indexFrame.shtml"Axis Video Server"',
        'inurl:axis.cgi/jpg',
        'inurl:"MultiCameraFrame?Mode=Motion"',
        'inurl:/view.shtml',
        'inurl:/view/index.shtml',
        '"mywebcamXP server!"'
    ]),
    ("Database Instances", [
        'intext:"kibana" intitle:"Kibana"',
        'intext:"MongoDB Server Information" intitle:"MongoDB" -intext:"MongoDB Server Version"'
    ]),
    ("Devices and Systems", [
        'intext:"FortiGate Console" intitle:"Dashboard"',
        'intitle:"OpenEMR Login" inurl:"/interface"',
        'intitle:"Jenkins Script Console" intext:"Run groovy script"'
    ]),
    ("PhP websites subject to SQLi", [
        'inurl:index.php?id=',
        'intitle:"site administration:please log in"',
        'intitle:"curriculum vitae" filetype:doc'
    ]),
    ("Vulnerable web cams", [
        'allintitle:"Network Camera NetworkCamera"',
        'intitle:"EvoCam" inurl:"webcam.html"',
        'intitle:"Live View / - AXIS"',
        'inurl:indexFrame.shtml"Axis Video Server"',
        'inurl:axis.cgi/jpg',
        'inurl:"MultiCameraFrame?Mode=Motion"',
        'inurl:/view.shtml',
        'inurl:/view/index.shtml',
        '"mywebcamXP server!"'
    ]),
    ("Sensitive Wordpress Uploads", [
        '_intitle:”index of/” “cfdb7_uploads”_',
        'intext:"user" filetype:php intext:"account" inurl:/admin'
    ])
]

for category, options in advanced_categories:
    category_label = ttk.Label(advanced_inner_frame, text=category, font=("Helvetica", 14, "bold"))
    category_label.pack(pady=5)
    for option in options:
        var = tk.BooleanVar(value=False)
        checkbox = tk.Checkbutton(advanced_inner_frame, text=option, variable=var)
        checkbox.pack(anchor="w")
        advanced_vars.append((var, option))

# Configure scrollbar to update based on the actual size of the inner frame
def update_scrollregion(event):
    advanced_canvas.configure(scrollregion=advanced_canvas.bbox("all"))

advanced_inner_frame.bind("<Configure>", update_scrollregion)
advanced_scroll.config(command=advanced_canvas.yview)

# Add tabs to the notebook
notebook.add(servers_frame, text="Servers")
notebook.add(filetypes_frame, text="Filetypes")
notebook.add(site_domains_frame, text="Site Domains")
notebook.add(advanced_frame, text="Advanced Dorking")
notebook.pack(fill="both", expand=True)

# Run search button
search_button = tk.Button(app, text="Run Search", command=run_search)
search_button.pack(pady=10)

# Update button
update_button = tk.Button(app, text="Update", command=update_application)
update_button.pack(pady=10)

app.mainloop()
