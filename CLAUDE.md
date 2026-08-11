# プロジェクト概要

Claude Codeを用いた**ウォーターフォール型開発の練習**プロジェクト。
題材: Windows GUIで動作する五目並べ(Gomoku)ゲームをPythonで開発する。

## 開発プロセス

以下の順に工程を進める。各工程の成果物はユーザーのレビュー・承認を得てから次工程に進むこと（勝手に次工程へ進まない）。

1. 要件定義 (`docs/01_requirements/`)
2. コンポーネント設計 (`docs/02_component_design/`)
3. 関数設計 (`docs/03_function_design/`)
4. 実装 (`src/`)
5. テスト (`docs/04_test/` に仕様書、`tests/` にテストコード)

## 現在の進捗（2026-08-11時点）

- [x] フォルダ構成・ローカルGitリポジトリ作成済み
- [x] `docs/01_requirements/requirements.md` 作成済み
- [ ] **ユーザーによる要件定義書のレビュー・承認 待ち** ← 次はここから再開
- [ ] コンポーネント設計
- [ ] 関数設計
- [ ] 実装
- [ ] テスト

再開時は、まずユーザーに要件定義書（`docs/01_requirements/requirements.md`）の内容に修正がないか確認し、
承認が得られたらコンポーネント設計書の作成に着手すること。

## 確定した仕様（要件定義で合意済み）

- 言語: Python、GUIは標準ライブラリの `tkinter`（追加パッケージ不要）
- 対局モード: 人 対 人のみ（CPU対戦・ネットワーク対戦は対象外）
- 盤面: 15×15、勝利条件は5つ連続（五連）
- 先手: 黒石
- 構成管理: Git（ローカルリポジトリのみ、リモート無し）

## Gitコミット規約

ユーザー自身のコミットとClaudeが作成したコミットを区別するため、Claudeがコミットする際は必ず以下のルールに従うこと。

- コミットメッセージの先頭に `[claude] ` を付ける
- コミット時に `--author="Claude <noreply@anthropic.com>"` を指定する（コミッターは変更しない）
- 例:
  ```powershell
  git commit -m "[claude] 要件定義書を作成" --author="Claude <noreply@anthropic.com>"
  ```
- ユーザー自身が手動でコミットする場合は、通常通りグローバルGit設定（ImSanghun / 21452104tpu@gmail.com）でコミットしてよい（接頭辞不要）

## 環境メモ

- このマシンには元々Gitが入っておらず、セッション中に `winget install --id Git.Git -e` でインストール済み。
- **重要**: このPowerShell環境ではツール呼び出しごとにシェル状態（PATH等）がリセットされる。
  `git` コマンドを実行する際、`git`が見つからない場合は以下でPATHを通してから実行すること。
  ```powershell
  [System.Environment]::SetEnvironmentVariable("PATH", [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User"), "Process")
  ```
- `git config user.email` / `user.name` はグローバル設定済み（21452104tpu@gmail.com / ImSanghun）。

## フォルダ構成

```
docs/
  01_requirements/      要件定義書
  02_component_design/  コンポーネント設計書（基本設計）
  03_function_design/   関数設計書（詳細設計）
  04_test/              テスト仕様書
src/                     実装コード
tests/                   テストコード
```
