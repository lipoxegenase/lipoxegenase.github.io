import sqlite3
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DATABASE = 'leads.db'

# Email configuration - these should be set as environment variables
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
EMAIL_USER = os.getenv('EMAIL_USER', 'support@katalystvc.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')  # App password for Gmail
INTERNAL_EMAIL = os.getenv('INTERNAL_EMAIL', 'support@katalystvc.com')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            company TEXT,
            role TEXT,
            phone TEXT,
            topic TEXT NOT NULL,
            notes TEXT,
            consent INTEGER NOT NULL,
            source_page TEXT,
            utm_source TEXT,
            utm_medium TEXT,
            utm_campaign TEXT,
            utm_term TEXT,
            utm_content TEXT,
            submission_time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def send_email(to_email, subject, body, is_html=False):
    """Send an email using SMTP"""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        
        if is_html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_USER, to_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

def get_confirmation_email_template(first_name, topic):
    """Generate confirmation email for the user"""
    topic_mapping = {
        'infra': 'AI-Ready Infrastructure Audit',
        'fhir': 'FHIR/TEFCA 90-Day Sprint'
    }
    
    topic_display = topic_mapping.get(topic, topic)
    download_link = f"https://katalystvc.com/downloads/{topic}-brief.html"
    
    subject = "Your KatalystVC Inquiry Has Been Received - What's Next?"
    
    body = f"""Dear {first_name},

Thank you for reaching out to KatalystVC. We've successfully received your inquiry regarding {topic_display}.

We appreciate your interest in our specialized technical consulting services. Our team is currently reviewing your submission and will get back to you within 24-48 business hours to schedule your 20-minute diagnostic session.

In the meantime, you can access your requested marketing brief here:
{download_link}

We look forward to connecting with you and exploring how KatalystVC can help you achieve your technical objectives with tight, efficient, and smart solutions.

Best regards,

The KatalystVC Team
support@katalystvc.com"""
    
    return subject, body

def get_internal_notification_template(lead_data):
    """Generate internal notification email for the team"""
    subject = f"NEW KatalystVC Lead: {lead_data['first_name']} {lead_data['last_name']} - {lead_data['topic']}"
    
    body = f"""Hello Team,

A new lead has been submitted via the KatalystVC website. Please find the details below:

**Lead Information:**
• Name: {lead_data['first_name']} {lead_data['last_name']}
• Email: {lead_data['email']}
• Company: {lead_data.get('company', 'N/A')}
• Role: {lead_data.get('role', 'N/A')}
• Phone: {lead_data.get('phone', 'N/A')}
• Topic of Interest: {lead_data['topic']}
• Notes/Message: {lead_data.get('notes', 'N/A')}
• Consent to Contact: {'Yes' if lead_data['consent'] else 'No'}

**Tracking Information:**
• Submission Date: {lead_data['submission_time']}
• Source Page: {lead_data.get('source_page', 'N/A')}
• UTM Source: {lead_data.get('utm_source', 'N/A')}
• UTM Medium: {lead_data.get('utm_medium', 'N/A')}
• UTM Campaign: {lead_data.get('utm_campaign', 'N/A')}
• UTM Term: {lead_data.get('utm_term', 'N/A')}
• UTM Content: {lead_data.get('utm_content', 'N/A')}

**Action Required:**
• Follow up with the lead within 24-48 business hours.
• Lead ID in database: {lead_data.get('id', 'TBD')}

Best regards,

KatalystVC Automated System"""
    
    return subject, body

# Initialize the database when the app starts
with app.app_context():
    init_db()

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    data = request.get_json()

    required_fields = ['firstName', 'lastName', 'email', 'topic', 'consent']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO leads (
                first_name, last_name, email, company, role, phone, topic, notes, consent,
                source_page, utm_source, utm_medium, utm_campaign, utm_term, utm_content, submission_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data['firstName'],
                data['lastName'],
                data['email'],
                data.get('company'),
                data.get('role'),
                data.get('phone'),
                data['topic'],
                data.get('notes'),
                1 if data['consent'] else 0,
                data.get('sourcePage'),
                data.get('utmSource'),
                data.get('utmMedium'),
                data.get('utmCampaign'),
                data.get('utmTerm'),
                data.get('utmContent'),
                datetime.now().isoformat()
            )
        )
        
        # Get the ID of the inserted record
        lead_id = cursor.lastrowid
        conn.commit()
        conn.close()

        # Prepare lead data for email templates
        lead_data = {
            'id': lead_id,
            'first_name': data['firstName'],
            'last_name': data['lastName'],
            'email': data['email'],
            'company': data.get('company'),
            'role': data.get('role'),
            'phone': data.get('phone'),
            'topic': data['topic'],
            'notes': data.get('notes'),
            'consent': data['consent'],
            'source_page': data.get('sourcePage'),
            'utm_source': data.get('utmSource'),
            'utm_medium': data.get('utmMedium'),
            'utm_campaign': data.get('utmCampaign'),
            'utm_term': data.get('utmTerm'),
            'utm_content': data.get('utmContent'),
            'submission_time': datetime.now().isoformat()
        }

        # Send confirmation email to user
        if EMAIL_PASSWORD:  # Only send emails if credentials are configured
            conf_subject, conf_body = get_confirmation_email_template(data['firstName'], data['topic'])
            user_email_sent = send_email(data['email'], conf_subject, conf_body)
            
            # Send internal notification email
            int_subject, int_body = get_internal_notification_template(lead_data)
            internal_email_sent = send_email(INTERNAL_EMAIL, int_subject, int_body)
            
            print(f"Lead {lead_id} submitted. User email sent: {user_email_sent}, Internal email sent: {internal_email_sent}")
        else:
            print(f"Lead {lead_id} submitted. Email credentials not configured - emails not sent.")

        return jsonify({
            'message': 'Lead submitted successfully',
            'lead_id': lead_id
        }), 200
        
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/leads', methods=['GET'])
def get_leads():
    """Get all leads from the database (for admin purposes)"""
    try:
        conn = get_db_connection()
        leads = conn.execute('SELECT * FROM leads ORDER BY submission_time DESC').fetchall()
        conn.close()
        
        leads_list = []
        for lead in leads:
            leads_list.append(dict(lead))
        
        return jsonify(leads_list), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

if __name__ == '__main__':
    print("KatalystVC CRM Microservice starting...")
    print(f"Database: {DATABASE}")
    print(f"Email configured: {'Yes' if EMAIL_PASSWORD else 'No (set EMAIL_PASSWORD environment variable)'}")
    app.run(debug=True, host='0.0.0.0', port=5000)
