from windows_tools.installed_software import get_installed_software

for software in get_installed_software():
    print(f"Name: {software['name']}, Version: {software['version']}, Publisher: {software['publisher']}")

#gmail handling
import requests

def clear_inbox():
    # This is a placeholder function. In a real implementation, you would use the Gmail API to clear the inbox.
    print("Inbox cleared.")
