#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IP Source Guard 模組測試案例
包含IP源保護配置、接口管理、綁定條目管理、IPv6源保護等相關API測試
支援接口過濾類型、學習模式、綁定表管理、靜態/動態綁定、阻塞條目清除等操作
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class IP_SOURCE_GUARDTests(BaseTests):
    """IP Source Guard 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取IP Source Guard模組支援的類別"""
        return [
            "ip_source_guard_interface_configuration",
            "ip_source_guard_binding_management",
            "ip_source_guard_blocked_entry_management",
            "ipv6_source_guard_interface_configuration",
            "ipv6_source_guard_binding_management",
            "ip_source_guard_advanced_operations",
            "ip_source_guard_error_handling"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有IP Source Guard測試案例"""
        all_tests = []
        all_tests.extend(self.get_ip_source_guard_interface_configuration_tests())
        all_tests.extend(self.get_ip_source_guard_binding_management_tests())
        all_tests.extend(self.get_ip_source_guard_blocked_entry_management_tests())
        all_tests.extend(self.get_ipv6_source_guard_interface_configuration_tests())
        all_tests.extend(self.get_ipv6_source_guard_binding_management_tests())
        all_tests.extend(self.get_ip_source_guard_advanced_operations_tests())
        all_tests.extend(self.get_ip_source_guard_error_handling_tests())
        return all_tests
    
    def get_ip_source_guard_interface_configuration_tests(self) -> List[APITestCase]:
        """IP Source Guard Interface Configuration API 測試案例"""
        return [
            # 獲取所有接口的IP源保護配置
            self.create_test_case(
                name="ip_source_guard_get_all_interfaces_configuration",
                method="GET",
                url="/api/v1/ip-source-guard/interfaces",
                category="ip_source_guard_interface_configuration",
                module="ip_source_guard",
                description="獲取所有接口的IP源保護配置"
            ),
            
            # 獲取特定接口的IP源保護配置 - eth1/1
            self.create_test_case(
                name="ip_source_guard_get_specific_interface_eth1_1",
                method="GET",
                url="/api/v1/ip-source-guard/interfaces/eth1%2f1",
                category="ip_source_guard_interface_configuration",
                module="ip_source_guard",
                description="獲取eth1/1接口的IP源保護配置"
            ),
            
            # 獲取特定接口的IP源保護配置 - eth1/5
            self.create_test_case(
                name="ip_source_guard_get_specific_interface_eth1_5",
                method="GET",
                url="/api/v1/ip-source-guard/interfaces/eth1%2f5",
                category="ip_source_guard_interface_configuration",
                module="ip_source_guard",
                description="獲取eth1/5接口的IP源保護配置"
            ),
            
            # 配置eth1/1接口 - MAC模式，SIP過濾
            self.create_test_case(
                name="ip_source_guard_configure_eth1_1_mac_mode_sip",
                method="PUT",
                url="/api/v1/ip-source-guard/interfaces/eth1%2f1",
                category="ip_source_guard_interface_configuration",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_eth1_1_mac_sip', {
                    "mode": "mac",
                    "filterType": "sip",
                    "macTableMaxBinding": 32,
                    "aclTableMaxBinding": 5
                }),
                description="配置eth1/1接口 - MAC模式，SIP過濾"
            ),
            
            # 配置eth1/2接口 - ACL模式，SIP-MAC過濾
            self.create_test_case(
                name="ip_source_guard_configure_eth1_2_acl_mode_sip_mac",
                method="PUT",
                url="/api/v1/ip-source-guard/interfaces/eth1%2f2",
                category="ip_source_guard_interface_configuration",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_eth1_2_acl_sip_mac', {
                    "mode": "acl",
                    "filterType": "sip-mac",
                    "macTableMaxBinding": 16,
                    "aclTableMaxBinding": 10
                }),
                description="配置eth1/2接口 - ACL模式，SIP-MAC過濾"
            ),
            
            # 配置eth1/5接口 - MAC模式，最大綁定數
            self.create_test_case(
                name="ip_source_guard_configure_eth1_5_mac_mode_max_binding",
                method="PUT",
                url="/api/v1/ip-source-guard/interfaces/eth1%2f5",
                category="ip_source_guard_interface_configuration",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_eth1_5_mac_max_binding', {
                    "mode": "mac",
                    "filterType": "sip",
                    "macTableMaxBinding": 228,
                    "aclTableMaxBinding": 5
                }),
                description="配置eth1/5接口 - MAC模式，最大綁定數"
            ),
            
            # 配置eth1/10接口 - ACL模式，最大綁定數
            self.create_test_case(
                name="ip_source_guard_configure_eth1_10_acl_mode_max_binding",
                method="PUT",
                url="/api/v1/ip-source-guard/interfaces/eth1%2f10",
                category="ip_source_guard_interface_configuration",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_eth1_10_acl_max_binding', {
                    "mode": "acl",
                    "filterType": "sip-mac",
                    "macTableMaxBinding": 16,
                    "aclTableMaxBinding": 16
                }),
                description="配置eth1/10接口 - ACL模式，最大綁定數"
            ),
            
            # 禁用eth1/15接口的IP源保護
            self.create_test_case(
                name="ip_source_guard_disable_eth1_15",
                method="PUT",
                url="/api/v1/ip-source-guard/interfaces/eth1%2f15",
                category="ip_source_guard_interface_configuration",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_eth1_15_disable', {
                    "filterType": "none"
                }),
                description="禁用eth1/15接口的IP源保護"
            ),
            
            # 配置trunk1接口 - MAC模式
            self.create_test_case(
                name="ip_source_guard_configure_trunk1_mac_mode",
                method="PUT",
                url="/api/v1/ip-source-guard/interfaces/trunk1",
                category="ip_source_guard_interface_configuration",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_trunk1_mac', {
                    "mode": "mac",
                    "filterType": "sip",
                    "macTableMaxBinding": 64,
                    "aclTableMaxBinding": 5
                }),
                description="配置trunk1接口 - MAC模式"
            ),
            
            # 驗證接口配置更新
            self.create_test_case(
                name="ip_source_guard_verify_interface_configuration_update",
                method="GET",
                url="/api/v1/ip-source-guard/interfaces",
                category="ip_source_guard_interface_configuration",
                module="ip_source_guard",
                description="驗證接口配置更新"
            )
        ]
    
    def get_ip_source_guard_binding_management_tests(self) -> List[APITestCase]:
        """IP Source Guard Binding Management API 測試案例"""
        return [
            # 獲取所有IP源保護綁定條目
            self.create_test_case(
                name="ip_source_guard_get_all_bindings",
                method="GET",
                url="/api/v1/ip-source-guard/bindings",
                category="ip_source_guard_binding_management",
                module="ip_source_guard",
                description="獲取所有IP源保護綁定條目"
            ),
            
            # 獲取靜態MAC綁定條目
            self.create_test_case(
                name="ip_source_guard_get_static_mac_bindings",
                method="GET",
                url="/api/v1/ip-source-guard/bindings?type=static-mac",
                category="ip_source_guard_binding_management",
                module="ip_source_guard",
                description="獲取靜態MAC綁定條目"
            ),
            
            # 獲取靜態ACL綁定條目
            self.create_test_case(
                name="ip_source_guard_get_static_acl_bindings",
                method="GET",
                url="/api/v1/ip-source-guard/bindings?type=static-acl",
                category="ip_source_guard_binding_management",
                module="ip_source_guard",
                description="獲取靜態ACL綁定條目"
            ),
            
            # 獲取動態綁定條目
            self.create_test_case(
                name="ip_source_guard_get_dynamic_bindings",
                method="GET",
                url="/api/v1/ip-source-guard/bindings?type=dynamic",
                category="ip_source_guard_binding_management",
                module="ip_source_guard",
                description="獲取動態綁定條目"
            ),
            
            # 獲取阻塞綁定條目
            self.create_test_case(
                name="ip_source_guard_get_blocked_bindings",
                method="GET",
                url="/api/v1/ip-source-guard/bindings?type=blocked",
                category="ip_source_guard_binding_management",
                module="ip_source_guard",
                description="獲取阻塞綁定條目"
            ),
            
            # 創建靜態MAC綁定條目
            self.create_test_case(
                name="ip_source_guard_create_static_mac_binding",
                method="POST",
                url="/api/v1/ip-source-guard/bindings",
                category="ip_source_guard_binding_management",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_static_mac_binding', {
                    "type": "static-mac",
                    "macAddress": "12-34-00-11-11-11",
                    "vlanId": 1,
                    "ipAddress": "192.168.1.12",
                    "ifId": "eth1/5"
                }),
                description="創建靜態MAC綁定條目"
            ),
            
            # 創建靜態ACL綁定條目
            self.create_test_case(
                name="ip_source_guard_create_static_acl_binding",
                method="POST",
                url="/api/v1/ip-source-guard/bindings",
                category="ip_source_guard_binding_management",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_static_acl_binding', {
                    "type": "static-acl",
                    "macAddress": "00-00-00-22-22-22",
                    "vlanId": 3,
                    "ipAddress": "192.168.3.15",
                    "ifId": "eth1/7"
                }),
                description="創建靜態ACL綁定條目"
            ),
            
            # 創建企業級靜態綁定條目
            self.create_test_case(
                name="ip_source_guard_create_enterprise_static_binding",
                method="POST",
                url="/api/v1/ip-source-guard/bindings",
                category="ip_source_guard_binding_management",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_enterprise_static_binding', {
                    "type": "static-mac",
                    "macAddress": "aa-bb-cc-dd-ee-ff",
                    "vlanId": 100,
                    "ipAddress": "10.1.1.50",
                    "ifId": "eth1/1"
                }),
                description="創建企業級靜態綁定條目"
            ),
            
            # 創建數據中心靜態綁定條目
            self.create_test_case(
                name="ip_source_guard_create_datacenter_static_binding",
                method="POST",
                url="/api/v1/ip-source-guard/bindings",
                category="ip_source_guard_binding_management",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_datacenter_static_binding', {
                    "type": "static-acl",
                    "macAddress": "11-22-33-44-55-66",
                    "vlanId": 200,
                    "ipAddress": "172.16.1.100",
                    "ifId": "eth1/2"
                }),
                description="創建數據中心靜態綁定條目"
            ),
            
            # 獲取特定綁定條目 - 靜態MAC
            self.create_test_case(
                name="ip_source_guard_get_specific_static_mac_binding",
                method="GET",
                url="/api/v1/ip-source-guard/bindings/types/static-mac/mac-addresses/12-34-00-11-11-11/ip-addresses/192.168.1.12",
                category="ip_source_guard_binding_management",
                module="ip_source_guard",
                description="獲取特定靜態MAC綁定條目"
            ),
            
            # 獲取特定綁定條目 - 靜態ACL
            self.create_test_case(
                name="ip_source_guard_get_specific_static_acl_binding",
                method="GET",
                url="/api/v1/ip-source-guard/bindings/types/static-acl/mac-addresses/00-00-00-22-22-22/ip-addresses/192.168.3.15",
                category="ip_source_guard_binding_management",
                module="ip_source_guard",
                description="獲取特定靜態ACL綁定條目"
            ),
            
            # 刪除靜態MAC綁定條目
            self.create_test_case(
                name="ip_source_guard_delete_static_mac_binding",
                method="DELETE",
                url="/api/v1/ip-source-guard/bindings/types/static-mac/mac-addresses/12-34-00-11-11-11/ip-addresses/192.168.1.12",
                category="ip_source_guard_binding_management",
                module="ip_source_guard",
                description="刪除靜態MAC綁定條目"
            ),
            
            # 刪除靜態ACL綁定條目
            self.create_test_case(
                name="ip_source_guard_delete_static_acl_binding",
                method="DELETE",
                url="/api/v1/ip-source-guard/bindings/types/static-acl/mac-addresses/00-00-00-22-22-22/ip-addresses/192.168.3.15",
                category="ip_source_guard_binding_management",
                module="ip_source_guard",
                description="刪除靜態ACL綁定條目"
            ),
            
            # 驗證綁定條目管理結果
            self.create_test_case(
                name="ip_source_guard_verify_binding_management_results",
                method="GET",
                url="/api/v1/ip-source-guard/bindings",
                category="ip_source_guard_binding_management",
                module="ip_source_guard",
                description="驗證綁定條目管理結果"
            )
        ]
    
    def get_ip_source_guard_blocked_entry_management_tests(self) -> List[APITestCase]:
        """IP Source Guard Blocked Entry Management API 測試案例"""
        return [
            # 清除IP源保護阻塞條目
            self.create_test_case(
                name="ip_source_guard_clear_blocked_entries",
                method="PUT",
                url="/api/v1/ip-source-guard/bindings:clear-blocked",
                category="ip_source_guard_blocked_entry_management",
                module="ip_source_guard",
                description="清除IP源保護阻塞條目"
            ),
            
            # 驗證阻塞條目清除結果
            self.create_test_case(
                name="ip_source_guard_verify_blocked_entries_cleared",
                method="GET",
                url="/api/v1/ip-source-guard/bindings?type=blocked",
                category="ip_source_guard_blocked_entry_management",
                module="ip_source_guard",
                description="驗證阻塞條目清除結果"
            ),
            
            # 再次清除阻塞條目（確保操作冪等性）
            self.create_test_case(
                name="ip_source_guard_clear_blocked_entries_idempotent",
                method="PUT",
                url="/api/v1/ip-source-guard/bindings:clear-blocked",
                category="ip_source_guard_blocked_entry_management",
                module="ip_source_guard",
                description="再次清除阻塞條目（確保操作冪等性）"
            )
        ]
    
    def get_ipv6_source_guard_interface_configuration_tests(self) -> List[APITestCase]:
        """IPv6 Source Guard Interface Configuration API 測試案例"""
        return [
            # 獲取所有接口的IPv6源保護配置
            self.create_test_case(
                name="ipv6_source_guard_get_all_interfaces_configuration",
                method="GET",
                url="/api/v1/ipv6-source-guard/interfaces",
                category="ipv6_source_guard_interface_configuration",
                module="ip_source_guard",
                description="獲取所有接口的IPv6源保護配置"
            ),
            
            # 獲取特定接口的IPv6源保護配置 - eth1/1
            self.create_test_case(
                name="ipv6_source_guard_get_specific_interface_eth1_1",
                method="GET",
                url="/api/v1/ipv6-source-guard/interfaces/eth1%2f1",
                category="ipv6_source_guard_interface_configuration",
                module="ip_source_guard",
                description="獲取eth1/1接口的IPv6源保護配置"
            ),
            
            # 獲取特定接口的IPv6源保護配置 - eth1/5
            self.create_test_case(
                name="ipv6_source_guard_get_specific_interface_eth1_5",
                method="GET",
                url="/api/v1/ipv6-source-guard/interfaces/eth1%2f5",
                category="ipv6_source_guard_interface_configuration",
                module="ip_source_guard",
                description="獲取eth1/5接口的IPv6源保護配置"
            ),
            
            # 配置eth1/1接口 - 啟用SIP過濾
            self.create_test_case(
                name="ipv6_source_guard_configure_eth1_1_sip_filter",
                method="PUT",
                url="/api/v1/ipv6-source-guard/interfaces/eth1%2f1",
                category="ipv6_source_guard_interface_configuration",
                module="ip_source_guard",
                body=self.test_data.get('ipv6_source_guard_eth1_1_sip', {
                    "filterType": "sip",
                    "maxBinding": 3
                }),
                description="配置eth1/1接口 - 啟用SIP過濾"
            ),
            
            # 配置eth1/5接口 - 最大綁定數
            self.create_test_case(
                name="ipv6_source_guard_configure_eth1_5_max_binding",
                method="PUT",
                url="/api/v1/ipv6-source-guard/interfaces/eth1%2f5",
                category="ipv6_source_guard_interface_configuration",
                module="ip_source_guard",
                body=self.test_data.get('ipv6_source_guard_eth1_5_max_binding', {
                    "filterType": "sip",
                    "maxBinding": 5
                }),
                description="配置eth1/5接口 - 最大綁定數"
            ),
            
            # 配置eth1/10接口 - 中等綁定數
            self.create_test_case(
                name="ipv6_source_guard_configure_eth1_10_medium_binding",
                method="PUT",
                url="/api/v1/ipv6-source-guard/interfaces/eth1%2f10",
                category="ipv6_source_guard_interface_configuration",
                module="ip_source_guard",
                body=self.test_data.get('ipv6_source_guard_eth1_10_medium_binding', {
                    "filterType": "sip",
                    "maxBinding": 3
                }),
                description="配置eth1/10接口 - 中等綁定數"
            ),
            
            # 禁用eth1/15接口的IPv6源保護
            self.create_test_case(
                name="ipv6_source_guard_disable_eth1_15",
                method="PUT",
                url="/api/v1/ipv6-source-guard/interfaces/eth1%2f15",
                category="ipv6_source_guard_interface_configuration",
                module="ip_source_guard",
                body=self.test_data.get('ipv6_source_guard_eth1_15_disable', {
                    "filterType": "none"
                }),
                description="禁用eth1/15接口的IPv6源保護"
            ),
            
            # 驗證IPv6接口配置更新
            self.create_test_case(
                name="ipv6_source_guard_verify_interface_configuration_update",
                method="GET",
                url="/api/v1/ipv6-source-guard/interfaces",
                category="ipv6_source_guard_interface_configuration",
                module="ip_source_guard",
                description="驗證IPv6接口配置更新"
            )
        ]
    
    def get_ipv6_source_guard_binding_management_tests(self) -> List[APITestCase]:
        """IPv6 Source Guard Binding Management API 測試案例"""
        return [
            # 獲取所有IPv6源保護綁定條目
            self.create_test_case(
                name="ipv6_source_guard_get_all_bindings",
                method="GET",
                url="/api/v1/ipv6-source-guard/bindings",
                category="ipv6_source_guard_binding_management",
                module="ip_source_guard",
                description="獲取所有IPv6源保護綁定條目"
            ),
            
            # 獲取靜態IPv6綁定條目
            self.create_test_case(
                name="ipv6_source_guard_get_static_bindings",
                method="GET",
                url="/api/v1/ipv6-source-guard/bindings?type=static",
                category="ipv6_source_guard_binding_management",
                module="ip_source_guard",
                description="獲取靜態IPv6綁定條目"
            ),
            
            # 獲取動態IPv6綁定條目
            self.create_test_case(
                name="ipv6_source_guard_get_dynamic_bindings",
                method="GET",
                url="/api/v1/ipv6-source-guard/bindings?type=dynamic",
                category="ipv6_source_guard_binding_management",
                module="ip_source_guard",
                description="獲取動態IPv6綁定條目"
            ),
            
            # 創建IPv6靜態綁定條目
            self.create_test_case(
                name="ipv6_source_guard_create_static_binding",
                method="POST",
                url="/api/v1/ipv6-source-guard/bindings",
                category="ipv6_source_guard_binding_management",
                module="ip_source_guard",
                body=self.test_data.get('ipv6_source_guard_static_binding', {
                    "macAddress": "66-66-00-11-11-11",
                    "vlanId": 1,
                    "ipv6Address": "2001::1",
                    "ifId": "eth1/1"
                }),
                description="創建IPv6靜態綁定條目"
            ),
            
            # 創建企業級IPv6靜態綁定條目
            self.create_test_case(
                name="ipv6_source_guard_create_enterprise_static_binding",
                method="POST",
                url="/api/v1/ipv6-source-guard/bindings",
                category="ipv6_source_guard_binding_management",
                module="ip_source_guard",
                body=self.test_data.get('ipv6_source_guard_enterprise_static_binding', {
                    "macAddress": "aa-bb-cc-11-22-33",
                    "vlanId": 100,
                    "ipv6Address": "2001:db8::100",
                    "ifId": "eth1/5"
                }),
                description="創建企業級IPv6靜態綁定條目"
            ),
            
            # 創建數據中心IPv6靜態綁定條目
            self.create_test_case(
                name="ipv6_source_guard_create_datacenter_static_binding",
                method="POST",
                url="/api/v1/ipv6-source-guard/bindings",
                category="ipv6_source_guard_binding_management",
                module="ip_source_guard",
                body=self.test_data.get('ipv6_source_guard_datacenter_static_binding', {
                    "macAddress": "dd-ee-ff-44-55-66",
                    "vlanId": 200,
                    "ipv6Address": "fd00::200:1",
                    "ifId": "eth1/10"
                }),
                description="創建數據中心IPv6靜態綁定條目"
            ),
            
            # 獲取特定IPv6綁定條目
            self.create_test_case(
                name="ipv6_source_guard_get_specific_binding",
                method="GET",
                url="/api/v1/ipv6-source-guard/bindings/mac-addresses/66-66-00-11-11-11/ipv6-addresses/2001::1",
                category="ipv6_source_guard_binding_management",
                module="ip_source_guard",
                description="獲取特定IPv6綁定條目"
            ),
            
            # 獲取企業級IPv6綁定條目
            self.create_test_case(
                name="ipv6_source_guard_get_enterprise_binding",
                method="GET",
                url="/api/v1/ipv6-source-guard/bindings/mac-addresses/aa-bb-cc-11-22-33/ipv6-addresses/2001:db8::100",
                category="ipv6_source_guard_binding_management",
                module="ip_source_guard",
                description="獲取企業級IPv6綁定條目"
            ),
            
            # 刪除IPv6靜態綁定條目
            self.create_test_case(
                name="ipv6_source_guard_delete_static_binding",
                method="DELETE",
                url="/api/v1/ipv6-source-guard/bindings/mac-addresses/66-66-00-11-11-11/ipv6-addresses/2001::1",
                category="ipv6_source_guard_binding_management",
                module="ip_source_guard",
                description="刪除IPv6靜態綁定條目"
            ),
            
            # 刪除企業級IPv6靜態綁定條目
            self.create_test_case(
                name="ipv6_source_guard_delete_enterprise_static_binding",
                method="DELETE",
                url="/api/v1/ipv6-source-guard/bindings/mac-addresses/aa-bb-cc-11-22-33/ipv6-addresses/2001:db8::100",
                category="ipv6_source_guard_binding_management",
                module="ip_source_guard",
                description="刪除企業級IPv6靜態綁定條目"
            ),
            
            # 驗證IPv6綁定條目管理結果
            self.create_test_case(
                name="ipv6_source_guard_verify_binding_management_results",
                method="GET",
                url="/api/v1/ipv6-source-guard/bindings",
                category="ipv6_source_guard_binding_management",
                module="ip_source_guard",
                description="驗證IPv6綁定條目管理結果"
            )
        ]
    
    def get_ip_source_guard_advanced_operations_tests(self) -> List[APITestCase]:
        """IP Source Guard Advanced Operations API 測試案例"""
        return [
            # 配置企業級IP源保護環境
            self.create_test_case(
                name="ip_source_guard_configure_enterprise_environment",
                method="PUT",
                url="/api/v1/ip-source-guard/interfaces/eth1%2f20",
                category="ip_source_guard_advanced_operations",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_enterprise_config', {
                    "mode": "mac",
                    "filterType": "sip-mac",
                    "macTableMaxBinding": 128,
                    "aclTableMaxBinding": 10
                }),
                description="配置企業級IP源保護環境"
            ),
            
            # 批量配置多個接口 - eth1/21
            self.create_test_case(
                name="ip_source_guard_batch_configure_eth1_21",
                method="PUT",
                url="/api/v1/ip-source-guard/interfaces/eth1%2f21",
                category="ip_source_guard_advanced_operations",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_batch_eth1_21', {
                    "mode": "acl",
                    "filterType": "sip",
                    "macTableMaxBinding": 16,
                    "aclTableMaxBinding": 8
                }),
                description="批量配置接口 - eth1/21"
            ),
            
            # 批量配置多個接口 - eth1/22
            self.create_test_case(
                name="ip_source_guard_batch_configure_eth1_22",
                method="PUT",
                url="/api/v1/ip-source-guard/interfaces/eth1%2f22",
                category="ip_source_guard_advanced_operations",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_batch_eth1_22', {
                    "mode": "mac",
                    "filterType": "sip",
                    "macTableMaxBinding": 64,
                    "aclTableMaxBinding": 5
                }),
                description="批量配置接口 - eth1/22"
            ),
            
            # 批量創建靜態綁定條目 - 條目1
            self.create_test_case(
                name="ip_source_guard_batch_create_binding_1",
                method="POST",
                url="/api/v1/ip-source-guard/bindings",
                category="ip_source_guard_advanced_operations",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_batch_binding_1', {
                    "type": "static-mac",
                    "macAddress": "aa-aa-aa-11-11-11",
                    "vlanId": 10,
                    "ipAddress": "10.0.10.100",
                    "ifId": "eth1/20"
                }),
                description="批量創建靜態綁定條目 - 條目1"
            ),
            
            # 批量創建靜態綁定條目 - 條目2
            self.create_test_case(
                name="ip_source_guard_batch_create_binding_2",
                method="POST",
                url="/api/v1/ip-source-guard/bindings",
                category="ip_source_guard_advanced_operations",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_batch_binding_2', {
                    "type": "static-acl",
                    "macAddress": "bb-bb-bb-22-22-22",
                    "vlanId": 20,
                    "ipAddress": "10.0.20.100",
                    "ifId": "eth1/21"
                }),
                description="批量創建靜態綁定條目 - 條目2"
            ),
            
            # 批量創建靜態綁定條目 - 條目3
            self.create_test_case(
                name="ip_source_guard_batch_create_binding_3",
                method="POST",
                url="/api/v1/ip-source-guard/bindings",
                category="ip_source_guard_advanced_operations",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_batch_binding_3', {
                    "type": "static-mac",
                    "macAddress": "cc-cc-cc-33-33-33",
                    "vlanId": 30,
                    "ipAddress": "10.0.30.100",
                    "ifId": "eth1/22"
                }),
                description="批量創建靜態綁定條目 - 條目3"
            ),
            
            # 配置高安全性IP源保護策略
            self.create_test_case(
                name="ip_source_guard_configure_high_security_policy",
                method="PUT",
                url="/api/v1/ip-source-guard/interfaces/eth1%2f25",
                category="ip_source_guard_advanced_operations",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_high_security_policy', {
                    "mode": "acl",
                    "filterType": "sip-mac",
                    "macTableMaxBinding": 16,
                    "aclTableMaxBinding": 16
                }),
                description="配置高安全性IP源保護策略"
            ),
            
            # 配置IPv6高級源保護
            self.create_test_case(
                name="ipv6_source_guard_configure_advanced_protection",
                method="PUT",
                url="/api/v1/ipv6-source-guard/interfaces/eth1%2f30",
                category="ip_source_guard_advanced_operations",
                module="ip_source_guard",
                body=self.test_data.get('ipv6_source_guard_advanced_protection', {
                    "filterType": "sip",
                    "maxBinding": 5
                }),
                description="配置IPv6高級源保護"
            ),
            
            # 動態調整源保護參數
            self.create_test_case(
                name="ip_source_guard_dynamic_adjust_parameters",
                method="PUT",
                url="/api/v1/ip-source-guard/interfaces/eth1%2f35",
                category="ip_source_guard_advanced_operations",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_dynamic_parameters', {
                    "mode": "mac",
                    "filterType": "sip",
                    "macTableMaxBinding": 100,
                    "aclTableMaxBinding": 5
                }),
                description="動態調整源保護參數"
            ),
            
            # 驗證高級操作結果
            self.create_test_case(
                name="ip_source_guard_verify_advanced_operations_results",
                method="GET",
                url="/api/v1/ip-source-guard/interfaces",
                category="ip_source_guard_advanced_operations",
                module="ip_source_guard",
                description="驗證高級操作結果"
            ),
            
            # 驗證綁定條目高級配置結果
            self.create_test_case(
                name="ip_source_guard_verify_binding_advanced_results",
                method="GET",
                url="/api/v1/ip-source-guard/bindings",
                category="ip_source_guard_advanced_operations",
                module="ip_source_guard",
                description="驗證綁定條目高級配置結果"
            )
        ]
    
    def get_ip_source_guard_error_handling_tests(self) -> List[APITestCase]:
        """IP Source Guard Error Handling API 測試案例"""
        return [
            # 測試無效的接口ID格式
            self.create_test_case(
                name="ip_source_guard_test_invalid_interface_id_format",
                method="GET",
                url="/api/v1/ip-source-guard/interfaces/invalid_interface",
                category="ip_source_guard_error_handling",
                module="ip_source_guard",
                expected_status=400,
                description="測試無效的接口ID格式"
            ),
            
            # 測試超出範圍的接口ID
            self.create_test_case(
                name="ip_source_guard_test_out_of_range_interface_id",
                method="GET",
                url="/api/v1/ip-source-guard/interfaces/eth9%2f99",
                category="ip_source_guard_error_handling",
                module="ip_source_guard",
                expected_status=400,
                description="測試超出範圍的接口ID"
            ),
            
            # 測試無效的學習模式
            self.create_test_case(
                name="ip_source_guard_test_invalid_learning_mode",
                method="PUT",
                url="/api/v1/ip-source-guard/interfaces/eth1%2f1",
                category="ip_source_guard_error_handling",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_invalid_mode', {
                    "mode": "invalid_mode"
                }),
                expected_status=400,
                description="測試無效的學習模式 (非mac/acl)"
            ),
            
            # 測試無效的過濾類型
            self.create_test_case(
                name="ip_source_guard_test_invalid_filter_type",
                method="PUT",
                url="/api/v1/ip-source-guard/interfaces/eth1%2f1",
                category="ip_source_guard_error_handling",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_invalid_filter_type', {
                    "filterType": "invalid_filter"
                }),
                expected_status=400,
                description="測試無效的過濾類型 (非none/sip/sip-mac)"
            ),
            
            # 測試無效的MAC表最大綁定數 - 超出範圍
            self.create_test_case(
                name="ip_source_guard_test_invalid_mac_table_max_binding_out_of_range",
                method="PUT",
                url="/api/v1/ip-source-guard/interfaces/eth1%2f1",
                category="ip_source_guard_error_handling",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_invalid_mac_table_max_binding', {
                    "mode": "mac",
                    "macTableMaxBinding": 300  # 超出範圍 (1-228)
                }),
                expected_status=400,
                description="測試無效的MAC表最大綁定數 - 超出範圍 (>228)"
            ),
            
            # 測試無效的ACL表最大綁定數 - 超出範圍
            self.create_test_case(
                name="ip_source_guard_test_invalid_acl_table_max_binding_out_of_range",
                method="PUT",
                url="/api/v1/ip-source-guard/interfaces/eth1%2f1",
                category="ip_source_guard_error_handling",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_invalid_acl_table_max_binding', {
                    "mode": "acl",
                    "aclTableMaxBinding": 20  # 超出範圍 (1-16)
                }),
                expected_status=400,
                description="測試無效的ACL表最大綁定數 - 超出範圍 (>16)"
            ),
            
            # 測試無效的VLAN ID - 超出範圍
            self.create_test_case(
                name="ip_source_guard_test_invalid_vlan_id_out_of_range",
                method="POST",
                url="/api/v1/ip-source-guard/bindings",
                category="ip_source_guard_error_handling",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_invalid_vlan_id', {
                    "type": "static-mac",
                    "macAddress": "00-00-00-11-11-11",
                    "vlanId": 5000,  # 超出範圍 (1-4094)
                    "ipAddress": "192.168.1.1",
                    "ifId": "eth1/1"
                }),
                expected_status=400,
                description="測試無效的VLAN ID - 超出範圍 (>4094)"
            ),
            
            # 測試無效的MAC地址格式
            self.create_test_case(
                name="ip_source_guard_test_invalid_mac_address_format",
                method="POST",
                url="/api/v1/ip-source-guard/bindings",
                category="ip_source_guard_error_handling",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_invalid_mac_address', {
                    "type": "static-mac",
                    "macAddress": "invalid-mac-address",
                    "vlanId": 1,
                    "ipAddress": "192.168.1.1",
                    "ifId": "eth1/1"
                }),
                expected_status=400,
                description="測試無效的MAC地址格式"
            ),
            
            # 測試無效的IP地址格式
            self.create_test_case(
                name="ip_source_guard_test_invalid_ip_address_format",
                method="POST",
                url="/api/v1/ip-source-guard/bindings",
                category="ip_source_guard_error_handling",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_invalid_ip_address', {
                    "type": "static-mac",
                    "macAddress": "00-00-00-11-11-11",
                    "vlanId": 1,
                    "ipAddress": "invalid.ip.address",
                    "ifId": "eth1/1"
                }),
                expected_status=400,
                description="測試無效的IP地址格式"
            ),
            
            # 測試無效的綁定類型
            self.create_test_case(
                name="ip_source_guard_test_invalid_binding_type",
                method="POST",
                url="/api/v1/ip-source-guard/bindings",
                category="ip_source_guard_error_handling",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_invalid_binding_type', {
                    "type": "invalid-type",
                    "macAddress": "00-00-00-11-11-11",
                    "vlanId": 1,
                    "ipAddress": "192.168.1.1",
                    "ifId": "eth1/1"
                }),
                expected_status=400,
                description="測試無效的綁定類型 (非static-mac/static-acl)"
            ),
            
            # 測試IPv6無效的過濾類型
            self.create_test_case(
                name="ipv6_source_guard_test_invalid_filter_type",
                method="PUT",
                url="/api/v1/ipv6-source-guard/interfaces/eth1%2f1",
                category="ip_source_guard_error_handling",
                module="ip_source_guard",
                body=self.test_data.get('ipv6_source_guard_invalid_filter_type', {
                    "filterType": "invalid_filter"
                }),
                expected_status=400,
                description="測試IPv6無效的過濾類型 (非none/sip)"
            ),
            
            # 測試IPv6無效的最大綁定數 - 超出範圍
            self.create_test_case(
                name="ipv6_source_guard_test_invalid_max_binding_out_of_range",
                method="PUT",
                url="/api/v1/ipv6-source-guard/interfaces/eth1%2f1",
                category="ip_source_guard_error_handling",
                module="ip_source_guard",
                body=self.test_data.get('ipv6_source_guard_invalid_max_binding', {
                    "filterType": "sip",
                    "maxBinding": 10  # 超出範圍 (1-5)
                }),
                expected_status=400,
                description="測試IPv6無效的最大綁定數 - 超出範圍 (>5)"
            ),
            
            # 測試IPv6無效的IPv6地址格式
            self.create_test_case(
                name="ipv6_source_guard_test_invalid_ipv6_address_format",
                method="POST",
                url="/api/v1/ipv6-source-guard/bindings",
                category="ip_source_guard_error_handling",
                module="ip_source_guard",
                body=self.test_data.get('ipv6_source_guard_invalid_ipv6_address', {
                    "macAddress": "00-00-00-11-11-11",
                    "vlanId": 1,
                    "ipv6Address": "invalid::ipv6::address",
                    "ifId": "eth1/1"
                }),
                expected_status=400,
                description="測試IPv6無效的IPv6地址格式"
            ),
            
            # 測試無效JSON格式 - IP源保護接口配置
            self.create_test_case(
                name="ip_source_guard_test_invalid_json_interface_config",
                method="PUT",
                url="/api/v1/ip-source-guard/interfaces/eth1%2f1",
                category="ip_source_guard_error_handling",
                module="ip_source_guard",
                body="invalid json format",
                expected_status=400,
                description="測試無效JSON格式 - IP源保護接口配置"
            ),
            
            # 測試無效JSON格式 - 綁定條目創建
            self.create_test_case(
                name="ip_source_guard_test_invalid_json_binding_creation",
                method="POST",
                url="/api/v1/ip-source-guard/bindings",
                category="ip_source_guard_error_handling",
                module="ip_source_guard",
                body="{ invalid json }",
                expected_status=400,
                description="測試無效JSON格式 - 綁定條目創建"
            ),
            
            # 恢復正常IP源保護配置
            self.create_test_case(
                name="ip_source_guard_restore_normal_configuration",
                method="PUT",
                url="/api/v1/ip-source-guard/interfaces/eth1%2f1",
                category="ip_source_guard_error_handling",
                module="ip_source_guard",
                body=self.test_data.get('ip_source_guard_restore_normal_config', {
                    "mode": "acl",
                    "filterType": "none",
                    "macTableMaxBinding": 16,
                    "aclTableMaxBinding": 5
                }),
                description="恢復正常IP源保護配置"
            ),
            
            # 最終IP源保護狀態檢查
            self.create_test_case(
                name="ip_source_guard_final_status_check",
                method="GET",
                url="/api/v1/ip-source-guard/interfaces",
                category="ip_source_guard_error_handling",
                module="ip_source_guard",
                description="最終IP源保護狀態檢查"
            )
        ]