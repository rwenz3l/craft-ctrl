from flask import Flask
import subprocess

app = Flask(__name__)
server = None

# todo: # check if another server independent from this app is running on the machine
def server_is_running():
    global server
    if server is None:
        return False
    else:
        return True

@app.route("/")
def index():
    return """
    <html>
    <head>
    <title>Craft-Ctl</title>
    </head>
    <body>
    <form action="/start" method="post">
    <button type="submit">Start Server</button>
    </form>
    <form action="/stop" method="post">
    <button type="submit">Stop Server</button>
    </form>
    </body>
    </html>
    """

# Start MC Server
@app.route("/start", methods=['POST'])
def start_server():
    global server
    if server_is_running():
        return "Server already started!"
    else:
        print("Starting Minecraft Server..:")
        server = subprocess.Popen(["java", "-Xmx1024M", "-Xms1024M", "-jar", "server.jar", "nogui"], stdin=subprocess.PIPE, cwd="craft")
        return """
        Server starting..!
        <a href="/status">Show Status</a>
        """

@app.route("/stop", methods=['POST'])
def stop_server():
    global server
    if server_is_running():
        # send "stop" to server
        server.communicate(input=b'stop\n')[0]
        server = None
        return """
        Server stopped!
        <a href="/">Back</a>
        """
    else:
        return """
        Server is not running!
        """


@app.route("/status", methods=['GET'])
def server_status():
    if server_is_running():
        return "Server is running"
    else:
        return "Server is not running"

app.run(host='0.0.0.0', port=8080)