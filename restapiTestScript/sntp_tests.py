#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SNTP REST API 測試腳本
基於 SNTP_API_Reference_v0.12.docx 文件生成
包含 SNTP 配置管理功能測試
"""

import requests
import json
import sys
import time
import ipaddress
import random

class SNTPAPITester:
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
        self.original_config = None  # 保存原始配置用於恢復
    
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
    
    def validate_ip_address(self, ip):
        """驗證IP地址格式"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    def generate_test_servers(self, count=3):
        """生成測試用的SNTP服務器列表"""
        base_ips = [
            "192.168.1.100",
            "192.168.1.101", 
            "192.168.1.102",
            "10.0.0.100",
            "10.0.0.101",
            "172.16.1.100"
        ]
        
        servers = []
        for i in range(min(count, len(base_ips))):
            servers.append({"ipAddress": base_ips[i]})
        
        return servers
    
    # ==================== 1.1 Get SNTP Information ====================
    
    def test_get_sntp_info(self):
        """測試 1.1: 獲取SNTP信息"""
        try:
            url = f"{self.base_url}/api/v1/sntp"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    
                    # 驗證必要字段
                    required_fields = ['sntpStatus', 'pollInterval']
                    missing_fields = [field for field in required_fields if field not in result_data]
                    
                    if missing_fields:
                        print(f"    缺少字段: {missing_fields}")
                        success = False
                    else:
                        print(f"    SNTP狀態: {'啟用' if result_data.get('sntpStatus') else '禁用'}")
                        print(f"    輪詢間隔: {result_data.get('pollInterval')} 秒")
                        
                        # 顯示可選字段
                        if 'currentTime' in result_data:
                            print(f"    當前時間: {result_data.get('currentTime')}")
                        if 'serviceMode' in result_data:
                            print(f"    服務模式: {result_data.get('serviceMode')}")
                        if 'currentServer' in result_data:
                            print(f"    當前服務器: {result_data.get('currentServer')}")
                        
                        # 顯示服務器列表
                        servers = result_data.get('sntpServers', [])
                        print(f"    SNTP服務器數量: {len(servers)}")
                        for i, server in enumerate(servers):
                            print(f"      服務器 {i+1}: {server.get('ipAddress')}")
                    
                    # 保存原始配置用於後續恢復
                    if success:
                        self.original_config = {
                            "sntpStatus": result_data.get('sntpStatus'),
                            "pollInterval": result_data.get('pollInterval'),
                            "sntpServers": result_data.get('sntpServers', [])
                        }
                else:
                    success = False
                    
            self.log_test("獲取SNTP信息", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取SNTP信息", False, error=e)
            return None
    
    # ==================== 1.2 Update SNTP Management Information ====================
    
    def test_set_sntp_basic_config(self):
        """測試 1.2: 設置基本SNTP配置"""
        try:
            url = f"{self.base_url}/api/v1/sntp"
            
            # 基本配置測試
            payload = {
                "sntpStatus": True,
                "pollInterval": 64
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置基本SNTP配置:")
                print(f"      SNTP狀態: {'啟用' if payload['sntpStatus'] else '禁用'}")
                print(f"      輪詢間隔: {payload['pollInterval']} 秒")
            
            self.log_test("設置基本SNTP配置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置基本SNTP配置", False, error=e)
            return None
    
    def test_set_sntp_with_servers(self):
        """測試 1.2: 設置包含服務器的SNTP配置"""
        try:
            url = f"{self.base_url}/api/v1/sntp"
            
            test_servers = self.generate_test_servers(3)
            
            payload = {
                "sntpStatus": True,
                "pollInterval": 128,
                "sntpServers": test_servers
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置SNTP配置（包含服務器）:")
                print(f"      SNTP狀態: {'啟用' if payload['sntpStatus'] else '禁用'}")
                print(f"      輪詢間隔: {payload['pollInterval']} 秒")
                print(f"      服務器數量: {len(payload['sntpServers'])}")
                for i, server in enumerate(payload['sntpServers']):
                    print(f"        服務器 {i+1}: {server['ipAddress']}")
            
            self.log_test("設置包含服務器的SNTP配置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置包含服務器的SNTP配置", False, error=e)
            return None
    
    def test_set_sntp_disable(self):
        """測試 1.2: 禁用SNTP服務"""
        try:
            url = f"{self.base_url}/api/v1/sntp"
            
            payload = {
                "sntpStatus": False,
                "pollInterval": 16  # 最小值
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功禁用SNTP服務:")
                print(f"      SNTP狀態: {'啟用' if payload['sntpStatus'] else '禁用'}")
                print(f"      輪詢間隔: {payload['pollInterval']} 秒")
            
            self.log_test("禁用SNTP服務", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("禁用SNTP服務", False, error=e)
            return None
    
    def test_set_sntp_single_server(self):
        """測試 1.2: 設置單個SNTP服務器"""
        try:
            url = f"{self.base_url}/api/v1/sntp"
            
            payload = {
                "sntpStatus": True,
                "pollInterval": 256,
                "sntpServers": [
                    {"ipAddress": "192.168.100.1"}
                ]
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置單個SNTP服務器:")
                print(f"      服務器地址: {payload['sntpServers'][0]['ipAddress']}")
                print(f"      輪詢間隔: {payload['pollInterval']} 秒")
            
            self.log_test("設置單個SNTP服務器", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置單個SNTP服務器", False, error=e)
            return None
    
    def test_set_sntp_multiple_servers(self):
        """測試 1.2: 設置多個SNTP服務器"""
        try:
            url = f"{self.base_url}/api/v1/sntp"
            
            test_servers = self.generate_test_servers(5)
            
            payload = {
                "sntpStatus": True,
                "pollInterval": 512,
                "sntpServers": test_servers
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置多個SNTP服務器:")
                print(f"      服務器數量: {len(payload['sntpServers'])}")
                for i, server in enumerate(payload['sntpServers']):
                    print(f"        服務器 {i+1}: {server['ipAddress']}")
            
            self.log_test("設置多個SNTP服務器", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置多個SNTP服務器", False, error=e)
            return None
    
    def test_set_sntp_ipv6_servers(self):
        """測試 1.2: 設置IPv6 SNTP服務器"""
        try:
            url = f"{self.base_url}/api/v1/sntp"
            
            payload = {
                "sntpStatus": True,
                "pollInterval": 1024,
                "sntpServers": [
                    {"ipAddress": "2001:db8::1"},
                    {"ipAddress": "2001:db8::2"},
                    {"ipAddress": "fe80::1"}
                ]
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置IPv6 SNTP服務器:")
                for i, server in enumerate(payload['sntpServers']):
                    print(f"        IPv6服務器 {i+1}: {server['ipAddress']}")
            
            self.log_test("設置IPv6 SNTP服務器", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置IPv6 SNTP服務器", False, error=e)
            return None
    
    def test_set_sntp_mixed_servers(self):
        """測試 1.2: 設置混合IPv4/IPv6 SNTP服務器"""
        try:
            url = f"{self.base_url}/api/v1/sntp"
            
            payload = {
                "sntpStatus": True,
                "pollInterval": 2048,
                "sntpServers": [
                    {"ipAddress": "192.168.1.10"},
                    {"ipAddress": "2001:db8::10"},
                    {"ipAddress": "10.0.0.10"},
                    {"ipAddress": "2001:db8::20"}
                ]
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置混合IPv4/IPv6 SNTP服務器:")
                for i, server in enumerate(payload['sntpServers']):
                    ip_type = "IPv6" if ":" in server['ipAddress'] else "IPv4"
                    print(f"        {ip_type}服務器 {i+1}: {server['ipAddress']}")
            
            self.log_test("設置混合IPv4/IPv6 SNTP服務器", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置混合IPv4/IPv6 SNTP服務器", False, error=e)
            return None
    
    # ==================== 綜合測試場景 ====================
    
    def test_complete_sntp_workflow(self):
        """測試完整的SNTP工作流程"""
        print("\n=== 完整SNTP工作流程測試 ===")
        
        try:
            # 步驟1: 獲取當前配置
            print("\n步驟1: 獲取當前SNTP配置")
            self.test_get_sntp_info()
            
            # 步驟2: 禁用SNTP服務
            print("\n步驟2: 禁用SNTP服務")
            self.test_set_sntp_disable()
            time.sleep(1)
            
            # 步驟3: 驗證禁用狀態
            print("\n步驟3: 驗證SNTP禁用狀態")
            self.test_get_sntp_info()
            
            # 步驟4: 啟用SNTP並設置基本配置
            print("\n步驟4: 啟用SNTP並設置基本配置")
            self.test_set_sntp_basic_config()
            time.sleep(1)
            
            # 步驟5: 添加單個服務器
            print("\n步驟5: 添加單個SNTP服務器")
            self.test_set_sntp_single_server()
            time.sleep(1)
            
            # 步驟6: 驗證單服務器配置
            print("\n步驟6: 驗證單服務器配置")
            self.test_get_sntp_info()
            
            # 步驟7: 添加多個服務器
            print("\n步驟7: 添加多個SNTP服務器")
            self.test_set_sntp_multiple_servers()
            time.sleep(1)
            
            # 步驟8: 驗證多服務器配置
            print("\n步驟8: 驗證多服務器配置")
            self.test_get_sntp_info()
            
            # 步驟9: 測試IPv6服務器
            print("\n步驟9: 測試IPv6服務器配置")
            self.test_set_sntp_ipv6_servers()
            time.sleep(1)
            
            # 步驟10: 測試混合服務器
            print("\n步驟10: 測試混合IPv4/IPv6服務器")
            self.test_set_sntp_mixed_servers()
            time.sleep(1)
            
            # 步驟11: 最終驗證
            print("\n步驟11: 最終配置驗證")
            self.test_get_sntp_info()
            
            print("\n✓ 完整工作流程測試完成")
            
        except Exception as e:
            print(f"\n✗ 工作流程測試失敗: {e}")
    
    def test_parameter_validation(self):
        """測試參數驗證"""
        print("\n=== 參數驗證測試 ===")
        
        # 測試輪詢間隔範圍
        interval_test_cases = [
            (16, "最小輪詢間隔"),
            (64, "標準輪詢間隔"),
            (1024, "中等輪詢間隔"),
            (8192, "大輪詢間隔"),
            (16384, "最大輪詢間隔")
        ]
        
        for interval, description in interval_test_cases:
            try:
                url = f"{self.base_url}/api/v1/sntp"
                payload = {
                    "sntpStatus": True,
                    "pollInterval": interval,
                    "sntpServers": [{"ipAddress": "192.168.1.100"}]
                }
                response = self.session.put(url, json=payload)
                success = response.status_code == 200
                self.log_test(f"輪詢間隔驗證測試 - {description} ({interval}秒)", success, response)
                time.sleep(0.5)
            except Exception as e:
                self.log_test(f"輪詢間隔驗證測試 - {description} ({interval}秒)", False, error=e)
        
        # 測試不同類型的IP地址
        ip_test_cases = [
            ("192.168.1.1", "私有IPv4地址"),
            ("10.0.0.1", "私有IPv4地址 (10.x.x.x)"),
            ("172.16.1.1", "私有IPv4地址 (172.16.x.x)"),
            ("8.8.8.8", "公共IPv4地址"),
            ("2001:db8::1", "IPv6地址"),
            ("::1", "IPv6回環地址"),
            ("fe80::1", "IPv6鏈路本地地址")
        ]
        
        for ip_addr, description in ip_test_cases:
            try:
                url = f"{self.base_url}/api/v1/sntp"
                payload = {
                    "sntpStatus": True,
                    "pollInterval": 64,
                    "sntpServers": [{"ipAddress": ip_addr}]
                }
                response = self.session.put(url, json=payload)
                success = response.status_code == 200
                self.log_test(f"IP地址驗證測試 - {description} ({ip_addr})", success, response)
                time.sleep(0.5)
            except Exception as e:
                self.log_test(f"IP地址驗證測試 - {description} ({ip_addr})", False, error=e)
        
        # 測試服務器數量限制
        server_count_test_cases = [
            (1, "單個服務器"),
            (3, "三個服務器"),
            (5, "五個服務器"),
            (8, "八個服務器")
        ]
        
        for count, description in server_count_test_cases:
            try:
                servers = self.generate_test_servers(count)
                url = f"{self.base_url}/api/v1/sntp"
                payload = {
                    "sntpStatus": True,
                    "pollInterval": 64,
                    "sntpServers": servers
                }
                response = self.session.put(url, json=payload)
                success = response.status_code == 200
                self.log_test(f"服務器數量驗證測試 - {description} ({count}個)", success, response)
                time.sleep(0.5)
            except Exception as e:
                self.log_test(f"服務器數量驗證測試 - {description} ({count}個)", False, error=e)
    
    def test_error_scenarios(self):
        """測試錯誤場景"""
        print("\n=== 錯誤場景測試 ===")
        
        # 測試1: 無效JSON格式
        try:
            url = f"{self.base_url}/api/v1/sntp"
            response = self.session.put(url, data="invalid json")
            success = response.status_code == 400
            self.log_test("無效JSON格式測試", success, response)
        except Exception as e:
            self.log_test("無效JSON格式測試", False, error=e)
        
        # 測試2: 超出範圍的輪詢間隔
        try:
            url = f"{self.base_url}/api/v1/sntp"
            payload = {
                "sntpStatus": True,
                "pollInterval": 20000  # 超出16384
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            self.log_test("超出範圍輪詢間隔測試 (>16384)", success, response)
        except Exception as e:
            self.log_test("超出範圍輪詢間隔測試 (>16384)", False, error=e)
        
        # 測試3: 小於最小值的輪詢間隔
        try:
            url = f"{self.base_url}/api/v1/sntp"
            payload = {
                "sntpStatus": True,
                "pollInterval": 10  # 小於16
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            self.log_test("小於最小值輪詢間隔測試 (<16)", success, response)
        except Exception as e:
            self.log_test("小於最小值輪詢間隔測試 (<16)", False, error=e)
        
        # 測試4: 無效的IP地址格式
        invalid_ip_cases = [
            ("256.256.256.256", "超出範圍的IPv4"),
            ("192.168.1", "不完整的IPv4"),
            ("invalid.ip.address", "無效格式"),
            ("", "空IP地址"),
            ("192.168.1.1.1", "過多段的IP"),
            ("gggg::1", "無效的IPv6")
        ]
        
        for invalid_ip, description in invalid_ip_cases:
            try:
                url = f"{self.base_url}/api/v1/sntp"
                payload = {
                    "sntpStatus": True,
                    "pollInterval": 64,
                    "sntpServers": [{"ipAddress": invalid_ip}]
                }
                response = self.session.put(url, json=payload)
                success = response.status_code == 400
                self.log_test(f"無效IP地址測試 - {description}", success, response)
            except Exception as e:
                self.log_test(f"無效IP地址測試 - {description}", False, error=e)
        
        # 測試5: 缺少必要參數
        try:
            url = f"{self.base_url}/api/v1/sntp"
            payload = {
                "sntpStatus": True
                # 缺少 pollInterval
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            self.log_test("缺少必要參數測試", success, response)
        except Exception as e:
            self.log_test("缺少必要參數測試", False, error=e)
        
        # 測試6: 錯誤的數據類型
        try:
            url = f"{self.base_url}/api/v1/sntp"
            payload = {
                "sntpStatus": "true",  # 應該是boolean
                "pollInterval": "64"   # 應該是integer
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            self.log_test("錯誤數據類型測試", success, response)
        except Exception as e:
            self.log_test("錯誤數據類型測試", False, error=e)
        
        # 測試7: 空的服務器列表但有ipAddress字段
        try:
            url = f"{self.base_url}/api/v1/sntp"
            payload = {
                "sntpStatus": True,
                "pollInterval": 64,
                "sntpServers": [{"ipAddress": ""}]  # 空IP地址
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            self.log_test("空IP地址測試", success, response)
        except Exception as e:
            self.log_test("空IP地址測試", False, error=e)
    
    def test_boundary_conditions(self):
        """測試邊界條件"""
        print("\n=== 邊界條件測試 ===")
        
        # 測試最小輪詢間隔
        try:
            url = f"{self.base_url}/api/v1/sntp"
            payload = {
                "sntpStatus": True,
                "pollInterval": 16,  # 最小值
                "sntpServers": [{"ipAddress": "192.168.1.1"}]
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            self.log_test("最小輪詢間隔邊界測試 (16秒)", success, response)
        except Exception as e:
            self.log_test("最小輪詢間隔邊界測試 (16秒)", False, error=e)
        
        # 測試最大輪詢間隔
        try:
            url = f"{self.base_url}/api/v1/sntp"
            payload = {
                "sntpStatus": True,
                "pollInterval": 16384,  # 最大值
                "sntpServers": [{"ipAddress": "192.168.1.1"}]
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            self.log_test("最大輪詢間隔邊界測試 (16384秒)", success, response)
        except Exception as e:
            self.log_test("最大輪詢間隔邊界測試 (16384秒)", False, error=e)
        
        # 測試空服務器列表
        try:
            url = f"{self.base_url}/api/v1/sntp"
            payload = {
                "sntpStatus": True,
                "pollInterval": 64,
                "sntpServers": []  # 空列表
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            self.log_test("空服務器列表邊界測試", success, response)
        except Exception as e:
            self.log_test("空服務器列表邊界測試", False, error=e)
        
        # 測試只設置狀態和間隔（不設置服務器）
        try:
            url = f"{self.base_url}/api/v1/sntp"
            payload = {
                "sntpStatus": False,
                "pollInterval": 128
                # 不設置 sntpServers
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            self.log_test("不設置服務器列表邊界測試", success, response)
        except Exception as e:
            self.log_test("不設置服務器列表邊界測試", False, error=e)
    
    def test_configuration_persistence(self):
        """測試配置持久性"""
        print("\n=== 配置持久性測試 ===")
        
        # 設置一個特定的配置
        test_config = {
            "sntpStatus": True,
            "pollInterval": 256,
            "sntpServers": [
                {"ipAddress": "192.168.100.10"},
                {"ipAddress": "192.168.100.11"}
            ]
        }
        
        try:
            # 步驟1: 設置配置
            url = f"{self.base_url}/api/v1/sntp"
            response = self.session.put(url, json=test_config)
            
            if response.status_code == 200:
                print("    配置設置成功")
                time.sleep(2)  # 等待配置生效
                
                # 步驟2: 讀取配置驗證
                get_response = self.test_get_sntp_info()
                if get_response:
                    get_data = get_response.json()
                    if 'result' in get_data:
                        result_data = get_data['result']
                        
                        # 驗證配置是否正確保存
                        status_match = result_data.get('sntpStatus') == test_config['sntpStatus']
                        interval_match = result_data.get('pollInterval') == test_config['pollInterval']
                        
                        servers_match = True
                        result_servers = result_data.get('sntpServers', [])
                        if len(result_servers) == len(test_config['sntpServers']):
                            for i, server in enumerate(test_config['sntpServers']):
                                if i < len(result_servers):
                                    if result_servers[i].get('ipAddress') != server['ipAddress']:
                                        servers_match = False
                                        break
                                else:
                                    servers_match = False
                                    break
                        else:
                            servers_match = False
                        
                        persistence_success = status_match and interval_match and servers_match
                        
                        print(f"    狀態匹配: {status_match}")
                        print(f"    間隔匹配: {interval_match}")
                        print(f"    服務器匹配: {servers_match}")
                        
                        self.log_test("配置持久性驗證", persistence_success)
                    else:
                        self.log_test("配置持久性驗證", False, error="無法獲取結果數據")
                else:
                    self.log_test("配置持久性驗證", False, error="無法讀取配置")
            else:
                self.log_test("配置持久性測試", False, response=response)
                
        except Exception as e:
            self.log_test("配置持久性測試", False, error=e)
    
    def restore_original_config(self):
        """恢復原始配置"""
        if self.original_config:
            print("\n=== 恢復原始SNTP配置 ===")
            try:
                url = f"{self.base_url}/api/v1/sntp"
                response = self.session.put(url, json=self.original_config)
                
                success = response.status_code == 200
                if success:
                    print("    ✓ 原始配置已恢復")
                    print(f"      SNTP狀態: {'啟用' if self.original_config['sntpStatus'] else '禁用'}")
                    print(f"      輪詢間隔: {self.original_config['pollInterval']} 秒")
                    print(f"      服務器數量: {len(self.original_config.get('sntpServers', []))}")
                else:
                    print("    ✗ 恢復原始配置失敗")
                
                self.log_test("恢復原始配置", success, response)
                
            except Exception as e:
                print(f"    ✗ 恢復原始配置時發生錯誤: {e}")
                self.log_test("恢復原始配置", False, error=e)
        else:
            print("    沒有保存的原始配置，跳過恢復")
    
    def run_all_tests(self):
        """運行所有測試"""
        print("=== SNTP REST API 測試開始 ===")
        print(f"測試目標: {self.base_url}")
        print("=" * 60)
        
        try:
            # 1. 基本功能測試
            print("\n=== SNTP 基本功能測試 ===")
            self.test_get_sntp_info()
            
            # 2. 配置設置測試
            print("\n=== SNTP 配置設置測試 ===")
            self.test_set_sntp_basic_config()
            time.sleep(1)
            self.test_get_sntp_info()  # 驗證設置
            
            self.test_set_sntp_with_servers()
            time.sleep(1)
            self.test_get_sntp_info()  # 驗證設置
            
            # 3. 完整工作流程測試
            self.test_complete_sntp_workflow()
            
            # 4. 參數驗證測試
            self.test_parameter_validation()
            
            # 5. 邊界條件測試
            self.test_boundary_conditions()
            
            # 6. 配置持久性測試
            self.test_configuration_persistence()
            
            # 7. 錯誤場景測試
            self.test_error_scenarios()
            
        finally:
            # 8. 恢復原始配置
            self.restore_original_config()
        
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
        get_tests = [r for r in self.test_results if '獲取' in r['test_name']]
        set_tests = [r for r in self.test_results if '設置' in r['test_name']]
        validation_tests = [r for r in self.test_results if ('驗證' in r['test_name'] or '邊界' in r['test_name'] or '持久性' in r['test_name'])]
        error_tests = [r for r in self.test_results if ('錯誤' in r['test_name'] or '無效' in r['test_name'])]
        workflow_tests = [r for r in self.test_results if '工作流程' in r['test_name']]
        
        print(f"\n功能測試統計:")
        print(f"  獲取配置測試: {len(get_tests)} 個測試")
        print(f"  設置配置測試: {len(set_tests)} 個測試")
        print(f"  工作流程測試: {len(workflow_tests)} 個測試")
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
        with open('sntp_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        print(f"\n詳細測試結果已保存到: sntp_test_results.json")
        
        # 輸出配置統計
        if self.original_config:
            print(f"\n原始配置信息:")
            print(f"  SNTP狀態: {'啟用' if self.original_config.get('sntpStatus') else '禁用'}")
            print(f"  輪詢間隔: {self.original_config.get('pollInterval')} 秒")
            print(f"  服務器數量: {len(self.original_config.get('sntpServers', []))}")

def main():
    """主函數"""
    if len(sys.argv) < 2:
        print("使用方法: python sntp_test.py <base_url> [username] [password]")
        print("範例: python sntp_test.py http://192.168.1.1 admin admin123")
        print("\n功能說明:")
        print("  - 測試所有SNTP API功能")
        print("  - 包含IPv4和IPv6服務器測試")
        print("  - 參數驗證和邊界條件測試")
        print("  - 配置持久性驗證")
        print("  - 自動恢復原始配置")
        print("  - 生成詳細測試報告")
        print("\n注意事項:")
        print("  - 輪詢間隔範圍: 16-16384 秒")
        print("  - 支持IPv4和IPv6地址")
        print("  - 測試會修改SNTP配置，完成後自動恢復")
        sys.exit(1)
    
    base_url = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else None
    password = sys.argv[3] if len(sys.argv) > 3 else None
    
    # 創建測試器並運行測試
    tester = SNTPAPITester(base_url, username, password)
    
    try:
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n測試被用戶中斷")
        print("正在恢復原始配置...")
        tester.restore_original_config()
    except Exception as e:
        print(f"\n測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        print("正在恢復原始配置...")
        tester.restore_original_config()

if __name__ == "__main__":
    main()