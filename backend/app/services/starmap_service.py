from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.plan import Plan
from app.schemas.starmap import StarMapResponse, StarNode, StarEdge
from app.ai.mock_data import generate_mock_starmap_data


async def get_starmap_data(db: AsyncSession, user_id: str):
    result = await db.execute(select(Plan).where(Plan.user_id == user_id))
    plans = result.scalars().all()
    
    nodes = []
    edges = []
    node_id_map = {}
    node_counter = 0
    
    color_map = {
        "short_term": "#a8edea",
        "mid_term": "#667eea",
        "long_term": "#fed6e3",
        "skill": "#a8edea",
        "career": "#667eea",
        "income": "#fed6e3"
    }
    
    for plan in plans:
        for milestone in plan.milestones:
            node_id = f"{plan.plan_type}_{milestone.get('id', f'm{node_counter}')}"
            node_counter += 1
            
            category = milestone.get("category", plan.plan_type)
            color = color_map.get(category, "#ffffff")
            
            node = StarNode(
                id=node_id,
                title=milestone.get("title", ""),
                category=category,
                probability=milestone.get("probability", 0.5),
                x=milestone.get("position", {}).get("x", 50),
                y=milestone.get("position", {}).get("y", 50),
                size=8 + milestone.get("probability", 0.5) * 12,
                color=color
            )
            nodes.append(node)
            node_id_map[milestone.get("id", "")] = node_id
        
        if plan.recommended_path:
            path_ids = plan.recommended_path.get("milestone_ids", [])
            for i in range(len(path_ids) - 1):
                source = node_id_map.get(path_ids[i])
                target = node_id_map.get(path_ids[i+1])
                if source and target:
                    edges.append(StarEdge(source=source, target=target, path_type="main"))
        
        for alt_path in plan.alternative_paths:
            path_ids = alt_path.get("milestone_ids", [])
            for i in range(len(path_ids) - 1):
                source = node_id_map.get(path_ids[i])
                target = node_id_map.get(path_ids[i+1])
                if source and target:
                    edges.append(StarEdge(source=source, target=target, path_type="alternative"))
    
    if not nodes:
        mock_data = generate_mock_starmap_data()
        nodes = [StarNode(**n) for n in mock_data["nodes"]]
        edges = [StarEdge(**e) for e in mock_data["edges"]]
    
    return StarMapResponse(nodes=nodes, edges=edges)
