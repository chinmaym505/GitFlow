# Import necessary libraries
import git  # Provides Git functionalities for repository management
import os  # Enables interaction with the operating system, such as file paths and directories
import re  # Allows the use of regular expressions for pattern matching
import requests  # Facilitates making HTTP requests to external APIs
import subprocess  # Enables the execution of external commands and processes
import json  # Provides functionalities for working with JSON data
import time  # Allows for time-related functions, such as delays
import keyboard  # Provides functionalities for keyboard event handling
import readchar  # Facilitates reading single characters from the keyboard
import sys  # Provides access to system-specific parameters and functions
import signal  # Provides mechanisms to handle asynchronous events, such as process termination

def toggle_keyboard_block(block=True):
    """Blocks or unblocks all common keys, including letters A-Z."""
    keys_to_manage = [
        'esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
        'print_screen', 'scroll_lock', 'pause',
        'tab', 'caps lock', 'shift', 'ctrl', 'alt', 'space', 'enter', 'backspace',
        'insert', 'home', 'page_up', 'delete', 'end', 'page_down',
        'left', 'right', 'up', 'down',
    ] + [str(i) for i in range(10)] + [chr(i) for i in range(ord('a'), ord('z')+1)]  # Numbers + Letters A-Z

    for key in keys_to_manage:
        if block:
            keyboard.block_key(key)
        else:
            keyboard.unblock_key(key)


# Define the AI assistant function
# This function provides interactive assistance for GitFlow commands
# It uses an external API to process user inputs and generate responses
# The AI assistant is designed to help users with GitFlow-related queries
# and provide suggestions or solutions based on the user's input
def ai():
    # Start the Llamafile server process only when AI is invoked
    server_process = subprocess.Popen(
        ["GitFlow-LLM-v15.llamafile.exe", "--threads", "8", "--port", "8080"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        system_prompt = """Your name is GitFlow Asistant, Chinmay M modified you to work for GitFlow. Your purpose is to help users navigate through GitFlow, a tool to simplify git made by Chinmay M.
    use these available tool commands to assist the user:

    - copy: copies a remote Git repository into a new local one
    - start: Initialize a new Git repository
    - link: Links current Git repository to a remote 
    - sync <message>: Stage, commit, and sync changes with a message
    - branch <branch_name>: Create and switch to a new branch
    - switch <branch_name>: Switch to an existing branch
    - delete <branch_name>: Delete an existing branch (requires confirmation)
    - reset: Discard all uncommitted changes (requires confirmation)
    - help: Displays the help menu
    - exit: Quit the tool

    REMEMBER TO TALK ABOUT GITFLOW COMMANDS, NOT GIT COMMANDS!!!!!
    ps. dont say you are chinmay m's assistant."""
    

        # Base URL for the local Llamafile server
        API_BASE_URL = "http://127.0.0.1:8080/v1/chat/completions"
        # Headers for the API request
        headers = {"Content-Type": "application/json"}

        conversation_history = [{"role": "system", "content": system_prompt}]  # Initialize with system prompt

        # Function to send a request to the local Llamafile server
        def run(inputs):
            # Prepare the input data for the API request, including the history
            messages = conversation_history + inputs
            input_data = {"model": "GitFlow-LLM", "messages": messages}
            # Send a POST request to the API and return the response
            try:
                toggle_keyboard_block() # Block input before making the request
                response = requests.post(API_BASE_URL, headers=headers, json=input_data)
                response.raise_for_status()
                return response.json()  # Return the JSON response from the API
            except requests.exceptions.RequestException as e:
                print(f"Error communicating with the server: {e}")
                return None
            except json.JSONDecodeError:
                print("Error: Could not decode the server's JSON response.")
                return None
            finally:
                toggle_keyboard_block(False) # Unblock input after the request
                

        # Function to interact with the AI model
        def ai_response(user_input):
            # Prepare the input messages for the AI model
            inputs = [{"role": "user", "content": user_input}]
            # Call the API and return the generated response
            output = run(inputs)
            if output and "choices" in output and output["choices"]:
                assistant_response = output["choices"][0]["message"]["content"].replace("<end_of_turn>", "").strip()
                # Add the user's input and the assistant's response to the history
                conversation_history.append({"role": "user", "content": user_input})
                conversation_history.append({"role": "assistant", "content": assistant_response})
                return assistant_response
            else:
                return "No response received from the AI."

        using = True  # Flag to keep the AI assistant running
        while using:
            print("> ", end="", flush=True)
            user_input = ""
            # Read characters until Enter is pressed
            while True:
                key = readchar.readkey()
                if key == readchar.key.ENTER:
                    print()
                    break
                elif key == readchar.key.BACKSPACE:
                    if len(user_input) > 0:
                        user_input = user_input[:-1]
                        print("\b \b", end="", flush=True)  # Erase the last character
                elif isinstance(key, str):
                    user_input += key
                    print(key, end="", flush=True)

            if user_input.lower() == "exit":  # Check if the user wants to exit
                using = False  # Set the flag to False to exit the loop
                print("Exiting chat. Goodbye!")
            elif user_input: # Only send to AI if there was input
                # Get the AI-generated response
                response = ai_response(user_input)
                if response:
                    print(response+"\n")
    finally:
        # Ensure the server process is terminated when the AI session ends
        if server_process.poll() is None:
            server_process.terminate()
            server_process.wait()

def start_repo():
    try:
        repo = git.Repo.init(os.getcwd())
        print("Initialized a new Git repository!")
    except Exception as e:
        print(f"Error initializing repository: {e}")

def check_uncommitted_changes(repo):
    if repo.is_dirty(untracked_files=True):
        print("There are uncommitted changes in your repository. Please stage or commit your changes before proceeding.")
        return True
    return False

def sync_changes(message):
    try:
        repo = git.Repo(os.getcwd())
        repo.git.add(all=True)
        repo.git.commit(m=message)
        try:
            origin = repo.remotes.origin
            origin.pull(rebase=True)
            origin.push()
        except:
            pass
        print(f"Changes synced with message: '{message}'")
    except Exception as e:
        print(f"Error syncing changes: {e}")

def create_branch(branch_name):
    try:
        repo = git.Repo(os.getcwd())
        if check_uncommitted_changes(repo):
            return
        repo.git.checkout('-b', branch_name)
        print(f"Branch '{branch_name}' created and switched to.")
    except Exception as e:
        print(f"Error creating branch: {e}")

def switch_branch(branch_name):
    try:
        repo = git.Repo(os.getcwd())
        if check_uncommitted_changes(repo):
            return
        repo.git.checkout(branch_name)
        print(f"Switched to branch '{branch_name}'.")
    except Exception as e:
        print(f"Error switching to branch: {e}")

def delete_branch(branch_name):
    try:
        repo = git.Repo(os.getcwd())
        if check_uncommitted_changes(repo):
            return
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
        repo = git.Repo(os.getcwd())
        confirmation = input("Are you sure you want to reset all uncommitted changes? This action cannot be undone. (yes/no): ").strip().lower()
        if confirmation == "yes":
            repo.git.reset('--hard')
            print("Uncommitted changes have been discarded.")
        else:
            print("Reset canceled.")
    except Exception as e:
        print(f"Error resetting changes: {e}")

def is_valid_git_url(url):
    git_url_pattern = r"^(https?:\/\/|git@)[\w.-]+(:\d+)?\/[\w./-]+(\.git)?$"
    return bool(re.match(git_url_pattern, url))

def link_remote(remote_name, remote_url):
    try:
        repo = git.Repo(os.getcwd())
        if not is_valid_git_url(remote_url):
            print(f"Error: '{remote_url}' is not a valid Git repository URL.")
            return
        repo.create_remote(remote_name, remote_url)
        print(f"Remote '{remote_name}' linked with URL: {remote_url}")
    except Exception as e:
        print(f"Error linking remote: {e}")

def clone_repository(remote_url, directory_name=None):
    try:
        if not is_valid_git_url(remote_url):
            print(f"Error: '{remote_url}' is not a valid Git repository URL.")
            return
        directory_name = directory_name or os.path.basename(remote_url).replace(".git", "")
        git.Repo.clone_from(remote_url, directory_name)
        print(f"Repository cloned into '{directory_name}'")
    except Exception as e:
        print(f"Error cloning repository: {e}")

def fork_repository(remote_to_be_forked, remote_forked):
    try:
        if not is_valid_git_url(remote_to_be_forked):
            print(f"Error: '{remote_to_be_forked}' is not a valid Git repository URL.")
            return
        if not is_valid_git_url(remote_forked):
            print(f"Error: '{remote_forked}' is not a valid Git repository URL.")
            return
        directory_name = os.path.basename(remote_to_be_forked).replace(".git", "")
        clone_repository(remote_to_be_forked, directory_name)
        repo = git.Repo(directory_name)
        link_remote("origin", remote_forked)
        print(f"Repository forked into '{directory_name}' and linked to '{remote_forked}'")
    except Exception as e:
        print(f"Error forking repository: {e}")

def print_help():
    print("""
    Welcome to Simplified Git! Available commands:
    - copy: copies a remote Git repository into a new local one
    - start: Initialize a new Git repository
    - link: Links current Git repository to a remote 
    - sync <message>: Stage, commit, and sync changes with a message
    - branch <branch_name>: Create and switch to a new branch
    - switch <branch_name>: Switch to an existing branch
    - delete <branch_name>: Delete an existing branch (requires confirmation)
    - reset: Discard all uncommitted changes (requires confirmation)
    - ai: Opens up an AI assistant to help you
    - help: Displays the help menu
    - exit: Quit the tool
    - fork <remote_to_be_forked> <remote_forked>: Fork a repository and link it to a new remote
    """)

def main():
    while True:
        working_directory = input("Enter the directory to work in: ").strip()
        if os.path.isdir(working_directory):
            os.chdir(working_directory)
            break
        else:
            print(f"Error: '{working_directory}' is not a valid directory. Please try again.")

    print(f"Working in directory: {working_directory}")
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
            # Handle the 'link' command to link a remote repository
            # Split the command into parts to extract the remote name and URL
            parts = command.split(" ")
            if len(parts) == 3:
                remote_name, remote_url = parts[1], parts[2]
                # Call the function to link the remote repository
                link_remote(remote_name, remote_url)
            else:
                # Inform the user about the correct usage of the 'link' command
                print("Usage: link <remote_name> <remote_url>")
        elif command == "ai":
            # Open the AI assistant for GitFlow help
            # This will provide interactive assistance for GitFlow commands
            ai()
        elif command == "help":
            # Display the help menu with all available commands
            print_help()
        elif command == "exit":
            # Exit the program gracefully
            print("Goodbye!")
            keyboard.unhook_all()  # Clean up keyboard hooks before exiting
            break
        elif command.startswith("fork"):
            # Handle the 'fork' command to fork a repository and link it to a new remote
            # Split the command into parts to extract the source and target remote URLs
            parts = command.split(" ")
            if len(parts) == 3:
                remote_to_be_forked, remote_forked = parts[1], parts[2]
                # Call the function to fork the repository
                fork_repository(remote_to_be_forked, remote_forked)
            else:
                # Inform the user about the correct usage of the 'fork' command
                print("Usage: fork <remote_to_be_forked> <remote_forked>")
        elif command.startswith("copy"):
            # Handle the 'copy' command to clone a remote repository
            # Split the command into parts to extract the remote URL
            parts = command.split(" ")
            if len(parts) == 2:
                remote_url = parts[1]
                # Call the function to clone the repository
                clone_repository(remote_url)
            else:
                # Inform the user about the correct usage of the 'copy' command
                print("Usage: copy <remote_url>")
        else:
            # Handle unknown commands by informing the user
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting program.")
        keyboard.unhook_all()  # Clean up keyboard hooks on interrupt
        sys.exit(0)