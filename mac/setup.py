from setuptools import setup
import os

APP = [os.path.join("mac", "gitFlow.py")]  # Adjust for new folder
OPTIONS = {
    'argv_emulation': True,
    'packages': ['requests', 'gitpython']
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
