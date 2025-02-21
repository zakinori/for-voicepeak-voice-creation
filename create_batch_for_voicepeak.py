import os
import json
import sys
from janome.tokenizer import Tokenizer

def read_setting_json():
    # json設定ファイルを読み込む
    with open('generator_settings.json', 'r') as f:
        json_data = json.load(f)
    return json_data

def read_text_file(file_path):
    # テキストファイルの読み込み
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def eliminate_distracting_elements(text):
    # テキストから不要な要素を削除
    return_text = text
    return_text = return_text.replace('\n', '')
    return_text = return_text.replace(' ', '')
    return return_text

def create_folder(folder):
    # フォルダの存在確認を実施し、存在しない場合は作成する。
    if not os.path.exists(folder):
        os.makedirs(folder)

def split_text_japanese(folder, text, number_digits, text_limit):
    # 日本語テキストを指定文字数で分割
    tokenizer = Tokenizer()
    words = [token.surface for token in tokenizer.tokenize(text)]
    index = 1
    current_chunk = []
    current_length = 0
    for word in words:
        if current_length + len(word) > text_limit:
            text_file_creator(folder, number_digits, index, ("".join(current_chunk)))
            index += 1 
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word)
    if current_chunk:
        text_file_creator(folder, number_digits, index, ("".join(current_chunk)))

def text_file_creator(folder, number_digits, index, chunk):
    # テキストファイルの作成
    output_file = f"{folder}/{folder}_{index:0{number_digits}}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(chunk)

def create_voicepeak_convert_batch(folder, exe_path, actor, emotion):
    # voicepeak実行バッチの生成
    files = os.listdir(folder)
    text_files = [file for file in files if file.endswith(".txt")]
    batch_file = f"voicepeak_wav_converter.bat"
    with open(batch_file, 'w', encoding='utf-8') as f:
        f.write(f"cd {folder}\n")
        for file in text_files:
            cmd = f"{exe_path} -t {file} -n {actor} -o {file.replace('.txt', '.wav')} -e {emotion}\n"
            f.write(cmd)

if __name__ == "__main__":
    # エントリポイント
    args = sys.argv
    if len(args) < 2:
        print("Usage: Invalid command line arguments")
        sys.exit()

    target_path = args[1]
    text_data = read_text_file(target_path)
    text_data = eliminate_distracting_elements(text_data)

    json_data = read_setting_json()
    number_digits = json_data['sequential_number_digits']
    text_limit = json_data['voicepeak_text_limit']
    workspace_folder = json_data['workspace_folder']

    create_folder(workspace_folder)
    split_text_japanese(workspace_folder, text_data, number_digits, text_limit)

    exe_path = json_data['voicepeak_exe']
    actor = json_data['voicepeak_actor']
    emotion = json_data['voicepeak_emotion']
    create_voicepeak_convert_batch(workspace_folder, exe_path, actor, emotion)
