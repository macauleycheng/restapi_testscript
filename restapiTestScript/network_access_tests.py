#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Network Access REST API 測試腳本
基於 Network_Access_API_Reference_v0.1.docx 文件生成
包含 MAC Authentication 和 Secure MAC 功能測試
# 基本使用
python network_access_test.py http://192.168.1.1

# 帶認證
python network_access_test.py http://192.168.1.1 admin admin123

# 啟用MAC地址刪除測試
ENABLE_DELETE_TESTS=true python network_access_test.py http://192.168.1.1 admin admin123
"""

import requests
import json
import sys
import time
from urllib.parse import quote
import re

class NetworkAccessAPITester:
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
        self.test_mac_addresses = []  # 用於存儲測試過程中發現的MAC地址
    
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
    
    def validate_mac_address(self, mac_address):
        """驗證MAC地址格式"""
        # 支持多種MAC地址格式
        patterns = [
            r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})
這個 Network Access API 測試腳本包含以下功能：,  # AA:BB:CC:DD:EE:FF 或 AA-BB-CC-DD-EE-FF
            r'^([0-9A-Fa-f]{4}\.){2}([0-9A-Fa-f]{4})
這個 Network Access API 測試腳本包含以下功能：      # AABB.CCDD.EEFF
        ]
        return any(re.match(pattern, mac_address) for pattern in patterns)
    
    def test_get_mac_auth_interface(self, interface_id="eth1/1"):
        """測試獲取接口的MAC認證設置"""
        try:
            encoded_if_id = quote(interface_id, safe='')
            url = f"{self.base_url}/api/v1/network-access/mac-auth/interfaces/{encoded_if_id}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                # 驗證響應結構
                if 'result' in data:
                    result_data = data['result']
                    required_fields = ['ifId', 'status', 'action', 'maxMacCount']
                    missing_fields = [field for field in required_fields if field not in result_data]
                    if missing_fields:
                        print(f"    缺少字段: {missing_fields}")
                        success = False
                    else:
                        print(f"    接口: {result_data.get('ifId')}")
                        print(f"    MAC認證狀態: {result_data.get('status')}")
                        print(f"    失敗動作: {result_data.get('action')}")
                        print(f"    最大MAC數量: {result_data.get('maxMacCount')}")
                else:
                    success = False
                    
            self.log_test(f"獲取接口{interface_id}的MAC認證設置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"獲取接口{interface_id}的MAC認證設置", False, error=e)
            return None
    
    def test_set_mac_auth_interface(self, interface_id="eth1/1", status=True, action="block", max_mac_count=1024):
        """測試設置接口的MAC認證配置"""
        try:
            encoded_if_id = quote(interface_id, safe='')
            url = f"{self.base_url}/api/v1/network-access/mac-auth/interfaces/{encoded_if_id}"
            
            payload = {}
            
            # 添加可選參數
            if status is not None:
                payload["status"] = status
            if action:
                payload["action"] = action
            if max_mac_count:
                payload["maxMacCount"] = max_mac_count
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置MAC認證: 狀態={status}, 動作={action}, 最大MAC數={max_mac_count}")
            
            self.log_test(f"設置接口{interface_id}的MAC認證配置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"設置接口{interface_id}的MAC認證配置", False, error=e)
            return None
    
    def test_get_all_secure_mac(self):
        """測試獲取所有已認證的MAC地址"""
        try:
            url = f"{self.base_url}/api/v1/network-access/secure-mac"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'result' in data and 'entries' in data['result']:
                    entries = data['result']['entries']
                    print(f"    找到 {len(entries)} 個已認證的MAC地址")
                    
                    # 存儲MAC地址用於後續測試
                    self.test_mac_addresses = []
                    for entry in entries[:3]:  # 只取前3個用於測試
                        mac_addr = entry.get('macAddress')
                        if mac_addr:
                            self.test_mac_addresses.append(mac_addr)
                            print(f"      MAC: {mac_addr}, 接口: {entry.get('ifId')}, "
                                  f"服務器: {entry.get('server')}, 類型: {entry.get('attribute')}")
                else:
                    print("    沒有找到已認證的MAC地址")
                    
            self.log_test("獲取所有已認證的MAC地址", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取所有已認證的MAC地址", False, error=e)
            return None
    
    def test_get_secure_mac_by_interface(self, interface_id="eth1/1"):
        """測試獲取指定接口的已認證MAC地址"""
        try:
            encoded_if_id = quote(interface_id, safe='')
            url = f"{self.base_url}/api/v1/network-access/secure-mac/interfaces/{encoded_if_id}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'result' in data and 'entries' in data['result']:
                    entries = data['result']['entries']
                    print(f"    接口 {interface_id} 上有 {len(entries)} 個已認證的MAC地址")
                    
                    for entry in entries:
                        mac_addr = entry.get('macAddress')
                        if mac_addr and mac_addr not in self.test_mac_addresses:
                            self.test_mac_addresses.append(mac_addr)
                        print(f"      MAC: {mac_addr}, 服務器: {entry.get('server')}, "
                              f"時間: {entry.get('time')}, 類型: {entry.get('attribute')}")
                else:
                    print(f"    接口 {interface_id} 上沒有已認證的MAC地址")
                    
            self.log_test(f"獲取接口{interface_id}的已認證MAC地址", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"獲取接口{interface_id}的已認證MAC地址", False, error=e)
            return None
    
    def test_delete_secure_mac(self, mac_address):
        """測試刪除已認證的MAC地址"""
        try:
            # 驗證MAC地址格式
            if not self.validate_mac_address(mac_address):
                raise ValueError(f"無效的MAC地址格式: {mac_address}")
            
            # URL編碼MAC地址
            encoded_mac = quote(mac_address, safe='')
            url = f"{self.base_url}/api/v1/network-access/secure-mac/macs/{encoded_mac}"
            response = self.session.delete(url)
            
            success = response.status_code == 200
            if success:
                print(f"    成功刪除MAC地址: {mac_address}")
            
            self.log_test(f"刪除已認證MAC地址 {mac_address}", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"刪除已認證MAC地址 {mac_address}", False, error=e)
            return None
    
    def test_mac_auth_scenarios(self, interface_id="eth1/1"):
        """測試MAC認證的各種場景"""
        print(f"\n=== 接口 {interface_id} MAC認證場景測試 ===")
        
        # 場景1: 啟用MAC認證，設置為block模式
        print("\n場景1: 啟用MAC認證 (block模式)")
        self.test_set_mac_auth_interface(interface_id, True, "block", 50)
        time.sleep(1)
        self.test_get_mac_auth_interface(interface_id)
        
        # 場景2: 修改為pass模式
        print("\n場景2: 修改為pass模式")
        self.test_set_mac_auth_interface(interface_id, True, "pass", 100)
        time.sleep(1)
        self.test_get_mac_auth_interface(interface_id)
        
        # 場景3: 禁用MAC認證
        print("\n場景3: 禁用MAC認證")
        self.test_set_mac_auth_interface(interface_id, False, "block", 1024)
        time.sleep(1)
        self.test_get_mac_auth_interface(interface_id)
        
        # 場景4: 測試最大MAC數量限制
        print("\n場景4: 測試不同的最大MAC數量")
        for max_count in [1, 10, 512, 1024]:
            self.test_set_mac_auth_interface(interface_id, True, "trap", max_count)
            time.sleep(0.5)
    
    def test_error_scenarios(self):
        """測試錯誤場景"""
        print("\n=== 錯誤場景測試 ===")
        
        # 測試1: 無效接口ID
        try:
            url = f"{self.base_url}/api/v1/network-access/mac-auth/interfaces/invalid_interface"
            response = self.session.get(url)
            success = response.status_code in [400, 404, 500]
            self.log_test("無效接口ID測試 (MAC認證)", success, response)
        except Exception as e:
            self.log_test("無效接口ID測試 (MAC認證)", False, error=e)
        
        # 測試2: 無效JSON格式
        try:
            url = f"{self.base_url}/api/v1/network-access/mac-auth/interfaces/eth1%2f1"
            response = self.session.put(url, data="invalid json")
            success = response.status_code == 400
            self.log_test("無效JSON格式測試", success, response)
        except Exception as e:
            self.log_test("無效JSON格式測試", False, error=e)
        
        # 測試3: 無效參數值
        try:
            url = f"{self.base_url}/api/v1/network-access/mac-auth/interfaces/eth1%2f1"
            payload = {
                "status": "invalid_boolean",
                "action": "invalid_action",
                "maxMacCount": -1
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            self.log_test("無效參數值測試", success, response)
        except Exception as e:
            self.log_test("無效參數值測試", False, error=e)
        
        # 測試4: 無效MAC地址格式
        try:
            url = f"{self.base_url}/api/v1/network-access/secure-mac/macs/invalid_mac_address"
            response = self.session.delete(url)
            success = response.status_code in [400, 404]
            self.log_test("無效MAC地址格式測試", success, response)
        except Exception as e:
            self.log_test("無效MAC地址格式測試", False, error=e)
        
        # 測試5: 刪除不存在的MAC地址
        try:
            fake_mac = "FF-FF-FF-FF-FF-FF"
            encoded_mac = quote(fake_mac, safe='')
            url = f"{self.base_url}/api/v1/network-access/secure-mac/macs/{encoded_mac}"
            response = self.session.delete(url)
            success = response.status_code in [400, 404, 500]
            self.log_test("刪除不存在MAC地址測試", success, response)
        except Exception as e:
            self.log_test("刪除不存在MAC地址測試", False, error=e)
    
    def test_boundary_conditions(self):
        """測試邊界條件"""
        print("\n=== 邊界條件測試 ===")
        
        # 測試最小和最大MAC數量
        test_interface = "eth1/1"
        
        # 最小值測試
        self.test_set_mac_auth_interface(test_interface, True, "block", 1)
        
        # 最大值測試
        self.test_set_mac_auth_interface(test_interface, True, "block", 1024)
        
        # 超出範圍測試
        try:
            encoded_if_id = quote(test_interface, safe='')
            url = f"{self.base_url}/api/v1/network-access/mac-auth/interfaces/{encoded_if_id}"
            payload = {"maxMacCount": 2000}  # 超出1024的限制
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            self.log_test("超出MAC數量範圍測試", success, response)
        except Exception as e:
            self.log_test("超出MAC數量範圍測試", False, error=e)
    
    def run_all_tests(self, test_interfaces=None):
        """運行所有測試"""
        if test_interfaces is None:
            test_interfaces = ["eth1/1", "eth1/2", "eth1/13"]
        
        print("=== Network Access REST API 測試開始 ===")
        print(f"測試目標: {self.base_url}")
        print(f"測試接口: {test_interfaces}")
        print("=" * 60)
        
        # 1. 獲取所有已認證MAC地址
        print("\n=== Secure MAC 功能測試 ===")
        self.test_get_all_secure_mac()
        
        # 2. 對每個測試接口進行MAC認證測試
        for interface in test_interfaces:
            print(f"\n=== 接口 {interface} MAC認證基本測試 ===")
            
            # 獲取當前MAC認證設置
            self.test_get_mac_auth_interface(interface)
            
            # 獲取該接口的已認證MAC地址
            self.test_get_secure_mac_by_interface(interface)
            
            time.sleep(1)
        
        # 3. 詳細場景測試（使用第一個接口）
        if test_interfaces:
            self.test_mac_auth_scenarios(test_interfaces[0])
        
        # 4. 邊界條件測試
        self.test_boundary_conditions()
        
        # 5. MAC地址刪除測試
        if self.test_mac_addresses:
            print(f"\n=== MAC地址刪除測試 ===")
            print(f"注意: 這將刪除實際的MAC地址條目，請確認是否繼續...")
            
            # 為了安全起見，只在測試環境中執行刪除操作
            # 可以通過環境變量或配置來控制
            import os
            if os.getenv('ENABLE_DELETE_TESTS', 'false').lower() == 'true':
                for mac_addr in self.test_mac_addresses[:2]:  # 只刪除前2個
                    self.test_delete_secure_mac(mac_addr)
                    time.sleep(1)
            else:
                print("    跳過MAC地址刪除測試 (設置 ENABLE_DELETE_TESTS=true 來啟用)")
        
        # 6. 錯誤場景測試
        self.test_error_scenarios()
        
        # 7. 輸出測試總結
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
        mac_auth_tests = [r for r in self.test_results if 'MAC認證' in r['test_name']]
        secure_mac_tests = [r for r in self.test_results if ('MAC地址' in r['test_name'] or 'secure-mac' in r['test_name'])]
        error_tests = [r for r in self.test_results if '錯誤' in r['test_name'] or '無效' in r['test_name']]
        
        print(f"\n功能測試統計:")
        print(f"  MAC認證功能: {len(mac_auth_tests)} 個測試")
        print(f"  Secure MAC功能: {len(secure_mac_tests)} 個測試")
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
        with open('network_access_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        print(f"\n詳細測試結果已保存到: network_access_test_results.json")
        
        # 輸出發現的MAC地址
        if self.test_mac_addresses:
            print(f"\n測試過程中發現的MAC地址:")
            for mac in self.test_mac_addresses:
                print(f"  - {mac}")

def main():
    """主函數"""
    if len(sys.argv) < 2:
        print("使用方法: python network_access_test.py <base_url> [username] [password]")
        print("範例: python network_access_test.py http://192.168.1.1 admin admin123")
        print("\n環境變量:")
        print("  ENABLE_DELETE_TESTS=true  # 啟用MAC地址刪除測試")
        sys.exit(1)
    
    base_url = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else None
    password = sys.argv[3] if len(sys.argv) > 3 else None
    
    # 創建測試器並運行測試
    tester = NetworkAccessAPITester(base_url, username, password)
    
    # 可以自定義測試接口
    test_interfaces = ["eth1/1", "eth1/2", "eth1/13"]
    
    try:
        tester.run_all_tests(test_interfaces)
    except KeyboardInterrupt:
        print("\n測試被用戶中斷")
    except Exception as e:
        print(f"\n測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()