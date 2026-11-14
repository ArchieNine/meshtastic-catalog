from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "data/catalog.json").read_text(encoding="utf-8-sig"))
models = data["models"]
display = data["public_display"]
ids = [m["id"] for m in models]
assert len(ids) == len(set(ids)), "模型 ID 重複"
assert all(i in display and "zh" in display[i] and "en" in display[i] for i in ids), "缺少中英文顯示資料"
assert all(re.match(r"^https?://", m.get("url", "")) for m in models), "模型來源網址缺失"
assert data["stats"]["records"] == len(models), "請同步更新 stats.records 與頁面發布說明"

def safe_json(x):
    return json.dumps(x, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")

template = (ROOT / "tools/template.html").read_text(encoding="utf-8")
for token in ("__CATALOG_DATA__", "__PUBLIC_DISPLAY__"):
    assert template.count(token) == 1, "版型資料位置有誤"
html = template.replace("__CATALOG_DATA__", safe_json(data)).replace("__PUBLIC_DISPLAY__", safe_json(display))
(ROOT / "docs/index.html").write_text(html, encoding="utf-8", newline="\n")
print(f"已產生網站：{len(models)} 筆，{len(display)} 筆顯示資料。")
