from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Manasi@2206'
app.config['MYSQL_DB'] = 'transaction'
mysql = MySQL(app)

# Function to get MySQL connection within the app context
def get_db_connection():
    return mysql.connection.cursor()

# Load the main dataset within the app context
with app.app_context():
    cursor = get_db_connection()
    main_dataset = pd.read_sql('SELECT * FROM main_dataset', con=cursor.connection)

# Preprocessing
label_encoder = LabelEncoder()
main_dataset['transaction_type_encoded'] = label_encoder.fit_transform(main_dataset['transaction_type'])
X = main_dataset[['birthdate', 'old_balance', 'transaction_type_encoded']]
y = main_dataset['is_fraud']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Manual Transaction
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_transaction', methods=['POST'])
def make_transaction():
    # Extract data from the request
    account_number = request.form['account_number']
    transaction_type = request.form['transaction_type']
    transaction_amount = float(request.form['transaction_amount'])
    old_balance = float(request.form['old_balance'])

    # Update main dataset within the app context
    with app.app_context():
        cursor = get_db_connection()
        new_balance = old_balance + transaction_amount
        cursor.execute(
            f"UPDATE main_dataset SET old_balance={old_balance}, new_balance={new_balance} WHERE account_number='{account_number}'"
        )
        cursor.connection.commit()

    # Update transaction dataset
    with app.app_context():
        cursor = get_db_connection()
        cursor.execute(
            f"INSERT INTO transaction_dataset (account_number, transaction_type, transaction_amount, old_balance, new_balance) "
            f"VALUES ('{account_number}', '{transaction_type}', {transaction_amount}, {old_balance}, {new_balance})"
        )
        cursor.connection.commit()

    # Test the transaction
    test_data = pd.DataFrame([[old_balance, transaction_amount, label_encoder.transform([transaction_type])[0]]],
                             columns=['old_balance', 'transaction_amount', 'transaction_type_encoded'])
    is_fraud = model.predict(test_data)[0]

    return jsonify({'is_fraud': int(is_fraud)})


if __name__ == '__main__':
    app.run(debug=True)