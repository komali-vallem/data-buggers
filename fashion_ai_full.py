from flask import Flask, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "fashion_secret_key"

# Simple in-memory user storage
users = {}

# Fashion dataset inside same file
fashion_data = [
    {"occasion": "Casual", "weather": "Hot", "mood": "Happy",
     "outfit": "Floral crop top with denim shorts",
     "accessories": "Sunglasses and white sneakers"},

    {"occasion": "Party", "weather": "Cold", "mood": "Elegant",
     "outfit": "Black long sleeve gown",
     "accessories": "Silver necklace and heels"},

    {"occasion": "Wedding", "weather": "Hot", "mood": "Elegant",
     "outfit": "Pastel lehenga with embroidery",
     "accessories": "Statement earrings"},

    {"occasion": "Office", "weather": "Cold", "mood": "Chill",
     "outfit": "Blazer with formal trousers",
     "accessories": "Watch and handbag"},

    {"occasion": "Date Night", "weather": "Pleasant", "mood": "Happy",
     "outfit": "Flowy midi dress",
     "accessories": "Soft curls and heels"},
]

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users:
            message = "User already exists!"
        else:
            users[username] = password
            message = "Registration successful! Please login."

    return page_template("""
        <h2>📝 Register</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Register</button>
        </form>
        <p>{}</p>
        <a href="/login">Already have account? Login</a>
    """.format(message))

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/")
        else:
            message = "Invalid credentials!"

    return page_template("""
        <h2>🔐 Login</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Login</button>
        </form>
        <p>{}</p>
        <a href="/register">Create new account</a>
    """.format(message))

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# ---------------- MAIN PAGE ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect("/login")

    recommendation = ""
    accessories = ""
    explanation = ""

    if request.method == "POST":
        occasion = request.form.get("occasion")
        weather = request.form.get("weather")
        mood = request.form.get("mood")

        matches = [
            item for item in fashion_data
            if item["occasion"] == occasion
            and item["weather"] == weather
            and item["mood"] == mood
        ]

        if matches:
            result = random.choice(matches)
            recommendation = result["outfit"]
            accessories = result["accessories"]
            explanation = f"This AI-generated outfit matches your {mood.lower()} mood for a {occasion.lower()} event."

        else:
            recommendation = "No match found. Try different options."

    return page_template(f"""
        <h2>👗 Welcome {session['user']}</h2>
        <a href="/logout">Logout</a>

        <form method="POST">
            <select name="occasion" required>
                <option value="">Select Occasion</option>
                <option>Casual</option>
                <option>Party</option>
                <option>Wedding</option>
                <option>Office</option>
                <option>Date Night</option>
            </select><br>

            <select name="weather" required>
                <option value="">Select Weather</option>
                <option>Hot</option>
                <option>Cold</option>
                <option>Pleasant</option>
            </select><br>

            <select name="mood" required>
                <option value="">Select Mood</option>
                <option>Happy</option>
                <option>Elegant</option>
                <option>Chill</option>
            </select><br>

            <button type="submit">Generate Outfit ✨</button>
        </form>

        {"<div class='result'><h3>✨ Outfit:</h3><p>"+recommendation+
         "</p><h4>Accessories:</h4><p>"+accessories+
         "</p><p>"+explanation+"</p></div>" if recommendation else ""}
    """)

# ---------------- COMMON TEMPLATE ----------------
def page_template(content):
    return f"""
    <html>
    <head>
        <title>AI Fashion System</title>
        <style>
            body {{
                font-family: Arial;
                background: linear-gradient(135deg,#ff9a9e,#fad0c4);
                display:flex;
                justify-content:center;
                align-items:center;
                height:100vh;
            }}
            .card {{
                background:white;
                padding:30px;
                width:400px;
                border-radius:15px;
                text-align:center;
                box-shadow:0 10px 25px rgba(0,0,0,0.2);
            }}
            input, select {{
                width:90%;
                padding:8px;
                margin:10px 0;
                border-radius:6px;
            }}
            button {{
                width:95%;
                padding:10px;
                background:#ff4b5c;
                color:white;
                border:none;
                border-radius:8px;
                cursor:pointer;
            }}
            button:hover {{
                background:#e63946;
            }}
            .result {{
                margin-top:20px;
                background:#f8edeb;
                padding:15px;
                border-radius:10px;
            }}
            a {{
                text-decoration:none;
                color:#ff4b5c;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            {content}
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)