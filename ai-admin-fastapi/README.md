# ai-admin-fastapi（1.0）

## 项目简介

基于 Python + FastAPI 构建的后端管理系统，采用三层架构设计，实现了用户注册/登录、JWT身份认证、用户信息增删改查、分页/模糊查询等核心后端功能，后续将集成AI文本处理、智能解析等能力模块。

## 技术栈

- 后端框架：FastAPI
- 数据库：MySQL
- ORM框架：SQLAlchemy
- 身份认证：JWT
- 数据校验：Pydantic
- 开发语言：Python 3.10+

## 项目目录结构
ai-admin-fastapi/
├── api/          # 接口控制层（Controller）：路由定义
├── service/      # 业务逻辑层（Service）：核心功能处理
├── dao/          # 数据访问层（DAO）：数据库操作
├── model/        # 数据模型（ORM实体类 + 参数校验）
├── utils/        # 工具类（JWT、数据库连接、异常处理）
├── config/       # 项目配置读取
├── main.py       # 项目入口文件
├── .env.example  # 环境变量模板
├── README.md     # 项目说明
└── requirements.txt  # 项目依赖

## 已实现功能

用户模块

- 用户注册/登录接口
- JWT Token身份认证与权限校验
- 用户信息增删改查（CRUD）
- 用户列表分页查询、模糊查询

基础能力

- 后端三层架构规范开发（Controller/Service/DAO）
- 请求参数全链路校验（Pydantic）
- 数据库ORM操作封装
- 接口异常统一处理

## 后续计划（AI模块待开发中）

AI文本关键词提取接口
AI智能解析Excel文件接口
（后续完成开发，同步更新代码与文档）

## 项目启动

1. 安装依赖
   pip install -r requirements.txt

2. 配置环境变量
   复制 .env.example 为 .env，填写本地数据库配置

3. 启动项目
   uvicorn app.main:app --reload

4. 接口文档地址
   http://127.0.0.1:8000/docs

