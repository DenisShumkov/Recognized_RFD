# -*- coding: utf-8 -*-
from PyQt6 import QtWidgets, QtCore, QtGui
from spectrogram import get_spectrogram
from classificator_inference import InferenceCNN
import os


class SpectrogramWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.id = 0
        self.image_label = QtWidgets.QLabel()
        self.pred_label = QtWidgets.QLabel()
        self.pred_label.setHidden(True)
        self.next_button = QtWidgets.QPushButton("Вперёд")
        self.prev_button = QtWidgets.QPushButton("Назад")

        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.prev_button)
        self.hbox.addWidget(self.next_button)
        self.vbox.addWidget(self.image_label)
        self.vbox.addWidget(self.pred_label)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)

        self.next_button.clicked.connect(self.on_clicked_next_button)
        self.prev_button.clicked.connect(self.on_clicked_prev_button)

        self.spec_fig = QtGui.QImage()
        self.painter = QtGui.QPainter()
        self.image_paths_list = list()
        self.images = None
        self.preds = None

    def load_images(self, image_paths_list):
        self.image_paths_list = image_paths_list
        self.images = [QtGui.QPixmap(image_path) for image_path in image_paths_list]
        self.show_spectrogram()

    def show_spectrogram(self):
        self.image_label.setPixmap(self.images[self.id])
        if self.preds is not None:
            self.pred_label.setText(f"Класс: {self.preds[self.id][0]}   Вероятность: {self.preds[self.id][1]*100:.2f}%")

    def on_clicked_next_button(self):
        self.id += 1
        if self.id > len(self.image_paths_list)-1: self.id = 0
        self.show_spectrogram()

    def on_clicked_prev_button(self):
        self.id -= 1
        if self.id < 0: self.id = len(self.image_paths_list) - 1
        self.show_spectrogram()

    def set_predictions(self, preds):
        self.pred_label.setHidden(False)
        self.preds = preds
        self.show_spectrogram()


class ErrorWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowFlag(QtCore.Qt.WindowType.Popup)
        self.resize(100, 100)
        # TODO: выравнять окно по центру
        # desktop = QtGui.QGuiApplication.desctop()
        # x = (desktop.width() - window.width()) // 2
        # y = (desktop.height() - window.height()) // 2
        # self.move(x, y)

        self.err_message = QtWidgets.QLabel("")
        self.err_message.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.ok_button = QtWidgets.QPushButton("Ок")
        self.ok_button.clicked.connect(self.close)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.err_message)
        self.vbox.addWidget(self.ok_button)
        self.setLayout(self.vbox)


class StartWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle("Конвертация аудиосигнала в спектрограмму")
        self.resize(300, 100)

        self.choice_button = QtWidgets.QPushButton("Выбрать файл аудиосигнала")
        self.filepath_line = QtWidgets.QLineEdit()
        self.ws_text = QtWidgets.QLabel("Укажите ширину окна, сек")
        self.choice_ws = QtWidgets.QLineEdit()
        validator = QtGui.QRegularExpressionValidator(
            # Только вещественные числа
            QtCore.QRegularExpression("[0-9]*\.[0-9]*"))
        self.choice_ws.setValidator(validator)
        self.push_button = QtWidgets.QPushButton("Получить спектрограмму")
        self.push_button.setDisabled(True)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.choice_button)  # self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.filepath_line)
        self.vbox.addWidget(self.ws_text)
        self.vbox.addWidget(self.choice_ws)
        self.vbox.addWidget(self.push_button)

        self.cnn_model = InferenceCNN()
        self.model_path_line = QtWidgets.QLineEdit()
        self.form = QtWidgets.QFormLayout()
        self.form.addRow("&Укажите директорию модели:", self.model_path_line)
        self.loadmodel_button = QtWidgets.QPushButton("Загрузить модель")
        self.loadmodel_button.setDisabled(True)
        self.model_discrp_text = QtWidgets.QTextEdit("*описание модели*\n")
        self.model_discrp_text.setReadOnly(True)

        self.v1box = QtWidgets.QVBoxLayout()
        self.v1box.addLayout(self.form)
        self.v1box.addWidget(self.loadmodel_button)
        self.v1box.addWidget(self.model_discrp_text)

        self.pred_button = QtWidgets.QPushButton("Классификация сигнала")
        self.pred_button.setDisabled(True)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addLayout(self.vbox)
        self.hbox.addLayout(self.v1box)

        self.vmainbox = QtWidgets.QVBoxLayout()
        self.vmainbox.addLayout(self.hbox)
        self.vmainbox.addWidget(self.pred_button)
        self.setLayout(self.vmainbox)

        self.loadmodel_button.clicked.connect(self.on_clicked_loadmodel_button)
        self.choice_button.clicked.connect(self.on_clicked_choice_button)
        self.push_button.clicked.connect(self.on_clicked_push_button)
        self.pred_button.clicked.connect(self.on_clicked_pred_button)

        self.spectrogramWindow = SpectrogramWindow()
        self.errWindow = ErrorWindow()

    def on_clicked_loadmodel_button(self):
        description = self.cnn_model.load_model(self.model_path_line.text())
        descr_text = "Наименование модели: " + description["model_name"] + \
                     "\nКлассы модели: " + ' '.join(description["classes"].keys()) + \
                     "\nСредняя точность классификации: " + str(description["acc"] * 100) + "%"
        self.model_discrp_text.setText(descr_text)
        self.pred_button.setDisabled(False)

    def on_clicked_pred_button(self):
        predictions = self.cnn_model.inference(self.spectrogramWindow.images)
        self.spectrogramWindow.set_predictions(predictions)

    def on_clicked_choice_button(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Выбрать аудиосигнал",
            QtCore.QDir.currentPath(),
            "Audio files (*.wav)")
        if filename:
            self.filepath_line.setText(filename)
            self.push_button.setDisabled(False)

    def on_clicked_push_button(self):
        self.spectrogramWindow.close()
        self.choice_button.setDisabled(True)
        self.push_button.setDisabled(True)

        ws = self.choice_ws.text()
        filepath = self.filepath_line.text()

        if ws == '' or float(ws) == 0.0:
            self.errWindow.err_message.setText(
                "Ошибка: введите корректное значение ширины окна")
            self.errWindow.show()
        elif not os.path.exists(filepath):
            self.errWindow.err_message.setText(
                f"Ошибка: указанного пути файла\n{filepath}\nне существует")
            self.errWindow.show()
        else:
            s, img_pths, err = get_spectrogram(filepath, float(ws))
            if err != '':
                self.errWindow.err_message.setText(err)
                self.errWindow.show()
            else:
                self.spectrogramWindow.id = 0
                self.spectrogramWindow.setWindowTitle(
                    f"Спектрограмма {os.path.basename(self.filepath_line.text())}")
                self.spectrogramWindow.show()
                self.spectrogramWindow.load_images(img_pths)

        self.choice_button.setDisabled(False)
        self.push_button.setDisabled(False)
        self.loadmodel_button.setDisabled(False)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec())
