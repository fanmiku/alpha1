__all__ = ["makedirs_if_not_exists","walk_files","plot_specgram","plot_wave"]
import os
import matplotlib.pyplot as plt

def makedirs_if_not_exists(dir_):
    if not os.path.exists(dir_):
        os.makedirs(dir_)

''' extract every file included in the path'''
def walk_files(root, extension):
    for path, dirs, files in os.walk(root):
        for file in files:
            if file.endswith(extension):
                yield os.path.join(path, file)

def plot_specgram(waveform, sample_rate, title="Spectrogram", method="save"):
    """plot a spectrum diagram for a given waveform and its sample_rate
    
    :param waveform: [channels, waveform]
    :param sample_rate: int
    :param title: Title of spectrogram, default:"Spectrogram"
    :param method: Use "save" to save image files whose filename is the same as its title in a subfolder named 'figs', use "show" to show the image only, default:"save"
    """
    num_channels, num_frames = waveform.shape
    figure, axes = plt.subplots(num_channels, 1)
    if num_channels == 1:
        axes = [axes]
    for c in range(num_channels):
        axes[c].specgram(waveform[c], Fs=sample_rate)
        if num_channels > 1:
            axes[c].set_ylabel(f"Channel {c+1}")
    figure.suptitle(title)
    makedirs_if_not_exists('figs')
    if method == "save":
        plt.savefig('figs/'+title+'.png')
    elif method == "show":
        plt.show(block=False)
    else:
        raise ValueError('param "method" should be "save" or "show"')


def plot_wave(waveform, sample_rate, title="Waveform",method="save"):
    """plot a waveform for a given waveform and its sample_rate
    
    :param waveform: [channels, waveform]
    :param sample_rate: int
    :param title: Title of image, default:"Waveform"
    :param method: Use "save" to save image files whose filename is the same as its title in a subfolder named 'figs', use "show" to show the image only, default:"save"
    """
    num_channels, num_frames = waveform.shape
    figure, axes = plt.subplots(num_channels, 1)
    if num_channels == 1:
        axes = [axes]
    for c in range(num_channels):
        axes[c].plot([i/sample_rate for i in range(num_frames)],waveform[c])
        if num_channels > 1:
            axes[c].set_ylabel(f"Channel {c+1}")
    figure.suptitle(title)
    makedirs_if_not_exists('figs')
    if method == "save":
        plt.savefig('figs/'+title+'.png')
    elif method == "show":
        plt.show(block=False)
    else:
        raise ValueError('param "method" should be "save" or "show"')