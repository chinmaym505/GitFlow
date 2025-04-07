import git
import os

def start_repo():
    try:
        repo = git.Repo.init(os.getcwd())  # Initialize a new repository in the current directory
        print("Initialized a new Git repository!")
    except Exception as e:
        print(f"Error initializing repository: {e}")

def save_changes(message):
    try:
        repo = git.Repo(os.getcwd())  # Access the current repository
        repo.git.add(all=True)        # Stage all changes
        repo.git.commit(m=message)    # Commit with the provided message
        print(f"Changes saved with message: '{message}'")
    except Exception as e:
        print(f"Error saving changes: {e}")

def sync_repo():
    try:
        repo = git.Repo(os.getcwd())  # Access the current repository
        origin = repo.remotes.origin
        origin.pull(rebase=True)  # Pull changes with rebase
        origin.push()             # Push changes to the remote
        print("Repository synced!")
    except Exception as e:
        print(f"Error syncing repository: {e}")

def main():
    print("Welcome to Simplified Git!")
    print("Available commands: start, save, sync")
    
    while True:
        command = input("Enter a command (or 'exit' to quit): ").strip().lower()
        
        if command == "start":
            start_repo()
        elif command.startswith("save"):
            message = command.split(" ", 1)[1] if " " in command else "Default commit message"
            save_changes(message)
        elif command == "sync":
            sync_repo()
        elif command == "exit":
            print("Goodbye!")
            break
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()