from typing import List, Dict, Tuple
import numpy as np
from ..coordinate.coordinate_system import Coordinate, CoordinateSystem

class TrajectoryAnalysis:
    def __init__(self, coordinate_system: CoordinateSystem):
        self.coordinate_system = coordinate_system
    
    def get_basic_stats(self) -> Dict:
        """获取基本统计信息"""
        trajectory = self.coordinate_system.get_trajectory()
        if not trajectory:
            return {
                'total_points': 0,
                'total_distance': 0,
                'average_step_size': 0,
                'direction_changes': 0
            }
        
        # 计算总距离和平均步长
        total_distance = 0
        step_sizes = []
        direction_changes = 0
        prev_direction = None
        
        for i in range(1, len(trajectory)):
            # 计算两点之间的距离
            dx = trajectory[i].x - trajectory[i-1].x
            dy = trajectory[i].y - trajectory[i-1].y
            distance = np.sqrt(dx*dx + dy*dy)
            
            total_distance += distance
            step_sizes.append(distance)
            
            # 计算方向变化
            if i > 1:
                prev_dx = trajectory[i-1].x - trajectory[i-2].x
                prev_dy = trajectory[i-1].y - trajectory[i-2].y
                current_direction = np.arctan2(dy, dx)
                prev_direction = np.arctan2(prev_dy, prev_dx)
                
                # 如果方向变化超过45度，计为一次方向改变
                angle_diff = abs(current_direction - prev_direction)
                if angle_diff > np.pi/4:  # 45度
                    direction_changes += 1
        
        return {
            'total_points': len(trajectory),
            'total_distance': round(total_distance, 2),
            'average_step_size': round(np.mean(step_sizes), 2) if step_sizes else 0,
            'direction_changes': direction_changes
        }
    
    def get_movement_patterns(self) -> Dict:
        """分析移动模式"""
        trajectory = self.coordinate_system.get_trajectory()
        if len(trajectory) < 3:
            return {
                'primary_direction': 'insufficient_data',
                'movement_type': 'insufficient_data',
                'area_coverage': 0
            }
        
        # 计算主要移动方向
        dx = trajectory[-1].x - trajectory[0].x
        dy = trajectory[-1].y - trajectory[0].y
        angle = np.arctan2(dy, dx) * 180 / np.pi
        
        # 确定主要方向
        directions = ['东', '东北', '北', '西北', '西', '西南', '南', '东南']
        index = int((angle + 22.5) % 360 / 45)
        primary_direction = directions[index]
        
        # 分析移动类型
        distances = []
        for i in range(1, len(trajectory)):
            dx = trajectory[i].x - trajectory[i-1].x
            dy = trajectory[i].y - trajectory[i-1].y
            distances.append(np.sqrt(dx*dx + dy*dy))
        
        std_dev = np.std(distances)
        if std_dev < 0.5:
            movement_type = '均匀移动'
        elif std_dev < 1.0:
            movement_type = '适度变化'
        else:
            movement_type = '剧烈变化'
        
        # 计算覆盖区域（简单凸包面积估计）
        x_coords = [p.x for p in trajectory]
        y_coords = [p.y for p in trajectory]
        area_coverage = (max(x_coords) - min(x_coords)) * (max(y_coords) - min(y_coords))
        
        return {
            'primary_direction': primary_direction,
            'movement_type': movement_type,
            'area_coverage': round(area_coverage, 2)
        }
    
    def predict_tendency(self) -> Dict:
        """预测移动倾向"""
        trajectory = self.coordinate_system.get_trajectory()
        if len(trajectory) < 5:
            return {
                'tendency': 'insufficient_data',
                'confidence': 0
            }
        
        # 获取最后几个点的移动方向
        last_points = trajectory[-5:]
        directions = []
        for i in range(1, len(last_points)):
            dx = last_points[i].x - last_points[i-1].x
            dy = last_points[i].y - last_points[i-1].y
            directions.append(np.arctan2(dy, dx))
        
        # 计算方向的一致性
        direction_std = np.std(directions)
        if direction_std < 0.3:  # 方向比较一致
            confidence = 0.8
            tendency = '保持当前方向'
        elif direction_std < 0.6:
            confidence = 0.5
            tendency = '可能改变方向'
        else:
            confidence = 0.3
            tendency = '方向不确定'
        
        return {
            'tendency': tendency,
            'confidence': confidence
        } 