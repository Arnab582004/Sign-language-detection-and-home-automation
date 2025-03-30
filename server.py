from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os
import signal

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables to store subprocesses
process = None
serial_output = ""
process_virtual_keyboard = subprocess.Popen(['python', 'virtualkeyboard.py'], cwd=r'c:\python\Handrecognition')
process_sign_language = None

@app.route('/run-hand-tracking', methods=['GET'])
def run_hand_tracking():
    global process
    try:
        if process is None or process.poll() is not None:  # Check if the process is not running
            process = subprocess.Popen(['python', 'test.py'], shell=True)
            return jsonify({"status": "success", "message": "Hand tracking and serial monitor started!"})
        else:
            return jsonify({"status": "error", "message": "Hand tracking is already running!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/stop-hand-tracking', methods=['GET'])
def stop_hand_tracking():
    global process
    try:
        if process is not None and process.poll() is None:  # Check if the process is running
            os.kill(process.pid, signal.SIGTERM)  # Forcefully terminate the process
            process = None
            return jsonify({"status": "success", "message": "Hand tracking and serial monitor stopped!"})
        else:
            return jsonify({"status": "error", "message": "No hand tracking process is running!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/serial-output', methods=['POST'])
def update_serial_output():
    global serial_output
    data = request.json
    serial_output = data.get("fingers_state", "")
    return jsonify({"status": "success"})

@app.route('/get-serial-output', methods=['GET'])
def get_serial_output():
    return jsonify({"serial_output": serial_output})

@app.route('/run-virtual-keyboard', methods=['GET'])
def run_virtual_keyboard():
    global process_virtual_keyboard
    try:
        if process_virtual_keyboard is None or process_virtual_keyboard.poll() is not None:  # Check if the process is not running
            process_virtual_keyboard = subprocess.Popen(['python', 'virtualkeyboard.py'], cwd=r'c:\python\Handrecognition')
            return jsonify({"status": "success", "message": "Virtual Keyboard started!"})
        else:
            return jsonify({"status": "error", "message": "Virtual Keyboard is already running!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/stop-virtual-keyboard', methods=['GET'])
def stop_virtual_keyboard():
    global process_virtual_keyboard
    try:
        if process_virtual_keyboard is not None and process_virtual_keyboard.poll() is None:  # Check if the process is running
            os.kill(process_virtual_keyboard.pid, signal.SIGTERM)  # Terminate the process
            process_virtual_keyboard = None
            return jsonify({"status": "success", "message": "Virtual Keyboard stopped!"})
        else:
            return jsonify({"status": "error", "message": "No Virtual Keyboard process is running!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/run-sign-language', methods=['GET'])
def run_sign_language():
    global process_sign_language
    try:
        if process_sign_language is None or process_sign_language.poll() is not None:  # Check if the process is not running
            process_sign_language = subprocess.Popen(['python', 'handtest.py'], cwd=r'c:\python\Handrecognition')
            return jsonify({"status": "success", "message": "Sign Language Detection started!"})
        else:
            return jsonify({"status": "error", "message": "Sign Language Detection is already running!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/stop-sign-language', methods=['GET'])
def stop_sign_language():
    global process_sign_language
    try:
        if process_sign_language is not None and process_sign_language.poll() is None:  # Check if the process is running
            os.kill(process_sign_language.pid, signal.SIGTERM)  # Terminate the process
            process_sign_language = None
            return jsonify({"status": "success", "message": "Sign Language Detection stopped!"})
        else:
            return jsonify({"status": "error", "message": "No Sign Language Detection process is running!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)