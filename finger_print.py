from flask import request
import hashlib
import re

def generate_fingerprint():
    user_agent = request.headers.get('User-Agent')
    screen_resolution = request.args.get('resolution')
    browser_info = parse_user_agent(user_agent)
    os_info = parse_os(user_agent)
    screen_size = request.args.get('screen_size')

    fingerprint_string = f'{screen_resolution}|{browser_info}|{os_info}|{screen_size}'

    fingerprint = hashlib.sha256(fingerprint_string.encode()).hexdigest()
    return fingerprint

def parse_user_agent(user_agent):
    # Extract browser name and version from User-Agent string
    browser_regex = r'(?:\s)(\w+)/(.*?)(?:\s|$)'
    matches = re.findall(browser_regex, user_agent)
    browser_info = '|'.join([f'{name}:{version}' for name, version in matches])
    return browser_info

def parse_os(user_agent):
    # Extract operating system information from User-Agent string
    os_regex = r'\((.*?)\)'
    matches = re.findall(os_regex, user_agent)
    os_info = '|'.join(matches)
    return os_info
