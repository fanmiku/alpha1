import argparse
import pathlib
from utils import *
from tqdm import tqdm
from torchaudio.transforms import Resample
import torchaudio
import torch
import numpy as np
from audiomentations import Compose, ApplyImpulseResponse, Gain, Clip, AddGaussianNoise

def a(waveform_raw, sample_rate_raw): # 2bb8d80b-2369-4775-b4ba-44a927a40f1a

    # downsample
    sample_rate_low = 1050
    sample_rate_high = 44100 # 需要整除low
    resample = Resample(sample_rate_raw, sample_rate_low)
    waveform_sample = resample(waveform_raw)

    # zero padding
    upsample_ratio = sample_rate_high//sample_rate_low
    t = torch.zeros(1,(waveform_sample.shape[1])*upsample_ratio)
    t[0,::upsample_ratio] = waveform_sample 

    # design impulse signal
    x3= np.linspace(0, 5, upsample_ratio)
    ImpulseSignal = np.ones(upsample_ratio) +0.2*np.sinc(x3)
    ImpulseSignal = np.reshape(ImpulseSignal,(1,-1))
    makedirs_if_not_exists("testaudio")
    filepath="testaudio\impulse.wav"
    torchaudio.save(filepath, torch.from_numpy(ImpulseSignal), 44100)

    # compose
    augment = Compose([
        ApplyImpulseResponse(ir_path="testaudio", p=1.0),
        Gain(min_gain_db=9.0,max_gain_in_db=9.0,p=1.0),
        Clip(a_min=-0.4,a_max=0.4,p=1.0)
    ])
    augmented_sound = augment(t.numpy(), sample_rate=44100)
    return torch.from_numpy(augmented_sound), 44100

def b(waveform_raw, sample_rate_raw): # 429e0cf5-6be3-4fce-a573-9ae4455fe499
    limit = 0.5
    is_count = False
    wave = waveform_raw.numpy()
    augment = Compose([
        AddGaussianNoise(min_amplitude=0.001,max_amplitude=0.003,p=1.0),
        Gain(min_gain_db=7.0,max_gain_in_db=7.0,p=1.0),
        Clip(a_min=-1.0,a_max=1.0,p=1.0),
    ])
    wave = augment(wave, sample_rate=16000)
    wavecopy =wave.copy()
    for point in range(0,wave.shape[1]):
        if abs(wave[0,point]) >= limit and is_count == False:
            is_count =True
            temppoint = point
            sign = int(np.sign(wave[0,point]))
        elif abs(wave[0,point]) <= limit and is_count == True:
            winlen = point-temppoint
            wavecopy[0,temppoint:point] -= sign*np.ones(winlen)
            is_count =False
    return torch.from_numpy(wavecopy), sample_rate_raw

METHOD = {"A":a, "B":b}
def main():
    parser = argparse.ArgumentParser(description="transform clean data to distorted data")
    parser.add_argument('-s', '--src', type=pathlib.Path, default = "sourceaudio",
                        help='dir for clean data(flac)')
    parser.add_argument('-d', '--dst', type=pathlib.Path, default = "outputaudio",
                        help='dir for export')
    parser.add_argument('--method', choices=METHOD, default="B",
                        help='choose a method a or b')
    args = parser.parse_args()

    src = args.src
    dst = args.dst
    makedirs_if_not_exists(dst)
    files = walk_files(src, "flac")
    func = METHOD[args.method]

    print("Transforming...")
    for f in tqdm(files):
        waveform_raw, sample_rate_raw = torchaudio.load(f)
        waveform_out, sample_rate_out = func(waveform_raw, sample_rate_raw)
        torchaudio.save(f.replace(str(src), str(dst)), waveform_out, sample_rate_out)
    print("complete transforming")

if __name__ == "__main__":
    main()
