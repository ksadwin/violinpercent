# alright chucklefucks
import time
import pyaudio
import librosa
import numpy as np

from DougDoug_keycodes import *

TESTING = False


CHUNK = 1024
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = -1
C_3 = float(librosa.note_to_hz("C3"))
E_6 = float(librosa.note_to_hz("E6"))
YINMIN = C_3
YINMAX = E_6
SEXIEST_INDEX = 1
DEVICE_INDEX = 1ness


# bizhawk_NOTE_TO_KEY_DICT = {
#     "A"  : UP_ARROW    ,
#     "A♯" : Z           ,
#     "B"  : X           ,
#     "C"  : RIGHT_SHIFT ,
#     "C♯" : X           ,
#     "D"  : LEFT_ARROW  ,
#     "D♯" : Z           ,
#     "E"  : RIGHT_ARROW ,
#     "F"  : Z           ,
#     "F♯" : X           ,
#     "G"  : DOWN_ARROW  ,
#     "G♯" : ENTER        
# }

bizhawk_NOTE_TO_KEY_DICT = {
    "A"  : RIGHT_ARROW ,
    "A♯" : Z           ,
    "B"  : X           ,
    "C"  : RIGHT_SHIFT ,
    "C♯" : X           ,
    "D"  : DOWN_ARROW  ,
    "D♯" : Z           ,
    "E"  : UP_ARROW    ,
    "F"  : Z           ,
    "F♯" : X           ,
    "G"  : LEFT_ARROW  ,
    "G♯" : ENTER        
}

NOTE_TO_KEY = bizhawk_NOTE_TO_KEY_DICT


current_pitch = ""


def transition_matrix(hz_min=YINMIN, hz_max=YINMAX, filename="transmat.npy"):
    # if file exists: return numpy.load(filename)
    midi_min = librosa.hz_to_midi(hz_min)
    midi_max = librosa.hz_to_midi(hz_max)
    n_notes = midi_max - midi_min + 1

    transmat = np.zeros((2 * n_notes + 1, 2 * n_notes + 1))

    # insert smart people logic here
    # numpy.save(filename, transmat)

    return transmat


def callback(in_data, frame_count, time_info, flag):
    global current_pitch

    numpy_array = np.frombuffer(in_data, dtype=np.float32)
    # newarray = np.nan_to_num(numpy_array, nan=np.finfo(np.float32).eps)
    # print(newarray)
    # ndarrayithink = librosa.yin(newarray, fmin=YINMIN, fmax=YINMAX, sr=RATE, frame_length=CHUNK)
    pyinarray, is_voiced, voiced_problt = librosa.pyin(numpy_array, fmin=YINMIN, fmax=YINMAX, sr=RATE, frame_length=CHUNK, win_length=int(CHUNK/2))
    # print(voiced_problt[SEXIEST_INDEX])
    if is_voiced[SEXIEST_INDEX]:
        midpitch = librosa.hz_to_note(pyinarray[SEXIEST_INDEX])
        if current_pitch != midpitch:
            if current_pitch not in ("stop", ""):
                ReleaseKey(NOTE_TO_KEY[current_pitch[:-1]])
            current_pitch = midpitch
            HoldKey(NOTE_TO_KEY[current_pitch[:-1]])
            print(current_pitch)
    elif current_pitch != "stop":
        if current_pitch:
            ReleaseKey(NOTE_TO_KEY[current_pitch[:-1]])
        current_pitch = "stop"
        print("stop")

    return None, pyaudio.paContinue


def callback_test(in_data, frame_count, time_info, flag):
    global current_pitch

    numpy_array = np.frombuffer(in_data, dtype=np.float32)
    # newarray = np.nan_to_num(numpy_array, nan=np.finfo(np.float32).eps)
    # print(newarray)
    # ndarrayithink = librosa.yin(newarray, fmin=YINMIN, fmax=YINMAX, sr=RATE, frame_length=CHUNK)
    pyinarray, is_voiced, voiced_problt = librosa.pyin(numpy_array, fmin=YINMIN, fmax=YINMAX, sr=RATE, frame_length=CHUNK, win_length=int(CHUNK/2))
    my_problt = sum([int(x) for x in is_voiced])
    print(my_problt)
    if is_voiced[SEXIEST_INDEX]:
        midpitch = librosa.hz_to_note(pyinarray[SEXIEST_INDEX])
        if current_pitch != midpitch:
            # if current_pitch not in ("stop", ""):
            #     ReleaseKey(NOTE_TO_KEY[current_pitch[:-1]])
            current_pitch = midpitch
            # HoldKey(NOTE_TO_KEY[current_pitch[:-1]])
            print(current_pitch)
    elif current_pitch != "stop":
        # if current_pitch:
        #     ReleaseKey(NOTE_TO_KEY[current_pitch[:-1]])
        current_pitch = "stop"
        print("stop")

    return None, pyaudio.paContinue


def detect_all_audio_inputs(total=20):
    p = pyaudio.PyAudio()

    for i in range(0,total):
        try:
            print(p.get_device_info_by_index(i))
        except IOError:
            print("Index %d doesn't exist" % i)
    print(p.get_default_input_device_info())
    p.terminate()



def listen():
    if TESTING:
        print("Hey Dip Shit You Are In Testing Mode Right Now Dont Try To Play Video Games")
    p = pyaudio.PyAudio()
    print(p.get_device_info_by_index(DEVICE_INDEX))
    if p.is_format_supported(rate=RATE, input_device=DEVICE_INDEX, input_channels=CHANNELS, input_format=FORMAT):
        if TESTING:
            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=DEVICE_INDEX, stream_callback=callback_test)
        else:
            stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=DEVICE_INDEX, stream_callback=callback)
    else:
        print("help me")
        exit()

    if stream.is_active():
        if RECORD_SECONDS > 0:
            time.sleep(RECORD_SECONDS)
            stream.stop_stream()
        else:
            while True:
                time.sleep(300)
        if current_pitch not in ("stop", ""):
            ReleaseKey(NOTE_TO_KEY[current_pitch[:-1]])
    else:
        print("help me")

    stream.close()
    p.terminate()


def main():
    detect_all_audio_inputs()
    listen()

main()