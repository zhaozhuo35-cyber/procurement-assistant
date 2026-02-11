# 智能研发样件采购助手系统
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from database import Database
from ai_helper import AIHelper
import config

# 页面配置
st.set_page_config(
    page_title=config.SYSTEM_NAME,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apple风格设计 - 墨绿色主题
st.markdown("""
<style>
    /* ============ 主色系：墨绿色 + Apple风格 ============ */
    :root {
        --primary-color: #1e4f4b;
        --primary-light: #2d5f5a;
        --primary-dark: #143734;
        --accent-color: #d4af37;
        --bg-main: #f5f5f7;
        --bg-white: #ffffff;
        --text-dark: #1d1d1f;
        --text-medium: #424245;
        --text-light: #86868b;
        --border-color: #d2d2d7;
        --shadow-sm: 0 2px 8px rgba(0,0,0,0.08);
        --shadow-md: 0 4px 16px rgba(0,0,0,0.12);
    }

    /* ============ 全局样式 - Apple简洁风 ============ */
    .stApp {
        background-color: var(--bg-main) !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", sans-serif !important;
    }

    .main .block-container {
        padding: 4rem 3rem !important;
        max-width: 1200px !important;
    }

    /* ============ 侧边栏 - Apple精致风格 ============ */
    section[data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid var(--border-color) !important;
        padding: 2rem 0 !important;
    }

    section[data-testid="stSidebar"] > div {
        padding: 0 1.5rem !important;
    }

    /* 侧边栏标题 */
    section[data-testid="stSidebar"] h1 {
        color: var(--primary-color) !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 0 0.5rem 0 !important;
        letter-spacing: -0.5px !important;
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: var(--text-medium) !important;
        font-size: 0.875rem !important;
        line-height: 1.6 !important;
    }

    /* 侧边栏分割线 */
    section[data-testid="stSidebar"] hr {
        border: none !important;
        border-top: 1px solid var(--border-color) !important;
        margin: 1.5rem 0 !important;
        opacity: 1 !important;
    }

    /* 侧边栏导航按钮 - Apple风格 */
    section[data-testid="stSidebar"] [role="radiogroup"] {
        gap: 4px !important;
        margin: 1.5rem 0 !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label {
        background-color: transparent !important;
        color: var(--text-dark) !important;
        padding: 0.875rem 1rem !important;
        margin: 0 !important;
        border-radius: 12px !important;
        border: none !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background-color: rgba(30, 79, 75, 0.08) !important;
        transform: translateX(2px) !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"] {
        background-color: var(--primary-color) !important;
        color: white !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(30, 79, 75, 0.3) !important;
    }

    /* 侧边栏info框 - Apple卡片风格 */
    section[data-testid="stSidebar"] .stAlert {
        background-color: rgba(30, 79, 75, 0.06) !important;
        border: 1px solid rgba(30, 79, 75, 0.15) !important;
        border-radius: 12px !important;
        padding: 1.25rem !important;
        border-left: none !important;
        color: var(--text-dark) !important;
    }

    section[data-testid="stSidebar"] .stAlert p,
    section[data-testid="stSidebar"] .stAlert li,
    section[data-testid="stSidebar"] .stAlert strong {
        color: var(--text-dark) !important;
        font-size: 0.875rem !important;
        line-height: 1.6 !important;
    }

    /* 侧边栏底部文字 */
    section[data-testid="stSidebar"] .stCaption {
        color: var(--text-light) !important;
        font-size: 0.75rem !important;
    }

    /* ============ 标题 - Apple简洁风 ============ */
    h1 {
        color: var(--text-dark) !important;
        font-weight: 700 !important;
        font-size: 3rem !important;
        letter-spacing: -1.5px !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 0 1rem 0 !important;
        line-height: 1.1 !important;
    }

    h2 {
        color: var(--text-dark) !important;
        font-weight: 600 !important;
        font-size: 1.75rem !important;
        margin: 3rem 0 1.5rem 0 !important;
        padding: 0 !important;
        border: none !important;
        letter-spacing: -0.5px !important;
    }

    h3 {
        color: var(--text-medium) !important;
        font-weight: 600 !important;
        font-size: 1.25rem !important;
        margin: 2rem 0 1rem 0 !important;
    }

    /* ============ 指标卡片 - Apple卡片风格 ============ */
    [data-testid="stMetric"] {
        background: var(--bg-white) !important;
        padding: 2rem 1.75rem !important;
        border-radius: 16px !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: var(--shadow-md) !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: var(--primary-color) !important;
        letter-spacing: -1px !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.875rem !important;
        color: var(--text-light) !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px !important;
        margin-bottom: 0.5rem !important;
    }

    /* ============ 按钮 - Apple风格 ============ */
    .stButton > button {
        background-color: var(--primary-color) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.875rem 1.75rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: -0.2px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 8px rgba(30, 79, 75, 0.25) !important;
    }

    .stButton > button:hover {
        background-color: var(--primary-light) !important;
        box-shadow: 0 4px 16px rgba(30, 79, 75, 0.35) !important;
        transform: translateY(-2px) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    .stButton > button[kind="primary"] {
        background-color: var(--accent-color) !important;
        color: white !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #c9a532 !important;
    }

    /* ============ 输入框 - Apple精致 ============ */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        background-color: var(--bg-white) !important;
        padding: 0.875rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(30, 79, 75, 0.1) !important;
        outline: none !important;
    }

    /* ============ Expander - Apple折叠面板 ============ */
    .streamlit-expanderHeader {
        background-color: var(--bg-white) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 1.25rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        color: var(--text-dark) !important;
        box-shadow: var(--shadow-sm) !important;
        margin-bottom: 0.75rem !important;
        transition: all 0.2s ease !important;
    }

    .streamlit-expanderHeader:hover {
        background-color: #fafafa !important;
        box-shadow: var(--shadow-md) !important;
    }

    .streamlit-expanderContent {
        background-color: var(--bg-white) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 1.75rem !important;
        margin-top: -0.5rem !important;
        box-shadow: var(--shadow-sm) !important;
    }

    /* ============ 表格 - Apple风格 ============ */
    [data-testid="stDataFrame"],
    .dataframe {
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: var(--shadow-sm) !important;
    }

    /* ============ Alert框 - Apple提示框 ============ */
    .stAlert {
        border-radius: 12px !important;
        border: 1px solid !important;
        padding: 1.25rem 1.5rem !important;
        background-color: var(--bg-white) !important;
        box-shadow: var(--shadow-sm) !important;
    }

    /* ============ 分割线 ============ */
    hr {
        border: none !important;
        border-top: 1px solid var(--border-color) !important;
        margin: 3rem 0 !important;
        opacity: 1 !important;
    }

    /* ============ Tabs - Apple标签页 ============ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background-color: transparent !important;
        border-bottom: 1px solid var(--border-color) !important;
        padding-bottom: 0 !important;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 0.875rem 1.5rem !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        color: var(--text-light) !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--primary-color) !important;
        background-color: rgba(30, 79, 75, 0.05) !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: var(--primary-color) !important;
        font-weight: 600 !important;
        border-bottom: 3px solid var(--primary-color) !important;
        margin-bottom: -1px !important;
    }

    /* ============ 图表 - Apple卡片 ============ */
    [data-testid="stPlotlyChart"] > div {
        background-color: var(--bg-white) !important;
        padding: 2rem !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 16px !important;
        box-shadow: var(--shadow-sm) !important;
    }

    /* ============ 隐藏Streamlit水印 ============ */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ============ 段落文字 - Apple排版 ============ */
    p {
        color: var(--text-medium) !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }
</style>
""", unsafe_allow_html=True)

# 初始化
@st.cache_resource
def init_database():
    return Database(config.DATABASE_PATH)

@st.cache_resource
def init_ai_helper():
    try:
        api_key = st.secrets.get("AI_API_KEY", "")
    except:
        api_key = config.AI_API_KEY
    return AIHelper(api_key, config.AI_API_URL)

db = init_database()
ai = init_ai_helper()

# 侧边栏导航
st.sidebar.title("🤖 " + config.SYSTEM_NAME)
st.sidebar.markdown(f"**版本**: {config.VERSION}")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "功能导航",
    ["📊 数据看板", "🔍 AI需求解析", "👥 供应商管理", "📚 历史案例"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info("""
**系统说明**
- AI需求解析：自动分析采购需求
- 智能匹配：推荐最佳供应商
- 历史复用：快速查找相似案例
- 数据统计：实时效率监控
""")

# ==================== 页面1：数据看板 ====================
if page == "📊 数据看板":
    st.title("📊 采购数据看板")

    # 获取统计数据
    stats = db.get_statistics()

    # 顶部指标卡片
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="本月处理需求",
            value=f"{stats['month_requests']} 单",
            delta=f"总计 {stats['total_requests']} 单"
        )

    with col2:
        avg_time = 25  # 这里可以后续加入真实计算
        st.metric(
            label="平均响应时间",
            value=f"{avg_time} 分钟",
            delta="-80% vs 传统方式",
            delta_color="inverse"
        )

    with col3:
        st.metric(
            label="供应商库",
            value=f"{stats['total_suppliers']} 家",
            delta="质量评分 " + str(stats['avg_quality'])
        )

    with col4:
        reuse_rate = min(28, (stats['month_requests'] / max(stats['total_requests'], 1)) * 100)
        st.metric(
            label="历史复用率",
            value=f"{reuse_rate:.0f}%",
            delta="持续提升中"
        )

    st.markdown("---")

    # 图表区域
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📈 效率提升趋势")

        # 模拟趋势数据
        trend_data = pd.DataFrame({
            '日期': pd.date_range(end=datetime.now(), periods=30, freq='D'),
            '处理时长(分钟)': [120, 115, 110, 105, 95, 90, 85, 80, 75, 70,
                         65, 60, 55, 50, 48, 45, 43, 40, 38, 35,
                         33, 32, 30, 29, 28, 27, 26, 25, 25, 25]
        })

        fig = px.line(trend_data, x='日期', y='处理时长(分钟)',
                     title='平均处理时长变化')
        fig.add_hline(y=150, line_dash="dash", line_color="red",
                     annotation_text="传统方式(150分钟)")
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("🎯 供应商使用分布")

        # 获取供应商数据（简化版本）
        suppliers = db.get_all_suppliers()
        if suppliers:
            # 模拟使用频率
            supplier_names = [s['name'] for s in suppliers[:5]]
            usage_counts = [12, 8, 6, 4, 2]

            fig = go.Figure(data=[go.Pie(
                labels=supplier_names,
                values=usage_counts,
                hole=.3
            )])
            fig.update_layout(title='TOP5供应商合作频次')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("暂无供应商数据，请先添加供应商信息")

    # 最近需求列表
    st.markdown("---")
    st.subheader("📋 最近采购需求")

    recent_requests = db.get_recent_requests(10)
    if recent_requests:
        df = pd.DataFrame(recent_requests)
        display_df = df[['request_title', 'material', 'process', 'quantity', 'status', 'created_at']]
        display_df.columns = ['需求标题', '材质', '工艺', '数量', '状态', '创建时间']
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("暂无采购需求记录，开始使用AI需求解析功能吧！")

# ==================== 页面2：AI需求解析 ====================
elif page == "🔍 AI需求解析":
    st.title("🔍 AI需求解析")
    st.markdown("输入采购需求，AI自动分析并推荐供应商")

    # 输入区域
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📝 输入需求")

        request_title = st.text_input("需求标题", placeholder="例如：L型铝合金支架")

        raw_description = st.text_area(
            "需求描述",
            height=150,
            placeholder="例如：需要加工一个铝合金支架，大概10件，下周要用，要阳极氧化处理"
        )

        uploaded_file = st.file_uploader("上传图纸/图片（可选）", type=['jpg', 'png', 'pdf'])

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            parse_btn = st.button("🤖 AI智能解析", type="primary", use_container_width=True)
        with col_btn2:
            clear_btn = st.button("🔄 清空重置", use_container_width=True)

    with col2:
        st.subheader("💡 快速示例")
        st.markdown("""
        **点击使用示例**：
        """)
        if st.button("示例1：CNC铝合金加工"):
            st.session_state.example = "需要CNC加工一个铝合金6061支架，10件，L型，需要阳极氧化，下周三前要"
        if st.button("示例2：3D打印"):
            st.session_state.example = "需要3D打印一个ABS塑料外壳，1件样品，明天要，用于测试"
        if st.button("示例3：钣金加工"):
            st.session_state.example = "不锈钢304钣金机箱，20件，需要折弯+焊接，10天交期"

        if 'example' in st.session_state:
            st.info(f"已加载示例：{st.session_state.example}")
            raw_description = st.session_state.example

    # 处理清空
    if clear_btn:
        st.session_state.clear()
        st.rerun()

    # AI解析处理
    if parse_btn and raw_description:
        with st.spinner("🤖 AI正在分析需求..."):
            # AI解析
            parsed_data = ai.parse_requirement(raw_description)

            # 保存到session state
            st.session_state.parsed_data = parsed_data
            st.session_state.raw_description = raw_description
            st.session_state.request_title = request_title or f"需求-{datetime.now().strftime('%Y%m%d%H%M')}"

        st.success("✅ 解析完成！")

    # 显示解析结果
    if 'parsed_data' in st.session_state:
        st.markdown("---")
        st.subheader("📋 解析结果")

        parsed = st.session_state.parsed_data

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**零件信息**")
            st.write(f"零件类型: `{parsed.get('part_type', '未识别')}`")
            st.write(f"材质: `{parsed.get('material', '未识别')}`")
            st.write(f"数量: `{parsed.get('quantity', 0)} 件`")

        with col2:
            st.markdown("**工艺要求**")
            st.write(f"加工工艺: `{parsed.get('process', '未识别')}`")
            st.write(f"表面处理: `{parsed.get('surface_treatment', '未识别')}`")
            st.write(f"交期: `{parsed.get('delivery_urgency', '未识别')}`")

        with col3:
            st.markdown("**需补充信息**")
            missing = parsed.get('missing_info', [])
            if missing:
                for info in missing:
                    st.warning(f"⚠️ {info}")
            else:
                st.success("✅ 信息完整")

        # 生成需求清单
        with st.expander("📄 查看需求确认清单（可复制发给研发）"):
            checklist = ai.generate_requirement_checklist(parsed)
            st.code(checklist, language="text")

        # 智能匹配供应商
        st.markdown("---")
        st.subheader("🎯 智能供应商匹配")

        suppliers = db.get_all_suppliers()

        if suppliers:
            with st.spinner("正在匹配供应商..."):
                matched_suppliers = ai.match_suppliers(parsed, suppliers)

            if matched_suppliers:
                st.success(f"✅ 找到 {len(matched_suppliers)} 家匹配供应商")

                for idx, supplier in enumerate(matched_suppliers, 1):
                    with st.expander(f"**{idx}. {supplier['name']}** - 匹配度 {supplier['match_score']:.0f}%", expanded=(idx==1)):
                        col1, col2 = st.columns([2, 1])

                        with col1:
                            st.markdown("**匹配理由**")
                            for reason in supplier['match_reasons']:
                                st.markdown(f"- {reason}")

                            st.markdown(f"**联系方式**: {supplier.get('contact_person', '')} / {supplier.get('phone', '')}")
                            st.markdown(f"**价格等级**: {supplier.get('price_level', '中')}")
                            st.markdown(f"**备注**: {supplier.get('notes', '无')}")

                        with col2:
                            st.metric("质量评分", f"{supplier['quality_score']:.1f}/5.0")
                            st.metric("准时率", f"{supplier['on_time_rate']:.0f}%")

                            if st.button(f"📤 生成询价单", key=f"rfq_{supplier['id']}"):
                                rfq_content = ai.generate_rfq_content(parsed, supplier)
                                st.session_state[f'rfq_{supplier["id"]}'] = rfq_content

                            if f'rfq_{supplier["id"]}' in st.session_state:
                                st.download_button(
                                    label="💾 下载询价单",
                                    data=st.session_state[f'rfq_{supplier["id"]}'],
                                    file_name=f"询价单_{supplier['name']}_{datetime.now().strftime('%Y%m%d')}.txt",
                                    mime="text/plain",
                                    key=f"download_{supplier['id']}"
                                )

                # 保存需求按钮
                st.markdown("---")
                if st.button("💾 保存本次需求记录", type="primary"):
                    request_data = {
                        'request_title': st.session_state.request_title,
                        'raw_description': st.session_state.raw_description,
                        'parsed_data': parsed,
                        'part_type': parsed.get('part_type', ''),
                        'material': parsed.get('material', ''),
                        'process': parsed.get('process', ''),
                        'quantity': parsed.get('quantity', 0),
                        'delivery_date': parsed.get('delivery_urgency', '')
                    }

                    request_id = db.add_procurement_request(request_data)
                    st.success(f"✅ 需求已保存！ID: {request_id}")
            else:
                st.warning("未找到合适的供应商，请先添加供应商信息")
        else:
            st.warning("⚠️ 供应商库为空，请先在【供应商管理】中添加供应商")

# ==================== 页面3：供应商管理 ====================
elif page == "👥 供应商管理":
    st.title("👥 供应商管理")

    tab1, tab2 = st.tabs(["📋 供应商列表", "➕ 添加供应商"])

    with tab1:
        st.subheader("现有供应商")

        suppliers = db.get_all_suppliers()

        if suppliers:
            # 筛选器
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_capability = st.multiselect(
                    "按能力筛选",
                    options=["CNC加工", "3D打印", "钣金", "注塑", "铸造"],
                    default=[]
                )
            with col2:
                filter_quick = st.checkbox("仅显示快速打样")
            with col3:
                sort_by = st.selectbox("排序方式", ["质量评分", "准时率", "名称"])

            # 过滤和排序
            filtered = suppliers
            if filter_capability:
                filtered = [s for s in filtered if any(cap in s['capabilities'] for cap in filter_capability)]
            if filter_quick:
                filtered = [s for s in filtered if s['quick_sample']]

            # 显示供应商卡片
            for supplier in filtered:
                with st.expander(f"**{supplier['name']}** ({supplier['price_level']}价格)", expanded=False):
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.markdown("**基本信息**")
                        st.write(f"联系人: {supplier['contact_person']}")
                        st.write(f"电话: {supplier['phone']}")
                        st.write(f"微信: {supplier['wechat']}")

                    with col2:
                        st.markdown("**能力标签**")
                        for cap in supplier['capabilities']:
                            st.badge(cap)
                        st.write(f"起订量: {supplier['moq']} 件")
                        st.write(f"响应速度: {supplier['response_time']}")
                        if supplier['quick_sample']:
                            st.success("✓ 支持快速打样")

                    with col3:
                        st.markdown("**评价数据**")
                        st.metric("质量评分", f"{supplier['quality_score']:.1f}/5.0")
                        st.metric("准时率", f"{supplier['on_time_rate']:.0f}%")
                        if supplier['last_cooperation']:
                            st.write(f"最后合作: {supplier['last_cooperation']}")

                    if supplier['notes']:
                        st.info(f"备注: {supplier['notes']}")
        else:
            st.info("暂无供应商数据，请添加供应商信息")

    with tab2:
        st.subheader("添加新供应商")

        with st.form("add_supplier_form"):
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("供应商名称*", placeholder="例如：鑫达加工厂")
                contact_person = st.text_input("联系人", placeholder="张师傅")
                phone = st.text_input("电话", placeholder="138xxxx")
                wechat = st.text_input("微信号")

            with col2:
                capabilities = st.multiselect(
                    "擅长工艺*",
                    ["CNC加工", "3D打印", "钣金", "注塑", "铸造", "车床", "铣床", "激光切割"]
                )
                price_level = st.select_slider("价格等级", options=["低", "中", "高"], value="中")
                moq = st.number_input("最小起订量(MOQ)", min_value=1, value=5)
                response_time = st.selectbox("响应速度", ["30分钟内", "2小时内", "半天", "1天"])

            quick_sample = st.checkbox("支持快速打样")
            notes = st.text_area("备注", placeholder="例如：质量稳定但周末不接单")

            submitted = st.form_submit_button("💾 添加供应商", type="primary")

            if submitted:
                if name and capabilities:
                    supplier_data = {
                        'name': name,
                        'contact_person': contact_person,
                        'phone': phone,
                        'wechat': wechat,
                        'capabilities': capabilities,
                        'quick_sample': quick_sample,
                        'price_level': price_level,
                        'moq': moq,
                        'response_time': response_time,
                        'notes': notes
                    }

                    supplier_id = db.add_supplier(supplier_data)
                    st.success(f"✅ 供应商已添加！ID: {supplier_id}")
                    st.rerun()
                else:
                    st.error("请填写必填项：供应商名称和擅长工艺")

# ==================== 页面5：历史案例 ====================
elif page == "📚 历史案例":
    st.title("📚 历史案例检索")

    st.markdown("快速查找相似的历史采购案例")

    col1, col2 = st.columns([3, 1])

    with col1:
        search_keywords = st.text_input(
            "输入关键词搜索",
            placeholder="例如：铝合金 支架 CNC"
        )

    with col2:
        search_btn = st.button("🔍 搜索", type="primary", use_container_width=True)

    if search_btn and search_keywords:
        keywords = search_keywords.split()
        cases = db.search_similar_cases(keywords, limit=10)

        if cases:
            st.success(f"找到 {len(cases)} 个相似案例")

            for idx, case in enumerate(cases, 1):
                with st.expander(f"**案例{idx}: {case['case_title']}** - {case['created_at']}", expanded=(idx==1)):
                    st.markdown(f"**描述**: {case['description']}")
                    st.markdown(f"**供应商**: {case['supplier_name']}")
                    st.markdown(f"**报价信息**: {case['price_info']}")
                    st.markdown(f"**交期信息**: {case['delivery_info']}")
                    st.metric("质量评分", f"{case['quality_score']}/5")

                    if case['lessons_learned']:
                        st.warning(f"💡 经验教训: {case['lessons_learned']}")

                    if st.button(f"📋 复用此方案", key=f"reuse_{case['id']}"):
                        st.info("可跳转到需求解析页面，自动填充相似参数")
        else:
            st.warning("未找到相似案例")
    else:
        st.info("💡 试试搜索：铝合金、CNC、支架、3D打印等关键词")

        # 显示最近案例
        st.markdown("---")
        st.subheader("📌 最近案例")
        recent_cases = db.search_similar_cases([''], limit=5)
        if recent_cases:
            for case in recent_cases:
                st.markdown(f"- **{case['case_title']}** ({case['created_at']})")
        else:
            st.info("暂无历史案例，完成采购后可记录案例")

# 底部信息
st.sidebar.markdown("---")
st.sidebar.caption(f"© 2025 {config.SYSTEM_NAME}")
st.sidebar.caption("Powered by Streamlit + AI")
