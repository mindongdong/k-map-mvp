from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter()

@router.get("/{chart_type}")
async def get_visualization(chart_type: str) -> Dict[str, Any]:
    """시각화 데이터 조회"""
    if chart_type not in ["umap", "heatmap", "boxplot"]:
        raise HTTPException(status_code=404, detail="Chart type not found")
    
    # 여기에서 각 차트 타입에 맞는 데이터를 생성하거나 조회하는 로직이 필요합니다.
    # 현재는 임시 목업 데이터를 반환합니다.
    mock_data = {
        "umap": {"x": [1, 2, 3], "y": [4, 5, 6], "labels": ["Cell A", "Cell B", "Cell C"]},
        "heatmap": {"z": [[1, 20, 30], [20, 1, 60], [30, 60, 1]]},
        "boxplot": {"y": [1, 2, 2, 3, 3, 3, 4, 4, 5]},
    }
    
    return {
        "chart_type": chart_type,
        "data": mock_data[chart_type],
        "layout": {"title": f"{chart_type.capitalize()} Plot"}
    }
