#!/usr/bin/env python3
"""Development server runner for TraceSpec"""

import subprocess
import sys
import os

def main():
    """Run the development server with debug mode enabled"""
    try:
        # Check if running from the right directory
        if not os.path.exists('app.py'):
            print("Error: app.py not found. Please run from the project root directory.")
            sys.exit(1)

        # Run the app with debug mode
        cmd = [sys.executable, 'app.py', '--debug', '--port=5000']
        print(f"Starting TraceSpec development server...")
        print(f"Running: {' '.join(cmd)}")
        print(f"Visit: http://localhost:5000")
        print("-" * 50)

        subprocess.run(cmd)

    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
