import pandas as pd

recipes = pd.read_csv('../data/recipes.csv')
reviews = pd.read_csv('../data/reviews.csv')

print(recipes.shape)
print(recipes.columns.tolist())
print(recipes.head(2))
print(reviews.columns.tolist())