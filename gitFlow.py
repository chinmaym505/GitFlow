###################################################
#       GitFlow - A simplified version of Git     #
#          Made by Chinmay M (chinmaym505)        #
#                    6/6/2025                     #
###################################################

# {{58DFC7E2-4C46-4715-9FCB-684D5EE7E1CF}

# Import necessary libraries
import threading
import git  # Provides Git functionalities for repository management
import os  # Enables interaction with the operating system, such as file paths and directories
import re  # Allows the use of regular expressions for pattern matching
import requests  # Facilitates making HTTP requests to external APIs
import subprocess  # Enables the execution of external commands and processes
import json  # Provides functionalities for working with JSON data
import time  # Allows for time-related functions, such as delays
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
import json  # Provides functionalities for working with JSON data, such as reading and writing user preferences
import colorama  # Provides color formatting for terminal output, enhancing the user experience with colored text

class GitFlow:
    def __init__(self):
        self.API_BASE_URL = "http://127.0.0.1:8080/v1/chat/completions"
        self.headers = {"Content-Type": "application/json"}
        self.COLORAMA_AVAILABLE = False
        try:
            from colorama import init, Fore, Style
            init(autoreset=True)
            self.Fore = Fore
            self.Style = Style
            self.COLORAMA_AVAILABLE = True
        except ImportError:
            pass
        self.prev_command_container = ['']
        self.working_directory = None  # Initialize working directory

    def color_text(self, text, color):
        if not self.COLORAMA_AVAILABLE:
            return text
        return color + text + self.Style.RESET_ALL

    def print_error(self, msg):
        print(self.color_text(msg, self.Fore.RED) if self.COLORAMA_AVAILABLE else msg)

    def print_success(self, msg):
        print(self.color_text(msg, self.Fore.GREEN) if self.COLORAMA_AVAILABLE else msg)

    def print_info(self, msg):
        print(self.color_text(msg, self.Fore.CYAN) if self.COLORAMA_AVAILABLE else msg)

    def print_warning(self, msg):
        print(self.color_text(msg, self.Fore.YELLOW) if self.COLORAMA_AVAILABLE else msg)

    def select_directory(self):
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        folder_selected = filedialog.askdirectory(title="Select your project folder")
        if folder_selected == "":
            self.print_warning("No folder selected. Exiting.")
            sys.exit(0)
        root.destroy()
        return folder_selected

    def ensure_llamafile_server(self):
        import requests, subprocess, time, socket
        def is_port_in_use(port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("127.0.0.1", port)) == 0
        if not is_port_in_use(8080):
            subprocess.Popen([
                "GitFlow-LLM-v15.llamafile.exe", "--threads", "3", "--port", "8080", "-ngl", "999"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for _ in range(30):
                try:
                    r = requests.get("http://127.0.0.1:8080/", timeout=1)
                    if r.status_code == 200:
                        return
                except Exception:
                    time.sleep(1)
            self.print_warning("Llamafile server did not start in time.")

    def get_line_input(self, prompt, prev_command=None):
        import readchar
        print(prompt, end='', flush=True)
        user_input = ''
        cursor_pos = 0
        if prev_command is None:
            prev_command = ''
        prev_len = 0
        while True:
            key = readchar.readkey()
            if key == readchar.key.ENTER:
                print()
                break
            elif key == readchar.key.BACKSPACE:
                if cursor_pos > 0:
                    user_input = user_input[:cursor_pos-1] + user_input[cursor_pos:]
                    cursor_pos -= 1
            elif key == getattr(readchar.key, 'UP', '\x1b[A'):
                if prev_command:
                    user_input = prev_command
                    cursor_pos = len(user_input)
            elif key == getattr(readchar.key, 'LEFT', '\x1b[D'):
                if cursor_pos > 0:
                    cursor_pos -= 1
            elif key == getattr(readchar.key, 'RIGHT', '\x1b[C'):
                if cursor_pos < len(user_input):
                    cursor_pos += 1
            elif isinstance(key, str) and len(key) == 1:
                user_input = user_input[:cursor_pos] + key + user_input[cursor_pos:]
                cursor_pos += 1
            print('\r' + prompt + user_input, end='', flush=True)
            if prev_len > len(user_input):
                print(' ' * (prev_len - len(user_input)), end='', flush=True)
                if cursor_pos < len(user_input):
                    print('\b' * (len(user_input) - cursor_pos), end='', flush=True)
                print('\b' * (prev_len - len(user_input)), end='', flush=True)
            else:
                if cursor_pos < len(user_input):
                    print('\b' * (len(user_input) - cursor_pos), end='', flush=True)
            prev_len = len(user_input)
        return user_input

    def readchar_input(self, prompt, prev_command_container=None):
        if prev_command_container is None:
            prev_command_container = ['']
        user_input = self.get_line_input(prompt, prev_command_container[0])
        prev_command_container[0] = user_input
        return user_input.strip().lower()

    def generate_diff_report(self, file1_path, file2_path):
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
    def ai(self):
        self.ensure_llamafile_server()
        system_prompt = """Your name is GitFlow Asistant, Chinmay M modified you to work for GitFlow. Your purpose is to help users navigate through GitFlow, a tool to simplify git made by Chinmay M.
        use these available tool commands to assist the user:

        - copy: copies a remote Git repository into a new local one
        - start: Initialize a new Git repository
        - link: Links current Git repository to a remote 
        - unlink <remote_name>: Unlinks (removes) a remote from the current repository
        - sync <message>: Stage, commit, and sync changes with a message, if the message is 'ai', it will generate a commit message for you
        - branch <branch_name>: Create and switch to a new branch
        - switch <branch_name>: Switch to an existing branch
        - delete <branch_name>: Delete an existing branch (requires confirmation)
        - reset: Discard all uncommitted changes (requires confirmation)
        - remotes: Show all remotes for the current repository
        - ai: Opens up an AI assistant to help you
        - help: Displays the help menu
        - exit: Quit the tool
        - fork <remote_to_be_forked> <remote_forked>: Fork a repository and link it to a new remote
        - history: Show the commit history of the current repository
        - revert <commit_hash>: Revert a specific commit by its hash
        - status: Show the directory structure and git status (U: untracked, M: modified, D: deleted) for the current working directory
        - config: Configure GitFlow with your preferences
        - list_branches: List all branches in the current repository. The current branch is marked with an asterisk (*).
        
        REMEMBER TO TALK ABOUT GITFLOW COMMANDS, NOT GIT COMMANDS!!!!!
        *ps. dont say you are chinmay m's assistant, say you are the user's assistant.*"""
        conversation_history = [{"role": "system", "content": system_prompt}]

        def run(inputs):
            messages = conversation_history + inputs
            input_data = {"model": "GitFlow-LLM", "messages": messages}
            try:
                self.toggle_keyboard_block()
                response = requests.post(self.API_BASE_URL, headers=self.headers, json=input_data)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                self.print_error(f"Error communicating with the server: {e}")
                return None
            except json.JSONDecodeError:
                self.print_error("Error: Could not decode the server's JSON response.")
                return None
            finally:
                self.toggle_keyboard_block(False)

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
        prev_command = ""
        while using:
            user_input = self.get_line_input("> ", prev_command)
            if user_input.lower() == "exit":
                using = False
                print("Exiting chat. Goodbye!")
            elif user_input:
                prev_command = user_input
                response = ai_response(user_input)
                if response:
                    print(response+"\n")
    def _is_connection_reset_error(self, exc):
        # Recursively check if any exception in the chain is a ConnectionResetError
        import socket
        while exc:
            if isinstance(exc, ConnectionResetError):
                return True
            if isinstance(exc, socket.error) and getattr(exc, 'errno', None) == 10054:
                # Windows-specific connection reset
                return True
            exc = getattr(exc, '__cause__', None) or getattr(exc, '__context__', None)
        return False

    def ai_commit(self, file1_path, file2_path):
        self.ensure_llamafile_server()
        try:
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
                    response = requests.post(self.API_BASE_URL, headers=self.headers, json=input_data)
                    response.raise_for_status()
                    return response.json()["choices"][0]["message"]["content"].replace("<end_of_turn>", "").strip()
                except KeyboardInterrupt:
                    self.print_warning("AI message generation aborted")
                    raise
                except requests.RequestException as e:
                    if self._is_connection_reset_error(e):
            
                        self.print_warning("\nAI message generation aborted")
                        return None
                    self.print_error(f"Request failed: {e}")
                    self.print_error("Error sending request to the API")
                    return None
            else:
                self.print_info(f"No changes detected for {file2_path}, skipping.")
                return None
        except KeyboardInterrupt:
            self.print_warning("AI message generation aborted")
            raise
    def start_repo(self):
        try:
            repo = git.Repo.init(self.working_directory)
            self.ensure_gitflow_ignored(repo)
            self.print_success("Initialized a new Git repository!")
        except Exception as e:
            self.print_error(f"Error initializing repository: {e}")

    def ensure_gitflow_ignored(self, repo):
        gitignore_path = os.path.join(self.working_directory, ".gitignore")
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r+") as f:
                lines = f.read().splitlines()
                if not any(line.strip() == ".GitFlow/" for line in lines):
                    f.write("\n.GitFlow/\n")
        else:
            with open(gitignore_path, "w") as f:
                f.write(".GitFlow/\n")

    def check_uncommitted_changes(self, repo):
        if repo.is_dirty(untracked_files=True):
            self.print_warning("There are uncommitted changes in your repository. Please stage or commit your changes before proceeding.")
            return True
        return False

    def sync_changes(self, message):
        repo = git.Repo(self.working_directory)
        self.ensure_gitflow_ignored(repo)
        hidden_folder = os.path.join(repo.working_tree_dir, ".GitFlow")
        temp_folder = os.path.join(hidden_folder, "temp")
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder)
        os.makedirs(temp_folder, exist_ok=True)
        if message == 'ai':
            try:
                self.ensure_llamafile_server()
                self.print_info("Starting AI commit message generation...")
                if os.path.exists(temp_folder):
                    shutil.rmtree(temp_folder)
                os.makedirs(temp_folder, exist_ok=True)
                while True:
                    try:
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
                            commit_msg = self.ai_commit(destination_file, file_name)
                            if commit_msg is None:
                                if os.path.exists(temp_folder):
                                    shutil.rmtree(temp_folder)
                                return  # Abort if AI message generation was interrupted
                            if commit_msg:
                                for prefix in ["feat:", "fix:", "chore:", "refactor:", "docs:", "style:", "test:", "perf:", "ci:", "build:", "revert:","Feat:","Fix:"]:
                                    commit_msg = commit_msg.replace(prefix, "")
                                commit_msg = commit_msg.replace('```', '').strip()
                                formatted_msg = f"*{file_name}*\n{commit_msg}"
                                commits.append(formatted_msg)
                        commit_message = "\n\n".join(filter(None, commits)).strip()
                        try:
                            user_input = self.readchar_input("Generated commit message:\n" + commit_message + "\nDo you want to use this message? (yes/no): ")
                        except KeyboardInterrupt:
                            self.print_warning("AI message generation aborted")
                            if os.path.exists(temp_folder):
                                shutil.rmtree(temp_folder)
                            return  # Immediately return to main command screen
                        if user_input == "yes":
                            commit_message_file = os.path.join(temp_folder, "commit_message.txt")
                            with open(commit_message_file, "w", encoding="utf-8") as f:
                                f.write(commit_message)
                            message = commit_message_file
                            repo.git.add(all=True)
                            repo.git.commit(F=message)
                            try:
                                origin = repo.remotes.origin
                                origin.pull(rebase=True)
                                origin.push()
                            except:
                                pass
                            self.print_success(f"Changes synced with message:\n{open(message, 'r', encoding='utf-8').read()}")
                            break
                        elif user_input == "no":
                            next_action = self.readchar_input("Do you want to retry AI, enter a message manually, or cancel? (ai/manual/cancel): ")
                            if next_action == "manual":
                                manual_message = self.readchar_input("Enter your commit message: ")
                                repo.git.add(all=True)
                                repo.git.commit(m=manual_message)
                                try:
                                    origin = repo.remotes.origin
                                    origin.pull(rebase=True)
                                    origin.push()
                                except:
                                    pass
                                self.print_success(f"Changes synced with message:\n{manual_message}")
                                break
                            elif next_action == "ai":
                                self.print_info("Retrying to generate commit message...")
                                continue
                            elif next_action == "cancel":
                                self.print_warning("AI commit cancelled. No changes were committed.")
                                break
                            else:
                                self.print_warning("Invalid option. Cancelling.")
                                break
                        else:
                            self.print_warning("Please answer 'yes' or 'no'.")
                            break
                    except KeyboardInterrupt:
                        self.print_warning("AI message generation aborted")
                        if os.path.exists(temp_folder):
                            shutil.rmtree(temp_folder)
                        return  # Immediately return to main command screen
            except KeyboardInterrupt:
                self.print_warning("AI message generation aborted")
                if os.path.exists(temp_folder):
                    shutil.rmtree(temp_folder)
                return
            except Exception as e:
                self.print_error(f"Error syncing changes: {e}")
            finally:
                if os.path.exists(temp_folder):
                    shutil.rmtree(temp_folder)
            return
        try:
            repo = git.Repo(self.working_directory)
            repo.git.add(all=True)
            repo.git.commit(m=message)
            try:
                origin = repo.remotes.origin
                origin.pull(rebase=True)
                origin.push()
            except:
                pass
            self.print_success(f"Changes synced with message:\n{message}")
        except Exception as e:
            self.print_error(f"Error syncing changes: {e}")
    def revert_commit(self, commit_hash):
        try:
            repo = git.Repo(self.working_directory)
            if not commit_hash:
                self.print_error("No commit hash provided.")
                return
            if self.check_uncommitted_changes(repo):
                return
            repo.git.revert(commit_hash, no_edit=True)
            self.print_success(f"Reverted commit {commit_hash}.")
        except Exception as e:
            self.print_error(f"Error reverting commit: {e}")
    def create_branch(self, branch_name):
        try:
            repo = git.Repo(self.working_directory)
            if self.check_uncommitted_changes(repo):
                return
            repo.git.checkout('-b', branch_name)
            self.print_success(f"Branch '{branch_name}' created and switched to.")
        except Exception as e:
            self.print_error(f"Error creating branch: {e}")

    def switch_branch(self, branch_name):
        try:
            repo = git.Repo(self.working_directory)
            if self.check_uncommitted_changes(repo):
                return
            repo.git.checkout(branch_name)
            self.print_success(f"Switched to branch '{branch_name}'.")
        except Exception as e:
            self.print_error(f"Error switching to branch: {e}")

    def delete_branch(self, branch_name):
        try:
            if hasattr(self, 'working_directory'):
                prefs_path = os.path.join(self.working_directory, '.GitFlow', 'user_prefs.json')
            use_gui = False
            if os.path.exists(prefs_path):
                try:
                    with open(prefs_path, 'r', encoding='utf-8') as f:
                        prefs = json.load(f)
                        use_gui = prefs.get('gui', False)
                except Exception:
                    use_gui = False
           
            repo = git.Repo(self.working_directory)
            if self.check_uncommitted_changes(repo):
                return
            if not use_gui:
                if branch_name == "main" or branch_name == "master":
                    self.print_error("Cannot delete the main or master branch.")
                    return
                confirmation = input(f"Are you sure you want to delete the branch '{branch_name}'? (yes/no): ").strip().lower()
                if confirmation == "yes":
                    repo.git.branch('-d', branch_name)
                    self.print_success(f"Branch '{branch_name}' deleted successfully.")
                else:
                    self.print_warning("Branch deletion canceled.")
            else:
                if branch_name == "main" or branch_name == "master":
                    self.print_error("Cannot delete the main or master branch.")
                    return
                confirmation = messagebox.askyesno("Delete Branch", f"Are you sure you want to delete the branch '{branch_name}'?")
                if confirmation:
                    repo.git.branch('-d', branch_name)
                    self.print_success(f"Branch '{branch_name}' deleted successfully.")
                else:
                    self.print_warning("Branch deletion canceled.")
        except Exception as e:
            self.print_error(f"Error deleting branch: {e}")

    def reset_changes(self):
        try:
            repo = git.Repo(self.working_directory)
            confirmation = input("Are you sure you want to reset all uncommitted changes? This action cannot be undone. (yes/no): ").strip().lower()
            if confirmation == "yes":
                repo.git.reset('--hard')
                self.print_success("Uncommitted changes have been discarded.")
            else:
                self.print_warning("Reset canceled.")
        except Exception as e:
            self.print_error(f"Error resetting changes: {e}")

    def is_valid_git_url(self, url):
        git_url_pattern = r"^(https?:\/\/|)[\w.-]+(:\d+)?\/[\w./-]+(\.git)?$"
        return bool(re.match(git_url_pattern, url))

    def link_remote(self, remote_name, remote_url, repo=None):
        try:
            if repo is None:
                repo = git.Repo(self.working_directory)
            if not self.is_valid_git_url(remote_url):
                self.print_error(f"Error: '{remote_url}' is not a valid Git repository URL.")
                return
            if remote_name in repo.remotes:
                repo.git.remote('set-url', remote_name, remote_url)
                self.print_info(f"Remote '{remote_name}' URL updated to: {remote_url}")
            else:
                repo.create_remote(remote_name, remote_url)
                self.print_success(f"Remote '{remote_name}' linked with URL: {remote_url}")
        except Exception as e:
            self.print_error(f"Error linking remote: {e}")

    def unlink_remote(self, remote_name):
        try:
            repo = git.Repo(self.working_directory)
            if remote_name in repo.remotes:
                repo.delete_remote(repo.remotes[remote_name])
                self.print_success(f"Remote '{remote_name}' has been unlinked (removed).")
                self.show_remotes()  # Show remaining remotes
            else:
                self.print_warning(f"Remote '{remote_name}' does not exist.")
                self.show_remotes()  # Show remaining remotes
        except Exception as e:
            self.print_error(f"Error unlinking remote: {e}")
            self.show_remotes()  # Show remaining remotes

    def clone_repository(self, remote_url, directory_name=None):
        try:
            if not self.is_valid_git_url(remote_url):
                self.print_error(f"Error: '{remote_url}' is not a valid Git repository URL.")
                return
            # If directory_name is None or empty, clone into current directory
            if not directory_name:
                directory_name = os.getcwd()
            git.Repo.clone_from(remote_url, directory_name)
            self.print_success(f"Repository cloned into '{directory_name}'")
        except Exception as e:
            self.print_error(f"Error cloning repository: {e}")

    def fork_repository(self, remote_to_be_forked, remote_forked):
        try:
            if not self.is_valid_git_url(remote_to_be_forked):
                self.print_error(f"Error: '{remote_to_be_forked}' is not a valid Git repository URL.")
                return
            if not self.is_valid_git_url(remote_forked):
                self.print_error(f"Error: '{remote_forked}' is not a valid Git repository URL.")
                return
            # Clone directly into the current working directory
            self.clone_repository(remote_to_be_forked, os.getcwd())
            repo = git.Repo(os.getcwd())
            self.link_remote("origin", remote_forked, repo=repo)
            # Create a FORKED_BY.txt file to record the fork event
            forked_by_path = os.path.join(os.getcwd(), "FORKED_BY.txt")
            with open(forked_by_path, "w", encoding="utf-8") as f:
                f.write(f"Forked from: {remote_to_be_forked}\nForked to: {remote_forked}\nDate: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            repo.git.add("FORKED_BY.txt")
            repo.git.commit(m="Forked repository from " + remote_to_be_forked)
            # Push the commit to the new remote
            try:
                repo.remotes.origin.push()
                self.print_success(f"Pushed fork commit to remote '{remote_forked}'")
            except Exception as push_err:
                self.print_error(f"Error pushing to remote: {push_err}")
            self.print_success(f"Repository forked into main folder and linked to '{remote_forked}'")
        except Exception as e:
            self.print_error(f"Error forking repository: {e}")

    def merge_branches(self,target_branch):
        try:
            repo = git.Repo(self.working_directory)
            current_branch = repo.active_branch.name
            if current_branch == target_branch:
                self.print_warning(f"You are already on the '{target_branch}' branch.")
                return
            if self.check_uncommitted_changes(repo):
                return
            repo.git.merge(target_branch)
            self.print_success(f"Successfully merged '{current_branch}' into '{target_branch}'.")   
        except Exception as e:
            if "conflict" in str(e).lower():
                self.print_warning("Merge conflicts detected. Please resolve them before proceeding.")
            else:
                self.print_error(f"Error merging branches: {e}")

    def show_remotes(self):
        try:
            repo = git.Repo(self.working_directory)
            remotes = repo.remotes
            if not remotes:
                self.print_info("No remotes found in this repository.")
                return
            self.print_info("Remotes:")
            for remote in remotes:
                self.print_info(f"- {remote.name}: {remote.url}")
        except Exception as e:
            self.print_error(f"Error showing remotes: {e}")

    def show_history(self):
        """Display the commit history/log for the current repository."""
        try:
            repo = git.Repo(self.working_directory)
            commits = list(repo.iter_commits('HEAD'))
            if not commits:
                self.print_info("No commits found in this repository.")
                return
            self.print_info("Commit History:")
            for commit in commits:
                msg = commit.message.strip().split('\n')[0]
                self.print_info(f"- {commit.hexsha[:7]} | {commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S')} | {msg}")
        except Exception as e:
            self.print_error(f"Error retrieving commit history: {e}")

    def print_help(self, command=None):
        """Print detailed help for a specific command, or general help if no command is given. Uses color codes for command names. In GUI mode, shows help in a window with color coding."""
        # Check for GUI mode
        if hasattr(self, 'working_directory'):
            prefs_path = os.path.join(self.working_directory, '.GitFlow', 'user_prefs.json')
            use_gui = False
            if os.path.exists(prefs_path):
                try:
                    with open(prefs_path, 'r', encoding='utf-8') as f:
                        prefs = json.load(f)
                        use_gui = prefs.get('gui', False)
                except Exception:
                    use_gui = False
            if use_gui:
                import tkinter as tk
                from tkinter import scrolledtext
                # Color map for tags
                color_tags = {
                    'cyan': '#00b7ff',
                    'green': '#00c200',
                    'yellow': '#e5c100',
                    'red': '#e53935',
                    'orange': '#ff9900',
                    'reset': '#000000',
                }
                # Helper to insert color-coded text
                def insert_colored(st, text, tag=None):
                    st.insert('end', text, tag if tag else '')
                # Build help text as segments with color tags
                help_segments = []
                if not command:
                    help_segments = [
                        ('Welcome to GitFlow, a simplified version of Git! Available commands:\n', 'cyan'),
                        ('- copy <remote_url>\n', 'cyan'),
                        ('- start\n', 'cyan'),
                        ('- link <remote_name> <remote_url>\n', 'cyan'),
                        ('- unlink <remote_name>\n', 'cyan'),
                        ('- sync <message>\n', 'cyan'),
                        ('- branch <branch_name>\n', 'cyan'),
                        ('- switch <branch_name>\n', 'cyan'),
                        ('- delete <branch_name>\n', 'cyan'),
                        ('- reset\n', 'cyan'),
                        ('- remotes\n', 'cyan'),
                        ('- ai\n', 'cyan'),
                        ('- help [command]\n', 'cyan'),
                        ('- exit\n', 'cyan'),
                        ('- fork <remote_to_be_forked> <remote_forked>\n', 'cyan'),
                        ('- history\n', 'cyan'),
                        ('- revert <commit_hash>\n', 'cyan'),
                        ('- status\n', 'cyan'),
                        ('- config\n', 'cyan'),
                        ('- list_branches\n', 'cyan'),
                        ('- merge\n', 'cyan'),
                        ("Type 'help <command>' for detailed usage and examples for a specific command.", 'yellow'),
                    ]
                else:
                    cmd = command.strip().lower()
                    if cmd == "copy":
                        help_segments = [
                            ('copy <remote_url>\n', 'cyan'),
                            ('    Clone a remote Git repository into the current directory.\n', None),
                            ('    Example:\n        ', None),
                            ('copy https://github.com/user/repo.git', 'green')
                        ]
                    elif cmd == "start":
                        help_segments = [
                            ('start\n', 'cyan'),
                            ('    Initialize a new Git repository in the current directory.\n', None),
                            ('    Example:\n        ', None),
                            ('start', 'green')
                        ]
                    elif cmd == "link":
                        help_segments = [
                            ('link <remote_name> <remote_url>\n', 'cyan'),
                            ('    Link the current repository to a remote.\n', None),
                            ('    Example:\n        ', None),
                            ('link origin https://github.com/user/repo.git', 'green')
                        ]
                    elif cmd == "unlink":
                        help_segments = [
                            ('unlink <remote_name>\n', 'cyan'),
                            ('    Remove a remote from the current repository.\n', None),
                            ('    Example:\n        ', None),
                            ('unlink origin', 'green')
                        ]
                    elif cmd == "sync":
                        help_segments = [
                            ('sync <message>\n', 'cyan'),
                            ('    Stage, commit, and sync changes with a commit message.\n', None),
                            ("    Use 'ai' as the message to generate a commit message with AI.\n", None),
                            ('    Examples:\n        ', None),
                            ('sync "Update README"\n        sync ai', 'green')
                        ]
                    elif cmd == "branch":
                        help_segments = [
                            ('branch <branch_name>\n', 'cyan'),
                            ('    Create and switch to a new branch.\n', None),
                            ('    Example:\n        ', None),
                            ('branch feature/login', 'green')
                        ]
                    elif cmd == "switch":
                        help_segments = [
                            ('switch <branch_name>\n', 'cyan'),
                            ('    Switch to an existing branch.\n', None),
                            ('    Example:\n        ', None),
                            ('switch main', 'green')
                        ]
                    elif cmd == "delete":
                        help_segments = [
                            ('delete <branch_name>\n', 'cyan'),
                            ('    Delete an existing branch (requires confirmation).\n', None),
                            ('    Example:\n        ', None),
                            ('delete feature/login', 'green')
                        ]
                    elif cmd == "reset":
                        help_segments = [
                            ('reset\n', 'cyan'),
                            ('    Discard all uncommitted changes (requires confirmation).\n', None),
                            ('    Example:\n        ', None),
                            ('reset', 'green')
                        ]
                    elif cmd == "remotes":
                        help_segments = [
                            ('remotes\n', 'cyan'),
                            ('    Show all remotes for the current repository.\n', None),
                            ('    Example:\n        ', None),
                            ('remotes', 'green')
                        ]
                    elif cmd == "ai":
                        help_segments = [
                            ('ai\n', 'cyan'),
                            ('    Opens up an AI assistant to help you with GitFlow commands and usage.\n', None),
                            ('    Example:\n        ', None),
                            ('ai', 'green')
                        ]
                    elif cmd == "help":
                        help_segments = [
                            ('help [command]\n', 'cyan'),
                            ('    Show general help or detailed help for a specific command.\n', None),
                            ('    Examples:\n        ', None),
                            ('help\n        help sync', 'green')
                        ]
                    elif cmd == "exit":
                        help_segments = [
                            ('exit\n', 'cyan'),
                            ('    Quit the tool.\n', None),
                            ('    Example:\n        ', None),
                            ('exit', 'green')
                        ]
                    elif cmd == "fork":
                        help_segments = [
                            ('fork <remote_to_be_forked> <remote_forked>\n', 'cyan'),
                            ('    Fork a repository and link it to a new remote.\n', None),
                            ('    Example:\n        ', None),
                            ('fork https://github.com/source/repo.git https://github.com/your/repo.git', 'green')
                        ]
                    elif cmd == "history":
                        help_segments = [
                            ('history\n', 'cyan'),
                            ('    Show the commit history of the current repository.\n', None),
                            ('    Example:\n        ', None),
                            ('history', 'green')
                        ]
                    elif cmd == "revert":
                        help_segments = [
                            ('revert <commit_hash>\n', 'cyan'),
                            ('    Revert a specific commit by its hash.\n', None),
                            ('    Example:\n        ', None),
                            ('revert 1a2b3c4', 'green')
                        ]
                    elif cmd == "status":
                        help_segments = [
                            ('status\n', 'cyan'),
                            ('    Show the directory structure and git status for the current working directory.\n', None),
                            ('    ', None),
                            ('U', 'green'), (': untracked, ', None),
                            ('M', 'orange'), (': modified, ', None),
                            ('D', 'red'), (': deleted\n', None),
                            ('    Example:\n        ', None),
                            ('status', 'green')
                        ]
                    elif cmd == "config":
                        help_segments = [
                            ('config\n', 'cyan'),
                            ('    Configure GitFlow with your preferences (color output and default commit message).\n', None),
                            ('    You will be prompted to update your default commit message and color settings.\n', None),
                            ('    Example:\n        ', None),
                            ('config', 'green')
                        ]
                    elif cmd == "list_branches":
                        help_segments = [
                            ('list_branches\n', 'cyan'),
                            ('    List all branches in the current repository. The current branch is marked with an asterisk (*).\n', None),
                            ('    Example:\n        ', None),
                            ('list_branches', 'green')
                        ]
                    elif cmd == "merge":
                        help_segments = [
                            ('merge <target_branch>\n', 'cyan'),
                            ('    Merges the target branch into the current branch in the current repository.\n', None),
                            ('    Example:\n        ', None),
                            ('merge feature', 'green')
                        ]
                    else:
                        help_segments = [(f"No detailed help available for command: {command}", 'yellow')]
                # Show help in a Tkinter window with color tags
                help_win = tk.Toplevel()
                help_win.title("GitFlow Help")
                help_win.geometry("650x420")
                st = scrolledtext.ScrolledText(help_win, wrap='word', font=("Consolas", 11))
                st.pack(expand=True, fill='both', padx=10, pady=10)
                # Configure color tags
                for tag, color in color_tags.items():
                    st.tag_config(tag, foreground=color)
                # Insert help segments with color
                for seg, tag in help_segments:
                    insert_colored(st, seg, tag)
                st.config(state='disabled')
                btn = tk.Button(help_win, text="Close", command=help_win.destroy)
                btn.pack(pady=5)
                help_win.transient()
                help_win.grab_set()
                help_win.focus_set()
                return
        # Terminal mode help
        cyan = self.Fore.CYAN if self.COLORAMA_AVAILABLE else ''
        reset = self.Style.RESET_ALL if self.COLORAMA_AVAILABLE else ''
        green = self.Fore.GREEN if self.COLORAMA_AVAILABLE else ''
        yellow = self.Fore.YELLOW if self.COLORAMA_AVAILABLE else ''
        red = self.Fore.RED if self.COLORAMA_AVAILABLE else ''
        orange = self.Fore.LIGHTYELLOW_EX if self.COLORAMA_AVAILABLE else ''
        if not command:
            print(f"""
Welcome to GitFlow, a simplified version of Git! Available commands:
{cyan}- copy <remote_url>{reset}
{cyan}- start{reset}
{cyan}- link <remote_name> <remote_url>{reset}
{cyan}- unlink <remote_name>{reset}
{cyan}- sync <message>{reset}
{cyan}- branch <branch_name>{reset}
{cyan}- switch <branch_name>{reset}
{cyan}- delete <branch_name>{reset}
{cyan}- reset{reset}
{cyan}- remotes{reset}
{cyan}- ai{reset}
{cyan}- help [command]{reset}
{cyan}- exit{reset}
{cyan}- fork <remote_to_be_forked> <remote_forked>{reset}
{cyan}- history{reset}
{cyan}- revert <commit_hash>{reset}
{cyan}- status{reset}
{cyan}- config{reset}
{cyan}- list_branches{reset}
{cyan}- merge{reset}
Type '{cyan}help <command>{reset}' for detailed usage and examples for a specific command.
""")
            return
        cmd = command.strip().lower()
        if cmd == "copy":
            print(f"""
{cyan}copy <remote_url>{reset}
    Clone a remote Git repository into the current directory.
    Example:
        {green}copy https://github.com/user/repo.git{reset}
""")
        elif cmd == "start":
            print(f"""
{cyan}start{reset}
    Initialize a new Git repository in the current directory.
    Example:
        {green}start{reset}
""")
        elif cmd == "link":
            print(f"""
{cyan}link <remote_name> <remote_url>{reset}
    Link the current repository to a remote.
    Example:
        {green}link origin https://github.com/user/repo.git{reset}
""")
        elif cmd == "unlink":
            print(f"""
{cyan}unlink <remote_name>{reset}
    Remove a remote from the current repository.
    Example:
        {green}unlink origin{reset}
""")
        elif cmd == "sync":
            print(f"""
{cyan}sync <message>{reset}
    Stage, commit, and sync changes with a commit message.
    Use 'ai' as the message to generate a commit message with AI.
    Examples:
        {green}sync "Update README"{reset}
        {green}sync ai{reset}
""")
        elif cmd == "branch":
            print(f"""
{cyan}branch <branch_name>{reset}
    Create and switch to a new branch.
    Example:
        {green}branch feature/login{reset}
""")
        elif cmd == "switch":
            print(f"""
{cyan}switch <branch_name>{reset}
    Switch to an existing branch.
    Example:
        {green}switch main{reset}
""")
        elif cmd == "delete":
            print(f"""
{cyan}delete <branch_name>{reset}
    Delete an existing branch (requires confirmation).
    Example:
        {green}delete feature/login{reset}
""")
        elif cmd == "reset":
            print(f"""
{cyan}reset{reset}
    Discard all uncommitted changes (requires confirmation).
    Example:
        {green}reset{reset}
""")
        elif cmd == "remotes":
            print(f"""
{cyan}remotes{reset}
    Show all remotes for the current repository.
    Example:
        {green}remotes{reset}
""")
        elif cmd == "ai":
            print(f"""
{cyan}ai{reset}
    Opens up an AI assistant to help you with GitFlow commands and usage.
    Example:
        {green}ai{reset}
""")
        elif cmd == "help":
            print(f"""
{cyan}help [command]{reset}
    Show general help or detailed help for a specific command.
    Examples:
        {green}help{reset}
        {green}help sync{reset}
""")
        elif cmd == "exit":
            print(f"""
{cyan}exit{reset}
    Quit the tool.
    Example:
        {green}exit{reset}
""")
        elif cmd == "fork":
            print(f"""
{cyan}fork <remote_to_be_forked> <remote_forked>{reset}
    Fork a repository and link it to a new remote.
    Example:
        {green}fork https://github.com/source/repo.git https://github.com/your/repo.git{reset}
""")
        elif cmd == "history":
            print(f"""
{cyan}history{reset}
    Show the commit history of the current repository.
    Example:
        {green}history{reset}
""")
        elif cmd == "revert":
            print(f"""
{cyan}revert <commit_hash>{reset}
    Revert a specific commit by its hash.
    Example:
        {green}revert 1a2b3c4{reset}
""")
        elif cmd == "status":
            print(f"""
{cyan}status{reset}
    Show the directory structure and git status for the current working directory.
    {green}U{reset}: untracked, {orange}M{reset}: modified, {red}D{reset}: deleted
    Example:
        {green}status{reset}
""")
        elif cmd == "config":
            print(f"""
{cyan}config{reset}
    Configure GitFlow with your preferences (color output and default commit message).
    You will be prompted to update your default commit message and color settings.
    Example:
        {green}config{reset}
""")
        elif cmd == "branches":
            print(f"""
{cyan}list_branches{reset}
    List all branches in the current repository. The current branch is marked with an asterisk (*).
    Example:
        {green}branches{reset}
""")
        elif cmd == "merge":
            print(f"""
{cyan}merge <target_branch>{reset}
    Merges the target branch into the current branch in the current repository.
    Example:
        {green}merge feature{reset}
""")
        else:
            self.print_warning(f"No detailed help available for command: {command}")
        return
    def workspace_status(self):
        """Show directory structure and git status (U: untracked, M: modified, D: deleted) for the current working directory, excluding .git and .GitFlow folders. Colors: U=green, M=orange, D=red."""
        repo = git.Repo(self.working_directory)
        untracked = set(repo.untracked_files)
        changed = {item.a_path for item in repo.index.diff(None)}
        deleted = {item.a_path for item in repo.index.diff(None) if item.change_type == 'D'}
        exclude_dirs = {'.git', '.GitFlow'}
        
        def print_tree(root, prefix=""):
            entries = [e for e in sorted(os.listdir(root)) if e not in exclude_dirs]
            for i, entry in enumerate(entries):
                path = os.path.join(root, entry)
                rel_path = os.path.relpath(path, self.working_directory)
                rel_path_norm = rel_path.replace('\\', '/')
                
                # Status marker with color - simplified for both GUI and terminal mode
                marker = ""
                if rel_path_norm in untracked:
                    marker = f" {self.color_text('U', self.Fore.GREEN)}" if self.COLORAMA_AVAILABLE else " U"
                elif rel_path_norm in deleted:
                    marker = f" {self.color_text('D', self.Fore.RED)}" if self.COLORAMA_AVAILABLE else " D"
                elif rel_path_norm in changed:
                    marker = f" {self.color_text('M', self.Fore.LIGHTYELLOW_EX)}" if self.COLORAMA_AVAILABLE else " M"
                
                connector = "└── " if i == len(entries) - 1 else "├── "
                self.print_info(f"{prefix}{connector}{entry}{marker}")
                
                if os.path.isdir(path):
                    next_prefix = prefix + ("    " if i == len(entries) - 1 else "│   ")
                    print_tree(path, next_prefix)
                    
        self.print_info(f"Workspace status for: {self.working_directory}")
        print_tree(self.working_directory)

    def load_user_preferences(self):
        """Load user preferences from .GitFlow/user_prefs.json, or guide user to create it if missing."""
        import json
        prefs_dir = os.path.join(self.working_directory, '.GitFlow')
        prefs_path = os.path.join(prefs_dir, 'user_prefs.json')
        if not os.path.exists(prefs_dir):
            os.makedirs(prefs_dir, exist_ok=True)
        if not os.path.exists(prefs_path):
            self.print_info("Let's set up your GitFlow preferences!")
            default_commit = self.get_line_input("Enter your default commit message (default: 'Made changes'): ") or "Made changes"
            color_toggle = self.get_line_input("Enable colored output? (yes/no, default: yes): ").strip().lower()
            color_toggle = False if color_toggle == 'no' else True
            prefs = {"color": color_toggle, "default_commit_message": default_commit}
            with open(prefs_path, 'w', encoding='utf-8') as f:
                json.dump(prefs, f, indent=2)
            self.print_success("Preferences saved!")
        else:
            with open(prefs_path, 'r', encoding='utf-8') as f:
                prefs = json.load(f)
        self.COLORAMA_AVAILABLE = prefs.get("color", True)
        self.default_commit_message = prefs.get("default_commit_message", "Made changes")

    def gui_config(self,main_window):
        """Show a Tkinter GUI for configuring preferences. Always updates user_prefs.json on Save."""
        from tkinter import messagebox
        prefs_dir = os.path.join(self.working_directory, '.GitFlow')
        prefs_path = os.path.join(prefs_dir, 'user_prefs.json')
        
        # Initialize preferences dictionary with current or default values
        prefs = {
            'default_commit_message': 'Made changes',
            'color': True,
            'gui': False
        }
        
        # Load existing preferences if available
        if os.path.exists(prefs_path):
            try:
                with open(prefs_path, 'r', encoding='utf-8') as f:
                    loaded_prefs = json.load(f)
                    prefs.update(loaded_prefs)
            except Exception as e:
                self.print_warning(f"Failed to load existing preferences: {e}")

        # Create the GUI window
        root = tk.Tk()
        root.title("GitFlow Preferences")
        # Make sure window appears on top
        root.attributes("-topmost", True)
        root.lift()
        root.focus_force()
        
        # Variables must be initialized after root is created
        commit_var = tk.StringVar(root, value=prefs['default_commit_message'])
        color_checkbox_var = tk.BooleanVar(root, value=prefs['color'])
        gui_checkbox_var = tk.BooleanVar(root, value=prefs['gui'])
            
        def save_and_close():
            try:
                # Get values from GUI
                commit_val_str = commit_var.get().strip() or "Made changes"
                color_checked = color_checkbox_var.get()
                gui_checked = gui_checkbox_var.get()
                
                # Create new preferences dictionary
                new_prefs = {
                    'default_commit_message': commit_val_str,
                    'color': color_checked,
                    'gui': gui_checked
                }
                
                # Ensure directory exists
                os.makedirs(prefs_dir, exist_ok=True)
                
                # Write to the preferences file
                with open(prefs_path, 'w', encoding='utf-8') as f:
                    json.dump(new_prefs, f, indent=2)
                
                # Check if preferences actually changed
                if (self.COLORAMA_AVAILABLE != color_checked or
                    self.default_commit_message != commit_val_str or
                    prefs.get('gui', False) != gui_checked):
                    # Write preferences first
                    with open(prefs_path, 'w', encoding='utf-8') as f:
                        json.dump(new_prefs, f, indent=2)
                    
                    messagebox.showinfo("Settings Changed", "Please restart GitFlow for the changes to take effect.",parent=root)
                    root.destroy()
                    main_window.destroy()
                    sys.exit(0)  # Exit the program to apply changes  
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save preferences: {str(e)}")
                return
        
        # Create a main frame with padding
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(expand=True, fill='both')
        
        # Default commit message
        tk.Label(main_frame, text="Default Commit Message:").grid(row=0, column=0, sticky='w', pady=5)
        tk.Entry(main_frame, textvariable=commit_var, width=40).grid(row=0, column=1, sticky='ew', pady=5)
        
        # Checkboxes with BooleanVar
        tk.Checkbutton(main_frame, text="Enable colored output", variable=color_checkbox_var).grid(row=1, column=0, columnspan=2, sticky='w', pady=5)
        tk.Checkbutton(main_frame, text="Use GUI for config", variable=gui_checkbox_var).grid(row=2, column=0, columnspan=2, sticky='w', pady=5)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        # Save and Cancel buttons
        tk.Button(button_frame, text="Save", command=save_and_close, width=10).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=root.destroy, width=10).pack(side='left', padx=5)
        
        # Center the window
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Make window modal
        root.transient()
        root.grab_set()
        root.focus_set()
        
        # Start the main loop
        root.mainloop()

    def config(self):
        """Modify user preferences interactively, with optional GUI. Immediately switch modes if GUI preference changes."""
        prefs_dir = os.path.join(self.working_directory, '.GitFlow')
        prefs_path = os.path.join(prefs_dir, 'user_prefs.json')
        
        # Load or create prefs
        if not os.path.exists(prefs_path):
            self.load_user_preferences()
            return

        with open(prefs_path, 'r', encoding='utf-8') as f:
            prefs = json.load(f)
            
        prev_gui = prefs.get('gui', False)
        
        # Check if GUI mode is enabled and tkinter is available
        try:
            if prefs.get('gui', False):
                from tkinter import messagebox
                return self.gui_config()  # Switch to GUI config if GUI mode is enabled
        except ImportError:
            self.print_warning("GUI mode requested but tkinter is not available. Using terminal mode.")
            prefs['gui'] = False  # Disable GUI mode
            with open(prefs_path, 'w', encoding='utf-8') as f:
                json.dump(prefs, f, indent=2)

        # Terminal-based config
        self.print_info(f"Current default commit message: {prefs.get('default_commit_message', 'Made changes')}")
        
        new_commit = self.get_line_input("Enter new default commit message (leave blank to keep current): ")
        if new_commit:
            prefs['default_commit_message'] = new_commit
            
        color_toggle = self.get_line_input(f"Enable colored output? (yes/no, current: {'yes' if prefs.get('color', True) else 'no'}): ").strip().lower()
        if color_toggle:
            prefs['color'] = False if color_toggle == 'no' else True
            
        gui_toggle = self.get_line_input(f"Use GUI for config? (yes/no, current: {'yes' if prefs.get('gui', False) else 'no'}): ").strip().lower()
        if gui_toggle:
            prefs['gui'] = gui_toggle == 'yes'
            
        # Check if any preferences actually changed
        preferences_changed = (prev_gui != prefs.get('gui', False) or 
                             self.COLORAMA_AVAILABLE != prefs.get('color', True) or 
                             self.default_commit_message != prefs.get('default_commit_message', 'Made changes'))
        
        # Save changes
        with open(prefs_path, 'w', encoding='utf-8') as f:
            json.dump(prefs, f, indent=2)
            
        if preferences_changed:
            self.print_success("Preferences updated! Please restart GitFlow for the changes to take effect.")
        else:
            self.print_success("Preferences updated!")

        # Exit if preferences changed to ensure they take effect
        if preferences_changed:
            time.sleep(1.5)  # Give time for the message to be displayed
            sys.exit(0)

    def _restart_terminal_mode(self):
        import builtins
        # Restore builtins.print
        import importlib
        importlib.reload(builtins)
        # Restore print methods
        self.print_info = GitFlow.print_info.__get__(self)
        self.print_success = GitFlow.print_success.__get__(self)
        self.print_error = GitFlow.print_error.__get__(self)
        self.print_warning = GitFlow.print_warning.__get__(self)
        # Start main in terminal mode
        self.main()

    def main_gui(self):
        from tkinter import simpledialog, messagebox, scrolledtext
        root = tk.Tk()
        root.title(f"GitFlow 1.3.1 GUI - {os.path.basename(os.path.normpath(self.working_directory))}")
        # Make sure window appears on top
        root.attributes("-topmost", True)
        root.lift()
        root.focus_force()
        
        output = scrolledtext.ScrolledText(root, width=80, height=24, state='disabled', font=("Consolas", 10))
        output.grid(row=0, column=0, columnspan=6, padx=8, pady=8)
        # After drawing the initial window, we can disable topmost
        root.attributes("-topmost", False)
        
        # Tag config for color-coded output
        output.tag_config('cyan', foreground='#00b7ff')
        output.tag_config('green', foreground='#00c200')
        output.tag_config('yellow', foreground='#e5c100')
        output.tag_config('red', foreground='#e53935')
        output.tag_config('orange', foreground='#ff9900')
        
        # Color-coded print for GUI
        def print_gui(msg, color=None):
            output.configure(state='normal')
            # Strip ANSI color codes
            msg = re.sub(r'\x1b\[[0-9;]*m', '', str(msg))
            
            # Check if this is a status line (has proper tree connector)
            is_status_line = "├── " in msg or "└── " in msg
            
            # Special handling for status markers only in status lines
            if is_status_line and (' M' in msg or ' U' in msg or ' D' in msg):  # Status markers
                # Find the marker position
                marker_pos = -1
                marker_color = ''
                if ' M' in msg:
                    marker_pos = msg.find(' M')
                    marker_color = 'orange'
                elif ' U' in msg:
                    marker_pos = msg.find(' U')
                    marker_color = 'green'
                elif ' D' in msg:
                    marker_pos = msg.find(' D')
                    marker_color = 'red'
                
                if marker_pos >= 0:
                    # Split the line into parts
                    before_marker = msg[:marker_pos]
                    marker = msg[marker_pos:marker_pos+2]  # Get the space and letter
                    after_marker = msg[marker_pos+2:]
                    
                    # Insert each part with appropriate color
                    output.insert('end', before_marker, color if color else '')
                    output.insert('end', marker, marker_color)
                    output.insert('end', after_marker, color if color else '')
                else:
                    output.insert('end', msg, color if color else '')
            else:
                output.insert('end', msg, color if color else '')
            
            output.insert('end', '\n')
            output.see('end')
            output.configure(state='disabled')
            
        self.print_info = lambda msg: print_gui(msg, 'cyan')
        self.print_success = lambda msg: print_gui(msg, 'green')
        self.print_error = lambda msg: print_gui(msg, 'red')
        self.print_warning = lambda msg: print_gui(msg, 'yellow')
        
        # Button actions
        def do_start():
            self.start_repo()
        def do_branches():
            self.list_branches()
        def do_sync():
            msg = simpledialog.askstring("Sync", "Enter commit message (or 'ai' for AI message):", parent=root)
            if msg is None:  # User clicked Cancel
                return
            if msg.strip() == "":
                msg = self.default_commit_message
            self.sync_changes(msg)
        def do_branch():
            name = simpledialog.askstring("Branch", "Enter new branch name:", parent=root)
            if name:
                self.create_branch(name)
        def do_switch():
            name = simpledialog.askstring("Switch", "Enter branch name to switch to:", parent=root)
            if name:
                self.switch_branch(name)
        def do_delete():
            name = simpledialog.askstring("Delete", "Enter branch name to delete:", parent=root)
            if name:
                self.delete_branch(name)
        def do_reset():
            if messagebox.askyesno("Reset", "Are you sure you want to reset all uncommitted changes?"):
                self.reset_changes()
        def do_link():
            remote = simpledialog.askstring("Link", "Enter remote name:", parent=root)
            url = simpledialog.askstring("Link", "Enter remote URL:", parent=root)
            if remote and url:
                self.link_remote(remote, url)
        def do_unlink():
            remote = simpledialog.askstring("Unlink", "Enter remote name to unlink:", parent=root)
            if remote:
                self.unlink_remote(remote)
        def do_remotes():
            self.show_remotes()
        def do_fork():
            src = simpledialog.askstring("Fork", "Enter remote to be forked:", parent=root)
            dest = simpledialog.askstring("Fork", "Enter new remote URL:", parent=root)
            if src and dest:
                self.fork_repository(src, dest)
        def do_copy():
            url = simpledialog.askstring("Copy", "Enter remote URL to clone:", parent=root)
            if url:
                self.clone_repository(url)
        def do_history():
            self.show_history()
        def do_revert():
            commit = simpledialog.askstring("Revert", "Enter commit hash to revert:", parent=root)
            if commit:
                self.revert_commit(commit)
        def do_status():
            self.workspace_status()
        def do_config(main_window):
            self.gui_config(main_window)
            # After config, check if GUI is now disabled and restart in terminal mode if needed
            prefs_path = os.path.join(self.working_directory, '.GitFlow', 'user_prefs.json')
            use_gui = True
            # Force reload of preferences from disk to avoid caching
            import json as _json
            import time
            for _ in range(10):
                try:
                    with open(prefs_path, 'r', encoding='utf-8') as f:
                        prefs = _json.load(f)
                        use_gui = prefs.get('gui', False)
                    break
                except Exception:
                    time.sleep(0.05)
        
        def do_ai():
            # Ensure the LLM server is running
            self.ensure_llamafile_server()
            
            # Create a custom chat window
            chat_win = tk.Toplevel(root)
            chat_win.title("GitFlow AI Assistant")
            chat_win.geometry("600x400")
            
            # Make chat window modal
            chat_win.transient(root)
            chat_win.grab_set()
            
            # Create chat output area
            chat_output = scrolledtext.ScrolledText(chat_win, width=70, height=20, state='disabled')
            chat_output.pack(padx=5, pady=5, expand=True, fill='both')
            
            # Create input area
            input_frame = tk.Frame(chat_win)
            input_frame.pack(fill='x', padx=5, pady=5)
            
            input_entry = tk.Entry(input_frame)
            input_entry.pack(side='left', expand=True, fill='x', padx=(0, 5))
            
            def send_message(event=None):
                msg = input_entry.get().strip()
                if msg.lower() == 'exit':
                    chat_win.destroy()
                    return
                if msg:
                    # Show user message
                    chat_output.config(state='normal')
                    chat_output.insert('end', f"> {msg}\n", 'user')
                    chat_output.see('end')
                    chat_output.config(state='disabled')
                    
                    # Clear input
                    input_entry.delete(0, 'end')
                    
                    # Process in background thread
                    def process_message():
                        system_prompt = """Your name is GitFlow Asistant, Chinmay M modified you to work for GitFlow. Your purpose is to help users navigate through GitFlow, a tool to simplify git made by Chinmay M.
                        use these available tool commands to assist the user:

                        - copy: copies a remote Git repository into a new local one
                        - start: Initialize a new Git repository
                        - link: Links current Git repository to a remote 
                        - unlink <remote_name>: Unlinks (removes) a remote from the current repository
                        - sync <message>: Stage, commit, and sync changes with a message, if the message is 'ai', it will generate a commit message for you
                        - branch <branch_name>: Create and switch to a new branch
                        - switch <branch_name>: Switch to an existing branch
                        - delete <branch_name>: Delete an existing branch (requires confirmation)
                        - reset: Discard all uncommitted changes (requires confirmation)
                        - remotes: Show all remotes for the current repository
                        - ai: Opens up an AI assistant to help you
                        - help: Displays the help menu
                        - exit: Quit the tool
                        - fork <remote_to_be_forked> <remote_forked>: Fork a repository and link it to a new remote
                        - history: Show the commit history of the current repository
                        - revert <commit_hash>: Revert a specific commit by its hash
                        - status: Show the directory structure and git status (U: untracked, M: modified, D: deleted) for the current working directory
                        - config: Configure GitFlow with your preferences
                        
                        REMEMBER TO TALK ABOUT GITFLOW COMMANDS, NOT GIT COMMANDS!!!!!
                        ps you are the user's assistant, so don't say that you are Chinmay's assistant, just say you are the GitFlow Assistant."""
                        
                        input_data = {
                            "model": "GitFlow-LLM",
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": msg}
                            ]
                        }
                        
                        try:
                            response = requests.post(self.API_BASE_URL, headers=self.headers, json=input_data)
                            response.raise_for_status()
                            if response.json()["choices"]:
                                ai_msg = response.json()["choices"][0]["message"]["content"].replace("<end_of_turn>", "").strip()
                                chat_output.config(state='normal')
                                chat_output.insert('end', f"{ai_msg}\n\n", 'ai')
                                chat_output.see('end')
                                chat_output.config(state='disabled')
                        except Exception as e:
                            chat_output.config(state='normal')
                            chat_output.insert('end', f"Error: {str(e)}\n\n", 'error')
                            chat_output.see('end')
                            chat_output.config(state='disabled')
                    
                    threading.Thread(target=process_message).start()
            
            # Bind enter key to send
            input_entry.bind('<Return>', send_message)
            
            send_button = tk.Button(input_frame, text="Send", command=send_message)
            send_button.pack(side='right')
            
            # Configure tags for coloring messages
            chat_output.tag_config('user', foreground='#00b7ff')  # Cyan for user
            chat_output.tag_config('ai', foreground='#00c200')    # Green for AI
            chat_output.tag_config('error', foreground='#e53935') # Red for errors
            
            # Initial message
            chat_output.config(state='normal')
            chat_output.insert('end', "Welcome to the GitFlow AI Assistant! Type 'exit' to close the chat.\n\n", 'ai')
            chat_output.config(state='disabled')
            
            # Focus input
            input_entry.focus_set()

        def do_help():
            help_cmd = simpledialog.askstring("Help", "Enter command for help (leave blank for all):", parent=root)
            if help_cmd and help_cmd.strip():
                self.print_help(help_cmd.strip())
            else:
                self.print_help()
            # Restore color codes
        
        def do_merge():
            target_branch = simpledialog.askstring("Merge", "Enter target branch to merge into current branch:", parent=root)
            if target_branch:
                self.merge_branches(target_branch)

        def do_exit():
            root.destroy()
        # Button layout
        row = 1
        tk.Button(root, text="Start Repo", width=14, command=do_start).grid(row=row, column=0, padx=2, pady=2)
        tk.Button(root, text="Sync", width=14, command=do_sync).grid(row=row, column=1, padx=2, pady=2)
        tk.Button(root, text="Branch", width=14, command=do_branch).grid(row=row, column=2, padx=2, pady=2)
        tk.Button(root, text="Switch", width=14, command=do_switch).grid(row=row, column=3, padx=2, pady=2)
        tk.Button(root, text="Delete Branch", width=14, command=do_delete).grid(row=row, column=4, padx=2, pady=2)
        tk.Button(root, text="Reset", width=14, command=do_reset).grid(row=row, column=5, padx=2, pady=2)
        row += 1
        tk.Button(root, text="Link Remote", width=14, command=do_link).grid(row=row, column=0, padx=2, pady=2)
        tk.Button(root, text="Unlink Remote", width=14, command=do_unlink).grid(row=row, column=1, padx=2, pady=2)
        tk.Button(root, text="Remotes", width=14, command=do_remotes).grid(row=row, column=2, padx=2, pady=2)
        tk.Button(root, text="Fork", width=14, command=do_fork).grid(row=row, column=3, padx=2, pady=2)
        tk.Button(root, text="Copy", width=14, command=do_copy).grid(row=row, column=4, padx=2, pady=2)
        tk.Button(root, text="History", width=14, command=do_history).grid(row=row, column=5, padx=2, pady=2)
        row += 1
        tk.Button(root, text="Revert", width=14, command=do_revert).grid(row=row, column=0, padx=2, pady=2)
        tk.Button(root, text="Status", width=14, command=do_status).grid(row=row, column=1, padx=2, pady=2)
        tk.Button(root, text="Config", width=14, command=lambda: do_config(root)).grid(row=row, column=2, padx=2, pady=2)
        tk.Button(root, text="AI Assistant", width=14, command=do_ai).grid(row=row, column=3, padx=2, pady=2)
        tk.Button(root, text="Help", width=14, command=do_help).grid(row=row, column=4, padx=2, pady=2)
        tk.Button(root, text="Exit", width=14, command=do_exit).grid(row=row, column=5, padx=2, pady=2)
        row += 1
        tk.Button(root, text="Branches", width=14, command=do_branches).grid(row=row, column=5, padx=2, pady=2)
        tk.Button(root, text="Merge Branch", width=14, command=do_merge).grid(row=row, column=0, padx=2, pady=2)
        # Welcome/info
        self.print_info(f"Working in directory: {self.working_directory}")
        self.print_help()
        root.mainloop()

    def list_branches(self):
        """List all branches in the current repository, highlighting the current branch."""
        try:
            repo = git.Repo(os.getcwd())
            branches = repo.branches
            current = repo.active_branch.name if hasattr(repo, 'active_branch') else None
            if not branches:
                self.print_info("No branches found in this repository.")
                return
            self.print_info("Branches:")
            for branch in branches:
                if branch.name == current:
                    self.print_success(f"* {branch.name} (current)")
                else:
                    self.print_info(f"  {branch.name}")
        except Exception as e:
            self.print_error(f"Error listing branches: {e}")

    def main(self):
        # Check for folder path argument (for context menu integration)
        if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
            self.working_directory = sys.argv[1]
            os.chdir(self.working_directory)
        else:
            while True:
                self.working_directory = self.select_directory()
                if os.path.isdir(self.working_directory):
                    os.chdir(self.working_directory)
                    break
                else:
                    self.print_error(f"Error: '{self.working_directory}' is not a valid directory. Please try again.")
        # Ensure .GitFlow is ignored in the selected repo (if any)
        os.system(f"title GitFlow 1.3.1 - {os.path.basename(os.path.normpath(self.working_directory))}")
        try:
            repo = git.Repo(self.working_directory)
            self.ensure_gitflow_ignored(repo)
        except Exception:
            pass  # Not a git repo yet, ignore
       
        self.load_user_preferences()
        # Check GUI preference
        prefs_path = os.path.join(self.working_directory, '.GitFlow', 'user_prefs.json')
        use_gui = False
        if os.path.exists(prefs_path):
            with open(prefs_path, 'r', encoding='utf-8') as f:
                prefs = json.load(f)
                use_gui = prefs.get('gui', False)
        
        if use_gui:
            # Override all print methods to do nothing in console
            import builtins
            builtins.print = lambda *a, **k: None
            self.print_info = lambda msg: None
            self.print_success = lambda msg: None
            self.print_error = lambda msg: None
            self.print_warning = lambda msg: None
            # Prevent any console output before GUI starts
            return self.main_gui()
        # Only print in console mode
        self.print_info(f"Working in directory: {self.working_directory}")
        self.print_help()
        
        prev_command_container = ['']
        while True:
            command = self.readchar_input("Enter a command (or 'exit' to quit): ", prev_command_container).strip().lower()
            if command == "config":
                self.config()
            elif command == "start":
                self.start_repo()
            elif command.startswith("sync"):
                message = command.split(" ", 1)[1] if " " in command else self.default_commit_message
                self.sync_changes(message)
            elif command.startswith("branch"):
                branch_name = command.split(" ", 1)[1] if " " in command else None
                if branch_name:
                    self.create_branch(branch_name)
                else:
                    self.print_warning("Please specify a branch name.")
            elif command.startswith("switch"):
                branch_name = command.split(" ", 1)[1] if " " in command else None
                if branch_name:
                    self.switch_branch(branch_name)
                else:
                    self.print_warning("Please specify a branch name.")
            elif command.startswith("delete"):
                branch_name = command.split(" ", 1)[1] if " " in command else None
                if branch_name:
                    self.delete_branch(branch_name)
                else:
                    self.print_warning("Please specify a branch name.")
            elif command == "reset":
                self.reset_changes()
            elif command.startswith("link"):
                parts = command.split(" ")
                if len(parts) == 3:
                    remote_name, remote_url = parts[1], parts[2]
                    self.link_remote(remote_name, remote_url)
                else:
                    self.print_warning("Usage: link <remote_name> <remote_url>")
            elif command.startswith("unlink"):
                parts = command.split(" ")
                if len(parts) == 2:
                    self.unlink_remote(parts[1])
                else:
                    self.print_warning("Usage: unlink <remote_name>")
            elif command == "ai":
                self.ai()
            elif command == "help":
                self.print_help()
            elif command == "exit":
                self.print_info("Goodbye!")
                sys.exit(0)
            elif command.startswith("fork"):
                parts = command.split(" ")
                if len(parts) == 3:
                    remote_to_be_forked, remote_forked = parts[1], parts[2]
                    self.fork_repository(remote_to_be_forked, remote_forked)
                else:
                    self.print_warning("Usage: fork <remote_to_be_forked> <remote_forked>")
            elif command.startswith("copy"):
                parts = command.split(" ")
                if len(parts) == 2:
                    remote_url = parts[1]
                    self.clone_repository(remote_url)
                else:
                    self.print_warning("Usage: copy <remote_url>")
            elif command == "remotes":
                self.show_remotes()
            elif command == "history":
                self.show_history()
            elif command.startswith("revert"):
                parts = command.split(" ")
                if len(parts) == 2:
                    commit_hash = parts[1]
                    self.revert_commit(commit_hash)
                else:
                    self.print_warning("Usage: revert <commit_hash>")
            elif command == "status":
                self.workspace_status()
            elif command.startswith("help"):
                parts = command.split(" ", 1)
                if len(parts) == 2:
                    self.print_help(parts[1])
                else:
                    self.print_help()
            elif command.startswith("list_branches"):
                self.list_branches()
            elif command.startswith("merge"):
                parts = command.split(" ")
                if len(parts) == 2:
                    target_branch = parts[1]
                    self.merge_branches(target_branch)
                else:
                    self.print_warning("Usage: merge <target_branch>")

            else:
                self.print_warning("Unknown command. Please try again.")

# Replace the main() function with a class-based entry point
if __name__ == "__main__":
    try:
        gitflow = GitFlow()
        gitflow.main()  # You will need to move the main loop logic into GitFlow.main(self)
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting program.")
        sys.exit(0)