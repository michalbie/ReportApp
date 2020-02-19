from ear_ui import *
from backend import *
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QObject, pyqtSignal


class MainWindow(QMainWindow, Ui_MainWindow, QObject):
    was_logged = pyqtSignal()

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        self.user = UserData()
        self.database = Database()
        self.connect_signals()
        self.check_if_logged()
        self.load_list_to_comboBox()
        self.show()

    def connect_signals(self):
        self.enter_button.pressed.connect(self.exit_login_page)
        self.enter_button.pressed.connect(self.set_user_data)
        self.was_logged.connect(self.exit_login_page)

        self.raport_button.pressed.connect(self.set_raport_page)
        self.generate_button.pressed.connect(self.set_generate_page)
        self.history_button.pressed.connect(self.set_history_page)

        self.submitRaport_button.pressed.connect(self.on_submit_raport)
        self.generateRaport_button.pressed.connect(self.on_generate_raport)
        self.push_button.pressed.connect(self.on_push_raport)

        self.history_comboBox.currentIndexChanged.connect(self.on_show_history)

    def exit_login_page(self):
        self.outer_stackedWidget.setCurrentIndex(1)

    def set_user_data(self):
        new_name = self.name_lineEdit.text()
        new_surname = self.surname_lineEdit.text()
        self.user.update_data(new_name, new_surname)

    def set_raport_page(self):
        self.inner_stackedWidget.setCurrentIndex(0)

    def set_generate_page(self):
        self.inner_stackedWidget.setCurrentIndex(1)

    def set_history_page(self):
        self.inner_stackedWidget.setCurrentIndex(2)

    def check_if_logged(self):
        if self.user.data['logged_once'] == 'Yes':
            self.was_logged.emit()

    def load_list_to_comboBox(self):
        list = self.database.load_dates_to_list()
        for date in list:
            self.history_comboBox.addItem(date)

    def on_submit_raport(self):
        if self.user.data['last_raport'] < self.database.db_data.today_format:
            self.database.send_raport(self.user.data['name'], self.user.data['surname'], self.raport_textEdit.toPlainText())
            self.raport_textEdit.clear()
            self.user.data['last_raport'] = self.database.db_data.today_format
            with open('data.json', 'w') as outfile:
                json.dump(self.user.data, outfile)
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "You have sent a report today.")

    def on_generate_raport(self):
        if self.ownerPassword_lineEdit.text() == self.user.data['owner_passwd']:
            raport = self.database.generate_raport()
            self.generatedRaport_textEdit.setReadOnly(False)
            self.generatedRaport_textEdit.setText(raport)
            self.generatedRaport_textEdit.setReadOnly(True)
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Wrong password. If you are not a boss, you can't generate daily report.")

    def on_push_raport(self):
        if self.database.check_if_pushed() == 0 and self.ownerPassword_lineEdit.text() == self.user.data['owner_passwd']:
            self.database.push_raport()
            QtWidgets.QMessageBox.information(self, "Pushed", "Today's report has been registered.")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Wrong password or you have already pushed a report.")

    def on_show_history(self):
        history_record = self.database.show_history(self.history_comboBox.currentText())
        self.history_textEdit.setReadOnly(False)
        self.history_textEdit.setText(history_record)
        self.history_textEdit.setReadOnly(True)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

#LUhC!I3eh)FASEJ( password for webpage
