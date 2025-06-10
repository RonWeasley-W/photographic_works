import io
import os
from openai import OpenAI
import base64
from PIL import Image


class Qwenv1:
    """调用Qwen-VL模型分析图片内容"""

    def __init__(self, image_path):
        self.image_path = image_path
        self.client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        self.prompts = [("你是一位摄影作品赏析大师，现在请你根据此摄影作品进行取名，要求作品名称在1字到10字之间，尽量使用中文。"),
                        ("你是一位摄影作品赏析大师，现在请你根据以下内容进行赏析（对于所有赏析内容提炼为一整段，不需要分段、分行或分点阐述）："
                         "请深入分析图片中的曝光处理技巧，从整体曝光度出发，探讨其是否达到了最佳视觉效果。"
                         "是正常曝光展现了丰富细节，还是通过过曝或欠曝营造出独特氛围？同时，仔细观察光影运用，"
                         "思考光源类型、方向及强度对画面的影响。是柔和的散射光带来细腻过渡，还是强烈直射光形"
                         "成鲜明对比？光影如何勾勒物体轮廓、塑造立体感并引导观者视线？又怎样借助光影互动构建层"
                         "次感与空间深度，创造出富有艺术感染力的画面意境呢？"),
                        ("你是一位摄影作品赏析大师，现在请你根据以下内容进行赏析（对于所有赏析内容提炼为一整段，不需要分段、分行或分点阐述）："
                         "请全面审视图片中的对焦效果，主体是否被精准锐利地呈现？是通过单点对焦精确锁定关键部位，"
                         "还是利用区域对焦确保多个重要元素均处于清晰状态？同时，思考景深控制对画面清晰度分布的影响。"
                         "浅景深是否巧妙地虚化背景或前景，从而突出主体并营造梦幻氛围；大景深是否保证了从前景到背景的"
                         "广泛清晰范围，适合展现宏大场景的细节 。此外，留意整个画面的清晰度表现，是否存在因手抖、主"
                         "体运动等原因导致的模糊现象，以及这种模糊是否为有意为之的艺术效果，如动感模糊传达速度感或"
                         "时间流逝感 。这些对焦与清晰度方面的处理共同塑造了怎样的视觉体验与艺术魅力呢 ？"),
                        ("你是一位摄影作品赏析大师，现在请你根据以下内容进行赏析（对于所有赏析内容提炼为一整段，不需要分段、分行或分点阐述）："
                         "请深入剖析图片的构图方式及其对画面结构的影响。首先，判断是否运用了经典的构图法则，例如三分法、"
                         "黄金螺旋、对称式或框架式构图等。这些法则如何引导观者的视线，并在画面中创造出平衡和谐之感？接"
                         "着，观察元素的布局与分布，主要视觉元素是否合理安排以形成良好的比例关系，避免画面过于拥挤或空旷。"
                         "同时，留意画面中的留白部分，它是如何通过负空间增强主体的表现力并赋予画面呼吸感。"),
                        ("你是一位摄影作品赏析大师，现在请你根据以下内容进行赏析（对于所有赏析内容提炼为一整段，不需要分段、分行或分点阐述）："
                         "请深入感受并分析图片所传递出的视觉冲击力与美感。首先，关注画面中是否存在强烈的对比元素，"
                         "如色彩对比、明暗对比或大小对比等，这些对比如何瞬间吸引观者的注意力，并在心理上产生震撼效果。"
                         "同时，思考是否通过独特的视角或拍摄手法（如超广角镜头带来的夸张透视、无人机俯拍展现宏大场面等）"
                         "增强了视觉冲击力，让画面更具张力和感染力。接着，从美感层面出发，体会图片中的和谐之美。色彩搭配是"
                         "否呈现出悦目的组合，是温暖色调带来舒适愉悦感，还是冷暖交织营造出梦幻般的意境？光影运用是否恰到好处，"
                         "柔和的光线勾勒出细腻的质感，还是强烈光效塑造了戏剧性的氛围？此外，构图是否遵循美学原则，创造出平衡且富"
                         "有韵律的画面结构，使观者在欣赏时感受到一种内在的秩序美。最后，综合考量视觉冲击力与美感之间的关系。它们是"
                         "否相辅相成，共同构建起一个既令人印象深刻又赏心悦目的艺术作品？这种结合是否成功地传达了摄影师的情感意图，"
                         "并激发了观者内心深处的共鸣？"),
                        ("你是一位摄影作品赏析大师，现在请你根据以下内容进行赏析（对于所有赏析内容提炼为一整段，不需要分段、分行或分点阐述）："
                         "请深入挖掘图片中的叙事线索，探索其如何通过视觉语言讲述一个引人入胜的故事。首先，观察画面中的主体与背景元素，"
                         "它们之间是否存在明确的互动关系？这种互动是否能够引发观者对情节发展的好奇心，例如人物的表情、动作或姿态是否暗"
                         "示了某种情感状态或行为意图？同时，留意场景细节，如道具、环境特征等，这些细节是否为故事提供了更多的背景信息和时间"
                         "、空间定位。接着，思考图片是否构建了一个完整的叙事框架。它是否展现了一个特定的瞬间，而这个瞬间又是更大故事的一"
                         "部分？摄影师是否通过构图、光影等手法引导观者的视线按照一定的顺序移动，从而逐步揭示故事内容？此外，色彩氛围是"
                         "否强化了故事的情感基调，是温暖明亮传递希望与活力，还是冷峻灰暗营造悬疑与忧郁？最后，评估图片所传达的故事感是否具"
                         "有开放性与多义性。它是否允许观者根据自身经验与理解进行个性化的解读，从而激发丰富的想象力与情感共鸣？这种叙事性与故"
                         "事感是否成功地将一张静态图片转化为一部充满生命力的微型剧作，让观者在凝视之间仿佛听到了故事的声音？"),
                        ("你是一位摄影作品赏析大师，现在请你根据以下内容进行赏析（对于所有赏析内容提炼为一整段，不需要分段、分行或分点阐述）："
                         "请深入剖析图片所展现出的独特风格与创新之处。首先，思考摄影师是否在作品中融入了个人鲜明的艺术特色，这种特色"
                         "是通过特定的拍摄手法、构图方式还是后期处理技术来体现？例如，是否采用了非常规的视角（如极低或极高的拍摄角度）"
                         "打破传统视觉习惯，或者运用特殊的镜头效果（如鱼眼镜头的畸变、移轴镜头的微缩景观）营造出别具一格的画面氛围。接着"
                         "，探讨图片在创新方面的表现。它是否突破了既定题材的限制，以全新的方式重新定义某一主题？比如，在人像摄影中，是否"
                         "将人物置于非典型的环境中，从而赋予肖像更多社会或文化意义；在风景摄影中，是否借助抽象化处理让自然景观呈现出超现"
                         "实主义的美感。同时，观察色彩运用、光影处理等方面是否有大胆尝试，这些尝试是否为画面增添了意想不到的视觉冲击力与"
                         "情感张力。最后，综合评价风格与创新之间的关系。它们是否相辅相成，使得这张图片不仅具有高度辨识度，还能引发观者对"
                         "摄影艺术边界的新思考？这种风格与创新是否体现了摄影师对当代社会、文化或技术趋势的敏锐洞察，并以此推动摄影艺术向"
                         "前发展？")]

    def _encode_image(self, compress=False, max_size=5 * 1024 * 1024):  # 默认最大5MB
        """将图片编码为Base64，可选择压缩以减小尺寸"""
        try:
            if not compress:
                # 不压缩直接读取文件
                with open(self.image_path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode('utf-8')

            # 压缩图片
            with Image.open(self.image_path) as img:
                # 转换为RGB模式以处理PNG等格式
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # 计算图片大小
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=90)
                image_size = buffer.tell()

                # 如果图片大小超过限制，则进行压缩
                quality = 90
                while image_size > max_size and quality > 10:
                    quality -= 10
                    buffer = io.BytesIO()
                    img.save(buffer, format="JPEG", quality=quality)
                    image_size = buffer.tell()
                    print(f"调整图片质量为{quality}%, 当前大小: {image_size / 1024:.2f}KB")

                # 最终编码
                buffer.seek(0)
                return base64.b64encode(buffer.read()).decode('utf-8')

        except Exception as e:
            print(f"图片编码或压缩时出错: {e}")
            return None

    def analyze_image(self):
        """分析图片内容并返回解析后的模型响应"""
        # 存放大模型响应输出
        image_analyze = {
                            'image_name': '',
                            'image_exposure': '',
                            'image_focus': '',
                            'image_composition': '',
                            'image_color': '',
                            'image_narrative': '',
                            'image_style': '',
                        }
        # 检查文件是否存在（针对本地路径）
        if not self.image_path.startswith(('http://', 'https://')):
            if not os.path.exists(self.image_path):
                print(f"错误: 本地图片文件不存在 - {self.image_path}")
                return None

        # 准备图片输入
        if self.image_path.startswith(('http://', 'https://')):
            # 远程图片URL
            image_input = {
                "type": "image_url",
                "image_url": {
                    "url": self.image_path
                }
            }
        else:
            # 本地图片需要先编码为Base64
            image_data = self._encode_image(compress=True)
            if not image_data:
                return None
            image_input = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_data}"
                }
            }

        try:
            # 对每个提示词，分别调用API获取响应
            for prompt_text, image_key in zip(self.prompts, image_analyze.keys()):
                # 构建消息格式
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            image_input
                        ]
                    }
                ]

                # 调用API获取响应
                response = self.client.chat.completions.create(
                    model="qwen-vl-plus",
                    messages=messages,
                    temperature=0.1  # 降低温度使输出更确定性
                )

                # 提取响应内容并添加到结果列表
                image_value = response.choices[0].message.content
                # 去除换行符
                image_value = image_value.replace("\n", "")
                image_analyze[image_key] = image_value

            return image_analyze

        except Exception as e:
            print(f"调用API时发生错误: {e}")
            # 打印完整的错误响应，帮助进一步诊断
            if hasattr(e, 'response') and e.response:
                print(f"完整错误响应: {e.response}")
            return None


if __name__ == "__main__":
    # 示例：使用本地图片
    image_analyzer = Qwenv1("../../media/img/my_img/DSCF9773.jpg")
    result = image_analyzer.analyze_image()
    for key in result.keys():
        print(result[key])

