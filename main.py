import urllib.request
import json
from pprint import pprint

### Command Line Stuff
while True:
### Getting the user
    username = input("github-activity ")
    
    if username == "exit":
        break
    
    url = f"https://api.github.com/users/{username}/events"

### Checking for URL related issues
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("Error: Invalid username.")
        else:
            print(f"HTTP Error: {e.code} - {e.reason}")
        continue
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        continue
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        continue

### If URL stuff doesn't happen
    data = json.loads(response.read().decode("utf-8"))

    pprint(data)

    with open(f"{username}'s events", "w") as file:
        json.dump(data, file, indent=4)

'''
Idea for dealing with the data:

The given data is a list so we can go through the list
For every element in the list we use:
- type for type of event
- repo.name for repo where the event happened
- payload for details of event
- created_at for time of action

events in github:
- PushEvent
- CreateEvent
- DeleteEvent
- IssuesEvent
- 
'''