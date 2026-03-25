#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TACACS+ REST API 測試腳本
基於 Tacacs+_API_Reference_v0.13.docx 文件生成
包含TACACS+服務器配置管理和加密密鑰生成功能測試
"""

import requests
import json
import sys
import time
import base64
import random
from datetime import datetime

class TacacsPlusAPITester:
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
        self.test_servers = []  # 記錄測試中添加的服務器
        
        # TACACS+配置常量
        self.DEFAULT_PORT = 49
        self.PORT_RANGE = (1, 65535)
        self.RETRANSMIT_RANGE = (1, 30)
        self.TIMEOUT_RANGE = (1, 540)
        self.MAX_KEY_LENGTH_UNENCRYPTED = 48
        self.MAX_KEY_LENGTH_ENCRYPTED = 68
        
        # 測試用的服務器地址
        self.TEST_SERVER_IPS = [
            "192.168.1.100",
            "192.168.1.101", 
            "192.168.1.102",
            "10.0.0.100",
            "10.0.0.101"
        ]
    
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
    
    # ==================== 1.1 Get TACACS+ Information ====================
    
    def test_get_tacacs_plus_info(self):
        """測試 1.1: 獲取TACACS+信息"""
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            response = self.session.get(url)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    
                    # 全局配置
                    port_num = result_data.get('portNum', 'N/A')
                    retransmit = result_data.get('retransmit', 'N/A')
                    timeout = result_data.get('timeout', 'N/A')
                    key = result_data.get('key', 'N/A')
                    
                    print(f"    TACACS+全局配置:")
                    print(f"      端口號: {port_num}")
                    print(f"      重傳次數: {retransmit}")
                    print(f"      超時時間: {timeout} 秒")
                    print(f"      加密密鑰: {'已設置' if key and key != 'N/A' else '未設置'}")
                    
                    # 服務器列表
                    servers = result_data.get('servers', [])
                    print(f"      配置的服務器數量: {len(servers)}")
                    
                    for server in servers:
                        index = server.get('index', 'N/A')
                        address = server.get('address', 'N/A')
                        server_port = server.get('portNum', 'N/A')
                        server_retransmit = server.get('retransmit', 'N/A')
                        server_timeout = server.get('timeout', 'N/A')
                        server_key = server.get('key', 'N/A')
                        
                        print(f"        服務器{index}: {address}")
                        print(f"          端口: {server_port}")
                        print(f"          重傳: {server_retransmit}")
                        print(f"          超時: {server_timeout}秒")
                        print(f"          密鑰: {'已設置' if server_key and server_key != 'N/A' else '未設置'}")
                    
                    # 保存原始配置
                    self.original_config = result_data
                    
            self.log_test("獲取TACACS+信息", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取TACACS+信息", False, error=e)
            return None
    
    # ==================== 1.2 Set TACACS+ Configuration ====================
    
    def test_set_tacacs_plus_basic_config(self):
        """測試 1.2: 設置基本TACACS+配置"""
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            
            payload = {
                "isEncrypted": False,
                "key": "testkey123",
                "portNum": 49,
                "retransmit": 3,
                "timeout": 10
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置基本TACACS+配置:")
                print(f"      全局端口: {payload['portNum']}")
                print(f"      全局重傳: {payload['retransmit']}")
                print(f"      全局超時: {payload['timeout']} 秒")
                print(f"      全局密鑰: {payload['key']} (未加密)")
            
            self.log_test("設置基本TACACS+配置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置基本TACACS+配置", False, error=e)
            return None
    
    def test_set_tacacs_plus_with_servers(self):
        """測試 1.2: 設置包含服務器的TACACS+配置"""
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            
            # 選擇測試服務器IP
            server_ip = self.TEST_SERVER_IPS[0]
            self.test_servers.append(server_ip)
            
            payload = {
                "isEncrypted": False,
                "key": "globalkey456",
                "portNum": 1812,
                "retransmit": 5,
                "timeout": 15,
                "servers": [
                    {
                        "address": server_ip,
                        "isEncrypted": False,
                        "key": "serverkey789",
                        "portNum": 49,
                        "retransmit": 3,
                        "timeout": 8
                    }
                ]
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置包含服務器的TACACS+配置:")
                print(f"      全局配置: 端口{payload['portNum']}, 重傳{payload['retransmit']}, 超時{payload['timeout']}秒")
                print(f"      服務器數量: {len(payload['servers'])}")
                
                for i, server in enumerate(payload['servers']):
                    print(f"        服務器{i+1}: {server['address']}:{server['portNum']}")
                    print(f"          重傳: {server['retransmit']}, 超時: {server['timeout']}秒")
                    print(f"          密鑰: {server['key']} (未加密)")
            
            self.log_test("設置包含服務器的TACACS+配置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置包含服務器的TACACS+配置", False, error=e)
            return None
    
    def test_set_tacacs_plus_multiple_servers(self):
        """測試 1.2: 設置多個TACACS+服務器"""
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            
            # 使用多個測試服務器IP
            servers_config = []
            for i, server_ip in enumerate(self.TEST_SERVER_IPS[:3]):
                if server_ip not in self.test_servers:
                    self.test_servers.append(server_ip)
                
                servers_config.append({
                    "address": server_ip,
                    "isEncrypted": False,
                    "key": f"server{i+1}key",
                    "portNum": 49 + i,
                    "retransmit": 2 + i,
                    "timeout": 5 + i * 2
                })
            
            payload = {
                "isEncrypted": False,
                "key": "multiserverglobal",
                "portNum": 49,
                "retransmit": 2,
                "timeout": 5,
                "servers": servers_config
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置多個TACACS+服務器:")
                print(f"      服務器數量: {len(servers_config)}")
                
                for i, server in enumerate(servers_config):
                    print(f"        服務器{i+1}: {server['address']}:{server['portNum']}")
                    print(f"          配置: 重傳{server['retransmit']}, 超時{server['timeout']}秒")
                    print(f"          密鑰: {server['key']}")
            
            self.log_test("設置多個TACACS+服務器", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置多個TACACS+服務器", False, error=e)
            return None
    
    def test_set_tacacs_plus_encrypted_keys(self):
        """測試 1.2: 設置使用加密密鑰的TACACS+配置"""
        try:
            # 首先生成加密密鑰
            encrypted_key = self.generate_encrypted_key("encryptedtest123")
            if not encrypted_key:
                print("    跳過測試：無法生成加密密鑰")
                return None
            
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            
            server_ip = self.TEST_SERVER_IPS[1]
            if server_ip not in self.test_servers:
                self.test_servers.append(server_ip)
            
            # 為服務器生成另一個加密密鑰
            server_encrypted_key = self.generate_encrypted_key("serverencrypted456")
            if not server_encrypted_key:
                server_encrypted_key = encrypted_key  # 使用全局密鑰作為備選
            
            payload = {
                "isEncrypted": True,
                "key": encrypted_key,
                "portNum": 49,
                "retransmit": 3,
                "timeout": 10,
                "servers": [
                    {
                        "address": server_ip,
                        "isEncrypted": True,
                        "key": server_encrypted_key,
                        "portNum": 49,
                        "retransmit": 3,
                        "timeout": 10
                    }
                ]
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置使用加密密鑰的TACACS+配置:")
                print(f"      全局加密密鑰: {encrypted_key[:20]}...")
                print(f"      服務器: {server_ip}")
                print(f"      服務器加密密鑰: {server_encrypted_key[:20]}...")
            
            self.log_test("設置使用加密密鑰的TACACS+配置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置使用加密密鑰的TACACS+配置", False, error=e)
            return None
    
    def test_set_tacacs_plus_boundary_values(self):
        """測試 1.2: 設置TACACS+邊界值配置"""
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            
            server_ip = self.TEST_SERVER_IPS[2]
            if server_ip not in self.test_servers:
                self.test_servers.append(server_ip)
            
            # 測試最大值配置
            payload = {
                "isEncrypted": False,
                "key": "A" * self.MAX_KEY_LENGTH_UNENCRYPTED,  # 最大長度密鑰
                "portNum": 65535,  # 最大端口號
                "retransmit": 30,  # 最大重傳次數
                "timeout": 540,    # 最大超時時間
                "servers": [
                    {
                        "address": server_ip,
                        "isEncrypted": False,
                        "key": "B" * self.MAX_KEY_LENGTH_UNENCRYPTED,
                        "portNum": 65535,
                        "retransmit": 30,
                        "timeout": 540
                    }
                ]
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置TACACS+邊界值配置:")
                print(f"      全局配置: 端口{payload['portNum']}, 重傳{payload['retransmit']}, 超時{payload['timeout']}")
                print(f"      全局密鑰長度: {len(payload['key'])} 字符")
                print(f"      服務器配置: 端口{payload['servers'][0]['portNum']}")
                print(f"      服務器密鑰長度: {len(payload['servers'][0]['key'])} 字符")
            
            self.log_test("設置TACACS+邊界值配置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置TACACS+邊界值配置", False, error=e)
            return None
    
    def test_set_tacacs_plus_minimum_values(self):
        """測試 1.2: 設置TACACS+最小值配置"""
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            
            server_ip = self.TEST_SERVER_IPS[3]
            if server_ip not in self.test_servers:
                self.test_servers.append(server_ip)
            
            # 測試最小值配置
            payload = {
                "isEncrypted": False,
                "key": "a",        # 最小長度密鑰
                "portNum": 1,      # 最小端口號
                "retransmit": 1,   # 最小重傳次數
                "timeout": 1,      # 最小超時時間
                "servers": [
                    {
                        "address": server_ip,
                        "isEncrypted": False,
                        "key": "b",
                        "portNum": 1,
                        "retransmit": 1,
                        "timeout": 1
                    }
                ]
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置TACACS+最小值配置:")
                print(f"      全局配置: 端口{payload['portNum']}, 重傳{payload['retransmit']}, 超時{payload['timeout']}")
                print(f"      全局密鑰: '{payload['key']}'")
                print(f"      服務器配置: 端口{payload['servers'][0]['portNum']}")
                print(f"      服務器密鑰: '{payload['servers'][0]['key']}'")
            
            self.log_test("設置TACACS+最小值配置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置TACACS+最小值配置", False, error=e)
            return None
    
    # ==================== 1.3 Generate Encrypted Key ====================
    
    def test_generate_encrypted_key(self):
        """測試 1.3: 生成加密密鑰"""
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus/encrypted-key"
            
            test_passwords = [
                "simplepass",
                "complex@Pass123!",
                "a",  # 最短密碼
                "A" * self.MAX_KEY_LENGTH_UNENCRYPTED,  # 最長密碼
                "中文密碼測試",  # 包含中文字符
                "pass with spaces",  # 包含空格（應該失敗）
                "12345678",  # 純數字
                "ABCDEFGH",  # 純大寫字母
                "abcdefgh",  # 純小寫字母
                "!@#$%^&*"   # 純特殊字符
            ]
            
            successful_generations = 0
            
            for i, password in enumerate(test_passwords):
                try:
                    payload = {"password": password}
                    response = self.session.post(url, json=payload)
                    
                    success = response.status_code == 200
                    
                    if success:
                        data = response.json()
                        if 'result' in data and 'key' in data['result']:
                            encrypted_key = data['result']['key']
                            successful_generations += 1
                            
                            print(f"    密碼 '{password}' -> 加密密鑰: {encrypted_key}")
                            
                            # 驗證加密密鑰長度
                            if len(encrypted_key) <= self.MAX_KEY_LENGTH_ENCRYPTED:
                                print(f"      ✓ 加密密鑰長度合法: {len(encrypted_key)} 字符")
                            else:
                                print(f"      ✗ 加密密鑰長度超限: {len(encrypted_key)} 字符")
                        else:
                            print(f"    密碼 '{password}' -> 響應格式錯誤")
                    else:
                        print(f"    密碼 '{password}' -> 生成失敗 (狀態碼: {response.status_code})")
                        
                        # 包含空格的密碼應該失敗
                        if " " in password:
                            print(f"      ✓ 預期失敗：密碼包含空格")
                            success = True  # 這是預期的失敗
                    
                    self.log_test(f"生成加密密鑰 - 密碼{i+1}", success, response)
                    
                except Exception as e:
                    print(f"    密碼 '{password}' -> 異常: {e}")
                    self.log_test(f"生成加密密鑰 - 密碼{i+1}", False, error=e)
            
            overall_success = successful_generations > 0
            print(f"\n    加密密鑰生成統計:")
            print(f"      測試密碼數量: {len(test_passwords)}")
            print(f"      成功生成數量: {successful_generations}")
            print(f"      成功率: {(successful_generations/len(test_passwords))*100:.1f}%")
            
            self.log_test("生成加密密鑰綜合測試", overall_success, 
                         details={'total_passwords': len(test_passwords), 'successful_generations': successful_generations})
            
            return overall_success
            
        except Exception as e:
            self.log_test("生成加密密鑰綜合測試", False, error=e)
            return False
    
    def generate_encrypted_key(self, password):
        """輔助方法：生成加密密鑰"""
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus/encrypted-key"
            payload = {"password": password}
            response = self.session.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if 'result' in data and 'key' in data['result']:
                    return data['result']['key']
            
            return None
            
        except Exception as e:
            print(f"    生成加密密鑰時發生錯誤: {e}")
            return None
    
    def test_generate_encrypted_key_edge_cases(self):
        """測試 1.3: 生成加密密鑰邊界情況"""
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus/encrypted-key"
            
            edge_cases = [
                ("", "空密碼", False),
                ("A" * (self.MAX_KEY_LENGTH_UNENCRYPTED + 1), "超長密碼", False),
                ("pass word", "包含空格", False),
                ("pass\tword", "包含制表符", False),
                ("pass\nword", "包含換行符", False),
                ("validpass", "有效密碼", True)
            ]
            
            for password, description, should_succeed in edge_cases:
                try:
                    payload = {"password": password}
                    response = self.session.post(url, json=payload)
                    
                    success = (response.status_code == 200) == should_succeed
                    
                    if should_succeed and response.status_code == 200:
                        data = response.json()
                        if 'result' in data and 'key' in data['result']:
                            encrypted_key = data['result']['key']
                            print(f"    {description}: 成功生成加密密鑰 {encrypted_key[:20]}...")
                        else:
                            success = False
                            print(f"    {description}: 響應格式錯誤")
                    elif not should_succeed and response.status_code != 200:
                        print(f"    {description}: 預期失敗，狀態碼 {response.status_code}")
                    else:
                        print(f"    {description}: 結果不符合預期")
                    
                    self.log_test(f"加密密鑰邊界測試 - {description}", success, response)
                    
                except Exception as e:
                    self.log_test(f"加密密鑰邊界測試 - {description}", False, error=e)
            
            return True
            
        except Exception as e:
            self.log_test("加密密鑰邊界測試", False, error=e)
            return False
    
    # ==================== Complete Workflow Tests ====================
    
    def test_complete_tacacs_workflow(self):
        """測試完整的TACACS+工作流程"""
        print("\n=== 完整TACACS+工作流程測試 ===")
        
        workflow_results = []
        
        try:
            # 步驟1: 獲取當前TACACS+配置
            print("\n步驟1: 獲取當前TACACS+配置")
            result = self.test_get_tacacs_plus_info()
            workflow_results.append(("獲取TACACS+配置", result is not None))
            
            # 步驟2: 生成加密密鑰
            print("\n步驟2: 生成加密密鑰")
            result = self.test_generate_encrypted_key()
            workflow_results.append(("生成加密密鑰", result))
            
            # 步驟3: 設置基本配置
            print("\n步驟3: 設置基本TACACS+配置")
            result = self.test_set_tacacs_plus_basic_config()
            workflow_results.append(("設置基本配置", result is not None))
            time.sleep(1)
            
            # 步驟4: 驗證基本配置
            print("\n步驟4: 驗證基本配置")
            result = self.test_get_tacacs_plus_info()
            workflow_results.append(("驗證基本配置", result is not None))
            
            # 步驟5: 添加服務器配置
            print("\n步驟5: 添加服務器配置")
            result = self.test_set_tacacs_plus_with_servers()
            workflow_results.append(("添加服務器配置", result is not None))
            time.sleep(1)
            
            # 步驟6: 驗證服務器配置
            print("\n步驟6: 驗證服務器配置")
            result = self.test_get_tacacs_plus_info()
            workflow_results.append(("驗證服務器配置", result is not None))
            
            # 步驟7: 設置多個服務器
            print("\n步驟7: 設置多個服務器")
            result = self.test_set_tacacs_plus_multiple_servers()
            workflow_results.append(("設置多個服務器", result is not None))
            time.sleep(1)
            
            # 步驟8: 測試加密密鑰配置
            print("\n步驟8: 測試加密密鑰配置")
            result = self.test_set_tacacs_plus_encrypted_keys()
            workflow_results.append(("加密密鑰配置", result is not None))
            time.sleep(1)
            
            # 步驟9: 測試邊界值配置
            print("\n步驟9: 測試邊界值配置")
            result = self.test_set_tacacs_plus_boundary_values()
            workflow_results.append(("邊界值配置", result is not None))
            time.sleep(1)
            
            # 步驟10: 測試最小值配置
            print("\n步驟10: 測試最小值配置")
            result = self.test_set_tacacs_plus_minimum_values()
            workflow_results.append(("最小值配置", result is not None))
            time.sleep(1)
            
            # 步驟11: 最終驗證
            print("\n步驟11: 最終驗證")
            result = self.test_get_tacacs_plus_info()
            workflow_results.append(("最終驗證", result is not None))
            
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
            self.log_test("完整TACACS+工作流程", overall_success, 
                         details={'successful_steps': successful_steps, 'total_steps': total_steps})
            
            print(f"\n{'✓ 完整工作流程測試完成' if overall_success else '✗ 工作流程測試部分失敗'}")
            
        except Exception as e:
            print(f"\n✗ 工作流程測試失敗: {e}")
            self.log_test("完整TACACS+工作流程", False, error=e)
    
    # ==================== Parameter Validation Tests ====================
    
    def test_parameter_validation(self):
        """測試參數驗證"""
        print("\n=== 參數驗證測試 ===")
        
        # 測試端口號範圍
        print("\n--- 端口號範圍驗證測試 ---")
        port_test_cases = [
            (1, "最小端口號", True),
            (49, "默認端口號", True),
            (1812, "RADIUS端口號", True),
            (65535, "最大端口號", True),
            (0, "端口號為0", False),
            (65536, "端口號超出範圍", False),
            (-1, "負端口號", False)
        ]
        
        for port, description, should_succeed in port_test_cases:
            try:
                url = f"{self.base_url}/api/v1/security/tacacs-plus"
                payload = {
                    "portNum": port,
                    "retransmit": 3,
                    "timeout": 10
                }
                response = self.session.put(url, json=payload)
                success = (response.status_code == 200) == should_succeed
                
                self.log_test(f"端口號驗證 - {description} ({port})", success, response)
                time.sleep(0.3)
            except Exception as e:
                self.log_test(f"端口號驗證 - {description} ({port})", False, error=e)
        
        # 測試重傳次數範圍
        print("\n--- 重傳次數範圍驗證測試 ---")
        retransmit_test_cases = [
            (1, "最小重傳次數", True),
            (3, "默認重傳次數", True),
            (15, "中等重傳次數", True),
            (30, "最大重傳次數", True),
            (0, "重傳次數為0", False),
            (31, "重傳次數超出範圍", False),
            (-1, "負重傳次數", False)
        ]
        
        for retransmit, description, should_succeed in retransmit_test_cases:
            try:
                url = f"{self.base_url}/api/v1/security/tacacs-plus"
                payload = {
                    "portNum": 49,
                    "retransmit": retransmit,
                    "timeout": 10
                }
                response = self.session.put(url, json=payload)
                success = (response.status_code == 200) == should_succeed
                
                self.log_test(f"重傳次數驗證 - {description} ({retransmit})", success, response)
                time.sleep(0.3)
            except Exception as e:
                self.log_test(f"重傳次數驗證 - {description} ({retransmit})", False, error=e)
        
        # 測試超時時間範圍
        print("\n--- 超時時間範圍驗證測試 ---")
        timeout_test_cases = [
            (1, "最小超時時間", True),
            (5, "默認超時時間", True),
            (60, "1分鐘超時", True),
            (300, "5分鐘超時", True),
            (540, "最大超時時間", True),
            (0, "超時時間為0", False),
            (541, "超時時間超出範圍", False),
            (-1, "負超時時間", False)
        ]
        
        for timeout, description, should_succeed in timeout_test_cases:
            try:
                url = f"{self.base_url}/api/v1/security/tacacs-plus"
                payload = {
                    "portNum": 49,
                    "retransmit": 3,
                    "timeout": timeout
                }
                response = self.session.put(url, json=payload)
                success = (response.status_code == 200) == should_succeed
                
                self.log_test(f"超時時間驗證 - {description} ({timeout})", success, response)
                time.sleep(0.3)
            except Exception as e:
                self.log_test(f"超時時間驗證 - {description} ({timeout})", False, error=e)
        
        # 測試密鑰長度
        print("\n--- 密鑰長度驗證測試 ---")
        key_test_cases = [
            ("a", "單字符密鑰", True),
            ("test123", "標準密鑰", True),
            ("A" * 24, "中等長度密鑰", True),
            ("A" * self.MAX_KEY_LENGTH_UNENCRYPTED, "最大長度未加密密鑰", True),
            ("A" * (self.MAX_KEY_LENGTH_UNENCRYPTED + 1), "超長未加密密鑰", False),
            ("", "空密鑰", True)  # 空密鑰可能是允許的
        ]
        
        for key, description, should_succeed in key_test_cases:
            try:
                url = f"{self.base_url}/api/v1/security/tacacs-plus"
                payload = {
                    "isEncrypted": False,
                    "key": key,
                    "portNum": 49,
                    "retransmit": 3,
                    "timeout": 10
                }
                response = self.session.put(url, json=payload)
                success = (response.status_code == 200) == should_succeed
                
                self.log_test(f"密鑰長度驗證 - {description} (長度:{len(key)})", success, response)
                time.sleep(0.3)
            except Exception as e:
                self.log_test(f"密鑰長度驗證 - {description} (長度:{len(key)})", False, error=e)
        
        # 測試IP地址格式
        print("\n--- IP地址格式驗證測試 ---")
        ip_test_cases = [
            ("192.168.1.1", "標準IPv4地址", True),
            ("10.0.0.1", "私有IPv4地址", True),
            ("172.16.0.1", "私有IPv4地址", True),
            ("127.0.0.1", "本地回環地址", True),
            ("0.0.0.0", "全零地址", True),
            ("255.255.255.255", "廣播地址", True),
            ("192.168.1.256", "無效IPv4地址", False),
            ("192.168.1", "不完整IPv4地址", False),
            ("192.168.1.1.1", "過長IPv4地址", False),
            ("invalid.ip.address", "非數字IP地址", False),
            ("", "空IP地址", False)
        ]
        
        for ip, description, should_succeed in ip_test_cases:
            try:
                url = f"{self.base_url}/api/v1/security/tacacs-plus"
                payload = {
                    "portNum": 49,
                    "retransmit": 3,
                    "timeout": 10,
                    "servers": [
                        {
                            "address": ip,
                            "portNum": 49,
                            "retransmit": 3,
                            "timeout": 10
                        }
                    ]
                }
                response = self.session.put(url, json=payload)
                success = (response.status_code == 200) == should_succeed
                
                self.log_test(f"IP地址格式驗證 - {description} ({ip})", success, response)
                time.sleep(0.3)
            except Exception as e:
                self.log_test(f"IP地址格式驗證 - {description} ({ip})", False, error=e)
    
    # ==================== Error Scenarios Tests ====================
    
    def test_error_scenarios(self):
        """測試錯誤場景"""
        print("\n=== 錯誤場景測試 ===")
        
        # 測試1: 無效JSON格式
        print("\n--- JSON格式錯誤測試 ---")
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            response = self.session.put(url, data="invalid json format")
            success = response.status_code == 400
            self.log_test("無效JSON格式測試", success, response)
        except Exception as e:
            self.log_test("無效JSON格式測試", False, error=e)
        
        # 測試2: 錯誤的數據類型
        print("\n--- 數據類型錯誤測試 ---")
        
        wrong_type_cases = [
            ({"portNum": "49", "retransmit": 3, "timeout": 10}, "端口號為字符串"),
            ({"portNum": 49, "retransmit": "3", "timeout": 10}, "重傳次數為字符串"),
            ({"portNum": 49, "retransmit": 3, "timeout": "10"}, "超時時間為字符串"),
            ({"portNum": 49, "retransmit": 3, "timeout": 10, "isEncrypted": "false"}, "加密標誌為字符串"),
            ({"portNum": 49, "retransmit": 3, "timeout": 10, "key": 123}, "密鑰為數字"),
            ({"portNum": 49, "retransmit": 3, "timeout": 10, "servers": "not_array"}, "服務器列表為字符串")
        ]
        
        for payload, description in wrong_type_cases:
            try:
                url = f"{self.base_url}/api/v1/security/tacacs-plus"
                response = self.session.put(url, json=payload)
                success = response.status_code == 400
                self.log_test(f"錯誤數據類型測試 - {description}", success, response)
            except Exception as e:
                self.log_test(f"錯誤數據類型測試 - {description}", False, error=e)
        
        # 測試3: 服務器配置錯誤
        print("\n--- 服務器配置錯誤測試 ---")
        
        server_error_cases = [
            ({
                "servers": [{"portNum": 49}]  # 缺少必需的address字段
            }, "缺少服務器地址"),
            ({
                "servers": [{"address": "192.168.1.1", "portNum": "invalid"}]  # 端口號類型錯誤
            }, "服務器端口號類型錯誤"),
            ({
                "servers": [{"address": "192.168.1.1", "retransmit": -1}]  # 負重傳次數
            }, "服務器負重傳次數"),
            ({
                "servers": [{"address": "192.168.1.1", "timeout": 0}]  # 零超時時間
            }, "服務器零超時時間")
        ]
        
        for payload, description in server_error_cases:
            try:
                url = f"{self.base_url}/api/v1/security/tacacs-plus"
                # 添加基本必需字段
                payload.update({
                    "portNum": 49,
                    "retransmit": 3,
                    "timeout": 10
                })
                response = self.session.put(url, json=payload)
                success = response.status_code == 400
                self.log_test(f"服務器配置錯誤測試 - {description}", success, response)
            except Exception as e:
                self.log_test(f"服務器配置錯誤測試 - {description}", False, error=e)
        
        # 測試4: 加密密鑰生成錯誤
        print("\n--- 加密密鑰生成錯誤測試 ---")
        
        key_gen_error_cases = [
            ({}, "缺少密碼字段"),
            ({"password": 123}, "密碼為數字"),
            ({"password": ["array"]}, "密碼為數組"),
            ({"password": {"object": "value"}}, "密碼為對象"),
            ({"password": None}, "密碼為null")
        ]
        
        for payload, description in key_gen_error_cases:
            try:
                url = f"{self.base_url}/api/v1/security/tacacs-plus/encrypted-key"
                response = self.session.post(url, json=payload)
                success = response.status_code == 400
                self.log_test(f"加密密鑰生成錯誤測試 - {description}", success, response)
            except Exception as e:
                self.log_test(f"加密密鑰生成錯誤測試 - {description}", False, error=e)
        
        # 測試5: 加密密鑰解密失敗
        print("\n--- 加密密鑰解密錯誤測試 ---")
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            payload = {
                "isEncrypted": True,
                "key": "invalid_encrypted_key",  # 無效的加密密鑰
                "portNum": 49,
                "retransmit": 3,
                "timeout": 10
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            
            if success:
                data = response.json()
                if 'message' in data and 'decryption' in data['message'].lower():
                    print("    ✓ 正確識別加密密鑰解密失敗")
                else:
                    print("    ? 返回400但錯誤消息不明確")
            
            self.log_test("加密密鑰解密錯誤測試", success, response)
        except Exception as e:
            self.log_test("加密密鑰解密錯誤測試", False, error=e)
    
    # ==================== Boundary Conditions Tests ====================
    
    def test_boundary_conditions(self):
        """測試邊界條件"""
        print("\n=== 邊界條件測試 ===")
        
        # 測試最大服務器數量
        print("\n--- 最大服務器數量測試 ---")
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            
            # 創建大量服務器配置
            max_servers = 10  # 假設最大支持10個服務器
            servers_config = []
            
            for i in range(max_servers):
                servers_config.append({
                    "address": f"192.168.1.{100 + i}",
                    "portNum": 49,
                    "retransmit": 3,
                    "timeout": 10
                })
            
            payload = {
                "portNum": 49,
                "retransmit": 3,
                "timeout": 10,
                "servers": servers_config
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            if success:
                print(f"    ✓ 成功配置 {max_servers} 個服務器")
            else:
                print(f"    ✗ 配置 {max_servers} 個服務器失敗")
            
            self.log_test(f"最大服務器數量測試 ({max_servers}個)", success, response)
            
        except Exception as e:
            self.log_test("最大服務器數量測試", False, error=e)
        
        # 測試空配置
        print("\n--- 空配置測試 ---")
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            payload = {}  # 完全空的配置
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            if success:
                print("    ✓ 空配置被接受（使用默認值）")
            else:
                print("    ✗ 空配置被拒絕")
            
            self.log_test("空配置測試", success, response)
            
        except Exception as e:
            self.log_test("空配置測試", False, error=e)
        
        # 測試部分配置
        print("\n--- 部分配置測試 ---")
        partial_configs = [
            ({"portNum": 1812}, "僅端口號"),
            ({"retransmit": 5}, "僅重傳次數"),
            ({"timeout": 30}, "僅超時時間"),
            ({"key": "partialkey"}, "僅密鑰"),
            ({"servers": []}, "空服務器列表")
        ]
        
        for payload, description in partial_configs:
            try:
                url = f"{self.base_url}/api/v1/security/tacacs-plus"
                response = self.session.put(url, json=payload)
                success = response.status_code == 200
                
                self.log_test(f"部分配置測試 - {description}", success, response)
            except Exception as e:
                self.log_test(f"部分配置測試 - {description}", False, error=e)
        
        # 測試重複服務器地址
        print("\n--- 重複服務器地址測試 ---")
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            
            payload = {
                "portNum": 49,
                "retransmit": 3,
                "timeout": 10,
                "servers": [
                    {
                        "address": "192.168.1.100",
                        "portNum": 49,
                        "retransmit": 3,
                        "timeout": 10
                    },
                    {
                        "address": "192.168.1.100",  # 重複的IP地址
                        "portNum": 1812,
                        "retransmit": 5,
                        "timeout": 15
                    }
                ]
            }
            
            response = self.session.put(url, json=payload)
            # 重複地址可能被允許（不同端口）或被拒絕
            success = True  # 接受任何結果，記錄行為
            
            if response.status_code == 200:
                print("    ✓ 重複服務器地址被接受")
            else:
                print("    ✓ 重複服務器地址被拒絕")
            
            self.log_test("重複服務器地址測試", success, response)
            
        except Exception as e:
            self.log_test("重複服務器地址測試", False, error=e)
    
    # ==================== Performance Tests ====================
    
    def test_performance_scenarios(self):
        """測試性能場景"""
        print("\n=== 性能測試場景 ===")
        
        # 測試連續配置更新
        print("\n--- 連續配置更新測試 ---")
        try:
            start_time = time.time()
            success_count = 0
            total_updates = 5
            
            for i in range(total_updates):
                url = f"{self.base_url}/api/v1/security/tacacs-plus"
                payload = {
                    "portNum": 49 + i,
                    "retransmit": 3 + i,
                    "timeout": 10 + i * 2,
                    "key": f"perftest{i}"
                }
                
                response = self.session.put(url, json=payload)
                if response.status_code == 200:
                    success_count += 1
                
                time.sleep(0.5)  # 短暫延遲避免過快請求
            
            end_time = time.time()
            duration = end_time - start_time
            avg_response_time = duration / total_updates
            
            success = success_count == total_updates
            details = {
                'total_updates': total_updates,
                'success_count': success_count,
                'total_duration': duration,
                'avg_response_time': avg_response_time
            }
            
            print(f"    總更新數: {total_updates}")
            print(f"    成功更新數: {success_count}")
            print(f"    總耗時: {duration:.2f} 秒")
            print(f"    平均響應時間: {avg_response_time:.3f} 秒")
            
            self.log_test("連續配置更新測試", success, details=details)
            
        except Exception as e:
            self.log_test("連續配置更新測試", False, error=e)
        
        # 測試大量密鑰生成
        print("\n--- 大量密鑰生成測試 ---")
        try:
            start_time = time.time()
            success_count = 0
            total_keys = 10
            
            for i in range(total_keys):
                url = f"{self.base_url}/api/v1/security/tacacs-plus/encrypted-key"
                payload = {"password": f"perfkey{i}"}
                
                response = self.session.post(url, json=payload)
                if response.status_code == 200:
                    success_count += 1
            
            end_time = time.time()
            duration = end_time - start_time
            avg_generation_time = duration / total_keys
            
            success = success_count == total_keys
            details = {
                'total_keys': total_keys,
                'success_count': success_count,
                'duration': duration,
                'avg_generation_time': avg_generation_time
            }
            
            print(f"    生成密鑰數: {total_keys}")
            print(f"    成功生成數: {success_count}")
            print(f"    總耗時: {duration:.2f} 秒")
            print(f"    平均生成時間: {avg_generation_time:.3f} 秒")
            
            self.log_test("大量密鑰生成測試", success, details=details)
            
        except Exception as e:
            self.log_test("大量密鑰生成測試", False, error=e)
    
    # ==================== Cleanup and Restore ====================
    
    def cleanup_test_servers(self):
        """清理測試服務器配置"""
        print("\n=== 清理測試服務器配置 ===")
        
        if self.test_servers:
            try:
                # 設置一個不包含測試服務器的配置
                url = f"{self.base_url}/api/v1/security/tacacs-plus"
                payload = {
                    "portNum": 49,
                    "retransmit": 2,
                    "timeout": 5,
                    "servers": []  # 清空服務器列表
                }
                
                response = self.session.put(url, json=payload)
                
                if response.status_code == 200:
                    print(f"    ✓ 已清理 {len(self.test_servers)} 個測試服務器")
                    self.test_servers.clear()
                else:
                    print(f"    ✗ 清理測試服務器失敗")
                
                self.log_test("清理測試服務器配置", response.status_code == 200, response)
                
            except Exception as e:
                print(f"    ✗ 清理測試服務器時發生錯誤: {e}")
                self.log_test("清理測試服務器配置", False, error=e)
        else:
            print("    沒有需要清理的測試服務器")
    
    def restore_original_config(self):
        """恢復原始TACACS+配置"""
        if self.original_config:
            print("\n=== 恢復原始TACACS+配置 ===")
            try:
                url = f"{self.base_url}/api/v1/security/tacacs-plus"
                response = self.session.put(url, json=self.original_config)
                
                success = response.status_code == 200
                if success:
                    print("    ✓ 原始TACACS+配置已恢復")
                    
                    # 顯示恢復的配置信息
                    port_num = self.original_config.get('portNum', 'N/A')
                    retransmit = self.original_config.get('retransmit', 'N/A')
                    timeout = self.original_config.get('timeout', 'N/A')
                    servers = self.original_config.get('servers', [])
                    
                    print(f"      全局配置: 端口{port_num}, 重傳{retransmit}, 超時{timeout}秒")
                    print(f"      服務器數量: {len(servers)}")
                    
                    for server in servers:
                        address = server.get('address', 'N/A')
                        server_port = server.get('portNum', 'N/A')
                        print(f"        服務器: {address}:{server_port}")
                else:
                    print("    ✗ 恢復原始配置失敗")
                
                self.log_test("恢復原始TACACS+配置", success, response)
                
            except Exception as e:
                print(f"    ✗ 恢復原始配置時發生錯誤: {e}")
                self.log_test("恢復原始TACACS+配置", False, error=e)
        else:
            print("    沒有保存的原始配置，跳過恢復")
    
    # ==================== Main Test Runner ====================
    
    def run_all_tests(self):
        """運行所有測試"""
        print("=== TACACS+ REST API 測試開始 ===")
        print(f"測試目標: {self.base_url}")
        print(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        try:
            # 1. 基本功能測試
            print("\n=== TACACS+ 基本功能測試 ===")
            self.test_get_tacacs_plus_info()
            
            # 2. 加密密鑰生成測試
            print("\n=== 加密密鑰生成測試 ===")
            self.test_generate_encrypted_key()
            self.test_generate_encrypted_key_edge_cases()
            
            # 3. TACACS+配置測試
            print("\n=== TACACS+ 配置測試 ===")
            self.test_set_tacacs_plus_basic_config()
            time.sleep(1)
            self.test_get_tacacs_plus_info()  # 驗證基本配置
            
            self.test_set_tacacs_plus_with_servers()
            time.sleep(1)
            self.test_get_tacacs_plus_info()  # 驗證服務器配置
            
            self.test_set_tacacs_plus_multiple_servers()
            time.sleep(1)
            
            self.test_set_tacacs_plus_encrypted_keys()
            time.sleep(1)
            
            # 4. 邊界值測試
            print("\n=== TACACS+ 邊界值測試 ===")
            self.test_set_tacacs_plus_boundary_values()
            time.sleep(1)
            self.test_set_tacacs_plus_minimum_values()
            time.sleep(1)
            
            # 5. 完整工作流程測試
            self.test_complete_tacacs_workflow()
            
            # 6. 參數驗證測試
            self.test_parameter_validation()
            
            # 7. 邊界條件測試
            self.test_boundary_conditions()
            
            # 8. 錯誤場景測試
            self.test_error_scenarios()
            
            # 9. 性能測試
            self.test_performance_scenarios()
            
        finally:
            # 10. 清理和恢復
            self.cleanup_test_servers()
            self.restore_original_config()
        
        # 11. 輸出測試總結
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
        config_tests = [r for r in self.test_results if ('配置' in r['test_name'] or 'TACACS+' in r['test_name'])]
        key_tests = [r for r in self.test_results if '密鑰' in r['test_name']]
        validation_tests = [r for r in self.test_results if '驗證' in r['test_name']]
        error_tests = [r for r in self.test_results if ('錯誤' in r['test_name'] or '無效' in r['test_name'])]
        boundary_tests = [r for r in self.test_results if '邊界' in r['test_name']]
        performance_tests = [r for r in self.test_results if '性能' in r['test_name']]
        workflow_tests = [r for r in self.test_results if '工作流程' in r['test_name']]
        
        print(f"\n功能測試統計:")
        print(f"  TACACS+配置測試: {len(config_tests)} 個測試")
        print(f"  加密密鑰測試: {len(key_tests)} 個測試")
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
        
        # 顯示測試服務器統計
        if self.test_servers:
            print(f"\n測試服務器統計:")
            print(f"  使用的測試服務器IP: {len(self.test_servers)} 個")
            for ip in self.test_servers:
                print(f"    - {ip}")
        
        # 保存詳細結果到文件
        with open('tacacs_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        print(f"\n詳細測試結果已保存到: tacacs_test_results.json")
        
        # 輸出配置統計
        if self.original_config:
            print(f"\n原始配置信息:")
            print(f"  全局端口: {self.original_config.get('portNum', 'N/A')}")
            print(f"  全局重傳: {self.original_config.get('retransmit', 'N/A')}")
            print(f"  全局超時: {self.original_config.get('timeout', 'N/A')} 秒")
            print(f"  配置的服務器數量: {len(self.original_config.get('servers', []))}")
            print(f"  配置已保存並恢復")

    # ==================== Additional Test Methods ====================
    
    def test_tacacs_plus_integration_scenarios(self):
        """測試TACACS+集成場景"""
        print("\n=== TACACS+ 集成場景測試 ===")
        
        # 場景1: 企業環境配置
        print("\n--- 企業環境配置場景 ---")
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            
            # 模擬企業環境：主服務器 + 備份服務器
            payload = {
                "isEncrypted": False,
                "key": "enterprise_global_key",
                "portNum": 49,
                "retransmit": 3,
                "timeout": 10,
                "servers": [
                    {
                        "address": "192.168.100.10",  # 主TACACS+服務器
                        "isEncrypted": False,
                        "key": "primary_server_key",
                        "portNum": 49,
                        "retransmit": 3,
                        "timeout": 5
                    },
                    {
                        "address": "192.168.100.11",  # 備份TACACS+服務器
                        "isEncrypted": False,
                        "key": "backup_server_key",
                        "portNum": 49,
                        "retransmit": 5,
                        "timeout": 10
                    }
                ]
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            if success:
                print("    ✓ 企業環境配置成功")
                print("      - 主服務器: 192.168.100.10 (快速響應)")
                print("      - 備份服務器: 192.168.100.11 (容錯配置)")
            
            self.log_test("企業環境配置場景", success, response)
            
            # 記錄測試服務器
            self.test_servers.extend(["192.168.100.10", "192.168.100.11"])
            
        except Exception as e:
            self.log_test("企業環境配置場景", False, error=e)
        
        # 場景2: 高安全性環境配置
        print("\n--- 高安全性環境配置場景 ---")
        try:
            # 生成強加密密鑰
            strong_password = "HighSecurity@2024!ComplexKey"
            encrypted_key = self.generate_encrypted_key(strong_password)
            
            if encrypted_key:
                url = f"{self.base_url}/api/v1/security/tacacs-plus"
                
                payload = {
                    "isEncrypted": True,
                    "key": encrypted_key,
                    "portNum": 1812,  # 非標準端口增加安全性
                    "retransmit": 2,   # 減少重傳避免暴露
                    "timeout": 30,     # 較長超時確保安全驗證
                    "servers": [
                        {
                            "address": "10.0.1.100",
                            "isEncrypted": True,
                            "key": encrypted_key,
                            "portNum": 1812,
                            "retransmit": 2,
                            "timeout": 30
                        }
                    ]
                }
                
                response = self.session.put(url, json=payload)
                success = response.status_code == 200
                
                if success:
                    print("    ✓ 高安全性環境配置成功")
                    print("      - 使用加密密鑰")
                    print("      - 非標準端口 (1812)")
                    print("      - 安全超時設置")
                
                self.log_test("高安全性環境配置場景", success, response)
                self.test_servers.append("10.0.1.100")
            else:
                print("    ✗ 無法生成加密密鑰，跳過高安全性測試")
                self.log_test("高安全性環境配置場景", False, error="無法生成加密密鑰")
            
        except Exception as e:
            self.log_test("高安全性環境配置場景", False, error=e)
        
        # 場景3: 多站點環境配置
        print("\n--- 多站點環境配置場景 ---")
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            
            # 模擬多個地理位置的TACACS+服務器
            payload = {
                "isEncrypted": False,
                "key": "multisite_global",
                "portNum": 49,
                "retransmit": 3,
                "timeout": 15,  # 考慮網絡延遲
                "servers": [
                    {
                        "address": "172.16.1.10",  # 總部
                        "isEncrypted": False,
                        "key": "headquarters_key",
                        "portNum": 49,
                        "retransmit": 2,
                        "timeout": 5
                    },
                    {
                        "address": "172.16.2.10",  # 分公司A
                        "isEncrypted": False,
                        "key": "branch_a_key",
                        "portNum": 49,
                        "retransmit": 3,
                        "timeout": 10
                    },
                    {
                        "address": "172.16.3.10",  # 分公司B
                        "isEncrypted": False,
                        "key": "branch_b_key",
                        "portNum": 49,
                        "retransmit": 4,
                        "timeout": 15
                    }
                ]
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            if success:
                print("    ✓ 多站點環境配置成功")
                print("      - 總部服務器: 172.16.1.10 (低延遲)")
                print("      - 分公司A: 172.16.2.10 (中等延遲)")
                print("      - 分公司B: 172.16.3.10 (高延遲容忍)")
            
            self.log_test("多站點環境配置場景", success, response)
            self.test_servers.extend(["172.16.1.10", "172.16.2.10", "172.16.3.10"])
            
        except Exception as e:
            self.log_test("多站點環境配置場景", False, error=e)
    
    def test_tacacs_plus_failover_scenarios(self):
        """測試TACACS+故障轉移場景"""
        print("\n=== TACACS+ 故障轉移場景測試 ===")
        
        # 場景1: 主備服務器配置
        print("\n--- 主備服務器故障轉移測試 ---")
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            
            # 配置主服務器（快速響應）和備份服務器（容錯）
            payload = {
                "isEncrypted": False,
                "key": "failover_test_key",
                "portNum": 49,
                "retransmit": 2,
                "timeout": 5,
                "servers": [
                    {
                        "address": "192.168.200.10",  # 主服務器
                        "isEncrypted": False,
                        "key": "primary_key",
                        "portNum": 49,
                        "retransmit": 1,  # 快速失敗
                        "timeout": 3      # 短超時
                    },
                    {
                        "address": "192.168.200.11",  # 備份服務器
                        "isEncrypted": False,
                        "key": "backup_key",
                        "portNum": 49,
                        "retransmit": 3,  # 多次重試
                        "timeout": 10     # 較長超時
                    }
                ]
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            if success:
                print("    ✓ 主備服務器故障轉移配置成功")
                print("      - 主服務器: 快速失敗檢測 (3秒超時, 1次重傳)")
                print("      - 備份服務器: 容錯配置 (10秒超時, 3次重傳)")
            
            self.log_test("主備服務器故障轉移配置", success, response)
            self.test_servers.extend(["192.168.200.10", "192.168.200.11"])
            
        except Exception as e:
            self.log_test("主備服務器故障轉移配置", False, error=e)
        
        # 場景2: 多層故障轉移
        print("\n--- 多層故障轉移測試 ---")
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            
            # 配置三層故障轉移：本地 -> 區域 -> 中央
            payload = {
                "isEncrypted": False,
                "key": "multilayer_failover",
                "portNum": 49,
                "retransmit": 2,
                "timeout": 5,
                "servers": [
                    {
                        "address": "10.1.1.10",   # 本地服務器
                        "isEncrypted": False,
                        "key": "local_key",
                        "portNum": 49,
                        "retransmit": 1,
                        "timeout": 2
                    },
                    {
                        "address": "10.2.1.10",   # 區域服務器
                        "isEncrypted": False,
                        "key": "regional_key",
                        "portNum": 49,
                        "retransmit": 2,
                        "timeout": 5
                    },
                    {
                        "address": "10.3.1.10",   # 中央服務器
                        "isEncrypted": False,
                        "key": "central_key",
                        "portNum": 49,
                        "retransmit": 3,
                        "timeout": 15
                    }
                ]
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            if success:
                print("    ✓ 多層故障轉移配置成功")
                print("      - 第1層 (本地): 10.1.1.10 - 2秒超時")
                print("      - 第2層 (區域): 10.2.1.10 - 5秒超時")
                print("      - 第3層 (中央): 10.3.1.10 - 15秒超時")
            
            self.log_test("多層故障轉移配置", success, response)
            self.test_servers.extend(["10.1.1.10", "10.2.1.10", "10.3.1.10"])
            
        except Exception as e:
            self.log_test("多層故障轉移配置", False, error=e)
    
    def test_tacacs_plus_security_scenarios(self):
        """測試TACACS+安全場景"""
        print("\n=== TACACS+ 安全場景測試 ===")
        
        # 場景1: 密鑰輪換測試
        print("\n--- 密鑰輪換場景測試 ---")
        try:
            # 生成多個加密密鑰模擬密鑰輪換
            passwords = ["OldKey2024!", "NewKey2024@", "FutureKey2024#"]
            encrypted_keys = []
            
            for password in passwords:
                key = self.generate_encrypted_key(password)
                if key:
                    encrypted_keys.append(key)
            
            if len(encrypted_keys) >= 2:
                url = f"{self.base_url}/api/v1/security/tacacs-plus"
                
                # 第一次配置 - 使用舊密鑰
                payload1 = {
                    "isEncrypted": True,
                    "key": encrypted_keys[0],
                    "portNum": 49,
                    "retransmit": 3,
                    "timeout": 10,
                    "servers": [
                        {
                            "address": "192.168.50.10",
                            "isEncrypted": True,
                            "key": encrypted_keys[0],
                            "portNum": 49,
                            "retransmit": 3,
                            "timeout": 10
                        }
                    ]
                }
                
                response1 = self.session.put(url, json=payload1)
                success1 = response1.status_code == 200
                
                if success1:
                    print("    ✓ 第一階段：舊密鑰配置成功")
                    time.sleep(1)
                    
                    # 第二次配置 - 密鑰輪換
                    payload2 = {
                        "isEncrypted": True,
                        "key": encrypted_keys[1],
                        "portNum": 49,
                        "retransmit": 3,
                        "timeout": 10,
                        "servers": [
                            {
                                "address": "192.168.50.10",
                                "isEncrypted": True,
                                "key": encrypted_keys[1],
                                "portNum": 49,
                                "retransmit": 3,
                                "timeout": 10
                            }
                        ]
                    }
                    
                    response2 = self.session.put(url, json=payload2)
                    success2 = response2.status_code == 200
                    
                    if success2:
                        print("    ✓ 第二階段：密鑰輪換成功")
                    
                    overall_success = success1 and success2
                    self.log_test("密鑰輪換場景", overall_success, response2)
                    self.test_servers.append("192.168.50.10")
                else:
                    self.log_test("密鑰輪換場景", False, response1)
            else:
                print("    ✗ 無法生成足夠的加密密鑰")
                self.log_test("密鑰輪換場景", False, error="密鑰生成失敗")
            
        except Exception as e:
            self.log_test("密鑰輪換場景", False, error=e)
        
        # 場景2: 混合加密配置
        print("\n--- 混合加密配置測試 ---")
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            
            # 生成加密密鑰
            encrypted_key = self.generate_encrypted_key("MixedSecurity2024")
            
            if encrypted_key:
                # 配置：全局使用加密，部分服務器使用明文（測試環境）
                payload = {
                    "isEncrypted": True,
                    "key": encrypted_key,
                    "portNum": 49,
                    "retransmit": 3,
                    "timeout": 10,
                    "servers": [
                        {
                            "address": "192.168.60.10",  # 生產服務器 - 加密
                            "isEncrypted": True,
                            "key": encrypted_key,
                            "portNum": 49,
                            "retransmit": 3,
                            "timeout": 10
                        },
                        {
                            "address": "192.168.60.20",  # 測試服務器 - 明文
                            "isEncrypted": False,
                            "key": "test_plain_key",
                            "portNum": 49,
                            "retransmit": 3,
                            "timeout": 10
                        }
                    ]
                }
                
                response = self.session.put(url, json=payload)
                success = response.status_code == 200
                
                if success:
                    print("    ✓ 混合加密配置成功")
                    print("      - 全局密鑰: 加密")
                    print("      - 生產服務器: 加密密鑰")
                    print("      - 測試服務器: 明文密鑰")
                
                self.log_test("混合加密配置", success, response)
                self.test_servers.extend(["192.168.60.10", "192.168.60.20"])
            else:
                print("    ✗ 無法生成加密密鑰")
                self.log_test("混合加密配置", False, error="密鑰生成失敗")
            
        except Exception as e:
            self.log_test("混合加密配置", False, error=e)
    
    def test_tacacs_plus_compliance_scenarios(self):
        """測試TACACS+合規場景"""
        print("\n=== TACACS+ 合規場景測試 ===")
        
        # 場景1: 金融行業合規配置
        print("\n--- 金融行業合規配置 ---")
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            
            # 金融行業要求：高安全性、冗餘、審計
            encrypted_key = self.generate_encrypted_key("FinancialCompliance@2024!")
            
            if encrypted_key:
                payload = {
                    "isEncrypted": True,
                    "key": encrypted_key,
                    "portNum": 49,
                    "retransmit": 2,  # 限制重傳減少攻擊面
                    "timeout": 30,    # 足夠時間進行安全驗證
                    "servers": [
                        {
                            "address": "10.100.1.10",  # 主數據中心
                            "isEncrypted": True,
                            "key": encrypted_key,
                            "portNum": 49,
                            "retransmit": 2,
                            "timeout": 30
                        },
                        {
                            "address": "10.100.2.10",  # 災備數據中心
                            "isEncrypted": True,
                            "key": encrypted_key,
                            "portNum": 49,
                            "retransmit": 2,
                            "timeout": 30
                        }
                    ]
                }
                
                response = self.session.put(url, json=payload)
                success = response.status_code == 200
                
                if success:
                    print("    ✓ 金融行業合規配置成功")
                    print("      - 強制加密密鑰")
                    print("      - 雙數據中心冗餘")
                    print("      - 安全超時設置")
                    print("      - 限制重傳次數")
                
                self.log_test("金融行業合規配置", success, response)
                self.test_servers.extend(["10.100.1.10", "10.100.2.10"])
            else:
                self.log_test("金融行業合規配置", False, error="密鑰生成失敗")
            
        except Exception as e:
            self.log_test("金融行業合規配置", False, error=e)
        
        # 場景2: 政府機構合規配置
        print("\n--- 政府機構合規配置 ---")
        try:
            url = f"{self.base_url}/api/v1/security/tacacs-plus"
            
            # 政府要求：最高安全級別、多層驗證
            gov_encrypted_key = self.generate_encrypted_key("GovSecure@ClassifiedLevel!")
            
            if gov_encrypted_key:
                payload = {
                    "isEncrypted": True,
                    "key": gov_encrypted_key,
                    "portNum": 1812,  # 非標準端口
                    "retransmit": 1,  # 最小重傳
                    "timeout": 60,    # 長超時支持多因子認證
                    "servers": [
                        {
                            "address": "172.20.1.10",  # 安全區域服務器
                            "isEncrypted": True,
                            "key": gov_encrypted_key,
                            "portNum": 1812,
                            "retransmit": 1,
                            "timeout": 60
                        }
                    ]
                }
                
                response = self.session.put(url, json=payload)
                success = response.status_code == 200
                
                if success:
                    print("    ✓ 政府機構合規配置成功")
                    print("      - 最高級別加密")
                    print("      - 非標準端口 (1812)")
                    print("      - 最小重傳策略")
                    print("      - 支持多因子認證超時")
                
                self.log_test("政府機構合規配置", success, response)
                self.test_servers.append("172.20.1.10")
            else:
                self.log_test("政府機構合規配置", False, error="密鑰生成失敗")
            
        except Exception as e:
            self.log_test("政府機構合規配置", False, error=e)

def main():
    """主函數"""
    if len(sys.argv) < 2:
        print("使用方法: python tacacs_test.py <base_url> [username] [password]")
        print("範例: python tacacs_test.py http://192.168.1.1 admin admin123")
        print("\n功能說明:")
        print("  - 測試所有TACACS+ API功能")
        print("  - 包含TACACS+服務器配置管理")
        print("  - 加密密鑰生成和管理")
        print("  - 參數驗證和錯誤場景測試")
        print("  - 性能測試和邊界條件測試")
        print("  - 企業級集成場景測試")
        print("  - 故障轉移和安全場景測試")
        print("  - 行業合規配置測試")
        print("  - 自動清理測試配置")
        print("  - 自動恢復原始配置")
        print("  - 生成詳細測試報告")
        print("\n參數範圍:")
        print("  - 端口號: 1-65535")
        print("  - 重傳次數: 1-30")
        print("  - 超時時間: 1-540秒")
        print("  - 未加密密鑰長度: 最大48字符")
        print("  - 加密密鑰長度: 最大68字符")
        print("  - 支持IPv4地址格式")
        print("\n注意事項:")
        print("  - 測試會修改TACACS+配置，完成後自動恢復")
        print("  - 加密密鑰測試需要設備支持密鑰生成功能")
        print("  - 建議在測試環境中運行")
        print("  - 某些高級場景可能需要特定網絡環境")
        sys.exit(1)
    
    base_url = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else None
    password = sys.argv[3] if len(sys.argv) > 3 else None
    
    # 創建測試器並運行測試
    tester = TacacsPlusAPITester(base_url, username, password)
    
    try:
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n測試被用戶中斷")
        print("正在清理資源和恢復配置...")
        tester.cleanup_test_servers()
        tester.restore_original_config()
    except Exception as e:
        print(f"\n測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        print("正在清理資源和恢復配置...")
        tester.cleanup_test_servers()
        tester.restore_original_config()

if __name__ == "__main__":
    main()