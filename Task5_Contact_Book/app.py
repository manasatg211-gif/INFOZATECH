from flask import Flask, render_template, request, redirect, url_for, flash
from pathlib import Path
import json

app = Flask(__name__)
app.secret_key = "local-demo-key"
DATA = Path(__file__).with_name("contacts.json")

def load():
    if not DATA.exists(): return []
    try: return json.loads(DATA.read_text(encoding="utf-8"))
    except (ValueError, OSError): return []

def save(items):
    DATA.write_text(json.dumps(items, indent=2), encoding="utf-8")

@app.get("/")
def index():
    q = request.args.get("q", "").strip().lower()
    contacts = load()
    if q:
        contacts = [c for c in contacts if any(q in c.get(k, "").lower() for k in ("name","email","phone","company"))]
    contacts.sort(key=lambda c: c["name"].lower())
    return render_template("index.html", contacts=contacts, q=request.args.get("q",""))

@app.post("/add")
def add():
    name=request.form.get("name","").strip()
    if not name:
        flash("Name is required.", "error")
        return redirect(url_for("index"))
    items=load()
    items.append({"id":max([c.get("id",0) for c in items],default=0)+1,
      "name":name,"email":request.form.get("email","").strip(),
      "phone":request.form.get("phone","").strip(),"company":request.form.get("company","").strip(),
      "notes":request.form.get("notes","").strip()})
    save(items)
    flash("Contact saved successfully.", "success")
    return redirect(url_for("index"))

@app.post("/delete/<int:cid>")
def delete(cid):
    items=load()
    new=[c for c in items if c.get("id") != cid]
    if len(new) != len(items):
        save(new); flash("Contact deleted.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
