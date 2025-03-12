import os
import re
import subprocess
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asd2ad2a'
socketio = SocketIO(app)

# --- Configuration (adjust these paths as needed) ---
SERVER_LOCATION = r"C:\Program Files (x86)\Steam\steamapps\common\DayZServer"
SERVER_BATCH_PATH = os.path.join(SERVER_LOCATION, "start.bat")  # Adjust if needed
MODS_DIR = SERVER_LOCATION
ONLINE_PLAYERS_LOG = os.path.join(SERVER_LOCATION, "profiles", "server.log")
CONFIG_FILE = os.path.join(SERVER_LOCATION, "serverDZ.cfg")  # The config file to edit

def parse_config_file(filepath):
    """Parse config file into a dictionary of key-value pairs."""
    config = {}
    with open(filepath, 'r') as f:
        file_content = f.read() # Read the entire file content
        # print("Raw file content read from serverDZ.cfg:\n", file_content) # REMOVED LOG
        for line in file_content.splitlines(): # Iterate over lines
            line = line.strip()
            # Skip empty lines or comments (assuming comments start with //)
            if not line or line.startswith("//"):
                continue
            # Match pattern: key = value; or key = value // comment
            match = re.match(r'^(\S+)\s*=\s*([^;]+)(?:;)?(?:\s*\/\/.*)?$', line)
            if match:
                key = match.group(1)
                value = match.group(2).strip()
                config[key] = value
    print("Parsed config:", config) # ADDED LOGGING
    return config

def rebuild_config_file(config):
    """Rebuild config file string from a dictionary."""
    lines = []
    for key, value in config.items():
        lines.append(f"{key} = {value};")
    return "\n".join(lines)

def background_thread():
    """Send real-time updates (online players and mods) every 5 seconds."""
    while True:
        players = []
        try:
            with open(ONLINE_PLAYERS_LOG, 'r') as log_file:
                for line in log_file:
                    if "Player connected:" in line:
                        player = line.split("Player connected:")[-1].strip()
                        players.append(player)
        except Exception as e:
            print(f"Error reading player log: {e}") # ADDED ERROR LOGGING
            players = ["Error reading log"]
        
        try:
            mods = os.listdir(MODS_DIR)
        except Exception as e:
            print(f"Error listing mods: {e}")
            mods = []
        
        socketio.emit('update_data', {'players': players, 'mods': mods}, namespace='/status')
        socketio.sleep(5)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_server():
    try:
        subprocess.Popen([SERVER_BATCH_PATH], shell=True)
        return jsonify({'status': 'Server starting...'})
    except Exception as e:
        return jsonify({'status': 'Error starting server', 'error': str(e)})

@app.route('/stop', methods=['POST'])
def stop_server():
    try:
        subprocess.call("taskkill /im DayZServer_x64.exe /F", shell=True)
        return jsonify({'status': 'Server stopped.'})
    except Exception as e:
        return jsonify({'status': 'Error stopping server', 'error': str(e)})

@app.route('/restart', methods=['POST'])
def restart_server():
    stop_server()  # Stop server first
    subprocess.Popen([SERVER_BATCH_PATH], shell=True)
    return jsonify({'status': 'Server restarted.'})

@app.route('/listmods', methods=['GET'])
def list_mods():
    try:
        mods = os.listdir(MODS_DIR)
        return jsonify({'mods': mods})
    except Exception as e:
        return jsonify({'status': 'Error listing mods', 'error': str(e)})

@app.route('/onlineplayers', methods=['GET'])
def online_players():
    try:
        players = []
        with open(ONLINE_PLAYERS_LOG, 'r') as log_file:
            for line in log_file:
                if "Player connected:" in line:
                    player = line.split("Player connected:")[-1].strip()
                    players.append(player)
        return jsonify({'players': players})
    except Exception as e:
        return jsonify({'status': 'Error reading online players', 'error': str(e)})

# --- Config Editing Endpoints ---

@app.route('/get_config', methods=['GET'])
def get_config():
    try:
        config_dict = parse_config_file(CONFIG_FILE)
        raw_config_content = ""
        with open(CONFIG_FILE, 'r') as f:
            raw_config_content = f.read()
        return jsonify({'config': config_dict, 'raw_config': raw_config_content})
    except Exception as e:
        return jsonify({'status': 'Error reading config', 'error': str(e)})

@app.route('/save_config', methods=['POST'])
def save_config():
    try:
        new_config = request.json.get('config')
        if not isinstance(new_config, dict):
            return jsonify({'status': 'Invalid data format'})
        # Rebuild config file content and save it
        new_content = rebuild_config_file(new_config)
        with open(CONFIG_FILE, 'w') as f:
            f.write(new_content)
        return jsonify({'status': 'Config saved successfully'})
    except Exception as e:
        return jsonify({'status': 'Error saving config', 'error': str(e)})

@socketio.on('connect', namespace='/status')
def handle_connect():
    emit('update_data', {'players': [], 'mods': []})

if __name__ == '__main__':
    socketio.start_background_task(target=background_thread)
    socketio.run(app, debug=True)
