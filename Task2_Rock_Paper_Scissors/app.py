from flask import Flask, render_template, request, session, redirect, url_for
import random, os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local-demo-secret-key")
CHOICES = ["rock", "paper", "scissors"]
EMOJI = {"rock":"✊", "paper":"✋", "scissors":"✌️"}

def new_game():
    return {"player":0,"computer":0,"draws":0,"rounds":0,"history":[]}

@app.route("/", methods=["GET","POST"])
def index():
    if "game" not in session: session["game"] = new_game()
    result = player = computer = None
    if request.method == "POST":
        if request.form.get("action") == "reset":
            session["game"] = new_game()
            return redirect(url_for("index"))
        player = request.form.get("choice","").lower()
        if player in CHOICES:
            game = session["game"]
            computer = random.choice(CHOICES)
            game["rounds"] += 1
            if player == computer:
                result, message = "draw", "It's a draw!"
                game["draws"] += 1
            elif (player,computer) in [("rock","scissors"),("paper","rock"),("scissors","paper")]:
                result, message = "win", "You win this round!"
                game["player"] += 1
            else:
                result, message = "lose", "Computer wins this round!"
                game["computer"] += 1
            game["history"].insert(0,{"round":game["rounds"],"player":player,"computer":computer,"result":result,"message":message})
            game["history"] = game["history"][:6]
            session["game"] = game
        else:
            return redirect(url_for("index"))
    return render_template("index.html", game=session["game"], result=result, player_choice=player, computer_choice=computer, emoji=EMOJI)

if __name__ == "__main__":
    app.run(debug=True)
