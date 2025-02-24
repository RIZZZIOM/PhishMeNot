import subprocess
import sys
import os

# List of required Python packages
required_packages = [
    "flask", "pyyaml", "jinja2", "datetime", "smtplib"
]

# Function to install missing dependencies
def install_packages():
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install required packages
install_packages()

# Run the Flask app
app_path = os.path.join("web", "app.py")
if os.path.exists(app_path):
    print("Starting Phish Me Not application...")
    subprocess.run([sys.executable, app_path])
else:
    print("Error: app.py not found in the 'web' directory!")
