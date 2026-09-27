#!/usr/bin/env python3
"""將計劃從 W1 更新到 W2"""
import json
from pathlib import Path

plan_path = Path("/Users/wu/Desktop/gym file/Yan-fitness-system-v2/个人训练系统/训练与周期/当前周期/2026年09月18日-上肢下肢全身-综合增肌力量训练计划-v02.json")

with open(plan_path, 'r', encoding='utf-8') as f:
    plan = json.load(f)

# 取得 W1 的三個訓練日作為模板
w1_schedule = plan['schedule']
w1_upper = next(s for s in w1_schedule if '上肢' in s.get('theme', ''))
w1_lower = next(s for s in w1_schedule if '下肢' in s.get('theme', ''))
w1_full = next(s for s in w1_schedule if '全身' in s.get('theme', ''))

# 創建 W2 排程（完全替換 W1）
w2_schedule = []

# W2 上肢：9月25日（週五）
w2_upper = json.loads(json.dumps(w1_upper))
w2_upper['day'] = '09-25'
w2_upper['label'] = 'W2 upper'
w2_upper['role'] = 'W2 校准/积累'
w2_schedule.append(w2_upper)

# W2 下肢：9月27日（週日）
w2_lower = json.loads(json.dumps(w1_lower))
w2_lower['day'] = '09-27'
w2_lower['label'] = 'W2 lower'
w2_lower['role'] = 'W2 校准/积累'
w2_schedule.append(w2_lower)

# W2 全身：9月30日（週三）
w2_full = json.loads(json.dumps(w1_full))
w2_full['day'] = '09-30'
w2_full['label'] = 'W2 full'
w2_full['role'] = 'W2 校准/积累'
w2_schedule.append(w2_full)

# 更新計劃
plan['schedule'] = w2_schedule

# 備份
backup_path = plan_path.with_suffix('.json.w1-backup')
with open(backup_path, 'w', encoding='utf-8') as f:
    # 先保存 W1 版本
    original_plan = json.load(open(plan_path, 'r', encoding='utf-8'))
    json.dump(original_plan, f, ensure_ascii=False, indent=2)

# 寫入 W2 版本
with open(plan_path, 'w', encoding='utf-8') as f:
    json.dump(plan, f, ensure_ascii=False, indent=2)

print("✓ 已將計劃更新為 W2")
print(f"✓ W1 版本備份：{backup_path}")
print("\nW2 排程：")
print(f"  09-25（週五）：上肢")
print(f"  09-27（週日）：下肢")
print(f"  09-30（週三）：全身")
print("\n所有動作的 observed_load 已保留（來自 W1 校準）")
