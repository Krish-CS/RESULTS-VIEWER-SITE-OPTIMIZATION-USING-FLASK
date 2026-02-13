from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, abort
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'mysecret')  # set SECRET_KEY in Render env for production

users = {
    "KRISH": {
        "name": "KRISH",
        "reg_no": "KRISH",
        "primary_email": "krish@gmail.com",
        "secondary_email": "krish@gmail.com",
        "password": "KRISH",
        "pdf": "k.pdf"
    },
    "KEERTHI07": {
        "name": "KEERTHIESWAR V",
        "reg_no": "8115U23CS045",
        "primary_email": "keerthieswar07@gmail.com",
        "secondary_email": "i2323@krce.ac.in",
        "password": "Keerthi7",
        "pdf": "KAI-CS45.pdf",
        "certificate_id": "KAI2026045"
    },
    "SABARI_THE_MASS": {
        "name": "SABARIVASAN M",
        "reg_no": "8115U23AD048",
        "primary_email": "sabarimayilvaganam2005@gmail.com",
        "secondary_email": "a2338@krce.ac.in",
        "password": "Sabari@2005",
        "pdf": "KAI-AD48.pdf"
    },
    "HARISH SKH": {
        "name": "KANNAN HARISH S",
        "reg_no": "8115U23CS043",
        "primary_email": "kannanharishtheking10@gmail.com",
        "secondary_email": "kannanharish582@gmail.com",
        "password": "Harishmi45",
        "pdf": "KAI-CS43.pdf",
        "certificate_id": "KAI2026043"
    },
    "KADHI": {
        "name": "AADHIKESAV A",
        "reg_no": "8115U23CS001",
        "primary_email": "aadhikesav2006@gmail.com",
        "secondary_email": "Aadhikesav07@gmail.com",
        "password": "Aadhikesav",
        "pdf": "KAI-CS01.pdf",
        "certificate_id": "KAI2026001"
    },
    "ARON_JONATH_16": {
        "name": "ARON JONATH A",
        "reg_no": "8115U23CS016",
        "primary_email": "aronjonath0807@gmail.com",
        "secondary_email": "aronjonath0807@gmail.com",
        "password": "zxcvbnm",
        "pdf": "KAI-CS16.pdf",
        "certificate_id": "KAI2026016"
    },
    "A.AKASH_RCB": {
        "name": "AAKASH A",
        "reg_no": "8115U23CS007",
        "primary_email": "a78154111@gmail.com",
        "secondary_email": "h2304@krce.ac.in",
        "password": "asdfghjkl",
        "pdf": "KAI-CS07.pdf",
        "certificate_id": "KAI2026007"
    },
    "MUTHUKARUPPAN P": {
        "name": "MUTHUKARUPPAN P",
        "reg_no": "8115U23CS069",
        "primary_email": "muthucs069@gmail.com",
        "secondary_email": "muthucs069@gmail.com",
        "password": "123@m12345",
        "pdf": "KAI-CS69.pdf",
        "certificate_id": "KAI2026069"
    },
    "ARAVINTH": {
        "name": "ARAVINTH C",
        "reg_no": "8115U23CS015",
        "primary_email": "aravinth2316@gmail.com",
        "secondary_email": "aravinthpk7@gmail.com",
        "password": "aravinth2316",
        "pdf": "KAI-CS15.pdf",
        "certificate_id": "KAI2026015"
    },
    "ANTONY_GODWIN": {
        "name": "ANTONY GODWIN S",
        "reg_no": "8115U23CS011",
        "primary_email": "antonygodwin08@gmail.com",
        "secondary_email": "",
        "password": "",
        "pdf": "KAI-CS11.pdf",
        "certificate_id": "KAI2026011"
    },
    "MADHUBALA_G": {
        "name": "MADHUBALA G",
        "reg_no": "8115U23CS057",
        "primary_email": "madhubala1234bala@gmail.com",
        "secondary_email": "",
        "password": "",
        "pdf": "KAI-CS57.pdf",
        "certificate_id": "KAI2026057"
    }
}

@app.route('/')
def home():
    return render_template('login_options.html')


@app.route('/login/<method>', methods=['GET', 'POST'])
def login(method):
    # remember last selected method so /back can return here
    session['last_method'] = method

    # Only allow 'regno' (Register Number) and 'primary' (Email) login methods
    if method == 'regno':
        label = 'Register Number'
    elif method == 'primary':
        label = 'Email'
    else:
        abort(404)

    if request.method == 'POST':
        identifier = request.form['identifier'].strip()
        # password is optional for regno/primary
        password = request.form.get('password', '').strip()

        for username, data in users.items():
            # Register Number and Email are passwordless per new requirement
            if method == 'regno' and data.get('reg_no', '').strip().upper() == identifier.upper():
                session['user'] = username
                return redirect(url_for('results'))
            elif method == 'primary' and data.get('primary_email', '').strip().lower() == identifier.lower():
                session['user'] = username
                return redirect(url_for('results'))

            # Fallback (not expected since only regno/primary are allowed)
            if password and data.get('password') == password:
                session['user'] = username
                return redirect(url_for('results'))

        return render_template('invalid.html')
    return render_template('login_form.html', method=label, raw_method=method)

@app.route('/results')


def results():
    if 'user' in session:
        user = session['user']
        data = users[user]
        regno = data.get('reg_no', '').strip()
        name = data.get('name', '')
        cert_id = data.get('certificate_id', '')
        code = regno.upper()[-5:]
        cert_filename = f"{code}.jpeg"
        marksheet_filename = f"{code}.pdf"
        cert_path = os.path.join(os.getcwd(), 'CERTIFICATES', cert_filename)
        marksheet_path = os.path.join(os.getcwd(), 'MARKSHEETS', marksheet_filename)
        if not os.path.exists(cert_path) and not os.path.exists(marksheet_path):
            return render_template('invalid.html')
        return render_template('certificate_page.html', name=name,
                               cert_file=cert_filename, marksheet_file=marksheet_filename,
                               reg_no=regno, cert_id=cert_id)
    return redirect(url_for('home'))


@app.route('/verify', methods=['GET', 'POST'])

def verify():
    if request.method == 'POST':
        regno = request.form.get('regno', '').strip()
        email = request.form.get('email', '').strip().lower()
        matched = None
        for username, data in users.items():
            if data.get('reg_no', '').strip().upper() == regno.upper():
                primary = data.get('primary_email', '').strip().lower()
                secondary = data.get('secondary_email', '').strip().lower()
                if email == primary or email == secondary:
                    matched = data
                    break
        if not matched:
            return render_template('invalid.html')
        code = regno.strip().upper()[-5:]
        cert_filename = f"{code}.jpeg"
        marksheet_filename = f"{code}.pdf"
        cert_path = os.path.join(os.getcwd(), 'CERTIFICATES', cert_filename)
        marksheet_path = os.path.join(os.getcwd(), 'MARKSHEETS', marksheet_filename)
        if not os.path.exists(cert_path) and not os.path.exists(marksheet_path):
            return render_template('invalid.html')
        return render_template('certificate_page.html', name=matched.get('name'),
                               cert_file=cert_filename, marksheet_file=marksheet_filename,
                               reg_no=matched.get('reg_no'), cert_id=matched.get('certificate_id', ''))
    return render_template('verify_form.html')

@app.route('/marksheet_page', methods=['POST'])
def marksheet_page():
    name = request.form.get('name')
    cert_file = request.form.get('cert_file')
    marksheet_file = request.form.get('marksheet_file')
    reg_no = request.form.get('reg_no')
    cert_id = request.form.get('cert_id')
    return render_template('marksheet_page.html', name=name, cert_file=cert_file, marksheet_file=marksheet_file, reg_no=reg_no, cert_id=cert_id)


@app.route('/certificates/<path:filename>')
def certificate_file(filename):
    cert_dir = os.path.join(os.getcwd(), 'CERTIFICATES')
    full = os.path.join(cert_dir, filename)
    if not os.path.exists(full):
        abort(404)
    return send_from_directory(cert_dir, filename)


@app.route('/marksheets/<path:filename>')
def marksheet_file(filename):
    marks_dir = os.path.join(os.getcwd(), 'MARKSHEETS')
    full = os.path.join(marks_dir, filename)
    if not os.path.exists(full):
        abort(404)
    return send_from_directory(marks_dir, filename)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/claim')
def claim():
    # Simple page that uses Firebase client SDK to sign in the user and store a claim
    reg_no = request.args.get('reg_no', '')
    cert_id = request.args.get('cert_id', '')
    return render_template('claim.html', reg_no=reg_no, cert_id=cert_id)


@app.route('/back')
def back():
    # Prefer returning to the last selected login method (stored in session).
    # If not available, try to return to the referring page (if same host).
    last = session.get('last_method')
    if last:
        return redirect(url_for('login', method=last))

    ref = request.referrer
    if ref and ref.startswith(request.host_url):
        return redirect(ref)

    return redirect(url_for('home'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)

