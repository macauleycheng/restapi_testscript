#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RADIUS REST API 測試腳本
基於 Radius_API_Reference_v0.14.docx 文件生成
包含 RADIUS 配置和加密密鑰生成功能測試
"""

import requests
import json
import sys
import time
import base64
import random
import string

class RADIUSAPITester:
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
        self.test_passwords = []  # 記錄測試用的密碼
    
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
    
    def generate_random_password(self, length=16):
        """生成隨機密碼"""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    def validate_base64(self, s):
        """驗證是否為有效的Base64字符串"""
        try:
            base64.b64decode(s)
            return True
        except:
            return False
    
    # ==================== 1.1 Get RADIUS Information ====================
    
    def test_get_radius_info(self):
        """測試 1.1: 獲取RADIUS信息"""
        try:
            url = f"{self.base_url}/api/v1/security/radius"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    
                    # 驗證必要字段
                    required_fields = ['authPortNum', 'acctPortNum', 'retransmit', 'timeout']
                    missing_fields = [field for field in required_fields if field not in result_data]
                    
                    if missing_fields:
                        print(f"    缺少字段: {missing_fields}")
                        success = False
                    else:
                        print(f"    全局認證端口: {result_data.get('authPortNum')}")
                        print(f"    全局計費端口: {result_data.get('acctPortNum')}")
                        print(f"    重傳次數: {result_data.get('retransmit')}")
                        print(f"    超時時間: {result_data.get('timeout')}")
                        
                        # 顯示加密密鑰（如果存在）
                        if 'key' in result_data:
                            key_value = result_data['key']
                            print(f"    全局加密密鑰: {key_value[:10]}... (已截斷)")
                        
                        # 顯示服務器信息
                        servers = result_data.get('servers', [])
                        print(f"    RADIUS服務器數量: {len(servers)}")
                        for i, server in enumerate(servers[:3]):  # 只顯示前3個
                            print(f"      服務器 {i+1}:")
                            print(f"        地址: {server.get('address')}")
                            print(f"        認證端口: {server.get('authPortNum')}")
                            print(f"        計費端口: {server.get('acctPortNum')}")
                            print(f"        重傳次數: {server.get('retransmit')}")
                            print(f"        超時時間: {server.get('timeout')}")
                            if 'key' in server:
                                print(f"        加密密鑰: {server['key'][:10]}... (已截斷)")
                    
                    # 保存原始配置用於後續恢復
                    if success:
                        self.original_config = result_data
                else:
                    success = False
                    
            self.log_test("獲取RADIUS信息", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取RADIUS信息", False, error=e)
            return None
    
    # ==================== 1.2 Set RADIUS Configuration ====================
    
    def test_set_radius_basic_config(self):
        """測試 1.2: 設置基本RADIUS配置"""
        try:
            url = f"{self.base_url}/api/v1/security/radius"
            
            # 基本配置測試
            payload = {
                "authPortNum": 1812,
                "acctPortNum": 1813,
                "isEncrypted": False,
                "key": "testkey123",
                "retransmit": 3,
                "timeout": 5
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置基本RADIUS配置:")
                print(f"      認證端口: {payload['authPortNum']}")
                print(f"      計費端口: {payload['acctPortNum']}")
                print(f"      重傳次數: {payload['retransmit']}")
                print(f"      超時時間: {payload['timeout']}")
                print(f"      加密密鑰: {payload['key']}")
            
            self.log_test("設置基本RADIUS配置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置基本RADIUS配置", False, error=e)
            return None
    
    def test_set_radius_with_servers(self):
        """測試 1.2: 設置包含服務器的RADIUS配置"""
        try:
            url = f"{self.base_url}/api/v1/security/radius"
            
            payload = {
                "authPortNum": 181,
                "acctPortNum": 181,
                "isEncrypted": False,
                "key": "green",
                "retransmit": 5,
                "timeout": 10,
                "servers": [
                    {
                        "address": "192.168.1.1",
                        "authPortNum": 1812,
                        "acctPortNum": 1813,
                        "retransmit": 2,
                        "timeout": 5
                    },
                    {
                        "address": "192.168.1.2",
                        "authPortNum": 1812,
                        "acctPortNum": 1813,
                        "retransmit": 2,
                        "timeout": 5
                    }
                ]
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置RADIUS配置（包含服務器）:")
                print(f"      全局端口: {payload['authPortNum']}/{payload['acctPortNum']}")
                print(f"      服務器數量: {len(payload['servers'])}")
                for i, server in enumerate(payload['servers']):
                    print(f"        服務器 {i+1}: {server['address']}:{server['authPortNum']}")
            
            self.log_test("設置包含服務器的RADIUS配置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置包含服務器的RADIUS配置", False, error=e)
            return None
    
    def test_set_radius_with_encrypted_key(self, encrypted_key):
        """測試 1.2: 使用加密密鑰設置RADIUS配置"""
        try:
            url = f"{self.base_url}/api/v1/security/radius"
            
            payload = {
                "authPortNum": 1812,
                "acctPortNum": 1813,
                "isEncrypted": True,  # 使用加密密鑰
                "key": encrypted_key,
                "retransmit": 2,
                "timeout": 5,
                "servers": [
                    {
                        "address": "10.0.0.1",
                        "authPortNum": 1812,
                        "acctPortNum": 1813,
                        "isEncrypted": True,
                        "key": encrypted_key,
                        "retransmit": 3,
                        "timeout": 8
                    }
                ]
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置RADIUS配置（使用加密密鑰）:")
                print(f"      加密密鑰: {encrypted_key[:20]}... (已截斷)")
                print(f"      服務器地址: {payload['servers'][0]['address']}")
            
            self.log_test("設置RADIUS配置（加密密鑰）", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置RADIUS配置（加密密鑰）", False, error=e)
            return None
    
    # ==================== 1.3 Generate Encrypted Key ====================
    
    def test_generate_encrypted_key(self, password):
        """測試 1.3: 生成加密密鑰"""
        try:
            url = f"{self.base_url}/api/v1/security/radius/encrypted-key"
            
            payload = {
                "password": password
            }
            
            response = self.session.post(url, json=payload)
            
            success = response.status_code == 200
            encrypted_key = None
            
            if success:
                data = response.json()
                if 'result' in data and 'key' in data['result']:
                    encrypted_key = data['result']['key']
                    
                    # 驗證加密密鑰格式
                    if self.validate_base64(encrypted_key):
                        print(f"    成功生成加密密鑰:")
                        print(f"      原始密碼: {password}")
                        print(f"      加密密鑰: {encrypted_key}")
                        print(f"      密鑰長度: {len(encrypted_key)} 字符")
                        
                        # 驗證密鑰長度限制（最大68字符）
                        if len(encrypted_key) <= 68:
                            print(f"      ✓ 密鑰長度符合規範 (≤68)")
                        else:
                            print(f"      ✗ 密鑰長度超出規範 (>68)")
                            success = False
                    else:
                        print(f"      ✗ 生成的密鑰不是有效的Base64格式")
                        success = False
                else:
                    success = False
            
            self.log_test(f"生成加密密鑰 (密碼: {password})", success, response)
            return encrypted_key if success else None
            
        except Exception as e:
            self.log_test(f"生成加密密鑰 (密碼: {password})", False, error=e)
            return None
    
    def test_generate_encrypted_key_various_lengths(self):
        """測試不同長度密碼的加密密鑰生成"""
        print("\n=== 測試不同長度密碼的加密密鑰生成 ===")
        
        test_cases = [
            ("1", "最短密碼"),
            ("12345", "短密碼"),
            ("1234567890123456", "中等長度密碼"),
            ("01234567890123456789012345678901", "長密碼"),
            ("0123456789012345678901234567890123456789012345678", "最大長度密碼(48字符)")
        ]
        
        generated_keys = []
        
        for password, description in test_cases:
            print(f"\n測試 {description} (長度: {len(password)})")
            encrypted_key = self.test_generate_encrypted_key(password)
            if encrypted_key:
                generated_keys.append((password, encrypted_key))
                self.test_passwords.append(password)
        
        return generated_keys
    
    # ==================== 綜合測試場景 ====================
    
    def test_complete_radius_workflow(self):
        """測試完整的RADIUS工作流程"""
        print("\n=== 完整RADIUS工作流程測試 ===")
        
        try:
            # 步驟1: 獲取當前配置
            print("\n步驟1: 獲取當前RADIUS配置")
            self.test_get_radius_info()
            
            # 步驟2: 生成加密密鑰
            print("\n步驟2: 生成加密密鑰")
            test_password = "WorkflowTest123"
            encrypted_key = self.test_generate_encrypted_key(test_password)
            
            if not encrypted_key:
                print("    ✗ 無法生成加密密鑰，跳過後續步驟")
                return
            
            # 步驟3: 使用明文密鑰設置配置
            print("\n步驟3: 使用明文密鑰設置RADIUS配置")
            self.test_set_radius_basic_config()
            
            # 步驟4: 驗證配置
            print("\n步驟4: 驗證配置設置")
            self.test_get_radius_info()
            
            # 步驟5: 使用加密密鑰設置配置
            print("\n步驟5: 使用加密密鑰設置RADIUS配置")
            self.test_set_radius_with_encrypted_key(encrypted_key)
            
            # 步驟6: 最終驗證
            print("\n步驟6: 最終配置驗證")
            self.test_get_radius_info()
            
            # 步驟7: 設置複雜配置（多服務器）
            print("\n步驟7: 設置複雜RADIUS配置")
            self.test_set_radius_with_servers()
            
            print("\n✓ 完整工作流程測試完成")
            
        except Exception as e:
            print(f"\n✗ 工作流程測試失敗: {e}")
    
    def test_parameter_validation(self):
        """測試參數驗證"""
        print("\n=== 參數驗證測試 ===")
        
        # 測試端口範圍
        port_test_cases = [
            (1, "最小端口號"),
            (1812, "標準認證端口"),
            (1813, "標準計費端口"),
            (65535, "最大端口號")
        ]
        
        for port, description in port_test_cases:
            try:
                url = f"{self.base_url}/api/v1/security/radius"
                payload = {
                    "authPortNum": port,
                    "acctPortNum": port,
                    "retransmit": 2,
                    "timeout": 5
                }
                response = self.session.put(url, json=payload)
                success = response.status_code == 200
                self.log_test(f"端口驗證測試 - {description} ({port})", success, response)
            except Exception as e:
                self.log_test(f"端口驗證測試 - {description} ({port})", False, error=e)
        
        # 測試重傳次數範圍
        retransmit_test_cases = [
            (1, "最小重傳次數"),
            (15, "中等重傳次數"),
            (30, "最大重傳次數")
        ]
        
        for retransmit, description in retransmit_test_cases:
            try:
                url = f"{self.base_url}/api/v1/security/radius"
                payload = {
                    "authPortNum": 1812,
                    "acctPortNum": 1813,
                    "retransmit": retransmit,
                    "timeout": 5
                }
                response = self.session.put(url, json=payload)
                success = response.status_code == 200
                self.log_test(f"重傳次數驗證測試 - {description} ({retransmit})", success, response)
            except Exception as e:
                self.log_test(f"重傳次數驗證測試 - {description} ({retransmit})", False, error=e)
        
        # 測試超時時間範圍
        timeout_test_cases = [
            (1, "最小超時時間"),
            (30, "中等超時時間"),
            (65535, "最大超時時間")
        ]
        
        for timeout, description in timeout_test_cases:
            try:
                url = f"{self.base_url}/api/v1/security/radius"
                payload = {
                    "authPortNum": 1812,
                    "acctPortNum": 1813,
                    "retransmit": 2,
                    "timeout": timeout
                }
                response = self.session.put(url, json=payload)
                success = response.status_code == 200
                self.log_test(f"超時時間驗證測試 - {description} ({timeout})", success, response)
            except Exception as e:
                self.log_test(f"超時時間驗證測試 - {description} ({timeout})", False, error=e)
    
    def test_error_scenarios(self):
        """測試錯誤場景"""
        print("\n=== 錯誤場景測試 ===")
        
        # 測試1: 無效JSON格式
        try:
            url = f"{self.base_url}/api/v1/security/radius"
            response = self.session.put(url, data="invalid json")
            success = response.status_code == 400
            self.log_test("無效JSON格式測試", success, response)
        except Exception as e:
            self.log_test("無效JSON格式測試", False, error=e)
        
        # 測試2: 超出範圍的端口號
        try:
            url = f"{self.base_url}/api/v1/security/radius"
            payload = {
                "authPortNum": 70000,  # 超出65535
                "acctPortNum": 1813
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            self.log_test("超出範圍端口號測試", success, response)
        except Exception as e:
            self.log_test("超出範圍端口號測試", False, error=e)
        
        # 測試3: 超出範圍的重傳次數
        try:
            url = f"{self.base_url}/api/v1/security/radius"
            payload = {
                "authPortNum": 1812,
                "acctPortNum": 1813,
                "retransmit": 50  # 超出30
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            self.log_test("超出範圍重傳次數測試", success, response)
        except Exception as e:
            self.log_test("超出範圍重傳次數測試", False, error=e)
        
        # 測試4: 過長的密碼
        try:
            url = f"{self.base_url}/api/v1/security/radius/encrypted-key"
            long_password = "a" * 50  # 超出48字符限制
            payload = {"password": long_password}
            response = self.session.post(url, json=payload)
            success = response.status_code == 400
            self.log_test("過長密碼測試", success, response)
        except Exception as e:
            self.log_test("過長密碼測試", False, error=e)
        
        # 測試5: 空密碼
        try:
            url = f"{self.base_url}/api/v1/security/radius/encrypted-key"
            payload = {"password": ""}
            response = self.session.post(url, json=payload)
            success = response.status_code == 400
            self.log_test("空密碼測試", success, response)
        except Exception as e:
            self.log_test("空密碼測試", False, error=e)
        
        # 測試6: 包含空格的密碼
        try:
            url = f"{self.base_url}/api/v1/security/radius/encrypted-key"
            payload = {"password": "test password with spaces"}
            response = self.session.post(url, json=payload)
            success = response.status_code == 400
            self.log_test("包含空格密碼測試", success, response)
        except Exception as e:
            self.log_test("包含空格密碼測試", False, error=e)
        
        # 測試7: 無效的服務器IP地址
        try:
            url = f"{self.base_url}/api/v1/security/radius"
            payload = {
                "servers": [
                    {
                        "address": "invalid.ip.address",
                        "authPortNum": 1812,
                        "acctPortNum": 1813
                    }
                ]
            }
            response = self.session.put(url, json=payload)
            success = response.status_code in [400, 500]
            self.log_test("無效服務器IP地址測試", success, response)
        except Exception as e:
            self.log_test("無效服務器IP地址測試", False, error=e)
    
    def test_boundary_conditions(self):
        """測試邊界條件"""
        print("\n=== 邊界條件測試 ===")
        
        # 測試最小值
        try:
            url = f"{self.base_url}/api/v1/security/radius"
            payload = {
                "authPortNum": 1,
                "acctPortNum": 1,
                "retransmit": 1,
                "timeout": 1
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            self.log_test("最小值邊界測試", success, response)
        except Exception as e:
            self.log_test("最小值邊界測試", False, error=e)
        
        # 測試最大值
        try:
            url = f"{self.base_url}/api/v1/security/radius"
            payload = {
                "authPortNum": 65535,
                "acctPortNum": 65535,
                "retransmit": 30,
                "timeout": 65535
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            self.log_test("最大值邊界測試", success, response)
        except Exception as e:
            self.log_test("最大值邊界測試", False, error=e)
        
        # 測試最大長度密碼
        max_length_password = "a" * 48
        encrypted_key = self.test_generate_encrypted_key(max_length_password)
        if encrypted_key:
            print(f"    最大長度密碼加密成功，密鑰長度: {len(encrypted_key)}")
    
    def restore_original_config(self):
        """恢復原始配置"""
        if self.original_config:
            print("\n=== 恢復原始RADIUS配置 ===")
            try:
                url = f"{self.base_url}/api/v1/security/radius"
                response = self.session.put(url, json=self.original_config)
                
                success = response.status_code == 200
                if success:
                    print("    ✓ 原始配置已恢復")
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
        print("=== RADIUS REST API 測試開始 ===")
        print(f"測試目標: {self.base_url}")
        print("=" * 60)
        
        try:
            # 1. 基本功能測試
            print("\n=== RADIUS 基本功能測試 ===")
            self.test_get_radius_info()
            
            # 2. 加密密鑰生成測試
            print("\n=== 加密密鑰生成測試 ===")
            self.test_generate_encrypted_key_various_lengths()
            
            # 3. RADIUS配置測試
            print("\n=== RADIUS 配置測試 ===")
            self.test_set_radius_basic_config()
            time.sleep(1)
            self.test_get_radius_info()  # 驗證設置
            
            # 4. 完整工作流程測試
            self.test_complete_radius_workflow()
            
            # 5. 參數驗證測試
            self.test_parameter_validation()
            
            # 6. 邊界條件測試
            self.test_boundary_conditions()
            
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
        encrypt_tests = [r for r in self.test_results if '加密' in r['test_name']]
        validation_tests = [r for r in self.test_results if ('驗證' in r['test_name'] or '邊界' in r['test_name'])]
        error_tests = [r for r in self.test_results if ('錯誤' in r['test_name'] or '無效' in r['test_name'])]
        
        print(f"\n功能測試統計:")
        print(f"  獲取配置測試: {len(get_tests)} 個測試")
        print(f"  設置配置測試: {len(set_tests)} 個測試")
        print(f"  加密密鑰測試: {len(encrypt_tests)} 個測試")
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
        with open('radius_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        print(f"\n詳細測試結果已保存到: radius_test_results.json")
        
        # 輸出測試統計
        if self.test_passwords:
            print(f"\n測試過程統計:")
            print(f"  測試的密碼數量: {len(self.test_passwords)}")
            print(f"  密碼長度範圍: {min(len(p) for p in self.test_passwords)} - {max(len(p) for p in self.test_passwords)} 字符")

def main():
    """主函數"""
    if len(sys.argv) < 2:
        print("使用方法: python radius_test.py <base_url> [username] [password]")
        print("範例: python radius_test.py http://192.168.1.1 admin admin123")
        print("\n功能說明:")
        print("  - 測試所有RADIUS API功能")
        print("  - 包含加密密鑰生成測試")
        print("  - 參數驗證和邊界條件測試")
        print("  - 自動恢復原始配置")
        print("  - 生成詳細測試報告")
        sys.exit(1)
    
    base_url = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else None
    password = sys.argv[3] if len(sys.argv) > 3 else None
    
    # 創建測試器並運行測試
    tester = RADIUSAPITester(base_url, username, password)
    
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