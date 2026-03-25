#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UDP Helper REST API 測試腳本
基於 UdpHelper_API_Reference_v0.13.docx

此腳本測試所有UDP Helper相關的REST API端點，包括：
- UDP Helper狀態管理
- 轉發協議端口管理  
- 網路地址管理
"""

import requests
import json
import sys
import time
from typing import Dict, Any, Optional

class UDPHelperAPITester:
    def __init__(self, base_url: str = "http://localhost:8080", timeout: int = 30):
        """
        初始化UDP Helper API測試器
        
        Args:
            base_url: API基礎URL
            timeout: 請求超時時間(秒)
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.test_results = []
        
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
        url = f"{self.base_url}/{endpoint}"
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
    
    def test_get_udp_helper_status(self):
        """測試1.1: 獲取UDP helper狀態"""
        try:
            response = self.make_request('GET', '/api/v1/udp-helper')
            
            if response.status_code == 200:
                data = response.json()
                if 'result' in data and 'helperStatus' in data['result']:
                    self.log_test_result(
                        "獲取UDP helper狀態", 
                        True, 
                        f"狀態: {data['result']['helperStatus']}"
                    )
                    return data['result']['helperStatus']
                else:
                    self.log_test_result("獲取UDP helper狀態", False, "回應格式錯誤")
            else:
                self.log_test_result(
                    "獲取UDP helper狀態", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_test_result("獲取UDP helper狀態", False, str(e))
        return None
    
    def test_set_udp_helper_status(self, status: bool):
        """測試1.2: 設置UDP helper狀態"""
        try:
            data = {"helperStatus": status}
            response = self.make_request('PUT', '/api/v1/udp-helper', data=data)
            
            if response.status_code == 200:
                self.log_test_result(
                    f"設置UDP helper狀態為{status}", 
                    True, 
                    "設置成功"
                )
                return True
            else:
                self.log_test_result(
                    f"設置UDP helper狀態為{status}", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_test_result(f"設置UDP helper狀態為{status}", False, str(e))
        return False
    
    def test_get_forward_protocol_entries(self, start_id: int = 1):
        """測試1.3: 獲取所有UDP helper轉發協議條目"""
        try:
            params = {"startId": start_id}
            response = self.make_request('GET', '/api/v1/udp-helper/forward-protocal', params=params)
            
            if response.status_code == 200:
                data = response.json()
                if 'result' in data and 'entries' in data['result']:
                    entries = data['result']['entries']
                    self.log_test_result(
                        "獲取轉發協議條目", 
                        True, 
                        f"找到 {len(entries)} 個條目"
                    )
                    return entries
                else:
                    self.log_test_result("獲取轉發協議條目", False, "回應格式錯誤")
            else:
                self.log_test_result(
                    "獲取轉發協議條目", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_test_result("獲取轉發協議條目", False, str(e))
        return []
    
    def test_add_forward_protocol_entry(self, udp_port: int):
        """測試1.4: 添加UDP helper轉發協議條目"""
        try:
            data = {"udpPort": udp_port}
            response = self.make_request('POST', '/api/v1/udp-helper/forward-protocal', data=data)
            
            if response.status_code == 200:
                self.log_test_result(
                    f"添加轉發協議端口 {udp_port}", 
                    True, 
                    "添加成功"
                )
                return True
            else:
                self.log_test_result(
                    f"添加轉發協議端口 {udp_port}", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_test_result(f"添加轉發協議端口 {udp_port}", False, str(e))
        return False
    
    def test_get_forward_protocol_entry(self, udp_port: int):
        """測試1.5: 獲取特定UDP helper轉發端口條目"""
        try:
            response = self.make_request('GET', f'/api/v1/udp-helper/forward-protocal/udp-ports/{udp_port}')
            
            if response.status_code == 200:
                data = response.json()
                if 'result' in data and 'udpPort' in data['result']:
                    self.log_test_result(
                        f"獲取轉發端口 {udp_port}", 
                        True, 
                        f"端口: {data['result']['udpPort']}"
                    )
                    return True
                else:
                    self.log_test_result(f"獲取轉發端口 {udp_port}", False, "回應格式錯誤")
            else:
                self.log_test_result(
                    f"獲取轉發端口 {udp_port}", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_test_result(f"獲取轉發端口 {udp_port}", False, str(e))
        return False
    
    def test_delete_forward_protocol_entry(self, udp_port: int):
        """測試1.6: 刪除UDP helper轉發協議條目"""
        try:
            response = self.make_request('DELETE', f'/api/v1/udp-helper/forward-protocal/udp-ports/{udp_port}')
            
            if response.status_code == 200:
                self.log_test_result(
                    f"刪除轉發端口 {udp_port}", 
                    True, 
                    "刪除成功"
                )
                return True
            else:
                self.log_test_result(
                    f"刪除轉發端口 {udp_port}", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_test_result(f"刪除轉發端口 {udp_port}", False, str(e))
        return False
    
    def test_get_address_entries(self, start_id: int = 1):
        """測試1.7: 獲取所有UDP helper地址條目"""
        try:
            params = {"startId": start_id}
            response = self.make_request('GET', '/api/v1/udp-helper/inet-addr/vlans', params=params)
            
            if response.status_code == 200:
                data = response.json()
                if 'result' in data and 'entries' in data['result']:
                    entries = data['result']['entries']
                    self.log_test_result(
                        "獲取地址條目", 
                        True, 
                        f"找到 {len(entries)} 個條目"
                    )
                    return entries
                else:
                    self.log_test_result("獲取地址條目", False, "回應格式錯誤")
            else:
                self.log_test_result(
                    "獲取地址條目", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_test_result("獲取地址條目", False, str(e))
        return []
    
    def test_add_address_entry(self, vlan_id: int, ip_address: str):
        """測試1.8: 添加UDP helper地址"""
        try:
            data = {"vlanId": vlan_id, "ipAddress": ip_address}
            response = self.make_request('POST', '/api/v1/udp-helper/inet-addr/vlans', data=data)
            
            if response.status_code == 200:
                self.log_test_result(
                    f"添加地址 VLAN{vlan_id}:{ip_address}", 
                    True, 
                    "添加成功"
                )
                return True
            else:
                self.log_test_result(
                    f"添加地址 VLAN{vlan_id}:{ip_address}", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_test_result(f"添加地址 VLAN{vlan_id}:{ip_address}", False, str(e))
        return False
    
    def test_get_address_entry(self, vlan_id: int, ip_address: str):
        """測試1.9: 獲取特定UDP helper地址條目"""
        try:
            response = self.make_request('GET', f'/api/v1/udp-helper/inet-addr/vlans/{vlan_id}/ip-address/{ip_address}')
            
            if response.status_code == 200:
                data = response.json()
                if 'result' in data and 'vlanId' in data['result'] and 'ipAddress' in data['result']:
                    self.log_test_result(
                        f"獲取地址 VLAN{vlan_id}:{ip_address}", 
                        True, 
                        f"VLAN: {data['result']['vlanId']}, IP: {data['result']['ipAddress']}"
                    )
                    return True
                else:
                    self.log_test_result(f"獲取地址 VLAN{vlan_id}:{ip_address}", False, "回應格式錯誤")
            else:
                self.log_test_result(
                    f"獲取地址 VLAN{vlan_id}:{ip_address}", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_test_result(f"獲取地址 VLAN{vlan_id}:{ip_address}", False, str(e))
        return False
    
    def test_delete_address_entry(self, vlan_id: int, ip_address: str):
        """測試1.10: 刪除UDP helper地址"""
        try:
            response = self.make_request('DELETE', f'/api/v1/udp-helper/inet-addr/vlans/{vlan_id}/ip-address/{ip_address}')
            
            if response.status_code == 200:
                self.log_test_result(
                    f"刪除地址 VLAN{vlan_id}:{ip_address}", 
                    True, 
                    "刪除成功"
                )
                return True
            else:
                self.log_test_result(
                    f"刪除地址 VLAN{vlan_id}:{ip_address}", 
                    False, 
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_test_result(f"刪除地址 VLAN{vlan_id}:{ip_address}", False, str(e))
        return False
    
    def test_error_cases(self):
        """測試錯誤情況"""
        print("\n=== 測試錯誤情況 ===")
        
        # 測試無效參數
        try:
            response = self.make_request('POST', '/api/v1/udp-helper/forward-protocal', 
                                      data={"udpPort": 70000})  # 超出範圍
            if response.status_code == 500:
                self.log_test_result("無效UDP端口測試", True, "正確返回500錯誤")
            else:
                self.log_test_result("無效UDP端口測試", False, f"期望500，實際{response.status_code}")
        except Exception as e:
            self.log_test_result("無效UDP端口測試", False, str(e))
        '''
        # 測試無效JSON
        try:
            response = self.session.put(
                f"{self.base_url}/api/v1/udp-helper",
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
        '''
    def run_comprehensive_test(self):
        """執行完整測試套件"""
        print("=== UDP Helper API 完整測試開始 ===\n")
        
        # 1. 測試UDP Helper狀態管理
        print("=== 測試UDP Helper狀態管理 ===")
        current_status = self.test_get_udp_helper_status()
        self.test_set_udp_helper_status(True)
        self.test_set_udp_helper_status(False)
        if current_status is not None:
            self.test_set_udp_helper_status(current_status)  # 恢復原狀態
        
        # 2. 測試轉發協議管理
        print("\n=== 測試轉發協議管理 ===")
        test_port = 547
        
        # 獲取現有條目
        existing_entries = self.test_get_forward_protocol_entries()
        
        # 添加測試端口
        self.test_add_forward_protocol_entry(test_port)
        
        # 獲取特定端口
        self.test_get_forward_protocol_entry(test_port)
        
        # 再次獲取所有條目確認添加
        self.test_get_forward_protocol_entries()
        
        # 刪除測試端口
        self.test_delete_forward_protocol_entry(test_port)
        
        # 3. 測試地址管理
        print("\n=== 測試地址管理 ===")
        test_vlan = 1
        test_ip = "192.168.2.255"
        
        # 獲取現有地址條目
        existing_addresses = self.test_get_address_entries()
        
        # 添加測試地址
        self.test_add_address_entry(test_vlan, test_ip)
        
        # 獲取特定地址
        self.test_get_address_entry(test_vlan, test_ip)
        
        # 再次獲取所有地址確認添加
        self.test_get_address_entries()
        
        # 刪除測試地址
        self.test_delete_address_entry(test_vlan, test_ip)
        
        # 4. 測試錯誤情況
        self.test_error_cases()
        
        # 5. 生成測試報告
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
        
        # 保存詳細報告到文件
        report_file = f"udp_helper_test_report_{int(time.time())}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        print(f"\n詳細報告已保存到: {report_file}")

def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description='UDP Helper API 測試腳本')
    parser.add_argument('--url', default='http://localhost:8080', 
                       help='API基礎URL (預設: http://localhost:8080)')
    parser.add_argument('--timeout', type=int, default=30, 
                       help='請求超時時間(秒) (預設: 30)')
    
    args = parser.parse_args()
    
    try:
        tester = UDPHelperAPITester(base_url=args.url, timeout=args.timeout)
        tester.run_comprehensive_test()
    except KeyboardInterrupt:

        print("\n測試被用戶中斷")
        sys.exit(1)
    except Exception as e:
        print(f"\n測試執行錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()