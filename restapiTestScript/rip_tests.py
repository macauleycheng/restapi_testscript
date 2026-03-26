#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RIP v1/v2 REST API 測試腳本
測試所有 RIP 相關的 API 端點
版本: v0.11
"""

import requests
import json
import sys
import time
from typing import Dict, Any, Optional, List

class RIPAPITester:
    def __init__(self, base_url: str = "http://localhost"):
        """
        初始化測試器
        
        Args:
            base_url: API 基礎 URL
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.test_results = []
        self.created_resources = {
            'network_vlans': [],
            'network_ip_addresses': [],
            'passive_interface_vlans': [],
            'neighbors': [],
            'instability_preventing_vlans': []
        }
        
    def log_test(self, test_name: str, success: bool, response: requests.Response = None, error: str = None):
        """記錄測試結果"""
        result = {
            'test_name': test_name,
            'success': success,
            'status_code': response.status_code if response else None,
            'response_data': response.json() if response and self._is_json_response(response) else None,
            'error': error
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if response:
            print(f"    狀態碼: {response.status_code}")
            if success and result['response_data']:
                self._print_response_summary(result['response_data'])
        if error:
            print(f"    錯誤: {error}")
        print()

    def _is_json_response(self, response: requests.Response) -> bool:
        """檢查回應是否為JSON格式"""
        content_type = response.headers.get('content-type', '')
        return 'application/json' in content_type

    def _print_response_summary(self, data: dict):
        """打印回應摘要"""
        if 'result' in data:
            result = data['result']
            if isinstance(result, dict):
                # RIP 基本配置信息
                if 'version' in result:
                    print(f"    RIP 版本: {result['version']}")
                if 'updateTimer' in result:
                    print(f"    更新計時器: {result['updateTimer']} 秒")
                if 'timeoutTimer' in result:
                    print(f"    超時計時器: {result['timeoutTimer']} 秒")
                if 'garbageTimer' in result:
                    print(f"    垃圾回收計時器: {result['garbageTimer']} 秒")
                
                # 網路配置信息
                if 'networks' in result and isinstance(result['networks'], list):
                    print(f"    網路數量: {len(result['networks'])}")
                    for net in result['networks'][:3]:  # 只顯示前3個
                        if 'vlanId' in net:
                            print(f"    - VLAN ID: {net['vlanId']}")
                        elif 'ipAddress' in net:
                            print(f"    - IP: {net['ipAddress']}/{net.get('prefixLen', 'N/A')}")
                
                # 被動介面信息
                if 'passiveInterfaces' in result and isinstance(result['passiveInterfaces'], list):
                    print(f"    被動介面數量: {len(result['passiveInterfaces'])}")
                
                # 鄰居信息
                if 'neighbors' in result and isinstance(result['neighbors'], list):
                    print(f"    鄰居數量: {len(result['neighbors'])}")

    # ==================== RIP 基本配置管理 ====================
    
    def test_get_rip_config(self):
        """測試 1.1: 獲取 RIP 配置"""
        try:
            url = f"{self.base_url}/api/v1/rip"
            response = self.session.get(url)
            
            success = response.status_code == 200
            self.log_test("獲取 RIP 配置", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取 RIP 配置", False, error=str(e))
            return None

    def test_update_rip_config(self):
        """測試 1.2: 更新 RIP 配置"""
        try:
            url = f"{self.base_url}/api/v1/rip"
            payload = {
                "version": 2,
                "defaultInformationOriginate": True,
                "defaultMetric": 5,
                "distance": 120,
                "maximumPaths": 4,
                "redistributeConnected": True,
                "redistributeStatic": True,
                "redistributeOspf": False,
                "autoSummary": True,
                "validateUpdateSource": True
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test("更新 RIP 配置", success, response)
            return success
            
        except Exception as e:
            self.log_test("更新 RIP 配置", False, error=str(e))
            return False

    # ==================== RIP 基本計時器管理 ====================
    
    def test_get_basic_timers(self):
        """測試 2.1: 獲取基本計時器"""
        try:
            url = f"{self.base_url}/api/v1/rip/basic-timers"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                result = data.get('result', {})
                print(f"    更新計時器: {result.get('updateTimer', 'N/A')} 秒")
                print(f"    超時計時器: {result.get('timeoutTimer', 'N/A')} 秒")
                print(f"    垃圾回收計時器: {result.get('garbageTimer', 'N/A')} 秒")
                
            self.log_test("獲取基本計時器", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取基本計時器", False, error=str(e))
            return None

    def test_update_basic_timers(self):
        """測試 2.2: 更新基本計時器"""
        try:
            url = f"{self.base_url}/api/v1/rip/basic-timers"
            payload = {
                "updateTimer": 30,
                "timeoutTimer": 180,
                "garbageTimer": 120
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test("更新基本計時器", success, response)
            return success
            
        except Exception as e:
            self.log_test("更新基本計時器", False, error=str(e))
            return False

    # ==================== 不穩定防護 VLAN 管理 ====================
    
    def test_get_instability_preventing_vlans(self):
        """測試 3.1: 獲取不穩定防護 VLAN"""
        try:
            url = f"{self.base_url}/api/v1/rip/instability-preventing/vlans"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                vlans = data.get('result', {}).get('vlans', [])
                print(f"    不穩定防護 VLAN 數量: {len(vlans)}")
                for vlan in vlans[:5]:  # 只顯示前5個
                    print(f"    - VLAN ID: {vlan.get('vlanId')}")
                
            self.log_test("獲取不穩定防護 VLAN", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取不穩定防護 VLAN", False, error=str(e))
            return None

    def test_get_instability_preventing_vlan(self, vlan_id: int = 100):
        """測試 3.2: 獲取特定不穩定防護 VLAN"""
        try:
            url = f"{self.base_url}/api/v1/rip/instability-preventing/vlans/{vlan_id}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            self.log_test(f"獲取不穩定防護 VLAN (ID: {vlan_id})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取不穩定防護 VLAN (ID: {vlan_id})", False, error=str(e))
            return None

    def test_update_instability_preventing_vlan(self, vlan_id: int = 100):
        """測試 3.3: 更新不穩定防護 VLAN"""
        try:
            url = f"{self.base_url}/api/v1/rip/instability-preventing/vlans/{vlan_id}"
            payload = {
                "splitHorizonStatus": "enable"
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['instability_preventing_vlans'].append(vlan_id)
                
            self.log_test(f"更新不穩定防護 VLAN (ID: {vlan_id})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新不穩定防護 VLAN (ID: {vlan_id})", False, error=str(e))
            return False

    # ==================== 網路 VLAN 管理 ====================
    
    def test_get_network_vlans(self):
        """測試 4.1: 獲取網路 VLAN"""
        try:
            url = f"{self.base_url}/api/v1/rip/network/vlans"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                vlans = data.get('result', {}).get('vlans', [])
                print(f"    網路 VLAN 數量: {len(vlans)}")
                for vlan in vlans[:5]:  # 只顯示前5個
                    print(f"    - VLAN ID: {vlan.get('vlanId')}")
                
            self.log_test("獲取網路 VLAN", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取網路 VLAN", False, error=str(e))
            return None

    def test_create_network_vlan(self, vlan_id: int = 200):
        """測試 4.2: 創建網路 VLAN"""
        try:
            url = f"{self.base_url}/api/v1/rip/network/vlans"
            payload = {"vlanId": vlan_id}
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['network_vlans'].append(vlan_id)
                
            self.log_test(f"創建網路 VLAN (ID: {vlan_id})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建網路 VLAN (ID: {vlan_id})", False, error=str(e))
            return False

    def test_get_network_vlan(self, vlan_id: int = 200):
        """測試 4.3: 獲取特定網路 VLAN"""
        try:
            url = f"{self.base_url}/api/v1/rip/network/vlans/{vlan_id}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            self.log_test(f"獲取網路 VLAN (ID: {vlan_id})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取網路 VLAN (ID: {vlan_id})", False, error=str(e))
            return None

    def test_delete_network_vlan(self, vlan_id: int = 200):
        """測試 4.4: 刪除網路 VLAN"""
        try:
            url = f"{self.base_url}/api/v1/rip/network/vlans/{vlan_id}"
            response = self.session.delete(url)
            
            success = response.status_code == 200
            self.log_test(f"刪除網路 VLAN (ID: {vlan_id})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"刪除網路 VLAN (ID: {vlan_id})", False, error=str(e))
            return False

    # ==================== 網路 IP 地址管理 ====================
    
    def test_get_network_ip_addresses(self):
        """測試 5.1: 獲取網路 IP 地址"""
        try:
            url = f"{self.base_url}/api/v1/rip/network/ip-addresses"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                ip_addresses = data.get('result', {}).get('ipAddresses', [])
                print(f"    網路 IP 地址數量: {len(ip_addresses)}")
                for ip in ip_addresses[:5]:  # 只顯示前5個
                    print(f"    - IP: {ip.get('ipAddress')}/{ip.get('prefixLen')}")
                
            self.log_test("獲取網路 IP 地址", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取網路 IP 地址", False, error=str(e))
            return None

    def test_create_network_ip_address(self, ip_address: str = "192.168.100.0", prefix_len: int = 24):
        """測試 5.2: 創建網路 IP 地址"""
        try:
            url = f"{self.base_url}/api/v1/rip/network/ip-addresses"
            payload = {
                "ipAddress": ip_address,
                "prefixLen": prefix_len
            }
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['network_ip_addresses'].append((ip_address, prefix_len))
                
            self.log_test(f"創建網路 IP 地址 ({ip_address}/{prefix_len})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建網路 IP 地址 ({ip_address}/{prefix_len})", False, error=str(e))
            return False

    def test_get_network_ip_address(self, ip_address: str = "192.168.100.0", prefix_len: int = 24):
        """測試 5.3: 獲取特定網路 IP 地址"""
        try:
            url = f"{self.base_url}/api/v1/rip/network/ip-addresses/{ip_address}/prefix/{prefix_len}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            self.log_test(f"獲取網路 IP 地址 ({ip_address}/{prefix_len})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取網路 IP 地址 ({ip_address}/{prefix_len})", False, error=str(e))
            return None

    def test_delete_network_ip_address(self, ip_address: str = "192.168.100.0", prefix_len: int = 24):
        """測試 5.4: 刪除網路 IP 地址"""
        try:
            url = f"{self.base_url}/api/v1/rip/network/ip-addresses/{ip_address}/prefix/{prefix_len}"
            response = self.session.delete(url)
            
            success = response.status_code == 200
            self.log_test(f"刪除網路 IP 地址 ({ip_address}/{prefix_len})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"刪除網路 IP 地址 ({ip_address}/{prefix_len})", False, error=str(e))
            return False

    # ==================== 被動介面 VLAN 管理 ====================
    
    def test_get_passive_interface_vlans(self):
        """測試 6.1: 獲取被動介面 VLAN"""
        try:
            url = f"{self.base_url}/api/v1/rip/passive-interface/vlans"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                vlans = data.get('result', {}).get('vlans', [])
                print(f"    被動介面 VLAN 數量: {len(vlans)}")
                for vlan in vlans[:5]:  # 只顯示前5個
                    print(f"    - VLAN ID: {vlan.get('vlanId')}")
                
            self.log_test("獲取被動介面 VLAN", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取被動介面 VLAN", False, error=str(e))
            return None

    def test_create_passive_interface_vlan(self, vlan_id: int = 300):
        """測試 6.2: 創建被動介面 VLAN"""
        try:
            url = f"{self.base_url}/api/v1/rip/passive-interface/vlans"
            payload = {"vlanId": vlan_id}
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['passive_interface_vlans'].append(vlan_id)
                
            self.log_test(f"創建被動介面 VLAN (ID: {vlan_id})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建被動介面 VLAN (ID: {vlan_id})", False, error=str(e))
            return False

    def test_get_passive_interface_vlan(self, vlan_id: int = 300):
        """測試 6.3: 獲取特定被動介面 VLAN"""
        try:
            url = f"{self.base_url}/api/v1/rip/passive-interface/vlans/{vlan_id}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            self.log_test(f"獲取被動介面 VLAN (ID: {vlan_id})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取被動介面 VLAN (ID: {vlan_id})", False, error=str(e))
            return None

    def test_update_passive_interface_vlan(self, vlan_id: int = 300):
        """測試 6.4: 更新被動介面 VLAN"""
        try:
            url = f"{self.base_url}/api/v1/rip/passive-interface/vlans/{vlan_id}"
            payload = {
                "passiveInterface": True,
                "description": f"Passive interface for VLAN {vlan_id}"
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"更新被動介面 VLAN (ID: {vlan_id})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新被動介面 VLAN (ID: {vlan_id})", False, error=str(e))
            return False

    def test_delete_passive_interface_vlan(self, vlan_id: int = 300):
        """測試 6.5: 刪除被動介面 VLAN"""
        try:
            url = f"{self.base_url}/api/v1/rip/passive-interface/vlans/{vlan_id}"
            response = self.session.delete(url)
            
            success = response.status_code == 200
            self.log_test(f"刪除被動介面 VLAN (ID: {vlan_id})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"刪除被動介面 VLAN (ID: {vlan_id})", False, error=str(e))
            return False

    # ==================== 鄰居管理 ====================
    
    def test_get_neighbors(self):
        """測試 7.1: 獲取所有鄰居"""
        try:
            url = f"{self.base_url}/api/v1/rip/neighbors"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                neighbors = data.get('result', {}).get('neighbors', [])
                print(f"    鄰居數量: {len(neighbors)}")
                for neighbor in neighbors[:5]:  # 只顯示前5個
                    print(f"    - IP: {neighbor.get('ipAddress')}")
                
            self.log_test("獲取所有鄰居", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取所有鄰居", False, error=str(e))
            return None

    def test_create_neighbor(self, ip_address: str = "192.168.1.100"):
        """測試 7.2: 創建鄰居"""
        try:
            url = f"{self.base_url}/api/v1/rip/neighbors"
            payload = {"ipAddress": ip_address}
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['neighbors'].append(ip_address)
                
            self.log_test(f"創建鄰居 ({ip_address})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建鄰居 ({ip_address})", False, error=str(e))
            return False

    def test_delete_neighbor(self, ip_address: str = "192.168.1.100"):
        """測試 7.3: 刪除鄰居"""
        try:
            url = f"{self.base_url}/api/v1/rip/neighbors/{ip_address}"
            response = self.session.delete(url)
            
            success = response.status_code == 200
            self.log_test(f"刪除鄰居 ({ip_address})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"刪除鄰居 ({ip_address})", False, error=str(e))
            return False

    # ==================== RIP 路由表和統計信息 ====================
    
    def test_get_rip_routes(self):
        """測試 8.1: 獲取 RIP 路由表"""
        try:
            url = f"{self.base_url}/api/v1/rip/routes"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                routes = data.get('result', {}).get('routes', [])
                print(f"    RIP 路由數量: {len(routes)}")
                for route in routes[:5]:  # 只顯示前5個
                    print(f"    - 目的地: {route.get('destination')}/{route.get('prefixLen')}")
                    print(f"      下一跳: {route.get('nextHop')}, 跳數: {route.get('metric')}")
                
            self.log_test("獲取 RIP 路由表", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取 RIP 路由表", False, error=str(e))
            return None

    def test_get_rip_statistics(self):
        """測試 8.2: 獲取 RIP 統計信息"""
        try:
            url = f"{self.base_url}/api/v1/rip/statistics"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                stats = data.get('result', {})
                print(f"    發送的更新包: {stats.get('updatesSent', 'N/A')}")
                print(f"    接收的更新包: {stats.get('updatesReceived', 'N/A')}")
                print(f"    錯誤包數量: {stats.get('badPackets', 'N/A')}")
                print(f"    路由超時數量: {stats.get('routeTimeouts', 'N/A')}")
                
            self.log_test("獲取 RIP 統計信息", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取 RIP 統計信息", False, error=str(e))
            return None

    def test_clear_rip_statistics(self):
        """測試 8.3: 清除 RIP 統計信息"""
        try:
            url = f"{self.base_url}/api/v1/rip/statistics/clear"
            response = self.session.post(url)
            
            success = response.status_code == 200
            self.log_test("清除 RIP 統計信息", success, response)
            return success
            
        except Exception as e:
            self.log_test("清除 RIP 統計信息", False, error=str(e))
            return False

    # ==================== RIP 介面配置 ====================
    
    def test_get_rip_interfaces(self):
        """測試 9.1: 獲取 RIP 介面配置"""
        try:
            url = f"{self.base_url}/api/v1/rip/interfaces"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                interfaces = data.get('result', {}).get('interfaces', [])
                print(f"    RIP 介面數量: {len(interfaces)}")
                for intf in interfaces[:5]:  # 只顯示前5個
                    print(f"    - 介面: {intf.get('interfaceName')}")
                    print(f"      IP: {intf.get('ipAddress')}, 狀態: {intf.get('status')}")
                
            self.log_test("獲取 RIP 介面配置", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取 RIP 介面配置", False, error=str(e))
            return None

    def test_update_rip_interface(self, interface_name: str = "vlan200"):
        """測試 9.2: 更新 RIP 介面配置"""
        try:
            url = f"{self.base_url}/api/v1/rip/interfaces/{interface_name}"
            payload = {
                "ripVersion": 2,
                "authentication": "md5",
                "authenticationKey": "rip123",
                "splitHorizon": True,
                "poisonReverse": True,
                "sendVersion": 2,
                "receiveVersion": 2
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"更新 RIP 介面配置 ({interface_name})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新 RIP 介面配置 ({interface_name})", False, error=str(e))
            return False

    # ==================== RIP 重分發配置 ====================
    
    def test_get_redistribute_config(self):
        """測試 10.1: 獲取重分發配置"""
        try:
            url = f"{self.base_url}/api/v1/rip/redistribute"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                redistribute = data.get('result', {})
                print(f"    重分發連接路由: {redistribute.get('connected', False)}")
                print(f"    重分發靜態路由: {redistribute.get('static', False)}")
                print(f"    重分發 OSPF 路由: {redistribute.get('ospf', False)}")
                
            self.log_test("獲取重分發配置", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取重分發配置", False, error=str(e))
            return None

    def test_update_redistribute_config(self):
        """測試 10.2: 更新重分發配置"""
        try:
            url = f"{self.base_url}/api/v1/rip/redistribute"
            payload = {
                "connected": True,
                "static": True,
                "ospf": False,
                "connectedMetric": 1,
                "staticMetric": 2,
                "ospfMetric": 5
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test("更新重分發配置", success, response)
            return success
            
        except Exception as e:
            self.log_test("更新重分發配置", False, error=str(e))
            return False

    # ==================== RIP 路由過濾 ====================
    
    def test_get_route_filters(self):
        """測試 11.1: 獲取路由過濾配置"""
        try:
            url = f"{self.base_url}/api/v1/rip/route-filters"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                filters = data.get('result', {}).get('filters', [])
                print(f"    路由過濾規則數量: {len(filters)}")
                
            self.log_test("獲取路由過濾配置", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取路由過濾配置", False, error=str(e))
            return None

    def test_create_route_filter(self, filter_name: str = "TEST-FILTER"):
        """測試 11.2: 創建路由過濾規則"""
        try:
            url = f"{self.base_url}/api/v1/rip/route-filters"
            payload = {
                "filterName": filter_name,
                "action": "permit",
                "network": "192.168.0.0",
                "mask": "255.255.0.0",
                "direction": "in"
            }
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"創建路由過濾規則 ({filter_name})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建路由過濾規則 ({filter_name})", False, error=str(e))
            return False

    # ==================== 錯誤場景測試 ====================
    
    def test_error_scenarios(self):
        """測試錯誤場景"""
        print("\n🚨 錯誤場景測試")
        print("-" * 30)
        
        # 測試無效 VLAN ID
        self.test_invalid_vlan_id()
        
        # 測試重複創建
        self.test_duplicate_creation()
        
        # 測試不存在的資源
        self.test_nonexistent_resources()
        
        # 測試無效參數
        self.test_invalid_parameters()

    def test_invalid_vlan_id(self):
        """測試無效 VLAN ID"""
        try:
            url = f"{self.base_url}/api/v1/rip/network/vlans/5000"  # 超出範圍的 VLAN ID
            response = self.session.get(url)
            
            success = response.status_code == 400
            self.log_test("無效 VLAN ID 測試", success, response)
            
        except Exception as e:
            self.log_test("無效 VLAN ID 測試", False, error=str(e))

    def test_duplicate_creation(self):
        """測試重複創建資源"""
        try:
            # 嘗試重複創建已存在的網路 VLAN
            url = f"{self.base_url}/api/v1/rip/network/vlans"
            payload = {"vlanId": 200}  # 假設已存在
            
            response = self.session.post(url, json=payload)
            success = response.status_code in [400, 409]  # 可能返回 400 或 409
            
            self.log_test("重複創建測試", success, response)
            
        except Exception as e:
            self.log_test("重複創建測試", False, error=str(e))

    def test_nonexistent_resources(self):
        """測試不存在的資源"""
        try:
            url = f"{self.base_url}/api/v1/rip/network/vlans/9999"  # 不存在的 VLAN
            response = self.session.get(url)
            
            success = response.status_code == 404
            self.log_test("不存在資源測試", success, response)
            
        except Exception as e:
            self.log_test("不存在資源測試", False, error=str(e))

    def test_invalid_parameters(self):
        """測試無效參數"""
        try:
            url = f"{self.base_url}/api/v1/rip"
            payload = {
                "version": 3,  # 無效的 RIP 版本
                "defaultMetric": -1  # 無效的度量值
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 400
            
            self.log_test("無效參數測試", success, response)
            
        except Exception as e:
            self.log_test("無效參數測試", False, error=str(e))

    # ==================== 清理操作 ====================
    
    def cleanup_resources(self):
        """清理測試創建的資源"""
        print("\n🗑️ 清理測試資源")
        print("-" * 30)
        
        # 刪除鄰居
        for ip_address in self.created_resources['neighbors']:
            try:
                self.test_delete_neighbor(ip_address)
            except Exception as e:
                print(f"    刪除鄰居 {ip_address} 失敗: {str(e)}")
        
        # 刪除被動介面 VLAN
        for vlan_id in self.created_resources['passive_interface_vlans']:
            try:
                self.test_delete_passive_interface_vlan(vlan_id)
            except Exception as e:
                print(f"    刪除被動介面 VLAN {vlan_id} 失敗: {str(e)}")
        
        # 刪除網路 IP 地址
        for ip_address, prefix_len in self.created_resources['network_ip_addresses']:
            try:
                self.test_delete_network_ip_address(ip_address, prefix_len)
            except Exception as e:
                print(f"    刪除網路 IP 地址 {ip_address}/{prefix_len} 失敗: {str(e)}")
        
        # 刪除網路 VLAN
        for vlan_id in self.created_resources['network_vlans']:
            try:
                self.test_delete_network_vlan(vlan_id)
            except Exception as e:
                print(f"    刪除網路 VLAN {vlan_id} 失敗: {str(e)}")

    def run_all_tests(self):
        """執行所有測試"""
        print("=" * 60)
        print("開始執行 RIP v1/v2 API 測試")
        print("=" * 60)
        print(f"API 基礎 URL: {self.base_url}")
        print()
        
        # 1. 基本配置測試
        print("📋 基本配置測試")
        print("-" * 30)
        self.test_get_rip_config()
        self.test_update_rip_config()
        
        # 2. 計時器配置測試
        print("\n⏰ 計時器配置測試")
        print("-" * 30)
        self.test_get_basic_timers()
        self.test_update_basic_timers()
        
        # 3. 不穩定防護 VLAN 測試
        print("\n🛡️ 不穩定防護 VLAN 測試")
        print("-" * 30)
        self.test_get_instability_preventing_vlans()
        self.test_get_instability_preventing_vlan(100)
        self.test_update_instability_preventing_vlan(100)
        
        # 4. 網路 VLAN 管理測試
        print("\n🌐 網路 VLAN 管理測試")
        print("-" * 30)
        self.test_get_network_vlans()
        self.test_create_network_vlan(200)
        self.test_get_network_vlan(200)
        
        # 5. 網路 IP 地址管理測試
        print("\n🔢 網路 IP 地址管理測試")
        print("-" * 30)
        self.test_get_network_ip_addresses()
        self.test_create_network_ip_address("192.168.100.0", 24)
        self.test_get_network_ip_address("192.168.100.0", 24)
        
        # 6. 被動介面 VLAN 管理測試
        print("\n🔇 被動介面 VLAN 管理測試")
        print("-" * 30)
        self.test_get_passive_interface_vlans()
        self.test_create_passive_interface_vlan(300)
        self.test_get_passive_interface_vlan(300)
        self.test_update_passive_interface_vlan(300)
        
        # 7. 鄰居管理測試
        print("\n👥 鄰居管理測試")
        print("-" * 30)
        self.test_get_neighbors()
        self.test_create_neighbor("192.168.1.100")
        
        # 8. 路由和統計信息測試
        print("\n📊 路由和統計信息測試")
        print("-" * 30)
        self.test_get_rip_routes()
        self.test_get_rip_statistics()
        self.test_clear_rip_statistics()
        
        # 9. 介面配置測試
        print("\n🔌 介面配置測試")
        print("-" * 30)
        self.test_get_rip_interfaces()
        self.test_update_rip_interface("vlan200")
        
        # 10. 重分發配置測試
        print("\n🔄 重分發配置測試")
        print("-" * 30)
        self.test_get_redistribute_config()
        self.test_update_redistribute_config()
        
        # 11. 路由過濾測試
        print("\n🚫 路由過濾測試")
        print("-" * 30)
        self.test_get_route_filters()
        self.test_create_route_filter("TEST-FILTER")
        
        # 12. 錯誤場景測試
        self.test_error_scenarios()
        
        # 13. 清理測試
        self.cleanup_resources()
        
        # 14. 測試結果統計
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
        
        # 統計創建的資源
        total_resources = sum(len(resources) for resources in self.created_resources.values())
        print(f"\n創建的測試資源總數: {total_resources}")
        for resource_type, resources in self.created_resources.items():
            if resources:
                print(f"  {resource_type}: {len(resources)}")
        
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
    print("RIP v1/v2 API 測試工具")
    print("=" * 40)
    
    # 獲取配置參數
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = input("請輸入 API 基礎 URL (預設: http://localhost): ").strip()
        if not base_url:
            base_url = "http://localhost"
    
    print(f"\n使用 API URL: {base_url}")
    
    confirm = input("確認開始測試? (y/N): ").strip().lower()
    if confirm != 'y':
        print("測試已取消")
        return
    
    # 創建測試器並執行測試
    tester = RIPAPITester(base_url)
    tester.run_all_tests()

if __name__ == "__main__":
    main()