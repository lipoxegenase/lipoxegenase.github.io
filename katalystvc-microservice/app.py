
import sqlite3
from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)
DATABASE = 'leads.db'

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
                1 if data['consent'] else 0, # Convert boolean to integer
                data.get('sourcePage'),
                data.get('utmSource'),
                data.get('utmMedium'),
                data.get('utmCampaign'),
                data.get('utmTerm'),
                data.get('utmContent'),
                datetime.now().isoformat()
            )
        )
        conn.commit()
        conn.close()

        # In a real scenario, you would also send emails here
        # For now, we'll just log that it would happen
        print(f"Lead submitted: {data['email']}. Confirmation and notification emails would be sent.")

        return jsonify({'message': 'Lead submitted successfully'}), 200
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # For local development, allow all origins. In production, restrict this.
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True, port=5000)

