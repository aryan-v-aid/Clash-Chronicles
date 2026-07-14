import os
import webbrowser
from threading import Timer
from app import app

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
    print("Starting Clash Chronicles Server...")
    print("A new browser window will open automatically in a moment.")

    # Automatically open browser after 1.5 seconds
    Timer(1.5, open_browser).start()

    # Run the server on port 5000 (accessible locally)
    app.run(host='127.0.0.1', port=5000, debug=False)
