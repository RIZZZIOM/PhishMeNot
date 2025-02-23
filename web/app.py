from flask import Flask, render_template, jsonify, request
from config import get_smtp_settings, get_port_forwarding_settings, save_user_settings
import smtplib
from jinja2 import Environment, FileSystemLoader
import os
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
# Define a separate Jinja2 environment for phishing templates
PHISHING_TEMPLATE_FOLDER = os.path.join(os.path.dirname(__file__), "backend", "templates")
phishing_env = Environment(loader=FileSystemLoader(PHISHING_TEMPLATE_FOLDER))

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
    template_file = f"{template_name}.html"

    # Ensure phishing template exists
    template_path = os.path.join(PHISHING_TEMPLATE_FOLDER, template_file)
    if not os.path.exists(template_path):
        return "Template not found", 404

    # Render phishing template using the separate Jinja environment
    template = phishing_env.get_template(template_file)
    return template.render()

@app.route("/api/host-template", methods=["POST"])
def host_template():
    try:
        data = request.json
        template_name = data.get("template", "").strip()

        if not template_name:
            return jsonify({"error": "Template name is required"}), 400

        # Generate the phishing link
        phishing_link = f"http://127.0.0.1:5000/phish/{template_name}"

        return jsonify({"message": "Template hosted successfully!", "link": phishing_link})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API Endpoint to Send Campaign Emails
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

        return jsonify({"message": "Campaign email sent successfully!", "sent_to": recipients})

    except smtplib.SMTPAuthenticationError:
        return jsonify({"error": "SMTP authentication failed. Use an App Password if using Gmail."}), 401
    except smtplib.SMTPException as e:
        return jsonify({"error": f"SMTP error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

app.run(debug=True)