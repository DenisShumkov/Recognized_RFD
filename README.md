# A means of automatic classification of objects emitting radio-electronic signals by their graphic portraits. Version 1.0

1. Input parameters:
‒ value of the width of the signal fragmentation window /n
‒ the path to the directory of the trained convolutional neural network model, the directory contains the following files:
• file of the trained convolutional neural network format.pth, 
• file description of the format model .json with the fields:
a) “model_name" – the name of the model architecture,
b) “model_path" – the full path to the .pth file of the trained neural network,
c) “classes" – a dictionary of the correspondence of class names to their index
d) “image_size" – the value of the image size
e) "acc" – the value of the average accuracy of the model determined at the training stage;
‒ classified radio broadcast in the format .wav.

3. Output data:
‒ a window showing spectrograms of audio signal fragments;
‒ name of the class of the corresponding spectrogram; 
‒ the reliability value as a percentage of the classification of objects emitting radio-electronic signals in the selected fragment of the radio broadcast.


#A control example of the work.
The selection and input of the source data is carried out in the initial dialog box (Figure 1). 
To download the audio signal file, click on the "Select audio signal file" button. To enter the value of the width of the window, you must enter a fractional number (the separator is ".").
To teach the spectrograms, you need to click on the "Teach the spectrogram" button, as a result, a new window will open, which displays the spectrogram of the current audio fragment, to change the audio fragment, you need to press the "Forward" or "Backward" button (Figure 2).
To download the classification model, enter the full path to the directory where the model file and the model description file are located in the "Specify the model directory:" 
field and click the "Upload model" button. As a result, the "*model description*" window displays information about the loaded model (Figure 3).
The spectrogram classification procedure is started by the "Signal Classification" button. 
The result of the work will be the addition to the window displaying the spectrogram of an audio signal fragment, information about the name of the signal class and the reliability of assigning the signal to this class (Figure 4).
