"""角色设计模块"""
from typing import Dict, List
from .core import NovelCore

class CharacterCreator:
    def __init__(self, core: NovelCore):
        self.core = core
    
    def create(self, name: str, role: str, archetype: str, 
               traits: List[str], gender: str = "男") -> Dict:
        prompt = f"""为一个网络小说角色创建详细档案：
角色名：{name}
定位：{role}
类型：{archetype}
性别：{gender}
性格特点：{','.join(traits)}

输出JSON格式，包含：外貌描写、性格分析、背景故事、核心动机、说话风格、成长弧线"""
        return self.core.generate(prompt)
    
    def generate_dialogue(self, character: Dict, context: str, emotion: str) -> str:
        prompt = f"""根据角色设定和情境生成对话：
角色档案：{character}
情境：{context}
情绪：{emotion}

要求：对话自然，符合角色性格和说话风格"""
        return self.core.generate(prompt).get("text", "")
