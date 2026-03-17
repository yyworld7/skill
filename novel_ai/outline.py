"""大纲生成模块"""
from typing import Dict, List
from .core import NovelCore

class OutlineGenerator:
    def __init__(self, core: NovelCore):
        self.core = core
    
    def generate(self, genre: str, keywords: str, length: str = "长篇") -> Dict:
        prompt = f"""根据以下信息生成网络小说大纲：
类型：{genre}
关键词：{keywords}
篇幅：{length}

要求：
- 包含至少10个主要情节点
- 每章有明确的标题和摘要
- 有清晰的升级体系
- 输出JSON格式，包含 chapters 列表"""
        return self.core.generate(prompt)
    
    def expand_chapter(self, chapter_summary: str, word_count: int = 3000) -> str:
        prompt = f"""将以下章节摘要扩展成完整的章节内容：
{chapter_summary}

目标字数：{word_count}字
要求：情节紧凑，对话自然，结尾留有悬念"""
        return self.core.generate(prompt).get("text", "")
