import numpy as np
import pytsmod as tsm
import crepe  # you can use other pitch tracking algorithms.
import soundfile as sf  # you can use other audio load packages.


def convert(path):

    x, sr = sf.read(path)

    _, f0_crepe, _, _ = crepe.predict(x, sr, viterbi=True, step_size=10)

    x_double_stretched = tsm.tdpsola(x, sr, f0_crepe, alpha=2, p_hop_size=441, p_win_size=1470)  # hop_size and frame_length for CREPE step_size=10 with sr=44100
    x_3keyup = tsm.tdpsola(x, sr, f0_crepe, beta=pow(2, 3/12), p_hop_size=441, p_win_size=1470)
    x_3keydown = tsm.tdpsola(x, sr, f0_crepe, f0_crepe * pow(2, -3/12), p_hop_size=441, p_win_size=1470)