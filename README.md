# 占位图生成工具

一个简单的占位图片生成服务，可以生成自定义尺寸和颜色的占位图。

## 功能特点

- 支持自定义图片尺寸
- 支持自定义背景颜色和文字颜色
- 在图片中显示尺寸信息
- 支持错误处理和日志记录

## 安装说明

### 1. 克隆仓库

```bash
git clone https://github.com/Chen-Yue/placeholder.git
cd placeholder
```

### 2. 创建虚拟环境并激活

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行服务

```bash
python app.py
```

## 接口使用说明

访问 [https://ph.ipenx.cn/docs](https://ph.ipenx.cn/docs) 获取详细的 API 文档。

### 基本用法示例：

1. 生成 300x200 的图片：

   ```
   https://ph.ipenx.cn/?300200
   ```

2. 自定义颜色：

   ```
   https://ph.ipenx.cn/?300200?bg=FFFFFF&color=000000
   ```

3. 生成正方形图片：

   ```
   https://ph.ipenx.cn/?500
   ```

### 参数说明

| 参数  | 说明                                       | 示例           | 默认值  |
| ----- | ------------------------------------------ | -------------- | ------- |
| 尺寸  | 图片尺寸，格式为 `width*height` 或单个数字 | 300*200 或 300 | 300x300 |
| bg    | 背景颜色，六位十六进制颜色值               | FFFFFF         | BEBEBE  |
| color | 文字颜色，六位十六进制颜色值               | 000000         | D3D3D3  |

## 配置要求

- Python 3.8+
- 需要楷体字体文件 (KaiTi-1.ttf)

## 日志

服务会自动记录访问日志到 `placeholder.log` 文件中，包含：

- 访问来源IP
- 浏览器信息
- 图片生成信息
- 错误信息

## 在线演示

访问以下链接查看效果：

- [300x200 默认图片](https://ph.ipenx.cn/?300*200)
- [500x500 黑底白字](https://ph.ipenx.cn/?500*500?bg=000000&color=FFFFFF)
- [800x400 自定义颜色](https://ph.ipenx.cn/?800*400?bg=F5F5F5&color=333333)

## 作者

Chen'Rue

## License

[MIT License](LICENSE)