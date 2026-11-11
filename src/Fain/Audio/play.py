import wave
import sys
import pyaudio #type: ignore

class AudioPlayingService():
    CHUNK = 1024
    def __init__(self):
        self.audio = pyaudio.PyAudio()
    
    def open(self, wfile:str):
        with wave.open(wfile, 'rb') as wf:
            audio_format = self.audio.get_format_from_width(wf.getsampwidth())
            stream = self.audio.open(format=audio_format,
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
            while len(data := wf.readframes(AudioPlayingService.CHUNK)):  # Requires Python 3.8+ for :=
                stream.write(data)

            # Close stream (4)
            stream.close()
            
    def close(self):
        self.audio.terminate()

class AudioRecordingService():
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1 if sys.platform == 'darwin' else 2
        self.RATE = 44100
        self.audio = pyaudio.PyAudio()

    def record_fixed(self, record_duration, filename:str):
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)

            stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True)
            print('Recording...')
            for _ in range(0, self.RATE // self.CHUNK * record_duration):
                wf.writeframes(stream.read(self.CHUNK))
            stream.close()
    
    def close(self):
        self.audio.terminate()          
    