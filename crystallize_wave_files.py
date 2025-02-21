import os
import json
import re
from pydub import AudioSegment

def read_setting_json():
    # json設定ファイルを読み込む
    with open('generator_settings.json', 'r') as f:
        json_data = json.load(f)
    return json_data

def wav_file_name_creator(folder):
    # 記事の音声ファイル名を生成
    return f"{folder}/{folder}.wav"

def connect_wav_files(folder):
    # wavファイルを結合
    files = os.listdir(folder)
    wav_files = [file for file in files if file.endswith(".wav")]
    combined_sound = AudioSegment.empty()
    output_file = wav_file_name_creator(folder)
    for file in wav_files:
        combined_sound += AudioSegment.from_wav(f"{folder}/{file}")
    if len(wav_files) > 0:
        combined_sound.export(output_file, format="wav")
    for file in wav_files:
        os.remove(f"{folder}/{file}")

def delete_work_files(folder):
    # 作業ファイルの削除
    files = os.listdir(folder)
    pattern = re.compile(rf"^{re.escape(folder)}_.*\.txt$")
    work_files = [file for file in files if pattern.match(file)]
    for file in work_files:
        os.remove(f"{folder}/{file}")

if __name__ == "__main__":
    # エントリポイント
    json_data = read_setting_json()
    workspace_folder = json_data['workspace_folder']
    connect_wav_files(workspace_folder)
    delete_work_files(workspace_folder)
