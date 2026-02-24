# 018_Practice_StandardLibrary

## 01 glob モジュール の使い方を確認。

### 要件
- スクリプト名は count_by_ext.py とする。
- 引数で検索するルートディレクトリを受け取る（省略時はカレントディレクトリ）。
- 再帰的にサブディレクトリも検索する（** を使う）。
- 隠しファイル・隠しディレクトリ（名前がドットで始まるもの）は無視する。
- バイナリ判定は不要。テキストファイルとして開けるものは行数を数える。読み込みで例外が出たファイルはスキップして警告を出す。
- 出力は拡張子ごとに ファイル数 と 合計行数 を降順（ファイル数→行数）で表示する。拡張子がないファイルは no_ext として扱う。
- 使用する検索は 標準ライブラリの glob（または pathlib.Path.glob / rglob） を必須で使うこと。os.walk のみで実装するのは不可。ただし補助に os や pathlib を使ってもよい。

### サンプルディレクトリ構成

project/
├─ README.md
├─ setup.py
├─ src/
│  ├─ main.py
│  ├─ utils.py
│  └─ lib/
│     ├─ helper.py
│     └─ data.json
├─ tests/
│  ├─ test_main.py
│  └─ .hidden_test.py
├─ docs/
│  └─ index.rst
└─ .git/
   └─ config

#### 注意点
- .hidden_test.py や .git/ 配下は無視すること。
- data.json や README.md もカウント対象。
- setup.py や index.rst も拡張子別に集計する。
