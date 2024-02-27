# Autodork
A GUI for crafting specific Google Dorking queries that will be automatically searched for in your browser and save the results found. Aswell as evaluting the usefulness of the discovered domain or filetype.

Only select 1 filetype, 1 site domain as of now. I'm working on fixing it up but this is the main premise of the script.

## Browser
Change the filepath to your browser of choice, I've defaulted it to Firefox at the moment. Which can be found at 
```
# Function to perform a Google search with the generated dork query
def search_google_with_dork(query):
    base_url = 'https://www.google.com/search?q='
    search_url = base_url + '+'.join(query.split())

    # Specify the full path to the Firefox executable
    firefox_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe" # <-------------------- Here

    # Open Firefox and perform the search
    webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))
    webbrowser.get('firefox').open(search_url)
 ```
