from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont
import io
import os
import re
import logging
from datetime import datetime

app = Flask(__name__)

# 配置日志
logging.basicConfig(
    filename='placeholder.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

@app.route('/')
def placeholder():
    try:
        # 记录请求信息
        client_ip = request.remote_addr
        user_agent = request.user_agent.string
        logging.info(f'访问来源 IP: {client_ip} - 浏览器信息: {user_agent}')

        size_param = request.query_string.decode('utf-8')
        match = re.match(r'(\d+)(?:\*(\d+))?', size_param)

        if not match:
            logging.warning(f'无效的尺寸参数: {size_param}')
            # 默认返回 300x300 的图片
            width = height = 300
        else:
            width = int(match.group(1))
            height = int(match.group(2)) if match.group(2) else width

        # 记录图片尺寸
        logging.info(f'正在生成图片，尺寸为: {width}x{height}')

        # 使用安全的颜色处理
        try:
            bg_color = request.args.get('bg', 'BEBEBE')
            bg_color = tuple(int(bg_color[i:i+2], 16) for i in (0, 2, 4))
        except (ValueError, IndexError):
            logging.warning(f'无效的背景颜色参数: {request.args.get("bg")}，使用默认颜色')
            bg_color = (190, 190, 190)  # 默认灰色

        try:
            text_color = request.args.get('color', 'D3D3D3')
            text_color = tuple(int(text_color[i:i+2], 16) for i in (0, 2, 4))
        except (ValueError, IndexError):
            logging.warning(f'无效的文字颜色参数: {request.args.get("color")}，使用默认颜色')
            text_color = (211, 211, 211)  # 默认浅灰色

        image = Image.new('RGB', (width, height), color=bg_color)
        draw = ImageDraw.Draw(image)

        text = f"{width}x{height}"
        font_size = min(width, height) // 5

        try:
            font_path = "KaiTi-1.ttf"
            font = ImageFont.truetype(font_path, font_size)
        except OSError:
            logging.error(f'找不到字体文件: {font_path}，使用系统默认字体')
            font = ImageFont.load_default()

        textbbox = draw.textbbox((0, 0), text, font=font)
        textwidth, textheight = textbbox[2] - textbbox[0], textbbox[3] - textbbox[1]

        text_x = (width - textwidth) / 2
        text_y = (height - textheight) / 2

        draw.text((text_x, text_y), text, font=font, fill=text_color)

        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)

        logging.info('图片生成成功')
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        logging.error(f'生成图片时发生错误: {str(e)}')
        # 返回一个默认的错误图片
        width = height = 300
        image = Image.new('RGB', (width, height), color=(190, 190, 190))
        draw = ImageDraw.Draw(image)
        error_text = "Error"
        font = ImageFont.load_default()
        textbbox = draw.textbbox((0, 0), error_text, font=font)
        textwidth, textheight = textbbox[2] - textbbox[0], textbbox[3] - textbbox[1]
        text_x = (width - textwidth) / 2
        text_y = (height - textheight) / 2
        draw.text((text_x, text_y), error_text, font=font, fill=(211, 211, 211))
        
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')

# 添加文档路由
@app.route('/docs')
def api_docs():
    docs = {
        "项目名称": "占位图生成工具",
        "基础URL": "https://ph.ipenx.cn",
        "接口说明": {
            "生成占位图": {
                "接口地址": "/",
                "请求方式": "GET",
                "参数说明": {
                    "尺寸": {
                        "格式": "width*height 或 size",
                        "示例": "/?300*200 或 /?300",
                        "说明": "宽度x高度，如果只提供一个数字则生成正方形图片"
                    },
                    "bg": {
                        "格式": "六位十六进制颜色值",
                        "示例": "/?300*200?bg=BEBEBE",
                        "说明": "背景颜色，默认为BEBEBE（灰色）"
                    },
                    "color": {
                        "格式": "六位十六进制颜色值",
                        "示例": "/?300*200?color=D3D3D3",
                        "说明": "文字颜色，默认为D3D3D3（浅灰色）"
                    }
                },
                "示例": [
                    "https://ph.ipenx.cn/?300*200",
                    "https://ph.ipenx.cn/?500",
                    "https://ph.ipenx.cn/?800*600?bg=FFFFFF&color=000000"
                ]
            }
        }
    }
    return jsonify(docs)

if __name__ == '__main__':
    app.run(debug=False)