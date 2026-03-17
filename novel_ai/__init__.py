from typing import List, Dict, Optional
import json
from .core import NovelCore

class NovelAI:
    """AI 小说创作主类"""
    
    def __init__(self, api_key: str, base_url: str, model: str = "gpt-4o"):
        self.core = NovelCore(api_key, base_url, model)
    
    def generate_outline(self, genre: str, keywords: str, length: str = "长篇") -> Dict:
        """生成故事大纲"""
        prompt = f"""根据以下信息生成网络小说大纲：
类型：{genre}
关键词：{keywords}
篇幅：{length}

要求：
- 包含至少10个主要情节点
- 每章有明确的标题和摘要
- 有清晰的升级体系
- 结尾要有完整的收束

输出JSON格式，包含 chapters 列表"""
        return self.core.generate(prompt)
    
    def create_character(self, name: str, role: str, archetype: str, 
                         traits: List[str]) -> Dict:
        """创建角色档案"""
        prompt = f"""为一个网络小说角色创建详细档案：
角色名：{name}
定位：{role}
类型：{archetype}
性格特点：{','.join(traits)}

输出JSON格式，包含：外貌、性格、背景、动机、说话风格"""
        return self.core.generate(prompt)
    
    def write_chapter(self, chapter_info: Dict, previous_context: str = "",
                      style: str = "流畅") -> str:
        """生成章节内容"""
        prompt = f"""根据以下信息创作网络小说章节：
章节信息：{json.dumps(chapter_info, ensure_ascii=False)}
前文背景：{previous_context}
写作风格：{style}

要求：情节紧凑，对话自然，结尾留有悬念"""
        result = self.core.generate(prompt)
        return result.get("text", str(result))
    
    def generate_dialogue(self, character: Dict, context: str, emotion: str) -> str:
        """生成角色对话"""
        prompt = f"""根据角色设定和情境生成对话：
角色：{json.dumps(character, ensure_ascii=False)}
情境：{context}
情绪：{emotion}

要求：对话自然，符合角色性格"""
        return self.core.generate(prompt).get("text", "")
    
    def analyze_style(self, style_name: str, reference_texts: List[str]) -> Dict:
        """学习并分析写作风格"""
        prompt = f"""分析以下文本的写作风格特征：
{chr(10).join(reference_texts[:5])}

输出JSON格式，包含：句子结构、常用词汇、节奏特点、描写方式"""
        return self.core.generate(prompt)