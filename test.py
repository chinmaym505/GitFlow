import git
import os

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

def print_help():
    print("""
    Welcome to Simplified Git! Available commands:
    - start: Initialize a new Git repository
    - sync <message>: Stage, commit, and sync changes with a message
    - branch <branch_name>: Create and switch to a new branch
    - switch <branch_name>: Switch to an existing branch
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
        elif command == "exit":
            print("Goodbye!")
            break
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()