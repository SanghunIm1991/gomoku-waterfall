# テスト実行手順書

## 1. 文書情報

| 項目 | 内容 |
|---|---|
| プロジェクト名 | 五目並べゲーム (Gomoku) |
| 版数 | 1.0 |
| 作成日 | 2026-08-11 |
| 目的 | `docs/04_test/test_specification.md`（自動単体テスト）および`docs/04_test/manual_test_checklist.md`（手動テスト）に基づき作成されたテストを、実際に実行する手順をユーザー向けにまとめる |

## 2. 前提条件

- 実装環境（Python）はCLAUDE.md「実装環境（Python）」章の通り、`py`ランチャー経由でPython 3.9.13（Visual Studio付属）を使用する。追加パッケージのインストールは不要。
- コマンドはプロジェクトルート（`D:\claudeProject`）で実行する。
- PowerShellを使用する（本プロジェクトの標準シェル）。

## 3. 自動単体テストの実行（`tests/`）

対象: COMP-01 Board、COMP-02 WinChecker、COMP-03 GameState、COMP-07 Constants（`tkinter`に依存しないロジック層）

### 3.1 全テストを一括実行する（基本）

```powershell
py -m unittest discover tests
```

- 最後に `OK` と表示され、実行件数（例: `Ran 30 tests in 0.0xxs`）が出力されれば全件成功。
- 失敗があると `FAILED (failures=n)` のように表示され、どのテストID（メソッド名）で失敗したかが詳細表示される。

### 3.2 詳細表示（各テストケース名を1件ずつ確認したい場合）

```powershell
py -m unittest discover tests -v
```

- テストファイル・メソッド単位で `ok` / `FAIL` / `ERROR` が1行ずつ表示される。

### 3.3 特定のテストファイルのみ実行する

```powershell
py -m unittest tests.test_board
py -m unittest tests.test_win_checker
py -m unittest tests.test_game_state
py -m unittest tests.test_constants
```

### 3.4 特定のテストケース（メソッド）のみ実行する

```powershell
py -m unittest tests.test_board.TestBoard.test_place_stone_success
```

（クラス名・メソッド名は各テストファイルの中身に合わせて指定する）

### 3.5 テストIDとテストファイル・要件の対応

各テストIDの内容・対応要件は `docs/04_test/test_specification.md`（4章）、および要件との対応関係は `docs/traceability_matrix.md`（③関数×テスト対応表、④要件×テスト対応表）を参照。

## 4. 手動テストの実行（`docs/04_test/manual_test_checklist.md`）

対象: COMP-04 MainWindow、COMP-05 BoardCanvas、COMP-06 AppController（GUI・Controller層）、NFR-01〜03、CON-01

### 4.1 アプリを起動する

```powershell
py src\main.py
```

### 4.2 チェックリストに沿って操作・確認する

`docs/04_test/manual_test_checklist.md` の「3. チェックリスト」に記載された手順（TC-MAN-01〜10）を上から順に実施し、期待結果と一致するかを目視で確認する。

### 4.3 結果の記録

確認できたテストIDについて、同ファイルの表の「結果」欄に `済`、「確認日」欄に実施日（YYYY-MM-DD）を記入する。期待結果と異なる場合は「未」のままとし、備考欄等に事象を記録した上でユーザー・Claudeと共有する。

## 5. うまく実行できない場合

- `py` コマンドが見つからない、または想定と異なるPythonが起動する場合は、CLAUDE.md「実装環境（Python）」章を参照し、`py`ランチャーの既定バージョンがPython 3.9.13になっているか確認する。
- `python`（`py`ではなく）コマンドで実行すると、Microsoft Storeのスタブに繋がり正しく動作しないことがあるため、本プロジェクトでは必ず `py` コマンドを使用する。
- `tkinter`関連のエラーが出る場合は、使用しているPython環境に`tkinter`（Tk 8.6）が含まれているかを確認する（3.9.13環境では動作確認済み）。

## 6. まとめ

| 種別 | 対象 | 実行コマンド | 詳細 |
|---|---|---|---|
| 自動単体テスト | ロジック層（COMP-01〜03, 07） | `py -m unittest discover tests` | `docs/04_test/test_specification.md` |
| 手動テスト | GUI・Controller層（COMP-04〜06）、NFR-01〜03, CON-01 | `py src\main.py` を起動しチェックリストを確認 | `docs/04_test/manual_test_checklist.md` |
