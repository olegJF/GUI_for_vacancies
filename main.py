import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from gui import Ui_mainWindow
import requests


class VacancyGetter(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.url = 'https://jobfinderapp.herokuapp.com/api/v1'
        self.cities_row = []
        self.cities = {}
        self.sp_row = []
        self.sp = {}
        self.set_cities()
        self.set_sp()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.set_comboBox()
        self.init_GUI()

    def init_GUI(self):
        self.ui.pushButton.clicked.connect(self.get_data)

    def set_cities(self):
        url = self.url + '/cities/'
        resp = requests.get(url)
        if resp.status_code == 200:
            self.cities_row = resp.json()
            for row in self.cities_row:
                self.cities[row['name']] = row['slug']

    def set_sp(self):
        url = self.url + '/specialties/'
        resp = requests.get(url)
        if resp.status_code == 200:
            self.sp_row = resp.json()
            for row in self.sp_row:
                self.sp[row['name']] = row['slug']

    def set_comboBox(self):
        _translate = QtCore.QCoreApplication.translate
        for i, row in enumerate(self.cities_row):
            self.ui.comboBox_city.addItem("")
            name = row['name']
            self.ui.comboBox_city.setItemText(
                i, _translate("mainWindow", name))

        for i, row in enumerate(self.sp_row):
            self.ui.comboBox_laguage.addItem("")
            name = row['name']
            self.ui.comboBox_laguage.setItemText(
                i, _translate("mainWindow", name))

    def get_data(self):
        city = str(self.ui.comboBox_city.currentText())
        sp = str(self.ui.comboBox_laguage.currentText())
        params = '/vacancies/?city={}&sp={}'.format(
            self.cities[city], self.sp[sp]
        )
        date = self.ui.date
        if date:
            date_str = date.toString('yyyy-MM-dd')
            params += f'&date={date_str}'
        url = self.url + params
        resp = requests.get(url)
        if resp.status_code == 200:
            text = ''
            for i, row in enumerate(resp.json(), 1):
                description = row["description"].replace('\n', ' ').replace('\t', ' ').strip()
                title = row["title"].replace('\n', '')
                text += f'{i}) {title}\n{description}\n{row["url"]}\n{row["timestamp"]}\n\n'
            if not text:
                text = 'Согласно Вашего запроса данные отсутствуют. Измените параметры'
            self.ui.textBrowser.setText(text)
        else:
            self.ui.textBrowser.setText(str(resp.status_code))


app = QtWidgets.QApplication([])
application = VacancyGetter()
application.show()

sys.exit(app.exec())

# pyuic5 gui.ui -o gui.py -x
