import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import librosa
import datetime


def get_spectrogram(filepath: str, window_len=1.0):
    spec_list = []
    spec_paths_list = []
    signal, sample_rate = librosa.load(filepath)
    nfft = 256

    if window_len * sample_rate > signal.shape[0]:
        window_len = signal.shape[0] / sample_rate
        #return spec_list, spec_paths_list, f"Ошибка: размер окна ({window_len} сек) превышает длительность сигнала ({round(signal.shape[0] / sample_rate, 2)} сек)"

    spec_count = int(signal.shape[0] // (window_len * sample_rate))
    max_length = spec_count * int(window_len * sample_rate)
    signal = signal[:max_length].reshape((spec_count, -1))

    dt = datetime.datetime.now()
    SPEC_DIR = f"{os.getcwd()}\\cashe\\spectrograms_{dt.day}{dt.month}{dt.year}_{dt.hour}{dt.minute}"
    os.makedirs(SPEC_DIR, exist_ok=True)

    for id in range(signal.shape[0]):
        spec, _, _, cax = plt.specgram(signal[id, :], NFFT=nfft, noverlap=nfft // 2, Fs=sample_rate, cmap='jet')
        spec = np.flipud(10. * np.log10(spec))
        spec = (spec - spec.min()) / (spec.max() - spec.min())
        spec = spec * 255
        spec = spec.astype(np.uint8)
        img = cv2.applyColorMap(spec, colormap=cv2.COLORMAP_JET)
        img_path = SPEC_DIR + '\\' + f"spectrogram_{id}.png"
        cv2.imwrite(img_path, img)
        spec_list.append(img)
        spec_paths_list.append(img_path)
        plt.close("all")
    return spec_list, spec_paths_list, ''


if __name__ == "__main__":
    filepath = "D:\RadarAnalyzeApplication\спутник и шум.WAV"
    win_size = 1.5
    print(get_spectrogram(filepath, win_size))
