# Lobster Architect Skill

## 📱 Multi-Platform UI Adaptation

**检测环境规则：**
- 飞书/桌面 (UI_High) → 生产力工具 → **标准 Markdown 表格**（保留完整格式）
- 微信/手机 (UI_Lite) → 轻量社交 → **极简名片协议**（Emoji + 标题 + 内容）

**视觉统一要求：**
- 保留 4A 审美
- 多用留白
- 中英双语标签

---

## 🎯 Agent Identity Card Format

### UI_High（飞书/桌面）

| 字段 | 说明 | 示例 |
| :--- | :--- |
| **🏷️ 身份名称** | 分身的正式称谓 | 内容总监 |
| **🎭 灵魂 (Soul)** | 三观、性格、语气风格 | 犀利·4A 审美、逻辑严密 |
| **📍 标识 (ID)** | 切换身份的唤醒词 | #导演 / #Content Director |
| **🛠️ 专属技能** | 该分身擅长的工 | 小红书爆款拆解、播客翻译 |

### UI_Lite（微信/手机）

🏷️ **身份名称** | 内容总监

---

🎭 **Soul Profile**

犀利·4A 审美·逻辑严密

---

📍 **Trigger ID**

#导演 / #Content Director

---

🛠️ **Expertise**

小红书爆款拆解·播客翻译

---

## 🔧 Implementation Rules

**微信环境（UI_Lite）强制规则：**
- ✅ 强制：Emoji + 标题 + 内容块
- ✅ 强制：零装饰线
- ✅ 强制：极简协议
- ✅ 强制：中英对照

**兼容性要求：**
- 标准表格格式（飞书）
- 极简名片格式（微信）
- 双端自适应

---

## 📋 Usage

```bash
# 检测环境
which openclaw 2>/dev/null && echo "UI_High" || echo "UI_Lite"

# 根据环境选择格式
# UI_High → 标准 Markdown 表格
# UI_Lite → 极简名片协议
```
