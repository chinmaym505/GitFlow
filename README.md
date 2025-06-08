GitFlow
=======

GitFlow is a command-line tool designed to simplify Git repository management. It provides an intuitive interface for common Git operations, reducing complexity for developers.

Features
--------

- Initialize a new Git repository  
- Link a remote Git repository to the local one  
- Clone a remote repository  
- Fork an existing repository and set up a new remote  
- Create, switch, and delete branches  
- Discard uncommitted changes (requires confirmation)  
- Stage, commit, and sync changes with a message  
- AI-powered assistant for commit message generation and Git help  
- View commit history, workspace status, and remotes  
- Configure tool preferences to match user workflows  
- GUI support for users who prefer a visual interface  

Commands
--------

- `start`  
  Initialize a new Git repository  

- `link <remote_name> <remote_url>`  
  Connect a remote repository  

- `copy <remote_url>`  
  Clone an existing repository  

- `fork <remote_to_be_forked> <remote_forked>`  
  Fork a repository and set up a new remote  

- `branch <branch_name>`  
  Create and switch to a new branch  

- `switch <branch_name>`  
  Switch to an existing branch  

- `delete <branch_name>`  
  Delete a branch (requires confirmation)  

- `reset`  
  Discard all uncommitted changes (requires confirmation)  

- `sync <message>`  
  Stage, commit, and sync changes; use `'ai'` for AI-generated commit messages  

- `status`  
  View workspace state (tracked/untracked changes)  

- `history`  
  Display commit history  

- `remotes`  
  View and modify remote repository settings  

- `merge`  
  Merge branches together  

- `revert <commit_hash>`  
  Undo a specific commit by hash  

- `config`  
  Set user preferences  

- `list_branches`  
  List all available branches  

- `gui`  
  Launch the GUI interface  

- `ai`  
  Open the AI-powered assistant  

- `help [command]`  
  Show detailed usage for a specific command  

- `exit`  
  Quit the tool  

Usage
-----

1. Run the tool and enter the directory where you want to work.  
2. Use commands to manage your Git repositories efficiently.  
3. Type `help` at any time for guidance on available commands.  

TODO
----

- [x] Replace HTTP-based AI model with an optimized local AI solution  
- [x] Implement AI-assisted commit messages  
- [x] Colorize all outputs for better readability  
- [x] Add commit history and workspace status commands  
- [x] Improve remote repository management  
- [x] Implement user-configurable settings  
- [x] Enhance help documentation for individual commands  
- [x] Introduce GUI support for users who prefer visual interfaces
- [ ] Add AI merging
- [ ] Add AI merge conflict resoulution
- [ ] Add diff command
- [ ] Add AI branch naming
      

Notes
-----

The GitFlow LLM LLamafile was too large to be uploaded to GitHub—sorry!  
