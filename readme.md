# DayZ Server Control Panel

[![License](https://img.shields.io/badge/License-Free_to_use-green.svg)](https://opensource.org/licenses/Free-to-use)

This project provides a web-based control panel for managing your DayZ server. It allows you to control server operations, monitor players and mods, and edit server configuration files through a user-friendly web interface.

## Features

- **Server Management**: Start, stop, and restart your DayZ server instance.
- **Mod Management**: View a list of installed server mods.
- **Player Monitoring**: See a list of currently online players in real-time.
- **Configuration Editing**: Edit key server configuration settings directly through the web interface.
- **Real-time Updates**: Utilizes Socket.IO for live updates on server status, online players, and mods.
- **Dark Mode**: Includes a dark mode for improved user experience in low-light environments.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.6+**: Python is required to run the Flask application. You can download it from [python.org](https://www.python.org/downloads/).
- **Flask**: Flask is a Python web framework used to build the control panel. Install it using pip:
  ```bash
  pip install flask flask-socketio
  ```
- **DayZ Server**: You need to have a DayZ server installation. This control panel is designed to manage a locally hosted DayZ server.

## Setup

1. **Clone the repository**:
   ```bash
   git clone [repository-url]
   cd dayz-server-control-panel
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Ensure `requirements.txt` is created with `flask` and `flask-socketio`)*

3. **Configure Server Paths**:
   - Open `app.py` in a text editor.
   - Modify the following configuration variables in the `# --- Configuration ---` section to match your DayZ server setup:
     - `SERVER_LOCATION`: Path to your DayZ Server installation directory (e.g., `"C:\Program Files (x86)\Steam\steamapps\common\DayZServer"`).
     - `SERVER_BATCH_PATH`: Path to your server start batch file (e.g., `os.path.join(SERVER_LOCATION, "start.bat")`).
     - `MODS_DIR`: Path to your server mods directory. If mods are in the DayZServer root, set to `SERVER_LOCATION`.
     - `ONLINE_PLAYERS_LOG`: Path to the server log file that records player connections (e.g., `os.path.join(SERVER_LOCATION, "Profiles", "server.log")`).
     - `CONFIG_FILE`: Path to your `serverDZ.cfg` configuration file (e.g., `os.path.join(SERVER_LOCATION, "serverDZ.cfg")`).

4. **Run the Control Panel**:
   ```bash
   python app.py
   ```

5. **Access the Web Interface**:
   - Open your web browser and go to `http://127.0.0.1:5000`.

## Configuration

- **`app.py`**: Contains the Flask application logic, server path configurations, and backend routes.
- **`templates/index.html`**:  HTML template for the web interface, using Bootstrap and Tailwind CSS for styling, and jQuery and Socket.IO for dynamic content.
- **`start.bat`**: Example batch file to start your DayZ server (you may need to customize this based on your server setup).
- **`serverDZ.cfg`**: DayZ server configuration file (path should be configured in `app.py`).
- **`profiles/server.log`**: Server log file containing player connection information (path should be configured in `app.py`).

## Troubleshooting

- **"Error reading player log"**:
  - Ensure the `ONLINE_PLAYERS_LOG` path in `app.py` is correct.
  - Verify that the DayZ server is configured to generate `server.log` in the specified profiles directory. Check your server startup parameters and `serverDZ.cfg` for logging configurations.
  - Make sure the `profiles` directory exists in your DayZ server installation folder and that the `server.log` file is present and being updated when players connect.
- **Players or Mods not showing up**:
  - Double-check the paths for `MODS_DIR` and `ONLINE_PLAYERS_LOG` in `app.py`.
  - Ensure that mods are correctly installed in the `MODS_DIR` and that the server is loading them properly (check server logs for mod loading errors).
  - For player lists, confirm that `server.log` contains entries like `"Player connected: ..."` and that the log parsing logic in `app.py` correctly extracts player names from these entries.
- **Server commands not working**:
  - Verify that `SERVER_BATCH_PATH` points to the correct `start.bat` or server executable script.
  - Check if the DayZ server executable (`DayZServer_x64.exe`) is in the location specified by `SERVER_LOCATION`.
  - Ensure that the user running the control panel has the necessary permissions to execute server commands and access server files.

## License

This project is free to use.

## Contributing

Contributions are welcome! Please feel free to submit pull requests to improve the project, add new features, or fix bugs. For major changes, please open an issue first to discuss what you would like to change.

---

&copy; 2025 Free To Use