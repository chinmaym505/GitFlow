###################################################
#       GitFlow - A simplified version of Git     #
#          Made by Chinmay M (chinmaym505)        #
#                    5/28/2025                    #
###################################################

# {{58DFC7E2-4C46-4715-9FCB-684D5EE7E1CF}

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
import ctypes # Provides access to low-level system calls, particularly for setting file attributes on Windows
import shutil # Provides high-level file operations, such as copying and removing files and directories
import socket # Enables low-level networking interfaces, such as creating sockets for network communication
import difflib # Provides classes and functions for comparing sequences, particularly useful for generating diffs between files
import subprocess # Allows the execution of external commands and processes, such as starting the Llamafile server
import requests # Facilitates making HTTP requests to external APIs, such as the Llamafile server for AI assistance
import tkinter as tk  # Provides a GUI toolkit for creating graphical user interfaces
from tkinter import filedialog  # Provides file dialog functionalities for selecting directories
from tkinter import messagebox  # Provides message box functionalities for displaying alerts and information   
os.system("title GitFlow 1.2.1")
 # Base URL for the local Llamafile server
API_BASE_URL = "http://127.0.0.1:8080/v1/chat/completions"
# Headers for the API request
headers = {"Content-Type": "application/json"}

def select_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_selected = filedialog.askdirectory(title="Select your project folder")
    if folder_selected == "":
        messagebox.showwarning("Warning","No folder selected. Exiting.")
        sys.exit(0)  # Exit if no folder is selected
    root.destroy()
    return folder_selected

def ensure_llamafile_server():
    """Ensure the Llamafile server is running. Start it if not already running."""
    import requests, subprocess, time, socket
    def is_port_in_use(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("127.0.0.1", port)) == 0
    if not is_port_in_use(8080):
        # Start the server
        subprocess.Popen(
            ["GitFlow-LLM-v15.llamafile.exe", "--threads", "3", "--port", "8080", "-ngl", "999"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # Wait for server to be ready
        for _ in range(30):
            try:
                r = requests.get("http://127.0.0.1:8080/", timeout=1)
                if r.status_code == 200:
                    return
            except Exception:
                time.sleep(1)
        print("Llamafile server did not start in time.")

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

def generate_diff_report(file1_path, file2_path):
  """Generates a diff report using difflib."""
  try:
      with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
          diff = difflib.unified_diff(file1.readlines(), file2.readlines(), fromfile=file1_path, tofile=file2_path)
          return ''.join(diff)
  except FileNotFoundError:
    return None
  
# Define the AI assistant function
# This function provides interactive assistance for GitFlow commands
# It uses an external API to process user inputs and generate responses
# The AI assistant is designed to help users with GitFlow-related queries
# and provide suggestions or solutions based on the user's input
def ai():
    ensure_llamafile_server()
    system_prompt = """Your name is GitFlow Asistant, Chinmay M modified you to work for GitFlow. Your purpose is to help users navigate through GitFlow, a tool to simplify git made by Chinmay M.
    use these available tool commands to assist the user:

    - copy: copies a remote Git repository into a new local one
    - start: Initialize a new Git repository
    - link: Links current Git repository to a remote 
    - sync <message>: Stage, commit, and sync changes with a message, if the message is 'ai', it will generate a commit message for you
    - branch <branch_name>: Create and switch to a new branch
    - switch <branch_name>: Switch to an existing branch
    - delete <branch_name>: Delete an existing branch (requires confirmation)
    - reset: Discard all uncommitted changes (requires confirmation)
    - help: Displays the help menu
    - exit: Quit the tool

    REMEMBER TO TALK ABOUT GITFLOW COMMANDS, NOT GIT COMMANDS!!!!!
    *ps. dont say you are chinmay m's assistant, say you are the user's assistant.*"""
    conversation_history = [{"role": "system", "content": system_prompt}]

    def run(inputs):
        messages = conversation_history + inputs
        input_data = {"model": "GitFlow-LLM", "messages": messages}
        try:
            toggle_keyboard_block()
            response = requests.post(API_BASE_URL, headers=headers, json=input_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with the server: {e}")
            return None
        except json.JSONDecodeError:
            print("Error: Could not decode the server's JSON response.")
            return None
        finally:
            toggle_keyboard_block(False)

    def ai_response(user_input):
        inputs = [{"role": "user", "content": user_input}]
        output = run(inputs)
        if output and "choices" in output and output["choices"]:
            assistant_response = output["choices"][0]["message"]["content"].replace("<end_of_turn>", "").strip()
            conversation_history.append({"role": "user", "content": user_input})
            conversation_history.append({"role": "assistant", "content": assistant_response})
            return assistant_response
        else:
            return "No response received from the AI."

    using = True
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
def ai_commit(file1_path, file2_path):
    ensure_llamafile_server()
    """makes a commit message using the AI assistant based on the diff between two files."""
    # Try to read the original file, if not found, treat as new file
    try:
        with open(file1_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except FileNotFoundError:
        original_content = ''
    try:
        with open(file2_path, 'r', encoding='utf-8') as f:
            new_content = f.read()
    except FileNotFoundError:
        new_content = ''
    # Generate diff
    diff_output = ''.join(difflib.unified_diff(
        original_content.splitlines(keepends=True),
        new_content.splitlines(keepends=True),
        fromfile=file1_path,
        tofile=file2_path
    ))
    if diff_output.strip():
        prompt = (
            "Given this git diff, generate a concise, conventional commit message. "
            "Only return the commit message, nothing else.\n\n" + diff_output
        )
        input_data = {
            "model": "GitFlow-LLM",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        try:
            response = requests.post(API_BASE_URL, headers=headers, json=input_data)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].replace("<end_of_turn>", "").strip()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            print("Error sending request to the API")
            return None
    else:
        print(f"No changes detected for {file2_path}, skipping.")
        return None
def start_repo():
    try:
        repo = git.Repo.init(os.getcwd())
        ensure_gitflow_ignored(repo)
        print("Initialized a new Git repository!")
    except Exception as e:
        print(f"Error initializing repository: {e}")

def ensure_gitflow_ignored(repo):
    gitignore_path = os.path.join(repo.working_tree_dir, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r+") as f:
            lines = f.read().splitlines()
            if not any(line.strip() == ".GitFlow/" for line in lines):
                f.write("\n.GitFlow/\n")
    else:
        with open(gitignore_path, "w") as f:
            f.write(".GitFlow/\n")

def check_uncommitted_changes(repo):
    if repo.is_dirty(untracked_files=True):
        print("There are uncommitted changes in your repository. Please stage or commit your changes before proceeding.")
        return True
    return False

def sync_changes(message):
    repo = git.Repo(os.getcwd())
    ensure_gitflow_ignored(repo)
    # Define the hidden folder path
    hidden_folder = os.path.join(repo.working_tree_dir, ".GitFlow")

    # Define the temp folder path inside .GitFlow
    temp_folder = os.path.join(hidden_folder, "temp")

    # Clean out the temp folder at the start
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
    os.makedirs(temp_folder, exist_ok=True)
    if message == 'ai':
        ensure_llamafile_server()  # Ensure server is started only if needed
        print("Starting AI commit message generation...")
        # Clean out the temp folder at the start
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)
        os.makedirs(temp_folder, exist_ok=True)
        try:
            while True:
                modified_files = [item.a_path for item in repo.index.diff(None)]
                hidden_folder = os.path.join(repo.working_tree_dir, ".GitFlow")
                ctypes.windll.kernel32.SetFileAttributesW(hidden_folder, 2)
                commits = []
                for file_name in modified_files:
                    original_content = repo.git.show(f"HEAD:{file_name}")
                    destination_file = os.path.join(temp_folder, "original " + file_name)
                    os.makedirs(os.path.dirname(destination_file), exist_ok=True)
                    with open(destination_file, "w", encoding="utf-8") as file:
                        file.write(original_content)
                    commit_msg = ai_commit(destination_file, file_name)
                    if commit_msg:
                        for prefix in ["feat:", "fix:", "chore:", "refactor:", "docs:", "style:", "test:", "perf:", "ci:", "build:", "revert:","Feat:","Fix:"]:
                            commit_msg = commit_msg.replace(prefix, "")
                        commit_msg = commit_msg.replace('```', '').strip()
                        formatted_msg = f"*{file_name}*\n{commit_msg}"
                        commits.append(formatted_msg)
                commit_message = "\n\n".join(filter(None, commits)).strip()
                user_input = input("Generated commit message:\n" + commit_message + "\nDo you want to use this message? (yes/no/cancel): ").strip().lower()
                if user_input == "yes":
                    commit_message_file = os.path.join(temp_folder, "commit_message.txt")
                    with open(commit_message_file, "w", encoding="utf-8") as f:
                        f.write(commit_message)
                    message = commit_message_file
                    # Proceed to commit
                    repo.git.add(all=True)
                    repo.git.commit(F=message)
                    try:
                        origin = repo.remotes.origin
                        origin.pull(rebase=True)
                        origin.push()
                    except:
                        pass
                    print(f"Changes synced with message:\n{open(message, 'r', encoding='utf-8').read()}")
                    break
                elif user_input == "no":
                    next_action = input("Do you want to retry AI, enter a message manually, or cancel? (ai/manual/cancel): ").strip().lower()
                    if next_action == "manual":
                        manual_message = input("Enter your commit message: ")
                        repo.git.add(all=True)
                        repo.git.commit(m=manual_message)
                        try:
                            origin = repo.remotes.origin
                            origin.pull(rebase=True)
                            origin.push()
                        except:
                            pass
                        print(f"Changes synced with message:\n{manual_message}")
                        break
                    elif next_action == "ai":
                        print("Retrying to generate commit message...")
                        continue
                    elif next_action == "cancel":
                        print("AI commit cancelled. No changes were committed.")
                        break
                    else:
                        print("Invalid option. Cancelling.")
                        break
                elif user_input == "cancel":
                    print("AI commit cancelled. No changes were committed.")
                    break
                else:
                    print("Please answer 'yes', 'no', or 'cancel'.")
        except Exception as e:
            print(f"Error syncing changes: {e}")
        finally:
            if os.path.exists(temp_folder):
                shutil.rmtree(temp_folder)
        return
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
        print(f"Changes synced with message:\n{message}")
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
    Welcome to GitFlow, a simplified version of Git! Available commands:
    - copy: copies a remote Git repository into a new local one
    - start: Initialize a new Git repository
    - link: Links current Git repository to a remote 
    - sync <message>: Stage, commit, and sync changes with a message, if the message is 'ai', it will generate a commit message for you
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
    # Check for folder path argument (for context menu integration)
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        working_directory = sys.argv[1]
        os.chdir(working_directory)
    else:
        while True:
            working_directory = select_directory()
            if os.path.isdir(working_directory):
                os.chdir(working_directory)
                break
            else:
                print(f"Error: '{working_directory}' is not a valid directory. Please try again.")
    # Ensure .GitFlow is ignored in the selected repo (if any)
    os.system(f"title {os.path.basename(os.path.normpath(working_directory))} - GitFlow 1.2.1")
    try:
        repo = git.Repo(os.getcwd())
        ensure_gitflow_ignored(repo)
    except Exception:
        pass  # Not a git repo yet, ignore
    print(f"Working in directory: {os.getcwd()}")
    print_help()
    while True:
        command = input("Enter a command (or 'exit' to quit): ").strip().lower()
        if command == "start":
            start_repo()
        elif command.startswith("sync"):
            message = command.split(" ", 1)[1] if " " in command else "Made changes"
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
            keyboard.unhook_all()
            break
        elif command.startswith("fork"):
            parts = command.split(" ")
            if len(parts) == 3:
                remote_to_be_forked, remote_forked = parts[1], parts[2]
                fork_repository(remote_to_be_forked, remote_forked)
            else:
                print("Usage: fork <remote_to_be_forked> <remote_forked>")
        elif command.startswith("copy"):
            parts = command.split(" ")
            if len(parts) == 2:
                remote_url = parts[1]
                clone_repository(remote_url)
            else:
                print("Usage: copy <remote_url>")
        else:
            print("Unknown command. Please try again.")
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting program.")
        keyboard.unhook_all()  # Clean up keyboard hooks on interrupt
        sys.exit(0)