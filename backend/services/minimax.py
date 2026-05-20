import httpx
import os
import json
from typing import Optional

class MiniMaxService:
    def __init__(self):
        self._api_key = None
        self._base_url = None
        self._model = None

    @property
    def api_key(self):
        if self._api_key is None:
            self._api_key = os.getenv("MINIMAX_API_KEY")
        return self._api_key

    @property
    def base_url(self):
        if self._base_url is None:
            self._base_url = os.getenv("MINIMAX_BASE_URL", "https://api.minimax.chat")
        return self._base_url

    @property
    def model(self):
        if self._model is None:
            self._model = os.getenv("MINIMAX_MODEL", "abab6.5s-chat")
        return self._model

    async def analyze_text(self, text: str) -> dict:
        prompt = f"""你是一個資料分析專家。請分析以下文字內容，自動識別內容類型並提取結構化資訊。

內容：
{text}

請根據內容自動判斷類型，並輸出對應的 JSON 結構：

**會議記錄 (meeting)** — 包含與會人員、討論事項、行動項目
**數據表格 (data_table)** — 純數字/文字列表、統計資料、排行榜
**合同法務 (contract)** — 法條、權利義務、條款項目
**報告分析 (report)** — 調研報告、財務分析、業績報告
**Bug問題分析 (bug_report)** — Bug列表、異常問題、缺陷追蹤、測試報告
**課程演講 (lecture)** — 教學內容、演講大綱、知識點
**財務報表 (financial)** — 收入支出、資產負債、數字統計

輸出格式（根據內容自動選擇）：
{{
  "content_type": "meeting" 或 "data_table" 或 "contract" 或 "report" 或 "bug_report" 或 "lecture" 或 "financial",
  "meeting_overview": {{
    "主題": "...",
    "日期": "...",
    "與會人員": ["姓名1", "姓名2"],
    "重點摘要": "..."
  }},
  "action_items": [
    {{
      "項目名稱": "...",
      "負責人": "...",
      "狀態": "pending" 或 "in_progress" 或 "completed",
      "截止日期": "..."
    }}
  ],
  "data_table": {{
    "title": "表格標題",
    "headers": ["欄位1", "欄位2"],
    "rows": [["資料1", "資料2"], ...],
    "summary": "對此數據表格的簡短總結，描述主要趨勢、重點或觀察結論"
  }},
  "bug_report": {{
    "標題": "Bug列表或問題報告標題",
    "摘要": "整體問題的簡短描述，描述主要問題類型和影響範圍",
    "headers": ["Bug ID", "嚴重程度", "問題描述", "狀態", "建立日期", "負責人"],
    "rows": [
      ["BUG-001", "High", "問題描述...", "OPEN", "2025/05/19", "張三"],
      ...
    ],
    "關鍵發現": ["發現1：主要問題是...", "發現2：...],
    "建議": "後續建議或待處理事項"
  }},
  "contract_info": {{
    "標題": "...",
    "甲方": "...",
    "乙方": "...",
    "關鍵條款": ["條款1", "條款2"],
    "風險提示": "..."
  }},
  "report_info": {{
    "標題": "...",
    "摘要": "...",
    "關鍵發現": ["發現1", "發現2"],
    "建議": "..."
  }},
  "lecture_info": {{
    "標題": "...",
    "大綱": ["章節1", "章節2"],
    "知識點": ["重點1", "重點2"]
  }},
  "financial_info": {{
    "標題": "...",
    "期間": "...",
    "項目": ["項目1", "項目2"],
    "數值": [["項目", "金額"], ...]
  }}
}}

規則：
- content_type 必須根據實際內容自動判斷，不要預設
- 如果內容是Bug列表、異常問題、測試報告，請優先判斷為 bug_report
- 對於 bug_report 類型，請同時提取 headers 和 rows 結構
- 無法判斷的欄位設為 null 或空陣列
- action_items 從會議內容中自動識別，若無則回傳空陣列
- 只輸出 JSON，不要有其他文字
- 狀態只能是 pending / in_progress / completed 三種之一"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/v1/messages",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            print(f"[DEBUG] API response: {result}")

            # Anthropic-compatible format: content is an array with text blocks
            content_list = result.get("content", [])
            content = ""
            for block in content_list:
                if block.get("type") == "text":
                    content = block.get("text", "")
                    break

            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]

            return json.loads(content.strip())

minimax_service = MiniMaxService()