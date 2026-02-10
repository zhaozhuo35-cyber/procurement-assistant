# AI助手模块
import json
import re
from typing import Dict, List, Optional

class AIHelper:
    """AI助手类，处理需求解析和智能推荐"""

    def __init__(self, api_key: str = "", api_url: str = ""):
        self.api_key = api_key
        self.api_url = api_url
        self.has_api = bool(api_key)

    def parse_requirement(self, raw_description: str, image_data: Optional[str] = None) -> Dict:
        """
        解析采购需求
        如果有API key，调用AI API；否则使用规则解析
        """
        if self.has_api and self.api_key:
            return self._ai_parse(raw_description, image_data)
        else:
            return self._rule_based_parse(raw_description)

    def _rule_based_parse(self, description: str) -> Dict:
        """基于规则的需求解析（不依赖API）"""
        result = {
            'part_type': '',
            'material': '',
            'process': '',
            'quantity': 0,
            'delivery_urgency': '',
            'surface_treatment': '',
            'missing_info': [],
            'parsed_success': True
        }

        desc_lower = description.lower()

        # 材质识别
        materials = {
            '铝合金': ['铝合金', '铝', '6061', '7075', 'aluminum'],
            '不锈钢': ['不锈钢', '304', '316', 'stainless'],
            '塑料': ['塑料', 'abs', 'pc', 'pvc', 'plastic'],
            '铜': ['铜', '黄铜', '紫铜', 'copper'],
            '钢': ['钢', 'steel', '碳钢']
        }
        for mat, keywords in materials.items():
            if any(kw in desc_lower for kw in keywords):
                result['material'] = mat
                break

        # 工艺识别
        processes = {
            'CNC加工': ['cnc', '加工', '铣', '车'],
            '3D打印': ['3d打印', '打印', '3d'],
            '钣金': ['钣金', '折弯', '冲压'],
            '注塑': ['注塑', '模具'],
            '铸造': ['铸造', '铸件']
        }
        for proc, keywords in processes.items():
            if any(kw in desc_lower for kw in keywords):
                result['process'] = proc
                break

        # 零件类型识别
        part_types = {
            '支架': ['支架', 'bracket'],
            '外壳': ['外壳', '壳体', 'housing', 'case'],
            '连接件': ['连接', '接头', 'connector'],
            '紧固件': ['螺丝', '螺栓', '螺母', 'screw', 'bolt'],
            '结构件': ['结构', '框架', 'frame']
        }
        for ptype, keywords in part_types.items():
            if any(kw in desc_lower for kw in keywords):
                result['part_type'] = ptype
                break

        # 数量识别
        quantity_pattern = r'(\d+)\s*件'
        match = re.search(quantity_pattern, description)
        if match:
            result['quantity'] = int(match.group(1))

        # 交期紧急度
        urgency_keywords = {
            '紧急': ['紧急', '急', '马上', '立刻', '今天', '明天'],
            '正常': ['下周', '本周', '这周'],
            '不急': ['下月', '不急']
        }
        for urgency, keywords in urgency_keywords.items():
            if any(kw in desc_lower for kw in keywords):
                result['delivery_urgency'] = urgency
                break

        # 表面处理
        surface_treatments = {
            '阳极氧化': ['阳极', '氧化'],
            '喷砂': ['喷砂'],
            '抛光': ['抛光'],
            '喷漆': ['喷漆', '喷涂'],
            '电镀': ['电镀', '镀']
        }
        for treatment, keywords in surface_treatments.items():
            if any(kw in desc_lower for kw in keywords):
                result['surface_treatment'] = treatment
                break

        # 检查缺失信息
        if not result['material']:
            result['missing_info'].append('材质规格')
        if not result['quantity'] or result['quantity'] == 0:
            result['missing_info'].append('精确数量')
        if not result['process']:
            result['missing_info'].append('加工工艺')
        if not result['surface_treatment']:
            result['missing_info'].append('表面处理要求')
        if not result['delivery_urgency']:
            result['missing_info'].append('具体交期')

        return result

    def _ai_parse(self, description: str, image_data: Optional[str] = None) -> Dict:
        """使用AI API解析需求（需要配置API key）"""
        try:
            import requests

            prompt = f"""
请分析以下采购需求，提取关键信息：

需求描述：{description}

请以JSON格式返回，包含以下字段：
- part_type: 零件类型
- material: 材质
- process: 加工工艺
- quantity: 数量
- delivery_urgency: 交期紧急度（紧急/正常/不急）
- surface_treatment: 表面处理
- missing_info: 缺失的关键信息列表

只返回JSON，不要其他内容。
"""

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            data = {
                "model": "moonshot-v1-8k",
                "messages": [
                    {"role": "system", "content": "你是一个专业的采购助手，擅长分析采购需求。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3
            }

            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                # 提取JSON
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group())
                    parsed['parsed_success'] = True
                    return parsed

            # API调用失败，回退到规则解析
            return self._rule_based_parse(description)

        except Exception as e:
            print(f"AI解析失败: {e}，使用规则解析")
            return self._rule_based_parse(description)

    def match_suppliers(self, requirement: Dict, suppliers: List[Dict]) -> List[Dict]:
        """
        匹配合适的供应商
        返回排序后的供应商列表，包含匹配度评分
        """
        scored_suppliers = []

        for supplier in suppliers:
            score = self._calculate_match_score(requirement, supplier)
            if score > 0:
                supplier_copy = supplier.copy()
                supplier_copy['match_score'] = score
                supplier_copy['match_reasons'] = self._get_match_reasons(requirement, supplier)
                scored_suppliers.append(supplier_copy)

        # 按匹配度排序
        scored_suppliers.sort(key=lambda x: x['match_score'], reverse=True)
        return scored_suppliers[:5]  # 返回前5个

    def _calculate_match_score(self, requirement: Dict, supplier: Dict) -> float:
        """计算供应商匹配度评分（0-100）"""
        score = 0.0

        # 能力匹配 (40分)
        required_process = requirement.get('process', '')
        capabilities = supplier.get('capabilities', [])

        if required_process:
            if required_process in capabilities:
                score += 40
            elif any(proc in required_process for proc in capabilities):
                score += 20

        # 起订量匹配 (15分)
        required_qty = requirement.get('quantity', 0)
        moq = supplier.get('moq', 1)
        if required_qty >= moq:
            score += 15
        elif required_qty > 0:
            score += 15 * (required_qty / moq)

        # 交期匹配 (20分)
        urgency = requirement.get('delivery_urgency', '')
        quick_sample = supplier.get('quick_sample', False)
        if urgency == '紧急' and quick_sample:
            score += 20
        elif urgency != '紧急':
            score += 15

        # 质量评分 (15分)
        quality_score = supplier.get('quality_score', 3.0)
        score += (quality_score / 5.0) * 15

        # 准时率 (10分)
        on_time_rate = supplier.get('on_time_rate', 80.0)
        score += (on_time_rate / 100.0) * 10

        return round(score, 1)

    def _get_match_reasons(self, requirement: Dict, supplier: Dict) -> List[str]:
        """获取匹配原因"""
        reasons = []

        # 能力匹配
        required_process = requirement.get('process', '')
        capabilities = supplier.get('capabilities', [])
        if required_process in capabilities:
            reasons.append(f"✓ 擅长{required_process}")

        # 快速打样
        if supplier.get('quick_sample') and requirement.get('delivery_urgency') == '紧急':
            reasons.append("✓ 快速打样能力")

        # 质量评分
        quality = supplier.get('quality_score', 0)
        if quality >= 4.5:
            reasons.append(f"✓ 高质量评分({quality:.1f}/5.0)")
        elif quality >= 4.0:
            reasons.append(f"✓ 质量可靠({quality:.1f}/5.0)")

        # 起订量
        required_qty = requirement.get('quantity', 0)
        moq = supplier.get('moq', 1)
        if moq <= required_qty:
            reasons.append(f"✓ 起订量{moq}件（符合要求）")
        else:
            reasons.append(f"✗ 起订量{moq}件（需{required_qty}件）")

        # 准时率
        on_time = supplier.get('on_time_rate', 0)
        if on_time >= 95:
            reasons.append(f"✓ 准时率{on_time:.0f}%")

        return reasons

    def generate_rfq_content(self, requirement: Dict, supplier: Dict) -> str:
        """生成询价单内容"""
        rfq = f"""
询价单

致：{supplier.get('name', '')}
联系人：{supplier.get('contact_person', '')}

我司有以下采购需求，请报价：

【零件信息】
零件类型：{requirement.get('part_type', '待确认')}
材质：{requirement.get('material', '待确认')}
加工工艺：{requirement.get('process', '待确认')}
表面处理：{requirement.get('surface_treatment', '待确认')}
数量：{requirement.get('quantity', 0)} 件

【交期要求】
期望交期：{requirement.get('delivery_urgency', '待确认')}

【其他说明】
{requirement.get('notes', '详见附件图纸')}

请提供：
1. 单价及总价
2. 交期（工作日）
3. 付款方式
4. 质保条件

期待您的回复！
"""
        return rfq.strip()

    def generate_requirement_checklist(self, parsed_data: Dict) -> str:
        """生成需求确认清单"""
        checklist = f"""
需求确认清单

【已识别信息】
"""
        if parsed_data.get('part_type'):
            checklist += f"✓ 零件类型：{parsed_data['part_type']}\n"
        if parsed_data.get('material'):
            checklist += f"✓ 材质：{parsed_data['material']}\n"
        if parsed_data.get('process'):
            checklist += f"✓ 工艺：{parsed_data['process']}\n"
        if parsed_data.get('quantity'):
            checklist += f"✓ 数量：{parsed_data['quantity']} 件\n"
        if parsed_data.get('surface_treatment'):
            checklist += f"✓ 表面处理：{parsed_data['surface_treatment']}\n"
        if parsed_data.get('delivery_urgency'):
            checklist += f"✓ 交期：{parsed_data['delivery_urgency']}\n"

        if parsed_data.get('missing_info'):
            checklist += f"\n【需补充信息】\n"
            for info in parsed_data['missing_info']:
                checklist += f"• {info}：__________\n"

        checklist += "\n【其他要求】\n• 公差等级：__________\n• 预算范围：__________\n• 特殊要求：__________\n"

        return checklist.strip()
