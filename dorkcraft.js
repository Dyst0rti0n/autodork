import tkinter as tk
from tkinter import ttk
import webbrowser
import random

def generate_random_dork(parameters):
    dork_query = ''
    selected_site_domains = [domain.cget("text") for domain, var in zip(domain_checkboxes, domain_vars) if var.get()]
    if selected_site_domains:
        dork_query += 'site:' + '+'.join(selected_site_domains) + ' '

    selected_filetypes = [file_type.cget("text") for file_type, var in zip(filetype_checkboxes, file_vars) if var.get()]
    if selected_filetypes:
        dork_query += 'filetype:' + random.choice(selected_filetypes) + ' '

    for parameter in parameters:
        if parameter.startswith('intext:') or parameter.startswith('intitle:'):
            selected_options = [option for var, option in advanced_vars if var.get()]
            if selected_options:
                dork_query += random.choice(selected_options) + ' '

    return dork_query.strip()

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
    selected_filetypes = [file_type.cget("text") for file_type, var in zip(filetype_checkboxes, file_vars) if var.get()]
    if selected_filetypes:
        selected_parameters.append('filetype:')
        selected_parameters.append(random.choice(selected_filetypes))
    selected_domains = [domain.cget("text") for domain, var in zip(domain_checkboxes, domain_vars) if var.get()]
    if selected_domains:
        selected_parameters.extend(['site:' + domain for domain in selected_domains])
    for var, option in advanced_vars:
        if var.get():
            selected_parameters.append(option)  # Append selected option string
    
    random_dork = generate_random_dork(selected_parameters)
    search_google_with_dork(random_dork)
    print("Google Dork Query:", random_dork)

# Create GUI
app = tk.Tk()
app.title("Google Dorking Crafter")

# Get the screen width
screen_width = app.winfo_screenwidth()

# Set window width based on screen resolution
app.geometry("500x400")

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
filetypes_var = tk.BooleanVar()
filetypes_label = tk.Label(filetypes_frame, text="Filetypes", font=("Helvetica", 14, "bold"))
filetypes_label.pack(pady=5)

# Create checkboxes for different filetypes
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

file_vars = []
filetype_checkboxes = []

# Check if checkboxes can be arranged side by side
if len(file_types) <= 5:
    for category, types in file_types.items():
        category_frame = tk.Frame(filetypes_frame)
        category_frame.pack(side="left", padx=10, pady=5, fill="y")
        category_label = tk.Label(category_frame, text=category, font=("Helvetica", 12, "bold"))
        category_label.pack(anchor="w")
        for file_type in types:
            var = tk.BooleanVar(value=False)  # Initially unticked
            checkbox = tk.Checkbutton(category_frame, text=file_type, variable=var)
            checkbox.pack(anchor="w")
            file_vars.append(var)
            filetype_checkboxes.append(checkbox)
else:
    filetypes_canvas = tk.Canvas(filetypes_frame)
    filetypes_canvas.pack(side="left", fill="both", expand=True)

    filetypes_inner_frame = tk.Frame(filetypes_canvas)
    filetypes_inner_frame.pack(fill="both", expand=True)

    filetypes_scroll = ttk.Scrollbar(filetypes_frame, orient="vertical", command=filetypes_canvas.yview)
    filetypes_scroll.pack(side="right", fill="y")

    filetypes_canvas.configure(yscrollcommand=filetypes_scroll.set)

    filetypes_canvas.create_window((0, 0), window=filetypes_inner_frame, anchor="nw")

    filetypes_inner_frame.bind("<Configure>", lambda e: filetypes_canvas.configure(scrollregion=filetypes_canvas.bbox("all")))

    for category, types in file_types.items():
        category_label = tk.Label(filetypes_inner_frame, text=category, font=("Helvetica", 12, "bold"))
        category_label.pack(anchor="w")
        for file_type in types:
            var = tk.BooleanVar(value=False)  # Initially unticked
            checkbox = tk.Checkbutton(filetypes_inner_frame, text=file_type, variable=var)
            checkbox.pack(anchor="w")
            file_vars.append(var)
            filetype_checkboxes.append(checkbox)

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

app.mainloop()
