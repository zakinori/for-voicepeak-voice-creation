import os
import json
import feedparser
import re
from newspaper import Article
from datetime import datetime
from pydub import AudioSegment

def change_current_directory():
    # スクリプトのディレクトリに移動
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

def read_setting_json():
    # json設定ファイルを読み込む
    with open('generator_settings.json', 'r') as f:
        json_data = json.load(f)
    return json_data

def create_folder_if_not_exists(folder_path):
    # フォルダが存在しない場合作成する
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def news_filename_creator(prefix):
    # 記事のファイル名を生成
    return f"{prefix}/{prefix}.txt"

def description_filename_creator(prefix, index, number_digits):
    # 記事の説明ファイル名を生成
    return f"{prefix}/{prefix}_{index:0{number_digits}}.txt"

def description_text_creator(description, prefix, number_digits):
    # 記事の説明を出力
    index = 0
    output_file = description_filename_creator(prefix, index, number_digits)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"本日の日付は{datetime.now().strftime('%Y年%-m月%-d日')}です。\n")
        f.write(f"これから、{description}を取得します。\n")

def rss_feed_reader(url):
    # RSSフィードを取得
    feed = feedparser.parse(url)
    return_text = []
    for entry in feed.entries:
        entry_text = extract_text_from_url(entry.link)
        return_text.append(eliminate_distracting_elements(entry_text))
        return_text.append('\n次の記事に移ります。')
    return ''.join(return_text)

def extract_text_from_url(url):
    # URLからテキストを抽出
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def eliminate_distracting_elements(text):
    # 記事から不要な要素を削除
    return_text = text
    # return_text = re.sub(r'^Image: .*$', '', return_text, flags=re.MULTILINE) # Sample
    # return_text = re.sub(r'^Source: .*$', '', return_text, flags=re.MULTILINE) # Sample
    # return_text = re.sub(r'^＞＞.*$', '', return_text, flags=re.MULTILINE) # Sample
    return return_text

def news_file_creator(news_text, prefix):
    # 記事のテキストを生成
    output_file = news_filename_creator(prefix)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(news_text)

if __name__ == "__main__":
    # エントリポイント
    change_current_directory()
    json_data = read_setting_json()
    number_digits = json_data['sequential_number_digits']
    records = json_data['rss_feed']
    for item in records:
        # RSS取得先分繰り返す
        url = item['url']
        prefix = item['file_prefix']
        description = item['description']
        try:
            create_folder_if_not_exists(prefix)
            description_text_creator(description, prefix, number_digits)
            rss_text = rss_feed_reader(url)
            news_file_creator(rss_text, prefix)
        except Exception as e:
            print(f"Error processing file create: {e}")
