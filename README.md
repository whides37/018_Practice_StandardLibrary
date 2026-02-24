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

```
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
```

#### 注意点
- .hidden_test.py や .git/ 配下は無視すること。
- data.json や README.md もカウント対象。
- setup.py や index.rst も拡張子別に集計する。

### テストケース（自分で検証するための例）
- 隠しファイルの除外
- tests/.hidden_test.py が存在しても集計に含めないこと。
- 拡張子なしファイルの扱い
- LICENSE のような拡張子なしファイルがあれば no_ext にカウントされること。
- 読み込みエラーの扱い
- 読み込みで UnicodeDecodeError が出たファイルはスキップし、標準エラーに警告を出すこと。
- 再帰検索
- src/lib/helper.py のような深い階層もカウントされること。

### ヒント
- glob.glob("**/*", recursive=True) や pathlib.Path(root).rglob("*") を使うと再帰検索できる。
- 隠しファイル・ディレクトリを除外するには、パスの各パート（Path.parts）にドットで始まる要素がないかチェックする方法が簡単。
- ファイルの拡張子は Path.suffix を使うと便利。複数拡張子（例: .tar.gz）は要件に応じて扱いを決めるが、ここでは最後のサフィックスのみで良い。
- 行数は open(path, "r", encoding="utf-8", errors="replace") のようにして読み、sum(1 for _ in f) で数えると効率的。
