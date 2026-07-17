import random
from datetime import datetime, timedelta


def generate_mock_diagnosis():
    health_score = random.randint(65, 95)
    return {
        "health_score": health_score,
        "dimensions": {
            "growth": random.randint(60, 95),
            "stability": random.randint(55, 90),
            "income_potential": random.randint(50, 95),
            "interest_match": random.randint(60, 100),
            "industry_outlook": random.randint(55, 95),
        },
        "strengths": [
            "技术能力扎实",
            "学习能力强",
            "沟通表达优秀",
            "目标导向明确",
        ],
        "risks": [
            "行业竞争激烈",
            "技能更新速度快",
            "职业瓶颈期",
        ],
        "summary": "综合评估显示您的职业健康状况良好。您具备扎实的技术基础和学习能力，是职业发展的核心优势。建议关注行业趋势变化，持续提升核心竞争力，同时注重工作与生活的平衡。",
    }


def generate_mock_plan(plan_type):
    titles = {
        "short_term": "1年技能突破计划",
        "mid_term": "3年晋升成长路径",
        "long_term": "5年职业愿景规划",
    }
    descriptions = {
        "short_term": "基于当前职业状况，制定1年内的技能提升和目标达成计划。重点关注核心技术栈的深度挖掘和项目经验积累。",
        "mid_term": "规划未来3年的职业发展路径，包括晋升策略、能力建设和关键决策点。帮助您实现从技术骨干到管理岗位或技术专家的转型。",
        "long_term": "描绘5-10年的职业蓝图，整合行业趋势、个人愿景和人生目标。为您的长期职业发展提供战略指引。",
    }
    
    now = datetime.now()
    milestones = []
    
    if plan_type == "short_term":
        for i in range(1, 5):
            months = i * 3
            milestones.append({
                "id": f"st_{i}",
                "title": ["掌握核心技术栈", "独立负责项目模块", "技术分享与影响力", "晋升初级管理岗"][i-1],
                "target_date": (now + timedelta(days=months*30)).strftime("%Y-%m"),
                "probability": min(0.95, 0.6 + i * 0.08),
                "category": "short_term",
                "metrics": {
                    "target_role": ["高级工程师", "技术组长", "技术专家", "技术经理"][i-1],
                },
            })
    elif plan_type == "mid_term":
        for i in range(1, 4):
            years = i
            milestones.append({
                "id": f"mt_{i}",
                "title": ["技术团队负责人", "跨部门协作突破", "业务架构设计"][i-1],
                "target_date": (now + timedelta(days=years*365)).strftime("%Y-%m"),
                "probability": min(0.9, 0.5 + i * 0.15),
                "category": "mid_term",
                "metrics": {
                    "target_role": ["技术经理", "高级技术经理", "技术总监"][i-1],
                },
            })
    else:
        for i in range(1, 4):
            years = i * 2 + 3
            milestones.append({
                "id": f"lt_{i}",
                "title": ["行业专家认证", "创业/合伙机会", "行业影响力建设"][i-1],
                "target_date": (now + timedelta(days=years*365)).strftime("%Y-%m"),
                "probability": min(0.85, 0.4 + i * 0.15),
                "category": "long_term",
                "metrics": {
                    "target_role": ["首席技术官", "创始人", "行业顾问"][i-1],
                },
            })
    
    return {
        "title": titles[plan_type],
        "description": descriptions[plan_type],
        "milestones": milestones,
        "recommended_path": {
            "name": "主路径：技术专家路线",
            "description": "深耕技术领域，成为行业技术专家，逐步向技术管理或架构师方向发展",
            "milestone_ids": [m["id"] for m in milestones],
        },
        "alternative_paths": [
            {
                "name": "管理路线",
                "description": "转型技术管理，负责团队建设和项目管理",
                "milestone_ids": [m["id"] for m in milestones],
            },
        ],
    }


def generate_mock_whatif(hypothesis):
    action = hypothesis.get("action", "")
    now = datetime.now()
    
    if action == "转行":
        target = hypothesis.get("target_industry", "AI行业")
        risk_level = "medium"
        simulated_milestones = [
            {
                "id": "sim_1",
                "title": f"学习{target}基础知识",
                "target_date": (now + timedelta(days=90)).strftime("%Y-%m"),
                "probability": 0.85,
            },
            {
                "id": "sim_2",
                "title": f"完成{target}项目实践",
                "target_date": (now + timedelta(days=180)).strftime("%Y-%m"),
                "probability": 0.75,
            },
            {
                "id": "sim_3",
                "title": f"成功转入{target}岗位",
                "target_date": (now + timedelta(days=365)).strftime("%Y-%m"),
                "probability": 0.65,
            },
        ]
        risks = ["技能差距较大", "行业经验不足", "薪资可能下降"]
        mitigation = ["系统学习目标领域知识", "参与开源项目积累经验", "寻找导师指导"]
    elif action == "读MBA":
        risk_level = "low"
        simulated_milestones = [
            {
                "id": "sim_1",
                "title": "备考MBA",
                "target_date": (now + timedelta(days=120)).strftime("%Y-%m"),
                "probability": 0.8,
            },
            {
                "id": "sim_2",
                "title": "入学学习",
                "target_date": (now + timedelta(days=365)).strftime("%Y-%m"),
                "probability": 0.95,
            },
            {
                "id": "sim_3",
                "title": "毕业并转型管理",
                "target_date": (now + timedelta(days=730)).strftime("%Y-%m"),
                "probability": 0.75,
            },
        ]
        risks = ["学费较高", "机会成本", "毕业后市场环境变化"]
        mitigation = ["申请奖学金", "提前规划职业目标", "保持行业联系"]
    elif action == "跳槽":
        target = hypothesis.get("target_industry", "大厂")
        risk_level = "medium"
        simulated_milestones = [
            {
                "id": "sim_1",
                "title": f"准备{target}面试",
                "target_date": (now + timedelta(days=60)).strftime("%Y-%m"),
                "probability": 0.85,
            },
            {
                "id": "sim_2",
                "title": f"拿到{target}offer",
                "target_date": (now + timedelta(days=90)).strftime("%Y-%m"),
                "probability": 0.65,
            },
            {
                "id": "sim_3",
                "title": "成功入职并适应",
                "target_date": (now + timedelta(days=180)).strftime("%Y-%m"),
                "probability": 0.8,
            },
        ]
        risks = ["面试失败风险", "企业文化不匹配", "薪资涨幅不及预期"]
        mitigation = ["充分准备面试", "深入了解目标公司", "多拿几个offer对比"]
    elif action == "创业":
        risk_level = "high"
        simulated_milestones = [
            {
                "id": "sim_1",
                "title": "验证商业模式",
                "target_date": (now + timedelta(days=90)).strftime("%Y-%m"),
                "probability": 0.7,
            },
            {
                "id": "sim_2",
                "title": "组建团队",
                "target_date": (now + timedelta(days=180)).strftime("%Y-%m"),
                "probability": 0.6,
            },
            {
                "id": "sim_3",
                "title": "获得首轮融资",
                "target_date": (now + timedelta(days=365)).strftime("%Y-%m"),
                "probability": 0.35,
            },
        ]
        risks = ["资金压力大", "团队不稳定", "市场竞争激烈"]
        mitigation = ["预留充足资金", "寻找互补合伙人", "快速迭代产品"]
    else:
        risk_level = "low"
        simulated_milestones = [
            {
                "id": "sim_1",
                "title": "深耕核心技术",
                "target_date": (now + timedelta(days=180)).strftime("%Y-%m"),
                "probability": 0.9,
            },
            {
                "id": "sim_2",
                "title": "成为技术骨干",
                "target_date": (now + timedelta(days=365)).strftime("%Y-%m"),
                "probability": 0.85,
            },
            {
                "id": "sim_3",
                "title": "获得晋升机会",
                "target_date": (now + timedelta(days=730)).strftime("%Y-%m"),
                "probability": 0.75,
            },
        ]
        risks = ["技术栈过时风险", "职业天花板"]
        mitigation = ["持续学习新技术", "拓展横向能力"]
    
    return {
        "simulated_milestones": simulated_milestones,
        "risk_assessment": {
            "risk_level": risk_level,
            "risks": risks,
            "mitigation": mitigation,
        },
        "comparison": {
            "original_path": "继续当前岗位稳步发展",
            "simulated_path": f"{action}后的发展路径",
            "key_differences": [
                f"{action}后初期可能面临较大挑战",
                f"{action}成功后职业发展空间更大",
                f"{action}需要投入更多时间和精力",
            ],
            "recommendation": "建议充分评估自身条件和外部环境，制定详细计划后再决策。",
        },
    }


def generate_mock_starmap_data():
    nodes = []
    edges = []
    
    node_counter = 0
    categories = ["短期目标", "中期目标", "长期目标", "技能节点", "职业节点"]
    
    for cat_idx, category in enumerate(categories):
        for i in range(3):
            node_id = f"node_{cat_idx}_{i}"
            x = 20 + cat_idx * 15 + i * 5
            y = 30 + i * 20
            size = 8 + random.random() * 10
            probability = 0.5 + random.random() * 0.4
            
            if category == "短期目标":
                color = "#a8edea"
            elif category == "中期目标":
                color = "#667eea"
            elif category == "长期目标":
                color = "#fed6e3"
            elif category == "技能节点":
                color = "#a8edea"
            else:
                color = "#667eea"
            
            titles = {
                "短期目标": ["掌握Python", "项目实战", "技术分享"],
                "中期目标": ["技术组长", "架构设计", "团队管理"],
                "长期目标": ["技术总监", "创业", "行业专家"],
                "技能节点": ["算法", "架构", "管理"],
                "职业节点": ["工程师", "经理", "创始人"],
            }
            
            nodes.append({
                "id": node_id,
                "title": titles[category][i],
                "category": category,
                "probability": probability,
                "x": x,
                "y": y,
                "size": size,
                "color": color,
                "metrics": {"target_role": titles[category][i]},
            })
    
    edges = [
        {"source": "node_0_0", "target": "node_0_1", "path_type": "main"},
        {"source": "node_0_1", "target": "node_0_2", "path_type": "main"},
        {"source": "node_0_2", "target": "node_1_0", "path_type": "main"},
        {"source": "node_1_0", "target": "node_1_1", "path_type": "main"},
        {"source": "node_1_1", "target": "node_1_2", "path_type": "main"},
        {"source": "node_1_2", "target": "node_2_0", "path_type": "main"},
        {"source": "node_2_0", "target": "node_2_1", "path_type": "alternative"},
        {"source": "node_2_0", "target": "node_2_2", "path_type": "alternative"},
        {"source": "node_3_0", "target": "node_0_0", "path_type": "alternative"},
        {"source": "node_3_1", "target": "node_1_1", "path_type": "alternative"},
        {"source": "node_3_2", "target": "node_2_0", "path_type": "alternative"},
        {"source": "node_4_0", "target": "node_0_2", "path_type": "alternative"},
        {"source": "node_4_1", "target": "node_1_2", "path_type": "alternative"},
        {"source": "node_4_2", "target": "node_2_1", "path_type": "alternative"},
    ]
    
    return {"nodes": nodes, "edges": edges}