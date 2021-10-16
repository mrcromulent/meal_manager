import lxml.etree as et
from PyQt5.QtCore import QTime


def add_to_tree(parent, tag_name, value):
    tmp = et.SubElement(parent, tag_name)
    tmp.text = value


def find_nutrition_units(s):
    return s[s.find("(") + 1:s.find(")")]


def find_nutrition_table(ui):
    nutrition_data = [
        ["Total Fat", ui.sbx_total_fat.text(), find_nutrition_units(ui.lbl_total_fat.text())],
        ["Saturated Fat", ui.sbx_saturated_fat.text(), find_nutrition_units(ui.lbl_saturated_fat.text())],
        ["Cholesterol", ui.sbx_cholesterol.text(), find_nutrition_units(ui.lbl_cholesterol.text())],
        ["Sodium", ui.sbx_sodium.text(), find_nutrition_units(ui.lbl_sodium.text())],
        ["Total Carbohydrates", ui.sbx_total_carbohydrates.text(),
         find_nutrition_units(ui.lbl_total_carbohydrates.text())],
        ["Dietary Fibre", ui.sbx_dietary_fibre.text(), find_nutrition_units(ui.lbl_dietary_fibre.text())],
        ["Total Sugars", ui.sbx_total_sugars.text(), find_nutrition_units(ui.lbl_total_sugars.text())],
        ["Protein", ui.sbx_protein.text(), find_nutrition_units(ui.lbl_protein.text())],
        ["Vitamin D", ui.sbx_vitamin_d.text(), find_nutrition_units(ui.lbl_vitamin_d.text())],
        ["Calcium", ui.sbx_calcium.text(), find_nutrition_units(ui.lbl_calcium.text())],
        ["Iron", ui.sbx_iron.text(), find_nutrition_units(ui.lbl_iron.text())],
        ["Potassium", ui.sbx_potassium.text(), find_nutrition_units(ui.lbl_potassium.text())]]

    return nutrition_data


def clear_all(ui):
    ui.led_recipe_name.clear()
    ui.sbx_serves.clear()
    ui.ted_prep_time.setTime(QTime(0, 0))
    ui.ted_cook_time.setTime(QTime(0, 0))

    ui.sbx_calories.clear()
    ui.sbx_total_fat.clear()
    ui.sbx_saturated_fat.clear()
    ui.sbx_cholesterol.clear()
    ui.sbx_sodium.clear()
    ui.sbx_total_carbohydrates.clear()
    ui.sbx_dietary_fibre.clear()
    ui.sbx_total_sugars.clear()
    ui.sbx_protein.clear()
    ui.sbx_vitamin_d.clear()
    ui.sbx_calcium.clear()
    ui.sbx_iron.clear()
    ui.sbx_potassium.clear()

    ui.lwt_instructions.setRowCount(0)
    ui.lwt_ingredients.setRowCount(0)
