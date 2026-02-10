# 配置文件
import os

# AI API配置（用户需要自己申请）
AI_API_KEY = os.getenv("AI_API_KEY", "")  # 从环境变量读取
AI_API_URL = "https://api.moonshot.cn/v1/chat/completions"  # Kimi API

# 数据库配置
DATABASE_PATH = "procurement_data.db"

# 系统配置
SYSTEM_NAME = "智能研发样件采购助手系统"
VERSION = "v1.0"

# 供应商匹配权重配置
MATCH_WEIGHTS = {
    "capability": 0.4,      # 能力匹配权重
    "response_time": 0.2,   # 响应速度权重
    "quality_score": 0.25,  # 质量评分权重
    "price_level": 0.15     # 价格等级权重
}

# 相似度阈值
SIMILARITY_THRESHOLD = 0.6  # 历史案例相似度阈值
