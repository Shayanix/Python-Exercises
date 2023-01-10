import csv
import requests
from http import HTTPStatus
from fake_useragent import UserAgent


def get_websites(csv_path):
    websites = []
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            url = row[1].strip()
            if not url.startswith(('http://', 'https://')):
                url = f'https://{url}'
            websites.append(url)
    return websites

def get_user_agent():
    ua = UserAgent()
    return ua.chrome

def get_status_code(status_code):
    for value in HTTPStatus:
        if value == status_code:
            description = f'({value} {value.name}) {value.description}'
            return description
            
    return 'unknown'

def check_website(website,user_agent):
    
    try:
        code = requests.get(website,headers={'User-Agent':user_agent}).status_code
        print(f'{website} - {get_status_code(code)}')
        
    except Exception as e:
        print (f'{website} - {e}')

def main():
    sites = get_websites('website.csv')
    user_agent = get_user_agent()
    
    for site in sites:
        check_website(site,user_agent)
        
if __name__ == '__main__':
    main()