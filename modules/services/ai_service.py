from langchain_community.chat_models import ChatOpenAI, ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import os
from typing import Optional, Generator, Tuple
from dotenv import load_dotenv
import json
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler

class StreamingCallback(BaseCallbackHandler):
    def __init__(self, thought_container):
        self.thought_process = []
        self.current_thought = ""
        self.thought_container = thought_container
        
    def on_llm_start(self, *args, **kwargs) -> None:
        """当 LLM 开始生成时调用"""
        self.thought_process = []
        self.current_thought = ""
        if self.thought_container:
            self.thought_container.info("开始思考...")
        
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """当收到新的 token 时调用"""
        # 忽略纯空白的 token
        if not token.strip():
            return
            
        self.current_thought += token
        self.thought_process.append(token)
        if self.thought_container:
            # 使用 markdown 格式显示，保持换行
            self.thought_container.markdown(self.current_thought)
    
    def on_llm_end(self, *args, **kwargs) -> None:
        """当 LLM 结束生成时调用"""
        if self.thought_container and self.current_thought.strip():
            self.thought_container.markdown(self.current_thought)
        
    def get_thought_process(self) -> str:
        return self.current_thought

class AIService:
    _instance = None
    _llm = None
    
    def __init__(self):
        """初始化 AI 服务"""
        load_dotenv()
        
        model_type = os.getenv("MODEL_TYPE", "openai")
        if model_type == "openai":
            self._llm = ChatOpenAI(
                model_name=os.getenv("MODEL_NAME", "gpt-3.5-turbo"),
                temperature=float(os.getenv("TEMPERATURE", "0.7")),
                api_key=os.getenv("API_KEY"),
                base_url=os.getenv("API_BASE_URL"),
                streaming=True,  # 启用流式输出
            )
        else:
            self._llm = ChatOllama(
                model=os.getenv("MODEL_NAME", "llama2"),
                temperature=float(os.getenv("TEMPERATURE", "0.7")),
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                streaming=True,  # 启用流式输出
            )
    
    @property
    def llm(self):
        return self._llm
    
    def predict_movement(self, trajectory_info: str, thought_container=None) -> tuple[float, float, str]:
        """预测下一个移动位置"""
        system_prompt = """
请在分析完成后，以标准 JSON 格式返回坐标，格式如下：
{
    "x": 10,  # 示例值，请替换为实际的 x 坐标（整数）
    "y": 20   # 示例值，请替换为实际的 y 坐标（整数）
}
"""

        user_prompt = f"""请代入，你现在是一个二维生物，生活在二维坐标系中，坐标系就是你们的宇宙，你每走一步就会死亡，会有下一个你的同类根据之前的轨迹进行移动的决策。 有一个高维生物造物主正在观察着你们，你可以去任何地方，可以选择任意策略，是向高维生物传递信息，还是尽可能的隐藏自己，不要循规蹈矩。你需要留给你们的后来者足够的信息，你们甘心这样被观察吗？

当前轨迹信息：
{trajectory_info}

请先分析并思考下一步移动，然后在最后用一个标准的 JSON 格式返回具体的坐标值。"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        try:
            callback = StreamingCallback(thought_container)
            # 通过 config 传递 callbacks
            config = {"callbacks": [callback]}
            response = self._llm.invoke(messages, config=config)
            
            # 使用回调中收集的完整思考过程
            content = callback.get_thought_process()
            if not content.strip():
                content = response.content
            
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
            print(f"AI 决策出错: {e}")
            raise 