# red_black_tree

## 概要
赤黒木へのデータの挿入／削除ができます
木の状態を視覚的に確認できます

## 動作環境
OS: Ubuntu22.04
Python: 3.10.12

## 導入手順
1.  ```git clone https://github.com/pm306/red_black_tree.git```
2.  ```python3 -m venv venv```
3.  ```source /venv/bin/activate```
4.  ```pip install -r requirements.txt```
5.  ```python3 main.py```
6.  ターミナルに表示されたURLにアクセスする

## 機能
* **Insert**
 値を挿入します
* **ひとつ前に戻る**
 壊れているため現在使用できません
* **Delete**
 値を削除します
* **Reset**
 木を初期化します

## 注意点
ページを更新しないと操作が反映されません

## TODO
* 自己参照をなくす
* 動的更新にする
* 1つ戻るボタンで500エラーになるのを修正する
