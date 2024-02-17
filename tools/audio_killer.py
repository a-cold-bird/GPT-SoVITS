import os
from pydub import AudioSegment

def delete_long_audio_files(folder_path, max_duration=20):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith('.wav'):
                audio = AudioSegment.from_wav(file_path)
                duration = len(audio) / 1000  # 将毫秒转换为秒
                if duration > max_duration:
                    os.remove(file_path)
                    print(f"Deleted {file_path}")

delete_long_audio_files('output/slicer_opt', max_duration=20)
