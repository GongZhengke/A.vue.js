# 论坛爬虫 API

这是一个使用 Flask 开发的论坛内容爬虫 API 服务。

## 功能特点

- 爬取论坛帖子列表
- 爬取帖子详情内容
- RESTful API 设计
- 支持跨域请求

## 安装说明

1. 克隆项目到本地
2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行项目：
```bash
python run.py
```

## API 接口说明

### 获取帖子列表
- 接口：`/api/posts`
- 方法：GET
- 参数：
  - timestamp: 时间戳（可选，默认无）

### 获取帖子详情
- 接口：`/api/posts/<post_id>`
- 方法：GET

## 注意事项

- 请遵守目标网站的robots.txt规则
- 建议添加适当的请求延迟，避免对目标服务器造成压力
- 仅用于学习和研究目的
