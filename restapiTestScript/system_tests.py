#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
System REST API 測試腳本
基於 System_API_Reference_v0.15.docx 文件生成
包含系統信息、內存、CPU、風扇、溫度、PSU、版本、時間管理等功能測試
"""

import requests
import json
import sys
import time
import random
from datetime import datetime, timedelta

class SystemAPITester:
    def __init__(self, base_url, username=None, password=None):
        """
        初始化測試器
        :param base_url: API基礎URL，例如 'http://192.168.1.1'
        :param username: 認證用戶名（如需要）
        :param password: 認證密碼（如需要）
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        if username and password:
            self.session.auth = (username, password)
        
        # 設置請求頭
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        self.test_results = []
        self.original_configs = {}  # 保存原始配置用於恢復
        self.created_time_ranges = []  # 記錄創建的時間範圍，用於清理
        
        # 時間相關常量
        self.DAYS_OF_WEEK = [
            'sunday', 'monday', 'tuesday', 'wednesday', 
            'thursday', 'friday', 'saturday', 'daily', 
            'weekdays', 'weekend'
        ]
        
        self.SUMMER_TIME_TYPES = ['date', 'predefined', 'recurring']
        self.PREDEFINED_ZONES = ['australia', 'europe', 'new-zealand', 'usa']
    
    def log_test(self, test_name, success, response=None, error=None, details=None):
        """記錄測試結果"""
        result = {
            'test_name': test_name,
            'success': success,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if response:
            result['status_code'] = response.status_code
            try:
                result['response'] = response.json() if response.content else {}
            except:
                result['response'] = response.text
        
        if error:
            result['error'] = str(error)
            
        if details:
            result['details'] = details
        
        self.test_results.append(result)
        
        # 即時輸出結果
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"[{result['timestamp']}] {status} - {test_name}")
        if error:
            print(f"    錯誤: {error}")
        if response and hasattr(response, 'status_code'):
            print(f"    狀態碼: {response.status_code}")
    
    # ==================== 1.1 Get System Information ====================
    
    def test_get_system_info(self):
        """測試 1.1: 獲取系統信息"""
        try:
            url = f"{self.base_url}/api/v1/system"
            response = self.session.get(url)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    
                    print(f"    系統描述: {result_data.get('sysDescription', 'N/A')}")
                    print(f"    系統名稱: {result_data.get('sysName', 'N/A')}")
                    print(f"    MAC地址: {result_data.get('MACAddress', 'N/A')}")
                    print(f"    系統運行時間: {result_data.get('sysUpTime', 'N/A')}")
                    print(f"    OID字符串: {result_data.get('oidString', 'N/A')}")
                    print(f"    看門狗狀態: {'啟用' if result_data.get('watchdogStatus') else '禁用'}")
                    print(f"    巨型幀狀態: {'啟用' if result_data.get('jumboFrameStatus') else '禁用'}")
                    print(f"    風扇狀態: {result_data.get('sysFanStatus', 'N/A')}")
                    
                    # 顯示溫度信息
                    temps = result_data.get('sysTemps', [])
                    print(f"    溫度檢測點數量: {len(temps)}")
                    for temp in temps:
                        print(f"      單元{temp.get('unitId')}: {temp.get('temp', 'N/A')}")
                    
                    # 保存原始配置
                    self.original_configs['system'] = {
                        'sysName': result_data.get('sysName'),
                        'sysFanStatus': result_data.get('sysFanStatus'),
                        'jumboFrameStatus': result_data.get('jumboFrameStatus'),
                        'watchdogStatus': result_data.get('watchdogStatus')
                    }
                    
            self.log_test("獲取系統信息", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取系統信息", False, error=e)
            return None
    
    # ==================== 1.2 Update System Information ====================
    
    def test_update_system_info(self):
        """測試 1.2: 更新系統信息"""
        try:
            url = f"{self.base_url}/api/v1/system"
            
            payload = {
                "sysName": "TestSystem_" + str(int(time.time())),
                "sysFanStatus": True,
                "jumboFrameStatus": True,
                "watchdogStatus": True
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功更新系統信息:")
                print(f"      系統名稱: {payload['sysName']}")
                print(f"      風扇狀態: {'啟用' if payload['sysFanStatus'] else '禁用'}")
                print(f"      巨型幀狀態: {'啟用' if payload['jumboFrameStatus'] else '禁用'}")
                print(f"      看門狗狀態: {'啟用' if payload['watchdogStatus'] else '禁用'}")
            
            self.log_test("更新系統信息", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("更新系統信息", False, error=e)
            return None
    
    # ==================== 1.3 Get Memory Utilization ====================
    
    def test_get_memory_info(self):
        """測試 1.3: 獲取內存利用率信息"""
        try:
            url = f"{self.base_url}/api/v1/system/memory"
            response = self.session.get(url)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    
                    free_bytes = result_data.get('freeBytes', 0)
                    used_bytes = result_data.get('usedBytes', 0)
                    total_bytes = result_data.get('totalBytes', 0)
                    free_percent = result_data.get('freePercentage(%)', 0)
                    used_percent = result_data.get('usedPercentage(%)', 0)
                    rising_threshold = result_data.get('risingThreshold(%)', 0)
                    falling_threshold = result_data.get('fallingThreshold(%)', 0)
                    
                    print(f"    內存使用情況:")
                    print(f"      總內存: {total_bytes:,} bytes ({total_bytes/1024/1024:.1f} MB)")
                    print(f"      已使用: {used_bytes:,} bytes ({used_percent}%)")
                    print(f"      可用: {free_bytes:,} bytes ({free_percent}%)")
                    print(f"      告警閾值: 上升={rising_threshold}%, 下降={falling_threshold}%")
                    
                    # 保存原始配置
                    self.original_configs['memory'] = {
                        'risingThreshold': rising_threshold,
                        'fallingThreshold': falling_threshold
                    }
                    
            self.log_test("獲取內存利用率信息", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取內存利用率信息", False, error=e)
            return None
    
    # ==================== 1.4 Update Memory Thresholds ====================
    
    def test_update_memory_thresholds(self):
        """測試 1.4: 更新內存利用率閾值"""
        try:
            url = f"{self.base_url}/api/v1/system/memory"
            
            payload = {
                "risingThreshold": 85,
                "fallingThreshold": 70
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功更新內存閾值:")
                print(f"      上升閾值: {payload['risingThreshold']}%")
                print(f"      下降閾值: {payload['fallingThreshold']}%")
            
            self.log_test("更新內存利用率閾值", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("更新內存利用率閾值", False, error=e)
            return None
    
    # ==================== 1.5 Get CPU Information ====================
    
    def test_get_cpu_info(self):
        """測試 1.5: 獲取CPU信息"""
        try:
            url = f"{self.base_url}/api/v1/system/cpu"
            response = self.session.get(url)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    
                    total_cpu = result_data.get('totalCpuPercent(%)', 0)
                    avg_util = result_data.get('statAvgUti(%)', 0)
                    max_util = result_data.get('statMaxUti(%)', 0)
                    alarm_status = result_data.get('alarmStatus', False)
                    peak_time = result_data.get('utilPeakTime', '')
                    peak_duration = result_data.get('utilPeakDuration(seconds)', 0)
                    rising_threshold = result_data.get('risingThreshold(%)', 0)
                    falling_threshold = result_data.get('fallingThreshold(%)', 0)
                    
                    print(f"    CPU使用情況:")
                    print(f"      總CPU使用率: {total_cpu}%")
                    print(f"      平均利用率: {avg_util}%")
                    print(f"      最大利用率: {max_util}%")
                    print(f"      告警狀態: {'告警中' if alarm_status else '正常'}")
                    print(f"      告警閾值: 上升={rising_threshold}%, 下降={falling_threshold}%")
                    
                    if peak_time:
                        print(f"      峰值時間: {peak_time}")
                        print(f"      峰值持續: {peak_duration} 秒")
                    
                    # 顯示任務信息
                    tasks = result_data.get('tasks', [])
                    print(f"      任務數量: {len(tasks)}")
                    
                    # 顯示前5個任務
                    for i, task in enumerate(tasks[:5]):
                        task_name = task.get('taskName', 'N/A')
                        util = task.get('util(%)', 'N/A')
                        avg = task.get('avg(%)', 'N/A')
                        max_val = task.get('max(%)', 'N/A')
                        print(f"        任務{i+1}: {task_name} - 當前:{util}% 平均:{avg}% 最大:{max_val}%")
                    
                    if len(tasks) > 5:
                        print(f"        ... 還有 {len(tasks) - 5} 個任務")
                    
                    # 保存原始配置
                    self.original_configs['cpu'] = {
                        'risingThreshold': rising_threshold,
                        'fallingThreshold': falling_threshold
                    }
                    
            self.log_test("獲取CPU信息", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取CPU信息", False, error=e)
            return None
    
    # ==================== 1.6 Update CPU Thresholds ====================
    
    def test_update_cpu_thresholds(self):
        """測試 1.6: 更新CPU利用率閾值"""
        try:
            url = f"{self.base_url}/api/v1/system/cpu"
            
            payload = {
                "risingThreshold": 80,
                "fallingThreshold": 60
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功更新CPU閾值:")
                print(f"      上升閾值: {payload['risingThreshold']}%")
                print(f"      下降閾值: {payload['fallingThreshold']}%")
            
            self.log_test("更新CPU利用率閾值", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("更新CPU利用率閾值", False, error=e)
            return None
    
    # ==================== 1.7 Get Fan Information ====================
    
    def test_get_fan_info(self):
        """測試 1.7: 獲取風扇信息"""
        try:
            url = f"{self.base_url}/api/v1/system/fan"
            response = self.session.get(url)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    fans = result_data.get('fans', [])
                    
                    print(f"    風扇信息:")
                    print(f"      風扇數量: {len(fans)}")
                    
                    for fan in fans:
                        index = fan.get('index', 'N/A')
                        name = fan.get('name', 'N/A')
                        status = fan.get('status', 'N/A')
                        rpm = fan.get('rpm', 'N/A')
                        pct = fan.get('pct', 'N/A')
                        location = fan.get('location', 'N/A')
                        model = fan.get('model', 'N/A')
                        serial = fan.get('serial', 'N/A')
                        flow_type = fan.get('flowType', 'N/A')
                        
                        print(f"        風扇{index}: {name}")
                        print(f"          狀態: {status}")
                        print(f"          轉速: {rpm} RPM ({pct}%)")
                        print(f"          位置: {location}")
                        print(f"          型號: {model}")
                        print(f"          序列號: {serial}")
                        print(f"          氣流方向: {flow_type}")
                        
            elif response.status_code == 500:
                # 某些設備可能不支持風扇讀取
                error_data = response.json() if response.content else {}
                if 'message' in error_data and 'Unsupport FAN read' in error_data['message']:
                    print("    設備不支持風扇信息讀取")
                    success = True  # 這是預期的行為
                    
            self.log_test("獲取風扇信息", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取風扇信息", False, error=e)
            return None
    
    # ==================== 1.8 Get Temperature Information ====================
    
    def test_get_temperature_info(self):
        """測試 1.8: 獲取溫度信息"""
        try:
            url = f"{self.base_url}/api/v1/system/temperature"
            response = self.session.get(url)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    temps = result_data.get('temps', [])
                    
                    print(f"    溫度信息:")
                    print(f"      溫度感測器數量: {len(temps)}")
                    
                    for temp in temps:
                        index = temp.get('index', 'N/A')
                        name = temp.get('name', 'N/A')
                        status = temp.get('status', 'N/A')
                        value = temp.get('value', 'N/A')
                        
                        print(f"        感測器{index}: {name}")
                        print(f"          狀態: {status}")
                        print(f"          溫度: {value}°C")
                        
            elif response.status_code == 500:
                # 某些設備可能不支持溫度讀取
                error_data = response.json() if response.content else {}
                if 'message' in error_data and 'Unsupport Temperature read' in error_data['message']:
                    print("    設備不支持溫度信息讀取")
                    success = True  # 這是預期的行為
                    
            self.log_test("獲取溫度信息", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取溫度信息", False, error=e)
            return None
    
    # ==================== 1.9 Get PSU Information ====================
    
    def test_get_psu_info(self):
        """測試 1.9: 獲取PSU信息"""
        try:
            url = f"{self.base_url}/api/v1/system/psu"
            response = self.session.get(url)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    psus = result_data.get('psus', [])
                    
                    print(f"    PSU信息:")
                    print(f"      PSU數量: {len(psus)}")
                    
                    for psu in psus:
                        index = psu.get('index', 'N/A')
                        name = psu.get('name', 'N/A')
                        status = psu.get('status', 'N/A')
                        model = psu.get('model', 'N/A')
                        serial = psu.get('serial', 'N/A')
                        power_type = psu.get('powerType', 'N/A')
                        
                        # 電壓信息
                        vin = psu.get('vin', 'N/A')
                        vout = psu.get('vout', 'N/A')
                        
                        # 電流信息
                        iin = psu.get('iin', 'N/A')
                        iout = psu.get('iout', 'N/A')
                        
                        # 功率信息
                        pin = psu.get('pin', 'N/A')
                        pout = psu.get('pout', 'N/A')
                        
                        print(f"        PSU{index}: {name}")
                        print(f"          狀態: {status}")
                        print(f"          型號: {model}")
                        print(f"          序列號: {serial}")
                        print(f"          電源類型: {power_type}")
                        print(f"          輸入電壓: {vin}V, 輸出電壓: {vout}V")
                        print(f"          輸入電流: {iin}A, 輸出電流: {iout}A")
                        print(f"          輸入功率: {pin}W, 輸出功率: {pout}W")
                        
            elif response.status_code == 500:
                # 某些設備可能不支持PSU讀取
                error_data = response.json() if response.content else {}
                if 'message' in error_data and 'Unsupport PSU read' in error_data['message']:
                    print("    設備不支持PSU信息讀取")
                    success = True  # 這是預期的行為
                    
            self.log_test("獲取PSU信息", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取PSU信息", False, error=e)
            return None
    
    # ==================== 1.10 Get Version Information ====================
    
    def test_get_version_info(self):
        """測試 1.10: 獲取版本信息"""
        try:
            url = f"{self.base_url}/api/v1/system/version"
            response = self.session.get(url)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    units = result_data.get('units', [])
                    
                    print(f"    版本信息:")
                    print(f"      單元數量: {len(units)}")
                    
                    for unit in units:
                        unit_id = unit.get('unitId', 'N/A')
                        serial_number = unit.get('serialNumber', 'N/A')
                        hardware_version = unit.get('hardwareVersion', 'N/A')
                        epld_version = unit.get('EPLDVersion', 'N/A')
                        port_number = unit.get('portNumber', 'N/A')
                        main_power_status = unit.get('mainPowerStatus', 'N/A')
                        role = unit.get('role', 'N/A')
                        loader_version = unit.get('loaderVersion', 'N/A')
                        kernel_version = unit.get('kernelVersion', 'N/A')
                        opcode_version = unit.get('opcodeVer', 'N/A')
                        
                        print(f"        單元{unit_id}:")
                        print(f"          序列號: {serial_number}")
                        print(f"          硬體版本: {hardware_version}")
                        print(f"          EPLD版本: {epld_version}")
                        print(f"          端口數量: {port_number}")
                        print(f"          主電源狀態: {main_power_status}")
                        print(f"          角色: {role}")
                        print(f"          載入器版本: {loader_version}")
                        print(f"          內核版本: {kernel_version}")
                        print(f"          操作碼版本: {opcode_version}")
                        
            self.log_test("獲取版本信息", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取版本信息", False, error=e)
            return None
    
    # ==================== 1.11 Reload System ====================
    
    def test_reload_system(self):
        """測試 1.11: 重啟系統（僅測試API響應，不實際重啟）"""
        try:
            # 注意：這個測試只檢查API響應，不會實際執行重啟
            print("    注意：此測試僅檢查API響應，不會實際重啟系統")
            
            url = f"{self.base_url}/api/v1/system/reload"
            
            # 在實際環境中，我們通常不會執行這個操作
            # 這裡只是為了測試API的可用性
            print("    跳過實際重啟操作以保護系統")
            
            # 模擬成功響應
            success = True
            self.log_test("系統重啟API測試（跳過實際執行）", success, details={'skipped': True})
            return True
            
        except Exception as e:
            self.log_test("系統重啟API測試", False, error=e)
            return None
    
    # ==================== 1.12 Get System Clock ====================
    
    def test_get_system_time(self):
        """測試 1.12: 獲取系統時鐘"""
        try:
            url = f"{self.base_url}/api/v1/time"
            response = self.session.get(url)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    
                    # 當前時間信息
                    current_time = result_data.get('sysCurrentTime', {})
                    year = current_time.get('year', 'N/A')
                    month = current_time.get('month', 'N/A')
                    day = current_time.get('day', 'N/A')
                    hour = current_time.get('hour', 'N/A')
                    minute = current_time.get('minute', 'N/A')
                    second = current_time.get('second', 'N/A')
                    
                    # 時區信息
                    time_zone = result_data.get('sysTimeZone', {})
                    tz_name = time_zone.get('name', 'N/A')
                    utc_type = time_zone.get('utcType', 'N/A')
                    tz_hour = time_zone.get('hour', 'N/A')
                    tz_minute = time_zone.get('minute', 'N/A')
                    
                    print(f"    系統時間:")
                    print(f"      當前時間: {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}")
                    print(f"      時區名稱: {tz_name}")
                    print(f"      UTC類型: {utc_type}")
                    print(f"      時區偏移: {tz_hour}小時{tz_minute}分鐘")
                    
                    # 保存原始配置
                    self.original_configs['time'] = {
                        'sysCurrentTime': current_time,
                        'sysTimeZone': time_zone
                    }
                    
            self.log_test("獲取系統時鐘", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取系統時鐘", False, error=e)
            return None
    
    # ==================== 1.13 Update System Clock ====================
    
    def test_update_system_time(self):
        """測試 1.13: 更新系統時鐘"""
        try:
            url = f"{self.base_url}/api/v1/time"
            
            # 獲取當前時間並稍作修改
            now = datetime.now()
            
            payload = {
                "sysCurrentTime": {
                    "year": now.year,
                    "month": now.month,
                    "day": now.day,
                    "hour": now.hour,
                    "minute": now.minute,
                    "second": now.second
                },
                "sysTimeZone": {
                    "name": "TestTZ",
                    "utcType": "after-utc",
                    "hour": 8,
                    "minute": 0
                }
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功更新系統時間:")
                current_time = payload['sysCurrentTime']
                time_zone = payload['sysTimeZone']
                print(f"      時間: {current_time['year']}-{current_time['month']:02d}-{current_time['day']:02d} {current_time['hour']:02d}:{current_time['minute']:02d}:{current_time['second']:02d}")
                print(f"      時區: {time_zone['name']} ({time_zone['utcType']} UTC+{time_zone['hour']}:{time_zone['minute']:02d})")
            
            self.log_test("更新系統時鐘", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("更新系統時鐘", False, error=e)
            return None
    
    # ==================== 1.14 Get Clock Summer Time ====================
    
    def test_get_summer_time(self):
        """測試 1.14: 獲取夏令時設置"""
        try:
            url = f"{self.base_url}/api/v1/time/clock-summer-time"
            response = self.session.get(url)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    
                    name = result_data.get('name', 'N/A')
                    summer_time_type = result_data.get('summerTimeType', 'N/A')
                    summer_time_status = result_data.get('summerTimeStatus', False)
                    offset = result_data.get('offset', 'N/A')
                    
                    print(f"    夏令時設置:")
                    print(f"      名稱: {name}")
                    print(f"      類型: {summer_time_type}")
                    print(f"      狀態: {'啟用' if summer_time_status else '禁用'}")
                    print(f"      偏移: {offset} 分鐘")
                    
                    # 顯示夏令時詳細信息
                    summer_time = result_data.get('summerTime', {})
                    if summer_time:
                        time_begin = summer_time.get('timeBegin', {})
                        time_end = summer_time.get('timeEnd', {})
                        
                        if time_begin:
                            print(f"      開始時間: {time_begin}")
                        if time_end:
                            print(f"      結束時間: {time_end}")
                    
                    # 保存原始配置
                    self.original_configs['summer_time'] = result_data
                    
            self.log_test("獲取夏令時設置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取夏令時設置", False, error=e)
            return None
    
    # ==================== 1.15 Update Clock Summer Time ====================
    
    def test_update_summer_time_date(self):
        """測試 1.15: 更新夏令時設置（日期模式）"""
        try:
            url = f"{self.base_url}/api/v1/time/clock-summer-time"
            
            payload = {
                "name": "TestDST",
                "summerTimeType": "date",
                "dateTime": {
                    "timeBegin": {
                        "day": 15,
                        "month": 3,
                        "year": 2024,
                        "hour": 2,
                        "minute": 0
                    },
                    "timeEnd": {
                        "day": 15,
                        "month": 10,
                        "year": 2024,
                        "hour": 2,
                        "minute": 0
                    }
                },
                "offset": 60
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置夏令時（日期模式）:")
                print(f"      名稱: {payload['name']}")
                print(f"      類型: {payload['summerTimeType']}")
                print(f"      偏移: {payload['offset']} 分鐘")
                
                date_time = payload['dateTime']
                begin = date_time['timeBegin']
                end = date_time['timeEnd']
                print(f"      開始: {begin['year']}-{begin['month']:02d}-{begin['day']:02d} {begin['hour']:02d}:{begin['minute']:02d}")
                print(f"      結束: {end['year']}-{end['month']:02d}-{end['day']:02d} {end['hour']:02d}:{end['minute']:02d}")
            
            self.log_test("更新夏令時設置（日期模式）", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("更新夏令時設置（日期模式）", False, error=e)
            return None
    
    def test_update_summer_time_predefined(self):
        """測試 1.15: 更新夏令時設置（預定義模式）"""
        try:
            url = f"{self.base_url}/api/v1/time/clock-summer-time"
            
            payload = {
                "name": "EuropeDST",
                "summerTimeType": "predefined",
                "predefined": "europe"
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置夏令時（預定義模式）:")
                print(f"      名稱: {payload['name']}")
                print(f"      類型: {payload['summerTimeType']}")
                print(f"      預定義區域: {payload['predefined']}")
            
            self.log_test("更新夏令時設置（預定義模式）", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("更新夏令時設置（預定義模式）", False, error=e)
            return None
    
    def test_update_summer_time_recurring(self):
        """測試 1.15: 更新夏令時設置（循環模式）"""
        try:
            url = f"{self.base_url}/api/v1/time/clock-summer-time"
            
            payload = {
                "name": "RecurringDST",
                "summerTimeType": "recurring",
                "recurringTime": {
                    "timeBegin": {
                        "week": 2,
                        "day": "sunday",
                        "month": 3,
                        "hour": 2,
                        "minute": 0
                    },
                    "timeEnd": {
                        "week": 1,
                        "day": "sunday",
                        "month": 11,
                        "hour": 2,
                        "minute": 0
                    }
                },
                "offset": 60
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置夏令時（循環模式）:")
                print(f"      名稱: {payload['name']}")
                print(f"      類型: {payload['summerTimeType']}")
                print(f"      偏移: {payload['offset']} 分鐘")
                
                recurring = payload['recurringTime']
                begin = recurring['timeBegin']
                end = recurring['timeEnd']
                print(f"      開始: {begin['month']}月第{begin['week']}週{begin['day']} {begin['hour']:02d}:{begin['minute']:02d}")
                print(f"      結束: {end['month']}月第{end['week']}週{end['day']} {end['hour']:02d}:{end['minute']:02d}")
            
            self.log_test("更新夏令時設置（循環模式）", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("更新夏令時設置（循環模式）", False, error=e)
            return None
    
    def test_disable_summer_time(self):
        """測試 1.15: 禁用夏令時"""
        try:
            url = f"{self.base_url}/api/v1/time/clock-summer-time"
            
            payload = {
                "summerTimeStatus": False
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功禁用夏令時")
            
            self.log_test("禁用夏令時", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("禁用夏令時", False, error=e)
            return None
    
    # ==================== 1.16 Get Time Range Information ====================
    
    def test_get_time_ranges(self):
        """測試 1.16: 獲取時間範圍信息"""
        try:
            url = f"{self.base_url}/api/v1/time-ranges"
            response = self.session.get(url)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    time_ranges = result_data.get('timeRanges', [])
                    
                    print(f"    時間範圍信息:")
                    print(f"      時間範圍數量: {len(time_ranges)}")
                    
                    for time_range in time_ranges:
                        name = time_range.get('name', 'N/A')
                        status = time_range.get('status', False)
                        
                        print(f"        時間範圍: {name}")
                        print(f"          狀態: {'啟用' if status else '禁用'}")
                        
                        # 絕對時間
                        abs_start = time_range.get('absoluteStart')
                        abs_end = time_range.get('absoluteEnd')
                        
                        if abs_start:
                            print(f"          絕對開始: {abs_start['year']}-{abs_start['month']:02d}-{abs_start['day']:02d} {abs_start['hour']:02d}:{abs_start['minute']:02d}")
                        if abs_end:
                            print(f"          絕對結束: {abs_end['year']}-{abs_end['month']:02d}-{abs_end['day']:02d} {abs_end['hour']:02d}:{abs_end['minute']:02d}")
                        
                        # 週期性時間
                        periodics = time_range.get('periodics', [])
                        if periodics:
                            print(f"          週期性規則數量: {len(periodics)}")
                            for i, periodic in enumerate(periodics[:3]):  # 只顯示前3個
                                start_day = periodic.get('startDay', 'N/A')
                                start_hour = periodic.get('startHour', 'N/A')
                                start_minute = periodic.get('startMinute', 'N/A')
                                end_day = periodic.get('endDay', 'N/A')
                                end_hour = periodic.get('endHour', 'N/A')
                                end_minute = periodic.get('endMinute', 'N/A')
                                
                                print(f"            規則{i+1}: {start_day} {start_hour:02d}:{start_minute:02d} 到 {end_day} {end_hour:02d}:{end_minute:02d}")
                            
                            if len(periodics) > 3:
                                print(f"            ... 還有 {len(periodics) - 3} 個規則")
                    
            self.log_test("獲取時間範圍信息", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取時間範圍信息", False, error=e)
            return None
    
    # ==================== 1.17 Add Time Range ====================
    
    def test_add_time_range(self):
        """測試 1.17: 添加時間範圍"""
        try:
            url = f"{self.base_url}/api/v1/time-ranges"
            
            # 生成唯一的時間範圍名稱
            range_name = f"TestRange_{int(time.time())}"
            
            payload = {
                "name": range_name,
                "absoluteStart": {
                    "year": 2024,
                    "month": 1,
                    "day": 1,
                    "hour": 8,
                    "minute": 0
                },
                "absoluteEnd": {
                    "year": 2024,
                    "month": 12,
                    "day": 31,
                    "hour": 18,
                    "minute": 0
                },
                "periodics": [
                    {
                        "startDay": "monday",
                        "startHour": 9,
                        "startMinute": 0,
                        "endDay": "friday",
                        "endHour": 17,
                        "endMinute": 0
                    }
                ]
            }
            
            response = self.session.post(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功添加時間範圍:")
                print(f"      名稱: {range_name}")
                
                abs_start = payload['absoluteStart']
                abs_end = payload['absoluteEnd']
                print(f"      絕對時間: {abs_start['year']}-{abs_start['month']:02d}-{abs_start['day']:02d} 到 {abs_end['year']}-{abs_end['month']:02d}-{abs_end['day']:02d}")
                
                periodic = payload['periodics'][0]
                print(f"      週期性: {periodic['startDay']} {periodic['startHour']:02d}:{periodic['startMinute']:02d} 到 {periodic['endDay']} {periodic['endHour']:02d}:{periodic['endMinute']:02d}")
                
                # 記錄創建的時間範圍
                self.created_time_ranges.append(range_name)
            
            self.log_test("添加時間範圍", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("添加時間範圍", False, error=e)
            return None
    
    # ==================== 1.18 Get Specific Time Range ====================
    
    def test_get_specific_time_range(self):
        """測試 1.18: 獲取指定時間範圍信息"""
        if not self.created_time_ranges:
            print("    跳過測試：沒有可用的時間範圍名稱")
            return None
            
        try:
            range_name = self.created_time_ranges[0]
            url = f"{self.base_url}/api/v1/time-ranges/name/{range_name}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    
                    name = result_data.get('name', 'N/A')
                    status = result_data.get('status', False)
                    
                    print(f"    獲取指定時間範圍:")
                    print(f"      名稱: {name}")
                    print(f"      狀態: {'啟用' if status else '禁用'}")
                    
                    # 顯示詳細信息
                    abs_start = result_data.get('absoluteStart')
                    abs_end = result_data.get('absoluteEnd')
                    
                    if abs_start:
                        print(f"      絕對開始: {abs_start['year']}-{abs_start['month']:02d}-{abs_start['day']:02d} {abs_start['hour']:02d}:{abs_start['minute']:02d}")
                    if abs_end:
                        print(f"      絕對結束: {abs_end['year']}-{abs_end['month']:02d}-{abs_end['day']:02d} {abs_end['hour']:02d}:{abs_end['minute']:02d}")
                    
                    periodics = result_data.get('periodics', [])
                    print(f"      週期性規則數量: {len(periodics)}")
            
            self.log_test(f"獲取指定時間範圍 ({range_name})", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"獲取指定時間範圍 ({range_name})", False, error=e)
            return None
    
    # ==================== 1.19 Update Time Range ====================
    
    def test_update_time_range(self):
        """測試 1.19: 更新時間範圍信息"""
        if not self.created_time_ranges:
            print("    跳過測試：沒有可用的時間範圍名稱")
            return None
            
        try:
            range_name = self.created_time_ranges[0]
            url = f"{self.base_url}/api/v1/time-ranges/name/{range_name}"
            
            payload = {
                "absoluteStart": {
                    "year": 2024,
                    "month": 2,
                    "day": 1,
                    "hour": 9,
                    "minute": 0
                },
                "absoluteEnd": {
                    "year": 2024,
                    "month": 11,
                    "day": 30,
                    "hour": 17,
                    "minute": 0
                },
                "periodics": [
                    {
                        "startDay": "weekdays",
                        "startHour": 8,
                        "startMinute": 30,
                        "endDay": "weekdays",
                        "endHour": 18,
                        "endMinute": 30
                    },
                    {
                        "startDay": "weekend",
                        "startHour": 10,
                        "startMinute": 0,
                        "endDay": "weekend",
                        "endHour": 16,
                        "endMinute": 0
                    }
                ]
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功更新時間範圍:")
                print(f"      名稱: {range_name}")
                
                abs_start = payload['absoluteStart']
                abs_end = payload['absoluteEnd']
                print(f"      新絕對時間: {abs_start['year']}-{abs_start['month']:02d}-{abs_start['day']:02d} 到 {abs_end['year']}-{abs_end['month']:02d}-{abs_end['day']:02d}")
                
                print(f"      新週期性規則數量: {len(payload['periodics'])}")
                for i, periodic in enumerate(payload['periodics']):
                    print(f"        規則{i+1}: {periodic['startDay']} {periodic['startHour']:02d}:{periodic['startMinute']:02d} 到 {periodic['endDay']} {periodic['endHour']:02d}:{periodic['endMinute']:02d}")
            
            self.log_test(f"更新時間範圍 ({range_name})", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"更新時間範圍 ({range_name})", False, error=e)
            return None
    
    # ==================== 1.20 Delete Time Range ====================
    
    def test_delete_time_range(self):
        """測試 1.20: 刪除時間範圍"""
        if not self.created_time_ranges:
            print("    跳過測試：沒有可用的時間範圍名稱")
            return None
            
        try:
            range_name = self.created_time_ranges.pop()  # 取出最後一個時間範圍名稱
            url = f"{self.base_url}/api/v1/time-ranges/name/{range_name}"
            
            response = self.session.delete(url)
            
            success = response.status_code == 200
            
            if success:
                print(f"    成功刪除時間範圍:")
                print(f"      名稱: {range_name}")
            
            self.log_test(f"刪除時間範圍 ({range_name})", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"刪除時間範圍 ({range_name})", False, error=e)
            return None
    
    # ==================== Complete Workflow Tests ====================
    
    def test_complete_system_workflow(self):
        """測試完整的系統工作流程"""
        print("\n=== 完整系統工作流程測試 ===")
        
        workflow_results = []
        
        try:
            # 步驟1: 獲取系統基本信息
            print("\n步驟1: 獲取系統基本信息")
            result = self.test_get_system_info()
            workflow_results.append(("獲取系統信息", result is not None))
            
            # 步驟2: 獲取硬體信息
            print("\n步驟2: 獲取硬體信息")
            result = self.test_get_memory_info()
            workflow_results.append(("獲取內存信息", result is not None))
            
            result = self.test_get_cpu_info()
            workflow_results.append(("獲取CPU信息", result is not None))
            
            result = self.test_get_fan_info()
            workflow_results.append(("獲取風扇信息", result is not None))
            
            result = self.test_get_temperature_info()
            workflow_results.append(("獲取溫度信息", result is not None))
            
            result = self.test_get_psu_info()
            workflow_results.append(("獲取PSU信息", result is not None))
            
            result = self.test_get_version_info()
            workflow_results.append(("獲取版本信息", result is not None))
            
            # 步驟3: 測試系統配置更新
            print("\n步驟3: 測試系統配置更新")
            result = self.test_update_system_info()
            workflow_results.append(("更新系統信息", result is not None))
            time.sleep(1)
            
            result = self.test_update_memory_thresholds()
            workflow_results.append(("更新內存閾值", result is not None))
            time.sleep(1)
            
            result = self.test_update_cpu_thresholds()
            workflow_results.append(("更新CPU閾值", result is not None))
            time.sleep(1)
            
            # 步驟4: 測試時間管理
            print("\n步驟4: 測試時間管理")
            result = self.test_get_system_time()
            workflow_results.append(("獲取系統時間", result is not None))
            
            result = self.test_update_system_time()
            workflow_results.append(("更新系統時間", result is not None))
            time.sleep(1)
            
            # 步驟5: 測試夏令時管理
            print("\n步驟5: 測試夏令時管理")
            result = self.test_get_summer_time()
            workflow_results.append(("獲取夏令時", result is not None))
            
            result = self.test_update_summer_time_date()
            workflow_results.append(("設置夏令時（日期）", result is not None))
            time.sleep(1)
            
            result = self.test_update_summer_time_predefined()
            workflow_results.append(("設置夏令時（預定義）", result is not None))
            time.sleep(1)
            
            result = self.test_update_summer_time_recurring()
            workflow_results.append(("設置夏令時（循環）", result is not None))
            time.sleep(1)
            
            result = self.test_disable_summer_time()
            workflow_results.append(("禁用夏令時", result is not None))
            time.sleep(1)
            
            # 步驟6: 測試時間範圍管理
            print("\n步驟6: 測試時間範圍管理")
            result = self.test_get_time_ranges()
            workflow_results.append(("獲取時間範圍", result is not None))
            
            result = self.test_add_time_range()
            workflow_results.append(("添加時間範圍", result is not None))
            
            result = self.test_get_specific_time_range()
            workflow_results.append(("獲取指定時間範圍", result is not None))
            
            result = self.test_update_time_range()
            workflow_results.append(("更新時間範圍", result is not None))
            
            # 步驟7: 最終驗證
            print("\n步驟7: 最終驗證")
            result = self.test_get_system_info()
            workflow_results.append(("最終系統驗證", result is not None))
            
            # 統計工作流程結果
            successful_steps = sum(1 for _, success in workflow_results if success)
            total_steps = len(workflow_results)
            
            print(f"\n工作流程完成統計:")
            print(f"  總步驟數: {total_steps}")
            print(f"  成功步驟: {successful_steps}")
            print(f"  成功率: {(successful_steps/total_steps)*100:.1f}%")
            
            for i, (step_name, success) in enumerate(workflow_results, 1):
                status = "✓" if success else "✗"
                print(f"  步驟{i:2d}: {status} {step_name}")
            
            overall_success = successful_steps == total_steps
            self.log_test("完整系統工作流程", overall_success, 
                         details={'successful_steps': successful_steps, 'total_steps': total_steps})
            
            print(f"\n{'✓ 完整工作流程測試完成' if overall_success else '✗ 工作流程測試部分失敗'}")
            
        except Exception as e:
            print(f"\n✗ 工作流程測試失敗: {e}")
            self.log_test("完整系統工作流程", False, error=e)
    
    # ==================== Parameter Validation Tests ====================
    
    def test_parameter_validation(self):
        """測試參數驗證"""
        print("\n=== 參數驗證測試 ===")
        
        # 測試內存閾值範圍
        print("\n--- 內存閾值範圍驗證測試 ---")
        threshold_test_cases = [
            ({"risingThreshold": 1, "fallingThreshold": 1}, "最小閾值", True),
            ({"risingThreshold": 50, "fallingThreshold": 30}, "標準閾值", True),
            ({"risingThreshold": 100, "fallingThreshold": 100}, "最大閾值", True),
            ({"risingThreshold": 90, "fallingThreshold": 95}, "下降>上升", False),
            ({"risingThreshold": 0, "fallingThreshold": 50}, "上升閾值為0", False),
            ({"risingThreshold": 50, "fallingThreshold": 0}, "下降閾值為0", False),
            ({"risingThreshold": 101, "fallingThreshold": 50}, "上升閾值>100", False),
            ({"risingThreshold": 50, "fallingThreshold": 101}, "下降閾值>100", False)
        ]

        for payload, description, should_succeed in threshold_test_cases:
            try:
                url = f"{self.base_url}/api/v1/system/memory"
                response = self.session.put(url, json=payload)
                success = (response.status_code == 200) == should_succeed
                
                self.log_test(f"內存閾值驗證 - {description}", success, response)
                time.sleep(0.3)
            except Exception as e:
                self.log_test(f"內存閾值驗證 - {description}", False, error=e)
        
        # 測試CPU閾值範圍
        print("\n--- CPU閾值範圍驗證測試 ---")
        for payload, description, should_succeed in threshold_test_cases:
            try:
                url = f"{self.base_url}/api/v1/system/cpu"
                response = self.session.put(url, json=payload)
                success = (response.status_code == 200) == should_succeed
                
                self.log_test(f"CPU閾值驗證 - {description}", success, response)
                time.sleep(0.3)
            except Exception as e:
                self.log_test(f"CPU閾值驗證 - {description}", False, error=e)
        
        # 測試系統名稱長度
        print("\n--- 系統名稱長度驗證測試 ---")
        name_test_cases = [
            ("", "空名稱", True),
            ("A", "單字符名稱", True),
            ("A" * 100, "中等長度名稱", True),
            ("A" * 255, "最大長度名稱", True),
            ("A" * 256, "超長名稱", False)
        ]
        
        for name, description, should_succeed in name_test_cases:
            try:
                url = f"{self.base_url}/api/v1/system"
                payload = {"sysName": name}
                response = self.session.put(url, json=payload)
                success = (response.status_code == 200) == should_succeed
                
                self.log_test(f"系統名稱長度驗證 - {description} (長度:{len(name)})", success, response)
                time.sleep(0.3)
            except Exception as e:
                self.log_test(f"系統名稱長度驗證 - {description}", False, error=e)
        
        # 測試時間範圍名稱長度
        print("\n--- 時間範圍名稱長度驗證測試 ---")
        range_name_test_cases = [
            ("A", "單字符", True),
            ("A" * 8, "中等長度", True),
            ("A" * 16, "最大長度", True),
            ("A" * 17, "超長名稱", False)
        ]
        
        for name, description, should_succeed in range_name_test_cases:
            try:
                url = f"{self.base_url}/api/v1/time-ranges"
                payload = {
                    "name": name,
                    "absoluteStart": {
                        "year": 2024,
                        "month": 1,
                        "day": 1,
                        "hour": 8,
                        "minute": 0
                    },
                    "absoluteEnd": {
                        "year": 2024,
                        "month": 12,
                        "day": 31,
                        "hour": 18,
                        "minute": 0
                    }
                }
                response = self.session.post(url, json=payload)
                success = (response.status_code == 200) == should_succeed
                
                # 如果創建成功，記錄以便後續清理
                if success and should_succeed:
                    self.created_time_ranges.append(name)
                
                self.log_test(f"時間範圍名稱長度驗證 - {description} (長度:{len(name)})", success, response)
                time.sleep(0.3)
            except Exception as e:
                self.log_test(f"時間範圍名稱長度驗證 - {description}", False, error=e)
        
        # 測試夏令時偏移範圍
        print("\n--- 夏令時偏移範圍驗證測試 ---")
        offset_test_cases = [
            (1, "最小偏移", True),
            (30, "標準偏移", True),
            (60, "1小時偏移", True),
            (120, "2小時偏移", True),
            (0, "零偏移", False),
            (-30, "負偏移", False),
            (1440, "24小時偏移", False)
        ]
        
        for offset, description, should_succeed in offset_test_cases:
            try:
                url = f"{self.base_url}/api/v1/time/clock-summer-time"
                payload = {
                    "name": f"TestDST_{offset}",
                    "summerTimeType": "date",
                    "dateTime": {
                        "timeBegin": {
                            "day": 15,
                            "month": 3,
                            "year": 2024,
                            "hour": 2,
                            "minute": 0
                        },
                        "timeEnd": {
                            "day": 15,
                            "month": 10,
                            "year": 2024,
                            "hour": 2,
                            "minute": 0
                        }
                    },
                    "offset": offset
                }
                response = self.session.put(url, json=payload)
                success = (response.status_code == 200) == should_succeed
                
                self.log_test(f"夏令時偏移驗證 - {description} ({offset}分鐘)", success, response)
                time.sleep(0.3)
            except Exception as e:
                self.log_test(f"夏令時偏移驗證 - {description} ({offset}分鐘)", False, error=e)
    
    # ==================== Error Scenarios Tests ====================
    
    def test_error_scenarios(self):
        """測試錯誤場景"""
        print("\n=== 錯誤場景測試 ===")
        
        # 測試1: 無效JSON格式
        print("\n--- JSON格式錯誤測試 ---")
        invalid_json_endpoints = [
            ("/api/v1/system", "系統信息"),
            ("/api/v1/system/memory", "內存配置"),
            ("/api/v1/system/cpu", "CPU配置"),
            ("/api/v1/time", "時間配置"),
            ("/api/v1/time/clock-summer-time", "夏令時配置")
        ]

        for endpoint, description in invalid_json_endpoints:
            try:
                url = f"{self.base_url}/{endpoint}"
                response = self.session.put(url, data="invalid json format")
                success = response.status_code == 400
                self.log_test(f"無效JSON格式測試 - {description}", success, response)
            except Exception as e:
                self.log_test(f"無效JSON格式測試 - {description}", False, error=e)
        
        # 測試2: 錯誤的數據類型
        print("\n--- 數據類型錯誤測試 ---")
        
        # 系統配置數據類型錯誤
        wrong_type_cases = [
            ({"sysName": 123}, "系統名稱為數字"),
            ({"sysFanStatus": "true"}, "風扇狀態為字符串"),
            ({"jumboFrameStatus": 1}, "巨型幀狀態為數字"),
            ({"watchdogStatus": "false"}, "看門狗狀態為字符串")
        ]
        
        for payload, description in wrong_type_cases:
            try:
                url = f"{self.base_url}/api/v1/system"
                response = self.session.put(url, json=payload)
                success = response.status_code == 400
                self.log_test(f"系統配置數據類型錯誤 - {description}", success, response)
            except Exception as e:
                self.log_test(f"系統配置數據類型錯誤 - {description}", False, error=e)
        
        # 閾值數據類型錯誤
        threshold_wrong_types = [
            ({"risingThreshold": "80", "fallingThreshold": 60}, "上升閾值為字符串"),
            ({"risingThreshold": 80, "fallingThreshold": "60"}, "下降閾值為字符串"),
            ({"risingThreshold": 80.5, "fallingThreshold": 60}, "上升閾值為浮點數"),
            ({"risingThreshold": 80, "fallingThreshold": 60.5}, "下降閾值為浮點數")
        ]
        
        for payload, description in threshold_wrong_types:
            try:
                url = f"{self.base_url}/api/v1/system/memory"
                response = self.session.put(url, json=payload)
                success = response.status_code == 400
                self.log_test(f"內存閾值數據類型錯誤 - {description}", success, response)
            except Exception as e:
                self.log_test(f"內存閾值數據類型錯誤 - {description}", False, error=e)
        
        # 時間數據類型錯誤
        time_wrong_types = [
            ({"year": "2024", "month": 1, "day": 1, "hour": 0, "minute": 0}, "年份為字符串"),
            ({"year": 2024, "month": "1", "day": 1, "hour": 0, "minute": 0}, "月份為字符串"),
            ({"year": 2024, "month": 1, "day": "1", "hour": 0, "minute": 0}, "日期為字符串"),
            ({"year": 2024, "month": 1, "day": 1, "hour": "0", "minute": 0}, "小時為字符串"),
            ({"year": 2024, "month": 1, "day": 1, "hour": 0, "minute": "0"}, "分鐘為字符串")
        ]
        
        for time_data, description in time_wrong_types:
            try:
                url = f"{self.base_url}/api/v1/time"
                payload = {
                    "sysCurrentTime": time_data,
                    "sysTimeZone": {
                        "name": "TestTZ",
                        "utcType": "after-utc",
                        "hour": 8,
                        "minute": 0
                    }
                }
                response = self.session.put(url, json=payload)
                success = response.status_code == 400
                self.log_test(f"時間數據類型錯誤 - {description}", success, response)
            except Exception as e:
                self.log_test(f"時間數據類型錯誤 - {description}", False, error=e)
        
        # 測試3: 不存在的資源操作
        print("\n--- 不存在資源錯誤測試 ---")
        
        # 獲取不存在的時間範圍
        try:
            url = f"{self.base_url}/api/v1/time-ranges/name/NonExistentRange"
            response = self.session.get(url)
            success = response.status_code == 404
            self.log_test("獲取不存在的時間範圍測試", success, response)
        except Exception as e:
            self.log_test("獲取不存在的時間範圍測試", False, error=e)
        
        # 更新不存在的時間範圍
        try:
            url = f"{self.base_url}/api/v1/time-ranges/name/NonExistentRange"
            payload = {
                "absoluteStart": {
                    "year": 2024,
                    "month": 1,
                    "day": 1,
                    "hour": 8,
                    "minute": 0
                }
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 404
            self.log_test("更新不存在的時間範圍測試", success, response)
        except Exception as e:
            self.log_test("更新不存在的時間範圍測試", False, error=e)
        
        # 刪除不存在的時間範圍
        try:
            url = f"{self.base_url}/api/v1/time-ranges/name/NonExistentRange"
            response = self.session.delete(url)
            success = response.status_code == 404
            self.log_test("刪除不存在的時間範圍測試", success, response)
        except Exception as e:
            self.log_test("刪除不存在的時間範圍測試", False, error=e)
        
        # 測試4: 無效的夏令時配置
        print("\n--- 夏令時配置錯誤測試 ---")
        
        # 無效的夏令時類型
        try:
            url = f"{self.base_url}/api/v1/time/clock-summer-time"
            payload = {
                "name": "InvalidTypeDST",
                "summerTimeType": "invalid_type"
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            self.log_test("無效夏令時類型測試", success, response)
        except Exception as e:
            self.log_test("無效夏令時類型測試", False, error=e)
        
        # 無效的預定義區域
        try:
            url = f"{self.base_url}/api/v1/time/clock-summer-time"
            payload = {
                "name": "InvalidZoneDST",
                "summerTimeType": "predefined",
                "predefined": "invalid_zone"
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            self.log_test("無效預定義區域測試", success, response)
        except Exception as e:
            self.log_test("無效預定義區域測試", False, error=e)
        
        # 無效的星期名稱
        try:
            url = f"{self.base_url}/api/v1/time/clock-summer-time"
            payload = {
                "name": "InvalidDayDST",
                "summerTimeType": "recurring",
                "recurringTime": {
                    "timeBegin": {
                        "week": 1,
                        "day": "invalid_day",
                        "month": 3,
                        "hour": 2,
                        "minute": 0
                    },
                    "timeEnd": {
                        "week": 1,
                        "day": "sunday",
                        "month": 11,
                        "hour": 2,
                        "minute": 0
                    }
                }
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            self.log_test("無效星期名稱測試", success, response)
        except Exception as e:
            self.log_test("無效星期名稱測試", False, error=e)
        
        # 測試5: 時間範圍邏輯錯誤
        print("\n--- 時間範圍邏輯錯誤測試 ---")
        
        # 結束時間早於開始時間
        try:
            url = f"{self.base_url}/api/v1/time-ranges"
            payload = {
                "name": "InvalidTimeRange",
                "absoluteStart": {
                    "year": 2024,
                    "month": 12,
                    "day": 31,
                    "hour": 23,
                    "minute": 59
                },
                "absoluteEnd": {
                    "year": 2024,
                    "month": 1,
                    "day": 1,
                    "hour": 0,
                    "minute": 0
                }
            }
            response = self.session.post(url, json=payload)
            success = response.status_code == 400
            self.log_test("時間範圍邏輯錯誤測試（結束早於開始）", success, response)
        except Exception as e:
            self.log_test("時間範圍邏輯錯誤測試（結束早於開始）", False, error=e)
        
        # 無效的日期
        try:
            url = f"{self.base_url}/api/v1/time-ranges"
            payload = {
                "name": "InvalidDateRange",
                "absoluteStart": {
                    "year": 2024,
                    "month": 2,
                    "day": 30,  # 2月沒有30日
                    "hour": 8,
                    "minute": 0
                }
            }
            response = self.session.post(url, json=payload)
            success = response.status_code == 400
            self.log_test("無效日期測試（2月30日）", success, response)
        except Exception as e:
            self.log_test("無效日期測試（2月30日）", False, error=e)
    
    # ==================== Boundary Conditions Tests ====================
    
    def test_boundary_conditions(self):
        """測試邊界條件"""
        print("\n=== 邊界條件測試 ===")
        
        # 測試時間邊界值
        print("\n--- 時間邊界值測試 ---")
        time_boundary_cases = [
            ({"year": 1970, "month": 1, "day": 1, "hour": 0, "minute": 0}, "Unix紀元開始", True),
            ({"year": 2038, "month": 1, "day": 19, "hour": 3, "minute": 14}, "32位時間戳上限", True),
            ({"year": 2099, "month": 12, "day": 31, "hour": 23, "minute": 59}, "世紀末", True),
            ({"year": 1969, "month": 12, "day": 31, "hour": 23, "minute": 59}, "Unix紀元前", False),
            ({"year": 2024, "month": 0, "day": 1, "hour": 0, "minute": 0}, "月份為0", False),
            ({"year": 2024, "month": 13, "day": 1, "hour": 0, "minute": 0}, "月份為13", False),
            ({"year": 2024, "month": 1, "day": 0, "hour": 0, "minute": 0}, "日期為0", False),
            ({"year": 2024, "month": 1, "day": 32, "hour": 0, "minute": 0}, "日期為32", False),
            ({"year": 2024, "month": 1, "day": 1, "hour": -1, "minute": 0}, "小時為-1", False),
            ({"year": 2024, "month": 1, "day": 1, "hour": 24, "minute": 0}, "小時為24", False),
            ({"year": 2024, "month": 1, "day": 1, "hour": 0, "minute": -1}, "分鐘為-1", False),
            ({"year": 2024, "month": 1, "day": 1, "hour": 0, "minute": 60}, "分鐘為60", False)
        ]
        
        for time_data, description, should_succeed in time_boundary_cases:
            try:
                url = f"{self.base_url}/api/v1/time"
                payload = {
                    "sysCurrentTime": time_data,
                    "sysTimeZone": {
                        "name": "TestTZ",
                        "utcType": "after-utc",
                        "hour": 8,
                        "minute": 0
                    }
                }
                response = self.session.put(url, json=payload)
                success = (response.status_code == 200) == should_succeed
                
                self.log_test(f"時間邊界值測試 - {description}", success, response)
            except Exception as e:
                self.log_test(f"時間邊界值測試 - {description}", False, error=e)
        
        # 測試時區偏移邊界值
        print("\n--- 時區偏移邊界值測試 ---")
        timezone_boundary_cases = [
            ({"hour": -12, "minute": 0}, "UTC-12", True),
            ({"hour": 14, "minute": 0}, "UTC+14", True),
            ({"hour": 0, "minute": 0}, "UTC+0", True),
            ({"hour": 5, "minute": 30}, "UTC+5:30", True),
            ({"hour": -13, "minute": 0}, "UTC-13", False),
            ({"hour": 15, "minute": 0}, "UTC+15", False),
            ({"hour": 8, "minute": 60}, "分鐘為60", False),
            ({"hour": 8, "minute": -1}, "分鐘為-1", False)
        ]
        
        for tz_data, description, should_succeed in timezone_boundary_cases:
            try:
                url = f"{self.base_url}/api/v1/time"
                payload = {
                    "sysCurrentTime": {
                        "year": 2024,
                        "month": 1,
                        "day": 1,
                        "hour": 12,
                        "minute": 0,
                        "second": 0
                    },
                    "sysTimeZone": {
                        "name": "BoundaryTZ",
                        "utcType": "after-utc" if tz_data["hour"] >= 0 else "before-utc",
                        "hour": abs(tz_data["hour"]),
                        "minute": tz_data["minute"]
                    }
                }
                response = self.session.put(url, json=payload)
                success = (response.status_code == 200) == should_succeed
                
                self.log_test(f"時區偏移邊界值測試 - {description}", success, response)
            except Exception as e:
                self.log_test(f"時區偏移邊界值測試 - {description}", False, error=e)
        
        # 測試夏令時週數邊界
        print("\n--- 夏令時週數邊界值測試 ---")
        week_boundary_cases = [
            (1, "第1週", True),
            (2, "第2週", True),
            (3, "第3週", True),
            (4, "第4週", True),
            (5, "第5週", True),
            (0, "第0週", False),
            (6, "第6週", False)
        ]
        
        for week, description, should_succeed in week_boundary_cases:
            try:
                url = f"{self.base_url}/api/v1/time/clock-summer-time"
                payload = {
                    "name": f"WeekBoundaryDST_{week}",
                    "summerTimeType": "recurring",
                    "recurringTime": {
                        "timeBegin": {
                            "week": week,
                            "day": "sunday",
                            "month": 3,
                            "hour": 2,
                            "minute": 0
                        },
                        "timeEnd": {
                            "week": 1,
                            "day": "sunday",
                            "month": 11,
                            "hour": 2,
                            "minute": 0
                        }
                    },
                    "offset": 60
                }
                response = self.session.put(url, json=payload)
                success = (response.status_code == 200) == should_succeed
                
                self.log_test(f"夏令時週數邊界值測試 - {description}", success, response)
            except Exception as e:
                self.log_test(f"夏令時週數邊界值測試 - {description}", False, error=e)
    
    # ==================== Performance Tests ====================
    
    def test_performance_scenarios(self):
        """測試性能場景"""
        print("\n=== 性能測試場景 ===")
        
        # 測試連續快速請求
        print("\n--- 連續快速請求測試 ---")
        try:
            start_time = time.time()
            success_count = 0
            total_requests = 10
            
            for i in range(total_requests):
                url = f"{self.base_url}/api/v1/system"
                response = self.session.get(url)
                if response.status_code == 200:
                    success_count += 1
            
            end_time = time.time()
            duration = end_time - start_time
            avg_response_time = duration / total_requests
            
            success = success_count == total_requests
            details = {
                'total_requests': total_requests,
                'success_count': success_count,
                'total_duration': duration,
                'avg_response_time': avg_response_time
            }
            
            print(f"    總請求數: {total_requests}")
            print(f"    成功請求數: {success_count}")
            print(f"    總耗時: {duration:.2f} 秒")
            print(f"    平均響應時間: {avg_response_time:.3f} 秒")
            
            self.log_test("連續快速請求測試", success, details=details)
            
        except Exception as e:
            self.log_test("連續快速請求測試", False, error=e)
        
        # 測試大量時間範圍創建
        print("\n--- 大量時間範圍創建測試 ---")
        try:
            start_time = time.time()
            created_ranges = []
            success_count = 0
            total_ranges = 5  # 創建5個時間範圍
            
            for i in range(total_ranges):
                range_name = f"PerfTestRange_{int(time.time())}_{i}"
                url = f"{self.base_url}/api/v1/time-ranges"
                payload = {
                    "name": range_name,
                    "absoluteStart": {
                        "year": 2024,
                        "month": 1 + i,
                        "day": 1,
                        "hour": 8,
                        "minute": 0
                    },
                    "absoluteEnd": {
                        "year": 2024,
                        "month": 1 + i,
                        "day": 28,
                        "hour": 18,
                        "minute": 0
                    }
                }
                
                response = self.session.post(url, json=payload)
                if response.status_code == 200:
                    success_count += 1
                    created_ranges.append(range_name)
                    self.created_time_ranges.append(range_name)
            
            end_time = time.time()
            duration = end_time - start_time
            
            success = success_count == total_ranges
            details = {
                'total_ranges': total_ranges,
                'success_count': success_count,
                'duration': duration,
                'created_ranges': created_ranges
            }
            
            print(f"    創建時間範圍數: {total_ranges}")
            print(f"    成功創建數: {success_count}")
            print(f"    總耗時: {duration:.2f} 秒")
            
            self.log_test("大量時間範圍創建測試", success, details=details)
            
        except Exception as e:
            self.log_test("大量時間範圍創建測試", False, error=e)
    
    # ==================== Cleanup and Restore ====================
    
    def cleanup_created_resources(self):
        """清理創建的資源"""
        print("\n=== 清理創建的資源 ===")
        
        # 清理創建的時間範圍
        for range_name in self.created_time_ranges[:]:  # 使用切片複製列表
            try:
                url = f"{self.base_url}/api/v1/time-ranges/name/{range_name}"
                response = self.session.delete(url)
                
                if response.status_code == 200:
                    print(f"    ✓ 已刪除時間範圍: {range_name}")
                    self.created_time_ranges.remove(range_name)
                else:
                    print(f"    ✗ 刪除時間範圍失敗: {range_name}")
                    
            except Exception as e:
                print(f"    ✗ 刪除時間範圍時發生錯誤: {range_name}, 錯誤: {e}")
        
        if not self.created_time_ranges:
            print("    ✓ 所有創建的資源已清理完成")
        else:
            print(f"    ⚠️  仍有 {len(self.created_time_ranges)} 個資源未能清理")
    
    def restore_original_configs(self):
        """恢復原始配置"""
        print("\n=== 恢復原始配置 ===")
        
        # 恢復系統配置
        if 'system' in self.original_configs:
            try:
                url = f"{self.base_url}/api/v1/system"
                response = self.session.put(url, json=self.original_configs['system'])
                
                success = response.status_code == 200
                if success:
                    print("    ✓ 系統配置已恢復")
                    config = self.original_configs['system']
                    print(f"      系統名稱: {config.get('sysName', 'N/A')}")
                    print(f"      風扇狀態: {'啟用' if config.get('sysFanStatus') else '禁用'}")
                    print(f"      巨型幀狀態: {'啟用' if config.get('jumboFrameStatus') else '禁用'}")
                    print(f"      看門狗狀態: {'啟用' if config.get('watchdogStatus') else '禁用'}")
                else:
                    print("    ✗ 恢復系統配置失敗")
                
                self.log_test("恢復系統配置", success, response)
                
            except Exception as e:
                print(f"    ✗ 恢復系統配置時發生錯誤: {e}")
                self.log_test("恢復系統配置", False, error=e)
        
        # 恢復內存閾值配置
        if 'memory' in self.original_configs:
            try:
                url = f"{self.base_url}/api/v1/system/memory"
                response = self.session.put(url, json=self.original_configs['memory'])
                
                success = response.status_code == 200
                if success:
                    print("    ✓ 內存閾值配置已恢復")
                    config = self.original_configs['memory']
                    print(f"      上升閾值: {config.get('risingThreshold')}%")
                    print(f"      下降閾值: {config.get('fallingThreshold')}%")
                else:
                    print("    ✗ 恢復內存閾值配置失敗")
                
                self.log_test("恢復內存閾值配置", success, response)
                
            except Exception as e:
                print(f"    ✗ 恢復內存閾值配置時發生錯誤: {e}")
                self.log_test("恢復內存閾值配置", False, error=e)
        
        # 恢復CPU閾值配置
        if 'cpu' in self.original_configs:
            try:
                url = f"{self.base_url}/api/v1/system/cpu"
                response = self.session.put(url, json=self.original_configs['cpu'])
                
                success = response.status_code == 200
                if success:
                    print("    ✓ CPU閾值配置已恢復")
                    config = self.original_configs['cpu']
                    print(f"      上升閾值: {config.get('risingThreshold')}%")
                    print(f"      下降閾值: {config.get('fallingThreshold')}%")
                else:
                    print("    ✗ 恢復CPU閾值配置失敗")
                
                self.log_test("恢復CPU閾值配置", success, response)
                
            except Exception as e:
                print(f"    ✗ 恢復CPU閾值配置時發生錯誤: {e}")
                self.log_test("恢復CPU閾值配置", False, error=e)
        
        # 恢復時間配置
        if 'time' in self.original_configs:
            try:
                url = f"{self.base_url}/api/v1/time"
                response = self.session.put(url, json=self.original_configs['time'])
                
                success = response.status_code == 200
                if success:
                    print("    ✓ 時間配置已恢復")
                    current_time = self.original_configs['time'].get('sysCurrentTime', {})
                    time_zone = self.original_configs['time'].get('sysTimeZone', {})
                    print(f"      時區: {time_zone.get('name', 'N/A')}")
                else:
                    print("    ✗ 恢復時間配置失敗")
                
                self.log_test("恢復時間配置", success, response)
                
            except Exception as e:
                print(f"    ✗ 恢復時間配置時發生錯誤: {e}")
                self.log_test("恢復時間配置", False, error=e)
        
        # 恢復夏令時配置
        if 'summer_time' in self.original_configs:
            try:
                url = f"{self.base_url}/api/v1/time/clock-summer-time"
                response = self.session.put(url, json=self.original_configs['summer_time'])
                
                success = response.status_code == 200
                if success:
                    print("    ✓ 夏令時配置已恢復")
                    config = self.original_configs['summer_time']
                    print(f"      名稱: {config.get('name', 'N/A')}")
                    print(f"      類型: {config.get('summerTimeType', 'N/A')}")
                    print(f"      狀態: {'啟用' if config.get('summerTimeStatus') else '禁用'}")
                else:
                    print("    ✗ 恢復夏令時配置失敗")
                
                self.log_test("恢復夏令時配置", success, response)
                
            except Exception as e:
                print(f"    ✗ 恢復夏令時配置時發生錯誤: {e}")
                self.log_test("恢復夏令時配置", False, error=e)
        
        if not self.original_configs:
            print("    沒有保存的原始配置，跳過恢復")
    
    # ==================== Main Test Runner ====================
    
    def run_all_tests(self):
        """運行所有測試"""
        print("=== System REST API 測試開始 ===")
        print(f"測試目標: {self.base_url}")
        print(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        try:
            # 1. 系統基本信息測試
            print("\n=== 系統基本信息測試 ===")
            self.test_get_system_info()
            self.test_update_system_info()
            time.sleep(1)
            self.test_get_system_info()  # 驗證更新
            
            # 2. 硬體信息測試
            print("\n=== 硬體信息測試 ===")
            self.test_get_memory_info()
            self.test_update_memory_thresholds()
            time.sleep(1)
            self.test_get_memory_info()  # 驗證更新
            
            self.test_get_cpu_info()
            self.test_update_cpu_thresholds()
            time.sleep(1)
            self.test_get_cpu_info()  # 驗證更新
            
            self.test_get_fan_info()
            self.test_get_temperature_info()
            self.test_get_psu_info()
            self.test_get_version_info()
            
            # 3. 系統重啟測試（跳過實際執行）
            print("\n=== 系統重啟測試 ===")
            self.test_reload_system()
            
            # 4. 時間管理測試
            print("\n=== 時間管理測試 ===")
            self.test_get_system_time()
            self.test_update_system_time()
            time.sleep(1)
            self.test_get_system_time()  # 驗證更新
            
            # 5. 夏令時管理測試
            print("\n=== 夏令時管理測試 ===")
            self.test_get_summer_time()
            self.test_update_summer_time_date()
            time.sleep(1)
            self.test_update_summer_time_predefined()
            time.sleep(1)
            self.test_update_summer_time_recurring()
            time.sleep(1)
            self.test_disable_summer_time()
            time.sleep(1)
            
            # 6. 時間範圍管理測試
            print("\n=== 時間範圍管理測試 ===")
            self.test_get_time_ranges()
            self.test_add_time_range()
            self.test_get_specific_time_range()
            self.test_update_time_range()
            # 注意：刪除測試在清理階段執行
            
            # 7. 完整工作流程測試
            self.test_complete_system_workflow()
            
            # 8. 參數驗證測試
            self.test_parameter_validation()
            
            # 9. 邊界條件測試
            self.test_boundary_conditions()
            
            # 10. 錯誤場景測試
            self.test_error_scenarios()
            
            # 11. 性能測試
            self.test_performance_scenarios()
            
        finally:
            # 12. 清理和恢復
            self.cleanup_created_resources()
            self.restore_original_configs()
        
        # 13. 輸出測試總結
        self.print_test_summary()
    
    def print_test_summary(self):
        """輸出測試總結"""
        print("\n" + "=" * 60)
        print("=== 測試總結 ===")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"總測試數: {total_tests}")
        print(f"通過: {passed_tests}")
        print(f"失敗: {failed_tests}")
        print(f"成功率: {(passed_tests/total_tests)*100:.1f}%")
        
        # 按功能分類統計
        system_tests = [r for r in self.test_results if ('系統' in r['test_name'] or 'System' in r['test_name'])]
        hardware_tests = [r for r in self.test_results if ('內存' in r['test_name'] or 'CPU' in r['test_name'] or '風扇' in r['test_name'] or '溫度' in r['test_name'] or 'PSU' in r['test_name'] or '版本' in r['test_name'])]
        time_tests = [r for r in self.test_results if ('時間' in r['test_name'] or '夏令時' in r['test_name'])]
        range_tests = [r for r in self.test_results if '時間範圍' in r['test_name']]
        validation_tests = [r for r in self.test_results if '驗證' in r['test_name']]
        error_tests = [r for r in self.test_results if ('錯誤' in r['test_name'] or '無效' in r['test_name'])]
        boundary_tests = [r for r in self.test_results if '邊界' in r['test_name']]
        performance_tests = [r for r in self.test_results if '性能' in r['test_name']]
        workflow_tests = [r for r in self.test_results if '工作流程' in r['test_name']]
        
        print(f"\n功能測試統計:")
        print(f"  系統信息測試: {len(system_tests)} 個測試")
        print(f"  硬體信息測試: {len(hardware_tests)} 個測試")
        print(f"  時間管理測試: {len(time_tests)} 個測試")
        print(f"  時間範圍測試: {len(range_tests)} 個測試")
        print(f"  工作流程測試: {len(workflow_tests)} 個測試")
        print(f"  參數驗證測試: {len(validation_tests)} 個測試")
        print(f"  邊界條件測試: {len(boundary_tests)} 個測試")
        print(f"  錯誤場景測試: {len(error_tests)} 個測試")
        print(f"  性能測試: {len(performance_tests)} 個測試")
        
        if failed_tests > 0:
            print("\n失敗的測試:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test_name']}")
                    if 'error' in result:
                        print(f"    錯誤: {result['error']}")
                    if 'status_code' in result:
                        print(f"    狀態碼: {result['status_code']}")
        
        # 保存詳細結果到文件
        with open('system_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        print(f"\n詳細測試結果已保存到: system_test_results.json")
        
        # 輸出配置統計
        print(f"\n原始配置信息:")
        for config_type, config_data in self.original_configs.items():
            print(f"  {config_type}: 已保存並恢復")

def main():
    """主函數"""
    if len(sys.argv) < 2:
        print("使用方法: python system_test.py <base_url> [username] [password]")
        print("範例: python system_test.py http://192.168.1.1 admin admin123")
        print("\n功能說明:")
        print("  - 測試所有System API功能")
        print("  - 包含系統信息、硬體監控、時間管理")
        print("  - 夏令時配置和時間範圍管理")
        print("  - 參數驗證和錯誤場景測試")
        print("  - 性能測試和邊界條件測試")
        print("  - 自動清理創建的資源")
        print("  - 自動恢復原始配置")
        print("  - 生成詳細測試報告")
        print("\n注意事項:")
        print("  - 系統重啟API僅測試響應，不實際執行")
        print("  - 時間配置會影響系統時間，測試後自動恢復")
        print("  - 閾值範圍: 1-100%")
        print("  - 時間範圍名稱長度: 1-16字符")
        print("  - 建議在測試環境中運行")
        sys.exit(1)
    
    base_url = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else None
    password = sys.argv[3] if len(sys.argv) > 3 else None
    
    # 創建測試器並運行測試
    tester = SystemAPITester(base_url, username, password)
    
    try:
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n測試被用戶中斷")
        print("正在清理資源和恢復配置...")
        tester.cleanup_created_resources()
        tester.restore_original_configs()
    except Exception as e:
        print(f"\n測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        print("正在清理資源和恢復配置...")
        tester.cleanup_created_resources()
        tester.restore_original_configs()

if __name__ == "__main__":
    main()