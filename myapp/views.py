import speech_recognition as sr
from django.shortcuts import render
from django.http import JsonResponse
import sounddevice as sd
import scipy.io.wavfile as wav
import datetime

def index(request):
    return render(request, 'index.html')

def recognize_from_mic(file_to_write):
    try:
        sample_rate = 48000
        duration = 5
        audio_recording = sd.rec(duration * sample_rate, samplerate=sample_rate, channels=1, dtype='int32')
        message = "Recording audio"
        sd.wait()
        message = "Audio recording completed, play audio"
        sd.play(audio_recording, sample_rate)
        sd.wait()
        message = "Audio played"
        wav.write(file_to_write, sample_rate, audio_recording)
        return message
    except Exception as e:
        message = f"Error recording audio:{e}"
        raise

def recognize_from_file(filename):
    try:
        r = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        print("Speech recognition API could not recognize speech")
        raise
    except Exception as e:
        print("Error recognizing speech:", e)
        raise

def save_to_text(text, filename):
    with open(filename, 'w') as f:
        f.write(text)

def talktotext(request):
    if request.method == 'POST': 
            timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            filename_from_mic = f"RECORDING-{timestamp}.WAV"
            voice_text_filename = f"VOICE_AS_TEXT-{timestamp}.txt"

            message = recognize_from_mic(filename_from_mic)
            text_from_voice = recognize_from_file(filename_from_mic)
            save_to_text(text_from_voice, voice_text_filename)

            with open(voice_text_filename,'r') as f:
                text = f.read()
                data =  {'message':message,'text':text}
            return JsonResponse(data)
        
    else:
        return render(request, 'index.html')