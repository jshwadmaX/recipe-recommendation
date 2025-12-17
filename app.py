import os
from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.impute import SimpleImputer

app = Flask(__name__)

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "my_recipe.csv")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------
# Load Dataset (ONCE)
# -----------------------------
print("📊 Loading dataset...")
recipe_df = pd.read_csv(CSV_PATH)

recipe_df["ingredients_list"] = recipe_df["ingredients_list"].fillna("")
recipe_df["calories"] = pd.to_numeric(recipe_df["calories"], errors="coerce").fillna(0)
recipe_df["fat"] = pd.to_numeric(recipe_df["fat"], errors="coerce").fillna(0)
recipe_df["carbohydrates"] = pd.to_numeric(
    recipe_df["carbohydrates"], errors="coerce"
).fillna(0)
recipe_df["protein"] = pd.to_numeric(recipe_df["protein"], errors="coerce").fillna(0)
recipe_df["avrg_rate"] = pd.to_numeric(recipe_df["avrg_rate"], errors="coerce").fillna(
    0
)

print(f"✅ Dataset loaded: {len(recipe_df)} recipes")

# -----------------------------
# Preprocessing
# -----------------------------
imputer = SimpleImputer(strategy="mean")

numerical_features = recipe_df[["calories", "fat", "carbohydrates", "protein"]]

numerical_imputed = imputer.fit_transform(numerical_features)

scaler = StandardScaler()
numerical_scaled = scaler.fit_transform(numerical_imputed)

vectorizer = TfidfVectorizer(max_features=500)
ingredient_vectors = vectorizer.fit_transform(recipe_df["ingredients_list"]).toarray()

combined_features = np.hstack([numerical_scaled, ingredient_vectors])

# -----------------------------
# KNN Model
# -----------------------------
knn = NearestNeighbors(n_neighbors=5, metric="cosine")
knn.fit(combined_features)

print("🤖 KNN model ready")


# -----------------------------
# Recommendation Logic
# -----------------------------
def recommend_recipes(input_features):
    calories, fats, carbs, protein, ingredients_str = input_features

    num = [calories, fats, carbs, protein]
    num_scaled = scaler.transform(imputer.transform([num]))

    ing_vec = vectorizer.transform([ingredients_str]).toarray()

    input_combined = np.hstack([num_scaled, ing_vec])

    distances, indices = knn.kneighbors(input_combined)

    results = recipe_df.iloc[indices[0]].copy()
    results["similarity_score"] = results["avrg_rate"]

    return results[
        [
            "recipe_name",
            "ingredients_list",
            "image_url",
            "similarity_score",
            "avrg_rate",
        ]
    ].head(3)


# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    try:
        calories = float(request.form["calories"])
        fats = float(request.form["fats"])
        carbohydrates = float(request.form["carbohydrates"])
        protein = float(request.form["protein"])
    except:
        return jsonify({"error": "Invalid input values"}), 400

    # Image is optional now (just save it)
    if "image" in request.files:
        img = request.files["image"]
        img.save(os.path.join(UPLOAD_FOLDER, img.filename))

    # Static ingredients (NO YOLO)
    ingredients_str = "tomato, onion, garlic"

    input_features = [
        calories,
        fats,
        carbohydrates,
        protein,
        ingredients_str,
    ]

    recommendations = recommend_recipes(input_features)

    return jsonify(
        {
            "recommendations": recommendations.to_dict(orient="records"),
            "message": "Top recipe recommendations based on nutrition",
        }
    )


@app.route("/test")
def test():
    input_features = [200, 10, 50, 30, "tomato, onion"]
    recs = recommend_recipes(input_features)

    return jsonify(
        {
            "recommendations": recs.to_dict(orient="records"),
            "message": "Test successful",
        }
    )


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    print("🚀 Starting Ryori (YOLO disabled)")
    app.run(debug=False)
