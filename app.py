from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'mysecret'

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
        "name": "V KEERTHI ESWAR",
        "reg_no": "8115U23CS045",
        "primary_email": "keerthiveeraiyan2005@gmail.com",
        "secondary_email": "i2323@krce.ac.in",
        "password": "Keerthi7",
        "pdf": "KAI-CS45.pdf"
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
        "name": "S. KANNAN HARISH",
        "reg_no": "8115U23CS043",
        "primary_email": "kannanharishtheking10@gmail.com",
        "secondary_email": "kannanharish582@gmail.com",
        "password": "Harishmi45",
        "pdf": "KAI-CS43.pdf"
    },
    "KADHI": {
        "name": "A. AADHIKESAV",
        "reg_no": "8115U23CS001",
        "primary_email": "csa2301@krce.ac.in",
        "secondary_email": "Aadhikesav07@gmail.com",
        "password": "Aadhikesav",
        "pdf": "KAI-CS01.pdf"
    },
    "ARON_JONATH_16": {
        "name": "A. ARON JONATH",
        "reg_no": "8115U23CS016",
        "primary_email": "aronjonath0807@gmail.com",
        "secondary_email": "aronjonath0807@gmail.com",
        "password": "zxcvbnm",
        "pdf": "KAI-CS16.pdf"
    },
    "A.AKASH_RCB": {
        "name": "A. AKASH",
        "reg_no": "8115U23CS007",
        "primary_email": "a78154111@gmail.com",
        "secondary_email": "h2304@krce.ac.in",
        "password": "asdfghjkl",
        "pdf": "KAI-CS07.pdf"
    },
    "MUTHUKARUPPAN P": {
        "name": "MUTHUKARUPPAN P",
        "reg_no": "8115U23CS069",
        "primary_email": "muthucs069@gmail.com",
        "secondary_email": "muthucs069@gmail.com",
        "password": "123@m12345",
        "pdf": "KAI-CS69.pdf"
    },
    "ARAVINTH": {
        "name": "ARAVINTH .C",
        "reg_no": "8115U23CS015",
        "primary_email": "aravinth2316@gmail.com",
        "secondary_email": "aravinthpk7@gmail.com",
        "password": "aravinth2316",
        "pdf": "KAI-CS16.pdf"
    }
}

@app.route('/')
def home():
    return render_template('login_options.html')


get_mem=''
@app.route('/login/<method>', methods=['GET', 'POST'])

def login(method):
    global get_mem
    get_mem=method
    # Set the label manually before POST or loop
    if method == 'username':
        label = 'Username'
    elif method == 'name':
        label = 'Name'
    elif method == 'regno':
        label = 'Register Number'
    elif method == 'primary':
        label = 'Primary E-mail'
    elif method == 'secondary':
        label = 'Secondary E-mail'
    else:
        label = method

    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']
        
        for username, data in users.items():
            if method == 'username' and username == identifier and data['password'] == password:
                session['user'] = username
                return redirect(url_for('results'))
            elif method == 'name' and data['name'] == identifier and data['password'] == password:
                session['user'] = username
                return redirect(url_for('results'))
            elif method == 'regno' and data['reg_no'] == identifier and data['password'] == password:
                session['user'] = username
                method='register number'
                return redirect(url_for('results'))
            elif method == 'primary' and data['primary_email'] == identifier and data['password'] == password:
                session['user'] = username
                method='primary e-mail'
                return redirect(url_for('results'))
            elif method == 'secondary' and data['secondary_email'] == identifier and data['password'] == password:
                session['user'] = username
                method='secondary e-mail'
                return redirect(url_for('results'))
        return render_template('invalid.html')
    return render_template('login_form.html', method=label)

@app.route('/results')
def results():
    if 'user' in session:
        user = session['user']
        name=users[user]['name']
        return render_template('results.html', user=name, pdf=users[user]['pdf'])
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/back')
def back():
    print(get_mem)
    return redirect(url_for('login',method=get_mem))


if __name__ == '__main__':
    app.run(debug=True)
