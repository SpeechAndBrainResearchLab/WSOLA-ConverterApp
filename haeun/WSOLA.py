import numpy as np
import pytsmod as tsm
import soundfile as sf  # you can use other audio load packages.


def convert(source_path: str, target_speed: float):
    x, sr = sf.read(source_path)
    x = x.T  # if the input is multichannel audio, it is recommended to use the shape (num_channels, audio_len)
    x_length = x.shape[-1]

    s_ap = np.array([[0, x_length / 2, x_length], [0, x_length, x_length * 1.5]])  # double the first half of the audio only and preserve the other half.

    x_s_fixed = tsm.wsola(x, target_speed)
    x_s_ap = tsm.wsola(x, s_ap)

    sf.write(source_path.replace('.wav', f'_EDIT_{target_speed}.wav'),
            x_s_fixed,
            44100)