# 生理基础模型 · 思想年谱

按时间阅读 2019–2026 年生理基础模型的公开进展。页面上的每一条写明它要回答的问题、做法和意义，并给出原文。点开一条之后，相关论文的标题会留在页面上，可以继续在本页阅读，也可以打开原文。移动鼠标不会把它关掉。

“意义”和条目之间的关系是编者解读。标题、机构、日期和链接来自公开页面。核对日期见 `data/meta.json` 的 `updated`。

未放上年谱、但已整理过的工作保存在 `data/sources-extra.json`，页面不列出这份清单。脉络、公司对照和问题矩阵仍在 `data/meta.json`，页面不再做成单独的视图。

## 结构

```
index.html          页面
css/style.css       样式
js/app.js           读取 JSON 并渲染
data/entries.json   年谱条目与原文链接
data/meta.json      时期、四条纲、主叙事，以及未展开的脉络、公司与问题
data/sources-extra.json
assets/favicon.svg
scripts/validate.py 结构与引用校验
```

没有构建步骤，也没有第三方依赖。

## 本地预览

```bash
python3 -m http.server 8000
```

在浏览器打开 <http://localhost:8000/>。页面通过 `fetch` 读取 JSON，直接双击 `index.html` 无法加载数据。

## 校验

```bash
python3 scripts/validate.py
```

直接编辑 `data/` 里的 JSON，再运行上面的命令。条目需要的字段与现有条目一致；时期必须和日期对应（e0 在 2023-12 之前，其后依次为 e1、e2、e3、e4）。

若要额外检查仓库里是否出现不应公开的词，把词表放在仓库外，并设置 `PRIVATE_TERMS` 为该文件路径后再运行校验。词表不要放进仓库。
