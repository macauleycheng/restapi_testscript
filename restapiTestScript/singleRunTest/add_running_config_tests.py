#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Running Config REST API 測試腳本
測試所有運行配置相關的 API 端點
版本: v0.11
"""

import requests
import json
import sys
import time
import os
from typing import Dict, Any, Optional
import hashlib

class AddRunningConfigAPITester:
    def __init__(self, base_url: str = "http://localhost", username: str = "admin", password: str = "admin"):
        """
        初始化測試器
        
        Args:
            base_url: API 基礎 URL
            username: 認證用戶名
            password: 認證密碼
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.test_results = []
        self.transaction_ids = []  # 儲存創建的 transaction ID
        
    def log_test(self, test_name: str, success: bool, response: requests.Response = None, error: str = None):
        """記錄測試結果"""
        result = {
            'test_name': test_name,
            'success': success,
            'status_code': response.status_code if response else None,
            'response_data': response.json() if response and response.headers.get('content-type', '').startswith('application/json') else None,
            'error': error
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if response:
            print(f"    狀態碼: {response.status_code}")
            if success and result['response_data']:
                if 'result' in result['response_data']:
                    res_data = result['response_data']['result']
                    if 'transactionId' in res_data:
                        print(f"    Transaction ID: {res_data['transactionId']}")
                    if 'status' in res_data:
                        print(f"    狀態: {res_data['status']}")
        if error:
            print(f"    錯誤: {error}")
        print()

    def create_test_config_file(self, filepath: str = "/tmp/test-config"):
        """創建測試用的配置文件"""
        try:
            config_content = """!
vlan database
vlan 200 name test_vlan media ethernet state active
!
interface ethernet 1/5
switchport mode access
switchport access vlan 200
!
"""
            # 模擬文件創建（實際環境中需要確保文件存在於目標設備上）
            print(f"📝 模擬創建配置文件: {filepath}")
            print(f"    內容預覽:\n{config_content}")
            return filepath
        except Exception as e:
            print(f"❌ 創建配置文件失敗: {str(e)}")
            return None

    def test_update_running_config_with_commands(self):
        """測試 1.1: 使用 commands 更新運行配置"""
        try:
            url = f"{self.base_url}/api/v1/running-config"
            payload = {
                "username": self.username,
                "password": self.password,
                "opertype": "commands",
                "commands": [
                    "!",
                    "vlan database",
                    "vlan 100 name vlan100 media ethernet state active",
                    "!",
                    "interface ethernet 1/10",
                    "switchport mode access"
                ]
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                transaction_id = data.get('result', {}).get('transactionId')
                if transaction_id:
                    self.transaction_ids.append(transaction_id)
                    
            self.log_test("更新運行配置 (commands 模式)", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("更新運行配置 (commands 模式)", False, error=str(e))
            return None

    def test_update_running_config_with_filepath(self):
        """測試 1.1: 使用 filepath 更新運行配置"""
        try:
            # 先創建測試配置文件
            test_filepath = self.create_test_config_file("/tmp/apply-config")
            if not test_filepath:
                self.log_test("更新運行配置 (filepath 模式)", False, error="無法創建測試配置文件")
                return None
                
            url = f"{self.base_url}/api/v1/running-config"
            payload = {
                "username": self.username,
                "password": self.password,
                "opertype": "filepath",
                "filepath": test_filepath
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                transaction_id = data.get('result', {}).get('transactionId')
                if transaction_id:
                    self.transaction_ids.append(transaction_id)
                    
            self.log_test("更新運行配置 (filepath 模式)", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("更新運行配置 (filepath 模式)", False, error=str(e))
            return None

    def test_get_running_config(self, transaction_id: int):
        """測試 1.2: 獲取運行配置狀態"""
        try:
            url = f"{self.base_url}/api/v1/running-config"
            params = {"transactionId": transaction_id}
            
            response = self.session.get(url, params=params)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                result = data.get('result', {})
                print(f"    Transaction ID: {result.get('transactionId')}")
                print(f"    狀態: {result.get('status')}")
                if 'commands' in result:
                    print(f"    命令預覽: {result['commands'][:100]}...")
                if 'filepath' in result:
                    print(f"    文件路徑: {result['filepath']}")
                    
            self.log_test(f"獲取運行配置狀態 (ID: {transaction_id})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取運行配置狀態 (ID: {transaction_id})", False, error=str(e))
            return None

    def test_delete_running_config(self, transaction_id: int):
        """測試 1.3: 刪除運行配置事務"""
        try:
            url = f"{self.base_url}/api/v1/running-config"
            params = {"transactionId": transaction_id}
            
            response = self.session.delete(url, params=params)
            success = response.status_code == 200
            
            self.log_test(f"刪除運行配置事務 (ID: {transaction_id})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"刪除運行配置事務 (ID: {transaction_id})", False, error=str(e))
            return False

    def test_error_scenarios(self):
        """測試錯誤場景"""
        print("\n🚨 錯誤場景測試")
        print("-" * 30)
        
        # 測試認證失敗
        self.test_authentication_failure()
        
        # 測試無效參數
        self.test_invalid_parameters()
        
        # 測試缺少參數
        self.test_missing_parameters()
        
        # 測試不存在的事務ID
        self.test_nonexistent_transaction()

    def test_authentication_failure(self):
        """測試認證失敗"""
        try:
            url = f"{self.base_url}/api/v1/running-config"
            payload = {
                "username": "invalid_user",
                "password": "invalid_pass",
                "opertype": "commands",
                "commands": ["!"]
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 403
            
            if success:
                data = response.json()
                print(f"    錯誤代碼: {data.get('code')}")
                print(f"    錯誤訊息: {data.get('message')}")
                
            self.log_test("認證失敗測試", success, response)
            
        except Exception as e:
            self.log_test("認證失敗測試", False, error=str(e))

    def test_invalid_parameters(self):
        """測試無效參數"""
        try:
            url = f"{self.base_url}/api/v1/running-config"
            payload = {
                "username": self.username,
                "password": self.password,
                "opertype": "invalid_type",  # 無效的操作類型
                "commands": ["!"]
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            
            if success:
                data = response.json()
                print(f"    錯誤代碼: {data.get('code')}")
                print(f"    錯誤訊息: {data.get('message')}")
                
            self.log_test("無效參數測試", success, response)
            
        except Exception as e:
            self.log_test("無效參數測試", False, error=str(e))

    def test_missing_parameters(self):
        """測試缺少參數"""
        try:
            url = f"{self.base_url}/api/v1/running-config"
            payload = {
                "username": self.username,
                "password": self.password,
                "opertype": "commands"
                # 缺少 commands 參數
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            
            if success:
                data = response.json()
                print(f"    錯誤代碼: {data.get('code')}")
                print(f"    錯誤訊息: {data.get('message')}")
                
            self.log_test("缺少參數測試", success, response)
            
        except Exception as e:
            self.log_test("缺少參數測試", False, error=str(e))

    def test_nonexistent_transaction(self):
        """測試不存在的事務ID"""
        try:
            url = f"{self.base_url}/api/v1/running-config"
            params = {"transactionId": 99999}  # 不存在的事務ID
            
            response = self.session.get(url, params=params)
            success = response.status_code == 404
            
            if success:
                data = response.json()
                print(f"    錯誤代碼: {data.get('code')}")
                print(f"    錯誤訊息: {data.get('message')}")
                
            self.log_test("不存在事務ID測試", success, response)
            
        except Exception as e:
            self.log_test("不存在事務ID測試", False, error=str(e))

    def test_large_commands_array(self):
        """測試大型命令陣列（接近1K限制）"""
        try:
            # 創建接近1K字節的命令陣列
            large_commands = ["!"]
            for i in range(1, 50):  # 創建多個VLAN命令
                large_commands.append(f"vlan {i + 100} name test_vlan_{i}")
            
            url = f"{self.base_url}/api/v1/running-config"
            payload = {
                "username": self.username,
                "password": self.password,
                "opertype": "commands",
                "commands": large_commands
            }
            
            # 計算payload大小
            payload_size = len(json.dumps(payload['commands']))
            print(f"    命令陣列大小: {payload_size} 字節")
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                transaction_id = data.get('result', {}).get('transactionId')
                if transaction_id:
                    self.transaction_ids.append(transaction_id)
                    
            self.log_test("大型命令陣列測試", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("大型命令陣列測試", False, error=str(e))
            return None

    def wait_for_transaction_completion(self, transaction_id: int, max_wait: int = 30):
        """等待事務完成"""
        print(f"⏳ 等待事務 {transaction_id} 完成...")
        
        for i in range(max_wait):
            try:
                url = f"{self.base_url}/api/v1/running-config"
                params = {"transactionId": transaction_id}
                response = self.session.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get('result', {}).get('status')
                    print(f"    第 {i+1} 次檢查 - 狀態: {status}")
                    
                    if status == "Done":
                        print(f"✅ 事務 {transaction_id} 已完成")
                        return True
                    elif status == "Failed":
                        print(f"❌ 事務 {transaction_id} 執行失敗")
                        return False
                        
                time.sleep(1)
                
            except Exception as e:
                print(f"    檢查事務狀態時發生錯誤: {str(e)}")
                
        print(f"⏰ 等待事務 {transaction_id} 完成超時")
        return False

    def run_all_tests(self):
        """執行所有測試"""
        print("=" * 60)
        print("開始執行 Add Running Config API 測試")
        print("=" * 60)
        print(f"API 基礎 URL: {self.base_url}")
        print(f"認證用戶: {self.username}")
        print()
        
        # 1. 基本功能測試
        print("📋 基本功能測試")
        print("-" * 30)
        
        # 測試使用 commands 更新配置
        result1 = self.test_update_running_config_with_commands()
        
        # 測試使用 filepath 更新配置
        result2 = self.test_update_running_config_with_filepath()
        
        # 2. 查詢測試
        print("\n🔍 查詢測試")
        print("-" * 30)
        
        # 查詢已創建的事務
        for transaction_id in self.transaction_ids:
            self.test_get_running_config(transaction_id)
            
        # 3. 等待事務完成
        if self.transaction_ids:
            print("\n⏳ 等待事務完成")
            print("-" * 30)
            for transaction_id in self.transaction_ids[:2]:  # 只等待前兩個事務
                self.wait_for_transaction_completion(transaction_id, max_wait=10)
        
        # 4. 進階測試
        print("\n🔧 進階測試")
        print("-" * 30)
        self.test_large_commands_array()
        
        # 5. 錯誤場景測試
        self.test_error_scenarios()
        
        # 6. 清理測試
        print("\n🗑️ 清理測試")
        print("-" * 30)
        
        # 嘗試刪除已完成的事務（某些可能無法刪除正在運行的事務）
        for transaction_id in self.transaction_ids:
            # 先檢查狀態
            result = self.test_get_running_config(transaction_id)
            if result:
                status = result.get('result', {}).get('status')
                if status in ["Done", "Failed"]:
                    self.test_delete_running_config(transaction_id)
                else:
                    print(f"⚠️  跳過刪除運行中的事務 {transaction_id} (狀態: {status})")
        
        # 7. 測試結果統計
        self.print_test_summary()

    def print_test_summary(self):
        """打印測試結果摘要"""
        print("\n" + "=" * 60)
        print("測試結果摘要")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"總測試數: {total_tests}")
        print(f"通過: {passed_tests} ✅")
        print(f"失敗: {failed_tests} ❌")
        print(f"成功率: {(passed_tests/total_tests)*100:.1f}%")
        
        if self.transaction_ids:
            print(f"\n創建的事務ID: {self.transaction_ids}")
        
        if failed_tests > 0:
            print("\n失敗的測試:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test_name']}")
                    if result['error']:
                        print(f"    錯誤: {result['error']}")
                    elif result['status_code']:
                        print(f"    狀態碼: {result['status_code']}")

def main():
    """主函數"""
    print("Add Running Config API 測試工具")
    print("=" * 40)
    
    # 獲取配置參數
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = input("請輸入 API 基礎 URL (預設: http://localhost): ").strip()
        if not base_url:
            base_url = "http://localhost"
    
    username = input("請輸入用戶名 (預設: admin): ").strip()
    if not username:
        username = "admin"
        
    password = input("請輸入密碼 (預設: admin): ").strip()
    if not password:
        password = "admin"
    
    print(f"\n使用配置:")
    print(f"  API URL: {base_url}")
    print(f"  用戶名: {username}")
    print(f"  密碼: {'*' * len(password)}")
    
    confirm = input("\n確認開始測試? (y/N): ").strip().lower()
    if confirm != 'y':
        print("測試已取消")
        return
    
    # 創建測試器並執行測試
    tester = AddRunningConfigAPITester(base_url, username, password)
    tester.run_all_tests()

if __name__ == "__main__":
    main()