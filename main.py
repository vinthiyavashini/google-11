from flask import Flask, render_template_string, request, redirect, session, url_for
import random, os

app = Flask(__name__)
# In production, use a random secret key. 'easy_key' is fine for testing.
app.secret_key = os.environ.get("SECRET_KEY", "easy_key")

# Simple Login Page
LOGIN_HTML = """
<body style="text-align:center; padding:50px; font-family:sans-serif;">
    <h1>Cloud Login</h1>
    <form action="/" method="POST">
        <input type="text" name="u" placeholder="User" required><br><br>
        <input type="password" name="p" placeholder="Pass" required><br><br>
        <button type="submit">Login</button>
    </form>
    <p style="color:red">{{ err }}</p>
</body>
"""

# Simple Portal Page
PORTAL_HTML = """
<body style="text-align:center; padding:50px; font-family:sans-serif;">
    <h1>Cloud Portal</h1>
    <p><strong>Fact:</strong> {{ fact }}</p>
    <br>
    <a href="{{ url_for('portal') }}">New Fact</a> | <a href="{{ url_for('logout') }}">Logout</a>
</body>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Added .strip() to handle accidental spaces in username/password
        username = request.form['u'].strip()
        password = request.form['p'].strip()
        
        if username == 'admin' and password == '123':
            session['user'] = 'admin'
            return redirect(url_for('portal'))
        
        return render_template_string(LOGIN_HTML, err="Try Again!")
    return render_template_string(LOGIN_HTML, err="")

@app.route('/portal')
def portal():
    if 'user' not in session: 
        return redirect(url_for('login'))
    
    facts = [
        "Cloud computing is the on-demand availability of computer system resources.", 
        "AWS was the first major cloud provider back in 2006.", 
        "Cloud storage makes it easy to access files from any device."
    ]
    return render_template_string(PORTAL_HTML, fact=random.choice(facts))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
