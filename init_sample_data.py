# 初始化示例数据
# 运行此脚本可以快速添加示例供应商数据，用于演示

from database import Database
import config

def init_sample_data():
    """初始化示例数据"""
    db = Database(config.DATABASE_PATH)

    print("开始添加示例供应商数据...")

    # 示例供应商数据
    sample_suppliers = [
        {
            'name': '鑫达精密加工厂',
            'contact_person': '张师傅',
            'phone': '138-1234-5678',
            'wechat': 'zhangshifu123',
            'capabilities': ['CNC加工', '钣金'],
            'quick_sample': True,
            'price_level': '中',
            'moq': 5,
            'response_time': '2小时内',
            'notes': '质量稳定，但周末不接单'
        },
        {
            'name': '速成3D打印工作室',
            'contact_person': '李总',
            'phone': '139-8765-4321',
            'wechat': 'li3dprint',
            'capabilities': ['3D打印'],
            'quick_sample': True,
            'price_level': '高',
            'moq': 1,
            'response_time': '30分钟内',
            'notes': '价格偏高但速度快，紧急情况首选'
        },
        {
            'name': '精工制造有限公司',
            'contact_person': '王经理',
            'phone': '135-2468-1357',
            'wechat': 'wangjinggong',
            'capabilities': ['CNC加工', '车床', '铣床'],
            'quick_sample': False,
            'price_level': '低',
            'moq': 20,
            'response_time': '1天',
            'notes': '价格优惠，适合批量，起订量较高'
        },
        {
            'name': '华通钣金加工',
            'contact_person': '赵师傅',
            'phone': '136-9876-5432',
            'wechat': 'zhaobanjin',
            'capabilities': ['钣金', '激光切割', '折弯'],
            'quick_sample': True,
            'price_level': '中',
            'moq': 10,
            'response_time': '2小时内',
            'notes': '钣金专业，配套焊接服务'
        },
        {
            'name': '众诚注塑模具厂',
            'contact_person': '刘工',
            'phone': '137-3456-7890',
            'wechat': 'liuzhushu',
            'capabilities': ['注塑', '模具'],
            'quick_sample': False,
            'price_level': '中',
            'moq': 100,
            'response_time': '半天',
            'notes': '需要开模，适合量产'
        },
        {
            'name': '锐速激光切割',
            'contact_person': '陈师傅',
            'phone': '138-5678-1234',
            'wechat': 'chenruisu',
            'capabilities': ['激光切割', '钣金'],
            'quick_sample': True,
            'price_level': '中',
            'moq': 5,
            'response_time': '2小时内',
            'notes': '激光切割速度快，精度高'
        },
        {
            'name': '铭创CNC加工中心',
            'contact_person': '孙总',
            'phone': '139-6789-2345',
            'wechat': 'sunmingchuang',
            'capabilities': ['CNC加工', '车床'],
            'quick_sample': True,
            'price_level': '中',
            'moq': 10,
            'response_time': '半天',
            'notes': '五轴加工，可处理复杂零件'
        },
        {
            'name': '飞扬铸造厂',
            'contact_person': '周师傅',
            'phone': '135-7890-3456',
            'wechat': 'zhouzhuzao',
            'capabilities': ['铸造'],
            'quick_sample': False,
            'price_level': '低',
            'moq': 50,
            'response_time': '1天',
            'notes': '适合铸件，交期较长'
        }
    ]

    # 添加供应商
    count = 0
    for supplier in sample_suppliers:
        try:
            supplier_id = db.add_supplier(supplier)
            print(f"✓ 已添加: {supplier['name']} (ID: {supplier_id})")
            count += 1
        except Exception as e:
            print(f"✗ 添加失败: {supplier['name']} - {e}")

    print(f"\n完成！共添加 {count}/{len(sample_suppliers)} 家供应商")
    print("\n现在可以启动系统进行演示了！")
    print("运行命令: streamlit run app.py")

if __name__ == "__main__":
    init_sample_data()
