"""章节写作模块"""
from typing import Dict, List
from .core import NovelCore

class ChapterWriter:
    def __init__(self, core: NovelCore):
        self.core = core
    
    def write(self, chapter_info: Dict, previous_context: str = "",
              style: str = "流畅", word_count: int = 3000) -> str:
        import json
        prompt = f"""创作网络小说章节：
章节：{json.dumps(chapter_info, ensure_ascii=False)}
前文：{previous_context}
风格：{style}
目标：{word_count}字

要求：情节紧凑有张力，对话自然符合人设，环境描写适度，结尾留悬念"""
        return self.core.generate(prompt).get("text", "")
    
    def expand_outline_to_chapter(self, outline_item: Dict, style: str) -> str:
        prompt = f"""将以下大纲扩展为完整章节：
{outline_item}
风格：{style}
输出小说正文"""
        return self.core.generate(prompt).get("text", "")
