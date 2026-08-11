# 関数設計書（詳細設計）

## 1. 文書情報

| 項目 | 内容 |
|---|---|
| プロジェクト名 | 五目並べゲーム (Gomoku) |
| 版数 | 1.0 |
| 作成日 | 2026-08-11 |
| 対象 | `docs/02_component_design/component_design.md` v1.0（承認済み） |

## 2. 目的・位置づけ

コンポーネント設計書で定義した各コンポーネント（COMP-01〜07）について、内部の関数・メソッドの入出力仕様（引数・戻り値・正常系／異常系の挙動）を定める。
CLAUDE.md の品質方針（テスト容易性）に基づき、ロジック層（COMP-01〜03）の関数は副作用を持たない入出力仕様として記述し、そのままテストケース設計（`docs/04_test/`）に転用できる粒度とする。

関数IDは `FUNC-01, FUNC-02, ...` の連番とし、所属コンポーネントを明記する。

## 3. 型定義（各関数の入出力で共通して用いる型）

実装時の具体的な表現（dataclass／NamedTuple／dict等）は問わないが、フィールド名・意味はここで固定し、関数設計・テスト設計の基準とする。

| 型名 | 定義 |
|---|---|
| `Color` | 石の色。`BLACK` または `WHITE`（値は `constants.py` で定義。COMP-07参照） |
| `StoneValue` | 盤面マスの状態。`EMPTY` / `BLACK` / `WHITE` のいずれか |
| `GameStatus` | 着手結果の状態。`ONGOING`（継続）／`WIN`（勝利成立）／`DRAW`（引き分け）／`ALREADY_OVER`（対局終了後の着手要求）／`INVALID_MOVE`（既に石がある交点への着手要求） |
| `WinResult` | `is_win: bool`（勝利成立か）, `cells: list[tuple[int, int]]`（勝利成立時のハイライト対象座標一覧。不成立時は空リスト） |
| `MoveResult` | `success: bool`（着手が受理されたか）, `status: GameStatus`, `winner: Color \| None`（勝者。未確定/引き分けは`None`）, `highlight_cells: list[tuple[int, int]]`, `current_turn: Color`（この結果の後の手番） |
| 座標 | `(row, col)` の `tuple[int, int]`。`0 <= row, col <= BOARD_SIZE - 1` |

## 4. COMP-07 Constants（定数一覧）

関数ではなく定数群のため、関数IDは付与しない。他の全関数はここで定義される定数を参照し、値をハードコーディングしない（NFR-05）。

| 定数名 | 内容例 | 対応要件 |
|---|---|---|
| `BOARD_SIZE` | 15（盤面マス数） | NFR-05, CON-02 |
| `WIN_LENGTH` | 5（勝利に必要な連続数） | NFR-05, CON-02 |
| `EMPTY`, `BLACK`, `WHITE` | 盤面マスの状態・石の色を表す値 | NFR-05 |
| `CELL_SIZE` | 1マスあたりのピクセル数 | NFR-05 |
| `MARGIN` | 盤面外周の余白（ピクセル） | NFR-05 |
| `WINDOW_WIDTH`, `WINDOW_HEIGHT` | ウィンドウサイズ（ピクセル） | NFR-05 |
| `STONE_COLORS` | `Color` → tkinter描画色のマッピング | NFR-05 |
| `HIGHLIGHT_COLOR` | 勝利ハイライトの表示色 | NFR-05 |

## 5. COMP-01 Board（盤面モデル）

| 関数ID | 関数 | 概要 |
|---|---|---|
| FUNC-01 | `place_stone(row, col, color) -> bool` | 指定交点に石を置く |
| FUNC-02 | `get_stone(row, col) -> StoneValue` | 指定交点の状態を取得する |
| FUNC-03 | `is_full() -> bool` | 盤面が全て埋まっているかを判定する |
| FUNC-04 | `reset() -> None` | 盤面を初期状態（全マス`EMPTY`）に戻す |

### FUNC-01 `Board.place_stone(row: int, col: int, color: Color) -> bool`
- **引数**: `row`, `col`（着手先座標）／`color`（置く石の色）
- **戻り値**: 着手が成功したか（`True`=成功／`False`=既に石があり失敗）
- **事前条件**: `0 <= row, col <= BOARD_SIZE - 1`（範囲外は `ValueError`）
- **正常系**: 対象マスが `EMPTY` の場合、`color` を設定し `True` を返す
- **異常系**: 対象マスが `EMPTY` 以外（既に石がある）場合、盤面を変更せず `False` を返す
- **対応要件**: REQ-04, REQ-05

### FUNC-02 `Board.get_stone(row: int, col: int) -> StoneValue`
- **引数**: `row`, `col`
- **戻り値**: 対象マスの状態（`EMPTY`/`BLACK`/`WHITE`）
- **事前条件**: `0 <= row, col <= BOARD_SIZE - 1`（範囲外は `ValueError`）
- **正常系**: 対象マスの状態を返す（副作用なし）
- **対応要件**: REQ-04, REQ-05

### FUNC-03 `Board.is_full() -> bool`
- **引数**: なし
- **戻り値**: 全225マスに石があるかどうか
- **正常系**: 空きマスが1つもない場合 `True`、それ以外は `False`
- **対応要件**: REQ-10

### FUNC-04 `Board.reset() -> None`
- **引数**: なし
- **戻り値**: なし
- **正常系**: 全マスを `EMPTY` にする
- **対応要件**: REQ-13

## 6. COMP-02 WinChecker（勝敗判定ロジック）

| 関数ID | 関数 | 概要 |
|---|---|---|
| FUNC-05 | `check_win(board, row, col, color) -> WinResult` | 起点座標を基準に勝利成立を判定し、成立時はハイライト対象座標を返す |

### FUNC-05 `WinChecker.check_win(board: Board, row: int, col: int, color: Color) -> WinResult`
- **引数**: `board`（判定対象の盤面）／`row`, `col`（直前に石が置かれた座標）／`color`（判定対象の色。通常は直前に置かれた石の色）
- **戻り値**: `WinResult`（`is_win`, `cells`）
- **事前条件**: `board.get_stone(row, col) == color` であること（呼び出し側が直前の着手座標を渡す契約。GameStateからのみ呼び出される）
- **正常系（判定方法）**: 縦／横／右上がり斜め／右下がり斜めの4方向それぞれについて、起点 `(row, col)` から両方向に同色 `color` の連続マスを数える。いずれかの方向で連続数が `WIN_LENGTH`（5）以上（長連含む）の場合、`is_win = True` とし、`cells` にはその方向で連続している同色マスの座標を**連続分すべて**含める（5つに限らない。REQ-12）。複数方向が同時に成立した場合は、成立した全方向の座標を`cells`に統合する（重複は除く）
- **異常系**: いずれの方向でも `WIN_LENGTH` に達しない場合、`is_win = False`, `cells = []`
- **対応要件**: REQ-08, REQ-09, REQ-12, CON-02

## 7. COMP-03 GameState（対局状態管理）

| 関数ID | 関数 | 概要 |
|---|---|---|
| FUNC-06 | `play(row, col) -> MoveResult` | 現在の手番で着手を試み、判定・状態更新を行う |
| FUNC-07 | `get_current_turn() -> Color` | 現在の手番を取得する |
| FUNC-08 | `is_game_over() -> bool` | 対局が終了しているかを取得する |
| FUNC-09 | `get_result() -> Color \| Literal["DRAW"] \| None` | 対局結果を取得する |
| FUNC-10 | `get_highlight_cells() -> list[tuple[int, int]]` | 勝利時のハイライト対象座標を取得する |
| FUNC-11 | `reset() -> None` | 対局状態を初期化する（Boardのリセットを含む） |

### FUNC-06 `GameState.play(row: int, col: int) -> MoveResult`
- **引数**: `row`, `col`（クリックされた交点座標）
- **戻り値**: `MoveResult`
- **正常系・異常系（分岐）**:
  1. 対局が既に終了している（`is_game_over() == True`）場合: Boardを変更せず `success=False, status=ALREADY_OVER, winner=現在の勝者/None, highlight_cells=現在のハイライト, current_turn=現在の手番` を返す（REQ-11）
  2. `board.place_stone(row, col, 現在の手番の色)` が `False`（既に石がある）場合: `success=False, status=INVALID_MOVE, winner=None, highlight_cells=[], current_turn=現在の手番（変更なし）` を返す（REQ-05）
  3. 着手成功時、`win_checker.check_win(board, row, col, 現在の手番の色)` を実行:
     - 勝利成立（`is_win=True`）: 内部状態を「対局終了・勝者=現在の手番」に更新し、`success=True, status=WIN, winner=現在の手番, highlight_cells=判定結果のcells, current_turn=現在の手番（手番交代なし）` を返す（REQ-08, REQ-09, REQ-12）
     - 勝利不成立かつ `board.is_full() == True`: 内部状態を「対局終了・引き分け」に更新し、`success=True, status=DRAW, winner=None, highlight_cells=[], current_turn=現在の手番` を返す（REQ-10）
     - それ以外（対局継続）: 手番を相手の色に交代し、`success=True, status=ONGOING, winner=None, highlight_cells=[], current_turn=交代後の手番` を返す（REQ-06）
- **対応要件**: REQ-04, REQ-05, REQ-06, REQ-08, REQ-09, REQ-10, REQ-11, REQ-12

### FUNC-07 `GameState.get_current_turn() -> Color`
- **引数**: なし
- **戻り値**: 現在の手番の色（対局終了後は終了時点の手番を返す）
- **対応要件**: REQ-07

### FUNC-08 `GameState.is_game_over() -> bool`
- **引数**: なし
- **戻り値**: 対局が終了している（勝者確定または引き分け確定）かどうか
- **対応要件**: REQ-11

### FUNC-09 `GameState.get_result() -> Color | Literal["DRAW"] | None`
- **引数**: なし
- **戻り値**: 対局が終了していない場合は `None`。勝者確定時は勝者の `Color`。引き分け確定時は文字列 `"DRAW"`
- **対応要件**: REQ-09, REQ-10

### FUNC-10 `GameState.get_highlight_cells() -> list[tuple[int, int]]`
- **引数**: なし
- **戻り値**: 直近の勝利判定で得られたハイライト対象座標一覧（勝利していない場合は空リスト）
- **対応要件**: REQ-12

### FUNC-11 `GameState.reset() -> None`
- **引数**: なし
- **戻り値**: なし
- **正常系**: `board.reset()` を呼び、手番を `BLACK`（先手）に、対局終了フラグ・勝者・ハイライト対象座標を初期状態に戻す
- **対応要件**: REQ-13

## 8. COMP-04 MainWindow（メインウィンドウ）

| 関数ID | 関数 | 概要 |
|---|---|---|
| FUNC-12 | `update_status_text(text) -> None` | 手番／勝敗結果の表示テキストを更新する |
| FUNC-13 | `set_reset_callback(callback) -> None` | リセットボタン押下時のコールバックを登録する |

### FUNC-12 `MainWindow.update_status_text(text: str) -> None`
- **引数**: `text`（表示する文字列。文言の組み立て（例:「黒の番です」「白の勝ちです」「引き分けです」）はAppController側の責務とし、本関数は受け取った文字列をそのまま表示する）
- **戻り値**: なし
- **対応要件**: REQ-07, REQ-09, REQ-10

### FUNC-13 `MainWindow.set_reset_callback(callback: Callable[[], None]) -> None`
- **引数**: `callback`（リセットボタン押下時に呼び出す関数。引数なし）
- **戻り値**: なし
- **対応要件**: REQ-13

## 9. COMP-05 BoardCanvas（盤面描画・入力）

| 関数ID | 関数 | 概要 |
|---|---|---|
| FUNC-14 | `draw_grid() -> None` | 盤面の格子線を描画する |
| FUNC-15 | `draw_stone(row, col, color) -> None` | 指定座標に指定色の石を描画する |
| FUNC-16 | `draw_highlight(cells) -> None` | 指定座標一覧をハイライト表示する |
| FUNC-17 | `clear() -> None` | 盤面表示をクリアする |
| FUNC-18 | `set_click_callback(callback) -> None` | クリックコールバックを登録する |
| FUNC-19 | `pixel_to_grid(x, y) -> tuple[int, int] \| None` | ピクセル座標を交点座標に変換する（内部関数） |

### FUNC-14 `BoardCanvas.draw_grid() -> None`
- **引数**: なし
- **戻り値**: なし
- **正常系**: `BOARD_SIZE × BOARD_SIZE` の格子線を `CELL_SIZE`, `MARGIN` に基づき描画する
- **対応要件**: REQ-01, REQ-02

### FUNC-15 `BoardCanvas.draw_stone(row: int, col: int, color: Color) -> None`
- **引数**: `row`, `col`（描画先の交点座標）／`color`
- **戻り値**: なし
- **正常系**: `STONE_COLORS[color]` の色で交点上に石（円）を描画する
- **対応要件**: REQ-04

### FUNC-16 `BoardCanvas.draw_highlight(cells: list[tuple[int, int]]) -> None`
- **引数**: `cells`（ハイライト対象の座標一覧）
- **戻り値**: なし
- **正常系**: `cells` の各座標に `HIGHLIGHT_COLOR` でハイライト（枠等）を描画する。`cells` が空の場合は何もしない
- **対応要件**: REQ-12

### FUNC-17 `BoardCanvas.clear() -> None`
- **引数**: なし
- **戻り値**: なし
- **正常系**: 石・ハイライトの描画のみを消去する（格子線は残す。再描画が必要な場合はAppControllerが `draw_grid()` を別途呼び出す）
- **対応要件**: REQ-13

### FUNC-18 `BoardCanvas.set_click_callback(callback: Callable[[int, int], None]) -> None`
- **引数**: `callback`（有効な交点がクリックされた際に `(row, col)` を渡して呼び出す関数）
- **戻り値**: なし
- **対応要件**: REQ-04

### FUNC-19 `BoardCanvas.pixel_to_grid(x: int, y: int) -> tuple[int, int] | None`（内部関数、tkinterのクリックイベントハンドラから呼び出す）
- **引数**: `x`, `y`（キャンバス上のクリックのピクセル座標）
- **戻り値**: 最寄りの交点座標 `(row, col)`。盤面外クリックと判定された場合は `None`
- **正常系（判定方法）**:
  1. `col = round((x - MARGIN) / CELL_SIZE)`, `row = round((y - MARGIN) / CELL_SIZE)` で最寄りの交点を求める
  2. `row` または `col` が `0 <= row, col <= BOARD_SIZE - 1` の範囲外の場合、`None` を返す（無効なクリック）
  3. 範囲内の場合、`(row, col)` を返す
- **補足**: 上記の `round()` により、各交点は縦横 `CELL_SIZE/2` 分の許容範囲（最寄り判定）を持つ。盤面の余白（`MARGIN`）部分のクリックのうち、最寄り交点が範囲外になるものはステップ2で `None` となり、`set_click_callback` に登録されたコールバックは呼び出されない
- **対応要件**: REQ-04

## 10. COMP-06 AppController（アプリケーション制御）

| 関数ID | 関数 | 概要 |
|---|---|---|
| FUNC-20 | `on_board_click(row, col) -> None` | 盤面クリック時の一連の処理を行う |
| FUNC-21 | `on_reset_click() -> None` | リセットボタン押下時の一連の処理を行う |
| FUNC-22 | `initialize() -> None` | 起動時の初期表示処理を行う |

### FUNC-20 `AppController.on_board_click(row: int, col: int) -> None`
- **引数**: `row`, `col`（`BoardCanvas.set_click_callback` 経由で渡される交点座標。`pixel_to_grid` で無効と判定されたクリックはこの関数に到達しない）
- **戻り値**: なし（GUI層への描画・表示更新の指示が副作用として発生する）
- **正常系（処理内容）**:
  1. `game_state.play(row, col)` を呼び出し `MoveResult` を得る
  2. `result.status` が `INVALID_MOVE` または `ALREADY_OVER` の場合、GUI更新は行わない（REQ-05, REQ-11）
  3. `result.status` が `ONGOING` / `WIN` / `DRAW` のいずれかの場合:
     - `board_canvas.draw_stone(row, col, 着手した色)` を呼ぶ
     - `result.status == WIN` の場合、`board_canvas.draw_highlight(result.highlight_cells)` を呼ぶ（REQ-12）
     - `main_window.update_status_text(...)` を、`result.status` に応じた表示文言（手番表示／勝者表示／引き分け表示）で呼ぶ（REQ-07, REQ-09, REQ-10）
- **非機能要件対応**: 上記処理は同期的に完結させ、非同期処理・待機を挟まない（NFR-03）
- **対応要件**: REQ-04, REQ-05, REQ-06, REQ-07, REQ-09, REQ-10, REQ-11, REQ-12, NFR-03

### FUNC-21 `AppController.on_reset_click() -> None`
- **引数**: なし
- **戻り値**: なし
- **正常系（処理内容）**: `game_state.reset()` → `board_canvas.clear()` → `main_window.update_status_text(...)` を先手（黒）の手番表示で呼ぶ、の順に実行する
- **対応要件**: REQ-13

### FUNC-22 `AppController.initialize() -> None`
- **引数**: なし
- **戻り値**: なし
- **正常系（処理内容）**: `board_canvas.set_click_callback(self.on_board_click)`、`main_window.set_reset_callback(self.on_reset_click)` を登録した上で、`board_canvas.draw_grid()` と、先手（黒）の手番表示を `main_window.update_status_text(...)` で行う
- **対応要件**: REQ-07（初期表示）, NFR-02（起動時処理の一部。起動処理本体は `src/main.py` が担う）

## 11. 今後の工程

本書のレビュー・承認後、以下を進める。

1. 実装（`src/`）。本書の関数ID・入出力仕様に対応する形でモジュール（4章の一覧）を実装する
2. テスト仕様書作成・テストコード実装（`docs/04_test/`, `tests/`）。ロジック層（COMP-01〜03）の関数は本書の「正常系／異常系」をそのままテストケースの元とする

あわせて `docs/traceability_matrix.md` の「②コンポーネント×関数対応表」を本書の内容で更新する。
