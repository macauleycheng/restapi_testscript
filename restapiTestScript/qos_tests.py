#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QoS REST API 測試腳本
基於 QoS_API_Reference_v0.12.docx 文件生成
包含 Class-Map, Policy-Map 和 Service-Policy 功能測試
"""

import requests
import json
import sys
import time
from urllib.parse import quote
import random

class QoSAPITester:
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
        self.created_class_maps = []  # 記錄創建的class-map
        self.created_policy_maps = []  # 記錄創建的policy-map
        self.applied_service_policies = []  # 記錄應用的service-policy
    
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
    
    # ==================== Class-Map 測試 ====================
    
    def test_get_all_class_maps(self):
        """測試 1.1: 獲取所有 class-map"""
        try:
            url = f"{self.base_url}/api/v1/qos/class-maps"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'result' in data and 'classMaps' in data['result']:
                    class_maps = data['result']['classMaps']
                    print(f"    找到 {len(class_maps)} 個 class-map")
                    for cm in class_maps[:3]:  # 顯示前3個
                        print(f"      - {cm.get('name')}: {cm.get('description', 'N/A')}")
                else:
                    print("    沒有找到 class-map")
                    
            self.log_test("獲取所有class-map", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取所有class-map", False, error=e)
            return None
    
    def test_create_class_map(self, name, description="Test class map", match_type="match-any", 
                             dscp_values=None, precedence_values=None):
        """測試 1.2: 創建 class-map"""
        try:
            url = f"{self.base_url}/api/v1/qos/class-maps"
            
            payload = {
                "name": name,
                "description": description,
                "matchType": match_type
            }
            
            # 添加DSCP匹配條件
            if dscp_values:
                payload["matchIpDscp"] = [{"dscp": dscp} for dscp in dscp_values]
            
            # 添加Precedence匹配條件
            if precedence_values:
                payload["matchIpPrecedence"] = [{"precedence": prec} for prec in precedence_values]
            
            response = self.session.post(url, json=payload)
            
            success = response.status_code == 200
            if success:
                self.created_class_maps.append(name)
                print(f"    成功創建class-map: {name}")
                if dscp_values:
                    print(f"      DSCP值: {dscp_values}")
                if precedence_values:
                    print(f"      Precedence值: {precedence_values}")
            
            self.log_test(f"創建class-map {name}", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"創建class-map {name}", False, error=e)
            return None
    
    def test_get_class_map(self, name):
        """測試 1.3: 獲取指定 class-map"""
        try:
            url = f"{self.base_url}/api/v1/qos/class-maps/{name}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    print(f"    Class-map名稱: {result_data.get('name')}")
                    print(f"    描述: {result_data.get('description', 'N/A')}")
                    print(f"    匹配類型: {result_data.get('matchType')}")
                    
                    # 顯示匹配條件
                    if result_data.get('matchIpDscp'):
                        dscp_list = [item['dscp'] for item in result_data['matchIpDscp']]
                        print(f"    DSCP匹配: {dscp_list}")
                    
                    if result_data.get('matchIpPrecedence'):
                        prec_list = [item['precedence'] for item in result_data['matchIpPrecedence']]
                        print(f"    Precedence匹配: {prec_list}")
                        
            self.log_test(f"獲取class-map {name}", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"獲取class-map {name}", False, error=e)
            return None
    
    def test_update_class_map(self, name, new_name=None, description=None, vlan_values=None):
        """測試 1.4: 更新 class-map"""
        try:
            url = f"{self.base_url}/api/v1/qos/class-maps/{name}"
            
            payload = {}
            
            if new_name:
                payload["name"] = new_name
            if description:
                payload["description"] = description
            if vlan_values:
                payload["matchVlan"] = [{"vlan": vlan} for vlan in vlan_values]
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功更新class-map: {name}")
                if new_name:
                    print(f"      新名稱: {new_name}")
                    # 更新記錄的名稱
                    if name in self.created_class_maps:
                        self.created_class_maps.remove(name)
                        self.created_class_maps.append(new_name)
                if vlan_values:
                    print(f"      VLAN匹配: {vlan_values}")
            
            self.log_test(f"更新class-map {name}", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"更新class-map {name}", False, error=e)
            return None
    
    def test_delete_class_map(self, name):
        """測試 1.5: 刪除 class-map"""
        try:
            url = f"{self.base_url}/api/v1/qos/class-maps/{name}"
            response = self.session.delete(url)
            
            success = response.status_code == 200
            if success:
                print(f"    成功刪除class-map: {name}")
                if name in self.created_class_maps:
                    self.created_class_maps.remove(name)
            
            self.log_test(f"刪除class-map {name}", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"刪除class-map {name}", False, error=e)
            return None
    
    # ==================== Policy-Map 測試 ====================
    
    def test_get_all_policy_maps(self):
        """測試 1.6: 獲取所有 policy-map"""
        try:
            url = f"{self.base_url}/api/v1/qos/policy-maps"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'result' in data and 'policyMaps' in data['result']:
                    policy_maps = data['result']['policyMaps']
                    print(f"    找到 {len(policy_maps)} 個 policy-map")
                    for pm in policy_maps[:3]:  # 顯示前3個
                        print(f"      - {pm.get('name')}: {len(pm.get('elements', []))} 個元素")
                else:
                    print("    沒有找到 policy-map")
                    
            self.log_test("獲取所有policy-map", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取所有policy-map", False, error=e)
            return None
    
    def test_create_policy_map(self, name, description="Test policy map", class_name=None):
        """測試 1.7: 創建 policy-map"""
        try:
            url = f"{self.base_url}/api/v1/qos/policy-maps"
            
            payload = {
                "name": name,
                "description": description
            }
            
            # 添加policy元素
            if class_name:
                payload["elements"] = [{
                    "className": class_name,
                    "setPhb": 3,
                    "policeType": "flow",
                    "meterRate": 100000,
                    "meterBurstSize": 4000,
                    "greenPktActionType": "transmit",
                    "redPktActionType": "drop"
                }]
            
            response = self.session.post(url, json=payload)
            
            success = response.status_code == 200
            if success:
                self.created_policy_maps.append(name)
                print(f"    成功創建policy-map: {name}")
                if class_name:
                    print(f"      關聯class-map: {class_name}")
            
            self.log_test(f"創建policy-map {name}", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"創建policy-map {name}", False, error=e)
            return None
    
    def test_get_policy_map(self, name):
        """測試 1.8: 獲取指定 policy-map"""
        try:
            url = f"{self.base_url}/api/v1/qos/policy-maps/{name}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    print(f"    Policy-map名稱: {result_data.get('name')}")
                    print(f"    描述: {result_data.get('description', 'N/A')}")
                    
                    elements = result_data.get('elements', [])
                    print(f"    包含 {len(elements)} 個元素:")
                    for elem in elements:
                        print(f"      - Class: {elem.get('className')}")
                        print(f"        PHB: {elem.get('setPhb')}")
                        print(f"        Police類型: {elem.get('policeType')}")
                        print(f"        速率: {elem.get('meterRate')} kbps")
                        
            self.log_test(f"獲取policy-map {name}", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"獲取policy-map {name}", False, error=e)
            return None
    
    def test_update_policy_map(self, name, new_name=None, description=None, class_name=None):
        """測試 1.9: 更新 policy-map"""
        try:
            url = f"{self.base_url}/api/v1/qos/policy-maps/{name}"
            
            payload = {}
            
            if new_name:
                payload["name"] = new_name
            if description:
                payload["description"] = description
            if class_name:
                payload["elements"] = [{
                    "className": class_name,
                    "setPhb": 2,
                    "policeType": "srtcm-color-blind",
                    "meterRate": 200000,
                    "meterBurstSize": 8000,
                    "greenPktActionType": "transmit",
                    "redPktActionType": "new dscp 20"
                }]
            
            response = self.session.put(url, json=payload)
            
            success = response.status_code == 200
            if success:
                print(f"    成功更新policy-map: {name}")
                if new_name:
                    print(f"      新名稱: {new_name}")
                    # 更新記錄的名稱
                    if name in self.created_policy_maps:
                        self.created_policy_maps.remove(name)
                        self.created_policy_maps.append(new_name)
            
            self.log_test(f"更新policy-map {name}", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"更新policy-map {name}", False, error=e)
            return None
    
    def test_delete_policy_map(self, name):
        """測試 1.10: 刪除 policy-map"""
        try:
            url = f"{self.base_url}/api/v1/qos/policy-maps/{name}"
            response = self.session.delete(url)
            
            success = response.status_code == 200
            if success:
                print(f"    成功刪除policy-map: {name}")
                if name in self.created_policy_maps:
                    self.created_policy_maps.remove(name)
            
            self.log_test(f"刪除policy-map {name}", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"刪除policy-map {name}", False, error=e)
            return None
    
    # ==================== Service-Policy 測試 ====================
    
    def test_get_all_service_policies(self):
        """測試 1.11: 獲取所有 service-policy"""
        try:
            url = f"{self.base_url}/api/v1/qos/policy-map/interfaces"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'result' in data and 'policyMapPorts' in data['result']:
                    policies = data['result']['policyMapPorts']
                    print(f"    找到 {len(policies)} 個 service-policy 綁定")
                    for policy in policies[:5]:  # 顯示前5個
                        print(f"      - 接口: {policy.get('ifId')}, "
                              f"方向: {policy.get('direction')}, "
                              f"Policy: {policy.get('policyMapName')}")
                else:
                    print("    沒有找到 service-policy 綁定")
                    
            self.log_test("獲取所有service-policy", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test("獲取所有service-policy", False, error=e)
            return None
    
    def test_bind_service_policy(self, interface_id, direction, policy_map_name):
        """測試 1.12: 綁定 service-policy 到接口"""
        try:
            url = f"{self.base_url}/api/v1/qos/policy-map/interfaces"
            
            payload = {
                "ifId": interface_id,
                "direction": direction,
                "policyMapName": policy_map_name
            }
            
            response = self.session.post(url, json=payload)
            
            success = response.status_code == 200
            if success:
                binding = f"{interface_id}:{direction}:{policy_map_name}"
                self.applied_service_policies.append(binding)
                print(f"    成功綁定service-policy:")
                print(f"      接口: {interface_id}")
                print(f"      方向: {direction}")
                print(f"      Policy-map: {policy_map_name}")
            
            self.log_test(f"綁定service-policy到{interface_id}", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"綁定service-policy到{interface_id}", False, error=e)
            return None
    
    def test_get_service_policy(self, interface_id, direction):
        """測試 1.13: 獲取指定接口的 service-policy"""
        try:
            encoded_if_id = quote(interface_id, safe='')
            url = f"{self.base_url}/api/v1/qos/policy-map/interfaces/{encoded_if_id}/directions/{direction}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if 'result' in data:
                    result_data = data['result']
                    print(f"    接口: {result_data.get('ifId')}")
                    print(f"    方向: {result_data.get('direction')}")
                    print(f"    Policy-map: {result_data.get('policyMapName')}")
                        
            self.log_test(f"獲取{interface_id}的service-policy", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"獲取{interface_id}的service-policy", False, error=e)
            return None
    
    def test_unbind_service_policy(self, interface_id, direction):
        """測試 1.14: 解綁 service-policy"""
        try:
            encoded_if_id = quote(interface_id, safe='')
            url = f"{self.base_url}/api/v1/qos/policy-map/interfaces/{encoded_if_id}/directions/{direction}"
            response = self.session.delete(url)
            
            success = response.status_code == 200
            if success:
                print(f"    成功解綁service-policy:")
                print(f"      接口: {interface_id}")
                print(f"      方向: {direction}")
                
                # 從記錄中移除
                to_remove = None
                for binding in self.applied_service_policies:
                    if binding.startswith(f"{interface_id}:{direction}:"):
                        to_remove = binding
                        break
                if to_remove:
                    self.applied_service_policies.remove(to_remove)
            
            self.log_test(f"解綁{interface_id}的service-policy", success, response)
            return response if success else None
            
        except Exception as e:
            self.log_test(f"解綁{interface_id}的service-policy", False, error=e)
            return None
    
    # ==================== 綜合測試場景 ====================
    
    def test_complete_qos_workflow(self):
        """測試完整的QoS工作流程"""
        print("\n=== 完整QoS工作流程測試 ===")
        
        # 生成唯一的測試名稱
        timestamp = int(time.time())
        class_map_name = f"test_class_{timestamp}"
        policy_map_name = f"test_policy_{timestamp}"
        
        try:
            # 步驟1: 創建class-map
            print("\n步驟1: 創建class-map")
            self.test_create_class_map(
                name=class_map_name,
                description="Complete workflow test class-map",
                dscp_values=[10, 20],
                precedence_values=[1, 2]
            )
            
            # 步驟2: 驗證class-map創建
            print("\n步驟2: 驗證class-map")
            self.test_get_class_map(class_map_name)
            
            # 步驟3: 創建policy-map並關聯class-map
            print("\n步驟3: 創建policy-map")
            self.test_create_policy_map(
                name=policy_map_name,
                description="Complete workflow test policy-map",
                class_name=class_map_name
            )
            
            # 步驟4: 驗證policy-map創建
            print("\n步驟4: 驗證policy-map")
            self.test_get_policy_map(policy_map_name)
            
            # 步驟5: 綁定service-policy到接口
            print("\n步驟5: 綁定service-policy")
            test_interface = "eth1/1"
            self.test_bind_service_policy(test_interface, "input", policy_map_name)
            
            # 步驟6: 驗證service-policy綁定
            print("\n步驟6: 驗證service-policy綁定")
            self.test_get_service_policy(test_interface, "input")
            
            # 步驟7: 解綁service-policy
            print("\n步驟7: 解綁service-policy")
            self.test_unbind_service_policy(test_interface, "input")
            
            # 步驟8: 清理資源
            print("\n步驟8: 清理測試資源")
            self.test_delete_policy_map(policy_map_name)
            self.test_delete_class_map(class_map_name)
            
            print("\n✓ 完整工作流程測試完成")
            
        except Exception as e:
            print(f"\n✗ 工作流程測試失敗: {e}")
    
    def test_error_scenarios(self):
        """測試錯誤場景"""
        print("\n=== 錯誤場景測試 ===")
        
        # 測試1: 創建重複的class-map
        try:
            duplicate_name = "duplicate_test_class"
            # 先創建一個
            self.test_create_class_map(duplicate_name, "First class-map")
            # 再創建同名的
            url = f"{self.base_url}/api/v1/qos/class-maps"
            payload = {"name": duplicate_name, "description": "Duplicate class-map"}
            response = self.session.post(url, json=payload)
            success = response.status_code == 500  # 應該返回錯誤
            self.log_test("創建重複class-map測試", success, response)
            # 清理
            self.test_delete_class_map(duplicate_name)
        except Exception as e:
            self.log_test("創建重複class-map測試", False, error=e)
        
        # 測試2: 獲取不存在的class-map
        try:
            url = f"{self.base_url}/api/v1/qos/class-maps/nonexistent_class"
            response = self.session.get(url)
            success = response.status_code in [400, 404, 500]
            self.log_test("獲取不存在class-map測試", success, response)
        except Exception as e:
            self.log_test("獲取不存在class-map測試", False, error=e)
        
        # 測試3: 無效的DSCP值
        try:
            url = f"{self.base_url}/api/v1/qos/class-maps"
            payload = {
                "name": "invalid_dscp_test",
                "matchIpDscp": [{"dscp": 100}]  # 超出0-63範圍
            }
            response = self.session.post(url, json=payload)
            success = response.status_code == 400
            self.log_test("無效DSCP值測試", success, response)
        except Exception as e:
            self.log_test("無效DSCP值測試", False, error=e)
        
        # 測試4: 無效的接口ID
        try:
            url = f"{self.base_url}/api/v1/qos/policy-map/interfaces"
            payload = {
                "ifId": "invalid_interface",
                "direction": "input",
                "policyMapName": "test_policy"
            }
            response = self.session.post(url, json=payload)
            success = response.status_code in [400, 500]
            self.log_test("無效接口ID測試", success, response)
        except Exception as e:
            self.log_test("無效接口ID測試", False, error=e)
        
        # 測試5: 無效JSON格式
        try:
            url = f"{self.base_url}/api/v1/qos/class-maps"
            response = self.session.post(url, data="invalid json")
            success = response.status_code == 400
            self.log_test("無效JSON格式測試", success, response)
        except Exception as e:
            self.log_test("無效JSON格式測試", False, error=e)
    
    def test_boundary_conditions(self):
        """測試邊界條件"""
        print("\n=== 邊界條件測試 ===")
        
        # 測試DSCP邊界值
        boundary_class = "boundary_test_class"
        
        # 最小DSCP值
        self.test_create_class_map(
            name=f"{boundary_class}_min",
            description="Minimum DSCP test",
            dscp_values=[0]
        )
        
        # 最大DSCP值
        self.test_create_class_map(
            name=f"{boundary_class}_max",
            description="Maximum DSCP test",
            dscp_values=[63]
        )
        
        # 最大Precedence值
        self.test_create_class_map(
            name=f"{boundary_class}_prec",
            description="Maximum Precedence test",
            precedence_values=[7]
        )
        
        # 清理邊界測試資源
        for suffix in ["_min", "_max", "_prec"]:
            self.test_delete_class_map(f"{boundary_class},{suffix}")
    
    def cleanup_test_resources(self):
        """清理測試資源"""
        print("\n=== 清理測試資源 ===")
        
        # 解綁所有測試的service-policy
        for binding in self.applied_service_policies[:]:
            parts = binding.split(':')
            if len(parts) >= 2:
                interface_id, direction = parts[0], parts[1]
                self.test_unbind_service_policy(interface_id, direction)
        
        # 刪除所有測試的policy-map
        for policy_name in self.created_policy_maps[:]:
            self.test_delete_policy_map(policy_name)
        
        # 刪除所有測試的class-map
        for class_name in self.created_class_maps[:]:
            self.test_delete_class_map(class_name)
        
        print("    測試資源清理完成")
    
    def run_all_tests(self, test_interfaces=None):
        """運行所有測試"""
        if test_interfaces is None:
            test_interfaces = ["eth1/1", "eth1/2"]
        
        print("=== QoS REST API 測試開始 ===")
        print(f"測試目標: {self.base_url}")
        print(f"測試接口: {test_interfaces}")
        print("=" * 60)
        
        try:
            # 1. 基本功能測試
            print("\n=== Class-Map 基本功能測試 ===")
            self.test_get_all_class_maps()
            
            # 創建測試用的class-map
            test_class_name = f"test_class_{int(time.time())}"
            self.test_create_class_map(
                name=test_class_name,
                description="API測試用class-map",
                dscp_values=[10, 20],
                precedence_values=[1, 2]
            )
            
            self.test_get_class_map(test_class_name)
            self.test_update_class_map(
                name=test_class_name,
                description="更新後的描述",
                vlan_values=[100, 200]
            )
            
            print("\n=== Policy-Map 基本功能測試 ===")
            self.test_get_all_policy_maps()
            
            # 創建測試用的policy-map
            test_policy_name = f"test_policy_{int(time.time())}"
            self.test_create_policy_map(
                name=test_policy_name,
                description="API測試用policy-map",
                class_name=test_class_name
            )
            
            self.test_get_policy_map(test_policy_name)
            self.test_update_policy_map(
                name=test_policy_name,
                description="更新後的policy-map描述"
            )
            
            print("\n=== Service-Policy 基本功能測試 ===")
            self.test_get_all_service_policies()
            
            # 測試service-policy綁定
            for interface in test_interfaces:
                for direction in ["input", "output"]:
                    self.test_bind_service_policy(interface, direction, test_policy_name)
                    time.sleep(1)
                    self.test_get_service_policy(interface, direction)
                    time.sleep(1)
            
            # 2. 完整工作流程測試
            self.test_complete_qos_workflow()
            
            # 3. 邊界條件測試
            self.test_boundary_conditions()
            
            # 4. 錯誤場景測試
            self.test_error_scenarios()
            
        finally:
            # 5. 清理測試資源
            self.cleanup_test_resources()
        
        # 6. 輸出測試總結
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
        class_map_tests = [r for r in self.test_results if 'class-map' in r['test_name']]
        policy_map_tests = [r for r in self.test_results if 'policy-map' in r['test_name']]
        service_policy_tests = [r for r in self.test_results if 'service-policy' in r['test_name']]
        error_tests = [r for r in self.test_results if ('錯誤' in r['test_name'] or '無效' in r['test_name'] or '邊界' in r['test_name'])]
        
        print(f"\n功能測試統計:")
        print(f"  Class-Map功能: {len(class_map_tests)} 個測試")
        print(f"  Policy-Map功能: {len(policy_map_tests)} 個測試")
        print(f"  Service-Policy功能: {len(service_policy_tests)} 個測試")
        print(f"  錯誤/邊界測試: {len(error_tests)} 個測試")
        
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
        with open('qos_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        print(f"\n詳細測試結果已保存到: qos_test_results.json")
        
        # 輸出創建的資源統計
        print(f"\n測試過程統計:")
        print(f"  創建的Class-Map: {len(self.created_class_maps)}")
        print(f"  創建的Policy-Map: {len(self.created_policy_maps)}")
        print(f"  應用的Service-Policy: {len(self.applied_service_policies)}")

def main():
    """主函數"""
    if len(sys.argv) < 2:
        print("使用方法: python qos_test.py <base_url> [username] [password]")
        print("範例: python qos_test.py http://192.168.1.1 admin admin123")
        print("\n功能說明:")
        print("  - 測試所有QoS API功能 (Class-Map, Policy-Map, Service-Policy)")
        print("  - 包含完整工作流程測試")
        print("  - 自動清理測試資源")
        print("  - 生成詳細測試報告")
        sys.exit(1)
    
    base_url = sys.argv[1]
    username = sys.argv[2] if len(sys.argv) > 2 else None
    password = sys.argv[3] if len(sys.argv) > 3 else None
    
    # 創建測試器並運行測試
    tester = QoSAPITester(base_url, username, password)
    
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