from PyQt5 import QtWidgets, uic
import sys
import os
import math


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        ui_path = r"D:\Desktop\Coding\Personal\Progetti Python\KSP Utility Tool\kut.ui"
        uic.loadUi(ui_path, self)
        self.comb_push_button = self.findChild(QtWidgets.QPushButton, "combPushButton")
        self.comb_push_button.clicked.connect(self.calculate_button_pressed)

        self.comb_mass_line = self.findChild(QtWidgets.QLineEdit, "combLineEdit_1")
        self.comb_velo_line = self.findChild(QtWidgets.QLineEdit, "combLineEdit_2")

        self.comb_combo_box = self.findChild(QtWidgets.QComboBox, "combComboBox")
        self.comb_combo_box.activated.connect(self.calculate_velocity)

        self.comb_text_browser = self.findChild(QtWidgets.QTextBrowser, "combTextBrowser")
        self.comb_text_browser_2 = self.findChild(QtWidgets.QTextBrowser, "combTextBrowser_2")

        self.mk16_spin_box = self.findChild(QtWidgets.QSpinBox, "mk16SpinBox")
        self.mk16_spin_box.valueChanged.connect(self.calculate_velocity)

        self.mk2r_spin_box = self.findChild(QtWidgets.QSpinBox, "Mk2rSpinBox")
        self.mk2r_spin_box.valueChanged.connect(self.calculate_velocity)

        self.mk16xl_spin_box = self.findChild(QtWidgets.QSpinBox, "mk16lSpinBox")
        self.mk16xl_spin_box.valueChanged.connect(self.calculate_velocity)

        self.mk25_spin_box = self.findChild(QtWidgets.QSpinBox, "mk25SpinBox")
        self.mk25_spin_box.valueChanged.connect(self.calculate_velocity)

        self.mk12r_spin_box = self.findChild(QtWidgets.QSpinBox, "mk12rSpinBox")
        self.mk12r_spin_box.valueChanged.connect(self.calculate_velocity)

        self.velo_line_edit = self.findChild(QtWidgets.QLineEdit, "veloLineEdit_3")
        self.velo_line_edit.textChanged.connect(self.calculate_velocity)

        self.velo_text_browser = self.findChild(QtWidgets.QTextBrowser, "veloTextBrowser")

        self.show()

    def calculate_button_pressed(self):
        values = []
        message = ""
        mass = self.comb_mass_line.text()
        velocity = self.comb_velo_line.text()
        planet = self.comb_combo_box.currentText()

        if mass == "":
            mass = 0
        else:
            mass = float(mass)

        if velocity == "":
            velocity = 0
        else:
            velocity = float(velocity)

        if planet != "Select a Planet...":
            values = self.calculate_list_1(mass, velocity, planet)
            if values is not None:
                message = f"Mk16: {values[0]}\n" \
                          f"Mk2-R: {values[1]}\n" \
                          f"Mk16-XL: {values[2]}\n" \
                          f"Mk25 (drogue): {values[3]}\n" \
                          f"Mk12-R (radial drogue): {values[4]}"
                self.comb_text_browser.clear()
                self.comb_text_browser.setPlainText(message)

            values = self.calculate_list_2(mass, velocity, planet)
            if values is not None:
                message = f"Mk16: {values[0]}\n" \
                          f"Mk2-R: {values[1]}\n" \
                          f"Mk16-XL: {values[2]}\n" \
                          f"Mk25 (drogue): {values[3]}\n" \
                          f"Mk12-R (radial drogue): {values[4]}"
                self.comb_text_browser_2.clear()
                self.comb_text_browser_2.setPlainText(message)

    def calculate_list_1(self, mass, velocity, planet):
        if mass == 0 or velocity == 0:
            self.comb_text_browser.setPlainText("Error: Insert valid values")
            self.comb_text_browser_2.setPlainText("Error: Insert valid values")
            return
        result_list_1 = []
        for parachute in planets[planet]:
            result = planets[planet][parachute] * mass / (velocity ** 2)
            if result < 1:
                result = 1
            result = round(result)
            result_list_1.append(result)
        return result_list_1

    def calculate_list_2(self, mass, velocity, planet):
        if mass == 0 or velocity == 0:
            self.comb_text_browser.setPlainText("Error: Insert valid values")
            self.comb_text_browser_2.setPlainText("Error: Insert valid values")
            return
        result_list_2 = []
        for parachute in planets[planet]:
            result = (planets[planet][parachute] * mass / (velocity ** 2)) ** (1/1.5)
            if result < 1:
                result = 1
            result = round(result)
            result_list_2.append(result)
        return result_list_2

    def calculate_velocity(self):
        result = 0
        mass = self.velo_line_edit.text()
        if mass == "":
            mass = 0
        mass = float(mass)
        planet = self.comb_combo_box.currentText()
        mk16_amount = self.mk16_spin_box.value()
        mk2r_amount = self.mk2r_spin_box.value()
        mk16xl_amount = self.mk16xl_spin_box.value()
        mk25_amount = self.mk25_spin_box.value()
        mk12r_amount = self.mk12r_spin_box.value()

        if mass == 0:
            return
        if mk16_amount == 0 and mk2r_amount == 0 and mk16xl_amount == 0 and mk25_amount == 0 and mk12r_amount == 0:
            return
        if planet == "Select a Planet...":
            return
        result = self.calculate_velocity_math(mk16_amount, mk2r_amount, mk16xl_amount, mk25_amount, mk12r_amount, mass, planet)
        result = round(result, 1)
        self.velo_text_browser.clear()
        self.velo_text_browser.setPlainText(f"{result}")

    def calculate_velocity_math(self, mk16_amount, mk2r_amount, mk16xl_amount, mk25_amount, mk12r_amount, mass,  planet):
        mk2r_fraction = 0
        mk12r_fraction = 0

        mk16_fraction = mk16_amount / planets[planet]["mk16"]
        if mk2r_amount == 1:
            mk2r_fraction = (mk2r_amount ** 1) / planets[planet]["mk2r"]
        else:
            mk2r_fraction = (mk2r_amount ** 1.5) / planets[planet]["mk2r"]
        mk16xl_fraction = mk16xl_amount / planets[planet]["mk16xl"]
        mk25_fraction = mk25_amount / planets[planet]["mk25"]
        if mk12r_amount == 1:
            mk12r_fraction = (mk12r_amount ** 1) / planets[planet]["mk12r"]
        else:
            mk12r_fraction = (mk12r_amount ** 1.5) / planets[planet]["mk12r"]

        fraction_sum = mk16_fraction + mk2r_fraction + mk16xl_fraction + mk25_fraction + mk12r_fraction
        pre_sqrt_result = (1 / fraction_sum) * mass
        result = math.sqrt(pre_sqrt_result)

        return result


planets = {"Kerbin": {"mk16": 0.029, "mk2r": 0.039, "mk16xl": 0.020, "mk25": 1.099, "mk12r": 1.065},
           "Duna": {"mk16": 0.079, "mk2r": 0.105, "mk16xl": 0.054, "mk25": 2.967, "mk12r": 2.877},
           "Eve": {"mk16": 0.009, "mk2r": 0.012, "mk16xl": 0.006, "mk25": 0.340, "mk12r": 0.330},
           "Laythe": {"mk16": 0.036, "mk2r": 0.047, "mk16xl": 0.024, "mk25": 1.331, "mk12r": 1.291},
           }
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
