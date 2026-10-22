from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    bmi = None
    category = None
    error = None
    if request.method == 'POST':
        try:
            height_cm = float(request.form.get('height', ''))
            weight_kg = float(request.form.get('weight', ''))
            if height_cm <= 0 or weight_kg <= 0:
                error = 'Please enter height and weight greater than zero.'
            else:
                bmi = round(weight_kg / ((height_cm / 100) ** 2), 1)
                if bmi < 18.5:
                    category = 'Underweight'
                elif bmi < 25:
                    category = 'Normal weight'
                elif bmi < 30:
                    category = 'Overweight'
                else:
                    category = 'Obesity range'
        except (ValueError, TypeError):
            error = 'Please enter valid numbers for height and weight.'
    return render_template('index.html', bmi=bmi, category=category, error=error)

if __name__ == '__main__':
    app.run(debug=True)
