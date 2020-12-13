def format_jenkins_server(server):
    parts = server.split("/")
    return f"https://{parts[2]}/"
