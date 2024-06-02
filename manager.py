from PySide6.QtGui import QMovie, QIcon, QPixmap
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import QPropertyAnimation
from building_the_model import NeuralNetworkClassifier
from gui_creation import UiMainWindow


class MainWindowManager(QMainWindow):
    def __init__(self):
        super(MainWindowManager, self).__init__()
        self.ui = UiMainWindow(self)
        icon = QIcon('C:/Users/ryszk/PycharmProjects/NeuralNetworkClassifier/Images/icon.png')
        self.setWindowIcon(icon)

        self.ui.pushButton.clicked.connect(self.open_directory_dialog)
        self.ui.pushButton_2.clicked.connect(self.go_to_second_page)
        self.ui.pushButton_7.clicked.connect(self.go_to_second_page)
        self.ui.pushButton_6.clicked.connect(self.go_to_first_page)
        self.ui.pushButton_5.clicked.connect(self.go_to_third_page)
        self.ui.pushButton_8.clicked.connect(self.build_and_train_the_model)
        self.ui.pushButton_9.clicked.connect(self.exit_application)
        self.ui.pushButton_10.clicked.connect(self.go_to_second_page)
        self.ui.pushButton_11.clicked.connect(self.go_to_first_page)

        self.pixmap = QPixmap('C:/Users/ryszk/PycharmProjects/NeuralNetworkClassifier/Images/roc.png')
        self.ui.label_34.setPixmap(self.pixmap)

        self.movie = QMovie('C:/Users/ryszk/PycharmProjects/NeuralNetworkClassifier/Images/neural.gif')
        self.ui.label_2.setMovie(self.movie)

        self.movie.setSpeed(170)
        self.movie.start()
        self.activation_dict = {'Exponential Linear Unit': 'elu',
                                'Rectified Linear Unit': 'rlu',
                                'Tanh': 'tanh',
                                'Sigmoidal': 'sigmoid',
                                'Softmax': 'softmax',
                                'Swish': 'swish',
                                'Hard Sigmoidal': 'hard_sigmoid'
                                }
        self.model = None
        self.predictions = None
        self.conf_matrix = None
        self.accuracy = 99.99
        self.precision = 99.99
        self.recall = 99.99
        self.f1 = 99.99

        self.animation_1 = QPropertyAnimation(self.ui.progressBar, b"value")
        self.animation_1.setDuration(1000)
        self.animation_1.setStartValue(0)
        self.animation_1.setEndValue(100)

        self.animation_2 = QPropertyAnimation(self.ui.progressBar_2, b"value")
        self.animation_2.setDuration(1500)
        self.animation_2.setStartValue(0)
        self.animation_2.setEndValue(100)

        self.animation_3 = QPropertyAnimation(self.ui.progressBar_3, b"value")
        self.animation_3.setDuration(2000)
        self.animation_3.setStartValue(0)
        self.animation_3.setEndValue(100)

        self.animation_4 = QPropertyAnimation(self.ui.progressBar_4, b"value")
        self.animation_4.setDuration(2500)
        self.animation_4.setStartValue(0)
        self.animation_4.setEndValue(100)

    def open_directory_dialog(self):
        directory = QFileDialog.getExistingDirectory(self, "Open Directory", "", QFileDialog.Option.ShowDirsOnly)
        if directory:
            self.ui.lineEdit.setText(directory)
            try:
                path_train = directory + '/' + 'prepared_data_train.csv'
                path_test = directory + '/' + 'prepared_data_test.csv'
                path_val = directory + '/' + 'prepared_data_val.csv'
                self.model = NeuralNetworkClassifier(path_train, path_test, path_val)
                QMessageBox.information(self, "Data loaded successfully.", directory)
                self.ui.pushButton_2.setEnabled(True)
            except FileNotFoundError:
                QMessageBox.information(self, "Correct data not found.", directory)

    def go_to_first_page(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def go_to_second_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def go_to_third_page(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def go_to_fourth_page(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def exit_application(self):
        self.close()

    def start_first_animation(self):
        self.animation_1.start()

    def start_second_animation(self):
        self.animation_2.start()

    def start_third_animation(self):
        self.animation_3.start()

    def start_fourth_animation(self):
        self.animation_4.start()

    def build_and_train_the_model(self):
        self.ui.pushButton_7.setEnabled(False)
        self.ui.pushButton_8.setEnabled(False)
        use_PReLu = self.ui.checkBox.isChecked()
        first_neurons = self.ui.spinBox_3.value()
        second_neurons = self.ui.spinBox_4.value()
        third_neurons = self.ui.spinBox_5.value()

        first_activation = self.activation_dict.get(self.ui.comboBox.currentText())
        second_activation = self.activation_dict.get(self.ui.comboBox_2.currentText())
        third_activation = self.activation_dict.get(self.ui.comboBox_3.currentText())
        output_activation = self.activation_dict.get(self.ui.comboBox_4.currentText())

        first_lambda = self.ui.doubleSpinBox.value()
        second_lambda = self.ui.doubleSpinBox_2.value()
        third_lambda = self.ui.doubleSpinBox_3.value()
        output_lambda = self.ui.doubleSpinBox_4.value()

        self.start_first_animation()
        self.start_second_animation()
        self.start_third_animation()
        self.start_fourth_animation()
        self.model.build_the_model(use_PReLu=use_PReLu, first_neurons=first_neurons, first_activation=first_activation,
                                   first_lambda=first_lambda, second_neurons=second_neurons,
                                   second_activation=second_activation, second_lambda=second_lambda,
                                   third_neurons=third_neurons, third_activation=third_activation,
                                   third_lambda=third_lambda, output_activation=output_activation,
                                   output_lambda=output_lambda)
        self.model.train()

        self.ui.pushButton_7.setEnabled(True)
        self.ui.pushButton_8.setEnabled(True)

        self.predictions = self.model.predict()
        self.accuracy, self.precision, self.recall, self.f1, self.conf_matrix = self.model.evaluate(self.predictions)

        self.ui.label_36.setText(f'{self.accuracy * 100:.2f}%')
        self.ui.label_37.setText(f'{self.precision * 100:.2f}%')
        self.ui.label_38.setText(f'{self.f1 * 100:.2f}%')
        self.ui.label_39.setText(f'{self.recall * 100:.2f}%')

        self.ui.label_43.setText(f'{self.conf_matrix[0][1]}')
        self.ui.label_44.setText(f'{self.conf_matrix[1][1]}')
        self.ui.label_45.setText(f'{self.conf_matrix[1][0]}')
        self.ui.label_46.setText(f'{self.conf_matrix[0][0]}')

        self.model.plot_roc_curve(self.predictions)
        self.pixmap = QPixmap('C:/Users/ryszk/PycharmProjects/NeuralNetworkClassifier/Images/curve.png')

        self.go_to_fourth_page()
