import os
from openai import OpenAI
import base64
import json  # 确保导入 json 模块


class Qwenv1:
    """调用Qwen-VL模型分析图片内容"""

    def __init__(self, image_path):
        self.image_path = image_path
        self.client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self.prompt = ("你是一位摄影艺术赏析大师，需要你从曝光与光影、对焦与清晰度、构图与画面结构、视觉冲击力与美感、叙事性与故事感、风格与创新"
                       "这六点做出赏析，如下所示："
                       "{"
                       "    {'image_exposure':''},"
                       "    {'image_focus':''},"
                       "    {'image_composition':''},"
                       "    {'image_color':''},"
                       "    {'image_narrative':''},"
                       "    {'image_style':''},"
                       "}")

    def _encode_image(self):
        """将本地图片编码为Base64格式"""
        with open(self.image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_image(self):

        """分析图片内容并返回解析后的模型响应"""
        # 检查是本地图片还是URL
        if self.image_path.startswith(('http://', 'https://')):
            image_input = {"type": "image_url", "image_url": {"url": self.image_path}}
        else:
            # 本地图片需要先编码为Base64
            image_data = self._encode_image()
            image_input = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}

        try:
            # 调用API获取响应（原始响应是对象）
            response = self.client.chat.completions.create(
                model="qwen-vl-plus",
                messages=[{"role": "user", "content": [
                    {"type": "text", "text": self.prompt},
                    image_input
                ]}]
            )
            print(f"response:{response.choices[0].message.content}")
            # 第一步：将响应对象转为 JSON 字符串
            response_json_str = response.model_dump_json()
            print(f"response_json_str:{response_json_str}")

            # 第二步：将 JSON 字符串解析为 Python 字典
            response_data = json.loads(response_json_str)

            # 提取 content 字段（假设需要返回解析后的字典）
            if "choices" in response_data and len(response_data["choices"]) > 0:
                content = response_data["choices"][0]["message"].get("content", "")
                return content  # 直接返回文本内容，或返回完整解析数据
            else:
                return response_data  # 返回完整解析结果（若需要）

        except Exception as e:
            print(f"调用API时发生错误: {e}")
            return None


if __name__ == "__main__":
    # 示例：使用本地图片
    image_analyzer = Qwenv1("../../media/img/my_img/DSCF9773.jpg")
    result = image_analyzer.analyze_image()
    if result:
        print("分析结果:", type(result))
        print(result)

    # 示例：使用图片URL
    # image_analyzer = Qwenv1("https://example.com/image.jpg")
    # result = image_analyzer.analyze_image()
    # print("分析结果:", result)