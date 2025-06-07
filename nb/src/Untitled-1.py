# %%
from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=["http://localhost:9200"],
    http_auth=None,
    use_ssl=False,
    verify_certs=False,
    ssl_show_warn=False,
)

# Create the 'recipes' index if it doesn't exist
if not client.indices.exists(index="recipes"):
    client.indices.create(index="recipes")
    print("Created 'recipes' index.")
else:
    print("'recipes' index already exists.")

# %% [markdown]
# # Keto/Vegan Diet classifier
# Argmax, a consulting firm specializing in search and recommendation solutions with offices in New York and Israel, is hiring entry-level Data Scientists and Machine Learning Engineers.
# 
# At Argmax, we prioritize strong coding skills and a proactive, “get-things-done” attitude over a perfect resume. As part of our selection process, candidates are required to complete a coding task demonstrating their practical abilities.
# 
# In this task, you’ll work with a large recipe dataset sourced from Allrecipes.com. Your challenge will be to classify recipes based on their ingredients, accurately identifying keto (low-carb) and vegan (no animal products) dishes.
# 
# Successfully completing this assignment is a crucial step toward joining Argmax’s talented team.

# %%
from opensearchpy import OpenSearch
from decouple import config
import pandas as pd

client = OpenSearch(
    hosts=[config('OPENSEARCH_URL', 'http://localhost:9200')],
    http_auth=None,
    use_ssl=False,
    verify_certs=False,
    ssl_show_warn=False,
)

# %% [markdown]
# # Recipes Index
# Our data is stored in OpenSearch, and you can query it using either Elasticsearch syntax or SQL.
# ## Elasticsearch Syntax

# %%
query = {
    "query": {
        "match": {
            "description": { "query": "egg" }
        }
    }
}

res = client.search(
    index="recipes",
    body=query,
    size=2
)

hits = res['hits']['hits']
hits

# %% [markdown]
# ## SQL syntax

# %%
query = """
SELECT *
FROM recipes
WHERE description like '%egg%'
LIMIT 10
"""

res = client.sql.query(body={'query': query})
df = pd.DataFrame(res["datarows"], columns=[c["name"] for c in res["schema"]])
df

# %% [markdown]
# # Task Instructions
# 
# Your goal is to implement two classifiers:
# 
# 1.	Vegan Meal Classifier
# 1.	Keto Meal Classifier
# 
# Unlike typical supervised machine learning tasks, the labels are not provided in the dataset. Instead, you will rely on clear and verifiable definitions to classify each meal based on its ingredients.
# 
# ### Definitions:
# 
# 1. **Vegan Meal**: Contains no animal products whatsoever (no eggs, milk, meat, etc.).
# 1. **Keto Meal**: Contains no ingredients with more than 10g of carbohydrates per 100g serving. For example, eggs are keto-friendly, while apples are not.
# 
# Note that some meals may meet both vegan and keto criteria (e.g., meals containing avocados), though most meals typically fall into neither category.
# 
# ## Example heuristic:

# %%
def is_ingredient_vegan(ing):
    for animal_product in "egg meat milk butter veel lamb beef chicken sausage".split():
        if animal_product in ing:
            return False
    return True

def is_vegan_example(ingredients):
    return all(map(is_ingredient_vegan, ingredients))
    
df["vegan"] = df["ingredients"].apply(is_vegan_example)
df

# %% [markdown]
# ### Limitations of the Simplistic Heuristic
# 
# The heuristic described above is straightforward but can lead to numerous false positives and negatives due to its reliance on keyword matching. Common examples of incorrect classifications include:
# - "Peanut butter" being misclassified as non-vegan, as “butter” is incorrectly assumed to imply dairy.
# - "eggless" recipes being misclassified as non-vegan, due to the substring “egg.”
# - Animal-derived ingredients such as “pork” and “bacon” being incorrectly identified as vegan, as they may not be explicitly listed in the keyword set.
# 
# 
# # Submission
# ## 1. Implement Diet Classifiers
# Complete the two classifier functions in the diet_classifiers.py file within this repository. Ensure your implementation correctly identifies “keto” and “vegan” meals. After implementing these functions, verify that the Flask server displays the appropriate badges (“keto” and “vegan”) next to the corresponding recipes.
# 
# > **Note**
# >
# > This repo contains two `diet_classifiers.py` files:
# > 1. One in this folder (`nb/src/diet_classifiers.py`)
# > 2. One in the Flask web app folder (`web/src/diet_classifiers.py`)
# >
# > You can develop your solution here in the notebook environment, but to apply your solution 
# > to the Flask app you will need to copy your implementation into the `diet_classifiers.py` 
# > file in the Flask folder!!!

# %%
def is_ingredient_keto(ingredient):
    # TODO: complete
    return False

def is_ingredient_vegan(ingredient):
    # TODO: complete
    return False    

# %% [markdown]
# For your convenience, you can sanity check your solution on a subset of labeled recipes by running `diet_classifiers.py`

# %%
! python diet_classifiers.py --ground_truth c:\Users\DELL\search_by_ingredients\data\ground_truth_sample.csv

# %% [markdown]
# ## 2. Repository Setup
# Create a **private** GitHub repository for your solution, and invite the GitHub user `argmax2025` as a collaborator. **Do not** share your implementation using a **forked** repository.
# 
# ## 3. Application Form
# Once you’ve completed the implementation and shared your private GitHub repository with argmax2025, please fill out the appropriate application form:
# 1. [US Application Form](https://forms.clickup.com/25655193/f/rexwt-1832/L0YE9OKG2FQIC3AYRR)
# 2.  [IL Application Form](https://forms.clickup.com/25655193/f/rexwt-1812/IP26WXR9X4P6I4LGQ6)
# 
# 
# Your application will not be considered complete until this form is submitted.
# 
# ## Evaluation process
# 
# 
# Your submission will be assessed based on the following criteria:
# 
# 
# 1.	**Readability & Logic** – Clearly explain your approach, including your reasoning and any assumptions. If you relied on external resources (e.g., ingredient databases, nutrition datasets), be sure to cite them.
# 2.	**Executability** – Your code should run as is when cloned from your GitHub repository. Ensure that all paths are relative, syntax is correct, and no manual setup is required.
# 3.	**Accuracy** – Your classifiers will be evaluated against a holdout set of 20,000 recipes with verified labels. Performance will be compared to the ground truth.
# data.
# 
# 
# ## Next steps
# If your submission passes the initial review, you’ll be invited to a 3-hour live coding interview, where you’ll be asked to extend and adapt your solution in real time.
# 
# Please make sure you join from a quiet environment and have access to a Python-ready workstation capable of running your submitted project.

# %%



