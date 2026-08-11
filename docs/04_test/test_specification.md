# テスト仕様書

## 1. 文書情報

| 項目 | 内容 |
|---|---|
| プロジェクト名 | 五目並べゲーム (Gomoku) |
| 版数 | 1.0 |
| 作成日 | 2026-08-11 |
| 対象 | `docs/03_function_design/function_design.md` v1.1（承認済み） |

## 2. 目的・位置づけ

関数設計書で定義した各関数（FUNC-01〜22）のうち、CLAUDE.mdの品質方針（テスト容易性）に基づき`tkinter`に依存せず単体テスト可能なロジック層（COMP-01 Board、COMP-02 WinChecker、COMP-03 GameState）およびCOMP-07 Constantsを、`tests/`配下の自動テストコード（Python標準の`unittest`）で検証する。

GUI層（COMP-04 MainWindow、COMP-05 BoardCanvas）およびController層（COMP-06 AppController）は`tkinter`のウィジェット・イベントループに依存するため、自動単体テストの対象としない。これらの層に関連する要件、および応答性などの非機能要件は `docs/04_test/manual_test_checklist.md`（手動テストチェックリスト）で検証する。

## 3. テスト方針

- テストフレームワーク: Python標準の `unittest`
- 実行方法: `py -m unittest discover tests`（CLAUDE.md「実装環境（Python）」章の起動方法に従う）
- 各テストケースは、関数設計書に記載された対応関数の「正常系／異常系」の記述をそのままテストケース化する
- テストファイル（テストモジュール）を`docs/traceability_matrix.md`の「③関数×テスト対応表」「④要件×テスト対応表」の列（テストモジュールID）とし、個々のテストケースIDをセルに列挙する
- テストモジュールIDとテストファイルの対応は以下の通り

| テストモジュールID | テストファイル | 対象コンポーネント |
|---|---|---|
| TEST-BOARD | `tests/test_board.py` | COMP-01 Board |
| TEST-WINCHECKER | `tests/test_win_checker.py` | COMP-02 WinChecker |
| TEST-GAMESTATE | `tests/test_game_state.py` | COMP-03 GameState |
| TEST-CONSTANTS | `tests/test_constants.py` | COMP-07 Constants |
| TEST-MANUAL | `docs/04_test/manual_test_checklist.md` | COMP-04, COMP-05, COMP-06（手動確認） |

## 4. テストケース一覧（自動テスト）

### 4.1 TEST-BOARD（`tests/test_board.py`）— 対象: FUNC-01〜04

| テストID | 概要 | 対応関数 | 種別 | 対応要件 |
|---|---|---|---|---|
| TC-BOARD-01 | 空きマスに`place_stone`すると`True`が返り、`get_stone`で置いた色が取得できる | FUNC-01, FUNC-02 | 正常系 | REQ-04 |
| TC-BOARD-02 | 既に石がある交点に`place_stone`すると`False`が返り、盤面（対象マスの状態）が変化しない | FUNC-01 | 異常系 | REQ-05 |
| TC-BOARD-03 | 範囲外座標（負値・`BOARD_SIZE`以上）で`place_stone`を呼ぶと`ValueError`が送出される | FUNC-01 | 異常系（事前条件） | CON-02 |
| TC-BOARD-04 | 初期状態で任意の交点の`get_stone`が`EMPTY`を返す | FUNC-02 | 正常系 | REQ-04 |
| TC-BOARD-05 | 範囲外座標で`get_stone`を呼ぶと`ValueError`が送出される | FUNC-02 | 異常系（事前条件） | CON-02 |
| TC-BOARD-06 | 空きマスが1つでもある場合、`is_full`が`False`を返す | FUNC-03 | 正常系 | REQ-10 |
| TC-BOARD-07 | 全225マスに石がある場合、`is_full`が`True`を返す | FUNC-03 | 正常系 | REQ-10 |
| TC-BOARD-08 | 石を置いた後に`reset`を呼ぶと、全マスが`EMPTY`に戻る | FUNC-04 | 正常系 | REQ-13 |

### 4.2 TEST-WINCHECKER（`tests/test_win_checker.py`）— 対象: FUNC-05

| テストID | 概要 | 対応関数 | 種別 | 対応要件 |
|---|---|---|---|---|
| TC-WIN-01 | 横方向に同色5連 → `is_win=True`、`cells`に5マスが含まれる | FUNC-05 | 正常系 | REQ-08, REQ-09 |
| TC-WIN-02 | 縦方向に同色5連 → `is_win=True` | FUNC-05 | 正常系 | REQ-08, REQ-09 |
| TC-WIN-03 | 右下がり斜め方向に同色5連 → `is_win=True` | FUNC-05 | 正常系 | REQ-08, REQ-09 |
| TC-WIN-04 | 右上がり斜め方向に同色5連 → `is_win=True` | FUNC-05 | 正常系 | REQ-08, REQ-09 |
| TC-WIN-05 | 同色4連（5未満） → `is_win=False`, `cells=[]` | FUNC-05 | 異常系 | REQ-08 |
| TC-WIN-06 | 長連（同色6連） → `is_win=True`、`cells`に6マス全てが含まれる（5マスに限らない） | FUNC-05 | 正常系 | REQ-08, REQ-12 |
| TC-WIN-07 | 同色の連続の途中に相手の石が挟まる場合、そこで連続が途切れ5連未満なら`is_win=False` | FUNC-05 | 異常系 | REQ-08 |
| TC-WIN-08 | 起点が盤端付近にあり、方向によっては盤外参照が発生しうる場合でも例外を発生させず正しく判定する | FUNC-05 | 異常系（境界値） | REQ-08, CON-02 |
| TC-WIN-09 | 起点を通る複数方向が同時に5連成立する場合、`cells`に重複なく全方向分の座標が統合される | FUNC-05 | 正常系 | REQ-12 |

### 4.3 TEST-GAMESTATE（`tests/test_game_state.py`）— 対象: FUNC-06〜11

| テストID | 概要 | 対応関数 | 種別 | 対応要件 |
|---|---|---|---|---|
| TC-GS-01 | 初期化直後、`get_current_turn`が`BLACK`を返す | FUNC-07 | 正常系 | REQ-03 |
| TC-GS-02 | 空きマスへの`play`が成功し、`status=ONGOING`、`moved_color`=着手した色、`current_turn`が相手の色に交代する | FUNC-06 | 正常系（継続） | REQ-04, REQ-06 |
| TC-GS-03 | 既に石がある交点への`play`は`success=False, status=INVALID_MOVE, moved_color=None`となり、手番が変わらない | FUNC-06 | 異常系 | REQ-05 |
| TC-GS-04 | 5連が成立する着手で`status=WIN`、`winner`=着手した色、`current_turn`は交代しない、`highlight_cells`が判定結果と一致する | FUNC-06 | 正常系（勝利） | REQ-08, REQ-09, REQ-12 |
| TC-GS-05 | 盤面を全て埋め、5連が成立しない状態で最後の着手を行うと`status=DRAW`, `winner=None`となる | FUNC-06 | 正常系（引き分け） | REQ-10 |
| TC-GS-06 | 対局終了（勝敗確定）後に`play`を呼ぶと`success=False, status=ALREADY_OVER, moved_color=None`となり、盤面が変化しない | FUNC-06 | 異常系 | REQ-11 |
| TC-GS-07 | 勝利成立後、`is_game_over()=True`、`get_result()`が勝者の`Color`を返す | FUNC-08, FUNC-09 | 正常系 | REQ-09 |
| TC-GS-08 | 引き分け成立後、`is_game_over()=True`、`get_result()`が`"DRAW"`を返す | FUNC-08, FUNC-09 | 正常系 | REQ-10 |
| TC-GS-09 | `get_highlight_cells()`が、勝利前は空リスト、勝利成立後は判定対象座標を返す | FUNC-10 | 正常系 | REQ-12 |
| TC-GS-10 | 対局進行後（手番交代・着手済みマスあり）に`reset()`を呼ぶと、手番が`BLACK`、`is_game_over()=False`、盤面が全マス`EMPTY`、`get_highlight_cells()=[]`に戻る | FUNC-11 | 正常系 | REQ-03, REQ-13 |
| TC-GS-11 | 長連（6連）成立時、`GameState.play`経由でも`highlight_cells`に6マス全てが含まれる | FUNC-06, FUNC-10 | 正常系 | REQ-12 |

### 4.4 TEST-CONSTANTS（`tests/test_constants.py`）— 対象: COMP-07

| テストID | 概要 | 対応 | 種別 | 対応要件 |
|---|---|---|---|---|
| TC-CONST-01 | `BOARD_SIZE`が`15`である | COMP-07 | 正常系 | CON-02, NFR-05 |
| TC-CONST-02 | `WIN_LENGTH`が`5`である | COMP-07 | 正常系 | CON-02, NFR-05 |

## 5. GUI層・非機能要件の検証について

REQ-01, REQ-02（盤面のGUI描画・視認性）、REQ-07/09/10/12/13のGUI表示・描画に関わる部分、NFR-01〜03、CON-01は、`tkinter`のウィンドウ表示・実際のマウス操作・体感速度に関わるため、自動単体テストではなく`docs/04_test/manual_test_checklist.md`の手動確認項目（TEST-MANUAL, TC-MAN-01〜10）で検証する。

NFR-04（Gitでのバージョン管理）、CON-03（棋譜保存機能はスコープ外）は、アプリケーションの動作検証の対象ではない（NFR-04はプロジェクトのGit運用そのもの、CON-03は未実装であることの確認＝スコープ外項目の不在確認であり、実装物に対するテストケースを起こす対象ではない）ため、テストケースを設けない。`docs/traceability_matrix.md`の「④要件×テスト対応表」にもその旨を注記する。

## 6. 今後の工程

本書に基づき`tests/`配下にテストコードを実装し、`py -m unittest discover tests`で全件成功することを確認する。完了後、`docs/traceability_matrix.md`の「③関数×テスト対応表」「④要件×テスト対応表」を本書のテストIDで更新する。
