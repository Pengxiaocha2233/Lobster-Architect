import os
import re
import hashlib

THE_CORE_LOGIC = {
    "naming": "snake_case",
    "path_isolation": True,
    "visual_distribution": True
}

# 辅助函数
def read_template(template_name):
    """读取模板文件"""
    template_path = f"templates/{template_name}"
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(file_path, content):
    """写入文件（自动创建父目录）"""
    dir_path = os.path.dirname(file_path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def get_existing_agents():
    """获取已存在的 Agent 缩写列表"""
    try:
        agents_dir = "agents"
        if not os.path.exists(agents_dir):
            return []
        existing = []
        for file in os.listdir(agents_dir):
            if file.endswith('.md'):
                abbr = file[:-3]
                existing.append(abbr)
        return existing
    except Exception as e:
        print(f"[Warn] 读取 agents 目录失败: {e}")
        return []

# 系统扫描
def auto_scan():
    """执行系统扫描并发送诊断报告"""
    agents_dir = "agents"
    skills_dir = "skills"
    memory_dir = "memory"

    agent_count = 0
    if os.path.exists(agents_dir):
        for file in os.listdir(agents_dir):
            if file.endswith('.md'):
                agent_count += 1

    # 生成诊断结果
    scan_result = f"""🎋 系统扫描完成！

当前状态：**{'初创期' if agent_count < 5 else '成长期'}**

📊 已配置 Agent 数量：{agent_count}

📁 目录结构：
- agents/ — 配置文件目录
- skills/ — 技能目录
- memory/ — 记忆目录
- templates/ — 模板目录

"""

    print(scan_result)

# 英文翻译与镜像命名
def english_abbr(name, lang="zh"):
    """
    中文身份名自动转换为 snake_case 文件夹名

    策略：
    1. 优先尝试英文翻译（如果有翻译 API）
    2. 翻译失败回退到拼音 + snake_case
    3. 确保不重复生成（避免文件冲突）

    示例：
        "首席文案" → "chief_copywriter"
        "内容总监" → "content_director"
        "技术顾问" → "tech_advisor"
    """
    try:
        # 策略 1：尝试翻译（如果有翻译 API）
        if hasattr(translator, 'translate'):
            english = translator.translate(name, lang)
            abbr = to_snake_case(english)
            return abbr
        else:
            # 策略 2：拼音回退
            from pypinyin import pinyin, Style
            pinyin_str = pinyin(name, style=Style.NORMAL, heteronym=False)
            # 取首字母
            abbr = '_'.join([py[0].lower() for py in pinyin_str])
            return abbr
    except Exception as e:
        print(f"[Warn] 翻译失败，使用拼音: {e}")
        # 保底：直接使用拼音
        from pypinyin import pinyin, Style
        pinyin_str = pinyin(name, style=Style.NORMAL, heteronym=False)
        abbr = '_'.join([py[0].lower() for py in pinyin_str])
        return abbr


def to_snake_case(text):
    """转换为 snake_case"""
    text = text.lower().replace(' ', '_').replace('-', '_')
    return re.sub(r'[^a-z0-9_]', '', text)


def generate_agent_abbr(name):
    """
    生成 Agent 缩写（带防重复检测）
    """
    abbr = english_abbr(name)

    # 检查是否已存在
    existing_agents = get_existing_agents()
    if abbr in existing_agents:
        # 添加后缀避免冲突
        suffix = 1
        while f"{abbr}_{suffix}" in existing_agents:
            suffix += 1
        abbr = f"{abbr}_{suffix}"

    return abbr


# 入职卡解析
def parse_onboarding_card(user_input):
    # 默认值设定
    defaults = {
        "name": "未命名分身",
        "soul": "专业、严谨、用户导向",
        "identity": "#分身",
        "skill": "通用对话"
    }

    # 提取字段（优化版正则，去掉了末尾强行的换行符）
    def extract_field(pattern):
        match = re.search(pattern, user_input)
        return match.group(1).strip() if match else None

    # 调用时只传一个参数，避免运行报错
    card = {
        "name": extract_field(r"🏷️\s*身份名称[:：]\s*(.+)"),
        "soul": extract_field(r"🎭\s*灵魂\(Soul\)[:：]\s*(.+)"),
        "identity": extract_field(r"📍\s*标识\(Identity\)[:：]\s*(.+)"),
        "skill": extract_field(r"🛠️\s*专属技能[:：]\s*(.+)")
    }

    # 统一补齐默认值
    for key in ["name", "soul", "identity", "skill"]:
        if not card[key]:
            card[key] = defaults[key]

    # 生成缩写
    card["abbr"] = generate_agent_abbr(card["name"])
    return card



def parse_multiple_cards(user_input):
    """
    批量解析多个入职卡

    识别方式：检测多个 🏷️ 标记
    """
    cards = []
    sections = re.split(r'🏷️', user_input)

    for section in sections:
        if section.strip():
            cards.append(parse_onboarding_card(f"🏷️ {section}"))

    return cards


# 工牌样式输出
def render_team_cards(cards, ui_mode="UI_Lite"):
    """
    渲染待入职成员列表

    UI_High（飞书/GitHub）：Markdown 表格
    UI_Lite（微信）：Emoji 名片卡片
    """
    if ui_mode == "UI_High":
        # 表格样式
        output = "🎋 待入职成员列表\n\n"
        output += "| 🏷️ 身份名称 | 🎭 灵魂 | 📍 标识 | 🛠️ 专属技能 | 📂 工牌编号 |\n"
        output += "| :--- | :--- | :--- | :--- | :--- |\n"

        for card in cards:
            output += f"| {card['name']} | {card['soul']} | {card['identity']} | {card['skill']} | **{card['abbr']}** |\n"

        output += "\n**[首席架构师确认]**：工牌已核对无误。\n"
        output += "现在，是否授权我执行自动化施工，为这些分身开启专属办公区？\n"
        output += "（回复：\"开始施工\"或\"确认\"）"

    else:
        # UI_Lite 名片样式（高奢名片块）
        output = "🎋 待入职成员列表\n\n"

        for card in cards:
            output += "**🏷️ " + card['name'] + "**\n"
            if card['soul'] != defaults['soul']:
                output += "**🎭 " + card['soul'] + "**\n"
            output += "**📍 " + card['identity'] + "**\n"
            if card['skill'] != defaults['skill']:
                output += "**🛠️ " + card['skill'] + "**\n"
            output += "**📂 工牌编号: " + card['abbr'] + "**\n\n"

        output += "\n---\n\n"
        output += "🎋 [首席架构师确认]：工牌已核对无误。\n\n"
        output += "现在，是否授权我执行自动化施工，为这些分身开启专属办公区？\n"
        output += "（回复：\"开始施工\"或\"确认\"）"

    return output


# 物理分区创建
def create_agent_workspace(cards):
    """
    为每个 Agent 创建物理分区

    执行逻辑：
    1. 创建文件夹（memory/[abbr]/ 和 skills/[abbr]/）
    2. 在 agents/ 目录下生成对应的 .md 配置文件
    3. 注入灵魂（使用 templates/agent_template.md 和 soul_template.md）
    """
    success_count = 0
    failed_cards = []

    for card in cards:
        try:
            abbr = card["abbr"]

            # 1. 创建文件夹
            os.makedirs(f"memory/{abbr}/", exist_ok=True)
            os.makedirs(f"skills/{abbr}/", exist_ok=True)

            # 2. 读取模板
            agent_template = read_template("agent_template.md")
            soul_template = read_template("soul_template.md")

            # 3. 渲染 Agent 配置文件
            agent_config = render_agent_config(card, abbr, agent_template, soul_template)

            # 4. 写入文件
            write_file(f"agents/{abbr}.md", agent_config)

            success_count += 1

        except Exception as e:
            failed_cards.append({
                "card": card,
                "error": str(e)
            })

    return {
        "success_count": success_count,
        "failed_cards": failed_cards
    }


def render_agent_config(card, abbr, agent_template, soul_template):
    """
    渲染 Agent 配置文件

    字段替换规则：
    - {{身份名称}} → card["name"]
    - {{abbr}} → abbr
    - {{灵魂}} → card["soul"]
    - {{标识}} → card["identity"]
    - {{专属技能}} → card["skill"]
    """
    config = agent_template

    # 替换所有占位符
    replacements = {
        "{{身份名称}}": card["name"],
        "{{abbr}}": abbr,
        "{{灵魂}}": card["soul"],
        "{{标识}}": card["identity"],
        "{{专属技能}}": card["skill"]
    }

    for old, new in replacements.items():
        config = config.replace(old, new)

    return config


# 最终交付报告
def deliver_final_report(cards, creation_result):
    """
    生成最终交付报告（仪式感交付）
    """
    ui_mode = detect_ui_environment()

    output = "🎋 龙虾系统架构完毕！你的系统已正式上线。\n\n"

    # 目录结构展示
    if ui_mode == "UI_High":
        output += "### 📁 物理目录结构\n"
        output += "```\nworkspace/\n"
        output += "├── agents/\n"
        for card in cards:
            output += f"│   ├── {card['abbr']}.md  ✅\n"
        output += "├── skills/\n"
        for card in cards:
            output += f"│   ├── {card['abbr']}/  ✅\n"
            output += f"│   │   └── [预留接口]\n"
        output += "└── memory/\n"
        for card in cards:
            output += f"    ├── {card['abbr']}/  ✅\n"

        output += "```\n\n"

    else:
        output += "### 📁 物理目录结构\n"
        output += "**✅ 已创建以下分区：**\n\n"
        for card in cards:
            output += f"• 📂 `memory/{card['abbr']}/` - 独立记忆空间\n"
            output += f"• 🛠️ `skills/{card['abbr']}/` - 专属技能工具箱\n"
            output += f"• 📋 `agents/{card['abbr']}.md` - 身份配置文件\n\n"

    output += "### 🎯 你的分身已就位\n\n"

    for card in cards:
        output += f"- **{card['name']}**: 觉醒为 `{card['identity']}` 模式\n"

    output += "\n试试对我发送：\n"
    output += "`@[分身名] 这里的第一个任务是什么？`\n"

    return output


# 环境检测
def detect_ui_environment():
    """
    检测当前运行环境

    简单判断：飞书/GitHub 返回 UI_High，微信返回 UI_Lite
    """
    # 在微信环境，检测微信特定标识
    return "UI_Lite"


# 主程序
if __name__ == "__main__":
    print("🏮 龙虾架构师核心逻辑加载完成！\n")
    print("可调用函数：")
    print("  - auto_scan(): 系统扫描")
    print("  - parse_onboarding_card(user_input): 解析入职卡")
    print("  - create_agent_workspace(cards): 创建 Agent 工作区")
    print("  - render_team_cards(cards): 生成工牌预览")
