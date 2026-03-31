#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DHCP 模組測試案例
包含DHCP Client, Server, Relay, Snooping, DHCPv6相關API測試
"""

from typing import List
# 修正導入方式 - 使用絕對導入
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class DHCPTests(BaseTests):
    """DHCP 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取DHCP模組支援的類別"""
        return [
            "dhcp_client",
            "dhcp_server", 
            "dhcp_relay",
            "dhcp_snooping",
            "dhcpv6_relay",
            "dhcpv6_snooping"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有DHCP測試案例"""
        all_tests = []
        all_tests.extend(self.get_dhcp_client_tests())
        all_tests.extend(self.get_dhcp_server_tests())
        all_tests.extend(self.get_dhcp_relay_tests())
        all_tests.extend(self.get_dhcp_snooping_tests())
        all_tests.extend(self.get_dhcpv6_relay_tests())
        all_tests.extend(self.get_dhcpv6_snooping_tests())
        return all_tests
    
    # ... 其餘方法保持不變
    def get_dhcp_client_tests(self) -> List[APITestCase]:
        """DHCP Client API 測試案例"""
        return [
            self.create_test_case(
                name="dhcp_client_get_all_vlans",
                method="GET",
                url="/api/v1/dhcp-client/vlans",
                category="dhcp_client",
                module="dhcp",
                description="獲取所有VLAN的DHCP客戶端信息"
            ),
            self.create_test_case(
                name="dhcp_client_get_vlan",
                method="GET",
                url="/api/v1/dhcp-client/vlans/{vlanId}",
                category="dhcp_client",
                module="dhcp",
                params={"vlanId": self.params.get('vlan_id', 100)},
                description=f"獲取VLAN {self.params.get('vlan_id', 100)}的DHCP客戶端信息"
            ),
            self.create_test_case(
                name="dhcp_client_update_vlan",
                method="PUT",
                url="/api/v1/dhcp-client/vlans/{vlanId}",
                category="dhcp_client",
                module="dhcp",
                params={"vlanId": self.params.get('vlan_id', 100)},
                body=self.test_data.get('dhcp_client_vlan', {"status": True, "addrMode": "DHCP"}),
                description=f"更新VLAN {self.params.get('vlan_id', 100)}的DHCP客戶端配置"
            ),
            self.create_test_case(
                name="dhcp_client_restart",
                method="PUT",
                url="/api/v1/dhcp-client/restart",
                category="dhcp_client",
                module="dhcp",
                body={},
                description="重啟DHCP客戶端服務"
            )
        ]
    
    def get_dhcp_server_tests(self) -> List[APITestCase]:
        """DHCP Server API 測試案例"""
        return [
            self.create_test_case(
                name="dhcp_server_get_all_pools",
                method="GET",
                url="/api/v1/dhcp-server/pools",
                category="dhcp_server",
                module="dhcp",
                description="獲取所有DHCP池信息"
            ),
            self.create_test_case(
                name="dhcp_server_create_pool",
                method="POST",
                url="/api/v1/dhcp-server/pools",
                category="dhcp_server",
                module="dhcp",
                body=self.test_data.get('dhcp_pool', {
                    "poolName": "test_pool",
                    "network": "192.168.100.0",
                    "netmask": "255.255.255.0"
                }),
                description="創建新的DHCP池"
            ),
            # ... 其他測試案例
        ]
    
    def get_dhcp_relay_tests(self) -> List[APITestCase]:
        """DHCP Relay API 測試案例"""
        return [
            self.create_test_case(
                name="dhcp_relay_get_all_vlans",
                method="GET",
                url="/api/v1/dhcp-relay/server-inet-addr/vlans",
                category="dhcp_relay",
                module="dhcp",
                description="獲取所有VLAN的DHCP中繼服務器信息"
            ),
            # ... 其他測試案例
        ]
    
    def get_dhcp_snooping_tests(self) -> List[APITestCase]:
        """DHCP Snooping API 測試案例"""
        return [
            self.create_test_case(
                name="dhcp_snooping_get_config",
                method="GET",
                url="/api/v1/dhcp-snooping",
                category="dhcp_snooping",
                module="dhcp",
                description="獲取DHCP Snooping全局配置"
            ),
            # ... 其他測試案例
        ]
    
    def get_dhcpv6_relay_tests(self) -> List[APITestCase]:
        """DHCPv6 Relay API 測試案例"""
        return [
            self.create_test_case(
                name="dhcpv6_relay_get_all_vlans",
                method="GET",
                url="/api/v1/dhcpv6-relay/vlans",
                category="dhcpv6_relay",
                module="dhcp",
                description="獲取所有VLAN的DHCPv6中繼配置"
            ),
            # ... 其他測試案例
        ]
    
    def get_dhcpv6_snooping_tests(self) -> List[APITestCase]:
        """DHCPv6 Snooping API 測試案例"""
        return [
            self.create_test_case(
                name="dhcpv6_snooping_get_config",
                method="GET",
                url="/api/v1/dhcpv6-snooping",
                category="dhcpv6_snooping",
                module="dhcp",
                description="獲取DHCPv6 Snooping全局配置"
            ),
            # ... 其他測試案例
        ]