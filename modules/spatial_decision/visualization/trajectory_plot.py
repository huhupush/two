import plotly.graph_objects as go
from typing import List, Tuple
import numpy as np
from ..coordinate.coordinate_system import Coordinate, CoordinateSystem

class TrajectoryPlot:
    def __init__(self, coordinate_system: CoordinateSystem):
        self.coordinate_system = coordinate_system
        
    def create_plot(self) -> go.Figure:
        """创建轨迹图"""
        trajectory = self.coordinate_system.get_trajectory()
        x_range, y_range = self.coordinate_system.get_range()
        
        # 创建基本图形
        fig = go.Figure()
        
        # 添加网格线
        self._add_grid(fig, x_range, y_range)
        
        # 如果有轨迹点，添加轨迹线和点
        if trajectory:
            x_coords = [coord.x for coord in trajectory]
            y_coords = [coord.y for coord in trajectory]
            
            # 添加轨迹线
            fig.add_trace(go.Scatter(
                x=x_coords,
                y=y_coords,
                mode='lines',
                name='轨迹',
                line=dict(color='blue', width=3)
            ))
            
            # 添加点
            fig.add_trace(go.Scatter(
                x=x_coords,
                y=y_coords,
                mode='markers',
                name='坐标点',
                marker=dict(
                    color='red',
                    size=10,
                    symbol='circle'
                )
            ))
            
            # 标记起点和终点
            fig.add_trace(go.Scatter(
                x=[x_coords[0]],
                y=[y_coords[0]],
                mode='markers+text',
                name='起点',
                text=['起点'],
                textposition='top center',
                marker=dict(color='green', size=15, symbol='star')
            ))
            
            fig.add_trace(go.Scatter(
                x=[x_coords[-1]],
                y=[y_coords[-1]],
                mode='markers+text',
                name='当前位置',
                text=['当前'],
                textposition='top center',
                marker=dict(color='purple', size=15, symbol='star')
            ))
        
        # 设置图形布局
        fig.update_layout(
            title=dict(
                text='AI 移动轨迹',
                font=dict(size=24)
            ),
            xaxis_title='X 坐标',
            yaxis_title='Y 坐标',
            showlegend=True,
            height=800,  # 增加图表高度
            xaxis=dict(
                range=[x_range[0], x_range[1]],
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='black',
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                range=[y_range[0], y_range[1]],
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor='black',
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                tickfont=dict(size=12)
            ),
            plot_bgcolor='white',
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                font=dict(size=12)
            )
        )
        
        return fig
    
    def _add_grid(self, fig: go.Figure, x_range: Tuple[float, float], y_range: Tuple[float, float]):
        """添加网格线"""
        # 计算网格间距
        x_span = x_range[1] - x_range[0]
        y_span = y_range[1] - y_range[0]
        
        # 根据范围大小动态调整网格间距
        grid_size = max(5, min(x_span, y_span) / 20)
        
        # 添加主要网格线
        x_ticks = np.arange(
            x_range[0],
            x_range[1] + 1,
            grid_size
        )
        y_ticks = np.arange(
            y_range[0],
            y_range[1] + 1,
            grid_size
        )
        
        # 垂直线
        for x in x_ticks:
            fig.add_shape(
                type='line',
                x0=x,
                y0=y_range[0],
                x1=x,
                y1=y_range[1],
                line=dict(color='lightgray', width=1, dash='dash')
            )
        
        # 水平线
        for y in y_ticks:
            fig.add_shape(
                type='line',
                x0=x_range[0],
                y0=y,
                x1=x_range[1],
                y1=y,
                line=dict(color='lightgray', width=1, dash='dash')
            ) 