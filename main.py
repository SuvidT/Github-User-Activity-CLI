import urllib.request
import json
import os

output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

while True:
    username = input("github-activity ")
    if username.lower() == "exit":
        break

    url = f"https://api.github.com/users/{username}/events"
    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode("utf-8"))

        # Save data to a file
        file_path = os.path.join(output_dir, f"{username}_events.json")
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Data saved to {file_path}")

        # Process and display events
        # Process and display events
        for event in data:
            event_type = event["type"]
            repo_name = event["repo"]["name"]

            if event_type == "PushEvent":
                commit_count = event["payload"]["size"]
                print(f"- Pushed {commit_count} commits to {repo_name}")
            elif event_type == "IssuesEvent":
                action = event["payload"]["action"]
                print(f"- {action.capitalize()} a new issue in {repo_name}")
            elif event_type == "WatchEvent":
                print(f"- Starred {repo_name}")
            elif event_type == "CreateEvent":
                ref_type = event["payload"]["ref_type"]
                ref = event["payload"]["ref"]
                print(f"- Created a new {ref_type} '{ref}' in {repo_name}")
            elif event_type == "DeleteEvent":
                ref_type = event["payload"]["ref_type"]
                ref = event["payload"]["ref"]
                print(f"- Deleted the {ref_type} '{ref}' in {repo_name}")
            elif event_type == "ForkEvent":
                forkee_name = event["payload"]["forkee"]["full_name"]
                print(f"- Forked {repo_name} to {forkee_name}")
            elif event_type == "PullRequestEvent":
                action = event["payload"]["action"]
                pr_title = event["payload"]["pull_request"]["title"]
                print(f"- {action.capitalize()} a pull request '{pr_title}' in {repo_name}")
            elif event_type == "IssueCommentEvent":
                action = event["payload"]["action"]
                comment_body = event["payload"]["comment"]["body"]
                print(f"- {action.capitalize()} a comment on an issue in {repo_name}: \"{comment_body}\"")
            elif event_type == "CommitCommentEvent":
                comment_body = event["payload"]["comment"]["body"]
                print(f"- Commented on a commit in {repo_name}: \"{comment_body}\"")
            elif event_type == "ReleaseEvent":
                action = event["payload"]["action"]
                release_tag = event["payload"]["release"]["tag_name"]
                print(f"- {action.capitalize()} a release '{release_tag}' in {repo_name}")
            elif event_type == "PublicEvent":
                print(f"- Made the repository {repo_name} public")
            elif event_type == "MemberEvent":
                action = event["payload"]["action"]
                member_name = event["payload"]["member"]["login"]
                print(f"- {action.capitalize()} {member_name} as a collaborator to {repo_name}")

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("Error: Invalid username.")
        else:
            print(f"HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")