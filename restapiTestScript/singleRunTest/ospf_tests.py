#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSPF REST API 測試腳本
測試所有 OSPF 相關的 API 端點
版本: v0.15
"""

import getpass

import requests
import json
import sys
import time
from typing import Dict, Any, Optional, List
import hashlib

class OSPFAPITester:
    def __init__(self, base_url: str = "http://localhost", username: str = None, password: str = None):
        """
        初始化測試器
        
        Args:
            base_url: API 基礎 URL
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.username = username
        self.password = password        
        self.test_results = []
        self.created_resources = {
            'ospf_processes': [],
            'nssas': [],
            'redistributes': [],
            'summary_addresses': [],
            'network_areas': [],
            'stub_areas': [],
            'virtual_interfaces': [],
            'area_aggregates': [],
            'if_auth_md5s': []
        }
        # 設定認證
        self._setup_authentication()
        
    def _setup_authentication(self):
        """設定認證方式"""
        if self.username and self.password:
            # 使用 HTTP Basic Authentication
            self.session.auth = (self.username, self.password)
            print(f"✅ 已設定 HTTP Basic 認證 (使用者: {self.username})")
            
            # 也可以設定 headers 方式的認證
            # import base64
            # credentials = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
            # self.session.headers.update({'Authorization': f'Basic {credentials}'})
                        
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
                if 'processes' in result and isinstance(result['processes'], list):
                    print(f"    OSPF 進程數量: {len(result['processes'])}")
                    for proc in result['processes'][:3]:  # 只顯示前3個
                        print(f"    - Process ID: {proc.get('processId')}, Router ID: {proc.get('routerId')}")
                elif 'processId' in result:
                    print(f"    Process ID: {result['processId']}")
                    if 'routerId' in result:
                        print(f"    Router ID: {result['routerId']}")

    # ==================== OSPF 進程管理 ====================
    
    def test_get_all_ospf_processes(self):
        """測試 1.1: 獲取所有 OSPF 進程"""
        try:
            url = f"{self.base_url}/api/v1/ospf"
            response = self.session.get(url)
            
            success = response.status_code == 200
            self.log_test("獲取所有 OSPF 進程", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取所有 OSPF 進程", False, error=str(e))
            return None

    def test_create_ospf_process(self, process_id: int = 100):
        """測試 1.2: 創建 OSPF 進程"""
        try:
            url = f"{self.base_url}/api/v1/ospf"
            payload = {"processId": process_id}
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['ospf_processes'].append(process_id)
                
            self.log_test(f"創建 OSPF 進程 (ID: {process_id})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建 OSPF 進程 (ID: {process_id})", False, error=str(e))
            return False

    def test_get_ospf_process(self, process_id: int = 100):
        """測試 1.3: 獲取特定 OSPF 進程"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            self.log_test(f"獲取 OSPF 進程 (ID: {process_id})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取 OSPF 進程 (ID: {process_id})", False, error=str(e))
            return None

    def test_update_ospf_process(self, process_id: int = 100):
        """測試 1.4: 更新 OSPF 進程"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}"
            payload = {
                "rfc1583CompatibleState": False,
                "autoCost": 100,
                "originateDefaultRoute": False,
                "advertiseDefaultRoute": "notAlways",
                "externalMetricType": "type2",
                "defaultExternalMetric": -1,
                "spfHoldTime": 10,
                "routerId": "192.168.1.1",
                "versionNumber": 2,
                "spfDelayTime": 5,
                "defaultMetric": -1
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"更新 OSPF 進程 (ID: {process_id})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新 OSPF 進程 (ID: {process_id})", False, error=str(e))
            return False

    # ==================== NSSA 管理 ====================
    
    def test_get_all_nssas(self, process_id: int = 100):
        """測試 2.1: 獲取所有 NSSA"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/nssas"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                nssas = data.get('result', {}).get('nssas', [])
                print(f"    NSSA 數量: {len(nssas)}")
                
            self.log_test(f"獲取所有 NSSA (Process {process_id})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取所有 NSSA (Process {process_id})", False, error=str(e))
            return None

    def test_create_nssa(self, process_id: int = 100, area_id: str = "0.0.0.1"):
        """測試 2.2: 創建 NSSA"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/nssas"
            payload = {"areaId": area_id}
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['nssas'].append((process_id, area_id))
                
            self.log_test(f"創建 NSSA (Area: {area_id})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建 NSSA (Area: {area_id})", False, error=str(e))
            return False

    def test_get_nssa(self, process_id: int = 100, area_id: str = "0.0.0.1"):
        """測試 2.3: 獲取特定 NSSA"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/nssas/{area_id}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            self.log_test(f"獲取 NSSA (Area: {area_id})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取 NSSA (Area: {area_id})", False, error=str(e))
            return None

    def test_update_nssa(self, process_id: int = 100, area_id: str = "0.0.0.1"):
        """測試 2.4: 更新 NSSA"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/nssas/{area_id}"
            payload = {
                "translatorRole": "candidate",
                "redistributeStatus": True,
                "originateStatus": False,
                "metricType": "type2",
                "metric": 1
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"更新 NSSA (Area: {area_id})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新 NSSA (Area: {area_id})", False, error=str(e))
            return False

    # ==================== 重分發管理 ====================
    
    def test_get_all_redistributes(self, process_id: int = 100):
        """測試 3.1: 獲取所有重分發"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/redistributes"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                redistributes = data.get('result', {}).get('redistributes', [])
                print(f"    重分發數量: {len(redistributes)}")
                
            self.log_test(f"獲取所有重分發 (Process {process_id})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取所有重分發 (Process {process_id})", False, error=str(e))
            return None

    def test_create_redistribute(self, process_id: int = 100, protocol: str = "static"):
        """測試 3.2: 創建重分發"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/redistributes"
            payload = {"protocol": protocol}
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['redistributes'].append((process_id, protocol))
                
            self.log_test(f"創建重分發 ({protocol})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建重分發 ({protocol})", False, error=str(e))
            return False

    def test_update_redistribute(self, process_id: int = 100, protocol: str = "static"):
        """測試 3.3: 更新重分發"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/redistributes/{protocol}"
            payload = {
                "metricType": "type2",
                "metric": 20,
                "tag": 100
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"更新重分發 ({protocol})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新重分發 ({protocol})", False, error=str(e))
            return False

    # ==================== 摘要地址管理 ====================
    
    def test_get_all_summary_addresses(self, process_id: int = 100):
        """測試 4.1: 獲取所有摘要地址"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/summary-addresses"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                addresses = data.get('result', {}).get('addresses', [])
                print(f"    摘要地址數量: {len(addresses)}")
                
            self.log_test(f"獲取所有摘要地址 (Process {process_id})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取所有摘要地址 (Process {process_id})", False, error=str(e))
            return None

    def test_create_summary_address(self, process_id: int = 100, addr: str = "192.168.2.0", pfx_len: int = 24):
        """測試 4.2: 創建摘要地址"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/summary-addresses"
            payload = {
                "addr": addr,
                "pfxLen": pfx_len
            }
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['summary_addresses'].append((process_id, addr, pfx_len))
                
            self.log_test(f"創建摘要地址 ({addr}/{pfx_len})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建摘要地址 ({addr}/{pfx_len})", False, error=str(e))
            return False

    def test_get_summary_address(self, process_id: int = 100, addr: str = "192.168.2.0", pfx_len: int = 24):
        """測試 4.3: 獲取特定摘要地址"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/summary-addresses/{addr}/prefix-len/{pfx_len}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            self.log_test(f"獲取摘要地址 ({addr}/{pfx_len})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取摘要地址 ({addr}/{pfx_len})", False, error=str(e))
            return None

    # ==================== 網路區域管理 ====================
    
    def test_get_all_network_areas(self, process_id: int = 100):
        """測試 5.1: 獲取所有網路區域"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/network-areas"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                network_areas = data.get('result', {}).get('networkAreas', [])
                print(f"    網路區域數量: {len(network_areas)}")
                
            self.log_test(f"獲取所有網路區域 (Process {process_id})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取所有網路區域 (Process {process_id})", False, error=str(e))
            return None

    def test_create_network_area(self, process_id: int = 100, addr: str = "192.168.2.0", pfx_len: int = 24, area_id: str = "0.0.0.18"):
        """測試 5.2: 創建網路區域"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/network-areas"
            payload = {
                "addr": addr,
                "pfxLen": pfx_len,
                "areaId": area_id
            }
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['network_areas'].append((process_id, addr, pfx_len))
                
            self.log_test(f"創建網路區域 ({addr}/{pfx_len} -> {area_id})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建網路區域 ({addr}/{pfx_len} -> {area_id})", False, error=str(e))
            return False

    def test_update_network_area(self, process_id: int = 100, addr: str = "192.168.2.0", pfx_len: int = 24, area_id: str = "0.0.0.20"):
        """測試 5.3: 更新網路區域"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/network-areas/{addr}/prefix-len/{pfx_len}"
            payload = {"areaId": area_id}
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"更新網路區域 ({addr}/{pfx_len} -> {area_id})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新網路區域 ({addr}/{pfx_len} -> {area_id})", False, error=str(e))
            return False

    # ==================== OSPF 介面管理 ====================
    
    def test_get_all_ospf_interfaces(self):
        """測試 6.1: 獲取所有 OSPF 介面"""
        try:
            url = f"{self.base_url}/api/v1/ospf-interface"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                interfaces = data.get('result', {}).get('interfaces', [])
                print(f"    OSPF 介面數量: {len(interfaces)}")
                for intf in interfaces[:3]:  # 只顯示前3個
                    print(f"    - IP: {intf.get('ipAddress')}, Area: {intf.get('areaId')}, State: {intf.get('state')}")
                
            self.log_test("獲取所有 OSPF 介面", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取所有 OSPF 介面", False, error=str(e))
            return None

    def test_get_ospf_interface(self, ip_address: str = "1.1.1.1"):
        """測試 6.2: 獲取特定 OSPF 介面"""
        try:
            url = f"{self.base_url}/api/v1/ospf/interface/{ip_address}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            self.log_test(f"獲取 OSPF 介面 ({ip_address})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取 OSPF 介面 ({ip_address})", False, error=str(e))
            return None

    def test_update_ospf_interface(self, ip_address: str = "192.168.2.2"):
        """測試 6.3: 更新 OSPF 介面"""
        try:
            url = f"{self.base_url}/api/v1/ospf/interface/{ip_address}"
            payload = {
                "helloInterval": 20,
                "deadInterval": 80,
                "cost": 10,
                "rtrPriority": 1,
                "transmitDelay": 1,
                "retransmitInterval": 5,
                "authType": "none"
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"更新 OSPF 介面 ({ip_address})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新 OSPF 介面 ({ip_address})", False, error=str(e))
            return False

    # ==================== OSPF 區域管理 ====================
    
    def test_get_all_areas(self, process_id: int = 100):
        """測試 7.1: 獲取所有區域"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/area"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                areas = data.get('result', {}).get('areas', [])
                print(f"    區域數量: {len(areas)}")
                for area in areas[:3]:  # 只顯示前3個
                    print(f"    - Area ID: {area.get('areaId')}, Type: {area.get('importAsExtern')}")
                
            self.log_test(f"獲取所有區域 (Process {process_id})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取所有區域 (Process {process_id})", False, error=str(e))
            return None

    def test_get_area(self, process_id: int = 100, area_id: str = "1.1.1.1"):
        """測試 7.2: 獲取特定區域"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/area/{area_id}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            self.log_test(f"獲取區域 (Area: {area_id})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取區域 (Area: {area_id})", False, error=str(e))
            return None

    def test_update_area(self, process_id: int = 100, area_id: str = "1.1.1.1"):
        """測試 7.3: 更新區域"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/area/{area_id}"
            payload = {"areaSummary": "sendAreaSummary"}
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"更新區域 (Area: {area_id})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新區域 (Area: {area_id})", False, error=str(e))
            return False

    # ==================== Stub 區域管理 ====================
    
    def test_get_all_stub_areas(self, process_id: int = 100):
        """測試 8.1: 獲取所有 Stub 區域"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/stub-area"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                stub_areas = data.get('result', {}).get('stubAreas', [])
                print(f"    Stub 區域數量: {len(stub_areas)}")
                
            self.log_test(f"獲取所有 Stub 區域 (Process {process_id})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取所有 Stub 區域 (Process {process_id})", False, error=str(e))
            return None

    def test_create_stub_area(self, process_id: int = 100, area_id: str = "192.168.2.0"):
        """測試 8.2: 創建 Stub 區域"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/stub-area"
            payload = {"stubAreaId": area_id}
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['stub_areas'].append((process_id, area_id))
                
            self.log_test(f"創建 Stub 區域 ({area_id})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建 Stub 區域 ({area_id})", False, error=str(e))
            return False

    def test_update_stub_area(self, process_id: int = 100, area_id: str = "192.168.2.0"):
        """測試 8.3: 更新 Stub 區域"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/stub-area/{area_id}"
            payload = {"stubMetric": 2000}
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"更新 Stub 區域 ({area_id})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新 Stub 區域 ({area_id})", False, error=str(e))
            return False

    # ==================== LSDB 管理 ====================
    
    def test_get_all_lsdbs(self, process_id: int = 100):
        """測試 9.1: 獲取所有 LSDB"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/lsdbs"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                lsdbs = data.get('result', {}).get('lsdbs', [])
                print(f"    LSDB 條目數量: {len(lsdbs)}")
                
            self.log_test(f"獲取所有 LSDB (Process {process_id})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取所有 LSDB (Process {process_id})", False, error=str(e))
            return None

    def test_get_lsdb_entry(self, process_id: int = 100, area_id: str = "1.1.1.1", 
                           lsa_type: str = "networkLink", lsid: str = "2.2.2.2", router_id: str = "192.168.1.1"):
        """測試 9.2: 獲取特定 LSDB 條目"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/lsdbs/area/{area_id}/type/{lsa_type}/ls/{lsid}/router/{router_id}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            self.log_test(f"獲取 LSDB 條目 ({lsa_type})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取 LSDB 條目 ({lsa_type})", False, error=str(e))
            return None

    # ==================== 虛擬介面管理 ====================
    
    def test_get_all_virtual_interfaces(self, process_id: int = 100):
        """測試 10.1: 獲取所有虛擬介面"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/virt-Ifs"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                virtual_interfaces = data.get('result', {}).get('virtualInterfaces', [])
                print(f"    虛擬介面數量: {len(virtual_interfaces)}")
                
            self.log_test(f"獲取所有虛擬介面 (Process {process_id})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取所有虛擬介面 (Process {process_id})", False, error=str(e))
            return None

    def test_create_virtual_interface(self, process_id: int = 100, area_id: str = "0.0.0.2", neighbor: str = "20.20.20.20"):
        """測試 10.2: 創建虛擬介面"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/virt-Ifs"
            payload = {
                "areaId": area_id,
                "neighbor": neighbor
            }
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['virtual_interfaces'].append((process_id, area_id, neighbor))
                
            self.log_test(f"創建虛擬介面 (Area: {area_id}, Neighbor: {neighbor})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建虛擬介面 (Area: {area_id}, Neighbor: {neighbor})", False, error=str(e))
            return False

    def test_update_virtual_interface(self, process_id: int = 100, area_id: str = "0.0.0.2", neighbor: str = "20.20.20.20"):
        """測試 10.3: 更新虛擬介面"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/virt-Ifs/area/{area_id}/neighbor/{neighbor}"
            payload = {
                "transmitDelay": 1,
                "retransmitInterval": 5,
                "helloInterval": 10,
                "deadInterval": 40,
                "authKey": "5566kk",
                "authType": "none"
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"更新虛擬介面 (Area: {area_id}, Neighbor: {neighbor})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新虛擬介面 (Area: {area_id}, Neighbor: {neighbor})", False, error=str(e))
            return False

    # ==================== 鄰居管理 ====================
    
    def test_get_all_neighbors(self, process_id: int = 100):
        """測試 11.1: 獲取所有鄰居"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/neighbors"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                neighbors = data.get('result', {}).get('neighbors', [])
                print(f"    鄰居數量: {len(neighbors)}")
                for neighbor in neighbors[:3]:  # 只顯示前3個
                    print(f"    - IP: {neighbor.get('ipAddr')}, State: {neighbor.get('state')}")
                
            self.log_test(f"獲取所有鄰居 (Process {process_id})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取所有鄰居 (Process {process_id})", False, error=str(e))
            return None

    def test_get_neighbor(self, process_id: int = 100, ip_addr: str = "192.168.16.20"):
        """測試 11.2: 獲取特定鄰居"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/neighbors/{ip_addr}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            self.log_test(f"獲取鄰居 ({ip_addr})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取鄰居 ({ip_addr})", False, error=str(e))
            return None

    # ==================== 路由管理 ====================
    
    def test_get_all_routes(self, process_id: int = 100):
        """測試 12.1: 獲取所有路由"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/routes"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                routes = data.get('result', {}).get('routes', [])
                print(f"    路由數量: {len(routes)}")
                for route in routes[:3]:  # 只顯示前3個
                    print(f"    - Dest: {route.get('dest')}/{route.get('pfxLen')}, NextHop: {route.get('nexthop')}")
                
            self.log_test(f"獲取所有路由 (Process {process_id})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取所有路由 (Process {process_id})", False, error=str(e))
            return None

    def test_get_route(self, process_id: int = 100, dest: str = "20.20.2.0", pfx_len: int = 24, nexthop: str = "192.168.4.1"):
        """測試 12.2: 獲取特定路由"""
        try:
            url = f"{self.base_url}/api/v1/ospf/{process_id}/routes/destination/{dest}/prefix-length/{pfx_len}/next-hop/{nexthop}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            self.log_test(f"獲取路由 ({dest}/{pfx_len})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取路由 ({dest}/{pfx_len})", False, error=str(e))
            return None

    # ==================== MD5 認證管理 ====================
    
    def test_get_all_if_auth_md5s(self):
        """測試 13.1: 獲取所有介面 MD5 認證"""
        try:
            url = f"{self.base_url}/api/v1/ospf-if-auth-md5s"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                if_auth_md5s = data.get('result', {}).get('ifAuthMd5s', [])
                print(f"    介面 MD5 認證數量: {len(if_auth_md5s)}")
                
            self.log_test("獲取所有介面 MD5 認證", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取所有介面 MD5 認證", False, error=str(e))
            return None

    def test_create_if_auth_md5(self, ip_address: str = "192.168.4.1", key_id: int = 2, key: str = "test3"):
        """測試 13.2: 創建介面 MD5 認證"""
        try:
            url = f"{self.base_url}/api/v1/ospf-if-auth-md5s"
            payload = {
                "ipAddress": ip_address,
                "keyId": key_id,
                "key": key
            }
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['if_auth_md5s'].append((ip_address, key_id))
                
            self.log_test(f"創建介面 MD5 認證 ({ip_address}, Key ID: {key_id})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建介面 MD5 認證 ({ip_address}, Key ID: {key_id})", False, error=str(e))
            return False

    def test_update_if_auth_md5(self, ip_address: str = "192.168.4.1", key_id: int = 2, key: str = "updated_key"):
        """測試 13.3: 更新介面 MD5 認證"""
        try:
            url = f"{self.base_url}/api/v1/ospf/if-auth-md5s/ip-address/{ip_address}/key/{key_id}"
            payload = {"key": key}
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"更新介面 MD5 認證 ({ip_address}, Key ID: {key_id})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新介面 MD5 認證 ({ip_address}, Key ID: {key_id})", False, error=str(e))
            return False

    # ==================== 錯誤場景測試 ====================
    
    def test_error_scenarios(self):
        """測試錯誤場景"""
        print("\n🚨 錯誤場景測試")
        print("-" * 30)
        
        # 測試無效進程ID
        self.test_invalid_process_id()
        
        # 測試重複創建
        self.test_duplicate_creation()
        
        # 測試不存在的資源
        self.test_nonexistent_resources()
        
        # 測試無效參數
        self.test_invalid_parameters()

    def test_invalid_process_id(self):
        """測試無效進程ID"""
        try:
            url = f"{self.base_url}/api/v1/ospf/99999"  # 不存在的進程ID
            response = self.session.get(url)
            
            success = response.status_code == 404
            self.log_test("無效進程ID測試", success, response)
            
        except Exception as e:
            self.log_test("無效進程ID測試", False, error=str(e))

    def test_duplicate_creation(self):
        """測試重複創建資源"""
        try:
            # 嘗試重複創建已存在的 OSPF 進程
            url = f"{self.base_url}/api/v1/ospf"
            payload = {"processId": 100}  # 假設已存在
            
            response = self.session.post(url, json=payload)
            success = response.status_code in [400, 409]  # 可能返回 400 或 409
            
            self.log_test("重複創建測試", success, response)
            
        except Exception as e:
            self.log_test("重複創建測試", False, error=str(e))

    def test_nonexistent_resources(self):
        """測試不存在的資源"""
        try:
            url = f"{self.base_url}/api/v1/ospf/65000/nssas/9.9.9.9"  # 不存在的資源
            response = self.session.get(url)
            
            success = response.status_code == 404
            self.log_test("不存在資源測試", success, response)
            
        except Exception as e:
            self.log_test("不存在資源測試", False, error=str(e))

    def test_invalid_parameters(self):
        """測試無效參數"""
        try:
            url = f"{self.base_url}/api/v1/ospf/100"
            payload = {
                "routerId": "invalid-ip",  # 無效的 IP 地址
                "spfHoldTime": -1  # 無效的數值
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
        
        # 刪除介面 MD5 認證
        for ip_address, key_id in self.created_resources['if_auth_md5s']:
            try:
                url = f"{self.base_url}/api/v1/ospf/if-auth-md5s/ip-address/{ip_address}/key/{key_id}"
                response = self.session.delete(url)
                success = response.status_code == 200
                self.log_test(f"刪除介面 MD5 認證 ({ip_address})", success, response)
            except Exception as e:
                print(f"    刪除介面 MD5 認證失敗: {str(e)}")
        
        # 刪除區域聚合
        for process_id, area_id, net, mask in self.created_resources['area_aggregates']:
            try:
                url = f"{self.base_url}/api/v1/ospf/{process_id}/area-aggregates/area/{area_id}/net/{net}/mask/{mask}"
                response = self.session.delete(url)
                success = response.status_code == 200
                self.log_test(f"刪除區域聚合 ({net}/{mask})", success, response)
            except Exception as e:
                print(f"    刪除區域聚合失敗: {str(e)}")
        
        # 刪除虛擬介面
        for process_id, area_id, neighbor in self.created_resources['virtual_interfaces']:
            try:
                url = f"{self.base_url}/api/v1/ospf/{process_id}/virt-Ifs/area/{area_id}/neighbor/{neighbor}"
                response = self.session.delete(url)
                success = response.status_code == 200
                self.log_test(f"刪除虛擬介面 ({area_id}, {neighbor})", success, response)
            except Exception as e:
                print(f"    刪除虛擬介面失敗: {str(e)}")
        
        # 刪除 Stub 區域
        for process_id, area_id in self.created_resources['stub_areas']:
            try:
                url = f"{self.base_url}/api/v1/ospf/{process_id}/stub-area/{area_id}"
                response = self.session.delete(url)
                success = response.status_code == 200
                self.log_test(f"刪除 Stub 區域 ({area_id})", success, response)
            except Exception as e:
                print(f"    刪除 Stub 區域失敗: {str(e)}")
        
        # 刪除網路區域
        for process_id, addr, pfx_len in self.created_resources['network_areas']:
            try:
                url = f"{self.base_url}/api/v1/ospf/{process_id}/network-areas/{addr}/prefix-len/{pfx_len}"
                response = self.session.delete(url)
                success = response.status_code == 200
                self.log_test(f"刪除網路區域 ({addr}/{pfx_len})", success, response)
            except Exception as e:
                print(f"    刪除網路區域失敗: {str(e)}")
        
        # 刪除摘要地址
        for process_id, addr, pfx_len in self.created_resources['summary_addresses']:
            try:
                url = f"{self.base_url}/api/v1/ospf/{process_id}/summary-addresses/{addr}/prefix-len/{pfx_len}"
                response = self.session.delete(url)
                success = response.status_code == 200
                self.log_test(f"刪除摘要地址 ({addr}/{pfx_len})", success, response)
            except Exception as e:
                print(f"    刪除摘要地址失敗: {str(e)}")
        
        # 刪除重分發
        for process_id, protocol in self.created_resources['redistributes']:
            try:
                url = f"{self.base_url}/api/v1/ospf/{process_id}/redistributes/{protocol}"
                response = self.session.delete(url)
                success = response.status_code == 200
                self.log_test(f"刪除重分發 ({protocol})", success, response)
            except Exception as e:
                print(f"    刪除重分發失敗: {str(e)}")
        
        # 刪除 NSSA
        for process_id, area_id in self.created_resources['nssas']:
            try:
                url = f"{self.base_url}/api/v1/ospf/{process_id}/nssas/{area_id}"
                response = self.session.delete(url)
                success = response.status_code == 200
                self.log_test(f"刪除 NSSA ({area_id})", success, response)
            except Exception as e:
                print(f"    刪除 NSSA 失敗: {str(e)}")
        
        # 刪除 OSPF 進程
        for process_id in self.created_resources['ospf_processes']:
            try:
                url = f"{self.base_url}/api/v1/ospf/{process_id}"
                response = self.session.delete(url)
                success = response.status_code == 200
                self.log_test(f"刪除 OSPF 進程 (ID: {process_id})", success, response)
            except Exception as e:
                print(f"    刪除 OSPF 進程失敗: {str(e)}")

    def run_all_tests(self):
        """執行所有測試"""
        print("=" * 60)
        print("開始執行 OSPF API 測試")
        print("=" * 60)
        print(f"API 基礎 URL: {self.base_url}")
        print()
        
        # 1. 基本查詢測試
        print("📋 基本查詢測試")
        print("-" * 30)
        self.test_get_all_ospf_processes()
        self.test_get_all_ospf_interfaces()
        
        # 2. OSPF 進程管理測試
        print("\n🔧 OSPF 進程管理測試")
        print("-" * 30)
        self.test_create_ospf_process(100)
        self.test_get_ospf_process(100)
        self.test_update_ospf_process(100)
        
        # 3. NSSA 管理測試
        print("\n🌐 NSSA 管理測試")
        print("-" * 30)
        self.test_get_all_nssas(100)
        self.test_create_nssa(100, "0.0.0.1")
        self.test_get_nssa(100, "0.0.0.1")
        self.test_update_nssa(100, "0.0.0.1")
        
        # 4. 重分發管理測試
        print("\n🔄 重分發管理測試")
        print("-" * 30)
        self.test_get_all_redistributes(100)
        self.test_create_redistribute(100, "static")
        self.test_update_redistribute(100, "static")
        
        # 5. 摘要地址管理測試
        print("\n📊 摘要地址管理測試")
        print("-" * 30)
        self.test_get_all_summary_addresses(100)
        self.test_create_summary_address(100, "192.168.2.0", 24)
        self.test_get_summary_address(100, "192.168.2.0", 24)
        
        # 6. 網路區域管理測試
        print("\n🗺️ 網路區域管理測試")
        print("-" * 30)
        self.test_get_all_network_areas(100)
        self.test_create_network_area(100, "192.168.2.0", 24, "0.0.0.18")
        self.test_update_network_area(100, "192.168.2.0", 24, "0.0.0.20")
        
        # 7. 介面管理測試
        print("\n🔌 介面管理測試")
        print("-" * 30)
        self.test_get_ospf_interface("1.1.1.1")
        self.test_update_ospf_interface("192.168.2.2")
        
        # 8. 區域管理測試
        print("\n🏢 區域管理測試")
        print("-" * 30)
        self.test_get_all_areas(100)
        self.test_get_area(100, "1.1.1.1")
        self.test_update_area(100, "1.1.1.1")
        
        # 9. Stub 區域管理測試
        print("\n🚫 Stub 區域管理測試")
        print("-" * 30)
        self.test_get_all_stub_areas(100)
        self.test_create_stub_area(100, "192.168.2.0")
        self.test_update_stub_area(100, "192.168.2.0")
        
        # 10. LSDB 測試
        print("\n📚 LSDB 測試")
        print("-" * 30)
        self.test_get_all_lsdbs(100)
        self.test_get_lsdb_entry(100, "1.1.1.1", "networkLink", "2.2.2.2", "192.168.1.1")
        
        # 11. 虛擬介面測試
        print("\n🔗 虛擬介面測試")
        print("-" * 30)
        self.test_get_all_virtual_interfaces(100)
        self.test_create_virtual_interface(100, "0.0.0.2", "20.20.20.20")
        self.test_update_virtual_interface(100, "0.0.0.2", "20.20.20.20")
        
        # 12. 鄰居測試
        print("\n👥 鄰居測試")
        print("-" * 30)
        self.test_get_all_neighbors(100)
        self.test_get_neighbor(100, "192.168.16.20")
        
        # 13. 路由測試
        print("\n🛣️ 路由測試")
        print("-" * 30)
        self.test_get_all_routes(100)
        self.test_get_route(100, "20.20.2.0", 24, "192.168.4.1")
        
        # 14. MD5 認證測試
        print("\n🔐 MD5 認證測試")
        print("-" * 30)
        self.test_get_all_if_auth_md5s()
        self.test_create_if_auth_md5("192.168.4.1", 2, "test3")
        self.test_update_if_auth_md5("192.168.4.1", 2, "updated_key")
        
        # 15. 錯誤場景測試
        self.test_error_scenarios()
        
        # 16. 清理測試
        self.cleanup_resources()
        
        # 17. 測試結果統計
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

def get_user_credentials():
    """獲取用戶認證信息"""
    print("請輸入認證信息:")
    username = input("用戶帳號: ").strip()
    
    if username:
        password = getpass.getpass("密碼: ")
        m = hashlib.md5(password.encode('utf-8'))
        # Get the hash in a hexadecimal format
        password = m.hexdigest()

        return username, password
    else:
        return None, None

def main():
    """主函數"""
    print("OSPF API 測試工具")
    print("=" * 40)
    
    # 獲取配置參數
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = input("請輸入 API 基礎 URL (預設: http://localhost): ").strip()
        if not base_url:
            base_url = "http://localhost"
    
    print(f"\n使用 API URL: {base_url}")

    # 獲取認證資訊
    username, password = get_user_credentials()
    
    confirm = input("確認開始測試? (y/N): ").strip().lower()
    if confirm != 'y':
        print("測試已取消")
        return
    
    # 創建測試器並執行測試
    tester = OSPFAPITester(base_url, username, password)
    tester.run_all_tests()

if __name__ == "__main__":
    main()