import numpy as np
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
df = pd.read_csv("DatSet.csv")

X = df.iloc[:, 1:-1]
# y is the second-to-last column
y = df.iloc[:, -2]

# 3. Identify Column Types for Preprocessing
numeric_features = X.select_dtypes(include=np.number).columns
categorical_features = X.select_dtypes(include=['object', 'category']).columns

# 4. Create Preprocessing Pipeline (Handles strings automatically)
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features),
        ('num', 'passthrough', numeric_features)
    ],
    remainder='drop'
)

# 5. Create the full Model Pipeline
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1))
])

# 6. Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 7. Train the Model
model_pipeline.fit(X_train, y_train)

# 8. Evaluate and Save
y_pred = model_pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy * 100:.2f}%")
# Save the entire pipeline, not just the model
joblib.dump(model_pipeline, "AIFinal_Forest_Pipeline.pkl")
print("Model pipeline saved")


