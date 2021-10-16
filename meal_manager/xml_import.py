from xml.etree import ElementTree
from bs4 import BeautifulSoup
from pprint import pprint
import xmlschema
import os


recipe_list = []

for file in os.listdir("recipes/"):
    if file.endswith(".xml"):
        recipe_list.append(file)

xs = xmlschema.XMLSchema('recipe_adder/schema/recipe2.xsd')

with open("ingredient.txt", "w") as f:
    for recipe in recipe_list:
        xt = ElementTree.parse("recipes/" + recipe)
        if xs.is_valid(xt):
            test = xs.to_dict(xt)


