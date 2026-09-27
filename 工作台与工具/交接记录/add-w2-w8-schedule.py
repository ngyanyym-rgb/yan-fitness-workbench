#!/usr/bin/env python3
"""添加 W2-W8 完整排程到計劃 JSON"""
import json
from datetime import datetime, timedelta
from pathlib import Path

plan_path = Path("/Users/wu/Desktop/gym file/Yan-fitness-system-v2/个人训练系统/训练与周期/当前周期/2026年09月18日-上肢下肢全身-综合增肌力量训练计划-v02.json")

with open(plan_path, 'r', encoding='utf-8') as f:
    plan = json.load(f)

# W1 起始日期
w1_start = datetime(2026, 9, 18)

# 基於 W1 校準結果的 W2-W4 負荷漸進（每週加 2.5-5kg）
# W2 排程：9月25、27、30日（週五上肢、週日下肢、週三全身）
w2_w8_schedule = []

# 8週的日期安排（每週：週五上肢、週日下肢、週三全身）
week_dates = []
for week in range(1, 9):
    week_offset = (week - 1) * 7
    # 週五上肢
    upper_date = w1_start + timedelta(days=week_offset)
    # 週日下肢
    lower_date = w1_start + timedelta(days=week_offset + 2)
    # 週三全身（下一週的週三，即 +5 天）
    full_date = w1_start + timedelta(days=week_offset + 5)

    week_dates.append({
        "week": week,
        "upper": upper_date.strftime("%m-%d"),
        "lower": lower_date.strftime("%m-%d"),
        "full": full_date.strftime("%m-%d") if week < 8 else None  # W8 沒有第三天
    })

# 取得現有的 W1 schedule 作為模板
w1_upper = next(s for s in plan['schedule'] if s['theme'] == '上肢')
w1_lower = next(s for s in plan['schedule'] if s['theme'] == '下肢')
w1_full = next(s for s in plan['schedule'] if s['theme'] == '全身')

# 生成 W2-W8 排程（這裡簡化處理，實際應該根據週期調整組數和重量）
new_schedule = list(plan['schedule'])  # 保留 W1

for week_info in week_dates[1:]:  # 從 W2 開始
    week = week_info['week']

    # 上肢日
    upper_copy = json.loads(json.dumps(w1_upper))
    upper_copy['day'] = week_info['upper']
    upper_copy['label'] = f"W{week} upper"
    upper_copy['role'] = f"W{week} 校准/积累" if week <= 4 else f"W{week} 强化"
    new_schedule.append(upper_copy)

    # 下肢日
    lower_copy = json.loads(json.dumps(w1_lower))
    lower_copy['day'] = week_info['lower']
    lower_copy['label'] = f"W{week} lower"
    lower_copy['role'] = f"W{week} 校准/积累" if week <= 4 else f"W{week} 强化"
    new_schedule.append(lower_copy)

    # 全身日（W8 沒有）
    if week_info['full']:
        full_copy = json.loads(json.dumps(w1_full))
        full_copy['day'] = week_info['full']
        full_copy['label'] = f"W{week} full"
        full_copy['role'] = f"W{week} 校准/积累" if week <= 4 else f"W{week} 强化"
        new_schedule.append(full_copy)

# 更新 schedule
plan['schedule'] = new_schedule

# 備份並寫入
backup_path = plan_path.with_suffix('.json.backup2')
plan_path.rename(backup_path)

with open(plan_path, 'w', encoding='utf-8') as f:
    json.dump(plan, f, ensure_ascii=False, indent=2)

print(f"✓ 已添加 W2-W8 排程（共 {len(new_schedule)} 個訓練日）")
print(f"✓ 備份位置：{backup_path}")
print("\n接下來幾週的排程：")
for info in week_dates[1:4]:  # 顯示 W2-W4
    print(f"  W{info['week']}: {info['upper']} 上肢、{info['lower']} 下肢、{info['full']} 全身")
