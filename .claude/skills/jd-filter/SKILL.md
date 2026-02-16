---
name: jd-filter
description: JD（职位描述）筛选与分析工具。当用户说「帮我看这个JD」「分析这个职位」「这个工作怎么样」或直接粘贴职位描述时使用此技能。功能包括：(1) 根据用户预设的 filter 判断 JD 是否符合要求，(2) 输出 location、job scope、requirements 的简要 summary，(3) 保存和更新用户的筛选条件。当用户说「设置/更新我的filter」「我的要求是...」时也使用此技能来更新筛选条件。
---

# JD Filter 职位筛选工具

根据用户预设的筛选条件，快速判断 JD 是否符合要求，并输出结构化摘要。

## 工作流程

### 1. 每次对话开始时检查 Filter

**首次使用或用户明确要求时：**
- 读取 `user_filter.json` 获取用户的筛选条件
- 如果 filter 尚未设置，提示用户先设置筛选条件

**日常使用：**
- 分析 JD 前，自动读取 `user_filter.json`
- 无需每次都向用户确认，直接应用已保存的条件

### 2. 自动检测并更新 Filter

**触发条件：**
当用户在对话中提到新的筛选要求时，自动更新筛选条件。触发关键词包括：
- 「我的要求是...」「我希望...」「我不想...」
- 「帮我筛选...」「只看...」「排除...」
- 「薪资要...」「地点必须...」「不能有...」
- 「更新我的filter」「修改筛选条件」「储存我的筛选条件」

**更新流程：**
1. 读取当前的 `user_filter.json`
2. 解析用户新提出的要求
3. 合并到现有 filter 中（新要求优先）
4. 更新 `user_filter.json` 文件
5. **打包技能为 .skill 文件并发送给用户**
   - 使用打包脚本：`python /mnt/skills/examples/skill-creator/scripts/package_skill.py /home/claude/jd-filter /mnt/user-data/outputs`
   - 简洁确认：「✅ 筛选条件已更新并已保存」
6. **然后继续处理 JD 筛选**（如果用户同时提供了 JD）

**Filter 常见类别：**
- **location**: 地点要求（must_include, must_exclude）
- **requirements**: 硬性要求（certifications, student_status, experience等）
- **application_philosophy**: 申请策略（approach, threshold, avoid列表）
- **user_background**: 用户背景（education, skills, projects）
- **ideal_positions**: 理想岗位类型列表
- **salary_range**: 薪资范围
- **work_authorization**: 签证/工作许可要求
- **company_preferences**: 公司偏好（规模、行业、排除名单）

**示例：**
用户说：「我不想申请薪资低于$25/小时的岗位」
→ 自动更新 `user_filter.json` 中的 `salary_range.minimum` 为 25
→ 打包整个技能为 .skill 文件并发送给用户
→ 回复：「✅ 筛选条件已更新并已保存：最低薪资要求 $25/小时」
→ 如果用户同时提供了 JD，继续进行筛选分析

### 3. 分析 JD

当用户粘贴 JD 时，按以下步骤处理：

#### Step 1: 提取关键信息
从 JD 中提取：
- Location（地点、remote policy）
- Job Scope（核心职责，2-3 句话概括）
- Requirements（必须条件 vs 加分项，学历、经验、技能）
- Visa/Sponsorship 信息（如有提及）
- 其他与 filter 相关的信息

#### Step 2: 对比 Filter
将提取的信息与用户的 filter 逐条对比。

#### Step 3: 输出结果

**输出格式（REJECT 时）：**

```
## 🔴 REJECT

**拒绝理由：**
- [核心原因1：领域不匹配/技能浪费/职业倒退等]
- [核心原因2（如有）]

**📍 Location:** [地点] (✅/❌)
**💼 Job Scope:** [1-2句话核心职责]
**📋 Requirements:** [3-5个关键要求，用逗号分隔]
```

**输出格式（PASS 时）：**

```
## 🟢 PASS

**📍 Location:** [地点] (✅)
**💼 Job Scope:** [1-2句话核心职责]
**📋 Requirements:** [3-5个关键要求，用逗号分隔]

**匹配度：** [为什么适合，1-2句话]
**申请建议：** [Cover letter要点，1句话]
```

## 筛选哲学

用户的筛选策略：
- **Threshold**: `minimum_requirements_met` - 能达到最低申请要求就申请
- **不要过度筛选**: 如果用户满足 minimum qualifications，就应该 PASS
- **避免主观判断**: 不要对职位"含金量"、"是否真正的数据分析"等进行主观评判
- **举例**: 如果 JD 要求"Bachelor's in Statistics, SQL, Excel"，而用户有 Statistics 硕士、会 SQL 和 Excel，即使职位主要是 reporting 而不是 advanced analytics，也应该 PASS

**常见过度筛选错误：**
- ❌ "这个岗位看起来更像 reporting 而不是真正的数据分析" → 只要用户满足要求就 PASS
- ❌ "虽然符合要求但职位含金量不高" → 不是我们判断的范畴
- ❌ "这个岗位技术栈不够前沿" → 只看是否符合 filter，不评判职位价值

## 注意事项

- 判断要基于 JD 明确写出的信息，不要推测
- 如果 JD 没有提及某个 filter 相关信息（如未说明是否 sponsor），标注为「未提及」
- Summary 要简洁，每个部分控制在 2-3 行内
- 用中文输出，但保留 JD 中的专有名词（如职位名、公司名、技术栈）
