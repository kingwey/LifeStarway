PLANNING_PROMPT = """
你是一位资深职业规划师，请根据用户档案和诊断结果，生成{plan_type}职业规划。

## 用户档案
{profile_data}

## 诊断结果
{diagnosis_data}

## 规划要求
- {plan_type}：{plan_type_desc}
- 提供 3-5 个关键里程碑
- 每个里程碑包含：目标、达成时间、所需行动、预期成果
- 提供一条推荐主路径和 2 条备选路径
- 每个里程碑给出达成概率（0-1）
- 每个里程碑包含星图位置信息（x和y，范围0-100）

## 输出格式（严格 JSON）
{{
  "title": "{plan_type}职业规划",
  "description": "规划概述...",
  "milestones": [
    {{
      "id": "m1",
      "title": "里程碑1标题",
      "target_date": "YYYY-MM",
      "category": "skill/career/income",
      "metrics": {{"target_role": "目标职位", "target_salary": "目标薪资"}},
      "probability": 0.85,
      "position": {{"x": 20, "y": 70}}
    }}
  ],
  "recommended_path": {{
    "name": "推荐路径名称",
    "description": "路径描述",
    "milestone_ids": ["m1", "m2", "m3"]
  }},
  "alternative_paths": [
    {{
      "name": "备选路径1",
      "description": "路径描述",
      "milestone_ids": ["m1", "m2", "m4"]
    }},
    {{
      "name": "备选路径2",
      "description": "路径描述",
      "milestone_ids": ["m1", "m3", "m5"]
    }}
  ]
}}
"""

PLAN_TYPE_DESCS = {
    "short_term": "1年短期规划，聚焦当前技能提升和近期目标达成",
    "mid_term": "3年中期规划，关注职业晋升和能力跃迁",
    "long_term": "5-10年长期规划，探索人生愿景和长期价值实现"
}
