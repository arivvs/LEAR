from flask import Flask, render_template, Response
from screen import VideoCamera
from audio import AudioStream
import struct

app = Flask(__name__)
def gen_header(sample_rate, bits, channels):
    datasize = 2000*10**6
    o = bytes("RIFF", 'ascii')
    o += struct.pack('<I', datasize + 36)
    o += bytes("WAVE", 'ascii')
    o += bytes("fmt ", 'ascii')
    o += struct.pack('<I', 16)
    o += struct.pack('<H', 1)
    o += struct.pack('<H', channels)
    o += struct.pack('<I', sample_rate)
    o += struct.pack('<I', sample_rate * channels * bits // 8)
    o += struct.pack('<H', channels * bits // 8)
    o += struct.pack('<H', bits)
    o += bytes("data", 'ascii')
    o += struct.pack('<I', datasize)
    return o

def gen_video(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen_audio(audio):
    yield gen_header(48000, 16, 2)
    for data in audio.get_audio():
        yield data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_video(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/audio_feed')
def audio_feed():
    return Response(gen_audio(AudioStream()),
                    mimetype='audio/wav')

if __name__ == '__main__':
    print("Запуск")
    app.run(host='0.0.0.0', port=5000, threaded=True)