from PyInstaller.__main__ import run

run([
    'gitFlow.py',
    '--onefile',  # Package as a single executable
    '--console',  # Ensure it runs in Terminal
    '--name=gitFlow'  # Name the final binary
])
