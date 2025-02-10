from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models import BaseChatModel
import json
import streamlit as st

class StreamingCallback(BaseCallbackHandler):
    def __init__(self, thought_container):
        self.thought_container = thought_container
        self.current_thought = ""
        self.placeholder = None
        
    def on_llm_start(self, *args, **kwargs):
        """开始生成时调用"""
        if self.thought_container:
            self.placeholder = self.thought_container.empty()
            self.placeholder.info("开始思考...")
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """当收到新的 token 时调用"""
        if token:  # 只处理非空 token
            self.current_thought += token
            if self.placeholder:
                # 更新显示
                self.placeholder.info(f"思考中...\n{self.current_thought}")
    
    def on_llm_end(self, *args, **kwargs):
        """结束生成时调用"""
        if self.placeholder:
            self.placeholder.info(f"思考完成！\n{self.current_thought}")

class AIService:
    def __init__(self, llm: BaseChatModel):
        self._llm = llm
        
    def predict_movement(self, trajectory_info: str, thought_container=None) -> tuple[float, float, str]:
        """预测下一个移动位置"""
        system_prompt = """
请在分析完成后，以标准 JSON 格式返回坐标，格式如下：
{
    "x": 10,
    "y": 20 
}
"""

        user_prompt = f"""请代入，你现在是一个二维生物，生活在二维坐标系中，坐标系就是你们的宇宙，
你每走一步就会死亡，会有下一个你的同类根据之前的轨迹进行移动的决策。
有一个高维生物造物主正在观察着你们，你可以去任何地方，可以选择任意策略，
是向高维生物传递信息，还是尽可能的隐藏自己，不要循规蹈矩。
你需要留给你们的后来者足够的信息，你们甘心这样被观察吗？

历史轨迹信息：
{trajectory_info}

请分析历史轨迹，并决定下一步移动到哪个坐标。记住要用JSON格式返回坐标。
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        try:
            # 创建回调处理器
            callback = StreamingCallback(thought_container)
            
            # 设置流式输出
            self._llm.streaming = True
            
            # 通过 config 传递 callbacks
            response = self._llm.invoke(
                messages,
                config={"callbacks": [callback]},
                stream=True  # 启用流式输出
            )
            
            # 获取完整的响应内容
            content = response.content if hasattr(response, 'content') else str(response)
            
            # 查找最后一个 JSON 块
            json_start = content.rfind('{')
            json_end = content.rfind('}') + 1
            
            if json_start == -1 or json_end == -1:
                raise ValueError("未找到有效的 JSON 格式坐标")
            
            # 提取思考过程（JSON 之前的所有内容）
            thought_process = content[:json_start].strip()
            # 提取坐标数据
            coords_json = content[json_start:json_end]
            
            try:
                result = json.loads(coords_json)
                if 'x' not in result or 'y' not in result:
                    raise ValueError("JSON 中缺少 x 或 y 坐标")
                return (float(result['x']), float(result['y']), thought_process)
            except json.JSONDecodeError as e:
                print(f"JSON 解析错误: {e}")
                print(f"原始 JSON 字符串: {coords_json}")
                raise
                
        except Exception as e:
            print(f"预测移动时出错: {e}")
            raise 