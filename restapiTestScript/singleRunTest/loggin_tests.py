
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logging REST API 測試腳本
基於 Logging_API_Reference_v0.14.docx

此腳本測試所有Logging相關的REST API端點，包括：
- 獲取系統日誌資訊
- 更新系統日誌設定
- 清除日誌記錄
"""

import hashlib

import requests
import json
import sys
import time
import getpass
import base64
from typing import Dict, Any, Optional, List

class LoggingAPITester:
    def __init__(self, base_url: str = "http://localhost:8080", timeout: int = 30, 
                 username: str = None, password: str = None):
        """
        初始化Logging API測試器
        
        Args:
            base_url: API基礎URL
            timeout: 請求超時時間(秒)
            username: 登入帳號
            password: 登入密碼
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.test_results = []
        
        # 設置認證
        if username and password:
            self.setup_authentication(username, password)
        
    def setup_authentication(self, username: str, password: str):
        """設置認證方式"""
        # Basic Authentication
        auth_string = f"{username}:{password}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        self.session.headers.update({
            'Authorization': f'Basic {encoded_auth}',
            'Content-Type': 'application/json'
        })
        
        print(f"已設置認證 - 使用者: {username}")
    
    def log_test_result(self, test_name: str, success: bool, details: str = ""):
        """記錄測試結果"""
        result = {
            'test_name': test_name,
            'success': success,
            'details': details,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.test_results.append(result)
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} - {test_name}")
        if details:
            print(f"    詳情: {details}")
    
    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                    params: Optional[Dict] = None) -> requests.Response:
        """發送HTTP請求"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )
            return response
        except requests.exceptions.RequestException as e:
            print(f"請求錯誤: {e}")
            raise
    
    def test_get_syslog_information(self):
        """測試1.1: 獲取系統日誌資訊"""
        try:
            response = self.make_request('GET', '/api/v1/syslog')
            
            if response.status_code == 200:
                data = response.json()
                if 'result' in data:
                    result = data['result']
                    
                    # 驗證必要欄位
                    required_fields = [
                        'sysLogStatus', 'sysLogHistoryFlashLevel', 'sysLogHistoryRamLevel',
                        'remoteLogStatus', 'remoteLogFacility', 'remoteLogLevel',
                        'remoteLogServers', 'flashLogs', 'ramLogs'
                    ]
                    
                    missing_fields = [field for field in required_fields if field not in result]
                    
                    if not missing_fields:
                        details = f"系統日誌狀態: {result['sysLogStatus']}, "
                        details += f"Flash日誌級別: {result['sysLogHistoryFlashLevel']}, "
                        details += f"RAM日誌級別: {result['sysLogHistoryRamLevel']}, "
                        details += f"遠端日誌狀態: {result['remoteLogStatus']}, "
                        details += f"RAM日誌數量: {len(result['ramLogs'])}, "
                        details += f"Flash日誌數量: {len(result['flashLogs'])}"
                        
                        self.log_test_result("獲取系統日誌資訊", True, details)
                        return result
                    else:
                        self.log_test_result("獲取系統日誌資訊", False, f"缺少欄位: {missing_fields}")
                else:
                    self.log_test_result("獲取系統日誌資訊", False, "回應格式錯誤 - 缺少result欄位")
            elif response.status_code == 401:
                self.log_test_result("獲取系統日誌資訊", False, "認證失敗 - 請檢查帳號密碼")
            elif response.status_code == 500:
                error_data = response.json() if response.content else {}
                error_code = error_data.get('code', 'unknown')
                error_message = error_data.get('message', 'unknown error')
                self.log_test_result("獲取系統日誌資訊", False, f"伺服器錯誤 - {error_code}: {error_message}")
            else:
                self.log_test_result(
                    "獲取系統日誌資訊", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_test_result("獲取系統日誌資訊", False, str(e))
        return None
    
    def test_update_syslog_information(self, config: Dict[str, Any]):
        """測試1.2: 更新系統日誌設定"""
        try:
            response = self.make_request('PUT', '/api/v1/syslog', data=config)
            
            if response.status_code == 200:
                self.log_test_result(
                    "更新系統日誌設定", 
                    True, 
                    f"成功更新設定: {json.dumps(config, ensure_ascii=False)}"
                )
                return True
            elif response.status_code == 400:
                error_data = response.json() if response.content else {}
                error_code = error_data.get('code', 'unknown')
                error_message = error_data.get('message', 'unknown error')
                self.log_test_result(
                    "更新系統日誌設定", 
                    False, 
                    f"參數錯誤 - {error_code}: {error_message}"
                )
            elif response.status_code == 500:
                error_data = response.json() if response.content else {}
                error_code = error_data.get('code', 'unknown')
                error_message = error_data.get('message', 'unknown error')
                self.log_test_result(
                    "更新系統日誌設定", 
                    False, 
                    f"伺服器錯誤 - {error_code}: {error_message}"
                )
            else:
                self.log_test_result(
                    "更新系統日誌設定", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_test_result("更新系統日誌設定", False, str(e))
        return False
    
    def test_clear_log(self, log_type: str):
        """測試1.3: 清除日誌"""
        try:
            response = self.make_request('PUT', f'/api/v1/syslog/log-clear/{log_type}')
            
            if response.status_code == 200:
                self.log_test_result(
                    f"清除{log_type}日誌", 
                    True, 
                    f"成功清除{log_type}日誌"
                )
                return True
            elif response.status_code == 500:
                error_data = response.json() if response.content else {}
                error_code = error_data.get('code', 'unknown')
                error_message = error_data.get('message', 'unknown error')
                self.log_test_result(
                    f"清除{log_type}日誌", 
                    False, 
                    f"伺服器錯誤 - {error_code}: {error_message}"
                )
            else:
                self.log_test_result(
                    f"清除{log_type}日誌", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_test_result(f"清除{log_type}日誌", False, str(e))
        return False
    
    def test_syslog_configuration_scenarios(self):
        """測試各種系統日誌設定情境"""
        print("\n=== 測試系統日誌設定情境 ===")
        
        # 情境1: 基本設定更新
        basic_config = {
            "sysLogStatus": True,
            "sysLogHistoryFlashLevel": 5,
            "sysLogHistoryRamLevel": 6
        }
        self.test_update_syslog_information(basic_config)
        
        # 情境2: 遠端日誌設定
        remote_config = {
            "remoteLogStatus": True,
            "remoteLogFacility": 20,
            "remoteLogLevel": 4,
            "remoteLogServers": [
                {
                    "ipAddress": "192.168.1.100",
                    "udpPort": 514
                },
                {
                    "ipAddress": "2001:db8::1",
                    "udpPort": 514
                }
            ]
        }
        self.test_update_syslog_information(remote_config)
        
        # 情境3: 完整設定
        full_config = {
            "sysLogStatus": True,
            "sysLogHistoryFlashLevel": 3,
            "sysLogHistoryRamLevel": 7,
            "remoteLogStatus": True,
            "remoteLogFacility": 23,
            "remoteLogLevel": 7,
            "remoteLogServers": [
                {
                    "ipAddress": "192.168.2.20",
                    "udpPort": 162
                },
                {
                    "ipAddress": "2001:1::2",
                    "udpPort": 514
                }
            ]
        }
        self.test_update_syslog_information(full_config)
        
        # 情境4: 停用系統日誌
        disable_config = {
            "sysLogStatus": False,
            "remoteLogStatus": False
        }
        self.test_update_syslog_information(disable_config)
    
    def test_log_clearing_scenarios(self):
        """測試各種日誌清除情境"""
        print("\n=== 測試日誌清除情境 ===")
        
        # 清除RAM日誌
        self.test_clear_log("ram")
        
        # 清除Flash日誌
        self.test_clear_log("flash")
        
        # 清除所有日誌
        self.test_clear_log("all")
    
    def test_error_cases(self):
        """測試錯誤情況"""
        print("\n=== 測試錯誤情況 ===")
        
        # 測試無效的日誌級別
        invalid_level_config = {
            "sysLogHistoryFlashLevel": 10  # 超出範圍 (0-7)
        }
        self.test_update_syslog_information(invalid_level_config)
        
        # 測試無效的設施類型
        invalid_facility_config = {
            "remoteLogFacility": 30  # 超出範圍 (16-23)
        }
        self.test_update_syslog_information(invalid_facility_config)
        
        # 測試無效的IP地址
        invalid_ip_config = {
            "remoteLogServers": [
                {
                    "ipAddress": "invalid.ip.address",
                    "udpPort": 514
                }
            ]
        }
        self.test_update_syslog_information(invalid_ip_config)
        
        # 測試無效的端口號
        invalid_port_config = {
            "remoteLogServers": [
                {
                    "ipAddress": "192.168.1.1",
                    "udpPort": 70000  # 超出範圍 (1-65535)
                }
            ]
        }
        self.test_update_syslog_information(invalid_port_config)
        
        # 測試無效的清除類型
        try:
            response = self.make_request('PUT', '/api/v1/syslog/log-clear/invalid')
            if response.status_code != 200:
                self.log_test_result("無效清除類型測試", True, f"正確返回錯誤: {response.status_code}")
            else:
                self.log_test_result("無效清除類型測試", False, "應該返回錯誤但成功了")
        except Exception as e:
            self.log_test_result("無效清除類型測試", False, str(e))
        
        # 測試無效JSON
        try:
            response = self.session.put(
                f"{self.base_url}/api/v1/syslog",
                data="invalid json",
                headers={'Content-Type': 'application/json'},
                timeout=self.timeout
            )
            if response.status_code == 400:
                self.log_test_result("無效JSON測試", True, "正確返回400錯誤")
            else:
                self.log_test_result("無效JSON測試", False, f"期望400，實際{response.status_code}")
        except Exception as e:
            self.log_test_result("無效JSON測試", False, str(e))
    
    def test_data_validation(self, syslog_data: Dict[str, Any]):
        """驗證系統日誌資料結構"""
        print("\n=== 驗證日誌資料結構 ===")
        
        if not syslog_data:
            self.log_test_result("資料結構驗證", False, "無法獲取系統日誌資料")
            return
        
        # 驗證RAM日誌結構
        if 'ramLogs' in syslog_data and syslog_data['ramLogs']:
            ram_log = syslog_data['ramLogs'][0]
            required_ram_fields = ['index', 'time', 'logOwnerInfo', 'logMessage']
            missing_ram_fields = [field for field in required_ram_fields if field not in ram_log]
            
            if not missing_ram_fields:
                # 驗證時間結構
                time_fields = ['year', 'month', 'day', 'hour', 'minute', 'second']
                missing_time_fields = [field for field in time_fields if field not in ram_log['time']]
                
                # 驗證日誌擁有者資訊結構
                owner_fields = ['level', 'function', 'module', 'event']
                missing_owner_fields = [field for field in owner_fields if field not in ram_log['logOwnerInfo']]
                
                if not missing_time_fields and not missing_owner_fields:
                    self.log_test_result("RAM日誌結構驗證", True, "結構完整")
                else:
                    missing = missing_time_fields + missing_owner_fields
                    self.log_test_result("RAM日誌結構驗證", False, f"缺少欄位: {missing}")
            else:
                self.log_test_result("RAM日誌結構驗證", False, f"缺少欄位: {missing_ram_fields}")
        else:
            self.log_test_result("RAM日誌結構驗證", True, "無RAM日誌資料")
        
        # 驗證Flash日誌結構（結構與RAM日誌相同）
        if 'flashLogs' in syslog_data and syslog_data['flashLogs']:
            flash_log = syslog_data['flashLogs'][0]
            required_flash_fields = ['index', 'time', 'logOwnerInfo', 'logMessage']
            missing_flash_fields = [field for field in required_flash_fields if field not in flash_log]
            
            if not missing_flash_fields:
                self.log_test_result("Flash日誌結構驗證", True, "結構完整")
            else:
                self.log_test_result("Flash日誌結構驗證", False, f"缺少欄位: {missing_flash_fields}")
        else:
            self.log_test_result("Flash日誌結構驗證", True, "無Flash日誌資料")
        
        # 驗證遠端日誌伺服器結構
        if 'remoteLogServers' in syslog_data and syslog_data['remoteLogServers']:
            server = syslog_data['remoteLogServers'][0]
            required_server_fields = ['ipAddress', 'udpPort']
            missing_server_fields = [field for field in required_server_fields if field not in server]
            
            if not missing_server_fields:
                self.log_test_result("遠端日誌伺服器結構驗證", True, "結構完整")
            else:
                self.log_test_result("遠端日誌伺服器結構驗證", False, f"缺少欄位: {missing_server_fields}")
        else:
            self.log_test_result("遠端日誌伺服器結構驗證", True, "無遠端日誌伺服器設定")
    
    def run_comprehensive_test(self):
        """執行完整測試套件"""
        print("=== Logging API 完整測試開始 ===\n")
        
        # 1. 測試獲取系統日誌資訊
        print("=== 測試獲取系統日誌資訊 ===")
        original_syslog_data = self.test_get_syslog_information()
        
        # 如果第一個API調用失敗（可能是認證問題），停止測試
        if original_syslog_data is None and self.test_results[-1]['details'].find('認證失敗') != -1:
            print("認證失敗，停止測試。請檢查帳號密碼是否正確。")
            return
        
        # 2. 驗證資料結構
        self.test_data_validation(original_syslog_data)
        
        # 3. 測試系統日誌設定更新
        self.test_syslog_configuration_scenarios()
        
        # 4. 測試日誌清除功能
        self.test_log_clearing_scenarios()
        
        # 5. 測試錯誤情況
        self.test_error_cases()
        
        # 6. 恢復原始設定（如果有的話）
        if original_syslog_data:
            print("\n=== 恢復原始設定 ===")
            # 移除只讀欄位
            restore_config = {k: v for k, v in original_syslog_data.items() 
                            if k not in ['flashLogs', 'ramLogs']}
            self.test_update_syslog_information(restore_config)
        
        # 7. 最終驗證
        print("\n=== 最終驗證 ===")
        final_syslog_data = self.test_get_syslog_information()
        
        # 8. 生成測試報告
        self.generate_test_report()
    
    def generate_test_report(self):
        """生成測試報告"""
        print("\n" + "="*50)
        print("測試報告")
        print("="*50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"總測試數: {total_tests}")
        print(f"通過: {passed_tests}")
        print(f"失敗: {failed_tests}")
        print(f"成功率: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n失敗的測試:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test_name']}: {result['details']}")
        
        # 按類別統計
        categories = {}
        for result in self.test_results:
            category = result['test_name'].split('測試')[0] if '測試' in result['test_name'] else '其他'
            if category not in categories:
                categories[category] = {'total': 0, 'passed': 0}
            categories[category]['total'] += 1
            if result['success']:
                categories[category]['passed'] += 1
        
        print("\n按類別統計:")
        for category, stats in categories.items():
            success_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"  {category}: {stats['passed']}/{stats['total']} ({success_rate:.1f}%)")
        
        # 保存詳細報告到文件
        report_file = f"logging_api_test_report_{int(time.time())}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        print(f"\n詳細報告已保存到: {report_file}")

def get_credentials():
    """獲取用戶認證資訊"""
    print("=== Logging API 認證 ===")
    username = input("請輸入帳號: ").strip()
    
    if not username:
        return None, None
        
    password = getpass.getpass("請輸入密碼: ")
    
    return username, password

def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Logging API 測試腳本')
    parser.add_argument('--url', default='http://localhost:8080', 
                       help='API基礎URL (預設: http://localhost:8080)')
    parser.add_argument('--timeout', type=int, default=30, 
                       help='請求超時時間(秒) (預設: 30)')
    parser.add_argument('--username', '-u', 
                       help='登入帳號')
    parser.add_argument('--password', '-p', 
                       help='登入密碼')
    parser.add_argument('--no-auth', action='store_true',
                       help='跳過認證（用於不需要認證的API）')
    
    args = parser.parse_args()
    
    username = args.username
    password = args.password
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    
    # 如果沒有提供認證資訊且不跳過認證，則提示輸入
    if not args.no_auth and (not username or not password):
        print("需要認證資訊來訪問API")
        username, password = get_credentials()
        
        if not username:
            print("未提供認證資訊，將嘗試不使用認證訪問API")
            username = password = None
    
    try:
        tester = LoggingAPITester(
            base_url=args.url, 
            timeout=args.timeout,
            username=username,
            password=password
        )
        
        tester.run_comprehensive_test()
            
    except KeyboardInterrupt:
        print("\n測試被用戶中斷")
        sys.exit(1)
    except Exception as e:
        print(f"\n測試執行錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()