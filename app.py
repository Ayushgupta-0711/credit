from flask import Flask, render_template, request
import mysql.connector as mc
import joblib

app = Flask(__name__)

# Database connection
conn = mc.connect(user='root', password='ayush@#11', host='localhost', database='credit_p')

# Load ML Model
model = joblib.load("randomforestregressor.lb")  # Ensure file extension is correct

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('userdata.html')

@app.route('/userdata', methods=['POST'])
def userdata():
    if request.method == 'POST':
        try:
            # Retrieve form data
            income = float(request.form['income'])
            credit_limit = float(request.form['limit'])
            cards = int(request.form['cards'])
            age = int(request.form['age'])
            education = int(request.form['education'])
            gender = int(request.form['gender'])
            student = int(request.form['student'])
            married = int(request.form['married'])
            ethnicity_input = request.form['ethnicity']

            # Ethnicity mapping
            ethnicity_mapping = {
                'Caucasian': 0,
                'Asian': 1,
                'African American': 2
            }

            ethnicity_encoded = ethnicity_mapping.get(ethnicity_input, 1)  # Default to 1 if unknown

            # Prepare data for model
            unseen_data = [[income, credit_limit, cards, age, education, gender, student, married, ethnicity_encoded]]

            # Predict output
            output = model.predict(unseen_data)[0]

            # Insert into database
            query = """INSERT INTO data (income, credit_limit, cards, age, education, gender, student, married, ethnicity, predicted)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            mycursor = conn.cursor()
            details = (income, credit_limit, cards, age, education, gender, student, married, ethnicity_encoded, int(output))
            mycursor.execute(query, details)
            conn.commit()
            mycursor.close()

            return f"The predicted credit score is: {output}"

        except Exception as e:
            return f"An error occurred: {str(e)}"

@app.route('/history')
def history():
    try:
        mycursor = conn.cursor()
        query = "SELECT * FROM data"
        mycursor.execute(query)
        data = mycursor.fetchall()
        mycursor.close()
        return render_template('history.html', userdetails=data)
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
