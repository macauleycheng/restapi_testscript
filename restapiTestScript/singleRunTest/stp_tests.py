#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STP REST API 測試腳本
基於 STP_API_Reference_v0.14.docx 文件生成
包含 STP 配置管理功能測試
"""

import hashlib

import requests
import json
import sys
import time
import random
from datetime import datetime

class STPAPITester:
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
        self.created_groups = []  # 記錄創建的組，用於清理
        
        # STP模式常量
        self.STP_MODES = {
            'STP': 'STP',
            'RSTP': 'RSTP', 
            'MSTP': 'MSTP'
        }
        
        # 端口狀態常量
        self.PORT_STATES = {
            'DISABLED': 'disabled',
            'BLOCKING': 'blocking',
            'LISTENING': 'listening',
            'LEARNING': 'learning',
            'FORWARDING': 'forwarding'
        }
    
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
        if response:
            print(f"    狀態碼: {response.status_code}")
    
    # ==================== MST Configuration Tests ====================
    
    def test_get_mst_config(self):
        """測試獲取MST配置"""
        try:
            url = f"{self.base_url}/api/v1/stp/mst"
            response = self.session.get(url)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    
                    print(f"    MST區域名稱: {result_data.get('name', 'N/A')}")
                    print(f"    修訂版本: {result_data.get('revision', 'N/A')}")
                    print(f"    最大跳數: {result_data.get('maxHops', 'N/A')}")
                    
                    instances = result_data.get('instances', [])
                    print(f"    實例數量: {len(instances)}")
                    
                    for instance in instances:
                        print(f"      實例ID: {instance.get('id')}")
                    
                    # 保存原始配置
                    self.original_config = result_data
                    
            self.log_test("獲取MST配置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取MST配置", False, error=e)
            return None
    
    def test_set_mst_basic_config(self):
        """測試設置基本MST配置"""
        try:
            url = f"{self.base_url}/api/v1/stp/mst"
            
            payload = {
                "name": "TestRegion",
                "revision": 1,
                "maxHops": 20
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置基本MST配置:")
                print(f"      區域名稱: {payload['name']}")
                print(f"      修訂版本: {payload['revision']}")
                print(f"      最大跳數: {payload['maxHops']}")
            
            self.log_test("設置基本MST配置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置基本MST配置", False, error=e)
            return None
    
    def test_set_mst_with_instances(self):
        """測試設置包含實例的MST配置"""
        try:
            url = f"{self.base_url}/api/v1/stp/mst"
            
            payload = {
                "name": "TestRegionWithInstances",
                "revision": 2,
                "maxHops": 25,
                "instances": [
                    {"id": 1},
                    {"id": 2},
                    {"id": 10}
                ]
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置MST配置（包含實例）:")
                print(f"      區域名稱: {payload['name']}")
                print(f"      修訂版本: {payload['revision']}")
                print(f"      最大跳數: {payload['maxHops']}")
                print(f"      實例數量: {len(payload['instances'])}")
                for instance in payload['instances']:
                    print(f"        實例ID: {instance['id']}")
            
            self.log_test("設置包含實例的MST配置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置包含實例的MST配置", False, error=e)
            return None
    
    def test_set_mst_boundary_values(self):
        """測試MST邊界值配置"""
        try:
            url = f"{self.base_url}/api/v1/stp/mst"
            
            # 測試最大值配置
            payload = {
                "name": "A" * 32,  # 最大長度32
                "revision": 65535,  # 最大值65535
                "maxHops": 40,      # 最大值40
                "instances": [
                    {"id": 1},
                    {"id": 4094}  # 最大實例ID
                ]
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置MST邊界值配置:")
                print(f"      區域名稱長度: {len(payload['name'])}")
                print(f"      修訂版本: {payload['revision']}")
                print(f"      最大跳數: {payload['maxHops']}")
                print(f"      實例ID範圍: {[i['id'] for i in payload['instances']]}")
            
            self.log_test("設置MST邊界值配置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置MST邊界值配置", False, error=e)
            return None
    
    def test_set_mst_minimum_values(self):
        """測試MST最小值配置"""
        try:
            url = f"{self.base_url}/api/v1/stp/mst"
            
            # 測試最小值配置
            payload = {
                "name": "",         # 最小長度0
                "revision": 0,      # 最小值0
                "maxHops": 1,       # 最小值1
                "instances": [
                    {"id": 1}       # 最小實例ID
                ]
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功設置MST最小值配置:")
                print(f"      區域名稱: '{payload['name']}'")
                print(f"      修訂版本: {payload['revision']}")
                print(f"      最大跳數: {payload['maxHops']}")
            
            self.log_test("設置MST最小值配置", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("設置MST最小值配置", False, error=e)
            return None
    
    # ==================== TC Prop Groups Tests ====================
    
    def test_get_tc_prop_groups(self):
        """測試獲取TC Prop組列表"""
        try:
            url = f"{self.base_url}/api/v1/stp/tc-prop/groups"
            response = self.session.get(url)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if 'result' in data:
                    groups = data['result']
                    print(f"    TC Prop組數量: {len(groups)}")
                    
                    for group in groups:
                        print(f"      組ID: {group.get('id')}")
                        print(f"      組名: {group.get('name', 'N/A')}")
            
            self.log_test("獲取TC Prop組列表", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取TC Prop組列表", False, error=e)
            return None
    
    def test_create_tc_prop_group(self):
        """測試創建TC Prop組"""
        try:
            url = f"{self.base_url}/api/v1/stp/tc-prop/groups"
            
            # 生成唯一的組名
            group_name = f"TestGroup_{int(time.time())}"
            
            payload = {
                "name": group_name,
                "description": "Test TC Prop Group"
            }
            
            response = self.session.post(url, json=payload)
            
            success = response.status_code == 201 or response.status_code == 200
            
            if success:
                data = response.json()
                if 'result' in data and 'id' in data['result']:
                    group_id = data['result']['id']
                    self.created_groups.append(group_id)
                    print(f"    成功創建TC Prop組:")
                    print(f"      組ID: {group_id}")
                    print(f"      組名: {group_name}")
                else:
                    print(f"    創建成功但無法獲取組ID")
            
            self.log_test("創建TC Prop組", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("創建TC Prop組", False, error=e)
            return None
    
    def test_get_tc_prop_group_by_id(self):
        """測試根據ID獲取TC Prop組"""
        if not self.created_groups:
            print("    跳過測試：沒有可用的組ID")
            return None
            
        try:
            group_id = self.created_groups[0]
            url = f"{self.base_url}/api/v1/stp/tc-prop/groups/{group_id}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                if 'result' in data:
                    group_data = data['result']
                    print(f"    獲取組詳情:")
                    print(f"      組ID: {group_data.get('id')}")
                    print(f"      組名: {group_data.get('name')}")
                    print(f"      描述: {group_data.get('description', 'N/A')}")
            
            self.log_test(f"根據ID獲取TC Prop組 (ID: {group_id})", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"根據ID獲取TC Prop組 (ID: {group_id})", False, error=e)
            return None
    
    def test_update_tc_prop_group(self):
        """測試更新TC Prop組"""
        if not self.created_groups:
            print("    跳過測試：沒有可用的組ID")
            return None
            
        try:
            group_id = self.created_groups[0]
            url = f"{self.base_url}/api/v1/stp/tc-prop/groups/{group_id}"
            
            payload = {
                "name": f"UpdatedGroup_{group_id}",
                "description": "Updated Test TC Prop Group"
            }
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            
            if success:
                print(f"    成功更新TC Prop組:")
                print(f"      組ID: {group_id}")
                print(f"      新組名: {payload['name']}")
                print(f"      新描述: {payload['description']}")
            
            self.log_test(f"更新TC Prop組 (ID: {group_id})", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"更新TC Prop組 (ID: {group_id})", False, error=e)
            return None
    
    def test_delete_tc_prop_group(self):
        """測試刪除TC Prop組"""
        if not self.created_groups:
            print("    跳過測試：沒有可用的組ID")
            return None
            
        try:
            group_id = self.created_groups.pop()  # 取出最後一個組ID
            url = f"{self.base_url}/api/v1/stp/tc-prop/groups/{group_id}"
            
            response = self.session.delete(url)
            
            success = response.status_code == 200
            
            if success:
                print(f"    成功刪除TC Prop組:")
                print(f"      組ID: {group_id}")
            
            self.log_test(f"刪除TC Prop組 (ID: {group_id})", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"刪除TC Prop組 (ID: {group_id})", False, error=e)
            return None
    
    # ==================== Complete Workflow Tests ====================
    
    def test_complete_stp_workflow(self):
        """測試完整的STP工作流程"""
        print("\n=== 完整STP工作流程測試 ===")
        
        workflow_results = []
        
        try:
            # 步驟1: 獲取當前MST配置
            print("\n步驟1: 獲取當前MST配置")
            result = self.test_get_mst_config()
            workflow_results.append(("獲取MST配置", result is not None))
            
            # 步驟2: 設置基本MST配置
            print("\n步驟2: 設置基本MST配置")
            result = self.test_set_mst_basic_config()
            workflow_results.append(("設置基本MST配置", result is not None))
            time.sleep(1)
            
            # 步驟3: 驗證MST配置
            print("\n步驟3: 驗證MST配置")
            result = self.test_get_mst_config()
            workflow_results.append(("驗證MST配置", result is not None))
            
            # 步驟4: 設置包含實例的MST配置
            print("\n步驟4: 設置包含實例的MST配置")
            result = self.test_set_mst_with_instances()
            workflow_results.append(("設置MST實例", result is not None))
            time.sleep(1)
            
            # 步驟5: 獲取TC Prop組列表
            print("\n步驟5: 獲取TC Prop組列表")
            result = self.test_get_tc_prop_groups()
            workflow_results.append(("獲取TC Prop組", result is not None))
            
            # 步驟6: 創建TC Prop組
            print("\n步驟6: 創建TC Prop組")
            result = self.test_create_tc_prop_group()
            workflow_results.append(("創建TC Prop組", result is not None))
            
            # 步驟7: 根據ID獲取TC Prop組
            print("\n步驟7: 根據ID獲取TC Prop組")
            result = self.test_get_tc_prop_group_by_id()
            workflow_results.append(("獲取指定TC Prop組", result is not None))
            
            # 步驟8: 更新TC Prop組
            print("\n步驟8: 更新TC Prop組")
            result = self.test_update_tc_prop_group()
            workflow_results.append(("更新TC Prop組", result is not None))
            
            # 步驟9: 測試邊界值配置
            print("\n步驟9: 測試MST邊界值配置")
            result = self.test_set_mst_boundary_values()
            workflow_results.append(("MST邊界值測試", result is not None))
            
            # 步驟10: 測試最小值配置
            print("\n步驟10: 測試MST最小值配置")
            result = self.test_set_mst_minimum_values()
            workflow_results.append(("MST最小值測試", result is not None))
            
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
            self.log_test("完整STP工作流程", overall_success, 
                         details={'successful_steps': successful_steps, 'total_steps': total_steps})
            
            print(f"\n{'✓ 完整工作流程測試完成' if overall_success else '✗ 工作流程測試部分失敗'}")
            
        except Exception as e:
            print(f"\n✗ 工作流程測試失敗: {e}")
            self.log_test("完整STP工作流程", False, error=e)
    
    # ==================== Parameter Validation Tests ====================
    
    def test_parameter_validation(self):
        """測試參數驗證"""
        print("\n=== 參數驗證測試 ===")
        
        # 測試MST參數範圍
        print("\n--- MST參數範圍驗證測試 ---")
        
        # 測試區域名稱長度
        name_test_cases = [
            ("", "空名稱", True),
            ("A", "單字符名稱", True),
            ("A" * 16, "中等長度名稱", True),
            ("A" * 32, "最大長度名稱", True)
        ]
        
        for name, description, should_succeed in name_test_cases:
            try:
                url = f"{self.base_url}/api/v1/stp/mst"
                payload = {
                    "name": name,
                    "revision": 1,
                    "maxHops": 20
                }
                response = self.session.put(url, json=payload)
                success = (response.status_code == 200) == should_succeed
                
                self.log_test(f"MST名稱長度驗證 - {description} (長度:{len(name)})", success, response)
                time.sleep(0.3)
            except Exception as e:
                self.log_test(f"MST名稱長度驗證 - {description}", False, error=e)
        
        # 測試修訂版本範圍
        revision_test_cases = [
            (0, "最小修訂版本", True),
            (1, "標準修訂版本", True),
            (32767, "中等修訂版本", True),
            (65535, "最大修訂版本", True)
        ]
        
        for revision, description, should_succeed in revision_test_cases:
            try:
                url = f"{self.base_url}/api/v1/stp/mst"
                payload = {
                    "name": "TestRegion",
                    "revision": revision,
                    "maxHops": 20
                }
                response = self.session.put(url, json=payload)
                success = (response.status_code == 200) == should_succeed
                
                self.log_test(f"MST修訂版本驗證 - {description} ({revision})", success, response)
                time.sleep(0.3)
            except Exception as e:
                self.log_test(f"MST修訂版本驗證 - {description} ({revision})", False, error=e)
        
        # 測試最大跳數範圍
        max_hops_test_cases = [
            (1, "最小跳數", True),
            (10, "標準跳數", True),
            (20, "中等跳數", True),
            (40, "最大跳數", True)
        ]
        
        for max_hops, description, should_succeed in max_hops_test_cases:
            try:
                url = f"{self.base_url}/api/v1/stp/mst"
                payload = {
                    "name": "TestRegion",
                    "revision": 1,
                    "maxHops": max_hops
                }
                response = self.session.put(url, json=payload)
                success = (response.status_code == 200) == should_succeed
                
                self.log_test(f"MST最大跳數驗證 - {description} ({max_hops})", success, response)
                time.sleep(0.3)
            except Exception as e:
                self.log_test(f"MST最大跳數驗證 - {description} ({max_hops})", False, error=e)
        
        # 測試實例ID範圍
        print("\n--- 實例ID範圍驗證測試 ---")
        instance_id_test_cases = [
            (1, "最小實例ID", True),
            (100, "標準實例ID", True),
            (2047, "中等實例ID", True),
            (4094, "最大實例ID", True)
        ]
        
        for instance_id, description, should_succeed in instance_id_test_cases:
            try:
                url = f"{self.base_url}/api/v1/stp/mst"
                payload = {
                    "name": "TestRegion",
                    "revision": 1,
                    "maxHops": 20,
                    "instances": [{"id": instance_id}]
                }
                response = self.session.put(url, json=payload)
                success = (response.status_code == 200) == should_succeed
                
                self.log_test(f"實例ID驗證 - {description} ({instance_id})", success, response)
                time.sleep(0.3)
            except Exception as e:
                self.log_test(f"實例ID驗證 - {description} ({instance_id})", False, error=e)
    
    # ==================== Error Scenarios Tests ====================
    
    def test_error_scenarios(self):
        """測試錯誤場景"""
        print("\n=== 錯誤場景測試 ===")
        
        # 測試1: 無效JSON格式
        print("\n--- JSON格式錯誤測試 ---")
        try:
            url = f"{self.base_url}/api/v1/stp/mst"
            response = self.session.put(url, data="invalid json format")
            success = response.status_code == 400
            self.log_test("無效JSON格式測試", success, response)
        except Exception as e:
            self.log_test("無效JSON格式測試", False, error=e)
        
        # 測試2: 超出範圍的參數值
        print("\n--- 參數範圍錯誤測試 ---")
        
        # 超長名稱
        try:
            url = f"{self.base_url}/api/v1/stp/mst"
            payload = {
                "name": "A" * 100,  # 超出32字符限制
                "revision": 1,
                "maxHops": 20
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            self.log_test("超長區域名稱測試", success, response)
        except Exception as e:
            self.log_test("超長區域名稱測試", False, error=e)
        
        # 超出範圍的修訂版本
        try:
            url = f"{self.base_url}/api/v1/stp/mst"
            payload = {
                "name": "TestRegion",
                "revision": 70000,  # 超出65535
                "maxHops": 20
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            self.log_test("超出範圍修訂版本測試", success, response)
        except Exception as e:
            self.log_test("超出範圍修訂版本測試", False, error=e)
        
        # 超出範圍的最大跳數
        try:
            url = f"{self.base_url}/api/v1/stp/mst"
            payload = {
                "name": "TestRegion",
                "revision": 1,
                "maxHops": 50  # 超出40
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            self.log_test("超出範圍最大跳數測試", success, response)
        except Exception as e:
            self.log_test("超出範圍最大跳數測試", False, error=e)
        
        # 無效的實例ID
        try:
            url = f"{self.base_url}/api/v1/stp/mst"
            payload = {
                "name": "TestRegion",
                "revision": 1,
                "maxHops": 20,
                "instances": [{"id": 0}]  # 0是CISTID，不能配置
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            self.log_test("無效實例ID測試 (ID=0)", success, response)
        except Exception as e:
            self.log_test("無效實例ID測試 (ID=0)", False, error=e)
        
        # 超出範圍的實例ID
        try:
            url = f"{self.base_url}/api/v1/stp/mst"
            payload = {
                "name": "TestRegion",
                "revision": 1,
                "maxHops": 20,
                "instances": [{"id": 5000}]  # 超出4094
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            self.log_test("超出範圍實例ID測試 (ID=5000)", success, response)
        except Exception as e:
            self.log_test("超出範圍實例ID測試 (ID=5000)", False, error=e)
        
        # 測試3: 錯誤的數據類型
        print("\n--- 數據類型錯誤測試 ---")
        
        wrong_type_cases = [
            ({"name": 123, "revision": 1, "maxHops": 20}, "name為數字"),
            ({"name": "Test", "revision": "1", "maxHops": 20}, "revision為字符串"),
            ({"name": "Test", "revision": 1, "maxHops": "20"}, "maxHops為字符串"),
            ({"name": "Test", "revision": 1, "maxHops": 20, "instances": "not_array"}, "instances為字符串"),
            ({"name": "Test", "revision": 1, "maxHops": 20, "instances": [{"id": "1"}]}, "實例ID為字符串")
        ]
        
        for payload, description in wrong_type_cases:
            try:
                url = f"{self.base_url}/api/v1/stp/mst"
                response = self.session.put(url, json=payload)
                success = response.status_code == 400
                self.log_test(f"錯誤數據類型測試 - {description}", success, response)
            except Exception as e:
                self.log_test(f"錯誤數據類型測試 - {description}", False, error=e)
        
        # 測試4: TC Prop組相關錯誤
        print("\n--- TC Prop組錯誤測試 ---")
        
        # 獲取不存在的組
        try:
            url = f"{self.base_url}/api/v1/stp/tc-prop/groups/99999"
            response = self.session.get(url)
            success = response.status_code == 404
            self.log_test("獲取不存在的TC Prop組測試", success, response)
        except Exception as e:
            self.log_test("獲取不存在的TC Prop組測試", False, error=e)
        
        # 更新不存在的組
        try:
            url = f"{self.base_url}/api/v1/stp/tc-prop/groups/99999"
            payload = {"name": "NonExistentGroup"}
            response = self.session.put(url, json=payload)
            success = response.status_code == 404
            self.log_test("更新不存在的TC Prop組測試", success, response)
        except Exception as e:
            self.log_test("更新不存在的TC Prop組測試", False, error=e)
        
        # 刪除不存在的組
        try:
            url = f"{self.base_url}/api/v1/stp/tc-prop/groups/99999"
            response = self.session.delete(url)
            success = response.status_code == 404
            self.log_test("刪除不存在的TC Prop組測試", success, response)
        except Exception as e:
            self.log_test("刪除不存在的TC Prop組測試", False, error=e)
    
    # ==================== Boundary Conditions Tests ====================
    
    def test_boundary_conditions(self):
        """測試邊界條件"""
        print("\n=== 邊界條件測試 ===")
        
        # 測試最小值邊界
        print("\n--- 最小值邊界測試 ---")
        try:
            url = f"{self.base_url}/api/v1/stp/mst"
            payload = {
                "name": "",      # 最小長度
                "revision": 0,   # 最小值
                "maxHops": 1     # 最小值
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            self.log_test("最小值邊界測試", success, response)
        except Exception as e:
            self.log_test("最小值邊界測試", False, error=e)
        
        # 測試最大值邊界
        try:
            url = f"{self.base_url}/api/v1/stp/mst"
            payload = {
                "name": "A" * 32,  # 最大長度
                "revision": 65535, # 最大值
                "maxHops": 40      # 最大值
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            self.log_test("最大值邊界測試", success, response)
        except Exception as e:
            self.log_test("最大值邊界測試", False, error=e)
        
        # 測試邊界值附近
        print("\n--- 邊界值附近測試 ---")
        boundary_cases = [
            ({"revision": -1}, "修訂版本-1", False),
            ({"revision": 0}, "修訂版本0", True),
            ({"revision": 1}, "修訂版本1", True),
            ({"revision": 65534}, "修訂版本65534", True),
            ({"revision": 65535}, "修訂版本65535", True),
            ({"revision": 65536}, "修訂版本65536", False),
            ({"maxHops": 0}, "最大跳數0", False),
            ({"maxHops": 1}, "最大跳數1", True),
            ({"maxHops": 2}, "最大跳數2", True),
            ({"maxHops": 39}, "最大跳數39", True),
            ({"maxHops": 40}, "最大跳數40", True),
            ({"maxHops": 41}, "最大跳數41", False)
        ]
        
        for partial_payload, description, should_succeed in boundary_cases:
            try:
                url = f"{self.base_url}/api/v1/stp/mst"
                payload = {
                    "name": "BoundaryTest",
                    "revision": 1,
                    "maxHops": 20
                }
                payload.update(partial_payload)
                
                response = self.session.put(url, json=payload)
                success = (response.status_code == 200) == should_succeed
                
                self.log_test(f"邊界值測試 - {description}", success, response)
            except Exception as e:
                self.log_test(f"邊界值測試 - {description}", False, error=e)
        
        # 測試空實例列表
        try:
            url = f"{self.base_url}/api/v1/stp/mst"
            payload = {
                "name": "EmptyInstancesTest",
                "revision": 1,
                "maxHops": 20,
                "instances": []  # 空列表
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            self.log_test("空實例列表邊界測試", success, response)
        except Exception as e:
            self.log_test("空實例列表邊界測試", False, error=e)
        
        # 測試省略可選字段
        try:
            url = f"{self.base_url}/api/v1/stp/mst"
            payload = {
                "revision": 1
                # 省略 name, maxHops, instances
            }
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            self.log_test("省略可選字段邊界測試", success, response)
        except Exception as e:
            self.log_test("省略可選字段邊界測試", False, error=e)
    
    # ==================== Cleanup and Restore ====================
    
    def cleanup_created_resources(self):
        """清理創建的資源"""
        print("\n=== 清理創建的資源 ===")
        
        # 清理創建的TC Prop組
        for group_id in self.created_groups[:]:  # 使用切片複製列表
            try:
                url = f"{self.base_url}/api/v1/stp/tc-prop/groups/{group_id}"
                response = self.session.delete(url)
                
                if response.status_code == 200:
                    print(f"    ✓ 已刪除TC Prop組 ID: {group_id}")
                    self.created_groups.remove(group_id)
                else:
                    print(f"    ✗ 刪除TC Prop組失敗 ID: {group_id}")
                    
            except Exception as e:
                print(f"    ✗ 刪除TC Prop組時發生錯誤 ID: {group_id}, 錯誤: {e}")
        
        if not self.created_groups:
            print("    ✓ 所有創建的資源已清理完成")
        else:
            print(f"    ⚠️  仍有 {len(self.created_groups)} 個資源未能清理")
    
    def restore_original_config(self):
        """恢復原始配置"""
        if self.original_config:
            print("\n=== 恢復原始STP配置 ===")
            try:
                url = f"{self.base_url}/api/v1/stp/mst"
                response = self.session.put(url, json=self.original_config)
                
                success = response.status_code == 200
                if success:
                    print("    ✓ 原始MST配置已恢復")
                    print(f"      區域名稱: {self.original_config.get('name', 'N/A')}")
                    print(f"      修訂版本: {self.original_config.get('revision', 'N/A')}")
                    print(f"      最大跳數: {self.original_config.get('maxHops', 'N/A')}")
                    
                    instances = self.original_config.get('instances', [])
                    print(f"      實例數量: {len(instances)}")
                else:
                    print("    ✗ 恢復原始配置失敗")
                
                self.log_test("恢復原始MST配置", success, response)
                
            except Exception as e:
                print(f"    ✗ 恢復原始配置時發生錯誤: {e}")
                self.log_test("恢復原始MST配置", False, error=e)
        else:
            print("    沒有保存的原始配置，跳過恢復")
    
    # ==================== Main Test Runner ====================
    
    def run_all_tests(self):
        """運行所有測試"""
        print("=== STP REST API 測試開始 ===")
        print(f"測試目標: {self.base_url}")
        print(f"測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        try:
            # 1. 基本功能測試
            print("\n=== STP 基本功能測試 ===")
            self.test_get_mst_config()
            
            # 2. MST配置測試
            print("\n=== MST 配置測試 ===")
            self.test_set_mst_basic_config()
            time.sleep(1)
            self.test_get_mst_config()  # 驗證設置
            
            self.test_set_mst_with_instances()
            time.sleep(1)
            self.test_get_mst_config()  # 驗證設置
            
            # 3. TC Prop組測試
            print("\n=== TC Prop 組管理測試 ===")
            self.test_get_tc_prop_groups()
            self.test_create_tc_prop_group()
            self.test_get_tc_prop_group_by_id()
            self.test_update_tc_prop_group()
            
            # 4. 完整工作流程測試
            self.test_complete_stp_workflow()
            
            # 5. 參數驗證測試
            self.test_parameter_validation()
            
            # 6. 邊界條件測試
            self.test_boundary_conditions()
            
            # 7. 錯誤場景測試
            self.test_error_scenarios()
            
        finally:
            # 8. 清理和恢復
            self.cleanup_created_resources()
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
        mst_tests = [r for r in self.test_results if 'MST' in r['test_name']]
        tc_prop_tests = [r for r in self.test_results if 'TC Prop' in r['test_name']]
        validation_tests = [r for r in self.test_results if '驗證' in r['test_name']]
        error_tests = [r for r in self.test_results if ('錯誤' in r['test_name'] or '無效' in r['test_name'])]
        workflow_tests = [r for r in self.test_results if '工作流程' in r['test_name']]
        boundary_tests = [r for r in self.test_results if '邊界' in r['test_name']]
        
        print(f"\n功能測試統計:")
        print(f"  MST配置測試: {len(mst_tests)} 個測試")
        print(f"  TC Prop組測試: {len(tc_prop_tests)} 個測試")
        print(f"  工作流程測試: {len(workflow_tests)} 個測試")
        print(f"  參數驗證測試: {len(validation_tests)} 個測試")
        print(f"  邊界條件測試: {len(boundary_tests)} 個測試")
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
        with open('stp_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        print(f"\n詳細測試結果已保存到: stp_test_results.json")
        
        # 輸出配置統計
        if self.original_config:
            print(f"\n原始配置信息:")
            print(f"  區域名稱: {self.original_config.get('name', 'N/A')}")
            print(f"  修訂版本: {self.original_config.get('revision', 'N/A')}")
            print(f"  最大跳數: {self.original_config.get('maxHops', 'N/A')}")
            instances = self.original_config.get('instances', [])
            print(f"  實例數量: {len(instances)}")

def main():
    """主函數"""
    if len(sys.argv) < 2:
        print("使用方法: python stp_test.py <base_url> [username] [password]")
        print("範例: python stp_test.py http://192.168.1.1 admin admin123")
        print("\n功能說明:")
        print("  - 測試所有STP API功能")
        print("  - 包含MST配置管理")
        print("  - TC Prop組管理")
        print("  - 參數驗證和錯誤場景測試")
        print("  - 自動清理創建的資源")
        print("  - 自動恢復原始配置")
        print("  - 生成詳細測試報告")
        print("\n注意事項:")
        print("  - 區域名稱範圍: 0-32 字符")
        print("  - 修訂版本範圍: 0-65535")
        print("  - 最大跳數範圍: 1-40")
        print("  - 實例ID範圍: 1-4094")
        print("  - 測試會修改STP配置，完成後自動恢復")
        print("  - 建議在測試環境中運行")
        sys.exit(1)
    
    base_url = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else None
    password = sys.argv[3] if len(sys.argv) > 3 else None
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    
    # 創建測試器並運行測試
    tester = STPAPITester(base_url, username, password)
    
    try:
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n測試被用戶中斷")
        print("正在清理資源和恢復配置...")
        tester.cleanup_created_resources()
        tester.restore_original_config()
    except Exception as e:
        print(f"\n測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        print("正在清理資源和恢復配置...")
        tester.cleanup_created_resources()
        tester.restore_original_config()

if __name__ == "__main__":
    main()