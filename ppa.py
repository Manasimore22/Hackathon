from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # Get form data
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        gender = request.form['gender']
        currAddress = request.form['currAddress']
        perAddress = request.form['perAddress']
        policeStation = request.form['policeStation']
        policePost = request.form['policePost']
        policeId = request.form['policeId']
        email = request.form['email']
        password = request.form['password']
        phoneNumber = request.form['number']

        # Simulate success message (replace this with actual CSV update logic)
        return 'Registration successful!'

if __name__ == '__main__':
    app.run(debug=True)
