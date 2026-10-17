import ast
import os

import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "my_recipe.csv")
NUMERICAL_COLUMNS = ["calories", "fat", "carbohydrates", "protein"]
RECOMMENDATION_COLUMNS = [
    "recipe_name",
    "ingredients_list",
    "image_url",
    "similarity_score",
    "avrg_rate",
]

print("Loading recipe dataset...")
recipe_df = pd.read_csv(CSV_PATH)
recipe_df["ingredients_list"] = recipe_df["ingredients_list"].fillna("")
for column in NUMERICAL_COLUMNS + ["avrg_rate"]:
    recipe_df[column] = pd.to_numeric(recipe_df[column], errors="coerce").fillna(0)

if recipe_df.empty:
    raise ValueError(f"The recipe dataset is empty: {CSV_PATH}")

numerical_features = recipe_df[NUMERICAL_COLUMNS]
scaler = StandardScaler()
numerical_scaled = scaler.fit_transform(numerical_features)

vectorizer = TfidfVectorizer(max_features=500)
ingredient_vectors = vectorizer.fit_transform(recipe_df["ingredients_list"])
combined_features = hstack(
    [csr_matrix(numerical_scaled), ingredient_vectors],
    format="csr",
)

knn = NearestNeighbors(
    n_neighbors=min(3, len(recipe_df)),
    metric="cosine",
)
knn.fit(combined_features)
print(f"Recipe model ready ({len(recipe_df)} recipes)")


def format_ingredients(value):
    try:
        ingredients = ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return value

    if isinstance(ingredients, list):
        return ", ".join(str(ingredient) for ingredient in ingredients)
    return value


def recommend_recipes(input_features):
    calories, fats, carbs, protein, ingredients_str = input_features
    numerical_input = pd.DataFrame(
        [[calories, fats, carbs, protein]],
        columns=NUMERICAL_COLUMNS,
    )
    numerical_scaled_input = scaler.transform(numerical_input)
    ingredient_vector = vectorizer.transform([ingredients_str])
    input_combined = hstack(
        [csr_matrix(numerical_scaled_input), ingredient_vector],
        format="csr",
    )

    distances, indices = knn.kneighbors(input_combined)
    results = recipe_df.iloc[indices[0]][RECOMMENDATION_COLUMNS[:-2]].copy()
    results["ingredients_list"] = results["ingredients_list"].map(format_ingredients)
    results["similarity_score"] = np.clip(1 - distances[0], 0, 1) * 100
    results["avrg_rate"] = recipe_df.iloc[indices[0]]["avrg_rate"].to_numpy()
    return results[RECOMMENDATION_COLUMNS]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    form_fields = {
        "calories": "calories",
        "fats": "fats",
        "carbohydrates": "carbohydrates",
        "protein": "protein",
    }
    try:
        nutrition_values = [
            float(request.form[field]) for field in form_fields
        ]
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Enter a valid number for each nutrition value."}), 400

    if not all(np.isfinite(value) and value >= 0 for value in nutrition_values):
        return jsonify({"error": "Nutrition values must be finite and non-negative."}), 400

    ingredients = request.form.get("ingredients", "").strip()
    if not ingredients:
        return jsonify({"error": "Enter at least one ingredient."}), 400

    recommendations = recommend_recipes([*nutrition_values, ingredients])
    return jsonify(
        {
            "recommendations": recommendations.to_dict(orient="records"),
            "message": "Top recipe recommendations based on nutrition and ingredients.",
        }
    )


@app.route("/test")
def test():
    recommendations = recommend_recipes([200, 10, 50, 30, "tomato, onion"])
    return jsonify(
        {
            "recommendations": recommendations.to_dict(orient="records"),
            "message": "Test successful",
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
