# トレーサビリティマトリックス

要件定義〜テストまでの対応関係を追跡する。1つの表に全工程を詰め込まず、**隣接する工程どうしの対応表**を4つ用意する方式とする。

各表は、上流工程のIDを行・下流工程のIDを列に配置した**マトリクス形式**とし、関連がある交点に「○」を付ける（同じ行・列が複数の交点に○を持ってよく、一対多・多対一・多対多をすべて自然に表現できる）。対応関係の**具体的な根拠**（なぜ関連するか）はこの表には書かず、各工程の成果物（コンポーネント設計書・関数設計書・テスト仕様書）側にID単位で明記する。

各工程の成果物を作成・更新するたびに、該当するマトリクスに○を追記すること（ルールは `CLAUDE.md` の「トレーサビリティマトリックス」章を参照）。

**更新履歴**:
- 2026-08-11、関数設計書レビューで検出した対応要件欄の不整合修正に伴い、「①要件×コンポーネント対応表」にREQ-08×COMP-03、REQ-09×COMP-02、REQ-10×COMP-01、REQ-12×COMP-03の○を追加（`docs/02_component_design/component_design.md` v1.1に合わせて更新）。
- 2026-08-11、テスト仕様書（`docs/04_test/test_specification.md`）・手動テストチェックリスト（`docs/04_test/manual_test_checklist.md`）・テストコード（`tests/`）の作成に伴い、「③関数×テスト対応表」「④要件×テスト対応表」にテストモジュールID（TEST-BOARD, TEST-WINCHECKER, TEST-GAMESTATE, TEST-CONSTANTS, TEST-MANUAL）と個々のテストIDを追記。全要件ID（REQ/NFR/CON）の行に最低1つのテストIDが記載されていることを確認済み（NFR-04, CON-03は注記の通りテスト対象外）。

## 要件一覧（参照用）

詳細は `docs/01_requirements/requirements.md` を正とする。ここではIDと概要のみを掲載する。

| 要件ID | 概要 |
|---|---|
| REQ-01 | 15×15マスの盤面をGUIで描画 |
| REQ-02 | 盤面交点の視認性確保 |
| REQ-03 | 2人のプレイヤーが交互に手番（先手は黒） |
| REQ-04 | 空いている交点のクリックで石を置く |
| REQ-05 | 石がある交点をクリックしても何もしない |
| REQ-06 | 石を置くごとに手番交代 |
| REQ-07 | 現在の手番をGUI上に表示 |
| REQ-08 | 五連・長連（6つ以上）の判定 |
| REQ-09 | 五連成立時に対局終了・勝者表示 |
| REQ-10 | 盤面が埋まり五連不成立で引き分け表示 |
| REQ-11 | 対局終了後は石を置けない |
| REQ-12 | 勝利判定対象の石をハイライト表示（長連は全て） |
| REQ-13 | 盤面をクリアして新しい対局を開始する操作 |
| NFR-01 | Python・tkinter（追加パッケージ不要） |
| NFR-02 | Windows GUIアプリとして起動可能 |
| NFR-03 | クリックから石表示・手番交代までの応答遅延なし |
| NFR-04 | Gitでのバージョン管理（ローカルのみ） |
| NFR-05 | 盤面サイズ等を定数として分離定義 |
| CON-01 | 対局モードは人対人のみ |
| CON-02 | 盤面15×15・五連固定（可変設定なし） |
| CON-03 | 棋譜の保存・読み込みは対象外 |

## 1. 要件×コンポーネント対応表

行＝要件ID、列＝コンポーネントID。対応関係の根拠は `docs/02_component_design/component_design.md` の各コンポーネントの「責務」「対応要件」を正とする。

| 要件ID＼コンポーネントID | COMP-01 | COMP-02 | COMP-03 | COMP-04 | COMP-05 | COMP-06 | COMP-07 |
|---|---|---|---|---|---|---|---|
| REQ-01 | | | | | ○ | | |
| REQ-02 | | | | | ○ | | |
| REQ-03 | | | ○ | | | | |
| REQ-04 | ○ | | ○ | | ○ | ○ | |
| REQ-05 | ○ | | ○ | | | ○ | |
| REQ-06 | | | ○ | | | ○ | |
| REQ-07 | | | ○ | ○ | | ○ | |
| REQ-08 | | ○ | ○ | | | | |
| REQ-09 | | ○ | ○ | ○ | | ○ | |
| REQ-10 | ○ | | ○ | ○ | | ○ | |
| REQ-11 | | | ○ | | | ○ | |
| REQ-12 | | ○ | ○ | | ○ | ○ | |
| REQ-13 | ○ | | ○ | ○ | ○ | ○ | |
| NFR-01 | | | | ○ | ○ | | |
| NFR-02 | | | | | | | |
| NFR-03 | | | | | | ○ | |
| NFR-04 | | | | | | | |
| NFR-05 | ○ | ○ | | ○ | ○ | | ○ |
| CON-01 | | | ○ | | | | |
| CON-02 | | ○ | | | | | ○ |
| CON-03 | | | | | | | |

注記（該当コンポーネントなしの行）:
- NFR-02（Windows GUIアプリとして起動可能）: `src/main.py` の起動処理で対応するため、該当コンポーネントなし
- NFR-04（Gitでのバージョン管理）: プロジェクトのGit運用のみで対応するため、該当コンポーネントなし
- CON-03（棋譜の保存・読み込みは対象外）: スコープ外のため、該当コンポーネントなし

## 2. コンポーネント×関数対応表

行＝コンポーネントID、列＝関数ID。対応関係の根拠は `docs/03_function_design/function_design.md` の各関数の記述を正とする。

| コンポーネントID＼関数ID | FUNC-01 | FUNC-02 | FUNC-03 | FUNC-04 | FUNC-05 | FUNC-06 | FUNC-07 | FUNC-08 | FUNC-09 | FUNC-10 | FUNC-11 | FUNC-12 | FUNC-13 | FUNC-14 | FUNC-15 | FUNC-16 | FUNC-17 | FUNC-18 | FUNC-19 | FUNC-20 | FUNC-21 | FUNC-22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| COMP-01 | ○ | ○ | ○ | ○ | | | | | | | | | | | | | | | | | | |
| COMP-02 | | | | | ○ | | | | | | | | | | | | | | | | | |
| COMP-03 | | | | | | ○ | ○ | ○ | ○ | ○ | ○ | | | | | | | | | | | |
| COMP-04 | | | | | | | | | | | | ○ | ○ | | | | | | | | | |
| COMP-05 | | | | | | | | | | | | | | ○ | ○ | ○ | ○ | ○ | ○ | | | |
| COMP-06 | | | | | | | | | | | | | | | | | | | | ○ | ○ | ○ |
| COMP-07 | | | | | | | | | | | | | | | | | | | | | | |

注記: COMP-07（Constants）は定数群のため対応する関数を持たない（各関数が定数を参照する）。

## 3. 関数×テスト対応表

行＝関数ID、列＝テストモジュール（テストファイル）ID。関数・テストケースは件数が多くなりやすいため、列は個々のテストIDではなくテストモジュール単位とし、セルには該当する具体的なテストIDを複数列挙してよい（例: `TEST-03, TEST-07`）。対応関係の根拠は `docs/04_test/test_specification.md` を正とする。COMP-04〜06（GUI層・Controller層）の関数は自動単体テストの対象外のため、`docs/04_test/manual_test_checklist.md`（TEST-MANUAL）のみを対応させる。

| 関数ID＼テストモジュールID | TEST-BOARD | TEST-WINCHECKER | TEST-GAMESTATE | TEST-CONSTANTS | TEST-MANUAL |
|---|---|---|---|---|---|
| FUNC-01 | TC-BOARD-01, TC-BOARD-02, TC-BOARD-03 | | | | |
| FUNC-02 | TC-BOARD-01, TC-BOARD-04, TC-BOARD-05 | | | | |
| FUNC-03 | TC-BOARD-06, TC-BOARD-07 | | | | |
| FUNC-04 | TC-BOARD-08 | | | | |
| FUNC-05 | | TC-WIN-01〜TC-WIN-09 | | | |
| FUNC-06 | | | TC-GS-02〜TC-GS-06, TC-GS-11 | | |
| FUNC-07 | | | TC-GS-01, TC-GS-02 | | TC-MAN-02, TC-MAN-03 |
| FUNC-08 | | | TC-GS-07, TC-GS-08 | | |
| FUNC-09 | | | TC-GS-07, TC-GS-08 | | |
| FUNC-10 | | | TC-GS-09 | | |
| FUNC-11 | | | TC-GS-10 | | |
| FUNC-12 | | | | | TC-MAN-02, TC-MAN-03, TC-MAN-05, TC-MAN-06, TC-MAN-07 |
| FUNC-13 | | | | | TC-MAN-07 |
| FUNC-14 | | | | | TC-MAN-01 |
| FUNC-15 | | | | | TC-MAN-03 |
| FUNC-16 | | | | | TC-MAN-05 |
| FUNC-17 | | | | | TC-MAN-07 |
| FUNC-18 | | | | | TC-MAN-03 |
| FUNC-19 | | | | | TC-MAN-03, TC-MAN-04 |
| FUNC-20 | | | | | TC-MAN-03, TC-MAN-04, TC-MAN-05, TC-MAN-06 |
| FUNC-21 | | | | | TC-MAN-07 |
| FUNC-22 | | | | | TC-MAN-01, TC-MAN-02 |

（COMP-07 Constants自体には関数IDが無いため、この表には現れない。TEST-CONSTANTSはCON-02・NFR-05への対応として「4. 要件×テスト対応表」側で扱う）

## 4. 要件×テスト対応表（直接検証トレース）

行＝要件ID、列＝テストモジュール（テストファイル）ID。セルには該当する具体的なテストIDを複数列挙してよい（例: `TEST-03, TEST-07`）。テスト工程完了時には、全要件ID（REQ/NFR/CON）の行に最低1つのテストIDが記載されていることを、テストの網羅性チェックに用いる。

| 要件ID＼テストモジュールID | TEST-BOARD | TEST-WINCHECKER | TEST-GAMESTATE | TEST-CONSTANTS | TEST-MANUAL |
|---|---|---|---|---|---|
| REQ-01 | | | | | TC-MAN-01 |
| REQ-02 | | | | | TC-MAN-01 |
| REQ-03 | | | TC-GS-01, TC-GS-10 | | |
| REQ-04 | TC-BOARD-01 | | TC-GS-02 | | TC-MAN-03 |
| REQ-05 | TC-BOARD-02 | | TC-GS-03 | | TC-MAN-04 |
| REQ-06 | | | TC-GS-02 | | TC-MAN-03 |
| REQ-07 | | | TC-GS-01 | | TC-MAN-02, TC-MAN-03 |
| REQ-08 | | TC-WIN-01〜TC-WIN-07 | TC-GS-04, TC-GS-11 | | |
| REQ-09 | | TC-WIN-01〜TC-WIN-04 | TC-GS-04, TC-GS-07 | | TC-MAN-05 |
| REQ-10 | TC-BOARD-06, TC-BOARD-07 | | TC-GS-05, TC-GS-08 | | TC-MAN-06 |
| REQ-11 | | | TC-GS-06 | | TC-MAN-05 |
| REQ-12 | | TC-WIN-06, TC-WIN-09 | TC-GS-04, TC-GS-09, TC-GS-11 | | TC-MAN-05 |
| REQ-13 | TC-BOARD-08 | | TC-GS-10 | | TC-MAN-07 |
| NFR-01 | | | | | TC-MAN-08 |
| NFR-02 | | | | | TC-MAN-08 |
| NFR-03 | | | | | TC-MAN-09 |
| NFR-04 | | | | | （注記参照） |
| NFR-05 | | | | TC-CONST-01, TC-CONST-02 | |
| CON-01 | | | | | TC-MAN-10 |
| CON-02 | TC-BOARD-03 | TC-WIN-08 | | TC-CONST-01, TC-CONST-02 | |
| CON-03 | | | | | （注記参照） |

注記:
- NFR-04（Gitでのバージョン管理）: プロジェクトのGit運用そのものであり、アプリケーションの動作としてのテストケースを設けない（「①要件×コンポーネント対応表」の注記と同様の扱い）。
- CON-03（棋譜の保存・読み込みは対象外）: スコープ外機能が存在しないことの確認であり、実装物に対する積極的なテストケースを設けない。
