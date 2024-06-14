import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Load the dataset
data = pd.read_csv('final_dataset.csv')

# Explicitly cast 'MISSING' to a compatible dtype before filling NaN values
data['aadhar_number'] = data['aadhar_number'].astype('object')  # Assuming 'object' is a compatible dtype for your data
data['aadhar_number'].fillna('MISSING', inplace=True)

# Preprocess string columns (name and address)
label_encoder = LabelEncoder()
name_mapping = dict(zip(data['name'], label_encoder.fit_transform(data['name'])))
address_mapping = dict(zip(data['address'], label_encoder.fit_transform(data['address'])))
id_mapping = dict(zip(data['id_number'], label_encoder.fit_transform(data['id_number'])))
pan_mapping = dict(zip(data['pan_number'], label_encoder.fit_transform(data['pan_number'])))

data['name'] = data['name'].map(name_mapping)
data['address'] = data['address'].map(address_mapping)
data['id_number'] = data['id_number'].map(id_mapping)
data['pan_number'] = data['pan_number'].map(pan_mapping)

# Condition 1: If aadhar_number is empty, mark the account as fake
data['fake_condition_1'] = data['aadhar_number'].apply(lambda x: 1 if x == 'MISSING' else 0)

# Condition 2: If multiple accounts have the same mobile number, mark the accounts without Aadhar number as fake
mobile_counts = data['mobile_number'].value_counts()
data['mobile_count'] = data['mobile_number'].map(mobile_counts)

def mark_fake_accounts(row):
    if row['mobile_count'] > 1 and row['aadhar_number'] == 'MISSING':
        return 1  # Fake account
    else:
        return 0  # Normal account

data['fake_condition_2'] = data.apply(mark_fake_accounts, axis=1)

# Combine the conditions to get the final label
data['is_fake'] = data['fake_condition_1'] | data['fake_condition_2']

# Drop intermediate columns
data.drop(['fake_condition_1', 'fake_condition_2', 'mobile_count'], axis=1, inplace=True)

# Split the data into features and target
X = data.drop(['is_fake'], axis=1)
y = data['is_fake']

# Define column transformer
# Separate transformations for numeric and categorical features
numeric_features = ['age', 'annual_income']
categorical_features = ['name', 'address', 'id_number', 'pan_number']

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),  # Impute missing values with the mean
    ('scaler', 'passthrough')                       # No scaling needed for RandomForestClassifier
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),  # Impute missing values with the most frequent value
    ('onehot', OneHotEncoder(handle_unknown='ignore'))     # One-hot encoding for categorical features
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Split the data into training and testing sets()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the RandomForestClassifier 
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', RandomForestClassifier(random_state=42))])

# Fit the model
clf.fit(X_train, y_train)

# Predict on the test set
y_pred = clf.predict(X_test)

# Calculate and print the accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Predict on the entire dataset
data['predicted_label'] = clf.predict(X)

# Save the results to a new CSV file
data.to_csv('fake_accounts_predictions.csv', index=False)

# Save only the entries marked as fake accounts to a separate CSV file with original format
fake_accounts = data[data['predicted_label'] == 1].copy()
fake_accounts['name'] = fake_accounts['name'].map({v: k for k, v in name_mapping.items()})
fake_accounts['address'] = fake_accounts['address'].map({v: k for k, v in address_mapping.items()})
fake_accounts['id_number'] = fake_accounts['id_number'].map({v: k for k, v in id_mapping.items()})
fake_accounts['pan_number'] = fake_accounts['pan_number'].map({v: k for k, v in pan_mapping.items()})
fake_accounts.to_csv('fake_accounts_only.csv', index=False)
