"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['menu.py']
DATA_FILES = ['./icon.png']
APP_NAME = 'QuickIR'
OPTIONS = {
'includes': ['webDriver', 'jpholiday','BeautifulSoup','requests'],
    'argv_emulation': False,
    'iconfile': 'icon.icns',
    'plist': {
        'LSUIElement': True    },
    'packages': ['rumps','webDriver', 'jpholiday','BeautifulSoup','requests',"datetime",'re'],
}
setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
