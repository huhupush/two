import streamlit as st
import os
from datetime import datetime
from modules.spatial_decision.coordinate.coordinate_system import CoordinateSystem
from modules.spatial_decision.visualization.trajectory_plot import TrajectoryPlot
from modules.spatial_decision.analysis.trajectory_analysis import TrajectoryAnalysis
import time

TRAJECTORY_FILE = 'data/trajectories/trajectory.json'

def init_coordinate_system():
    """初始化或获取坐标系统"""
    if 'coordinate_system' not in st.session_state:
        st.session_state.coordinate_system = CoordinateSystem()
        # 尝试加载轨迹
        load_trajectory(st.session_state.coordinate_system)
    return st.session_state.coordinate_system

def init_state():
    """初始化状态变量"""
    if 'is_thinking' not in st.session_state:
        st.session_state.is_thinking = False
    if 'current_thought' not in st.session_state:
        st.session_state.current_thought = ""
    if 'thought_container' not in st.session_state:
        st.session_state.thought_container = None

def save_trajectory(coordinate_system):
    """保存轨迹到文件"""
    if not os.path.exists('data/trajectories'):
        os.makedirs('data/trajectories')
    coordinate_system.save_trajectory(TRAJECTORY_FILE)

def load_trajectory(coordinate_system):
    """加载轨迹文件"""
    if os.path.exists(TRAJECTORY_FILE):
        coordinate_system.load_trajectory(TRAJECTORY_FILE)
        return True
    return False

def display_analysis(analysis: TrajectoryAnalysis):
    """显示轨迹分析结果"""
    st.subheader('轨迹分析')
    
    # 基本统计信息
    stats = analysis.get_basic_stats()
    st.write('基本统计：')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('总点数', stats['total_points'])
    with col2:
        st.metric('总距离', f"{stats['total_distance']:.2f}")
    with col3:
        st.metric('平均步长', f"{stats['average_step_size']:.2f}")
    
    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric('方向改变次数', stats['direction_changes'])
    with col5:
        patterns = analysis.get_movement_patterns()
        st.metric('主要方向', patterns['primary_direction'])
    with col6:
        st.metric('移动类型', patterns['movement_type'])
    
    # 移动倾向预测
    tendency = analysis.predict_tendency()
    col7, col8 = st.columns(2)
    with col7:
        st.metric('预测趋势', tendency['tendency'])
    with col8:
        st.metric('置信度', f"{tendency['confidence']*100:.0f}%")

def main():
    st.set_page_config(layout="wide")
    st.title('AI 空间决策研究')
    st.write('研究 AI 在二维坐标系中的移动决策行为')
    
    # 初始化坐标系统和状态
    coordinate_system = init_coordinate_system()
    init_state()
    
    # 创建分析器
    analysis = TrajectoryAnalysis(coordinate_system)
    
    # 创建标签页
    tab1, tab2 = st.tabs(['轨迹可视化', '数据分析'])
    
    with tab1:
        # 创建状态显示区域（在最上方）
        status_area = st.container()
        with status_area:
            # 创建两列用于状态显示
            status_col1, status_col2 = st.columns([1, 4])
            with status_col1:
                if st.session_state.is_thinking:
                    st.info('🤔 AI 正在思考')
            with status_col2:
                # 创建思考过程显示容器
                thought_placeholder = st.empty()
                st.session_state.thought_container = thought_placeholder
        
        # 创建两列布局，调整比例使图表更大
        col1, col2 = st.columns([4, 1])
        
        with col1:
            # 显示轨迹图
            plot = TrajectoryPlot(coordinate_system)
            st.plotly_chart(plot.create_plot(), use_container_width=True)
        
        with col2:
            st.subheader('控制面板')
            
            # 添加新的坐标点
            if st.button('生成下一个坐标', use_container_width=True):
                try:
                    # 设置思考状态
                    st.session_state.is_thinking = True
                    st.session_state.current_thought = "正在分析当前轨迹..."
                    if st.session_state.thought_container:
                        st.session_state.thought_container.info(st.session_state.current_thought)
                    
                    # 预测下一个点
                    next_x, next_y, thought_process = coordinate_system.predict_next_point(
                        thought_container=st.session_state.thought_container
                    )
                    
                    # 添加新点
                    coordinate_system.add_point(next_x, next_y, thought_process)
                    
                    # 自动保存轨迹
                    save_trajectory(coordinate_system)
                    st.success(f'添加新坐标点: ({next_x:.2f}, {next_y:.2f})')
                    
                finally:
                    # 确保状态被重置
                    st.session_state.is_thinking = False
                    st.session_state.current_thought = ""
            
            # 显示当前轨迹信息
            trajectory = coordinate_system.get_trajectory()
            if trajectory:
                st.write(f'当前轨迹点数: {len(trajectory)}')
                
                # 显示最后一个点的坐标
                last_point = trajectory[-1]
                st.write(f'当前位置: ({last_point.x:.2f}, {last_point.y:.2f})')
                
                # 显示最后一个点的思考过程
                if last_point.thought_process:
                    with st.expander("上一步的决策过程", expanded=False):
                        st.write(last_point.thought_process)
            
            # 重置轨迹
            if st.button('重置轨迹', use_container_width=True):
                if os.path.exists(TRAJECTORY_FILE):
                    os.remove(TRAJECTORY_FILE)
                st.session_state.coordinate_system = CoordinateSystem()
                st.rerun()
    
    with tab2:
        if coordinate_system.get_trajectory():
            display_analysis(analysis)
        else:
            st.info('请先生成一些轨迹点以查看分析结果')

if __name__ == '__main__':
    main() 