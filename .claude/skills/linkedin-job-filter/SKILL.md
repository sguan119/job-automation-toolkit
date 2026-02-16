---
name: linkedin-job-filter
description: LinkedIn 职位自动筛选工具。使用 agent-browser (--headed) 打开 LinkedIn 职位搜索页面，逐个点击职位查看完整 JD，调用 jd-filter 进行筛选，对不符合条件的职位点击 dismiss (X) 按钮。触发词包括 "筛选LinkedIn职位"、"filter LinkedIn jobs"、"linkedin job filter"，或用户提供 LinkedIn Jobs 搜索 URL。
allowed-tools: Bash(agent-browser:*), Skill(jd-filter)
---

# LinkedIn Job Filter Skill

在 LinkedIn 职位搜索结果页面上，逐个查看职位详情，使用 jd-filter 筛选，自动 dismiss 不合格的职位。

## 适用场景

- 用户提供 LinkedIn Jobs 搜索结果 URL（如 `https://www.linkedin.com/jobs/search/...`）
- 用户说「帮我筛选 LinkedIn 上的职位」「filter LinkedIn jobs」
- 用户已经在 LinkedIn 上搜索好了职位，想要批量筛选

## 前置条件

- `agent-browser` 已安装并在 PATH 中
- 用户已登录 LinkedIn（需要 agent-browser state 或手动登录）
- `jd-filter` skill 的 `user_filter.json` 已配置

## 限制

- **不支持翻页** - 仅处理当前页面可见的职位列表
- 需要用户已登录 LinkedIn（若未登录，提示用户手动登录后继续）

## 工作流程

### Step 0: 加载筛选条件

读取 jd-filter 的筛选条件：
```
.claude/skills/jd-filter/user_filter.json
```
如果不存在，提示用户先设置筛选条件（使用 jd-filter skill）。

### Step 1: 打开 LinkedIn 页面

```bash
agent-browser open "<linkedin-jobs-url>" --headed
agent-browser wait --load networkidle
agent-browser wait 3000
```

**重要：** 必须使用 `--headed`，用户需要看到浏览器窗口。

### Step 2: 检查登录状态

```bash
agent-browser snapshot -i
```

检查 snapshot 输出：
- 如果看到 "Sign in" / "Join now" 等按钮 → 提示用户手动登录
- 如果看到职位列表 → 继续下一步

如果需要登录：
1. 提示用户在浏览器中手动完成登录
2. 等待用户确认已登录
3. 重新导航到职位搜索 URL
4. 再次 snapshot 确认

### Step 3: 获取职位列表

```bash
agent-browser snapshot -i
```

从 snapshot 中识别所有职位卡片。LinkedIn 职位搜索结果通常包含：
- 职位标题链接（可点击）
- 公司名称
- 地点
- 发布时间
- dismiss 按钮（X 图标）

记录每个职位的：
- **title_ref**: 职位标题的 @ref（用于点击查看详情）
- **dismiss_ref**: X 按钮的 @ref（用于 dismiss 不合格的职位）
- **title_text**: 职位标题文字
- **company_text**: 公司名称

将所有职位信息保存到内存列表中，准备逐个处理。

### Step 4: 逐个处理职位

对列表中的每个职位，执行以下流程：

#### 4a: 点击职位查看详情

```bash
agent-browser click @title_ref
agent-browser wait --load networkidle
agent-browser wait 2000
```

点击后，LinkedIn 右侧面板会显示职位详情。

#### 4b: 提取 JD 文本

```bash
agent-browser snapshot -i
```

从 snapshot 中找到职位描述区域。LinkedIn JD 通常在以下位置：
- `jobs-description__content` 类下
- 或 `jobs-box__html-content` 类下

找到 JD 内容的 @ref 后：
```bash
agent-browser get text @jd_ref
```

同时提取：
- 职位标题
- 公司名称
- 地点
- 工作类型（Full-time, Contract 等）
- Remote/Hybrid/On-site

#### 4c: 调用 jd-filter 进行筛选

将提取的 JD 文本交给 jd-filter 进行评估。jd-filter 会返回：
- **PASS** - 职位符合用户要求
- **REJECT** - 职位不符合用户要求

#### 4d: 处理筛选结果

**如果 REJECT：**
1. 在当前 snapshot 中找到该职位的 dismiss (X) 按钮
2. 需要重新 snapshot 获取最新 refs：
   ```bash
   agent-browser snapshot -i
   ```
3. 找到 dismiss 按钮的 @ref（通常是一个小的 X 图标按钮，在职位卡片右上角）
4. 点击 dismiss：
   ```bash
   agent-browser click @dismiss_ref
   agent-browser wait 1000
   ```
5. 输出：`REJECT - [职位标题] @ [公司] - [拒绝理由]`

**如果 PASS：**
1. 不做任何操作，保留该职位
2. 输出：`PASS - [职位标题] @ [公司] - [匹配理由]`

#### 4e: 准备处理下一个职位

```bash
agent-browser snapshot -i
```

重新获取 snapshot，因为 dismiss 操作可能改变了页面结构和 refs。
找到下一个未处理的职位，重复 4a-4d。

### Step 5: 输出汇总报告

所有职位处理完毕后，输出汇总：

```
## LinkedIn 职位筛选报告

总计处理: X 个职位
- PASS: Y 个
- REJECT: Z 个

### PASS 的职位:
1. [职位标题] @ [公司] - [地点]
2. ...

### REJECT 的职位:
1. [职位标题] @ [公司] - [拒绝理由]
2. ...
```

### Step 6: 关闭浏览器

```bash
agent-browser close
```

## LinkedIn 页面结构参考

### 职位列表页面

典型的 LinkedIn 搜索结果页面结构：
- 左侧：职位卡片列表（可滚动）
- 右侧：选中职位的详细信息面板

### 常见元素

| 元素 | 描述 | 查找方式 |
|------|------|----------|
| 职位标题 | 可点击链接 | snapshot 中的 `<a>` 标签，文本为职位名 |
| 公司名称 | 文本 | 职位标题下方 |
| 地点 | 文本 | 公司名称下方 |
| Dismiss 按钮 | X 图标 | 职位卡片右上角的按钮，通常有 `dismiss` 相关属性 |
| JD 内容 | 详情面板 | 右侧面板中的主要文本区域 |
| "Show more" 按钮 | 展开完整 JD | JD 区域底部 |

### 展开完整 JD

LinkedIn 默认只显示部分 JD，需要点击 "Show more" / "See more" 展开：

```bash
# 在 JD 面板中找到 "Show more" 按钮
agent-browser snapshot -i
# 如果找到 "Show more" / "...more" / "See more" 按钮
agent-browser click @show_more_ref
agent-browser wait 1000
agent-browser snapshot -i
# 现在可以获取完整 JD
agent-browser get text @full_jd_ref
```

## 关键原则

1. **必须 --headed** - 用户需要看到浏览器
2. **每次操作后重新 snapshot** - LinkedIn 是 SPA，DOM 频繁变化
3. **处理速度适中** - 每个职位间等待 1-2 秒，避免被限流
4. **遇到异常不中断** - 如果某个职位提取失败，记录错误并继续下一个
5. **先 snapshot 再操作** - 永远不要使用过期的 @ref
6. **展开 JD** - 点击 "Show more" 获取完整职位描述再筛选
7. **dismiss 后重新定位** - dismiss 一个职位后，列表会变化，需要重新 snapshot
8. **不要关闭浏览器** - 处理完保持浏览器开启，用户可能需要继续操作

## 处理效率优化

### 高效处理策略
- **明显不相关的职位**: 对于零售、part-time、医疗等明显不符合的职位，可以直接从标题判断后dismiss，不需要点进去读完整JD
- **优先级**: 只有标题看起来有潜力的职位才需要完整读JD，节省时间

### Dismiss 后的行为
- Dismiss一个职位后，LinkedIn会自动显示新的职位填补空位
- **必须追踪新出现的职位** - 不要遗漏dismiss后出现的新职位
- 重新snapshot时检查列表，处理所有未处理的职位

## 错误处理

| 错误类型 | 处理方式 |
|----------|----------|
| 未登录 | 提示用户手动登录，等待确认 |
| 职位详情加载失败 | 等待 3 秒重试一次，仍失败则跳过 |
| JD 文本为空 | 尝试点击 "Show more"，仍为空则跳过 |
| Dismiss 按钮找不到 | 跳过 dismiss，标记为手动处理 |
| 页面限流/验证码 | 暂停，提示用户完成验证后继续 |
| Snapshot 超时 | 等待 5 秒后重试 |

## 使用示例

```
用户: 帮我筛选这个LinkedIn页面的职位 https://www.linkedin.com/jobs/search/?keywords=software%20engineer&location=Toronto

助手:
1. 打开 LinkedIn 页面（可见浏览器）
2. 检查登录状态
3. 获取页面上的 25 个职位
4. 逐个点击 → 提取 JD → jd-filter 筛选 → REJECT 的点 X
5. 输出汇总报告
```
