#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BGP REST API 測試腳本
測試所有 BGP 相關的 API 端點
版本: v0.9
"""

import requests
import json
import sys
import time
from typing import Dict, Any, Optional, List

class BGPAPITester:
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
            'bgp_processes': [],
            'peer_groups': [],
            'peers': [],
            'prefix_lists': [],
            'community_lists': [],
            'extcommunity_lists': [],
            'route_maps': [],
            'as_paths': []
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
                if 'router-id' in result:
                    print(f"    Router ID: {result['router-id']}")
                if 'as-number' in result:
                    print(f"    AS Number: {result['as-number']}")
                if 'bgp' in result and isinstance(result['bgp'], list):
                    print(f"    BGP 進程數量: {len(result['bgp'])}")

    # ==================== BGP 進程管理 ====================
    
    def test_get_all_bgp_processes(self):
        """測試 1.1: 獲取所有 BGP 進程"""
        try:
            url = f"{self.base_url}/api/v1/bgp"
            response = self.session.get(url)
            
            success = response.status_code == 200
            self.log_test("獲取所有 BGP 進程", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取所有 BGP 進程", False, error=str(e))
            return None

    def test_create_bgp_process(self, as_number: int = 100):
        """測試 1.2: 創建 BGP 進程"""
        try:
            url = f"{self.base_url}/api/v1/bgp"
            payload = {"as-number": str(as_number)}
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['bgp_processes'].append(as_number)
                
            self.log_test(f"創建 BGP 進程 (AS {as_number})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建 BGP 進程 (AS {as_number})", False, error=str(e))
            return False

    def test_get_bgp_process_by_as(self, as_number: int = 100):
        """測試 1.3: 獲取特定 AS 的 BGP 進程"""
        try:
            url = f"{self.base_url}/api/v1/bgp/process/{as_number}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            self.log_test(f"獲取 BGP 進程 (AS {as_number})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取 BGP 進程 (AS {as_number})", False, error=str(e))
            return None

    def test_update_bgp_process(self, as_number: int = 100):
        """測試 1.4: 更新 BGP 進程配置"""
        try:
            url = f"{self.base_url}/api/v1/bgp/process/{as_number}"
            payload = {
                "router-id": "1.2.3.4",
                "local-preference": 100,
                "log-neighbor-changes": True,
                "always-compare-med": True,
                "deterministic-med": True,
                "keepalive": 60,
                "holdtime": 180
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"更新 BGP 進程 (AS {as_number})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新 BGP 進程 (AS {as_number})", False, error=str(e))
            return False

    def test_bgp_network_configuration(self, as_number: int = 100):
        """測試 1.5: BGP 網路配置"""
        try:
            url = f"{self.base_url}/api/v1/bgp/process/{as_number}"
            payload = {
                "network": True,
                "ip": "192.168.1.0",
                "mask": "255.255.255.0",
                "routemap": "test-map"
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"配置 BGP 網路 (AS {as_number})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"配置 BGP 網路 (AS {as_number})", False, error=str(e))
            return False

    def test_bgp_redistribute_configuration(self, as_number: int = 100):
        """測試 1.6: BGP 重分發配置"""
        try:
            url = f"{self.base_url}/api/v1/bgp/process/{as_number}"
            payload = {
                "redistribute": True,
                "route-type": "ospf",
                "metric": 10,
                "route-map": "redistribute-map"
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"配置 BGP 重分發 (AS {as_number})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"配置 BGP 重分發 (AS {as_number})", False, error=str(e))
            return False

    # ==================== BGP 鄰居管理 ====================
    
    def test_create_peer_group(self, as_number: int = 100, group_name: str = "TEST-GROUP"):
        """測試 2.1: 創建 Peer Group"""
        try:
            url = f"{self.base_url}/api/v1/bgp/process/{as_number}/neighbor/peer-group"
            payload = {"group-name": group_name}
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['peer_groups'].append((as_number, group_name))
                
            self.log_test(f"創建 Peer Group ({group_name})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建 Peer Group ({group_name})", False, error=str(e))
            return False

    def test_update_peer_group(self, as_number: int = 100, group_name: str = "TEST-GROUP"):
        """測試 2.2: 更新 Peer Group"""
        try:
            url = f"{self.base_url}/api/v1/bgp/process/{as_number}/neighbor/{group_name}/peer-group"
            payload = {
                "remote-as": 200,
                "description": "Test peer group",
                "timer-action": True,
                "keepalive": 30,
                "holdtime": 90,
                "next-hop-self": True,
                "route-reflector-client": True
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"更新 Peer Group ({group_name})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新 Peer Group ({group_name})", False, error=str(e))
            return False

    def test_create_bgp_peer(self, as_number: int = 100, peer_ip: str = "192.168.1.1"):
        """測試 2.3: 創建 BGP 鄰居"""
        try:
            url = f"{self.base_url}/api/v1/bgp/process/{as_number}/neighbor/peer"
            payload = {
                "peer": peer_ip,
                "remote-as": 200
            }
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['peers'].append((as_number, peer_ip))
                
            self.log_test(f"創建 BGP 鄰居 ({peer_ip})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建 BGP 鄰居 ({peer_ip})", False, error=str(e))
            return False

    def test_update_bgp_peer(self, as_number: int = 100, peer_ip: str = "192.168.1.1"):
        """測試 2.4: 更新 BGP 鄰居"""
        try:
            url = f"{self.base_url}/api/v1/bgp/process/{as_number}/neighbor/{peer_ip}/peer"
            payload = {
                "description": "Test BGP neighbor",
                "timer-action": True,
                "keepalive": 30,
                "holdtime": 90,
                "password": "bgp123",
                "next-hop-self": True,
                "soft-reconfiguration-inbound": True
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"更新 BGP 鄰居 ({peer_ip})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新 BGP 鄰居 ({peer_ip})", False, error=str(e))
            return False

    # ==================== BGP 路由信息 ====================
    
    def test_get_bgp_routes(self):
        """測試 3.1: 獲取 BGP 路由表"""
        try:
            url = f"{self.base_url}/api/v1/bgp/route"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                routes = data.get('result', {}).get('routes', [])
                print(f"    路由數量: {len(routes)}")
                
            self.log_test("獲取 BGP 路由表", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取 BGP 路由表", False, error=str(e))
            return None

    def test_get_bgp_route_summary(self):
        """測試 3.2: 獲取 BGP 路由摘要"""
        try:
            url = f"{self.base_url}/api/v1/bgp/route/summary"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                summary = data.get('result', {}).get('summary', [])
                if summary:
                    print(f"    路由器數量: {len(summary)}")
                    for s in summary:
                        print(f"    - Router ID: {s.get('router-identifier')}, AS: {s.get('local-AS')}")
                
            self.log_test("獲取 BGP 路由摘要", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取 BGP 路由摘要", False, error=str(e))
            return None

    def test_get_bgp_neighbors(self):
        """測試 3.3: 獲取 BGP 鄰居信息"""
        try:
            url = f"{self.base_url}/api/v1/bgp/route/neighbor"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                neighbors = data.get('result', {}).get('neighbor', [])
                print(f"    鄰居數量: {len(neighbors)}")
                
            self.log_test("獲取 BGP 鄰居信息", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取 BGP 鄰居信息", False, error=str(e))
            return None

    # ==================== Prefix List 管理 ====================
    
    def test_create_prefix_list(self, name: str = "TEST-PREFIX", seq: int = 10):
        """測試 4.1: 創建 Prefix List"""
        try:
            url = f"{self.base_url}/api/v1/bgp/ip/prefix-list"
            payload = {
                "prefix-list-name": name,
                "seq": seq
            }
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['prefix_lists'].append((name, seq))
                
            self.log_test(f"創建 Prefix List ({name})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建 Prefix List ({name})", False, error=str(e))
            return False

    def test_update_prefix_list(self, name: str = "TEST-PREFIX", seq: int = 10):
        """測試 4.2: 更新 Prefix List"""
        try:
            url = f"{self.base_url}/api/v1/bgp/ip/prefix-list/{name}/seq/{seq}"
            payload = {
                "permit": True,
                "ip-address": "192.168.0.0",
                "mask": "255.255.0.0",
                "ge": 24,
                "le": 32
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"更新 Prefix List ({name})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新 Prefix List ({name})", False, error=str(e))
            return False

    def test_get_prefix_lists(self):
        """測試 4.3: 獲取所有 Prefix List"""
        try:
            url = f"{self.base_url}/api/v1/bgp/ip/prefix-list"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                prefix_lists = data.get('result', {}).get('prefixlist', [])
                print(f"    Prefix List 數量: {len(prefix_lists)}")
                
            self.log_test("獲取所有 Prefix List", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取所有 Prefix List", False, error=str(e))
            return None

    # ==================== Community List 管理 ====================
    
    def test_create_community_list(self, name: str = "TEST-COMM"):
        """測試 5.1: 創建 Community List"""
        try:
            url = f"{self.base_url}/api/v1/bgp/ip/community-list"
            payload = {
                "community-list": name,
                "style": "standard",
                "permit": True,
                "internet": True,
                "local-as": True,
                "community": ["100:200", "300:400"]
            }
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['community_lists'].append(name)
                
            self.log_test(f"創建 Community List ({name})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建 Community List ({name})", False, error=str(e))
            return False

    def test_get_community_lists(self):
        """測試 5.2: 獲取所有 Community List"""
        try:
            url = f"{self.base_url}/api/v1/bgp/ip/community-list"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                comm_lists = data.get('result', {}).get('community-list', [])
                print(f"    Community List 數量: {len(comm_lists)}")
                
            self.log_test("獲取所有 Community List", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取所有 Community List", False, error=str(e))
            return None

    # ==================== Route Map 管理 ====================
    
    def test_create_route_map(self, name: str = "TEST-MAP"):
        """測試 6.1: 創建 Route Map"""
        try:
            url = f"{self.base_url}/api/v1/bgp/route-map"
            payload = {
                "map-name": name,
                "permit": True,
                "index": 10
            }
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['route_maps'].append((name, True, 10))
                
            self.log_test(f"創建 Route Map ({name})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建 Route Map ({name})", False, error=str(e))
            return False

    def test_update_route_map_match(self, name: str = "TEST-MAP"):
        """測試 6.2: 更新 Route Map Match 條件"""
        try:
            url = f"{self.base_url}/api/v1/bgp/route-map/{name}/action/true/index/10"
            payload = {
                "command": "match-ip-address",
                "action": True,
                "prefix-list": True,
                "list-name": "TEST-PREFIX"
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"更新 Route Map Match ({name})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新 Route Map Match ({name})", False, error=str(e))
            return False

    def test_update_route_map_set(self, name: str = "TEST-MAP"):
        """測試 6.3: 更新 Route Map Set 動作"""
        try:
            url = f"{self.base_url}/api/v1/bgp/route-map/{name}/action/true/index/10"
            payload = {
                "command": "set-local-preference",
                "action": True,
                "preference-value": 150
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"更新 Route Map Set ({name})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新 Route Map Set ({name})", False, error=str(e))
            return False

    def test_get_route_maps(self):
        """測試 6.4: 獲取所有 Route Map"""
        try:
            url = f"{self.base_url}/api/v1/bgp/route-map"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                route_maps = data.get('result', {}).get('route-map', [])
                print(f"    Route Map 數量: {len(route_maps)}")
                
            self.log_test("獲取所有 Route Map", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取所有 Route Map", False, error=str(e))
            return None

    # ==================== AS Path 管理 ====================
    
    def test_create_as_path(self, name: str = "TEST-AS-PATH"):
        """測試 7.1: 創建 AS Path"""
        try:
            url = f"{self.base_url}/api/v1/bgp/ip/as-path"
            payload = {
                "access-list-name": name,
                "permit": True,
                "regular-expression": "^100_"
            }
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                self.created_resources['as_paths'].append((name, True, "^100_"))
                
            self.log_test(f"創建 AS Path ({name})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"創建 AS Path ({name})", False, error=str(e))
            return False

    def test_get_as_paths(self):
        """測試 7.2: 獲取所有 AS Path"""
        try:
            url = f"{self.base_url}/api/v1/bgp/ip/as-path"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                as_paths = data.get('result', {}).get('as-path-access-list', [])
                print(f"    AS Path 數量: {len(as_paths)}")
                
            self.log_test("獲取所有 AS Path", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取所有 AS Path", False, error=str(e))
            return None

    # ==================== BGP 清除操作 ====================
    
    def test_clear_bgp(self, as_number: int = 100):
        """測試 8.1: 清除 BGP 連接"""
        try:
            url = f"{self.base_url}/api/v1/bgp/process/{as_number}/ip:clear"
            payload = {
                "clear-all": True,
                "soft": True,
                "in": True
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"清除 BGP 連接 (AS {as_number})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"清除 BGP 連接 (AS {as_number})", False, error=str(e))
            return False

    # ==================== 錯誤場景測試 ====================
    
    def test_error_scenarios(self):
        """測試錯誤場景"""
        print("\n🚨 錯誤場景測試")
        print("-" * 30)
        
        # 測試無效 AS 號碼
        self.test_invalid_as_number()
        
        # 測試重複創建
        self.test_duplicate_creation()
        
        # 測試不存在的資源
        self.test_nonexistent_resources()
        
        # 測試無效參數
        self.test_invalid_parameters()

    def test_invalid_as_number(self):
        """測試無效 AS 號碼"""
        try:
            url = f"{self.base_url}/api/v1/bgp/process/99999999"  # 超出範圍
            response = self.session.get(url)
            
            success = response.status_code == 400
            self.log_test("無效 AS 號碼測試", success, response)
            
        except Exception as e:
            self.log_test("無效 AS 號碼測試", False, error=str(e))

    def test_duplicate_creation(self):
        """測試重複創建資源"""
        try:
            # 嘗試重複創建已存在的 BGP 進程
            url = f"{self.base_url}/api/v1/bgp"
            payload = {"as-number": "100"}  # 假設已存在
            
            response = self.session.post(url, json=payload)
            success = response.status_code in [400, 409]  # 可能返回 400 或 409
            
            self.log_test("重複創建測試", success, response)
            
        except Exception as e:
            self.log_test("重複創建測試", False, error=str(e))

    def test_nonexistent_resources(self):
        """測試不存在的資源"""
        try:
            url = f"{self.base_url}/api/v1/bgp/process/65000"  # 不存在的 AS
            response = self.session.get(url)
            
            success = response.status_code == 404
            self.log_test("不存在資源測試", success, response)
            
        except Exception as e:
            self.log_test("不存在資源測試", False, error=str(e))

    def test_invalid_parameters(self):
        """測試無效參數"""
        try:
            url = f"{self.base_url}/api/v1/bgp/process/100"
            payload = {
                "router-id": "invalid-ip",  # 無效的 IP 地址
                "keepalive": -1  # 無效的數值
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
        
        # 刪除 AS Path
        for name, permit, expression in self.created_resources['as_paths']:
            try:
                url = f"{self.base_url}/api/v1/bgp/ip/as-path/{name}/action/{str(permit).lower()}/regular/{expression}"
                response = self.session.delete(url)
                success = response.status_code == 200
                self.log_test(f"刪除 AS Path ({name})", success, response)
            except Exception as e:
                print(f"    刪除 AS Path {name} 失敗: {str(e)}")
        
        # 刪除 Route Map
        for name, permit, index in self.created_resources['route_maps']:
            try:
                url = f"{self.base_url}/api/v1/bgp/route-map/{name}/action/{str(permit).lower()}/index/{index}"
                response = self.session.delete(url)
                success = response.status_code == 200
                self.log_test(f"刪除 Route Map ({name})", success, response)
            except Exception as e:
                print(f"    刪除 Route Map {name} 失敗: {str(e)}")
        
        # 刪除 Community List
        for name in self.created_resources['community_lists']:
            try:
                url = f"{self.base_url}/api/v1/bgp/ip/community-list"
                payload = {"community-list": name, "style": "standard"}
                response = self.session.delete(url, json=payload)
                success = response.status_code == 200
                self.log_test(f"刪除 Community List ({name})", success, response)
            except Exception as e:
                print(f"    刪除 Community List {name} 失敗: {str(e)}")
        
        # 刪除 Prefix List
        for name, seq in self.created_resources['prefix_lists']:
            try:
                url = f"{self.base_url}/api/v1/bgp/ip/prefix-list/{name}/seq/{seq}"
                response = self.session.delete(url)
                success = response.status_code == 200
                self.log_test(f"刪除 Prefix List ({name})", success, response)
            except Exception as e:
                print(f"    刪除 Prefix List {name} 失敗: {str(e)}")
        
        # 刪除 BGP 鄰居
        for as_number, peer_ip in self.created_resources['peers']:
            try:
                url = f"{self.base_url}/api/v1/bgp/process/{as_number}/neighbor/{peer_ip}/peer"
                response = self.session.delete(url)
                success = response.status_code == 200
                self.log_test(f"刪除 BGP 鄰居 ({peer_ip})", success, response)
            except Exception as e:
                print(f"    刪除 BGP 鄰居 {peer_ip} 失敗: {str(e)}")
        
        # 刪除 Peer Group
        for as_number, group_name in self.created_resources['peer_groups']:
            try:
                url = f"{self.base_url}/api/v1/bgp/process/{as_number}/neighbor/{group_name}/peer-group"
                response = self.session.delete(url)
                success = response.status_code == 200
                self.log_test(f"刪除 Peer Group ({group_name})", success, response)
            except Exception as e:
                print(f"    刪除 Peer Group {group_name} 失敗: {str(e)}")
        
        # 刪除 BGP 進程
        for as_number in self.created_resources['bgp_processes']:
            try:
                url = f"{self.base_url}/api/v1/bgp/process/{as_number}"
                response = self.session.delete(url)
                success = response.status_code == 200
                self.log_test(f"刪除 BGP 進程 (AS {as_number})", success, response)
            except Exception as e:
                print(f"    刪除 BGP 進程 AS {as_number} 失敗: {str(e)}")

    def run_all_tests(self):
        """執行所有測試"""
        print("=" * 60)
        print("開始執行 BGP API 測試")
        print("=" * 60)
        print(f"API 基礎 URL: {self.base_url}")
        print()
        
        # 1. 基本查詢測試
        print("📋 基本查詢測試")
        print("-" * 30)
        self.test_get_all_bgp_processes()
        self.test_get_bgp_routes()
        self.test_get_bgp_route_summary()
        self.test_get_bgp_neighbors()
        
        # 2. BGP 進程管理測試
        print("\n🔧 BGP 進程管理測試")
        print("-" * 30)
        self.test_create_bgp_process(100)
        self.test_get_bgp_process_by_as(100)
        self.test_update_bgp_process(100)
        self.test_bgp_network_configuration(100)
        self.test_bgp_redistribute_configuration(100)
        
        # 3. 鄰居管理測試
        print("\n👥 BGP 鄰居管理測試")
        print("-" * 30)
        self.test_create_peer_group(100, "TEST-GROUP")
        self.test_update_peer_group(100, "TEST-GROUP")
        self.test_create_bgp_peer(100, "192.168.1.1")
        self.test_update_bgp_peer(100, "192.168.1.1")
        
        # 4. 策略配置測試
        print("\n📜 策略配置測試")
        print("-" * 30)
        self.test_create_prefix_list("TEST-PREFIX", 10)
        self.test_update_prefix_list("TEST-PREFIX", 10)
        self.test_get_prefix_lists()
        
        self.test_create_community_list("TEST-COMM")
        self.test_get_community_lists()
        
        self.test_create_route_map("TEST-MAP")
        self.test_update_route_map_match("TEST-MAP")
        self.test_update_route_map_set("TEST-MAP")
        self.test_get_route_maps()
        
        self.test_create_as_path("TEST-AS-PATH")
        self.test_get_as_paths()
        
        # 5. BGP 操作測試
        print("\n⚡ BGP 操作測試")
        print("-" * 30)
        self.test_clear_bgp(100)
        
        # 6. 錯誤場景測試
        self.test_error_scenarios()
        
        # 7. 清理測試
        self.cleanup_resources()
        
        # 8. 測試結果統計
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
    print("BGP API 測試工具")
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
    tester = BGPAPITester(base_url)
    tester.run_all_tests()

if __name__ == "__main__":
    main()