# -*- coding: utf-8 -*-
from collections import defaultdict
import numpy as np
import librosa
from num2words import num2words
from pydub import AudioSegment
import os
from scipy.io import wavfile
from scipy.signal import argrelextrema


def pitch_marks_fun(wav):
    autokorelacija = librosa.autocorrelate(wav)
    peeks = argrelextrema(autokorelacija, np.greater)
    start = peeks[0][0]
    f0 = np.where(autokorelacija == np.amax(autokorelacija[start:]))
    pitch_marks = np.arange(0, len(autokorelacija), int(f0[0]))
    return int(f0[0]), pitch_marks

def tts(buffer, wav, f0):
    return np.concatenate((buffer[:-f0], np.add(buffer[-f0:], wav[:f0]), wav[f0:]), axis=0)

text = "ovo je umjetna sinteza govora"

rootdirall = "C:\\Users\\NIKOLA\\Desktop\\ROGJ\\Difoni\\Baza\\DifoniAll\\"
alldifonidict = defaultdict(int)
for subdir, dirs, files in os.walk(rootdirall):
    alldifoni = files
    break
for tmp in alldifoni:
    alldifonidict[tmp] = 1

for i in text.split():
    if i.isdigit():
        text = text.replace(i, num2words(i, lang="sr"))

rootdirsplit = "C:\\Users\\NIKOLA\\Desktop\\ROGJ\\Difoni\\Baza\\Difoni\\"
for subdir, dirs, files in os.walk(rootdirsplit):
    files = set([file.split('_')[1].split('.')[0] for file in files])
    novo = files
    break

text = text.replace('dž', '#')
text = text.replace('lj', '(')
text = text.replace('ć', '^')
text = text.replace('č', '~')
text = text.replace('š', '{')
text = text.replace('ž', '`')
text = text.replace('đ', '}')
text = text.replace('nj', '!')

i = 0
flag = 0
difonidict = defaultdict(int)
for tmp in novo:
    difonidict[tmp] = 1

rijeci = text.split(' ')

#PSOLA
sample_rate, buffer = wavfile.read(rootdirall + "silsil.wav")
#LJEPLJENJE
ans = AudioSegment.silent(duration=1)

for i in range(len(rijeci)):
    if rijeci[i] in difonidict:

        rootdirword = "C:\\Users\\NIKOLA\\Desktop\\ROGJ\\Difoni\\Baza\\Difoni\\"
        for subdir, dirs, files in os.walk(rootdirword):
            novo = set([])
            for file in files:
                if(file.split('_')[1].split('.')[0] == rijeci[i]):
                    novo.add(file.split('_')[0] + '.wav')
            break

        rijecdict = defaultdict(int)
        for tmp in novo:
            rijecdict[tmp] = 1

        if i == 0:
            if "sil-" + rijeci[i][0] + ".wav" in rijecdict:
                #PSOLA
                sample_rate, wav = wavfile.read(rootdirsplit + "sil-" + rijeci[i][0] + "_" + rijeci[i] + ".wav")
                if not os.path.exists(rootdirsplit + "sil-" + rijeci[i][0] + "_" + rijeci[i] + ".txt"):
                    f0, pitch_marks = pitch_marks_fun(wav)
                    np.savetxt(rootdirsplit + "sil-" + rijeci[i][0] + "_" + rijeci[i] + ".txt", pitch_marks)
                else:
                    pitch_marks = np.loadtxt(rootdirsplit + "sil-" + rijeci[i][0] + "_" + rijeci[i] + ".txt")
                    f0 = int(pitch_marks[1])
                buffer = tts(buffer, wav, f0)
                #LJEPLJENJE
                ans += AudioSegment.from_wav(rootdirsplit + "sil-" + rijeci[i][0] + "_" + rijeci[i] + ".wav")
            elif "sil" + rijeci[i][0] + ".wav" in alldifonidict:
                
                # PSOLA
                sample_rate, wav = wavfile.read(rootdirall + "sil" + rijeci[i][0] + ".wav")
                if not os.path.exists(rootdirall + "sil" + rijeci[i][0] + ".txt"):
                    f0, pitch_marks = pitch_marks_fun(wav)
                    np.savetxt(rootdirall + "sil" + rijeci[i][0] + ".txt", pitch_marks)
                else:
                    pitch_marks = np.loadtxt(rootdirall + "sil" + rijeci[i][0] + ".txt")
                    f0 = int(pitch_marks[1])
                buffer = tts(buffer, wav, f0)
                # LJEPLJENJE
                ans += AudioSegment.from_wav(rootdirall + "sil" + rijeci[i][0] + ".wav")
            else:
                
                # PSOLA
                sample_rate, wav = wavfile.read(rootdirall + "silsil.wav")
                if not os.path.exists(rootdirall + "silsil.txt"):
                    f0, pitch_marks = pitch_marks_fun(wav)
                    np.savetxt(rootdirall + "silsil.txt", pitch_marks)
                else:
                    pitch_marks = np.loadtxt(rootdirall + "silsil.txt")
                    f0 = int(pitch_marks[1])
                buffer = tts(buffer, wav, f0)
                # LJEPLJENJE
                ans += AudioSegment.silent(duration=100)
            for j in range(0, len(rijeci[i]) - 1):
                if rijeci[i][j] + "-" + rijeci[i][j + 1] + ".wav" in rijecdict:
                    # PSOLA
                    sample_rate, wav = wavfile.read(rootdirsplit + rijeci[i][j] + "-" + rijeci[i][j + 1] + "_" + rijeci[i] + ".wav")
                    if not os.path.exists(rootdirsplit + rijeci[i][j] + "-" + rijeci[i][j + 1] + "_" + rijeci[i] + ".txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirsplit + rijeci[i][j] + "-" + rijeci[i][j + 1] + "_" + rijeci[i] + ".txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirsplit + rijeci[i][j] + "-" + rijeci[i][j + 1] + "_" + rijeci[i] + ".txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, 2)
                    # LJEPLJENJE
                    ans += AudioSegment.from_wav(
                        rootdirsplit + rijeci[i][j] + "-" + rijeci[i][j + 1] + "_" + rijeci[i] + ".wav")
                elif rijeci[i][j] + rijeci[i][j + 1] + ".wav" in alldifonidict:
                    
                    # PSOLA
                    sample_rate, wav = wavfile.read(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".wav")
                    if not os.path.exists(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.from_wav(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".wav")
                else:
                    # PSOLA
                    # nema
                    # LJEPLJENJE
                    print("nema")
            if i == len(rijeci) - 1:
                if rijeci[i][-1] + "sil.wav" in alldifonidict:
                    
                    # PSOLA
                    sample_rate, wav = wavfile.read(rootdirall + rijeci[i][-1] + "sil.wav")
                    if not os.path.exists(rootdirall + rijeci[i][-1] + "sil.txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirall + rijeci[i][-1] + "sil.txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirall + rijeci[i][-1] + "sil.txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.from_wav(rootdirall + rijeci[i][-1] + "sil.wav")
                else:
                    
                    # PSOLA
                    sample_rate, wav = wavfile.read(rootdirall + "silsil.wav")
                    if not os.path.exists(rootdirall + "silsil.txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirall + "silsil.txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirall + "silsil.txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.silent(duration=100)
        else:
            if rijeci[i - 1] + "-" + rijeci[i] in difonidict:
                sredinadict = defaultdict(int)
                rootdirword = "C:\\Users\\NIKOLA\\Desktop\\ROGJ\\Difoni\\Baza\\Difoni\\"
                for subdir, dirs, files in os.walk(rootdirword):
                    for file in files:
                        if ('-' in file.split('_')[0]):
                            novo.add(file.split('_')[0] + '.wav')
                    break
                for tmp in novo:
                    sredinadict[tmp] = 1
                if rijeci[i - 1][-1] + "-" + rijeci[i][0] + ".wav" in sredinadict:
                    # PSOLA
                    sample_rate, wav = wavfile.read(rootdirsplit +
                                                 rijeci[i - 1][-1] + "-" + rijeci[i][0] + "_" + rijeci[i - 1] + "-" + rijeci[i] + ".wav")
                    if not os.path.exists(rootdirsplit +
                                                 rijeci[i - 1][-1] + "-" + rijeci[i][0] + "_" + rijeci[i - 1] + "-" + rijeci[i] + ".txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirsplit +
                                                 rijeci[i - 1][-1] + "-" + rijeci[i][0] + "_" + rijeci[i - 1] + "-" + rijeci[i] + ".txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirsplit +
                                                 rijeci[i - 1][-1] + "-" + rijeci[i][0] + "_" + rijeci[i - 1] + "-" + rijeci[i] + ".txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.from_wav(rootdirsplit +
                                                 rijeci[i - 1][-1] + "-" + rijeci[i][0] + "_" + rijeci[i - 1] + "-" + rijeci[i] + ".wav")
                else:
                    if rijeci[i - 1][-1] + "sil.wav" in alldifonidict:
                        
                        # PSOLA
                        sample_rate, wav = wavfile.read(rootdirall + rijeci[i - 1][-1] + "sil.wav")
                        if not os.path.exists(rootdirall + rijeci[i - 1][-1] + "sil.txt"):
                            f0, pitch_marks = pitch_marks_fun(wav)
                            np.savetxt(rootdirall + rijeci[i - 1][-1] + "sil.txt", pitch_marks)
                        else:
                            pitch_marks = np.loadtxt(rootdirall + rijeci[i - 1][-1] + "sil.txt")
                            f0 = int(pitch_marks[1])
                        buffer = tts(buffer, wav, f0)
                        # LJEPLJENJE
                        ans += AudioSegment.from_wav(rootdirall + rijeci[i - 1][-1] + "sil.wav")
                        if "sil" + rijeci[i][0] + ".wav" in alldifonidict:
                            
                            # PSOLA
                            sample_rate, wav = wavfile.read(rootdirall + "sil" + rijeci[i][0] + ".wav")
                            if not os.path.exists(rootdirall + "sil" + rijeci[i][0] + ".txt"):
                                f0, pitch_marks = pitch_marks_fun(wav)
                                np.savetxt(rootdirall + "sil" + rijeci[i][0] + ".txt", pitch_marks)
                            else:
                                pitch_marks = np.loadtxt(rootdirall + "sil" + rijeci[i][0] + ".txt")
                                f0 = int(pitch_marks[1])
                            buffer = tts(buffer, wav, f0)
                            # LJEPLJENJE
                            ans += AudioSegment.from_wav(rootdirall + "sil" + rijeci[i][0] + ".wav")
                        else:
                            # PSOLA
                            
                            sample_rate, wav = wavfile.read(rootdirall + "silsil.wav")
                            if not os.path.exists(rootdirall + "silsil.txt"):
                                f0, pitch_marks = pitch_marks_fun(wav)
                                np.savetxt(rootdirall + "silsil.txt", pitch_marks)
                            else:
                                pitch_marks = np.loadtxt(rootdirall + "silsil.txt")
                                f0 = int(pitch_marks[1])
                            buffer = tts(buffer, wav, f0)
                            # LJEPLJENJE
                            ans += AudioSegment.silent(duration=100)
                    else:
                        # PSOLA
                        
                        sample_rate, wav = wavfile.read(rootdirall + "silsil.wav")
                        if not os.path.exists(rootdirall + "silsil.txt"):
                            f0, pitch_marks = pitch_marks_fun(wav)
                            np.savetxt(rootdirall + "silsil.txt", pitch_marks)
                        else:
                            pitch_marks = np.loadtxt(rootdirall + "silsil.txt")
                            f0 = int(pitch_marks[1])
                        buffer = tts(buffer, wav, f0)
                        # LJEPLJENJE
                        ans += AudioSegment.silent(duration=100)
            else:
                if rijeci[i - 1][-1] + "sil.wav" in alldifonidict:
                    
                    # PSOLA
                    sample_rate, wav = wavfile.read(rootdirall + rijeci[i - 1][-1] + "sil.wav")
                    if not os.path.exists(rootdirall + rijeci[i - 1][-1] + "sil.txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirall + rijeci[i - 1][-1] + "sil.txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirall + rijeci[i - 1][-1] + "sil.txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.from_wav(rootdirall + rijeci[i - 1][-1] + "sil.wav")
                    if "sil" + rijeci[i][0] + ".wav" in alldifonidict:
                        
                        # PSOLA
                        sample_rate, wav = wavfile.read(rootdirall + "sil" + rijeci[i][0] + ".wav")
                        if not os.path.exists(rootdirall + "sil" + rijeci[i][0] + ".txt"):
                            f0, pitch_marks = pitch_marks_fun(wav)
                            np.savetxt(rootdirall + "sil" + rijeci[i][0] + ".txt", pitch_marks)
                        else:
                            pitch_marks = np.loadtxt(rootdirall + "sil" + rijeci[i][0] + ".txt")
                            f0 = int(pitch_marks[1])
                        buffer = tts(buffer, wav, f0)
                        # LJEPLJENJE
                        ans += AudioSegment.from_wav(rootdirall + "sil" + rijeci[i][0] + ".wav")
                    else:
                        # PSOLA
                        
                        sample_rate, wav = wavfile.read(rootdirall + "silsil.wav")
                        if not os.path.exists(rootdirall + "silsil.txt"):
                            f0, pitch_marks = pitch_marks_fun(wav)
                            np.savetxt(rootdirall + "silsil.txt", pitch_marks)
                        else:
                            pitch_marks = np.loadtxt(rootdirall + "silsil.txt")
                            f0 = int(pitch_marks[1])
                        buffer = tts(buffer, wav, f0)
                        # LJEPLJENJE
                        ans += AudioSegment.silent(duration=100)
                else:
                    # PSOLA
                    
                    sample_rate, wav = wavfile.read(rootdirall + "silsil.wav")
                    if not os.path.exists(rootdirall + "silsil.txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirall + "silsil.txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirall + "silsil.txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.silent(duration=100)
            for j in range(0, len(rijeci[i]) - 1):
                if rijeci[i][j] + "-" + rijeci[i][j + 1] + ".wav" in rijecdict:
                    # PSOLA
                    sample_rate, wav = wavfile.read(rootdirsplit + rijeci[i][j] + "-" +
                                                 rijeci[i][j + 1] + "_" + rijeci[i] + ".wav")
                    if not os.path.exists(rootdirsplit + rijeci[i][j] + "-" +
                                                 rijeci[i][j + 1] + "_" + rijeci[i] + ".txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirsplit + rijeci[i][j] + "-" +
                                                 rijeci[i][j + 1] + "_" + rijeci[i] + ".txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirsplit + rijeci[i][j] + "-" +
                                                 rijeci[i][j + 1] + "_" + rijeci[i] + ".txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.from_wav(rootdirsplit + rijeci[i][j] + "-" +
                                                 rijeci[i][j + 1] + "_" + rijeci[i] + ".wav")
                elif rijeci[i][j] + rijeci[i][j + 1] + ".wav" in alldifonidict:
                    
                    # PSOLA
                    sample_rate, wav = wavfile.read(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".wav")
                    if not os.path.exists(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.from_wav(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".wav")
                else:
                    # PSOLA
                    # nema
                    # LJEPLJENJE
                    print("nema")
            if i == len(rijeci) - 1:
                if rijeci[i][-1] + "-sil.wav" in rijecdict:
                    # PSOLA
                    sample_rate, wav = wavfile.read(rootdirsplit + rijeci[i][-1] + "-sil" + "_" + rijeci[i] + ".wav")
                    if not os.path.exists(rootdirsplit + rijeci[i][-1] + "-sil" + "_" + rijeci[i] + ".txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirsplit + rijeci[i][-1] + "-sil" + "_" + rijeci[i] + ".txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirsplit + rijeci[i][-1] + "-sil" + "_" + rijeci[i] + ".txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.from_wav(
                        rootdirsplit + rijeci[i][-1] + "-sil" + "_" + rijeci[i] + ".wav")
                elif rijeci[i][-1] + "sil.wav" in alldifonidict:
                    
                    # PSOLA
                    sample_rate, wav = wavfile.read(rootdirall + rijeci[i][-1] + "sil.wav")
                    if not os.path.exists(rootdirall + rijeci[i][-1] + "sil.txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirall + rijeci[i][-1] + "sil.txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirall + rijeci[i][-1] + "sil.txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.from_wav(rootdirall + rijeci[i][-1] + "sil.wav")
                else:
                    # PSOLA
                    
                    sample_rate, wav = wavfile.read(rootdirall + "silsil.wav")
                    if not os.path.exists(rootdirall + "silsil.txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirall + "silsil.txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirall + "silsil.txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.silent(duration=100)
    else:
        
        if i == 0:
            if "sil" + rijeci[i][0] + ".wav" in alldifonidict:
                
                # PSOLA
                sample_rate, wav = wavfile.read(rootdirall + "sil" + rijeci[i][0] + ".wav")
                if not os.path.exists(rootdirall + "sil" + rijeci[i][0] + ".txt"):
                    f0, pitch_marks = pitch_marks_fun(wav)
                    np.savetxt(rootdirall + "sil" + rijeci[i][0] + ".txt", pitch_marks)
                else:
                    pitch_marks = np.loadtxt(rootdirall + "sil" + rijeci[i][0] + ".txt")
                    f0 = int(pitch_marks[1])
                buffer = tts(buffer, wav, f0)
                # LJEPLJENJE
                ans += AudioSegment.from_wav(rootdirall + "sil" + rijeci[i][0] + ".wav")
            else:
                
                # PSOLA
                sample_rate, wav = wavfile.read(rootdirall + "silsil.wav")
                if not os.path.exists(rootdirall + "silsil.txt"):
                    f0, pitch_marks = pitch_marks_fun(wav)
                    np.savetxt(rootdirall + "silsil.txt", pitch_marks)
                else:
                    pitch_marks = np.loadtxt(rootdirall + "silsil.txt")
                    f0 = int(pitch_marks[1])
                buffer = tts(buffer, wav, f0)
                # LJEPLJENJE
                ans += AudioSegment.silent(duration=100)
            for j in range(0, len(rijeci[i]) - 1):
                if rijeci[i][j] + rijeci[i][j + 1] + ".wav" in alldifonidict:
                    
                    # PSOLA
                    sample_rate, wav = wavfile.read(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".wav")
                    if not os.path.exists(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.from_wav(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".wav")
                else:
                    # PSOLA
                    # nema
                    # LJEPLJENJE
                    print("nema")
            if i == len(rijeci) - 1:
                if rijeci[i][-1] + "sil.wav" in alldifonidict:
                    
                    # PSOLA
                    sample_rate, wav = wavfile.read(rootdirall + rijeci[i][-1] + "sil.wav")
                    if not os.path.exists(rootdirall + rijeci[i][-1] + "sil.txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirall + rijeci[i][-1] + "sil.txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirall + rijeci[i][-1] + "sil.txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.from_wav(rootdirall + rijeci[i][-1] + "sil.wav")
                else:
                    
                    # PSOLA
                    sample_rate, wav = wavfile.read(rootdirall + "silsil.wav")
                    if not os.path.exists(rootdirall + "silsil.txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirall + "silsil.txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirall + "silsil.txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.silent(duration=100)
        else:
            if rijeci[i - 1][-1] + "sil.wav" in alldifonidict:
                
                # PSOLA
                sample_rate, wav = wavfile.read(rootdirall + rijeci[i - 1][-1] + "sil.wav")
                if not os.path.exists(rootdirall + rijeci[i - 1][-1] + "sil.txt"):
                    f0, pitch_marks = pitch_marks_fun(wav)
                    np.savetxt(rootdirall + rijeci[i - 1][-1] + "sil.txt", pitch_marks)
                else:
                    pitch_marks = np.loadtxt(rootdirall + rijeci[i - 1][-1] + "sil.txt")
                    f0 = int(pitch_marks[1])
                buffer = tts(buffer, wav, f0)
                # LJEPLJENJE
                ans += AudioSegment.from_wav(rootdirall + rijeci[i - 1][-1] + "sil.wav")
                if "sil" + rijeci[i][0] + ".wav" in alldifonidict:
                    
                    # PSOLA
                    sample_rate, wav = wavfile.read(rootdirall + "sil" + rijeci[i][0] + ".wav")
                    if not os.path.exists(rootdirall + "sil" + rijeci[i][0] + ".txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirall + "sil" + rijeci[i][0] + ".txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirall + "sil" + rijeci[i][0] + ".txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.from_wav(rootdirall + "sil" + rijeci[i][0] + ".wav")
                else:
                    # PSOLA
                    
                    sample_rate, wav = wavfile.read(rootdirall + "silsil.wav")
                    if not os.path.exists(rootdirall + "silsil.txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirall + "silsil.txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirall + "silsil.txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.silent(duration=100)
            else:
                # PSOLA
                
                sample_rate, wav = wavfile.read(rootdirall + "silsil.wav")
                if not os.path.exists(rootdirall + "silsil.txt"):
                    f0, pitch_marks = pitch_marks_fun(wav)
                    np.savetxt(rootdirall + "silsil.txt", pitch_marks)
                else:
                    pitch_marks = np.loadtxt(rootdirall + "silsil.txt")
                    f0 = int(pitch_marks[1])
                buffer = tts(buffer, wav, f0)
                # LJEPLJENJE
                ans += AudioSegment.silent(duration=100)
            for j in range(0, len(rijeci[i]) - 1):
                if rijeci[i][j] + rijeci[i][j + 1] + ".wav" in alldifonidict:
                    
                    # PSOLA
                    sample_rate, wav = wavfile.read(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".wav")
                    if not os.path.exists(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.from_wav(rootdirall + rijeci[i][j] + rijeci[i][j + 1] + ".wav")
                else:
                    # PSOLA
                    # nema
                    # LJEPLJENJE
                    print("nema")
            if i == len(rijeci) - 1:
                if rijeci[i][-1] + "sil.wav" in alldifonidict:
                    
                    # PSOLA
                    sample_rate, wav = wavfile.read(rootdirall + rijeci[i][-1] + "sil.wav")
                    if not os.path.exists(rootdirall + rijeci[i][-1] + "sil.txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirall + rijeci[i][-1] + "sil.txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirall + rijeci[i][-1] + "sil.txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.from_wav(rootdirall + rijeci[i][-1] + "sil.wav")
                else:
                    
                    # PSOLA
                    sample_rate, wav = wavfile.read(rootdirall + "silsil.wav")
                    if not os.path.exists(rootdirall + "silsil.txt"):
                        f0, pitch_marks = pitch_marks_fun(wav)
                        np.savetxt(rootdirall + "silsil.txt", pitch_marks)
                    else:
                        pitch_marks = np.loadtxt(rootdirall + "silsil.txt")
                        f0 = int(pitch_marks[1])
                    buffer = tts(buffer, wav, f0)
                    # LJEPLJENJE
                    ans += AudioSegment.silent(duration=100)
#PSOLA
wavfile.write("C:\\Users\\NIKOLA\\Desktop\\ROGJ\\Difoni\\" + text +"-PSOLA" + ".wav", sample_rate, buffer)
#LJEPLJENJE
ans.export("C:\\Users\\NIKOLA\\Desktop\\ROGJ\\Difoni\\" + text +"-LJEPLJENJE" + ".wav", format="wav")
