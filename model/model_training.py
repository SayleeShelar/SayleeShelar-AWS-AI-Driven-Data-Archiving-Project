import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

# Load data
data = pd.read_csv('../data/metadata.csv')

# Preprocessing
data['days_since_modified'] = (pd.Timestamp.now() - pd.to_datetime(data['Last Modified Date'], dayfirst=True)).dt.days
features = data[['days_since_modified', 'Size']]
labels = (data['days_since_modified'] > 30).astype(int)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Train Model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save Model
joblib.dump(model, 'model.joblib')

# Evaluate Model
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print(f"Precision: {precision_score(y_test, y_pred)}")
print(f"Recall: {recall_score(y_test, y_pred)}")
print(f"F1-Score: {f1_score(y_test, y_pred)}")
