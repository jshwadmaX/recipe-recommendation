# Ryouri — Recipe Recommendations

Ryouri is a small Flask web app that recommends recipes from a local recipe dataset. Enter nutrition targets and ingredients you have; the app ranks recipes using nutritional similarity and ingredient text.

> **Ingredient photos are not analyzed.** The current recommender uses the text you enter and does not run image recognition.

## Screenshots

Add screenshots here when they are ready:

### Home page

_Screenshot placeholder — add the home page image here._

### Recipe recommendations

_Screenshot placeholder — add a recommendations image here._

## Features

- Search a bundled dataset of nearly 49,000 recipes.
- Rank the closest recipes using nutrition values and ingredient text.
- Show recipe images, ingredient lists, match scores, and ratings.
- Run locally without downloading a model or setting up API keys.

## Requirements

- Python 3.10 or newer
- `pip`

The web app's runtime dependencies are listed in [`requirements.txt`](requirements.txt). An optional dependency list for the exploratory notebook is in [`requirements-notebook.txt`](requirements-notebook.txt).

## Run locally

### Windows (PowerShell)

From the project folder:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000> in your browser. Keep the terminal open while using the app; press `Ctrl+C` there to stop the server.

If PowerShell blocks virtual-environment activation, run the environment's Python directly instead:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```

Then visit <http://127.0.0.1:5000>.

The recipe data is included in `my_recipe.csv`. The app loads and prepares it when it starts, so the first request may take a few seconds. You do not need to run a separate training step.

## Use the app

1. Enter calories, fat, carbohydrates, and protein as non-negative numbers.
2. Enter one or more ingredients, separated by commas (for example, `tomato, onion, garlic`).
3. Select **Discover Recipes** to see the top matches.

The match percentage represents similarity to the entered nutrition and ingredient features. The star rating is the recipe's average dataset rating; it is a separate value.

## Run the tests

With the project environment activated:

```bash
python -m unittest discover -s tests -v
```

## Optional notebook

`Ryouri Code.ipynb` contains a separate model-experimentation workflow and is not needed to run the web app. To install its additional Python packages:

```bash
python -m pip install -r requirements-notebook.txt
```

Open the notebook in Jupyter or VS Code. Some notebook cells may require adapting their data paths or runtime-specific setup for your machine.

## Project layout

```text
app.py                  Flask app and recommendation model
my_recipe.csv           Recipe dataset used by the app
templates/index.html    Web interface
static/                 Styles and local fallback images
tests/                  Automated route and recommendation tests
requirements.txt        Web app dependencies
requirements-notebook.txt
                        Optional notebook dependencies
```
