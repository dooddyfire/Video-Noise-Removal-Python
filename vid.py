from moviepy.editor import VideoFileClip

from scipy.io import wavfile
import noisereduce as nr

import subprocess

########### extract audio from video
# video original mp4
input_video = "demovideo.mp4"   

videoclip = VideoFileClip(input_video )
videoclip.audio.write_audiofile('audio.wav',fps=16000,bitrate='96k',nbytes=2,verbose=False)

########### Remove noise from audio
rate, data = wavfile.read('audio.wav')
if len(data.shape) > 1:
 data = data[:, 0]
reduced_noise = nr.reduce_noise(y=data, sr=rate) ### this consumes lot of memory. You may need to break into chunks for longer duration of audio.
wavfile.write('nraudio.wav', rate, reduced_noise)

input_audio = "nraudio.wav"

########## Merge audio and video
subprocess.call([
    'ffmpeg',
    '-i', input_video,
    '-i', input_audio,
    '-map', '0:v',  # Correct mapping for the video stream
    '-map', '1:a',  # Correct mapping for the audio stream
    '-c:v', 'copy',  # Copy the video stream without re-encoding
    '-shortest',  # Ensure the output is as short as the shortest input
    '-threads', '2',
    'outvideo.mp4'
])

print("ลบเสียง noise จากวิดีโอสำเร็จ")
