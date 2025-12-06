from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv
from email_validator import validate_email, EmailNotValidError

import os
import secrets

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # random secret key each run

# Yahoo Mail SMTP configuration
app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('DEL_EMAIL')
app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD')

mail = Mail(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/send_email', methods=['POST'])
def send_email():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email or not message:
        flash("Please fill in all fields before submitting.", "danger")
        return redirect(url_for('home'))

    try:
        # validate email first
        validate_email(email)

        msg = Message(
            subject=f"New Message from {name}",
            sender=os.getenv('DEL_EMAIL'),
            recipients=[os.getenv('REC_EMAIL')]
        )
        msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        mail.send(msg)

        flash("Your message has been sent successfully!", "success")
    
    except EmailNotValidError:
        flash("Please enter a valid email address.", "danger")

    except Exception as e:
        flash(f"Error sending email: {e}", "danger")

    return redirect(url_for('home'))


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=10000)
