# 五目並べ (Gomoku)

Windows上でGUI操作により対局できる、人対人専用の五目並べゲームです。

> **Note**
> このプロジェクトは、[Claude Code](https://www.anthropic.com/claude-code) を使ったウォーターフォール型開発プロセス（要件定義 → コンポーネント設計 → 関数設計 → 実装 → テスト）の練習として作成しました。仕様・設計・実装・テストのすべてをこのプロセスに沿って進めています。

## 概要

- 15×15の盤面で、黒石・白石が交互に手番を持ち対局します（先手は黒石）
- 縦・横・斜めのいずれかに同色の石が5つ以上連続（長連含む）すると勝利です
- 勝利が成立した石は盤面上でハイライト表示されます
- 盤面が全て埋まり、かつ五連が成立しない場合は引き分けとなります
- いつでも盤面をリセットして新しい対局を開始できます
- CPU対戦・ネットワーク対戦は対象外です（人対人のローカル対局のみ）

## 動作環境

- Windows 10 / 11
- Python 3.9 以上（標準ライブラリの `tkinter` のみ使用。追加パッケージのインストールは不要）

## 実行方法

### ソースから実行する場合

```powershell
py src\main.py
```

### 配布用exeを使う場合

Python未インストールのPCでも動作する単体実行ファイル（`Gomoku.exe`）としてビルド・配布する手順は [`docs/05_distribution/distribution_manual.md`](docs/05_distribution/distribution_manual.md) を参照してください。

## プロジェクト構成

```
docs/
  01_requirements/       要件定義書
  02_component_design/   コンポーネント設計書（基本設計）
  03_function_design/    関数設計書（詳細設計）
  04_test/               テスト仕様書・手動テストチェックリスト
  05_distribution/       配布マニュアル
  traceability_matrix.md 要件〜実装〜テストのトレーサビリティマトリックス
  qa_log.md              開発中の判断・承認記録
src/                      実装コード（ゲームロジックとGUIを分離した構成）
tests/                    自動テストコード
```

## テスト

ゲームロジック層（盤面管理・勝敗判定・状態管理）の自動テストを用意しています。

```powershell
py -m unittest discover tests
```

GUI層・操作系の確認項目は [`docs/04_test/manual_test_checklist.md`](docs/04_test/manual_test_checklist.md) にまとめています。

## 開発ドキュメント

要件定義から設計・テストまでの成果物は `docs/` 以下にすべて残しています。ウォーターフォール開発の各工程がどのように進んだかは [`docs/traceability_matrix.md`](docs/traceability_matrix.md) と [`docs/qa_log.md`](docs/qa_log.md)（開発中のQA記録）から追えます。
