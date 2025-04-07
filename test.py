import git
import os

def start_repo():
    try:
        repo = git.Repo.init(os.getcwd())  # Initialize a new repository in the current directory
        print("Initialized a new Git repository!")
    except Exception as e:
        print(f"Error initializing repository: {e}")

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

def print_help():
    print("""
    Welcome to Simplified Git! Available commands:
    - start: Initialize a new Git repository
    - sync <message>: Stage, commit, and sync changes with a message
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
        elif command == "exit":
            print("Goodbye!")
            break
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()