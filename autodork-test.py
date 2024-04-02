import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import random
import requests
import os
import sys
import subprocess
import datetime
from bs4 import BeautifulSoup
from evaluator import evaluate_domain
import urllib.parse

# Global Variables

current_tab_index = 0 
filetype_radio_buttons = []
recent_queries = []
extracted_domains = ['example.com''example.com', 'trusted-site.com', 'random-site.net']
history_file = "history.txt" # File to store history

def load_history():
    if os.path.exists(history_file):
        with open (history_file, "r") as f:
            return [line.strip() for line in f.readlines()]
    else:
        return []
    
def save_history():
    with open(history_file, "w") as f:
        f.write("\n".join(recent_queries))
        
def remove_query(idx):
    if 0 <= idx < len(recent_queries):
        del recent_queries[idx]
        update_history_tab()
        save_history()
        
def add_to_history(query):
    recent_queries.append(query)
    update_history_tab()
    save_history()

def clear_filetype_selection():
    for var in filetype_radio_buttons:
        var.set("")

def clear_site_domain_selection():
    for var in domain_vars:
        var.set(False)
        
def clear_advanced_selection():
    for var, _ in advanced_vars:
        var.set(False)

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

# Function to display recent queries in the history rtab
def display_recent_queries():
    for query in recent_queries:
        query_label = tk.Label(history_frame, text=query, font=("Helvetica", 12))
        query_label.pack(anchor="w")

def extracted_domains_from_query(query):
    base_url = 'https://www.google.com/search?q='
    search_url = base_url + '+'.join(query.split())

    print("Search URL:", search_url) 

    response = requests.get(search_url)
    print("Response Status Code:", response.status_code)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        extracted_domains = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'url?q=' in href:
                # Extract the URL from the href attribute
                encoded_url = href.split('url?q=')[1].split('&')[0]
                # Decode te URL using urllib.parse.unquote
                url = urllib.parse.unquote(encoded_url)
                print("Extracted url:", url )
                # Append the domain to the extracted_domains list 
                extracted_domains.append(url)
                
        # Specify the full path to the Firefox executable
        firefox_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

        # Open Firefox and perform the search
        webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))
        webbrowser.get('firefox').open(search_url)
        
        return extracted_domains
    else:
        print("Failed to perform Google search. Please check your internet connection.")
        return []

def run_search():
    selected_parameters = []
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
    
    # Generate random dork and extract domains
    random_dork = generate_random_dork(selected_parameters)
    extracted_domains = extracted_domains_from_query(random_dork)
    add_to_history(random_dork)
    print("Google Dork Query:", random_dork)
    
    if extracted_domains:
        # Evaluate extracted domains
        for domain in extracted_domains:
            evaluate_result = evaluate_domain(domain)
            if evaluate_result == "good":
                print(f"Domain {domain} is considered good")

        # Check if the number of extracted domains is less than 100
        if len(extracted_domains) < 250:
            # If there are less than 100 domains, proceed to evaluate them
            for domain in extracted_domains:
                # Optionally, you can evaluate each domain here
                rating = evaluate_domain(domain)
                print(f"Domain: {domain}, Rating: {rating:.2f}/100")
                
                # Write domain and its rating to a file
                with open("collected-domains.txt", "a") as f:
                    f.write(f"Domain: {domain}, Rating: {rating:.2f}/100\n")
        else:
            print("More than 100 domains found. Unable to evaluate all.")
    else:
        print("No domains extracted from the query.")


# Function to update the application
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
            with open('autodork.py', 'wb') as file:
                file.write(script_response.content)
            
            # Execute the updated script
            subprocess.Popen(['python', 'autodork.py'])

        else:
            messagebox.showinfo("No Assets", "No assets found for the latest release.")
    except Exception as e:
        messagebox.showerror("Update Error", f"Failed to update application: {str(e)}")

def clear_current_tab_selection():
    global current_tab_index
    if current_tab_index == 1: # Filetypes Tab
        clear_filetype_selection()
    elif current_tab_index == 2: # Site Domains Tab
        clear_site_domain_selection()
    elif current_tab_index == 3: # Advanced Dorking Tab
        clear_advanced_selection()

# Create GUI
app = tk.Tk()
app.title("Google Dorking Crafter")

# Get the Directoy of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the image
image_path = os.path.join(script_dir, 'dystortion.png')
# Load the image
creator_image = tk.PhotoImage(file=image_path)

# Get the screen width
screen_width = app.winfo_screenwidth()

# Set window width based on screen resolution
app.geometry("800x600")

# Option tabs for different categories
notebook = ttk.Notebook(app)

# Servers tab
servers_frame = tk.Frame(notebook)
servers_frame.pack(fill="both", expand=True)

# About Me - The Creator section
creator_info_label = tk.Label(servers_frame, text="About Me - The Creator\nDystortion is a Google Dorking nerd, so this tool was creted to make it much more accessible to anyone.", font=("Helvetica", 12))
creator_info_label.pack(pady=10)

# Create a label to display the image
creator_image_label = tk.Label(servers_frame, image=creator_image)
creator_image_label.pack(pady=10)

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
    category_label = tk.Label(filetypes_inner_frame, text=category, font=("Helvetica", 12, "bold"), anchor="w")
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
    "CC Domains": ['.us', '.uk', '.de', '.fr', '.jp', '.cn', '.ru', '.au'],
    "Edu Domains": ['.edu', '.ac', '.sch'],
    "Gov Domains": ['.gov', '.mil'],
}

domain_vars = []
domain_checkboxes = []

for category, domains in domain_categories.items():
    category_frame = tk.Frame(site_domains_frame)
    category_frame.pack(side="left", padx=10, pady=5, fill="y")
    category_label = tk.Label(category_frame, text=category, font=("Helvetica", 12, "bold"), anchor="w")
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

advanced_canvas = tk.Canvas(advanced_frame)
advanced_canvas.pack(side="left", fill="both", expand=True)

advanced_inner_frame = ttk.Frame(advanced_canvas)
advanced_canvas.create_window((0, 0), window=advanced_inner_frame, anchor="nw")

advanced_scroll = ttk.Scrollbar(advanced_frame, orient="vertical", command=advanced_canvas.yview)
advanced_scroll.pack(side="right", fill="y")
advanced_canvas.configure(yscrollcommand=advanced_scroll.set)

advanced_vars = []

advanced_categories = [
    ("Security Related", [
        "filetype:pdf password",
        "intitle:index.of password.txt",
        "intext:”username” filetype:xls",
        "intext:”email” filetype:pdf",
        "inurl:admin login",
        "intitle:”Login page” “Username” “Password”",
        "inurl:login intext:”password”",
        "inurl:.php?id=",
        "intitle:”SQL query failed” intext:”mysql”",
        "site:.edu filetype:pdf",
        "intext:”Private Key” filetype:pem",
        "intitle:”Index of /” +passwd",
        "intitle:”Index of /” +secret",
        "intext:”Confidential” filetype:ppt",
        "intext:”Database Error” intitle:”Warning”",
        "intext:”PHP Script” “Debug”",
        "intext:”to=python” filetype:py",
        "intext:”API Key” filetype:yml",
        "intext:”API Key” filetype:env",
        "intext:”Private Key” filetype:key",
        "intext:”System Information” filetype:log",
        "intitle:”Index of /” +backup",
    ]),
    ("Vulnerable Webcams", [
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
    ("Database Instances", [
        'intext:"kibana" intitle:"Kibana"',
        'intext:"MongoDB Server Information" intitle:"MongoDB" -intext:"MongoDB Server Version"'
    ]),
    ("Devices and Systems", [
        'intext:"FortiGate Console" intitle:"Dashboard"',
        'intitle:"OpenEMR Login" inurl:"/interface"',
        'intitle:"Jenkins Script Console" intext:"Run groovy script"'
    ]),
    ("PhP Websites Subject to SQLi", [
        'inurl:index.php?id=',
        'intitle:"site administration:please log in"',
        'intitle:"curriculum vitae" filetype:doc'
    ]),
    ("Sensitive Wordpress Uploads", [
        '_intitle:”index of/” “cfdb7_uploads”_',
        'intext:"user" filetype:php intext:"account" inurl:/admin'
    ]),
    ("API Keys", [
        "extension:json api.forecast.io try variations, find api keys/secrets",
        "extension:json mongolab.com mongolab credentials in json configs",
        "extension:yaml mongolab.com mongolab credentials in yaml configs (try with yml)",
        "jsforce extension:js conn.login possible salesforce credentials in nodejs projects",
        "SF_USERNAME salesforce possible salesforce credentials",
        "HEROKU_API_KEY language:shell Heroku api keys",
        "HEROKU_API_KEY language:json Heroku api keys in json files",
        "shodan_api_key language:python Shodan API keys (try other languages too)",
        "HOMEBREW_GITHUB_API_TOKEN language:shell Github token usually set by homebrew users"
    ]),
    ("GitHub Tokens", [
        "PT_TOKEN language:bash pivotaltracker tokens",
        "filename:hub oauth_token hub config that stores github tokens",
        "JEKYLL_GITHUB_TOKEN Github tokens used for jekyll"
    ]),
    ("Cloud Related", [
        "filename:.npmrc _auth npm registry authentication data",
        "filename:.dockercfg auth docker registry authentication data",
        "filename:config.json auths docker registry authentication data",
        "filename:idea14.key IntelliJ Idea 14 key, try variations for other versions",
        "filename:.tugboat NOT _tugboat Digital Ocean tugboat config",
        "filename:robomongo.json mongodb credentials file used by robomongo",
        "filename:filezilla.xml Pass filezilla config file with possible user/pass to ftp",
        "filename:recentservers.xml Pass filezilla config file with possible user/pass to ftp",
        "filename:express.conf path:.openshift openshift config, only email and server thou",
        "filename:configuration.php JConfig password Joomla configuration file",
        "filename:config.php dbpasswd PHP application database password (e.g., phpBB forum software)",
        "filename:.pgpass PostgreSQL file which can contain passwords",
        "filename:proftpdpasswd Usernames and passwords of proftpd created by cpanel",
        "filename:ventrilo_srv.ini Ventrilo configuration",
        "[WFClient] Password= extension:ica WinFrame-Client infos needed by users to connect toCitrix Application Servers",
        "filename:server.cfg rcon password Counter Strike RCON Passwords",
        "filename:dhcpd.conf DHCP service config",
        "filename:.s3cfg might return false negatives with dummy values",
        "filename:wp-config.php wordpress config files",
        "filename:.htpasswd htpasswd files",
        "filename:.env DB_USERNAME NOT homestead laravel .env (CI, various ruby based frameworks too)",
        "filename:.env MAIL_HOST=smtp.gmail.com gmail smtp configuration (try different smtp services too)",
        "filename:.git-credentials git credentials store, add NOT username for more valid results",
        "filename:.bashrc password search for passwords, etc. in .bashrc (try with .bash_profile too)",
        "filename:.bashrc mailchimp variation of above (try more variations)",
        "filename:.bash_profile aws aws access and secret keys",
        "rds.amazonaws.com password Amazon RDS possible credentials",
        "extension:json googleusercontent client_secret OAuth credentials for accessing Google APIs",
        "filename:connections.xml possible db connections configuration, try variations to be specific"
    ]),
    ("Miscellaneous", [
        "intitle:\"Apache2 Debian Default Page\"",
        "intitle:\"Welcome to nginx!\"",
        "intitle:\"Welcome to IIS\"",
        "intitle:\"Login\" or intitle:\"Log In\"",
        "intitle:\"Index of /\" or intitle:\"Browse Directory\"",
        "intitle:\"config.json\"",
        "intitle:\"index of\" inurl:.git",
        "intitle:\"Apache Tomcat\" intitle:\"Administration\"",
        "intitle:\"Dashboard [Jenkins]\"",
        "intitle:\"Index of /svn\"",
        "intitle:\"phpMyAdmin\" or intext:\"phpMyAdmin MySQL-Dump\"",
        "intitle:\"Microsoft SharePoint\" intext:\"Sign in to SharePoint\"",
        "intitle:\"Redis\" intext:\"Server Information\"",
        "intitle:\"Elasticsearch Head\"",
        "intitle:\"MongoDB Server Information\"",
        "intitle:\"CouchDB - Welcome\"",
        "intitle:\"Memcached Server Information\"",
        "intitle:\"remote desktop inurl:rdweb\"",
        "intitle:\"VNC viewer for Java\"",
        "intitle:\"welcome to\" intext:\"telnet\"",
        "intitle:\"welcome to\" intext:\"snmp\"",
        "intitle:\"Index of /smb.conf\"",
        "intitle:\"Index of /ftp\"",
        "intitle:\"Index of /exports\"",
        "intext:\"printer meter\"",
        "intitle:\"Asterisk Management Portal\"",
        "intitle:\"Live View / - AXIS\"",
        "intitle:\"webcamXP 5\" inurl:8080",
        "intitle:\"Linksys Viewer - Login\" -inurl:mainFrame",
        "intitle:\"D-Link\" inurl:\"/video.htm\"",
        "intitle:\"Panasonic Network Camera\"",
        "intitle:\"Foscam\" intext:\"user login\"",
        "intext:\"SMART TV\" inurl:password.txt",
        "intitle:\"Netgear\" intext:\"NETGEAR\"",
        "intext:\"Ubiquiti\" intitle:\"AirOS\"",
        "intext:\"MikroTik RouterOS\" inurl:winbox",
        "intitle:\"Siemens SIMATIC\" intext:\"Web Server\" -inurl:/portal",
        "intext:\"Schneider Electric\" intitle:\"PowerLogic Web-",
        "intitle:\"Johnson Controls - WorkPlace\" intext:\"User name :\""
    ])
]

def toggle_options(event, category, frame):
    # Clear previously displayed options
    for widget in frame.winfo_children():
        widget.destroy()
    # Display options for the clicked heading
    for cat, options in advanced_categories:
        if cat == category:
            for option in options:
                var = tk.BooleanVar(value=False)
                checkbox = tk.Checkbutton(frame, text=option, variable=var, anchor="w")
                checkbox.pack(anchor="w")
                advanced_vars.append((var, option))
            break

def create_category_labels():
    for category, _ in advanced_categories:
        category_label = tk.Button(advanced_inner_frame, text=category, font=("Helvetica", 14, "bold"), cursor="hand2", anchor="w", command=lambda cat=category, frame=advanced_inner_frame: toggle_options(None, cat, frame))
        category_label.pack(pady=5, anchor="w")

def back_to_categories():
    for widget in advanced_inner_frame.winfo_children():
        widget.destroy()
    create_category_labels()

# Back button for the Advanced Dorking tab
back_button = tk.Button(advanced_frame, text="Back to Headings", command=back_to_categories, font=("Helvetica", 12))
back_button.pack(pady=10)

create_category_labels()

# Configure scrollbar to update based on the actual size of the inner frame
def update_scrollregion(event):
    advanced_canvas.configure(scrollregion=advanced_canvas.bbox("all"))

advanced_canvas.bind("<Configure>", update_scrollregion)
advanced_scroll.config(command=advanced_canvas.yview)

# History Tab
history_frame = tk.Frame(notebook)
history_frame.pack(fill="both", expand=True)

history_text = tk.Text(history_frame, wrap="word", font=("Helvetica", 12))
history_text.pack(fill="both", expand=True)

def update_history_tab():
    history_text.delete("1.0", tk.END) # Clear previous Content
    for idx, query in enumerate(recent_queries, start=1):
        history_text.insert(tk.END, f"{idx}. {query}\n")
        remove_button = tk.Button(history_text, text="X", command=lambda idx=idx-1: remove_query(idx))
        history_text.window_create(tk.END, window=remove_button)
        history_text.insert(tk.END, "\n")
        
# Load History
recent_queries = load_history()
update_history_tab()

# Create a custom style for the buttons
style = ttk.Style()
style.configure("Custom.TButton",
                foreground="black",  # Text color
                background="#90ee90",  # Button color
                font=("Helvetica", 16, "bold"),
                padding=10,  # Padding around text
                borderwidth=5,  # No border
                width=20,  # Button width
                focuscolor="#4CAF50",  # Color when button is focused
                highlightthickness=10  # No highlight
                )

# Run search button
search_button = ttk.Button(app, text="Run Search", command=run_search, style="Custom.TButton")
search_button.place(relx=0.35, rely=0.95, anchor="sw", width=150, height=50)

update_button = ttk.Button(app, text="Update", command=update_application, style="Custom.TButton")
update_button.place(relx=0.65, rely=0.95, anchor="s", width=150, height=50)

clear_button = ttk.Button(app, text="Clear", command=clear_current_tab_selection, style="Custom.TButton")
clear_button.place(relx=0.95, rely=0.95, anchor="se", width=150, height=50)


# Clear button for history tab
clear_history_button = tk.Button(history_frame, text="Clear History", command=lambda: recent_queries.clear())
clear_history_button.pack(side="bottom", pady=20)

def on_tab_changed(event):
    global current_tab_index
    current_tab_index = notebook.index(notebook.select())

# Update history tab when it is selected
notebook.bind("<<NotebookTabChanged>>", lambda event: update_history_tab())
notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

# Add tabs to the notebook
notebook.add(servers_frame, text="Home")
notebook.add(filetypes_frame, text="Filetypes")
notebook.add(site_domains_frame, text="Site Domains")
notebook.add(advanced_frame, text="Advanced Dorking")
notebook.add(history_frame, text="History")
notebook.pack(fill="both", expand=True)

app.mainloop()
