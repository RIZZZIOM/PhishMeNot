import subprocess
import sys
import os

required_packages = [
    "flask", "pyyaml", "jinja2", "datetime", "smtplib"
]

def install_packages():
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_packages()

app_path = os.path.join("web", "app.py")
if os.path.exists(app_path):
    print("Starting Phish Me Not application...")
    subprocess.run([sys.executable, app_path])
else:
    print("Error: app.py not found in the 'web' directory!")
