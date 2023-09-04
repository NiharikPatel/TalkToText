import speech_recognition as sr
import sounddevice as sd
# import numpy as np
import scipy.io.wavfile as wav
import time
import datetime

sample_rate = 44100
duration = 5
r = sr.Recognizer()


timestamp = datetime.datetime.now().strftime("%Y%M%D-%H%M%S")
filename_from_mic = f"RECORDING-{timestamp}.WAV"
voice_text_filename = f"VOICE_AS_TEXT-{timestamp}.txt"


def recognize_from_mic(file_to_write):

    audio_recording = sd.rec(duration * sample_rate, samplerate=sample_rate, channels=1, dtype='int32')
    # print("Recording audio")
    sd.wait()
    # print("Audio recording completed, play audio")
    # sd.play(audio_recording, sample_rate)
    sd.wait()
    # print("Audio played")
    wav.write(file_to_write, sample_rate, audio_recording)


def recognize_from_file(filename):
    with sr.AudioFile(filename) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        return text

def save_to_text(text, filename):
    with open(filename, 'w') as f:
        f.write(text)

if __name__ == "__main__":
    recognize_from_mic(filename_from_mic)
    try:
        text_from_voice = recognize_from_file(filename_from_mic)
        save_to_text(text_from_voice, voice_text_filename)
    except sr.UnknownValueError:
        print("Could not recognize speech speak again")
   