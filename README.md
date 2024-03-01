# Autodork
A GUI for crafting specific Google Dorking queries that will be automatically searched for in your browser and save the results found. Aswell as evaluting the usefulness of the discovered domain or filetype.

Select 1 site domain as of now. I'm working on fixing it up but this is the main premise of the script.
## To run
`python autodork.py`


## Browser
Change the filepath to your browser of choice, I've defaulted it to Firefox at the moment. Which can be found at 
```
# Function to perform a Google search with the generated dork query
def search_google_with_dork(query):
    ...

    # Specify the full path to the Firefox executable
    firefox_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe" # <-------------------- Here

    # Open Firefox and perform the search
    webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path)) # <------- If you wish to change the browser name (opt)
    webbrowser.get('firefox').open(search_url)
 ```


## To Add
- Clear Button (Clearing all parameters for a tab that have been selected)
- Pulling external info off of sites such as exploit-db.com
- Smoother, more appealing looking GUI
- Figure out on Tab 1 What to include
