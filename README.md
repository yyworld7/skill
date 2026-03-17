# AI Novel Writing Skill

一个利用最新 AI 技术辅助创作网络小说的完整解决方案。

## 核心功能

- **故事大纲生成** - 基于关键词/类型生成结构化故事大纲
- **角色设计** - 创建立体的角色档案（外貌、性格、背景、动机）
- **情节编排** - 生成起承转合的章节安排和情节节点
- **对话生成** - 为不同角色生成符合人设的对话
- **文风模仿** - 学习和模仿特定作者的写作风格
- **多版本生成** - 同一场景生成多个版本供选择
- **内容扩展** - 将简短的描述扩展成完整的章节

## 快速开始

```bash
pip install -r requirements.txt
```

```python
from novel_ai import NovelAI

ai = NovelAI(api_key="xxx", base_url="http://localhost:9875/v1", model="moltboter")
outline = ai.generate_outline(genre="玄幻", keywords="废材逆袭", length="长篇")
```

## 许可证

MIT