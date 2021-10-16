import sys
from PyQt5 import QtWidgets
import widget_add_edit_ingredients


class ControlAddEditIngredients(QtWidgets.QDialog):

    def __init__(self, parent=None):
        # Parent class constructor
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = widget_add_edit_ingredients.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.btn_add.clicked.connect(self.add)
        self.ui.btn_replace.clicked.connect(self.replace)
        self.ui.btn_delete.clicked.connect(self.delete)

    def add(self):

        if self.ui.led_name.text() and self.ui.led_units.text() and self.ui.sbx_quantity.value() != 0:
            data_list = [self.ui.led_name.text(),
                         self.ui.led_notes.text(),
                         str(self.ui.sbx_quantity.value()),
                         self.ui.led_units.text(),
                         str(self.ui.rad_staple.isChecked())]

            new_row_count = self.ui.tbl_ingredients.rowCount() + 1
            self.ui.tbl_ingredients.setRowCount(new_row_count)

            for elem_num, elem_val in enumerate(data_list):
                self.ui.tbl_ingredients.setItem(new_row_count - 1, elem_num, QtWidgets.QTableWidgetItem(elem_val))

            self.ui.led_name.clear()
            self.ui.led_units.clear()
            self.ui.sbx_quantity.clear()
            self.ui.led_notes.clear()
            self.ui.rad_staple.setChecked(False)

    def replace(self):
        self.delete()
        self.add()

    def delete(self):
        curr_row = self.ui.tbl_ingredients.currentRow()
        self.ui.tbl_ingredients.removeRow(curr_row)

    def get_table(self):
        return self.ui.tbl_ingredients


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = ControlAddEditIngredients()
    form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
