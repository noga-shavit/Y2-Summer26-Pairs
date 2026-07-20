---
name: recipe-book
description: Store recipes in a JSON file and retrieve them when the user asks for a recipe.
---

# Recipe Book

Use `references/recipes.json` as the recipe database.

## Saving recipes

When the user says "save this recipe" or provides a recipe to store:

1. Read `references/recipes.json`.
2. Add or update the recipe using its lowercase name as the key.
3. Preserve all existing recipes.
4. Write valid JSON back to the same file.
5. Confirm which recipe was saved.

## Retrieving recipes

When the user asks for a recipe:

1. Read `references/recipes.json`.
2. Match the recipe name without case sensitivity.
3. Return its ingredients and numbered instructions.
4. If it does not exist, say so.