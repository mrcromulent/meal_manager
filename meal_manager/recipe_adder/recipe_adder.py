# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 11:55:11 2020

@author: Pierre
"""

import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QFileDialog
from lxml_to_dict import lxml_to_dict
from PyQt5.QtCore import QTranslator
import lxml.etree as et
import xmlschema

import widget_recipe_adder
import add_edit_ingredients
from helper_functions import add_to_tree, find_nutrition_table, clear_all

schema = et.XMLSchema(etree=None, file='schema/recipe.xsd')
parser = et.XMLParser(schema=schema)


class ControlRecipeAdder(QtWidgets.QDialog):

    def __init__(self, parent=None):
        # Parent class constructor
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = widget_recipe_adder.Ui_Form()
        self.ui.setupUi(self)

        self.error_dialog = QtWidgets.QErrorMessage()

        # Ingredients
        self.ui_ing_dialog = add_edit_ingredients.ControlAddEditIngredients()
        self.ui_ing_dialog.ui.button_box.accepted.connect(self.populate_table)
        self.ui.btn_add_edit_ingredients.clicked.connect(self.add_edit_ingredients)

        # Instructions
        self.ui.btn_add_step.clicked.connect(self.add_step)
        self.ui.btn_delete_step.clicked.connect(self.delete_step)

        # Import/Export stuff
        self.ui.btn_export.clicked.connect(self.export)
        self.ui.btn_clear_all.clicked.connect(self.clear_all)
        self.ui.btn_import.clicked.connect(self.import_func)

    def import_func(self):
        xs = et.XMLSchema(etree=None, file='schema/recipe.xsd')

        file_name, _ = QFileDialog.getOpenFileName(self, "Open", ".", "(*.xml)")

        if file_name != '':
            try:
                tree = et.parse(file_name, parser=parser)
                tree_dict = lxml_to_dict(tree.getroot())
                self.repopulate_form(tree_dict)

            except et.XMLSyntaxError as e:
                self.error_dialog = QtWidgets.QErrorMessage()
                self.error_dialog.showMessage(str(e.error_log))

    def xs_duration_to_ted(self, xsd):
        start = xsd.find('T') + 1
        end = xsd.find('H', start)
        hrs = xsd[start:end]

        start = xsd.find('H') + 1
        end = xsd.find('M', start)
        mns = xsd[start:end]

        return (hrs,mns)

    def repopulate_form(self, tree_dict):
        recipe = tree_dict['recipe']

        self.ui.led_recipe_name.setText(recipe['name'])
        self.ui.sbx_serves.setValue(int(recipe['serves']))

        if recipe.get('prepTime', None) is not None:
            hrs, mns = self.xs_duration_to_ted(recipe['prepTime'])
            self.ui.ted_prep_time.setTime(QTime(int(hrs), int(mns)))

        if recipe.get('cookTime', None) is not None:
            hrs, mns = self.xs_duration_to_ted(recipe['cookTime'])
            self.ui.ted_cook_time.setTime(QTime(int(hrs), int(mns)))

        if recipe.get('nutrition', None) is not None:
            nutrition = recipe['nutrition']

        dict_keys = ['name', 'notes', 'quantity', 'unit', 'staple']
        ingredients = recipe['ingredients']
        for i in range(len(ingredients)):
            if i == 0:
                tag = 'ingredient'
            else:
                tag = 'ingredient' + str(i)

            ingredient = ingredients[tag]

            new_row_count = self.ui.lwt_ingredients.rowCount() + 1
            self.ui.lwt_ingredients.setRowCount(new_row_count)

            for j in range(len(dict_keys)):
                to_insert = ingredient[dict_keys[j]]
                self.ui.lwt_ingredients.setItem(new_row_count - 1, j, QtWidgets.QTableWidgetItem(to_insert))

        instructions = recipe['instructions']
        for i in range(len(instructions)):
            if i == 0:
                tag = 'step'
            else:
                tag = 'step' + str(i)

            step = instructions[tag]

            new_row_count = self.ui.lwt_instructions.rowCount() + 1
            self.ui.lwt_instructions.setRowCount(new_row_count)
            self.ui.lwt_instructions.setItem(new_row_count - 1, 0, QtWidgets.QTableWidgetItem(step))

    def add_edit_ingredients(self):
        self.ui_ing_dialog.show()

    def add_step(self):

        # Need this if-else because of the initialised row count
        if self.ui.lwt_instructions.rowCount() > 0:
            tgt_row = self.ui.lwt_instructions.rowCount()
        else:
            tgt_row = 0

        self.ui.lwt_instructions.insertRow(tgt_row)
        self.ui.lwt_instructions.setItem(tgt_row, 0, QtWidgets.QTableWidgetItem(""))

    def delete_step(self):
        curr_row = self.ui.lwt_instructions.currentRow()
        self.ui.lwt_instructions.removeRow(curr_row)

    def add_nutrition_to_tree(self, root):
        nutrition = et.SubElement(root, "nutrition")
        add_to_tree(nutrition, "kilocalories", self.ui.sbx_calories.text())

        column_headers = ["name", "quantity", "unit"]
        nutrition_data = find_nutrition_table(self.ui)

        for i in range(len(nutrition_data)):
            nutrient = et.SubElement(nutrition, "nutrient")
            for j in range(len(column_headers)):
                add_to_tree(nutrient, column_headers[j], nutrition_data[i][j])

    def add_instructions_to_tree(self, root):
        instructions = et.SubElement(root, "instructions")
        for i in range(self.ui.lwt_instructions.rowCount()):
            add_to_tree(instructions, "step", self.ui.lwt_instructions.item(i, 0).text())

    def add_ingredients_to_tree(self, root):
        ingredients = et.SubElement(root, "ingredients")
        column_headers = ["name", "notes", "quantity", "unit", "staple"]
        for i in range(self.ui.lwt_ingredients.rowCount()):
            ingredient = et.SubElement(ingredients, "ingredient")
            for j in range(self.ui.lwt_ingredients.columnCount()):
                add_to_tree(ingredient, column_headers[j], self.ui.lwt_ingredients.item(i, j).text())

    def export(self):

        root = et.Element("recipe", nsmap={'xsi': "http://www.w3.org/2001/XMLSchema-instance"})

        add_to_tree(root, "name", self.ui.led_recipe_name.text())
        add_to_tree(root, "serves", self.ui.sbx_serves.text())
        if not (self.ui.ted_prep_time.text() == "0:00"):
            hrs = str(self.ui.ted_prep_time.time().hour())
            mns = str(self.ui.ted_prep_time.time().minute())

            time = "PT" + hrs + "H" + mns + "M"
            add_to_tree(root, "prepTime", time)
        if not (self.ui.ted_cook_time.text() == "0:00"):

            hrs = str(self.ui.ted_cook_time.time().hour())
            mns = str(self.ui.ted_cook_time.time().minute())

            time = "PT" + hrs + "H" + mns + "M"
            add_to_tree(root, "cookTime", time)

        if self.ui.gbx_nutrition.isChecked():
            self.add_nutrition_to_tree(root)

        self.add_ingredients_to_tree(root)
        self.add_instructions_to_tree(root)

        self.write_to_file(root)

    def write_to_file(self, root):

        try:
            tree = et.ElementTree(root, parser=parser)

            file_location = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))

            if os.path.exists(file_location):
                tmp = file_location + "/" + self.ui.led_recipe_name.text().replace(" ", "_").lower() + ".xml"
                tmp.replace("/", "\\")

                with open(tmp, 'wb') as f:
                    tree.write(f, encoding="utf-8", xml_declaration=True, pretty_print=True)

        except et.XMLSyntaxError as e:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage(str(e.error_log))

    def clear_all(self):
        clear_all(self.ui)

    def populate_table(self):

        table = self.ui_ing_dialog.get_table()
        new_row_count = table.rowCount()
        new_col_count = table.columnCount()

        self.ui.lwt_ingredients.setRowCount(new_row_count)

        for row_num in range(new_row_count):
            for col_num in range(new_col_count):
                self.ui.lwt_ingredients.setItem(row_num, col_num,
                                                QtWidgets.QTableWidgetItem(table.item(row_num, col_num).text()))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my_form = ControlRecipeAdder()
    my_form.show()
    sys.exit(app.exec_())