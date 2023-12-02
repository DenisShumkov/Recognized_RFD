# A means of automatic classification of objects emitting radio-electronic signals by their graphic portraits. Version 1.0

### 1. Input parameters:
‒ value of the width of the signal fragmentation window

‒ the path to the directory of the trained convolutional neural network model, the directory contains the following files:

• file of the trained convolutional neural network format.pth, 

• file description of the format model .json with the fields:

a) “model_name" – the name of the model architecture,

b) “model_path" – the full path to the .pth file of the trained neural network,

c) “classes" – a dictionary of the correspondence of class names to their index

d) “image_size" – the value of the image size

e) "acc" – the value of the average accuracy of the model determined at the training stage;

‒ classified radio broadcast in the format .wav.

### 2. Output data:

‒ a window showing spectrograms of audio signal fragments;

‒ name of the class of the corresponding spectrogram; 

‒ the reliability value as a percentage of the classification of objects emitting radio-electronic signals in the selected fragment of the radio broadcast.


## A control example of the work.
The selection and input of the source data is carried out in the initial dialog box (Figure 1). 
To download the audio signal file, click on the "Select audio signal file" button. To enter the value of the width of the window, you must enter a fractional number (the separator is ".").
To teach the spectrograms, you need to click on the "Teach the spectrogram" button, as a result, a new window will open, which displays the spectrogram of the current audio fragment, to change the audio fragment, you need to press the "Forward" or "Backward" button (Figure 2).
To download the classification model, enter the full path to the directory where the model file and the model description file are located in the "Specify the model directory:" 
field and click the "Upload model" button. As a result, the "*model description*" window displays information about the loaded model (Figure 3).

# Средство автоматической классификации объектов, излучающих радиоэлектронные сигналы, по их графическим портретам. Версия 1.0

### 1. Входные параметры:
‒ значение ширины окна фрагментации сигнала

‒ путь к каталогу обученной модели сверточной нейронной сети, каталог содержит следующие файлы:

• файл обученной сверточной нейронной сети format.pth,

• описание файла формата модели .json с полями:

а) «имя_модели» – название архитектуры модели,

б) «model_path» – полный путь к .pth файлу обученной нейронной сети,

в) «классы» – словарь соответствия названий классов их индексу.

г) «image_size» – значение размера изображения

д) «acc» – значение средней точности модели, определенное на этапе обучения;

‒ секретное радиовещание в формате .wav.

### 2. Выходные данные:

‒ окно отображения спектрограмм фрагментов аудиосигнала;

‒ название класса соответствующей спектрограммы;

‒ значение достоверности в процентах от классификации объектов, излучающих радиоэлектронные сигналы, в выделенном фрагменте радиопередачи.


## Контрольный пример работы.
Выбор и ввод исходных данных осуществляется в начальном диалоговом окне (рис. 1).
Чтобы скачать файл аудиосигнала, нажмите кнопку «Выбрать файл аудиосигнала». Для ввода значения ширины окна необходимо ввести дробное число (разделитель — «.»).
Для обучения спектрограммы необходимо нажать на кнопку «Обучить спектрограмму», в результате откроется новое окно, в котором отображается спектрограмма текущего аудиофрагмента, для изменения аудиофрагмента необходимо нажать кнопку « Кнопка «Вперед» или «Назад» (рис. 2).
Чтобы скачать модель классификации, введите полный путь к каталогу, в котором находятся файл модели и файл описания модели, в поле «Укажите каталог модели:»
поле и нажмите кнопку «Загрузить модель». В результате в окне «*описание модели*» отображается информация о загруженной модели (рис. 3).
Процедура классификации спектрограмм запускается кнопкой «Классификация сигнала».
Результатом работы станет добавление в окно отображения спектрограммы фрагмента аудиосигнала информации о названии класса сигнала и достоверности отнесения сигнала к этому классу (рисунок 4).
The spectrogram classification procedure is started by the "Signal Classification" button. 
The result of the work will be the addition to the window displaying the spectrogram of an audio signal fragment, information about the name of the signal class and the reliability of assigning the signal to this class (Figure 4).
