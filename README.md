# for-voicepeak-voice-creation

* [voicepeak公式インストーラー](<https://www.ah-soft.com/voice/setup/>)
* [voicepeak公式機能マニュアル](<https://www.ah-soft.com/voice/manual/>)

CLI利用の音声生成では文字数制限に引っかかるので
出力したいテキストファイルを制限文字数で分割し、
一括変換を実施できるwindowsバッチを作成するpythonスクリプトです。
出来上がった音声ファイルを結合するpythonスクリプトも含まれます。

## 構成

| ファイル | 説明 |
| :- | :- |
| generator_settings.json | 個人毎スクリプト設定（テンプレートから作成してください） |
| create_batch_for_voicepeak.py | テキストを設定値の文字数で分割し、voicepeak音声データ生成バッチを作る。 |
| crystallize_wave_files.py | 音声データ（wave）の統合 |
| rss_feed_scraper.py | rss情報の取得 |

## 実行サンプル

* バッチ生成

```voicepeak.py
python3 create_batch_for_voicepeak.py {path}
```

※音声ファイル結合, rss情報取得は引数不要
