
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RMON REST API 測試腳本
基於 RMON_API_Reference_v0.13.docx 文件生成
包含 Alarms, Events, Histories 和 RMON1 Statistics 功能測試
"""

import hashlib

import requests
import json
import sys
import time
from urllib.parse import quote
import random

class RMONAPITester:
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
        self.created_alarms = []      # 記錄創建的alarm
        self.created_events = []      # 記錄創建的event
        self.created_histories = []   # 記錄創建的history
        self.created_rmon1 = []       # 記錄創建的rmon1
    
    def log_test(self, test_name, success, response=None, error=None):
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
        
        self.test_results.append(result)
        
        # 即時輸出結果
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"[{result['timestamp']}] {status} - {test_name}")
        if error:
            print(f"    錯誤: {error}")
        if response:
            print(f"    狀態碼: {response.status_code}")
    
    def encode_interface_id(self, interface_id):
        """編碼接口ID，處理特殊字符"""
        # 將 eth1/1 轉換為 eth1%2f1
        return quote(interface_id, safe='')
    
    # ==================== 1.1 Get all RMON alarms ====================
    
    def test_get_all_alarms(self, start_id=1):
        """測試 1.1: 獲取所有RMON alarms"""
        try:
            url = f"{self.base_url}/api/v1/rmon/alarms"
            params = {"startId": start_id}
            response = self.session.get(url, params=params)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    start_id_resp = result_data.get('startId')
                    alarms = result_data.get('alarms', [])
                    
                    print(f"    起始ID: {start_id_resp}")
                    print(f"    找到 {len(alarms)} 個 alarm")
                    
                    for alarm in alarms[:3]:  # 顯示前3個
                        print(f"      Alarm {alarm.get('index')}:")
                        print(f"        變量: {alarm.get('variable')}")
                        print(f"        間隔: {alarm.get('interval')} 秒")
                        print(f"        採樣類型: {alarm.get('sampleType')}")
                        print(f"        上升閾值: {alarm.get('risingThreshold')}")
                        print(f"        下降閾值: {alarm.get('fallingThreshold')}")
                        print(f"        擁有者: {alarm.get('owner', 'N/A')}")
                else:
                    print("    沒有找到 alarm")
                    
            self.log_test(f"獲取所有alarms (startId={start_id})", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"獲取所有alarms (startId={start_id})", False, error=e)
            return None
    
    # ==================== 1.2 Add an RMON alarm ====================
    
    def test_create_alarm(self, index, variable, interval=50, sample_type="absolute",
                         rising_threshold=999, falling_threshold=99, 
                         rising_event_index=None, falling_event_index=None, owner="test"):
        """測試 1.2: 創建RMON alarm"""
        try:
            url = f"{self.base_url}/api/v1/rmon/alarms"
            
            payload = {
                "index": index,
                "variable": variable,
                "interval": interval,
                "sampleType": sample_type,
                "risingThreshold": rising_threshold,
                "fallingThreshold": falling_threshold,
                "owner": owner
            }
            
            # 添加可選的事件索引
            if rising_event_index:
                payload["risingEventIndex"] = rising_event_index
            if falling_event_index:
                payload["fallingEventIndex"] = falling_event_index
            
            response = self.session.post(url, json=payload)
            
            success = response.status_code == 200
            if success:
                self.created_alarms.append(index)
                print(f"    成功創建alarm {index}:")
                print(f"      變量: {variable}")
                print(f"      間隔: {interval} 秒")
                print(f"      採樣類型: {sample_type}")
                print(f"      上升閾值: {rising_threshold}")
                print(f"      下降閾值: {falling_threshold}")
                print(f"      擁有者: {owner}")
            
            self.log_test(f"創建alarm {index}", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"創建alarm {index}", False, error=e)
            return None
    
    # ==================== 1.3 Get an RMON alarm ====================
    
    def test_get_alarm(self, index):
        """測試 1.3: 獲取指定RMON alarm"""
        try:
            url = f"{self.base_url}/api/v1/rmon/alarms/index/{index}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    print(f"    Alarm索引: {result_data.get('index')}")
                    print(f"    變量: {result_data.get('variable')}")
                    print(f"    間隔: {result_data.get('interval')} 秒")
                    print(f"    採樣類型: {result_data.get('sampleType')}")
                    print(f"    最後值: {result_data.get('lastValue')}")
                    print(f"    上升閾值: {result_data.get('risingThreshold')}")
                    print(f"    下降閾值: {result_data.get('fallingThreshold')}")
                    print(f"    狀態: {result_data.get('status')}")
                    print(f"    擁有者: {result_data.get('owner')}")
                        
            self.log_test(f"獲取alarm {index}", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"獲取alarm {index}", False, error=e)
            return None
    
    # ==================== 1.4 Delete an RMON alarm ====================
    
    def test_delete_alarm(self, index):
        """測試 1.4: 刪除RMON alarm"""
        try:
            url = f"{self.base_url}/api/v1/rmon/alarms/index/{index}"
            response = self.session.delete(url)
            
            success = response.status_code == 200
            if success:
                print(f"    成功刪除alarm {index}")
                if index in self.created_alarms:
                    self.created_alarms.remove(index)
            
            self.log_test(f"刪除alarm {index}", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"刪除alarm {index}", False, error=e)
            return None
    
    # ==================== 1.5 Get all RMON events ====================
    
    def test_get_all_events(self, start_id=1):
        """測試 1.5: 獲取所有RMON events"""
        try:
            url = f"{self.base_url}/api/v1/rmon/events"
            params = {"startId": start_id}
            response = self.session.get(url, params=params)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    start_id_resp = result_data.get('startId')
                    events = result_data.get('events', [])
                    
                    print(f"    起始ID: {start_id_resp}")
                    print(f"    找到 {len(events)} 個 event")
                    
                    for event in events[:3]:  # 顯示前3個
                        print(f"      Event {event.get('index')}:")
                        print(f"        社區: {event.get('community')}")
                        print(f"        描述: {event.get('description')}")
                        print(f"        事件類型: {event.get('eventType')}")
                        print(f"        狀態: {event.get('status')}")
                        print(f"        最後發送時間: {event.get('lastTimeSent')}")
                else:
                    print("    沒有找到 event")
                    
            self.log_test(f"獲取所有events (startId={start_id})", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"獲取所有events (startId={start_id})", False, error=e)
            return None
    
    # ==================== 1.6 Add an RMON event ====================
    
    def test_create_event(self, index, event_type="log", community="test", 
                         description="Test event", owner="test"):
        """測試 1.6: 創建RMON event"""
        try:
            url = f"{self.base_url}/api/v1/rmon/events"
            
            payload = {
                "index": index,
                "eventType": event_type,
                "community": community,
                "description": description,
                "owner": owner
            }
            
            response = self.session.post(url, json=payload)
            
            success = response.status_code == 200
            if success:
                self.created_events.append(index)
                print(f"    成功創建event {index}:")
                print(f"      事件類型: {event_type}")
                print(f"      社區: {community}")
                print(f"      描述: {description}")
                print(f"      擁有者: {owner}")
            
            self.log_test(f"創建event {index}", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"創建event {index}", False, error=e)
            return None
    
    # ==================== 1.7 Get an RMON event ====================
    
    def test_get_event(self, index):
        """測試 1.7: 獲取指定RMON event"""
        try:
            url = f"{self.base_url}/api/v1/rmon/events/index/{index}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    print(f"    Event索引: {result_data.get('index')}")
                    print(f"    社區: {result_data.get('community')}")
                    print(f"    描述: {result_data.get('description')}")
                    print(f"    事件類型: {result_data.get('eventType')}")
                    print(f"    擁有者: {result_data.get('owner')}")
                    print(f"    狀態: {result_data.get('status')}")
                    print(f"    最後發送時間: {result_data.get('lastTimeSent')}")
                        
            self.log_test(f"獲取event {index}", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"獲取event {index}", False, error=e)
            return None
    
    # ==================== 1.8 Delete an RMON event ====================
    
    def test_delete_event(self, index):
        """測試 1.8: 刪除RMON event"""
        try:
            url = f"{self.base_url}/api/v1/rmon/events/index/{index}"
            response = self.session.delete(url)
            
            success = response.status_code == 200
            if success:
                print(f"    成功刪除event {index}")
                if index in self.created_events:
                    self.created_events.remove(index)
            
            self.log_test(f"刪除event {index}", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"刪除event {index}", False, error=e)
            return None
    
    # ==================== 1.9 Get RMON collection histories ====================
    
    def test_get_all_histories(self, start_id=1):
        """測試 1.9: 獲取RMON collection histories"""
        try:
            url = f"{self.base_url}/api/v1/rmon/histories"
            params = {"startId": start_id}
            response = self.session.get(url, params=params)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    start_id_resp = result_data.get('startId')
                    histories = result_data.get('histories', [])
                    
                    print(f"    起始ID: {start_id_resp}")
                    print(f"    找到 {len(histories)} 個 history")
                    
                    for history in histories[:2]:  # 顯示前2個
                        print(f"      History {history.get('index')}:")
                        print(f"        狀態: {history.get('status')}")
                        print(f"        擁有者: {history.get('owner')}")
                        print(f"        數據源: {history.get('dataSource')}")
                        print(f"        間隔: {history.get('interval')} 秒")
                        print(f"        請求桶數: {history.get('bucketsRequested')}")
                        print(f"        授予桶數: {history.get('bucketsGranted')}")
                        
                        history_datas = history.get('historyDatas', [])
                        print(f"        歷史數據: {len(history_datas)} 條")
                else:
                    print("    沒有找到 history")
                    
            self.log_test(f"獲取所有histories (startId={start_id})", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"獲取所有histories (startId={start_id})", False, error=e)
            return None
    
    # ==================== 1.10 Add an RMON collection history ====================
    
    def test_create_history(self, interface_id, index, owner="test", buckets=50, interval=30):
        """測試 1.10: 創建RMON collection history"""
        try:
            url = f"{self.base_url}/api/v1/rmon/histories"
            
            payload = {
                "ifId": interface_id,
                "index": index,
                "owner": owner,
                "buckets": buckets,
                "interval": interval
            }
            
            response = self.session.post(url, json=payload)
            
            success = response.status_code == 200
            if success:
                self.created_histories.append((interface_id, index))
                print(f"    成功創建history {index}:")
                print(f"      接口: {interface_id}")
                print(f"      桶數: {buckets}")
                print(f"      間隔: {interval} 秒")
                print(f"      擁有者: {owner}")
            
            self.log_test(f"創建history {index} (接口: {interface_id})", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"創建history {index} (接口: {interface_id})", False, error=e)
            return None
    
    # ==================== 1.11 Get an RMON collection history ====================
    
    def test_get_history(self, interface_id, index):
        """測試 1.11: 獲取指定RMON collection history"""
        try:
            encoded_if_id = self.encode_interface_id(interface_id)
            url = f"{self.base_url}/api/v1/rmon/histories/interfaces/{encoded_if_id}/index/{index}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    print(f"    接口ID: {result_data.get('ifId')}")
                    print(f"    History索引: {result_data.get('index')}")
                    print(f"    狀態: {result_data.get('status')}")
                    print(f"    擁有者: {result_data.get('owner')}")
                    print(f"    數據源: {result_data.get('dataSource')}")
                    print(f"    間隔: {result_data.get('interval')} 秒")
                    print(f"    請求桶數: {result_data.get('bucketsRequested')}")
                    print(f"    授予桶數: {result_data.get('bucketsGranted')}")
                    
                    history_datas = result_data.get('historyDatas', [])
                    print(f"    歷史數據條數: {len(history_datas)}")
                    if history_datas:
                        sample_data = history_datas[0]
                        print(f"      樣本數據 (索引 {sample_data.get('index')}):")
                        print(f"        開始間隔: {sample_data.get('startInterval')}")
                        print(f"        丟棄事件: {sample_data.get('dropEvents')}")
                        print(f"        八位組: {sample_data.get('octets')}")
                        print(f"        數據包: {sample_data.get('packets')}")
                        
            self.log_test(f"獲取history {index} (接口: {interface_id})", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"獲取history {index} (接口: {interface_id})", False, error=e)
            return None
    
    # ==================== 1.12 Delete an RMON collection history ====================
    
    def test_delete_history(self, interface_id, index):
        """測試 1.12: 刪除RMON collection history"""
        try:
            encoded_if_id = self.encode_interface_id(interface_id)
            url = f"{self.base_url}/api/v1/rmon/histories/interfaces/{encoded_if_id}/index/{index}"
            response = self.session.delete(url)
            
            success = response.status_code == 200
            if success:
                print(f"    成功刪除history {index} (接口: {interface_id})")
                if (interface_id, index) in self.created_histories:
                    self.created_histories.remove((interface_id, index))
            
            self.log_test(f"刪除history {index} (接口: {interface_id})", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"刪除history {index} (接口: {interface_id})", False, error=e)
            return None
    
    # ==================== 1.13 Get RMON collection rmon1 statistics ====================
    
    def test_get_all_rmon1_statistics(self, start_id=1):
        """測試 1.13: 獲取RMON collection rmon1 statistics"""
        try:
            url = f"{self.base_url}/api/v1/rmon/rmon1"
            params = {"startId": start_id}
            response = self.session.get(url, params=params)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    start_id_resp = result_data.get('startId')
                    statistics = result_data.get('statistics', [])
                    
                    print(f"    起始ID: {start_id_resp}")
                    print(f"    找到 {len(statistics)} 個 rmon1 統計")
                    
                    for stat in statistics[:2]:  # 顯示前2個
                        print(f"      RMON1統計 {stat.get('index')}:")
                        print(f"        數據源: {stat.get('dataSource')}")
                        print(f"        丟棄事件: {stat.get('dropEvents')}")
                        print(f"        八位組: {stat.get('octets')}")
                        print(f"        數據包: {stat.get('packets')}")
                        print(f"        廣播包: {stat.get('brcastPkts')}")
                        print(f"        組播包: {stat.get('mcastPkts')}")
                        print(f"        CRC對齊錯誤: {stat.get('crcAlign')}")
                        print(f"        碰撞: {stat.get('collision')}")
                        print(f"        擁有者: {stat.get('owner')}")
                        print(f"        狀態: {stat.get('status')}")
                else:
                    print("    沒有找到 rmon1 統計")
                    
            self.log_test(f"獲取所有rmon1統計 (startId={start_id})", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"獲取所有rmon1統計 (startId={start_id})", False, error=e)
            return None
    
    # ==================== 1.14 Add an RMON collection rmon1 ====================
    
    def test_create_rmon1(self, interface_id, index, owner="test"):
        """測試 1.14: 創建RMON collection rmon1"""
        try:
            url = f"{self.base_url}/api/v1/rmon/rmon1"
            
            payload = {
                "ifId": interface_id,
                "index": index,
                "owner": owner
            }
            
            response = self.session.post(url, json=payload)
            
            success = response.status_code == 200
            if success:
                self.created_rmon1.append((interface_id, index))
                print(f"    成功創建rmon1 {index}:")
                print(f"      接口: {interface_id}")
                print(f"      擁有者: {owner}")
            
            self.log_test(f"創建rmon1 {index} (接口: {interface_id})", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"創建rmon1 {index} (接口: {interface_id})", False, error=e)
            return None
    
    # ==================== 1.15 Get an RMON collection rmon1 statistic ====================
    
    def test_get_rmon1_statistic(self, interface_id, index):
        """測試 1.15: 獲取指定RMON collection rmon1 statistic"""
        try:
            encoded_if_id = self.encode_interface_id(interface_id)
            url = f"{self.base_url}/api/v1/rmon/rmon1/interfaces/{encoded_if_id}/index/{index}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    print(f"    接口ID: {result_data.get('ifId')}")
                    print(f"    RMON1索引: {result_data.get('index')}")
                    print(f"    數據源: {result_data.get('dataSource')}")
                    print(f"    丟棄事件: {result_data.get('dropEvents')}")
                    print(f"    八位組: {result_data.get('octets')}")
                    print(f"    數據包: {result_data.get('packets')}")
                    print(f"    廣播包: {result_data.get('brcastPkts')}")
                    print(f"    組播包: {result_data.get('mcastPkts')}")
                    print(f"    CRC對齊錯誤: {result_data.get('crcAlign')}")
                    print(f"    過小包: {result_data.get('undersize')}")
                    print(f"    過大包: {result_data.get('oversize')}")
                    print(f"    碎片: {result_data.get('fragments')}")
                    print(f"    干擾: {result_data.get('jabbers')}")
                    print(f"    碰撞: {result_data.get('collision')}")
                    print(f"    64字節包: {result_data.get('pkts64')}")
                    print(f"    65-127字節包: {result_data.get('pkts65_127')}")
                    print(f"    128-255字節包: {result_data.get('pkts128_255')}")
                    print(f"    256-511字節包: {result_data.get('pkts256_511')}")
                    print(f"    512-1023字節包: {result_data.get('pkts512_1023')}")
                    print(f"    1024-1518字節包: {result_data.get('pkts1024_1518')}")
                    print(f"    擁有者: {result_data.get('owner')}")
                    print(f"    狀態: {result_data.get('status')}")
                        
            self.log_test(f"獲取rmon1統計 {index} (接口: {interface_id})", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"獲取rmon1統計 {index} (接口: {interface_id})", False, error=e)
            return None
    
    # ==================== 1.16 Delete an RMON collection rmon1 ====================
    
    def test_delete_rmon1(self, interface_id, index):
        """測試 1.16: 刪除RMON collection rmon1"""
        try:
            encoded_if_id = self.encode_interface_id(interface_id)
            url = f"{self.base_url}/api/v1/rmon/rmon1/interfaces/{encoded_if_id}/index/{index}"
            response = self.session.delete(url)
            
            success = response.status_code == 200
            if success:
                print(f"    成功刪除rmon1 {index} (接口: {interface_id})")
                if (interface_id, index) in self.created_rmon1:
                    self.created_rmon1.remove((interface_id, index))
            
            self.log_test(f"刪除rmon1 {index} (接口: {interface_id})", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"刪除rmon1 {index} (接口: {interface_id})", False, error=e)
            return None
    
    # ==================== 綜合測試場景 ====================
    
    def test_complete_rmon_workflow(self):
        """測試完整的RMON工作流程"""
        print("\n=== 完整RMON工作流程測試 ===")
        
        # 生成唯一的測試索引
        timestamp = int(time.time()) % 10000
        event_index = 50000 + timestamp
        alarm_index = 60000 + timestamp
        history_index = 70000 + timestamp
        rmon1_index = 80000 + timestamp
        test_interface = "eth1/1"
        
        try:
            # 步驟1: 創建Event
            print("\n步驟1: 創建RMON Event")
            self.test_create_event(
                index=event_index,
                event_type="log-and-trap",
                community="workflow_test",
                description="Complete workflow test event"
            )
            
            # 步驟2: 驗證Event創建
            print("\n步驟2: 驗證Event")
            self.test_get_event(event_index)
            
            # 步驟3: 創建Alarm並關聯Event
            print("\n步驟3: 創建RMON Alarm")
            self.test_create_alarm(
                index=alarm_index,
                variable="1.3.6.1.2.1.16.1.1.1.6.1",
                interval=60,
                sample_type="absolute",
                rising_threshold=1000000,
                falling_threshold=500000,
                rising_event_index=event_index,
                falling_event_index=event_index,
                owner="workflow_test"
            )
            
            # 步驟4: 驗證Alarm創建
            print("\n步驟4: 驗證Alarm")
            self.test_get_alarm(alarm_index)
            
            # 步驟5: 創建History
            print("\n步驟5: 創建RMON History")
            self.test_create_history(
                interface_id=test_interface,
                index=history_index,
                owner="workflow_test",
                buckets=100,
                interval=60
            )
            
            # 步驟6: 驗證History創建
            print("\n步驟6: 驗證History")
            self.test_get_history(test_interface, history_index)
            
            # 步驟7: 創建RMON1統計
            print("\n步驟7: 創建RMON1統計")
            self.test_create_rmon1(
                interface_id=test_interface,
                index=rmon1_index,
                owner="workflow_test"
            )
            
            # 步驟8: 驗證RMON1統計創建
            print("\n步驟8: 驗證RMON1統計")
            self.test_get_rmon1_statistic(test_interface, rmon1_index)
            
            # 步驟9: 清理資源（按依賴順序）
            print("\n步驟9: 清理測試資源")
            self.test_delete_alarm(alarm_index)  # 先刪除依賴Event的Alarm
            self.test_delete_event(event_index)  # 再刪除Event
            self.test_delete_history(test_interface, history_index)
            self.test_delete_rmon1(test_interface, rmon1_index)
            
            print("\n✓ 完整工作流程測試完成")
            
        except Exception as e:
            print(f"\n✗ 工作流程測試失敗: {e}")
    
    def test_parameter_validation(self):
        """測試參數驗證"""
        print("\n=== 參數驗證測試 ===")
        
        # 測試索引範圍
        index_test_cases = [
            (1, "最小索引"),
            (32768, "中等索引"),
            (65535, "最大索引")
        ]
        
        for index, description in index_test_cases:
            # 測試Event索引
            self.test_create_event(
                index=index,
                event_type="log",
                description=f"Index validation test - {description}"
            )
            time.sleep(0.5)
            self.test_delete_event(index)
        
        # 測試間隔範圍
        interval_test_cases = [
            (1, "最小間隔"),
            (1800, "中等間隔"),
            (31622400, "最大間隔")
        ]
        
        base_index = 55000
        for i, (interval, description) in enumerate(interval_test_cases):
            test_index = base_index + i
            self.test_create_alarm(
                index=test_index,
                variable="1.3.6.1.2.1.16.1.1.1.6.1",
                interval=interval,
                sample_type="absolute",
                rising_threshold=1000,
                falling_threshold=500
            )
            time.sleep(0.5)
            self.test_delete_alarm(test_index)
        
        # 測試閾值範圍
        threshold_test_cases = [
            (0, 2147483647, "邊界閾值"),
            (1000000, 500000, "常用閾值")
        ]
        
        for i, (rising, falling, description) in enumerate(threshold_test_cases):
            test_index = base_index + 10 + i
            self.test_create_alarm(
                index=test_index,
                variable="1.3.6.1.2.1.16.1.1.1.6.1",
                interval=50,
                sample_type="delta",
                rising_threshold=rising,
                falling_threshold=falling
            )
            time.sleep(0.5)
            self.test_delete_alarm(test_index)
    
    def test_error_scenarios(self):
        """測試錯誤場景"""
        print("\n=== 錯誤場景測試 ===")
        
        # 測試1: 創建重複索引的alarm
        try:
            duplicate_index = 99999
            # 先創建一個
            self.test_create_alarm(duplicate_index, "1.3.6.1.2.1.16.1.1.1.6.1")
            # 再創建同索引的
            url = f"{self.base_url}/api/v1/rmon/alarms"
            payload = {
                "index": duplicate_index,
                "variable": "1.3.6.1.2.1.16.1.1.1.6.2",
                "interval": 50,
                "sampleType": "absolute",
                "risingThreshold": 1000,
                "fallingThreshold": 500
            }
            response = self.session.post(url, json=payload)
            success = response.status_code == 500  # 應該返回錯誤
            self.log_test("創建重複索引alarm測試", success, response)
            # 清理
            self.test_delete_alarm(duplicate_index)
        except Exception as e:
            self.log_test("創建重複索引alarm測試", False, error=e)
        
        # 測試2: 獲取不存在的alarm
        try:
            url = f"{self.base_url}/api/v1/rmon/alarms/index/99998"
            response = self.session.get(url)
            success = response.status_code in [400, 404, 500]
            self.log_test("獲取不存在alarm測試", success, response)
        except Exception as e:
            self.log_test("獲取不存在alarm測試", False, error=e)
        
        # 測試3: 無效的變量OID
        try:
            url = f"{self.base_url}/api/v1/rmon/alarms"
            payload = {
                "index": 99997,
                "variable": "invalid.oid.format",
                "interval": 50,
                "sampleType": "absolute",
                "risingThreshold": 1000,
                "fallingThreshold": 500
            }
            response = self.session.post(url, json=payload)
            success = response.status_code == 400
            self.log_test("無效變量OID測試", success, response)
        except Exception as e:
            self.log_test("無效變量OID測試", False, error=e)
        
        # 測試4: 無效的接口ID
        try:
            url = f"{self.base_url}/api/v1/rmon/histories"
            payload = {
                "ifId": "invalid_interface",
                "index": 99996,
                "buckets": 50,
                "interval": 30
            }
            response = self.session.post(url, json=payload)
            success = response.status_code in [400, 500]
            self.log_test("無效接口ID測試", success, response)
        except Exception as e:
            self.log_test("無效接口ID測試", False, error=e)
        
        # 測試5: 超出範圍的參數
        try:
            url = f"{self.base_url}/api/v1/rmon/alarms"
            payload = {
                "index": 99995,
                "variable": "1.3.6.1.2.1.16.1.1.1.6.1",
                "interval": 50000000,  # 超出最大值
                "sampleType": "absolute",
                "risingThreshold": 1000,
                "fallingThreshold": 500
            }
            response = self.session.post(url, json=payload)
            success = response.status_code == 400
            self.log_test("超出範圍參數測試", success, response)
        except Exception as e:
            self.log_test("超出範圍參數測試", False, error=e)
        
        # 測試6: 無效JSON格式
        try:
            url = f"{self.base_url}/api/v1/rmon/events"
            response = self.session.post(url, data="invalid json")
            success = response.status_code == 400
            self.log_test("無效JSON格式測試", success, response)
        except Exception as e:
            self.log_test("無效JSON格式測試", False, error=e)
    
    def cleanup_test_resources(self):
        """清理測試資源"""
        print("\n=== 清理測試資源 ===")
        
        # 刪除所有測試的alarm（先刪除，因為可能依賴event）
        for alarm_index in self.created_alarms[:]:
            self.test_delete_alarm(alarm_index)
        
        # 刪除所有測試的event
        for event_index in self.created_events[:]:
            self.test_delete_event(event_index)
        
        # 刪除所有測試的history
        for interface_id, history_index in self.created_histories[:]:
            self.test_delete_history(interface_id, history_index)
        
        # 刪除所有測試的rmon1
        for interface_id, rmon1_index in self.created_rmon1[:]:
            self.test_delete_rmon1(interface_id, rmon1_index)
        
        print("    測試資源清理完成")
    
    def run_all_tests(self, test_interfaces=None):
        """運行所有測試"""
        if test_interfaces is None:
            test_interfaces = ["eth1/1", "eth1/2"]
        
        print("=== RMON REST API 測試開始 ===")
        print(f"測試目標: {self.base_url}")
        print(f"測試接口: {test_interfaces}")
        print("=" * 60)
        
        try:
            # 1. 基本功能測試 - Alarms
            print("\n=== RMON Alarms 基本功能測試 ===")
            self.test_get_all_alarms()
            
            # 創建測試用的event（用於alarm關聯）
            test_event_index = 50001
            self.test_create_event(
                index=test_event_index,
                event_type="log-and-trap",
                community="test_community",
                description="Test event for alarm association"
            )
            
            # 創建測試用的alarm
            test_alarm_index = 60001
            self.test_create_alarm(
                index=test_alarm_index,
                variable="1.3.6.1.2.1.16.1.1.1.6.1",
                interval=60,
                sample_type="absolute",
                rising_threshold=892800,
                falling_threshold=446400,
                rising_event_index=test_event_index,
                falling_event_index=test_event_index,
                owner="api_test"
            )
            
            self.test_get_alarm(test_alarm_index)
            
            # 2. 基本功能測試 - Events
            print("\n=== RMON Events 基本功能測試 ===")
            self.test_get_all_events()
            self.test_get_event(test_event_index)
            
            # 創建更多測試event
            for i, event_type in enumerate(["log", "trap", "log-and-trap"]):
                event_index = 50010 + i
                self.test_create_event(
                    index=event_index,
                    event_type=event_type,
                    community=f"test_comm_{i}",
                    description=f"Test {event_type} event"
                )
            
            # 3. 基本功能測試 - Histories
            print("\n=== RMON Histories 基本功能測試 ===")
            self.test_get_all_histories()
            
            # 為每個測試接口創建history
            for i, interface in enumerate(test_interfaces):
                history_index = 70010 + i
                self.test_create_history(
                    interface_id=interface,
                    index=history_index,
                    owner="api_test",
                    buckets=100,
                    interval=60
                )
                time.sleep(1)
                self.test_get_history(interface, history_index)
            
            # 4. 基本功能測試 - RMON1 Statistics
            print("\n=== RMON1 Statistics 基本功能測試 ===")
            self.test_get_all_rmon1_statistics()
            
            # 為每個測試接口創建rmon1統計
            for i, interface in enumerate(test_interfaces):
                rmon1_index = 80010 + i
                self.test_create_rmon1(
                    interface_id=interface,
                    index=rmon1_index,
                    owner="api_test"
                )
                time.sleep(1)
                self.test_get_rmon1_statistic(interface, rmon1_index)
            
            # 5. 完整工作流程測試
            self.test_complete_rmon_workflow()
            
            # 6. 參數驗證測試
            self.test_parameter_validation()
            
            # 7. 錯誤場景測試
            self.test_error_scenarios()
            
        finally:
            # 8. 清理測試資源
            self.cleanup_test_resources()
        
        # 9. 輸出測試總結
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
        alarm_tests = [r for r in self.test_results if 'alarm' in r['test_name']]
        event_tests = [r for r in self.test_results if 'event' in r['test_name']]
        history_tests = [r for r in self.test_results if 'history' in r['test_name']]
        rmon1_tests = [r for r in self.test_results if 'rmon1' in r['test_name']]
        validation_tests = [r for r in self.test_results if ('驗證' in r['test_name'] or '參數' in r['test_name'])]
        error_tests = [r for r in self.test_results if ('錯誤' in r['test_name'] or '無效' in r['test_name'])]
        
        print(f"\n功能測試統計:")
        print(f"  RMON Alarms: {len(alarm_tests)} 個測試")
        print(f"  RMON Events: {len(event_tests)} 個測試")
        print(f"  RMON Histories: {len(history_tests)} 個測試")
        print(f"  RMON1 Statistics: {len(rmon1_tests)} 個測試")
        print(f"  參數驗證測試: {len(validation_tests)} 個測試")
        print(f"  錯誤場景測試: {len(error_tests)} 個測試")
        
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
        with open('rmon_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        print(f"\n詳細測試結果已保存到: rmon_test_results.json")
        
        # 輸出創建的資源統計
        print(f"\n測試過程統計:")
        print(f"  創建的Alarms: {len(self.created_alarms)}")
        print(f"  創建的Events: {len(self.created_events)}")
        print(f"  創建的Histories: {len(self.created_histories)}")
        print(f"  創建的RMON1統計: {len(self.created_rmon1)}")

def main():
    """主函數"""
    if len(sys.argv) < 2:
        print("使用方法: python rmon_test.py <base_url> [username] [password]")
        print("範例: python rmon_test.py http://192.168.1.1 admin admin123")
        print("\n功能說明:")
        print("  - 測試所有RMON API功能 (Alarms, Events, Histories, RMON1)")
        print("  - 包含完整工作流程測試")
        print("  - 自動清理測試資源")
        print("  - 生成詳細測試報告")
        print("\n注意事項:")
        print("  - 接口ID格式: eth1/1 會自動轉換為 eth1%2f1")
        print("  - 測試會創建臨時的RMON配置，完成後自動清理")
        print("  - 建議在測試環境中運行")
        sys.exit(1)
    
    base_url = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else None
    password = sys.argv[3] if len(sys.argv) > 3 else None
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    
    # 創建測試器並運行測試
    tester = RMONAPITester(base_url, username, password)
    
    # 可以自定義測試接口
    test_interfaces = ["eth1/1", "eth1/2"]
    
    try:
        tester.run_all_tests(test_interfaces)
    except KeyboardInterrupt:
        print("\n測試被用戶中斷")
        print("正在清理測試資源...")
        tester.cleanup_test_resources()
    except Exception as e:
        print(f"\n測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        print("正在清理測試資源...")
        tester.cleanup_test_resources()

if __name__ == "__main__":
    main()