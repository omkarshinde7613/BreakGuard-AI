import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

df = pd.read_csv("schemas/training_data.csv")

X_train, X_test, y_train, y_test = train_test_split(
    df["description"], df["risk"], test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print("Training rows:", X_train_vec.shape)
print("Test rows:", X_test_vec.shape)