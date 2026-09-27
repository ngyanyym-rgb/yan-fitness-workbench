#!/usr/bin/env python3
"""同步 W1 校準結果到計劃 JSON"""
import json
from pathlib import Path

# W1 校準結果（來自訓練復盤）
W1_CALIBRATION = {
    "upper": {  # 2026-09-18
        "藥球上拋|藥球胸前推擲": {"load": "4 kg", "sets": "3×5", "notes": "完成"},
        "槓鈴臥推": {"load": "45 kg", "sets": "40kg×8、45kg×7@8-9、45kg×6@9-10", "notes": "45kg可作工作負荷"},
        "引體向上|負重引體向上|下拉": {"load": "自重", "sets": "8、7@8-9、6@9-10", "notes": "自重可作工作負荷"},
        "槓鈴肩推|站姿推舉": {"load": "30 kg", "sets": "30kg×10、10@8-9、8@9-10", "notes": "30kg可作工作負荷"},
        "槓鈴划船|胸托划船|坐姿划船": {"load": "50 kg", "sets": "45kg×12@7-8、50kg×10@8-9、50kg×8@9-10", "notes": "50kg略高，下次降回45kg"},
        "啞鈴上斜臥推|上斜啞鈴臥推": {"load": "17.5 kg×2", "sets": "3×12@7-8", "notes": "17.5kg可作工作負荷"},
        "面拉|反向飛鳥|肩袖外旋": {"load": "輕重量", "sets": "未記錄", "notes": "未詳細記錄"},
        "槓鈴彎舉|啞鈴彎舉": {"load": "20 kg", "sets": "20kg×10@8-9×2", "notes": "20kg可作工作負荷"},
        "繩索下壓|肱三頭肌下壓": {"load": "中等重量", "sets": "未記錄", "notes": "未詳細記錄"},
        "側平舉": {"load": "輕重量", "sets": "未記錄", "notes": "未詳細記錄"},
    },
    "lower": {  # 2026-09-20
        "跳箱|增強式跳躍|垂直跳|箱跳": {"load": "體重", "sets": "3×5", "notes": "完成"},
        "後蹲|槓鈴後蹲": {"load": "60 kg", "sets": "40kg×10、50kg×10、60kg×10@7-8", "notes": "60kg可作工作負荷"},
        "保加利亞分腿蹲|分腿蹲": {"load": "15 kg×2", "sets": "15kg×10×3@7-8", "notes": "15kg可作工作負荷"},
        "羅馬尼亞硬拉|RDL": {"load": "60 kg", "sets": "40kg×12、50kg×10、60kg×10@8-9", "notes": "60kg可作工作負荷"},
        "腿彎舉": {"load": "27.5 kg", "sets": "20kg×15、25kg×15@8-9、27.5kg×12@9-10", "notes": "末組達RPE 9-10，下次降低"},
        "站姿提踵|提踵": {"load": "60 kg", "sets": "60kg×15×3@7-8", "notes": "60kg可作工作負荷"},
        "哥本哈根側橋|哥本哈根支撐": {"load": "體重", "sets": "20秒×3@9-10", "notes": "強度過高，下次降至15秒"},
        "Pallof抗旋轉|Pallof": {"load": "輕重量", "sets": "12次×2", "notes": "完成"},
        "死蟲": {"load": "體重", "sets": "未記錄", "notes": "完成"},
    },
    "full": {  # 2026-09-24
        "懸垂高翻技術|高翻拉": {"load": "45 kg", "sets": "40kg×2、45kg×2×3", "notes": "45kg可作工作負荷"},
        "傳統硬拉|硬拉": {"load": "70 kg", "sets": "60kg×5、70kg×5@7-8×2", "notes": "70kg可作工作負荷"},
        "站姿推舉|肩推": {"load": "32.5 kg", "sets": "30kg×8、35kg×8@7-8、35kg×7@9-10", "notes": "35kg第3組達RPE 9-10，下次降回32.5kg"},
        "頸前深蹲|前蹲|腿舉": {"load": "50 kg", "sets": "40kg×10、50kg×10@7-8", "notes": "50kg可作工作負荷"},
        "高位下拉|單臂啞鈴划船": {"load": "52.5 kg", "sets": "42.5kg×12、50kg×12、52.5kg×12@8-9", "notes": "52.5kg可作工作負荷"},
        "雙槓臂屈伸|器械推胸": {"load": "彈力帶輔助", "sets": "12@7-8×2", "notes": "維持相同彈力帶"},
        "農夫行走": {"load": "未執行", "sets": "未執行", "notes": "時間不足"},
        "反向飛鳥": {"load": "輕重量", "sets": "未記錄", "notes": "未詳細記錄"},
    }
}

def main():
    plan_path = Path("/Users/wu/Desktop/gym file/Yan-fitness-system-v2/个人训练系统/训练与周期/当前周期/2026年09月18日-上肢下肢全身-综合增肌力量训练计划-v02.json")

    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = json.load(f)

    # 更新 schedule 中的 load_status
    for session in plan.get("schedule", []):
        day_key = None
        day = session.get("day", "")
        exercises = session.get("exercises", [])

        # 根據日期判斷是哪一天
        if day == "09-18":
            day_key = "upper"
        elif day == "09-20":
            day_key = "lower"
        elif day == "09-23":
            day_key = "full"

        if day_key and day_key in W1_CALIBRATION:
            calibration = W1_CALIBRATION[day_key]
            for exercise in exercises:
                name = exercise.get("name", "")
                # 模糊匹配動作名稱 - 支持 "|" 分隔的多個別名
                matched_load = None
                for calib_names, calib_data in calibration.items():
                    # calib_names 可能包含多個用 "|" 分隔的別名
                    aliases = [alias.strip() for alias in calib_names.split("|")]
                    # 檢查動作名稱是否包含任一別名
                    if any(alias in name for alias in aliases):
                        matched_load = calib_data
                        break

                if matched_load and exercise.get("load_status") == "calibration_required":
                    exercise["load_status"] = "observed_load"
                    exercise["observed_load"] = matched_load["load"]
                    exercise["calibration_notes"] = matched_load["notes"]

    # 更新 training_days 中的 load.status
    for day in plan.get("training_days", []):
        day_key = None
        if "upper" in day.get("label", "").lower() or "上肢" in day.get("theme", ""):
            day_key = "upper"
        elif "lower" in day.get("label", "").lower() or "下肢" in day.get("theme", ""):
            day_key = "lower"
        elif "full" in day.get("label", "").lower() or "全身" in day.get("theme", ""):
            day_key = "full"

        if day_key and day_key in W1_CALIBRATION:
            calibration = W1_CALIBRATION[day_key]
            for exercise in day.get("exercises", []):
                name = exercise.get("name", "")
                matched_load = None
                for calib_names, calib_data in calibration.items():
                    aliases = [alias.strip() for alias in calib_names.split("|")]
                    if any(alias in name for alias in aliases):
                        matched_load = calib_data
                        break

                if matched_load and exercise.get("load", {}).get("status") == "calibration_required":
                    exercise["load"]["status"] = "observed_load"
                    exercise["load"]["observed_value"] = matched_load["load"]
                    exercise["load"]["calibration_notes"] = matched_load["notes"]

    # 寫回檔案
    backup_path = plan_path.with_suffix('.json.backup')
    plan_path.rename(backup_path)

    with open(plan_path, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    print(f"✓ 已更新計劃檔案")
    print(f"✓ 備份位置：{backup_path}")

if __name__ == "__main__":
    main()
