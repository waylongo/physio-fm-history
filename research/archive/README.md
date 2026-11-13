# 已退役的生成脚本

`build_entries.py` 与 `build_meta.py` 是第一版数据的编写脚本，**已退役，请勿运行**：它们会用旧内容覆盖 `data/*.json`。

自第二版（2026-11-13）起，`data/entries.json` 与 `data/meta.json` 是唯一数据源。第二版的增改记录在 `research/migrate_v2.py`（幂等，只按 id 更新）。
