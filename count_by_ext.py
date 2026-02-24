#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path
from collections import defaultdict
import traceback

def is_hidden(path: Path) -> bool:
    # パスの各パートにドットで始まる要素があれば隠しとみなす
    return any(part.startswith('.') for part in path.parts)

def count_lines(path: Path) -> int:
    try:
        # テキストとして読み、行数を数える。読み込みエラーは例外で上位へ
        with path.open('r', encoding='utf-8', errors='strict') as f:
            return sum(1 for _ in f)
    except UnicodeDecodeError:
        # UTF-8 で読めない場合は警告を出してスキップ
        print(f"Warning: cannot decode file {path!s}, skipping.", file=sys.stderr)
        return 0
    except Exception as e:
        # その他の読み込みエラーも警告してスキップ
        print(f"Warning: failed to read {path!s}: {e}", file=sys.stderr)
        return 0

def main():
    parser = argparse.ArgumentParser(description="Count files and total lines by extension using glob/rglob.")
    parser.add_argument('root', nargs='?', default='.', help='root directory to search (default: current dir)')
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"Error: {root!s} does not exist.", file=sys.stderr)
        sys.exit(2)

    stats = defaultdict(lambda: {'files': 0, 'lines': 0})

    # rglob("*") で再帰的にすべてのパスを列挙
    for p in root.rglob('*'):
        # ファイルのみ対象
        if not p.is_file():
            continue
        # 隠しファイル・隠しディレクトリを除外
        if is_hidden(p.relative_to(root)):
            continue

        # 拡張子（最後のサフィックス）を取得
        suffix = p.suffix  # 例: '.py' または ''（拡張子なし）
        key = suffix if suffix else 'no_ext'

        # 行数を数える。読み込み失敗は 0 行として扱う（警告は出す）
        lines = count_lines(p)
        # 読み込みで例外が出た場合はファイル数にカウントしない方がよければここで調整可能
        stats[key]['files'] += 1
        stats[key]['lines'] += lines

    # ソート：ファイル数降順、同数なら行数降順
    sorted_items = sorted(
        stats.items(),
        key=lambda kv: (kv[1]['files'], kv[1]['lines']),
        reverse=True
    )

    # 出力フォーマットを整える
    for ext, v in sorted_items:
        # ext が拡張子なら先頭にドットがあるはず。表示幅を揃えるためフォーマット
        label = ext if ext == 'no_ext' else ext
        print(f"{label:6}: {v['files']:4} files, {v['lines']:6} lines")

if __name__ == '__main__':
    main()