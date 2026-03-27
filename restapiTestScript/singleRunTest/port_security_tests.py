#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Port Security REST API 測試腳本
基於 PortSecurity_API_Reference_v0.12.docx 文件生成
# 基本使用
python port_security_test.py http://192.168.1.1

# 帶認證
python port_security_test.py http://192.168.1.1 admin admin123
"""

import requests
import json
import sys
import time
from urllib.parse import quote
import hashlib

class PortSecurityAPITester:
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
    
    def log_test(self, test_name, success, response=None, error=None):
        """記錄測試結果"""
        result = {
            'test_name': test_name,
            'success': success,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if response:
            result['status_code'] = response.status_code
            result['response'] = response.json() if response.content else {}
        
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
    
    def test_get_all_port_security(self):
        """測試 1.1: 獲取所有接口的 Port Security 配置"""
        try:
            url = f"{self.base_url}/api/v1/port-security/interfaces"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                # 驗證響應結構
                if 'result' in data and 'portSecurity' in data['result']:
                    print(f"    找到 {len(data['result']['portSecurity'])} 個接口配置")
                else:
                    success = False
                    
            self.log_test("獲取所有接口Port Security配置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取所有接口Port Security配置", False, error=e)
            return None
    
    def test_get_single_port_security(self, interface_id="eth1/1"):
        """測試 1.2: 獲取單個接口的 Port Security 配置"""
        try:
            # URL編碼接口ID
            encoded_if_id = quote(interface_id, safe='')
            url = f"{self.base_url}/api/v1/port-security/interfaces/{encoded_if_id}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                # 驗證響應包含必要字段
                required_fields = ['ifId', 'portStatus', 'action', 'maxMacCount', 'currMacCount', 'aging']
                if 'result' in data:
                    result_data = data['result']
                    missing_fields = [field for field in required_fields if field not in result_data]
                    if missing_fields:
                        print(f"    缺少字段: {missing_fields}")
                        success = False
                    else:
                        print(f"    接口: {result_data.get('ifId')}, 狀態: {result_data.get('portStatus')}")
                        
            self.log_test(f"獲取接口{interface_id}的Port Security配置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"獲取接口{interface_id}的Port Security配置", False, error=e)
            return None
    
    def test_update_port_security(self, interface_id="eth1/1", port_status=True, action="trap", max_mac_count=512):
        """測試 1.3: 更新接口的 Port Security 配置"""
        try:
            encoded_if_id = quote(interface_id, safe='')
            url = f"{self.base_url}/api/v1/port-security/interfaces/{encoded_if_id}"
            
            payload = {
                "portStatus": port_status
            }
            
            # 添加可選參數
            if action:
                payload["action"] = action
            if max_mac_count:
                payload["maxMacCount"] = max_mac_count
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            self.log_test(f"更新接口{interface_id}的Port Security配置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"更新接口{interface_id}的Port Security配置", False, error=e)
            return None
    
    def test_save_mac_as_permanent(self, interface_id="eth1/1"):
        """測試 1.4: 將學習到的MAC地址保存為靜態條目"""
        try:
            encoded_if_id = quote(interface_id, safe='')
            url = f"{self.base_url}/api/v1/port-security/interfaces:mac-as-permanent"
            params = {"ifId": interface_id}
            
            response = self.session.put(url, params=params)
            
            success = response.status_code == 200
            self.log_test(f"保存接口{interface_id}的MAC地址為靜態條目", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"保存接口{interface_id}的MAC地址為靜態條目", False, error=e)
            return None
    
    def test_get_mac_learning(self, interface_id="eth1/1"):
        """測試 1.5: 獲取MAC學習狀態"""
        try:
            encoded_if_id = quote(interface_id, safe='')
            url = f"{self.base_url}/api/v1/mac-learning/interfaces/{encoded_if_id}"
            
            response = self.session.get(url)
            
            success = response.status_code == 200
            self.log_test(f"獲取接口{interface_id}的MAC學習狀態", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"獲取接口{interface_id}的MAC學習狀態", False, error=e)
            return None
    
    def test_update_mac_learning(self, interface_id="eth1/1", status=True):
        """測試 1.6: 更新MAC學習狀態"""
        try:
            encoded_if_id = quote(interface_id, safe='')
            url = f"{self.base_url}/api/v1/mac-learning/interfaces/{encoded_if_id}"
            
            payload = {"status": status}
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            self.log_test(f"更新接口{interface_id}的MAC學習狀態", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"更新接口{interface_id}的MAC學習狀態", False, error=e)
            return None
    
    def test_error_scenarios(self):
        """測試錯誤場景"""
        print("\n=== 錯誤場景測試 ===")
        
        # 測試無效接口ID
        try:
            url = f"{self.base_url}/api/v1/port-security/interfaces/invalid_interface"
            response = self.session.get(url)
            success = response.status_code in [400, 404, 500]
            self.log_test("無效接口ID測試", success, response)
        except Exception as e:
            self.log_test("無效接口ID測試", False, error=e)
        
        # 測試無效JSON
        try:
            url = f"{self.base_url}/api/v1/port-security/interfaces/eth1%2f1"
            response = self.session.put(url, data="invalid json")
            success = response.status_code == 400
            self.log_test("無效JSON測試", success, response)
        except Exception as e:
            self.log_test("無效JSON測試", False, error=e)
        
        # 測試缺少必要參數
        try:
            url = f"{self.base_url}/api/v1/port-security/interfaces/eth1%2f1"
            response = self.session.put(url, json={})  # 缺少portStatus
            success = response.status_code == 400
            self.log_test("缺少必要參數測試", success, response)
        except Exception as e:
            self.log_test("缺少必要參數測試", False, error=e)
    
    def run_all_tests(self, test_interfaces=None):
        """運行所有測試"""
        if test_interfaces is None:
            test_interfaces = ["eth1/1", "eth1/5"]
        
        print("=== Port Security REST API 測試開始 ===")
        print(f"測試目標: {self.base_url}")
        print(f"測試接口: {test_interfaces}")
        print("=" * 50)
        
        # 1. 獲取所有接口配置
        print("\n=== 基本功能測試 ===")
        self.test_get_all_port_security()
        
        # 2. 對每個測試接口進行完整測試
        for interface in test_interfaces:
            print(f"\n=== 接口 {interface} 測試 ===")
            
            # 獲取當前配置
            current_config = self.test_get_single_port_security(interface)
            
            # 更新配置
            self.test_update_port_security(interface, True, "trap", 1024)
            
            # 驗證更新後的配置
            self.test_get_single_port_security(interface)
            
            # MAC學習測試
            self.test_get_mac_learning(interface)
            self.test_update_mac_learning(interface, True)
            
            # 保存MAC為靜態條目
            self.test_save_mac_as_permanent(interface)
            
            time.sleep(1)  # 避免請求過於頻繁
        
        # 3. 錯誤場景測試
        self.test_error_scenarios()
        
        # 4. 輸出測試總結
        self.print_test_summary()
    
    def print_test_summary(self):
        """輸出測試總結"""
        print("\n" + "=" * 50)
        print("=== 測試總結 ===")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"總測試數: {total_tests}")
        print(f"通過: {passed_tests}")
        print(f"失敗: {failed_tests}")
        print(f"成功率: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n失敗的測試:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test_name']}")
                    if 'error' in result:
                        print(f"    錯誤: {result['error']}")
        
        # 保存詳細結果到文件
        with open('port_security_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        print(f"\n詳細測試結果已保存到: port_security_test_results.json")

def main():
    """主函數"""
    if len(sys.argv) < 2:
        print("使用方法: python port_security_test.py <base_url> [username] [password]")
        print("範例: python port_security_test.py http://192.168.1.1 admin admin123")
        sys.exit(1)
    
    base_url = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else None
    password = sys.argv[3] if len(sys.argv) > 3 else None
    password = hashlib.md5(password.encode('utf-8')).hexdigest()

    # 創建測試器並運行測試
    tester = PortSecurityAPITester(base_url, username, password)
    
    # 可以自定義測試接口
    test_interfaces = ["eth1/1", "eth1/5", "eth1/28"]
    
    try:
        tester.run_all_tests(test_interfaces)
    except KeyboardInterrupt:
        print("\n測試被用戶中斷")
    except Exception as e:
        print(f"\n測試過程中發生錯誤: {e}")

if __name__ == "__main__":
    main()