import datetime
import os
import time

# Example blacklist and whitelist
blacklist = ['example.com', 'sensitive-site.org']
whitelist = ['trusted-site.com', 'useful-site.net']

# Function to check if a domain is in the blacklist
def is_blacklisted(domain):
    return domain in blacklist

# Function to check if a domain is in the whitelist
def is_whitelisted(domain):
    return domain in whitelist

# Function to calculate domain reputation (example)
def calculate_reputation(domain):
    # Simulated reputation calculation
    return len(domain) * 2

# Function to calculate domain age (example)
def calculate_age(domain):
    # Simulated age calculation (in years)
    return (datetime.datetime.now() - datetime.datetime(2000, 1, 1)).days / 365

# Function to evaluate a domain and assign a rating out of 100
def evaluate_domain(domain):
    rating = 0
    
    # Check if domain is blacklisted
    if is_blacklisted(domain):
        rating = 0  # Domain is sensitive
    # Check if domain is whitelisted
    elif is_whitelisted(domain):
        rating = 100  # Domain is useful
    else:
        # Additional metrics for evaluation (you can add more as needed)
        metrics = {
            '.gov': 30,
            '.mil': 30,
            '.edu': 20,
            '.org': 10,
            '.com': 5,
            '.net': 5
        }
        
        # Check domain TLD for sensitivity
        for tld, weight in metrics.items():
            if domain.endswith(tld):
                rating += weight
        
        # Simulated reputation calculation
        reputation = calculate_reputation(domain)
        # Simulated age calculation (in years)
        age = calculate_age(domain)
        
        # Calculate rating based on reputation, age, and sensitivity
        rating += min(reputation / 2 + age * 5, 100)
    
    return rating

# Functio to wait for the file to be created
def wait_for_file(filenames, timeout=60):
    start_time = time.time()
    while True:
        for filename in filenames:
            if os.path.exists(filename):
                return True
        if time.time() - start_time > timeout:
            print(f"Timeout reached. Files {filenames} not found.")
            return False
        time.sleep(1) # Wait for 1 second before checking again 
    
# Function to filter domains based on criteria
def filter_domains(domains):
    # Remove duplicates
    return list(set(domains))

# Define the output folder
output_folder = r'C:\Users\jamie\Downloads'  # Specify the full path to your desired folder

# Wait for the file to be created
if wait_for_file(os.path.join(output_folder, 'collected-domains.txt')):
    # Proceed with domain evaluation
    with open(os.path.join(output_folder, 'collected-domains.txt'), 'r') as file:
        extracted_domains = [line.strip() for line in file]

    # Filter domains based on criteria
    filtered_domains = filter_domains(extracted_domains)

        # Evaluate each domain and print the result
    evaluated_domains = {}
    for domain in extracted_domains:
        rating = evaluate_domain(domain)
        evaluated_domains[domain] = rating
        
# Function to write evaluated domains to a file
def write_to_file(domains, filename):
    with open(filename,"w") as f:
        for domain, rating in domains.items():
            f.write(f"Domain: {domain}, Rating: {rating: .2f}/100\n")

# Write evaluated domains to a file
    write_to_file(evaluated_domains, "evaluated_domains.txt")
