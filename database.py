# 数据库操作模块
import sqlite3
from datetime import datetime
import json
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)

    def init_database(self):
        """初始化数据库表"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 供应商表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact_person TEXT,
                phone TEXT,
                wechat TEXT,
                capabilities TEXT,  -- JSON格式存储能力标签
                quick_sample BOOLEAN,
                price_level TEXT,  -- 低/中/高
                moq INTEGER,  -- 最小起订量
                response_time TEXT,  -- 响应速度
                quality_score REAL DEFAULT 5.0,  -- 质量评分(1-5)
                on_time_rate REAL DEFAULT 100.0,  -- 准时率
                last_cooperation TEXT,  -- 最后合作时间
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 采购需求表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS procurement_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_title TEXT NOT NULL,
                raw_description TEXT,  -- 原始需求描述
                parsed_data TEXT,  -- AI解析后的结构化数据(JSON)
                part_type TEXT,  -- 零件类型
                material TEXT,  -- 材质
                process TEXT,  -- 加工工艺
                quantity INTEGER,
                delivery_date TEXT,
                budget REAL,
                status TEXT DEFAULT 'pending',  -- pending/processing/completed
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 采购订单表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS procurement_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id INTEGER,
                supplier_id INTEGER,
                quotation TEXT,  -- 报价详情(JSON)
                unit_price REAL,
                total_price REAL,
                delivery_days INTEGER,  -- 交期天数
                actual_delivery_days INTEGER,  -- 实际交期
                quality_rating INTEGER,  -- 质量评分(1-5)
                notes TEXT,
                status TEXT DEFAULT 'quoted',  -- quoted/ordered/delivered/completed
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT,
                FOREIGN KEY (request_id) REFERENCES procurement_requests(id),
                FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
            )
        ''')

        # 历史案例表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS case_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                case_title TEXT,
                description TEXT,
                keywords TEXT,  -- 关键词，用于搜索
                supplier_name TEXT,
                price_info TEXT,
                delivery_info TEXT,
                quality_score INTEGER,
                lessons_learned TEXT,  -- 经验教训
                attachments TEXT,  -- 附件路径(JSON)
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES procurement_orders(id)
            )
        ''')

        conn.commit()
        conn.close()

    # ===== 供应商管理 =====
    def add_supplier(self, supplier_data: Dict) -> int:
        """添加供应商"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO suppliers (name, contact_person, phone, wechat, capabilities,
                                 quick_sample, price_level, moq, response_time, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            supplier_data['name'],
            supplier_data.get('contact_person', ''),
            supplier_data.get('phone', ''),
            supplier_data.get('wechat', ''),
            json.dumps(supplier_data.get('capabilities', []), ensure_ascii=False),
            supplier_data.get('quick_sample', False),
            supplier_data.get('price_level', '中'),
            supplier_data.get('moq', 1),
            supplier_data.get('response_time', ''),
            supplier_data.get('notes', '')
        ))

        supplier_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return supplier_id

    def get_all_suppliers(self) -> List[Dict]:
        """获取所有供应商"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM suppliers ORDER BY quality_score DESC, on_time_rate DESC')
        rows = cursor.fetchall()

        suppliers = []
        for row in rows:
            supplier = {
                'id': row[0],
                'name': row[1],
                'contact_person': row[2],
                'phone': row[3],
                'wechat': row[4],
                'capabilities': json.loads(row[5]) if row[5] else [],
                'quick_sample': bool(row[6]),
                'price_level': row[7],
                'moq': row[8],
                'response_time': row[9],
                'quality_score': row[10],
                'on_time_rate': row[11],
                'last_cooperation': row[12],
                'notes': row[13]
            }
            suppliers.append(supplier)

        conn.close()
        return suppliers

    def update_supplier_score(self, supplier_id: int, quality_rating: int, on_time: bool):
        """更新供应商评分"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 获取当前评分
        cursor.execute('SELECT quality_score, on_time_rate FROM suppliers WHERE id = ?', (supplier_id,))
        current = cursor.fetchone()

        if current:
            # 简单的移动平均更新
            new_quality = (current[0] * 0.8 + quality_rating * 0.2)
            new_on_time = current[1] * 0.8 + (100 if on_time else 0) * 0.2

            cursor.execute('''
                UPDATE suppliers
                SET quality_score = ?, on_time_rate = ?, last_cooperation = ?
                WHERE id = ?
            ''', (new_quality, new_on_time, datetime.now().strftime('%Y-%m-%d'), supplier_id))

        conn.commit()
        conn.close()

    # ===== 采购需求管理 =====
    def add_procurement_request(self, request_data: Dict) -> int:
        """添加采购需求"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO procurement_requests (request_title, raw_description, parsed_data,
                                            part_type, material, process, quantity, delivery_date, budget)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            request_data['request_title'],
            request_data.get('raw_description', ''),
            json.dumps(request_data.get('parsed_data', {}), ensure_ascii=False),
            request_data.get('part_type', ''),
            request_data.get('material', ''),
            request_data.get('process', ''),
            request_data.get('quantity', 0),
            request_data.get('delivery_date', ''),
            request_data.get('budget', 0)
        ))

        request_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return request_id

    def get_recent_requests(self, limit: int = 10) -> List[Dict]:
        """获取最近的采购需求"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM procurement_requests
            ORDER BY created_at DESC LIMIT ?
        ''', (limit,))

        rows = cursor.fetchall()
        requests = []
        for row in rows:
            requests.append({
                'id': row[0],
                'request_title': row[1],
                'raw_description': row[2],
                'parsed_data': json.loads(row[3]) if row[3] else {},
                'part_type': row[4],
                'material': row[5],
                'process': row[6],
                'quantity': row[7],
                'delivery_date': row[8],
                'budget': row[9],
                'status': row[10],
                'created_at': row[11]
            })

        conn.close()
        return requests

    # ===== 订单管理 =====
    def add_order(self, order_data: Dict) -> int:
        """添加订单"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO procurement_orders (request_id, supplier_id, quotation, unit_price,
                                          total_price, delivery_days, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_data['request_id'],
            order_data['supplier_id'],
            json.dumps(order_data.get('quotation', {}), ensure_ascii=False),
            order_data.get('unit_price', 0),
            order_data.get('total_price', 0),
            order_data.get('delivery_days', 0),
            order_data.get('notes', '')
        ))

        order_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return order_id

    def complete_order(self, order_id: int, actual_days: int, quality_rating: int, notes: str = ''):
        """完成订单并更新评价"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 更新订单状态
        cursor.execute('''
            UPDATE procurement_orders
            SET actual_delivery_days = ?, quality_rating = ?, notes = ?,
                status = 'completed', completed_at = ?
            WHERE id = ?
        ''', (actual_days, quality_rating, notes, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), order_id))

        # 获取供应商ID和预期交期
        cursor.execute('SELECT supplier_id, delivery_days FROM procurement_orders WHERE id = ?', (order_id,))
        result = cursor.fetchone()

        if result:
            supplier_id, expected_days = result
            on_time = actual_days <= expected_days
            self.update_supplier_score(supplier_id, quality_rating, on_time)

        conn.commit()
        conn.close()

    # ===== 统计数据 =====
    def get_statistics(self) -> Dict:
        """获取统计数据"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 总需求数
        cursor.execute('SELECT COUNT(*) FROM procurement_requests')
        total_requests = cursor.fetchone()[0]

        # 本月需求数
        cursor.execute('''
            SELECT COUNT(*) FROM procurement_requests
            WHERE created_at >= date('now', 'start of month')
        ''')
        month_requests = cursor.fetchone()[0]

        # 供应商总数
        cursor.execute('SELECT COUNT(*) FROM suppliers')
        total_suppliers = cursor.fetchone()[0]

        # 平均质量评分
        cursor.execute('SELECT AVG(quality_score) FROM suppliers')
        avg_quality = cursor.fetchone()[0] or 0

        # 完成订单数
        cursor.execute('SELECT COUNT(*) FROM procurement_orders WHERE status = "completed"')
        completed_orders = cursor.fetchone()[0]

        # 平均交期
        cursor.execute('SELECT AVG(actual_delivery_days) FROM procurement_orders WHERE status = "completed"')
        avg_delivery = cursor.fetchone()[0] or 0

        conn.close()

        return {
            'total_requests': total_requests,
            'month_requests': month_requests,
            'total_suppliers': total_suppliers,
            'avg_quality': round(avg_quality, 2),
            'completed_orders': completed_orders,
            'avg_delivery_days': round(avg_delivery, 1)
        }

    # ===== 历史案例检索 =====
    def search_similar_cases(self, keywords: List[str], limit: int = 5) -> List[Dict]:
        """搜索相似历史案例"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 简单的关键词匹配
        search_pattern = '%' + '%'.join(keywords) + '%'
        cursor.execute('''
            SELECT * FROM case_history
            WHERE keywords LIKE ? OR description LIKE ?
            ORDER BY created_at DESC LIMIT ?
        ''', (search_pattern, search_pattern, limit))

        rows = cursor.fetchall()
        cases = []
        for row in rows:
            cases.append({
                'id': row[0],
                'case_title': row[2],
                'description': row[3],
                'supplier_name': row[5],
                'price_info': row[6],
                'delivery_info': row[7],
                'quality_score': row[8],
                'lessons_learned': row[9],
                'created_at': row[11]
            })

        conn.close()
        return cases
