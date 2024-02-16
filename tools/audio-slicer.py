import os
from typing import final
import numpy as np
import librosa
import soundfile as sf
from slicer2 import Slicer
import argparse
import subprocess

class AutoSlicer:
    def __init__(self):
        self.slicer_params = {
            "threshold": -40,
            "min_length": 5000,
            "min_interval": 300,
            "hop_size": 10,
            "max_sil_kept": 500,
        }
        self.original_min_interval = self.slicer_params["min_interval"]

    def auto_slice(self, filename, input_dir, output_dir, max_sec):
        audio, sr = librosa.load(os.path.join(input_dir, filename), sr=None, mono=False)
        slicer = Slicer(sr=sr, **self.slicer_params)
        chunks = slicer.slice(audio)
        files_to_delete = []
        for i, chunk in enumerate(chunks):
            if len(chunk.shape) > 1:
                chunk = chunk.T
            output_filename = f"{os.path.splitext(filename)[0]}_{i}"
            output_filename = "".join(c for c in output_filename if c.isascii() or c == "_") + ".wav"
            output_filepath = os.path.join(output_dir, output_filename)
            sf.write(output_filepath, chunk, sr)
            #Check and re-slice audio that more than max_sec.
            while True:
                new_audio, sr = librosa.load(output_filepath, sr=None, mono=False)
                if librosa.get_duration(y=new_audio, sr=sr) <= max_sec:
                    break
                self.slicer_params["min_interval"] = self.slicer_params["min_interval"] // 2
                if self.slicer_params["min_interval"] >= self.slicer_params["hop_size"]:
                    new_chunks = Slicer(sr=sr, **self.slicer_params).slice(new_audio)
                    for j, new_chunk in enumerate(new_chunks):
                        if len(new_chunk.shape) > 1:
                            new_chunk = new_chunk.T
                        new_output_filename = f"{os.path.splitext(output_filename)[0]}_{j}.wav"
                        sf.write(os.path.join(output_dir, new_output_filename), new_chunk, sr)
                    files_to_delete.append(output_filepath)
                else:
                    break
            self.slicer_params["min_interval"] = self.original_min_interval
        for file_path in files_to_delete:
            if os.path.exists(file_path):
                os.remove(file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audio Slicing Tool")
    parser.add_argument("--input", help="Input directory", required=True)
    parser.add_argument("--output", help="Output directory", required=True)
    parser.add_argument("max_sec", type=int, help="Maximum seconds")

    args = parser.parse_args()

    auto_slicer = AutoSlicer()
    input_dir = args.input
    output_dir = args.output
    max_sec = args.max_sec

    for filename in os.listdir(input_dir):
        auto_slicer.auto_slice(filename, input_dir, output_dir, max_sec)

