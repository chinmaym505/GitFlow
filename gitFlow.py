import git
import os
import re
import requests
def ai():
    print("Enter 'exit' to exit")
    API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/31f7cbaa95c2a8ee374b735d539bbc08/ai/run/"
    headers = {"Authorization": "Bearer TurQr-Rnk6U9uTnYYceuqRtV2TXuVf5PFh_1Gr7p"}

    def run(model, inputs):
        input_data = {"messages": inputs}
        response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input_data)
        return response.json()

    def ai(user_input):
        inputs = [
            {"role": "system", "content": """You are a friendly assistant that helps solve issues with GitFlow, a simplified version of git. this is the tool's code so you can understand it to help the user navigate errors, and their questions:
            import git
    import os
    import re


    def start_repo():
        try:
            repo = git.Repo.init(os.getcwd())  # Initialize a new repository in the current directory
            print("Initialized a new Git repository!")
        except Exception as e:
            print(f"Error initializing repository: {e}")

    def check_uncommitted_changes(repo):
        \"""Check for uncommitted changes in the repository.\"""
        if repo.is_dirty(untracked_files=True):
            print("There are uncommitted changes in your repository. Please stage or commit your changes before proceeding.")
            return True
        return False

    def sync_changes(message):
        try:
            repo = git.Repo(os.getcwd())  # Access the current repository
            repo.git.add(all=True)        # Stage all changes
            repo.git.commit(m=message)    # Commit with the provided message
            origin = repo.remotes.origin  # Access the remote repository
            origin.pull(rebase=True)      # Pull changes with rebase
            origin.push()                 # Push changes to the remote
            print(f"Changes synced with message: '{message}'")
        except Exception as e:
            print(f"Error syncing changes: {e}")

    def create_branch(branch_name):
        try:
            repo = git.Repo(os.getcwd())  # Access the current repository
            if check_uncommitted_changes(repo):
                return  # Stop branch creation if there are uncommitted changes
            repo.git.checkout('-b', branch_name)  # Create and switch to the new branch
            print(f"Branch '{branch_name}' created and switched to.")
        except Exception as e:
            print(f"Error creating branch: {e}")

    def switch_branch(branch_name):
        try:
            repo = git.Repo(os.getcwd())  # Access the current repository
            if check_uncommitted_changes(repo):
                return  # Stop branch switching if there are uncommitted changes
            repo.git.checkout(branch_name)  # Switch to the specified branch
            print(f"Switched to branch '{branch_name}'.")
        except Exception as e:
            print(f"Error switching to branch: {e}")

    def delete_branch(branch_name):
        try:
            repo = git.Repo(os.getcwd())  # Access the current repository
            if check_uncommitted_changes(repo):
                return  # Stop branch deletion if there are uncommitted changes
            
            confirmation = input(f"Are you sure you want to delete the branch '{branch_name}'? (yes/no): ").strip().lower()
            if confirmation == "yes":
                repo.git.branch('-d', branch_name)
                print(f"Branch '{branch_name}' deleted successfully.")
            else:
                print("Branch deletion canceled.")
        except Exception as e:
            print(f"Error deleting branch: {e}")

    def is_valid_git_url(url):
    git_url_pattern = r"^(https?:\\/\\/|git@)[\\w.-]+(:\\d+)?\\/[\\w./-]+(\\.git)?$"
    return bool(re.match(git_url_pattern, url))

def link_remote(remote_name, remote_url):
    try:
        repo = git.Repo(os.getcwd())

        # Validate remote URL before adding
        if not is_valid_git_url(remote_url):
            print(f"Error: '{remote_url}' is not a valid Git repository URL.")
            return

        repo.create_remote(remote_name, remote_url)
        print(f"Remote '{remote_name}' linked with URL: {remote_url}")
    except Exception as e:
        print(f"Error linking remote: {e}")

    def reset_changes():
        try:
            repo = git.Repo(os.getcwd())  # Access the current repository
            if check_uncommitted_changes(repo):
                return  # Stop resetting if there are uncommitted changes
            
            confirmation = input("Are you sure you want to reset all uncommitted changes? This action cannot be undone. (yes/no): ").strip().lower()
            if confirmation == "yes":
                repo.git.reset('--hard')
                print("Uncommitted changes have been discarded.")
            else:
                print("Reset canceled.")
        except Exception as e:
            print(f"Error resetting changes: {e}")

    def print_help():
        print(\"""
        Welcome to Simplified Git! Available commands:
        - start: Initialize a new Git repository
        - link: Links current git repository to a remote
        - sync <message>: Stage, commit, and sync changes with a message
        - branch <branch_name>: Create and switch to a new branch
        - switch <branch_name>: Switch to an existing branch
        - delete <branch_name>: Delete an existing branch (requires confirmation)
        - reset: Discard all uncommitted changes (requires confirmation)
        - help: displays the help menu
        - exit: Quit the tool
        \""")

    def main():
        print_help()
        while True:
            command = input("Enter a command (or 'exit' to quit): ").strip().lower()
            
            if command == "start":
                start_repo()
            elif command.startswith("sync"):
                message = command.split(" ", 1)[1] if " " in command else "Default sync message"
                sync_changes(message)
            elif command.startswith("branch"):
                branch_name = command.split(" ", 1)[1] if " " in command else None
                if branch_name:
                    create_branch(branch_name)
                else:
                    print("Please specify a branch name.")
            elif command.startswith("switch"):
                branch_name = command.split(" ", 1)[1] if " " in command else None
                if branch_name:
                    switch_branch(branch_name)
                else:
                    print("Please specify a branch name.")
            elif command.startswith("delete"):
                branch_name = command.split(" ", 1)[1] if " " in command else None
                if branch_name:
                    delete_branch(branch_name)
                else:
                    print("Please specify a branch name.")
            elif command == "reset":
                reset_changes()
            elif command == "help":
                print_help()
            elif command == "exit":
                print("Goodbye!")
                break
            else:
                print("Unknown command. Please try again.")

    if __name__ == "__main__":
        main()"""},
            {"role": "user", "content": user_input}
        ]
        output = run("@cf/meta/llama-3-8b-instruct", inputs)
        
        # Extract only the response text
        return output.get("result", {}).get("response", "No response received.")
    using = True
    while using:
        user_input = input("> ")
        if user_input == "exit":
            using = False
        else:
            print(ai(user_input))
def start_repo():
    try:
        repo = git.Repo.init(os.getcwd())  # Initialize a new repository in the current directory
        print("Initialized a new Git repository!")
    except Exception as e:
        print(f"Error initializing repository: {e}")

def check_uncommitted_changes(repo):
    """Check for uncommitted changes in the repository."""
    if repo.is_dirty(untracked_files=True):
        print("There are uncommitted changes in your repository. Please stage or commit your changes before proceeding.")
        return True
    return False

def sync_changes(message):
    try:
        repo = git.Repo(os.getcwd())  # Access the current repository
        repo.git.add(all=True)        # Stage all changes
        repo.git.commit(m=message)    # Commit with the provided message
        origin = repo.remotes.origin  # Access the remote repository
        origin.pull(rebase=True)      # Pull changes with rebase
        origin.push()                 # Push changes to the remote
        print(f"Changes synced with message: '{message}'")
    except Exception as e:
        print(f"Error syncing changes: {e}")

def create_branch(branch_name):
    try:
        repo = git.Repo(os.getcwd())  # Access the current repository
        if check_uncommitted_changes(repo):
            return  # Stop branch creation if there are uncommitted changes
        repo.git.checkout('-b', branch_name)  # Create and switch to the new branch
        print(f"Branch '{branch_name}' created and switched to.")
    except Exception as e:
        print(f"Error creating branch: {e}")

def switch_branch(branch_name):
    try:
        repo = git.Repo(os.getcwd())  # Access the current repository
        if check_uncommitted_changes(repo):
            return  # Stop branch switching if there are uncommitted changes
        repo.git.checkout(branch_name)  # Switch to the specified branch
        print(f"Switched to branch '{branch_name}'.")
    except Exception as e:
        print(f"Error switching to branch: {e}")

def delete_branch(branch_name):
    try:
        repo = git.Repo(os.getcwd())  # Access the current repository
        if check_uncommitted_changes(repo):
            return  # Stop branch deletion if there are uncommitted changes
        
        confirmation = input(f"Are you sure you want to delete the branch '{branch_name}'? (yes/no): ").strip().lower()
        if confirmation == "yes":
            repo.git.branch('-d', branch_name)
            print(f"Branch '{branch_name}' deleted successfully.")
        else:
            print("Branch deletion canceled.")
    except Exception as e:
        print(f"Error deleting branch: {e}")

def reset_changes():
    try:
        repo = git.Repo(os.getcwd())  # Access the current repository
        if check_uncommitted_changes(repo):
            return  # Stop resetting if there are uncommitted changes
        
        confirmation = input("Are you sure you want to reset all uncommitted changes? This action cannot be undone. (yes/no): ").strip().lower()
        if confirmation == "yes":
            repo.git.reset('--hard')
            print("Uncommitted changes have been discarded.")
        else:
            print("Reset canceled.")
    except Exception as e:
        print(f"Error resetting changes: {e}")

def is_valid_git_url(url):
    """Validate if the provided URL is a valid Git remote repository."""
    git_url_pattern = r"^(https?:\/\/|git@)[\w.-]+(:\d+)?\/[\w./-]+(\.git)?$"
    return bool(re.match(git_url_pattern, url))

def link_remote(remote_name, remote_url):
    try:
        repo = git.Repo(os.getcwd())

        # Validate remote URL before adding
        if not is_valid_git_url(remote_url):
            print(f"Error: '{remote_url}' is not a valid Git repository URL.")
            return

        repo.create_remote(remote_name, remote_url)
        print(f"Remote '{remote_name}' linked with URL: {remote_url}")
    except Exception as e:
        print(f"Error linking remote: {e}")

def print_help():
    print("""
    Welcome to Simplified Git! Available commands:
    - start: Initialize a new Git repository
    - link: Links current git repository to a remote 
    - sync <message>: Stage, commit, and sync changes with a message
    - branch <branch_name>: Create and switch to a new branch
    - switch <branch_name>: Switch to an existing branch
    - delete <branch_name>: Delete an existing branch (requires confirmation)
    - reset: Discard all uncommitted changes (requires confirmation)
    - ai: Opens up an AI assistant to help you
    - help: Displays the help menu
    - exit: Quit the tool
    """)

def main():
    print_help()
    while True:
        command = input("Enter a command (or 'exit' to quit): ").strip().lower()
        
        if command == "start":
            start_repo()
        elif command.startswith("sync"):
            message = command.split(" ", 1)[1] if " " in command else "Default sync message"
            sync_changes(message)
        elif command.startswith("branch"):
            branch_name = command.split(" ", 1)[1] if " " in command else None
            if branch_name:
                create_branch(branch_name)
            else:
                print("Please specify a branch name.")
        elif command.startswith("switch"):
            branch_name = command.split(" ", 1)[1] if " " in command else None
            if branch_name:
                switch_branch(branch_name)
            else:
                print("Please specify a branch name.")
        elif command.startswith("delete"):
            branch_name = command.split(" ", 1)[1] if " " in command else None
            if branch_name:
                delete_branch(branch_name)
            else:
                print("Please specify a branch name.")
        elif command == "reset":
            reset_changes()
        elif command.startswith("link"):
            parts = command.split(" ")
            if len(parts) == 3:
                remote_name, remote_url = parts[1], parts[2]
                link_remote(remote_name, remote_url)
            else:
                print("Usage: link <remote_name> <remote_url>")

        elif command == "ai":
            ai()
        elif command == "help":
                print_help()
        elif command == "exit":
            print("Goodbye!")
            break
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()