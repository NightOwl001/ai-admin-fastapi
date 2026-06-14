# ai-admin-fastapi (1.0)

> **一个修复了模糊查询失效与非法注册漏洞的企业级 FastAPI 后端脚手架。**

## 项目简介

基于 Python + FastAPI 构建的后端管理系统，采用标准三层架构，独立实现用户注册/登录、JWT 身份认证、用户信息 CRUD、分页/模糊查询等核心功能。项目重点修复了模糊查询失效、非法用户注册等关键 Bug，确保系统稳定性与数据安全性。后续计划集成大模型 API 实现文档结构化提取。

## 技术栈

- **后端框架**：FastAPI
- **数据库**：MySQL 8.0+
- **ORM**：SQLAlchemy 2.0
- **身份认证**：PyJWT
- **数据校验**：Pydantic V2
- **开发语言**：Python 3.10+

## 项目目录结构
ai-admin-fastapi/
├── app/
│ ├── api/ # 接口控制层：路由定义与请求分发
│ ├── service/ # 业务逻辑层：核心功能处理
│ ├── dao/ # 数据访问层：数据库操作封装
│ ├── model/ # 数据模型：ORM实体类 + 请求/响应参数校验
│ ├── utils/ # 工具类：JWT工具、数据库连接、日志配置
│ ├── config/ # 项目配置：环境变量读取
│ └── main.py # 项目入口文件
├── .env.example # 环境变量模板
├── README.md # 项目说明文档
└── requirements.txt # 项目依赖清单

text

## 已实现功能

### 用户模块
- 用户注册接口（严格参数校验 + 自动清洗）
- 用户登录接口（JWT Token 生成与校验）
- 用户信息增删改查（CRUD）
- 用户列表分页查询（自定义页码与每页条数）
- 用户信息模糊查询（支持任意位置匹配）

### 基础工程能力
- 标准三层架构（Controller/Service/DAO）
- 请求参数全链路校验（类型、长度、格式）
- 数据库 ORM 操作封装
- 全局异常统一处理 + 标准化返回格式
- 接口访问日志记录

## 核心问题解决与优化

### 1. 修复模糊查询完全失效
- **现象**：数据库存在匹配数据，但条件查询返回空列表。
- **解决方案**：  
  - 将 SQL 通配符改为 `%{username}%`，实现任意位置匹配。  
  - 增加严格空值/纯空格过滤（`if username is not None and username.strip() != ""`）。  
- **成果**：模糊查询准确率 100%，支持关键词任意位置匹配。

### 2. 修复非法用户注册的安全漏洞
- **现象**：空用户名、1位用户名、5位短密码可正常注册，产生脏数据。
- **解决方案**：  
  - 使用 Pydantic V2 的 `Field(min_length=, max_length=)` 限制用户名（2-32位）和密码（6-64位）。  
  - 修复自动去空格的兼容性问题（采用 `@field_validator(mode='before')`）。  
- **成果**：彻底杜绝非法注册，数据质量与系统安全性大幅提升。

## 后续计划（AI 模块）

- 集成大模型 API（DeepSeek）实现 Excel/TXT 文档的字段自动提取（JSON 输出）。
- 支持批量导入时的数据清洗与校验。

## 项目启动

### 安装依赖
```bash
pip install -r requirements.txt
配置环境变量
复制 .env.example 为 .env，填写本地数据库配置：

env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=你的密码
DB_NAME=study
DB_CHARSET=utf8mb4
JWT_SECRET_KEY=你的密钥
JWT_EXPIRE_MINUTES=1440
启动项目
bash
uvicorn app.main:app --reload
访问接口文档
启动成功后，浏览器打开：

text
http://127.0.0.1:8000/docs
注意事项
若提示 “URL 拼写错误”，请检查项目是否成功启动、端口是否被占用、浏览器地址是否正确（不要漏掉 /docs）。

Python 版本建议 3.10 以上。
