import sys
from execute import Execute
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QLabel, QPushButton, QLineEdit, \
    QComboBox, QWidget

app = QApplication([])

# Create a window which size is 480*560
window = QMainWindow()
window.resize(400, 350)
window.setWindowTitle("import_tool")

# Create a label and set its text
label = QLabel(window)
label.setText("log in neo4j")
# place it to left-top
label.move(10, 10)

# Create a button and set its text
line_edit1 = QLineEdit(window)
# set line_edit1 size = 200*30
line_edit1.resize(200, 30)
line_edit1.move(10, 40)
# set default text
line_edit1.setText("neo4j")
# set another two line_edit and set their default text
line_edit2 = QLineEdit(window)
line_edit2.resize(200, 30)
line_edit2.move(10, 80)
line_edit2.setText("password")
line_edit3 = QLineEdit(window)
line_edit3.resize(200, 30)
line_edit3.move(10, 120)
line_edit3.setText("http://localhost:7474")
#Create a line_edit to select xmind file




# Create window2
class Ui2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.list = None
        self.combo = None

        # create a sub widget to log in mysql
        self.widget = QWidget(self)
        self.widget.resize(400, 350)
        self.widget.setWindowTitle("import_tool")
        # add a button to log in mysql
        button2 = QPushButton(self.widget)
        button2.setText("log in")
        button2.move(10, 200)
        # storage all line_edit text when click button
        button2.clicked.connect(self.on_button_clicked_login_mysql)
        # add several line_edit for input message to log in mysql
        self.line_edit4 = QLineEdit(self.widget)
        self.line_edit4.resize(200, 30)
        self.line_edit4.move(10, 40)
        self.line_edit4.setText("localhost")
        self.line_edit5 = QLineEdit(self.widget)
        self.line_edit5.resize(200, 30)
        self.line_edit5.move(10, 80)
        self.line_edit5.setText("user")
        self.line_edit6 = QLineEdit(self.widget)
        self.line_edit6.resize(200, 30)
        self.line_edit6.move(10, 120)
        self.line_edit6.setText("password")
        self.line_edit7 = QLineEdit(self.widget)
        self.line_edit7.resize(200, 30)
        self.line_edit7.move(10, 160)
        self.line_edit7.setText("database")
        self.widget.close()

        # create a sub widget to select xlsx file
        self.widget2 = QWidget(self)
        self.widget2.resize(400, 350)
        self.widget2.setWindowTitle("import_tool")
        # add a button to select xlsx file
        button3 = QPushButton(self.widget2)
        button3.setText("select xlsx file")
        button3.move(10, 200)
        # storage all line_edit text when click button
        button3.clicked.connect(self.on_button_clicked_confirm_xlsx)
        # add a line_edit to show xlsx file path
        self.line_edit8 = QLineEdit(self.widget2)
        self.line_edit8.resize(200, 30)
        self.line_edit8.move(10, 40)
        self.line_edit8.setText("xlsx file path")
        # add a small button beside line_edit8 to open a QFiledialog to select xlsx file
        button4 = QPushButton(self.widget2)
        button4.setText("...")
        button4.move(220, 40)
        button4.clicked.connect(self.on_button_clicked_select_xlsx_file)
        self.widget2.close()

        # Create a sub widget start to import
        self.widget4 = QWidget(self)
        self.widget4.resize(400, 350)
        self.widget4.setWindowTitle("import_tool")
        # add a button to start to import
        button7 = QPushButton(self.widget4)
        button7.setText("start to import")
        button7.move(10, 200)
        button7.clicked.connect(self.on_button_clicked_start_import)
        self.widget4.close()

    def appoint_options(self, text):
        """
        for optional list
        :param text: 
        :return: 
        """
        self.widget2.close()
        self.widget.close()
        if text == "xlsx":
            self.xlsx_show()
        elif text == "mysql":
            self.mysql_show()
        else:
            QMessageBox.information(self, "information", "this function is not available now")

    def mysql_show(self):
        """
        :return:
        """
        self.widget.show()

    def xlsx_show(self):
        self.widget2.show()

    def import_show(self):
        self.widget.close()
        self.widget2.close()
        self.disable_combox()
        self.widget4.show()

    def furnish(self):
        self.resize(400, 350)
        self.setWindowTitle("import_tool")
        #  Create an optional list which include xlsx,mysql,and click it to choose
        self.list = ["xlsx", "mysql", "sql server", "oracle", "MongoDB", "csv"]
        self.combo = QComboBox(self)
        self.combo.resize(200, 30)
        self.combo.addItems(self.list)
        self.combo.move(10, 10)
        # call appoint_options function when choose an option
        self.combo.currentTextChanged.connect(self.appoint_options)

        self.widget2.show()

    def disable_combox(self):
        """
        disable combox when click button to import
        :return:
        """
        self.combo.setEnabled(False)

    def on_button_clicked_login_mysql(self):
        """
        for log in mysql
        :return:
        """

        # TODO:
        self.import_show()

        # try:
        #     execute.set_source("mysql", host=self.line_edit4.text(), user=self.line_edit5.text(),
        #                     password=self.line_edit6.text(), database=self.line_edit7.text())
        #     QMessageBox.information(self, "success", "log in mysql successfully")
        #     self.select_xmind()
        # except Exception as e:
        #     QMessageBox.critical(self, "error", str(e))

    def on_button_clicked_confirm_xlsx(self):
        """
        to confirm xlsx file path
        :return:
        """
        self.import_show()

    def on_button_clicked_select_xlsx_file(self):
        """
        open QFileDialog to select xlsx file
        :return:
        """
        # Generate a QFileDialog instance to elect xlsx file
        file_dialog = QFileDialog(self.widget2)
        # set file_dialog title
        file_dialog.setWindowTitle("select xlsx file")
        # set file_dialog filter
        file_dialog.setNameFilter("xlsx(*.xlsx)")
        # set file_dialog path
        file_dialog.setDirectory("./")
        # get file_dialog path
        file_dialog.fileSelected.connect(self.line_edit8.setText)
        file_dialog.show()

    def on_button_clicked_start_import(self):
        QMessageBox.information(self, "success", "import successfully")


execute = Execute()
Ui2 = Ui2()


def on_button_clicked():
    """
    when click button, execute this function
    :return:
    """
    neo4j = line_edit1.text()
    password = line_edit2.text()
    url = line_edit3.text()

    # TODO:
    bl = [True]
    if bl[0]:
        QMessageBox.information(window, "success", "log in neo4j successfully")
        window.close()
        Ui2.furnish()
        execute.set_xmind_path(line_edit5.text())
        Ui2.show()
    else:
        QMessageBox.information(window, "fail", "log in neo4j failed")
        #  show b[1] by MessageBox
        QMessageBox.information(window, "fail", str(bl[1]))

def on_button_clicked_select_xmind():
    """
    open QFileDialog to select xmind file
    :return:
    """
    # Generate a QFileDialog instance to elect xmind file
    file_dialog = QFileDialog(window)
    # set file_dialog title
    file_dialog.setWindowTitle("select xmind file")
    # set file_dialog filter
    file_dialog.setNameFilter("xmind(*.xmind)")
    # set file_dialog path
    file_dialog.setDirectory("./")
    # get file_dialog path
    file_dialog.fileSelected.connect(line_edit5.setText)
    file_dialog.show()

#Create a line_edit to input the path of xmind
line_edit5=QLineEdit(window)
line_edit5.resize(200,30)
line_edit5.move(10,160)
line_edit5.setText("xmind path")
button_to_select_xmind=QPushButton(window)
button_to_select_xmind.setText("...")
button_to_select_xmind.resize(30,30)
button_to_select_xmind.move(220,160)
button_to_select_xmind.clicked.connect(on_button_clicked_select_xmind)



# Create a button and set its text
button = QPushButton(window)
button.setText("log in")
button.move(10, 200)
button.clicked.connect(on_button_clicked)


# storage all line_edit text when click button


window.show()
app.exec()
