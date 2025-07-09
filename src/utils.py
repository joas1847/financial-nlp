import re

def clean_text(text: str) -> str:
    """    Cleans the input text by removing non informational words such as URLs mentions or special characters.
    Args:
        text (str): The input text to be cleaned.
    Returns:
        str: The cleaned text.
    """
    # Convert text to lower case
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

    # Remove tweet mentions
    text = re.sub(r'<user>', '', text)
    text = re.sub(r'<url>', '', text)

    # Remove special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Replace all whitespace characters with a single space
    text = re.sub(r'\s+', ' ', text)

    # Remove leading and trailing whitespace
    text = text.strip()

    return text
    
import os

from getpass import getpass
from huggingface_hub import login
from huggingface_hub import notebook_login


os.environ["REQUESTS_CA_BUNDLE"] = "/etc/pki/tls/certs/sanofi-ca.crt"
token = getpass("Enter your Hugging Face token: ")
login(token=token)