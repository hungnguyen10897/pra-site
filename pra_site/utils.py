import re

def format_jenkins_server(server):
    parts = server.split("/")
    return f"https://{parts[2]}/"

def get_proper_file_name(origin):
    p = re.compile("[^0-9a-z-_]")
    return p.sub('_', origin.lower())