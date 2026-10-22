from flask import Flask, render_template, request
import secrets
import string

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    password = None
    error = None
    length = 16
    options = {
        "uppercase": True,
        "lowercase": True,
        "numbers": True,
        "symbols": False,
    }

    if request.method == "POST":
        try:
            length = int(request.form.get("length", "16"))
            options = {
                "uppercase": request.form.get("uppercase") == "on",
                "lowercase": request.form.get("lowercase") == "on",
                "numbers": request.form.get("numbers") == "on",
                "symbols": request.form.get("symbols") == "on",
            }

            if not 8 <= length <= 64:
                error = "Choose a password length between 8 and 64 characters."
            else:
                pools = []
                if options["uppercase"]:
                    pools.append(string.ascii_uppercase)
                if options["lowercase"]:
                    pools.append(string.ascii_lowercase)
                if options["numbers"]:
                    pools.append(string.digits)
                if options["symbols"]:
                    pools.append("!@#$%^&*()-_=+[]{};:,.?")

                if not pools:
                    error = "Select at least one character type."
                else:
                    # Ensure at least one character from each selected pool.
                    chars = [secrets.choice(pool) for pool in pools]
                    all_chars = "".join(pools)
                    chars.extend(secrets.choice(all_chars) for _ in range(length - len(chars)))
                    # Securely shuffle without using a predictable random generator.
                    for i in range(len(chars) - 1, 0, -1):
                        j = secrets.randbelow(i + 1)
                        chars[i], chars[j] = chars[j], chars[i]
                    password = "".join(chars)
        except (TypeError, ValueError):
            error = "Please choose a valid password length."

    return render_template("index.html", password=password, error=error,
                           length=length, options=options)

if __name__ == "__main__":
    app.run(debug=True)
