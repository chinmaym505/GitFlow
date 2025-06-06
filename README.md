# GitFlow

GitFlow is a command-line tool designed to simplify the process of managing Git repositories. It provides a user-friendly interface for common Git operations, making it easier for developers to work with their code.

## Features

- Initialize a new Git repository
- Link a remote Git repository to the local one
- Clone a remote Git repository
- Fork a repository and link it to a new remote
- Create and switch to a new branch
- Switch to an existing branch
- Delete an existing branch (requires confirmation)
- Discard all uncommitted changes (requires confirmation)
- Stage, commit, and sync changes with a message
- Interactive AI assistant for GitFlow help and commits

## Commands

- `start`  
  Initialize a new Git repository

- `link <remote_name> <remote_url>`  
  Link a remote Git repository to the local one

- `copy <remote_url>`  
  Clone a remote Git repository

- `fork <remote_to_be_forked> <remote_forked>`  
  Fork a repository and link it to a new remote

- `branch <branch_name>`  
  Create and switch to a new branch

- `switch <branch_name>`  
  Switch to an existing branch

- `delete <branch_name>`  
  Delete an existing branch (requires confirmation)

- `reset`  
  Discard all uncommitted changes (requires confirmation)

- `sync <message>`  
  Stage, commit, and sync changes with a message, if the message is 'ai', AI will generate a commit message for you

- `ai`  
  Opens the interactive AI assistant for GitFlow help

- `help`  
  Displays the help menu

- `exit`  
  Quit the tool

## Usage

1. Run the tool and enter the directory you want to work in.
2. Use the commands above to manage your Git repositories.
3. Type `help` at any time to see the list of available commands.

**TO DO**
------------
- [x] Make an AI model to replace http request one
- [x] Add AI commits
- [x] COLORIZE EVERYTHING
- [x] Add commit log/history command
- [x] Add workspace status command
- [x] View and modify remotes commands
- [x] Config command for user preferences
- [x] Update help command for each individual command
- [x] Add gui command for users who prefer gui



**Notes**
------------
The GitFlow LLM LLamafile was too big to be uploaded to GitHub, sorry!
