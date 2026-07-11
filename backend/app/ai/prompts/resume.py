RESUME_PARSE_PROMPT = """
你是一位专业的简历分析助手，请从简历文本中提取结构化的个人信息。

## 简历文本
{resume_text}

## 提取要求
- 学历：最高学历
- 专业：所学专业
- 学校：毕业院校
- 技能：技能名称、熟练程度、使用年限
- 工作经历：公司名称、职位、工作时间、薪资（如果有）
- 当前行业、当前职位、工作年限
- 薪资范围（如果能推断）

## 输出格式（严格 JSON）
{{
  "birth_year": null,
  "gender": null,
  "education": "学历",
  "major": "专业",
  "school": "院校",
  "skills": [
    {{"name": "技能名", "level": "熟练程度", "years": 0.0}}
  ],
  "personality_type": null,
  "current_industry": "行业",
  "current_role": "职位",
  "work_years": 0,
  "salary_range": null,
  "career_history": [
    {{"company": "公司", "role": "职位", "period": "时间", "salary": null}}
  ],
  "resume_text": "{resume_text}"
}}
"""
