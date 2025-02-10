from dataclasses import dataclass
from typing import List, Tuple
import numpy as np
import json
from datetime import datetime
from modules.services.ai_service import AIService

@dataclass
class Coordinate:
    x: float
    y: float
    timestamp: str = None
    thought_process: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'timestamp': self.timestamp,
            'thought_process': self.thought_process
        }

class CoordinateSystem:
    def __init__(self):
        self.trajectory: List[Coordinate] = []
        self.ai_service = AIService()
        
    def get_range(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """获取当前轨迹的坐标范围，如果没有轨迹则返回默认范围"""
        if not self.trajectory:
            return ((-50, 50), (-50, 50))
        
        x_coords = [p.x for p in self.trajectory]
        y_coords = [p.y for p in self.trajectory]
        
        # 计算实际范围
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        # 添加边距
        margin = 10
        x_range = (x_min - margin, x_max + margin)
        y_range = (y_min - margin, y_max + margin)
        
        # 确保范围至少是 100x100
        if x_range[1] - x_range[0] < 100:
            center = sum(x_range) / 2
            x_range = (center - 50, center + 50)
        if y_range[1] - y_range[0] < 100:
            center = sum(y_range) / 2
            y_range = (center - 50, center + 50)
            
        return (x_range, y_range)
        
    def add_point(self, x: float, y: float, thought_process: str = None) -> Coordinate:
        """添加一个新的坐标点到轨迹中"""
        coord = Coordinate(x, y, thought_process=thought_process)
        self.trajectory.append(coord)
        return coord
    
    def get_trajectory(self) -> List[Coordinate]:
        """获取完整轨迹"""
        return self.trajectory
    
    def get_last_n_points(self, n: int) -> List[Coordinate]:
        """获取最后 n 个坐标点"""
        return self.trajectory[-n:] if n > 0 else []
    
    def predict_next_point(self, thought_container=None) -> Tuple[float, float, str]:
        """使用 AI 预测下一个坐标点"""
        if not self.trajectory:
            # 如果是第一个点，随机生成一个起始点
            return (np.random.uniform(-10, 10), np.random.uniform(-10, 10), "随机生成初始点")
        
        try:
            # 准备轨迹信息
            trajectory_info = self._format_trajectory_info()
            # 使用 AI 服务预测下一个点
            return self.ai_service.predict_movement(trajectory_info, thought_container)
        except Exception as e:
            print(f"AI 预测失败: {e}")
            # 如果 AI 预测失败，使用简单的规则
            return self._fallback_prediction()
    
    def _format_trajectory_info(self) -> str:
        """格式化轨迹信息"""
        if not self.trajectory:
            return "当前没有轨迹点"
        
        last_points = self.get_last_n_points(5)  # 获取最后5个点
        points_info = []
        
        for i, point in enumerate(last_points):
            points_info.append(f"点{i+1}: ({point.x:.2f}, {point.y:.2f})")
        
        current = self.trajectory[-1]
        total_points = len(self.trajectory)
        
        return f"""总点数: {total_points}
当前位置: ({current.x:.2f}, {current.y:.2f})
最近的轨迹点:
{chr(10).join(points_info)}"""
    
    def _fallback_prediction(self) -> Tuple[float, float, str]:
        """简单的规则预测（作为 AI 预测失败的后备方案）"""
        if len(self.trajectory) < 2:
            x = np.random.uniform(-10, 10)
            y = np.random.uniform(-10, 10)
            return x, y, "随机生成初始点"
        
        last_points = self.get_last_n_points(2)
        dx = last_points[1].x - last_points[0].x
        dy = last_points[1].y - last_points[0].y
        
        noise = np.random.normal(0, 2, 2)
        new_x = last_points[1].x + dx + noise[0]
        new_y = last_points[1].y + dy + noise[1]
        
        return new_x, new_y, "使用简单规则预测（AI 决策失败的后备方案）"
    
    def save_trajectory(self, filepath: str):
        """保存轨迹到文件"""
        with open(filepath, 'w') as f:
            json.dump([coord.to_dict() for coord in self.trajectory], f, indent=2)
    
    def load_trajectory(self, filepath: str):
        """从文件加载轨迹"""
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.trajectory = [
                Coordinate(
                    x=point['x'],
                    y=point['y'],
                    timestamp=point['timestamp'],
                    thought_process=point.get('thought_process')
                ) for point in data
            ] 