#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARP 模組測試案例
包含ARP表項管理、靜態ARP配置、ARP代理、本地ARP代理、ARP緩存管理等相關API測試
支援ARP表項的增刪改查、超時配置、代理功能等操作
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class ARPTests(BaseTests):
    """ARP 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取ARP模組支援的類別"""
        return [
            "arp_entry_management",
            "arp_static_config",
            "arp_cache_management",
            "arp_proxy_management",
            "arp_local_proxy_management",
            "arp_advanced_operations"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有ARP測試案例"""
        all_tests = []
        all_tests.extend(self.get_arp_entry_management_tests())
        all_tests.extend(self.get_arp_static_config_tests())
        all_tests.extend(self.get_arp_cache_management_tests())
        all_tests.extend(self.get_arp_proxy_management_tests())
        all_tests.extend(self.get_arp_local_proxy_management_tests())
        all_tests.extend(self.get_arp_advanced_operations_tests())
        return all_tests
    
    def get_arp_entry_management_tests(self) -> List[APITestCase]:
        """ARP Entry Management API 測試案例"""
        return [
            # 獲取所有ARP表項
            self.create_test_case(
                name="arp_get_all_entries",
                method="GET",
                url="/api/v1/layer3/arps",
                category="arp_entry_management",
                module="arp",
                description="獲取所有ARP表項"
            ),
            
            # 添加靜態ARP表項 - 基本配置
            self.create_test_case(
                name="arp_add_static_entry_basic",
                method="POST",
                url="/api/v1/layer3/arps",
                category="arp_entry_management",
                module="arp",
                body=self.test_data.get('arp_static_entry_basic', {
                    "ipAddress": "192.168.1.100",
                    "macAddress": "00-11-22-33-44-55"
                }),
                description="添加靜態ARP表項 - 基本配置"
            ),
            
            # 添加靜態ARP表項 - 不同網段
            self.create_test_case(
                name="arp_add_static_entry_different_subnet",
                method="POST",
                url="/api/v1/layer3/arps",
                category="arp_entry_management",
                module="arp",
                body=self.test_data.get('arp_static_entry_different_subnet', {
                    "ipAddress": "10.0.0.50",
                    "macAddress": "aa-bb-cc-dd-ee-ff"
                }),
                description="添加靜態ARP表項 - 不同網段"
            ),
            
            # 添加靜態ARP表項 - 私有網段
            self.create_test_case(
                name="arp_add_static_entry_private_subnet",
                method="POST",
                url="/api/v1/layer3/arps",
                category="arp_entry_management",
                module="arp",
                body=self.test_data.get('arp_static_entry_private_subnet', {
                    "ipAddress": "172.16.1.10",
                    "macAddress": "11-22-33-44-55-66"
                }),
                description="添加靜態ARP表項 - 私有網段"
            ),
            
            # 添加靜態ARP表項 - 廣播MAC
            self.create_test_case(
                name="arp_add_static_entry_broadcast_mac",
                method="POST",
                url="/api/v1/layer3/arps",
                category="arp_entry_management",
                module="arp",
                body=self.test_data.get('arp_static_entry_broadcast_mac', {
                    "ipAddress": "192.168.2.1",
                    "macAddress": "ff-ff-ff-ff-ff-ff"
                }),
                description="添加靜態ARP表項 - 廣播MAC地址"
            ),
            
            # 獲取特定ARP表項 - 基本IP
            self.create_test_case(
                name="arp_get_specific_entry_basic",
                method="GET",
                url="/api/v1/layer3/arps/ip-address/{ipAddress}",
                category="arp_entry_management",
                module="arp",
                params={"ipAddress": "192.168.1.100"},
                description="獲取特定ARP表項 - 基本IP"
            ),
            
            # 獲取特定ARP表項 - 不同網段
            self.create_test_case(
                name="arp_get_specific_entry_different_subnet",
                method="GET",
                url="/api/v1/layer3/arps/ip-address/{ipAddress}",
                category="arp_entry_management",
                module="arp",
                params={"ipAddress": "10.0.0.50"},
                description="獲取特定ARP表項 - 不同網段"
            ),
            
            # 獲取參數化ARP表項
            self.create_test_case(
                name="arp_get_parameterized_entry",
                method="GET",
                url="/api/v1/layer3/arps/ip-address/{ipAddress}",
                category="arp_entry_management",
                module="arp",
                params={"ipAddress": self.params.get('arp_ip_address', '192.168.1.100')},
                description=f"獲取參數化ARP表項 - {self.params.get('arp_ip_address', '192.168.1.100')}"
            ),
            
            # 測試添加重複IP地址
            self.create_test_case(
                name="arp_test_add_duplicate_ip",
                method="POST",
                url="/api/v1/layer3/arps",
                category="arp_entry_management",
                module="arp",
                body=self.test_data.get('arp_duplicate_ip', {
                    "ipAddress": "192.168.1.100",  # 重複IP
                    "macAddress": "77-88-99-aa-bb-cc"
                }),
                expected_status=500,
                description="測試添加重複IP地址"
            ),
            
            # 測試無效IP地址格式
            self.create_test_case(
                name="arp_test_invalid_ip_format",
                method="POST",
                url="/api/v1/layer3/arps",
                category="arp_entry_management",
                module="arp",
                body=self.test_data.get('arp_invalid_ip_format', {
                    "ipAddress": "999.999.999.999",  # 無效IP格式
                    "macAddress": "00-11-22-33-44-55"
                }),
                expected_status=400,
                description="測試無效IP地址格式"
            ),
            
            # 測試無效MAC地址格式
            self.create_test_case(
                name="arp_test_invalid_mac_format",
                method="POST",
                url="/api/v1/layer3/arps",
                category="arp_entry_management",
                module="arp",
                body=self.test_data.get('arp_invalid_mac_format', {
                    "ipAddress": "192.168.1.200",
                    "macAddress": "invalid-mac-address"  # 無效MAC格式
                }),
                expected_status=500,
                description="測試無效MAC地址格式"
            ),
            
            # 驗證ARP表項添加
            self.create_test_case(
                name="arp_verify_entries_added",
                method="GET",
                url="/api/v1/layer3/arps",
                category="arp_entry_management",
                module="arp",
                description="驗證ARP表項添加結果"
            )
        ]
    
    def get_arp_static_config_tests(self) -> List[APITestCase]:
        """ARP Static Configuration API 測試案例"""
        return [
            # 獲取所有靜態配置ARP表項
            self.create_test_case(
                name="arp_get_all_static_config",
                method="GET",
                url="/api/v1/layer3/arps/static-config",
                category="arp_static_config",
                module="arp",
                description="獲取所有靜態配置ARP表項"
            ),
            
            # 添加更多靜態ARP表項
            self.create_test_case(
                name="arp_add_more_static_entries",
                method="POST",
                url="/api/v1/layer3/arps",
                category="arp_static_config",
                module="arp",
                body=self.test_data.get('arp_static_entry_server1', {
                    "ipAddress": "192.168.1.10",
                    "macAddress": "00-50-56-12-34-56"
                }),
                description="添加靜態ARP表項 - 服務器1"
            ),
            
            # 添加靜態ARP表項 - 服務器2
            self.create_test_case(
                name="arp_add_static_entry_server2",
                method="POST",
                url="/api/v1/layer3/arps",
                category="arp_static_config",
                module="arp",
                body=self.test_data.get('arp_static_entry_server2', {
                    "ipAddress": "192.168.1.20",
                    "macAddress": "00-50-56-78-90-ab"
                }),
                description="添加靜態ARP表項 - 服務器2"
            ),
            
            # 添加靜態ARP表項 - 網關
            self.create_test_case(
                name="arp_add_static_entry_gateway",
                method="POST",
                url="/api/v1/layer3/arps",
                category="arp_static_config",
                module="arp",
                body=self.test_data.get('arp_static_entry_gateway', {
                    "ipAddress": "192.168.1.1",
                    "macAddress": "00-1a-2b-3c-4d-5e"
                }),
                description="添加靜態ARP表項 - 網關"
            ),
            
            # 添加靜態ARP表項 - DNS服務器
            self.create_test_case(
                name="arp_add_static_entry_dns",
                method="POST",
                url="/api/v1/layer3/arps",
                category="arp_static_config",
                module="arp",
                body=self.test_data.get('arp_static_entry_dns', {
                    "ipAddress": "8.8.8.8",
                    "macAddress": "00-aa-bb-cc-dd-ee"
                }),
                description="添加靜態ARP表項 - DNS服務器"
            ),
            
            # 驗證靜態配置ARP表項
            self.create_test_case(
                name="arp_verify_static_config_entries",
                method="GET",
                url="/api/v1/layer3/arps/static-config",
                category="arp_static_config",
                module="arp",
                description="驗證靜態配置ARP表項"
            ),
            
            # 刪除靜態ARP表項 - 基本IP
            self.create_test_case(
                name="arp_delete_static_entry_basic",
                method="DELETE",
                url="/api/v1/layer3/arps/ip-address/{ipAddress}",
                category="arp_static_config",
                module="arp",
                params={"ipAddress": "192.168.1.100"},
                description="刪除靜態ARP表項 - 基本IP"
            ),
            
            # 刪除靜態ARP表項 - 服務器1
            self.create_test_case(
                name="arp_delete_static_entry_server1",
                method="DELETE",
                url="/api/v1/layer3/arps/ip-address/{ipAddress}",
                category="arp_static_config",
                module="arp",
                params={"ipAddress": "192.168.1.10"},
                description="刪除靜態ARP表項 - 服務器1"
            ),
            
            # 測試刪除不存在的ARP表項
            self.create_test_case(
                name="arp_test_delete_nonexistent_entry",
                method="DELETE",
                url="/api/v1/layer3/arps/ip-address/{ipAddress}",
                category="arp_static_config",
                module="arp",
                params={"ipAddress": "192.168.99.99"},
                expected_status=500,
                description="測試刪除不存在的ARP表項"
            ),
            
            # 驗證ARP表項刪除
            self.create_test_case(
                name="arp_verify_entries_deleted",
                method="GET",
                url="/api/v1/layer3/arps/static-config",
                category="arp_static_config",
                module="arp",
                description="驗證ARP表項刪除結果"
            )
        ]
    
    def get_arp_cache_management_tests(self) -> List[APITestCase]:
        """ARP Cache Management API 測試案例"""
        return [
            # 獲取ARP超時配置
            self.create_test_case(
                name="arp_get_cache_timeout",
                method="GET",
                url="/api/v1/layer3/arps/cache-timeout",
                category="arp_cache_management",
                module="arp",
                description="獲取ARP緩存超時配置"
            ),
            
            # 設置ARP超時 - 默認值
            self.create_test_case(
                name="arp_set_cache_timeout_default",
                method="PUT",
                url="/api/v1/layer3/arps/cache-timeout",
                category="arp_cache_management",
                module="arp",
                body=self.test_data.get('arp_cache_timeout_default', {
                    "cacheTimeout": 1200
                }),
                description="設置ARP緩存超時 - 默認值 (20分鐘)"
            ),
            
            # 設置ARP超時 - 最小值
            self.create_test_case(
                name="arp_set_cache_timeout_min",
                method="PUT",
                url="/api/v1/layer3/arps/cache-timeout",
                category="arp_cache_management",
                module="arp",
                body=self.test_data.get('arp_cache_timeout_min', {
                    "cacheTimeout": 300
                }),
                description="設置ARP緩存超時 - 最小值 (5分鐘)"
            ),
            
            # 設置ARP超時 - 最大值
            self.create_test_case(
                name="arp_set_cache_timeout_max",
                method="PUT",
                url="/api/v1/layer3/arps/cache-timeout",
                category="arp_cache_management",
                module="arp",
                body=self.test_data.get('arp_cache_timeout_max', {
                    "cacheTimeout": 86400
                }),
                description="設置ARP緩存超時 - 最大值 (1天)"
            ),
            
            # 設置ARP超時 - 自定義值
            self.create_test_case(
                name="arp_set_cache_timeout_custom",
                method="PUT",
                url="/api/v1/layer3/arps/cache-timeout",
                category="arp_cache_management",
                module="arp",
                body=self.test_data.get('arp_cache_timeout_custom', {
                    "cacheTimeout": 3600
                }),
                description="設置ARP緩存超時 - 自定義值 (1小時)"
            ),
            
            # 驗證ARP超時設置
            self.create_test_case(
                name="arp_verify_cache_timeout_setting",
                method="GET",
                url="/api/v1/layer3/arps/cache-timeout",
                category="arp_cache_management",
                module="arp",
                description="驗證ARP緩存超時設置"
            ),
            
            # 清除ARP緩存
            self.create_test_case(
                name="arp_clear_cache",
                method="PUT",
                url="/api/v1/layer3/arps/cache:clear",
                category="arp_cache_management",
                module="arp",
                description="清除ARP緩存"
            ),
            
            # 測試無效超時值 - 低於最小值
            self.create_test_case(
                name="arp_test_invalid_timeout_below_min",
                method="PUT",
                url="/api/v1/layer3/arps/cache-timeout",
                category="arp_cache_management",
                module="arp",
                body=self.test_data.get('arp_cache_timeout_below_min', {
                    "cacheTimeout": 200  # 低於最小值300
                }),
                expected_status=400,
                description="測試無效超時值 - 低於最小值"
            ),
            
            # 測試無效超時值 - 超過最大值
            self.create_test_case(
                name="arp_test_invalid_timeout_above_max",
                method="PUT",
                url="/api/v1/layer3/arps/cache-timeout",
                category="arp_cache_management",
                module="arp",
                body=self.test_data.get('arp_cache_timeout_above_max', {
                    "cacheTimeout": 100000  # 超過最大值86400
                }),
                expected_status=400,
                description="測試無效超時值 - 超過最大值"
            ),
            
            # 恢復默認ARP超時
            self.create_test_case(
                name="arp_restore_default_cache_timeout",
                method="PUT",
                url="/api/v1/layer3/arps/cache-timeout",
                category="arp_cache_management",
                module="arp",
                body=self.test_data.get('arp_cache_timeout_restore_default', {
                    "cacheTimeout": 1200
                }),
                description="恢復默認ARP緩存超時"
            )
        ]
    
    def get_arp_proxy_management_tests(self) -> List[APITestCase]:
        """ARP Proxy Management API 測試案例"""
        return [
            # 獲取ARP代理狀態 - VLAN 1
            self.create_test_case(
                name="arp_get_proxy_status_vlan1",
                method="GET",
                url="/api/v1/layer3/arps/proxy/vlans/{vlanId}",
                category="arp_proxy_management",
                module="arp",
                params={"vlanId": "1"},
                description="獲取ARP代理狀態 - VLAN 1"
            ),
            
            # 啟用ARP代理 - VLAN 1
            self.create_test_case(
                name="arp_enable_proxy_vlan1",
                method="PUT",
                url="/api/v1/layer3/arps/proxy/vlans/{vlanId}",
                category="arp_proxy_management",
                module="arp",
                params={"vlanId": "1"},
                body=self.test_data.get('arp_proxy_enable_vlan1', {
                    "status": True
                }),
                description="啟用ARP代理 - VLAN 1"
            ),
            
            # 啟用ARP代理 - VLAN 100
            self.create_test_case(
                name="arp_enable_proxy_vlan100",
                method="PUT",
                url="/api/v1/layer3/arps/proxy/vlans/{vlanId}",
                category="arp_proxy_management",
                module="arp",
                params={"vlanId": "100"},
                body=self.test_data.get('arp_proxy_enable_vlan100', {
                    "status": True
                }),
                description="啟用ARP代理 - VLAN 100"
            ),
            
            # 啟用ARP代理 - VLAN 200
            self.create_test_case(
                name="arp_enable_proxy_vlan200",
                method="PUT",
                url="/api/v1/layer3/arps/proxy/vlans/{vlanId}",
                category="arp_proxy_management",
                module="arp",
                params={"vlanId": "200"},
                body=self.test_data.get('arp_proxy_enable_vlan200', {
                    "status": True
                }),
                description="啟用ARP代理 - VLAN 200"
            ),
            
            # 獲取參數化ARP代理狀態
            self.create_test_case(
                name="arp_get_parameterized_proxy_status",
                method="GET",
                url="/api/v1/layer3/arps/proxy/vlans/{vlanId}",
                category="arp_proxy_management",
                module="arp",
                params={"vlanId": str(self.params.get('vlan_id', 1))},
                description=f"獲取參數化ARP代理狀態 - VLAN {self.params.get('vlan_id', 1)}"
            ),
            
            # 禁用ARP代理 - VLAN 1
            self.create_test_case(
                name="arp_disable_proxy_vlan1",
                method="PUT",
                url="/api/v1/layer3/arps/proxy/vlans/{vlanId}",
                category="arp_proxy_management",
                module="arp",
                params={"vlanId": "1"},
                body=self.test_data.get('arp_proxy_disable_vlan1', {
                    "status": False
                }),
                description="禁用ARP代理 - VLAN 1"
            ),
            
            # 禁用ARP代理 - VLAN 100
            self.create_test_case(
                name="arp_disable_proxy_vlan100",
                method="PUT",
                url="/api/v1/layer3/arps/proxy/vlans/{vlanId}",
                category="arp_proxy_management",
                module="arp",
                params={"vlanId": "100"},
                body=self.test_data.get('arp_proxy_disable_vlan100', {
                    "status": False
                }),
                description="禁用ARP代理 - VLAN 100"
            ),
            
            # 測試不存在的VLAN
            self.create_test_case(
                name="arp_test_proxy_nonexistent_vlan",
                method="PUT",
                url="/api/v1/layer3/arps/proxy/vlans/{vlanId}",
                category="arp_proxy_management",
                module="arp",
                params={"vlanId": "9999"},
                body=self.test_data.get('arp_proxy_nonexistent_vlan', {
                    "status": True
                }),
                expected_status=500,
                description="測試不存在的VLAN ARP代理"
            ),
            
            # 測試無效VLAN ID
            self.create_test_case(
                name="arp_test_proxy_invalid_vlan_id",
                method="GET",
                url="/api/v1/layer3/arps/proxy/vlans/{vlanId}",
                category="arp_proxy_management",
                module="arp",
                params={"vlanId": "invalid"},
                expected_status=400,
                description="測試無效VLAN ID"
            ),
            
            # 驗證ARP代理配置
            self.create_test_case(
                name="arp_verify_proxy_configuration",
                method="GET",
                url="/api/v1/layer3/arps/proxy/vlans/{vlanId}",
                category="arp_proxy_management",
                module="arp",
                params={"vlanId": "200"},
                description="驗證ARP代理配置"
            )
        ]
    
    def get_arp_local_proxy_management_tests(self) -> List[APITestCase]:
        """ARP Local Proxy Management API 測試案例"""
        return [
            # 獲取本地ARP代理狀態 - VLAN 1
            self.create_test_case(
                name="arp_get_local_proxy_status_vlan1",
                method="GET",
                url="/api/v1/layer3/arps/local-proxy/vlans/{vlanId}",
                category="arp_local_proxy_management",
                module="arp",
                params={"vlanId": "1"},
                description="獲取本地ARP代理狀態 - VLAN 1"
            ),
            
            # 啟用本地ARP代理 - VLAN 1
            self.create_test_case(
                name="arp_enable_local_proxy_vlan1",
                method="PUT",
                url="/api/v1/layer3/arps/local-proxy/vlans/{vlanId}",
                category="arp_local_proxy_management",
                module="arp",
                params={"vlanId": "1"},
                body=self.test_data.get('arp_local_proxy_enable_vlan1', {
                    "status": True
                }),
                description="啟用本地ARP代理 - VLAN 1"
            ),
            
            # 啟用本地ARP代理 - VLAN 50
            self.create_test_case(
                name="arp_enable_local_proxy_vlan50",
                method="PUT",
                url="/api/v1/layer3/arps/local-proxy/vlans/{vlanId}",
                category="arp_local_proxy_management",
                module="arp",
                params={"vlanId": "50"},
                body=self.test_data.get('arp_local_proxy_enable_vlan50', {
                    "status": True
                }),
                description="啟用本地ARP代理 - VLAN 50"
            ),
            
            # 啟用本地ARP代理 - VLAN 300
            self.create_test_case(
                name="arp_enable_local_proxy_vlan300",
                method="PUT",
                url="/api/v1/layer3/arps/local-proxy/vlans/{vlanId}",
                category="arp_local_proxy_management",
                module="arp",
                params={"vlanId": "300"},
                body=self.test_data.get('arp_local_proxy_enable_vlan300', {
                    "status": True
                }),
                description="啟用本地ARP代理 - VLAN 300"
            ),
            
            # 獲取參數化本地ARP代理狀態
            self.create_test_case(
                name="arp_get_parameterized_local_proxy_status",
                method="GET",
                url="/api/v1/layer3/arps/local-proxy/vlans/{vlanId}",
                category="arp_local_proxy_management",
                module="arp",
                params={"vlanId": str(self.params.get('local_proxy_vlan_id', 50))},
                description=f"獲取參數化本地ARP代理狀態 - VLAN {self.params.get('local_proxy_vlan_id', 50)}"
            ),
            
            # 禁用本地ARP代理 - VLAN 1
            self.create_test_case(
                name="arp_disable_local_proxy_vlan1",
                method="PUT",
                url="/api/v1/layer3/arps/local-proxy/vlans/{vlanId}",
                category="arp_local_proxy_management",
                module="arp",
                params={"vlanId": "1"},
                body=self.test_data.get('arp_local_proxy_disable_vlan1', {
                    "status": False
                }),
                description="禁用本地ARP代理 - VLAN 1"
            ),
            
            # 禁用本地ARP代理 - VLAN 50
            self.create_test_case(
                name="arp_disable_local_proxy_vlan50",
                method="PUT",
                url="/api/v1/layer3/arps/local-proxy/vlans/{vlanId}",
                category="arp_local_proxy_management",
                module="arp",
                params={"vlanId": "50"},
                body=self.test_data.get('arp_local_proxy_disable_vlan50', {
                    "status": False
                }),
                description="禁用本地ARP代理 - VLAN 50"
            ),
            
            # 測試本地代理不存在的VLAN
            self.create_test_case(
                name="arp_test_local_proxy_nonexistent_vlan",
                method="PUT",
                url="/api/v1/layer3/arps/local-proxy/vlans/{vlanId}",
                category="arp_local_proxy_management",
                module="arp",
                params={"vlanId": "8888"},
                body=self.test_data.get('arp_local_proxy_nonexistent_vlan', {
                    "status": True
                }),
                expected_status=500,
                description="測試本地代理不存在的VLAN"
            ),
            
            # 測試本地代理無效VLAN ID
            self.create_test_case(
                name="arp_test_local_proxy_invalid_vlan_id",
                method="GET",
                url="/api/v1/layer3/arps/local-proxy/vlans/{vlanId}",
                category="arp_local_proxy_management",
                module="arp",
                params={"vlanId": "invalid"},
                expected_status=400,
                description="測試本地代理無效VLAN ID"
            ),
            
            # 驗證本地ARP代理配置
            self.create_test_case(
                name="arp_verify_local_proxy_configuration",
                method="GET",
                url="/api/v1/layer3/arps/local-proxy/vlans/{vlanId}",
                category="arp_local_proxy_management",
                module="arp",
                params={"vlanId": "300"},
                description="驗證本地ARP代理配置"
            )
        ]
    
    def get_arp_advanced_operations_tests(self) -> List[APITestCase]:
        """ARP Advanced Operations API 測試案例"""
        return [
            # 批量添加ARP表項
            self.create_test_case(
                name="arp_batch_add_entries",
                method="POST",
                url="/api/v1/layer3/arps",
                category="arp_advanced_operations",
                module="arp",
                body=self.test_data.get('arp_batch_entry_1', {
                    "ipAddress": "192.168.10.1",
                    "macAddress": "00-01-02-03-04-05"
                }),
                description="批量添加ARP表項 - 條目1"
            ),
            
            # 批量添加ARP表項 - 條目2
            self.create_test_case(
                name="arp_batch_add_entries_2",
                method="POST",
                url="/api/v1/layer3/arps",
                category="arp_advanced_operations",
                module="arp",
                body=self.test_data.get('arp_batch_entry_2', {
                    "ipAddress": "192.168.10.2",
                    "macAddress": "00-01-02-03-04-06"
                }),
                description="批量添加ARP表項 - 條目2"
            ),
            
            # 批量添加ARP表項 - 條目3
            self.create_test_case(
                name="arp_batch_add_entries_3",
                method="POST",
                url="/api/v1/layer3/arps",
                category="arp_advanced_operations",
                module="arp",
                body=self.test_data.get('arp_batch_entry_3', {
                    "ipAddress": "192.168.10.3",
                    "macAddress": "00-01-02-03-04-07"
                }),
                description="批量添加ARP表項 - 條目3"
            ),
            
            # 驗證批量添加結果
            self.create_test_case(
                name="arp_verify_batch_add_results",
                method="GET",
                url="/api/v1/layer3/arps",
                category="arp_advanced_operations",
                module="arp",
                description="驗證批量添加ARP表項結果"
            ),
            
            # 配置多VLAN ARP代理
            self.create_test_case(
                name="arp_configure_multi_vlan_proxy",
                method="PUT",
                url="/api/v1/layer3/arps/proxy/vlans/{vlanId}",
                category="arp_advanced_operations",
                module="arp",
                params={"vlanId": "500"},
                body=self.test_data.get('arp_multi_vlan_proxy_500', {
                    "status": True
                }),
                description="配置多VLAN ARP代理 - VLAN 500"
            ),
            
            # 配置多VLAN ARP代理 - VLAN 600
            self.create_test_case(
                name="arp_configure_multi_vlan_proxy_600",
                method="PUT",
                url="/api/v1/layer3/arps/proxy/vlans/{vlanId}",
                category="arp_advanced_operations",
                module="arp",
                params={"vlanId": "600"},
                body=self.test_data.get('arp_multi_vlan_proxy_600', {
                    "status": True
                }),
                description="配置多VLAN ARP代理 - VLAN 600"
            ),
            
            # 配置多VLAN本地ARP代理
            self.create_test_case(
                name="arp_configure_multi_vlan_local_proxy",
                method="PUT",
                url="/api/v1/layer3/arps/local-proxy/vlans/{vlanId}",
                category="arp_advanced_operations",
                module="arp",
                params={"vlanId": "500"},
                body=self.test_data.get('arp_multi_vlan_local_proxy_500', {
                    "status": True
                }),
                description="配置多VLAN本地ARP代理 - VLAN 500"
            ),
            
            # 清除ARP緩存並重新添加
            self.create_test_case(
                name="arp_clear_cache_and_readd",
                method="PUT",
                url="/api/v1/layer3/arps/cache:clear",
                category="arp_advanced_operations",
                module="arp",
                description="清除ARP緩存並準備重新添加"
            ),
            
            # 重新添加關鍵ARP表項
            self.create_test_case(
                name="arp_readd_critical_entries",
                method="POST",
                url="/api/v1/layer3/arps",
                category="arp_advanced_operations",
                module="arp",
                body=self.test_data.get('arp_critical_entry_gateway', {
                    "ipAddress": "192.168.1.1",
                    "macAddress": "00-1a-2b-3c-4d-5e"
                }),
                description="重新添加關鍵ARP表項 - 網關"
            ),
            
            # 批量刪除ARP表項
            self.create_test_case(
                name="arp_batch_delete_entries",
                method="DELETE",
                url="/api/v1/layer3/arps/ip-address/{ipAddress}",
                category="arp_advanced_operations",
                module="arp",
                params={"ipAddress": "192.168.10.1"},
                description="批量刪除ARP表項 - 條目1"
            ),
            
            # 批量刪除ARP表項 - 條目2
            self.create_test_case(
                name="arp_batch_delete_entries_2",
                method="DELETE",
                url="/api/v1/layer3/arps/ip-address/{ipAddress}",
                category="arp_advanced_operations",
                module="arp",
                params={"ipAddress": "192.168.10.2"},
                description="批量刪除ARP表項 - 條目2"
            ),
            
            # 最終驗證ARP配置
            self.create_test_case(
                name="arp_final_verification",
                method="GET",
                url="/api/v1/layer3/arps",
                category="arp_advanced_operations",
                module="arp",
                description="最終驗證ARP配置"
            )
        ]