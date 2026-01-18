# 🍽️ Ryouri – Recipe Recommendation System
<img width="1536" height="1024" alt="ChatGPT Image Jan 18, 2026, 06_57_07 PM" src="https://github.com/user-attachments/assets/c6738f0d-57a8-466f-9761-50d33379a88b" />

Ryouri is an intelligent **recipe recommendation web application** that suggests recipes based on **ingredients detected from images** and **nutritional preferences** provided by the user.  
The system combines **computer vision**, **machine learning**, and a **Flask web interface** to deliver personalized recipe suggestions.

🔗 **Live Demo**: https://recipe-recommendation-knii.onrender.com/

---

## 📌 Features

- 📷 **Ingredient Detection from Images**
  - Upload a food image and automatically detect ingredients.
- 🧠 **ML-Based Recipe Recommendation**
  - Uses similarity-based machine learning models to recommend recipes.
- 🥗 **Nutritional Preference Filtering**
  - Considers calories, protein, fats, and carbohydrates.
- 🌐 **Flask Web Application**
  - Clean UI with HTML/CSS templates.
- ⚡ **Lazy Loading & Data Limiting**
  - Optimized backend for faster response times.

---

## 🏗️ Tech Stack

### Backend
- **Python**
- **Flask**
- **Pandas, NumPy**
- **Scikit-Learn**

### Machine Learning
- Ingredient detection using **YOLO (custom trained)**
- Recipe similarity using:
  - KNN
  - XGBoost (experimentation & training in notebook)

### Frontend
- **HTML**
- **CSS**
- **Jinja2 Templates**

### Deployment
- **Render**

---


---

## ⚙️ How It Works

1. **User uploads a food image**
2. **Ingredients are detected** using a trained YOLO model
3. **Nutritional input** (calories, protein, carbs, fats) is taken
4. **Machine learning model** finds the closest matching recipes
5. **Recommended recipes** are displayed on the web interface

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository

git clone https://github.com/jshwadmaX/recipe-recommendation.git
cd recipe-recommendation

#### 
2️⃣ Create a Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the Application
python app.py

5️⃣ Open in Browser
http://127.0.0.1:5000

📊 Dataset

Source: Custom curated recipe dataset

Format: CSV (my_recipe.csv)

Fields include:

Recipe Name

Ingredients

Calories

Protein

Carbohydrates

Fats

🔒 Limitations

Ingredient detection accuracy depends on image quality
Limited dataset size affects recommendation diversity
Currently supports single-image input

🛠️ Future Improvements:
🔄 Real-time ingredient detection
📱 Mobile-friendly UI
🧾 User accounts & history
🧠 Deep learning–based recommendation
🌍 Multi-cuisine support
## 📁 Project Structure

