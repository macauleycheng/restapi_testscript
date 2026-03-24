#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ND Snoop 模組測試案例
包含IPv6鄰居發現監聽配置、VLAN管理、接口管理、綁定表管理、前綴表管理等相關API測試
支援ND Snoop全局配置、VLAN級別配置、接口信任狀態、動態綁定表、前綴表清除等操作
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class ND_SNOOPTests(BaseTests):
    """ND Snoop 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取ND Snoop模組支援的類別"""
        return [
            "nd_snoop_global_configuration",
            "nd_snoop_vlan_management",
            "nd_snoop_interface_management",
            "nd_snoop_binding_table_management",
            "nd_snoop_prefix_table_management",
            "nd_snoop_advanced_operations",
            "nd_snoop_error_handling"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有ND Snoop測試案例"""
        all_tests = []
        all_tests.extend(self.get_nd_snoop_global_configuration_tests())
        all_tests.extend(self.get_nd_snoop_vlan_management_tests())
        all_tests.extend(self.get_nd_snoop_interface_management_tests())
        all_tests.extend(self.get_nd_snoop_binding_table_management_tests())
        all_tests.extend(self.get_nd_snoop_prefix_table_management_tests())
        all_tests.extend(self.get_nd_snoop_advanced_operations_tests())
        all_tests.extend(self.get_nd_snoop_error_handling_tests())
        return all_tests
    
    def get_nd_snoop_global_configuration_tests(self) -> List[APITestCase]:
        """ND Snoop Global Configuration API 測試案例"""
        return [
            # 獲取ND Snoop全局配置
            self.create_test_case(
                name="nd_snoop_get_global_configuration",
                method="GET",
                url="/api/v1/nd-snoop",
                category="nd_snoop_global_configuration",
                module="nd_snoop",
                description="獲取ND Snoop全局配置"
            ),
            
            # 設置ND Snoop全局配置 - 啟用基本功能
            self.create_test_case(
                name="nd_snoop_set_global_configuration_enable_basic",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_global_configuration",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_global_enable_basic', {
                    "ndSnoopEnable": True,
                    "ndSnoopAutodetect": True,
                    "ndSnoopPrefixTimeout": 200,
                    "ndSnoopRetransmitCount": 5,
                    "ndSnoopRetransmitInterval": 5
                }),
                description="設置ND Snoop全局配置 - 啟用基本功能"
            ),
            
            # 設置ND Snoop全局配置 - 企業級配置
            self.create_test_case(
                name="nd_snoop_set_global_configuration_enterprise",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_global_configuration",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_global_enterprise', {
                    "ndSnoopEnable": True,
                    "ndSnoopAutodetect": True,
                    "ndSnoopPrefixTimeout": 600,
                    "ndSnoopRetransmitCount": 3,
                    "ndSnoopRetransmitInterval": 3
                }),
                description="設置ND Snoop全局配置 - 企業級配置"
            ),
            
            # 設置ND Snoop全局配置 - 數據中心配置
            self.create_test_case(
                name="nd_snoop_set_global_configuration_datacenter",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_global_configuration",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_global_datacenter', {
                    "ndSnoopEnable": True,
                    "ndSnoopAutodetect": False,
                    "ndSnoopPrefixTimeout": 1800,
                    "ndSnoopRetransmitCount": 5,
                    "ndSnoopRetransmitInterval": 10
                }),
                description="設置ND Snoop全局配置 - 數據中心配置"
            ),
            
            # 設置ND Snoop全局配置 - 最小超時配置
            self.create_test_case(
                name="nd_snoop_set_global_configuration_min_timeout",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_global_configuration",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_global_min_timeout', {
                    "ndSnoopEnable": True,
                    "ndSnoopAutodetect": True,
                    "ndSnoopPrefixTimeout": 3,
                    "ndSnoopRetransmitCount": 1,
                    "ndSnoopRetransmitInterval": 1
                }),
                description="設置ND Snoop全局配置 - 最小超時配置"
            ),
            
            # 設置ND Snoop全局配置 - 最大超時配置
            self.create_test_case(
                name="nd_snoop_set_global_configuration_max_timeout",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_global_configuration",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_global_max_timeout', {
                    "ndSnoopEnable": True,
                    "ndSnoopAutodetect": True,
                    "ndSnoopPrefixTimeout": 1800,
                    "ndSnoopRetransmitCount": 5,
                    "ndSnoopRetransmitInterval": 10
                }),
                description="設置ND Snoop全局配置 - 最大超時配置"
            ),
            
            # 禁用ND Snoop全局功能
            self.create_test_case(
                name="nd_snoop_disable_global_configuration",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_global_configuration",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_global_disable', {
                    "ndSnoopEnable": False,
                    "ndSnoopAutodetect": False
                }),
                description="禁用ND Snoop全局功能"
            ),
            
            # 重新啟用ND Snoop全局功能
            self.create_test_case(
                name="nd_snoop_re_enable_global_configuration",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_global_configuration",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_global_re_enable', {
                    "ndSnoopEnable": True,
                    "ndSnoopAutodetect": True,
                    "ndSnoopPrefixTimeout": 200,
                    "ndSnoopRetransmitCount": 5,
                    "ndSnoopRetransmitInterval": 5
                }),
                description="重新啟用ND Snoop全局功能"
            ),
            
            # 驗證ND Snoop全局配置更新
            self.create_test_case(
                name="nd_snoop_verify_global_configuration_update",
                method="GET",
                url="/api/v1/nd-snoop",
                category="nd_snoop_global_configuration",
                module="nd_snoop",
                description="驗證ND Snoop全局配置更新"
            )
        ]
    
    def get_nd_snoop_vlan_management_tests(self) -> List[APITestCase]:
        """ND Snoop VLAN Management API 測試案例"""
        return [
            # 獲取VLAN 1的ND Snoop狀態
            self.create_test_case(
                name="nd_snoop_get_vlan_1_status",
                method="GET",
                url="/api/v1/nd-snoop/vlans/1",
                category="nd_snoop_vlan_management",
                module="nd_snoop",
                description="獲取VLAN 1的ND Snoop狀態"
            ),
            
            # 獲取VLAN 100的ND Snoop狀態
            self.create_test_case(
                name="nd_snoop_get_vlan_100_status",
                method="GET",
                url="/api/v1/nd-snoop/vlans/100",
                category="nd_snoop_vlan_management",
                module="nd_snoop",
                description="獲取VLAN 100的ND Snoop狀態"
            ),
            
            # 啟用VLAN 1的ND Snoop
            self.create_test_case(
                name="nd_snoop_enable_vlan_1",
                method="PUT",
                url="/api/v1/nd-snoop/vlans/1",
                category="nd_snoop_vlan_management",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_vlan_1_enable', {
                    "ndSnoopVlanEnable": True
                }),
                description="啟用VLAN 1的ND Snoop"
            ),
            
            # 啟用VLAN 100的ND Snoop
            self.create_test_case(
                name="nd_snoop_enable_vlan_100",
                method="PUT",
                url="/api/v1/nd-snoop/vlans/100",
                category="nd_snoop_vlan_management",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_vlan_100_enable', {
                    "ndSnoopVlanEnable": True
                }),
                description="啟用VLAN 100的ND Snoop"
            ),
            
            # 啟用VLAN 200的ND Snoop - 企業級VLAN
            self.create_test_case(
                name="nd_snoop_enable_vlan_200_enterprise",
                method="PUT",
                url="/api/v1/nd-snoop/vlans/200",
                category="nd_snoop_vlan_management",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_vlan_200_enterprise_enable', {
                    "ndSnoopVlanEnable": True
                }),
                description="啟用VLAN 200的ND Snoop - 企業級VLAN"
            ),
            
            # 啟用VLAN 500的ND Snoop - 數據中心VLAN
            self.create_test_case(
                name="nd_snoop_enable_vlan_500_datacenter",
                method="PUT",
                url="/api/v1/nd-snoop/vlans/500",
                category="nd_snoop_vlan_management",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_vlan_500_datacenter_enable', {
                    "ndSnoopVlanEnable": True
                }),
                description="啟用VLAN 500的ND Snoop - 數據中心VLAN"
            ),
            
            # 禁用VLAN 300的ND Snoop
            self.create_test_case(
                name="nd_snoop_disable_vlan_300",
                method="PUT",
                url="/api/v1/nd-snoop/vlans/300",
                category="nd_snoop_vlan_management",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_vlan_300_disable', {
                    "ndSnoopVlanEnable": False
                }),
                description="禁用VLAN 300的ND Snoop"
            ),
            
            # 批量啟用多個VLAN - VLAN 10
            self.create_test_case(
                name="nd_snoop_batch_enable_vlan_10",
                method="PUT",
                url="/api/v1/nd-snoop/vlans/10",
                category="nd_snoop_vlan_management",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_vlan_10_batch_enable', {
                    "ndSnoopVlanEnable": True
                }),
                description="批量啟用VLAN 10的ND Snoop"
            ),
            
            # 批量啟用多個VLAN - VLAN 20
            self.create_test_case(
                name="nd_snoop_batch_enable_vlan_20",
                method="PUT",
                url="/api/v1/nd-snoop/vlans/20",
                category="nd_snoop_vlan_management",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_vlan_20_batch_enable', {
                    "ndSnoopVlanEnable": True
                }),
                description="批量啟用VLAN 20的ND Snoop"
            ),
            
            # 驗證VLAN ND Snoop配置更新
            self.create_test_case(
                name="nd_snoop_verify_vlan_configuration_update",
                method="GET",
                url="/api/v1/nd-snoop/vlans/1",
                category="nd_snoop_vlan_management",
                module="nd_snoop",
                description="驗證VLAN ND Snoop配置更新"
            ),
            
            # 驗證VLAN 100配置更新
            self.create_test_case(
                name="nd_snoop_verify_vlan_100_configuration_update",
                method="GET",
                url="/api/v1/nd-snoop/vlans/100",
                category="nd_snoop_vlan_management",
                module="nd_snoop",
                description="驗證VLAN 100配置更新"
            )
        ]
    
    def get_nd_snoop_interface_management_tests(self) -> List[APITestCase]:
        """ND Snoop Interface Management API 測試案例"""
        return [
            # 獲取eth1/1接口的ND Snoop配置
            self.create_test_case(
                name="nd_snoop_get_interface_eth1_1_configuration",
                method="GET",
                url="/api/v1/nd-snoop/interfaces/eth1%2f1",
                category="nd_snoop_interface_management",
                module="nd_snoop",
                description="獲取eth1/1接口的ND Snoop配置"
            ),
            
            # 獲取eth1/2接口的ND Snoop配置
            self.create_test_case(
                name="nd_snoop_get_interface_eth1_2_configuration",
                method="GET",
                url="/api/v1/nd-snoop/interfaces/eth1%2f2",
                category="nd_snoop_interface_management",
                module="nd_snoop",
                description="獲取eth1/2接口的ND Snoop配置"
            ),
            
            # 獲取trunk1接口的ND Snoop配置
            self.create_test_case(
                name="nd_snoop_get_interface_trunk1_configuration",
                method="GET",
                url="/api/v1/nd-snoop/interfaces/trunk1",
                category="nd_snoop_interface_management",
                module="nd_snoop",
                description="獲取trunk1接口的ND Snoop配置"
            ),
            
            # 設置eth1/1接口為信任狀態
            self.create_test_case(
                name="nd_snoop_set_interface_eth1_1_trust_enable",
                method="PUT",
                url="/api/v1/nd-snoop/interfaces/eth1%2f1",
                category="nd_snoop_interface_management",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_interface_eth1_1_trust_enable', {
                    "ndSnoopPortTrustEnable": True,
                    "ndSnoopPortMaxBinding": 3
                }),
                description="設置eth1/1接口為信任狀態"
            ),
            
            # 設置eth1/2接口為非信任狀態
            self.create_test_case(
                name="nd_snoop_set_interface_eth1_2_trust_disable",
                method="PUT",
                url="/api/v1/nd-snoop/interfaces/eth1%2f2",
                category="nd_snoop_interface_management",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_interface_eth1_2_trust_disable', {
                    "ndSnoopPortTrustEnable": False,
                    "ndSnoopPortMaxBinding": 5
                }),
                description="設置eth1/2接口為非信任狀態"
            ),
            
            # 設置trunk1接口配置
            self.create_test_case(
                name="nd_snoop_set_interface_trunk1_configuration",
                method="PUT",
                url="/api/v1/nd-snoop/interfaces/trunk1",
                category="nd_snoop_interface_management",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_interface_trunk1_config', {
                    "ndSnoopPortTrustEnable": True,
                    "ndSnoopPortMaxBinding": 5
                }),
                description="設置trunk1接口配置"
            ),
            
            # 設置eth1/5接口 - 最小綁定數
            self.create_test_case(
                name="nd_snoop_set_interface_eth1_5_min_binding",
                method="PUT",
                url="/api/v1/nd-snoop/interfaces/eth1%2f5",
                category="nd_snoop_interface_management",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_interface_eth1_5_min_binding', {
                    "ndSnoopPortTrustEnable": False,
                    "ndSnoopPortMaxBinding": 1
                }),
                description="設置eth1/5接口 - 最小綁定數"
            ),
            
            # 設置eth1/10接口 - 最大綁定數
            self.create_test_case(
                name="nd_snoop_set_interface_eth1_10_max_binding",
                method="PUT",
                url="/api/v1/nd-snoop/interfaces/eth1%2f10",
                category="nd_snoop_interface_management",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_interface_eth1_10_max_binding', {
                    "ndSnoopPortTrustEnable": True,
                    "ndSnoopPortMaxBinding": 5
                }),
                description="設置eth1/10接口 - 最大綁定數"
            ),
            
            # 批量配置多個接口 - eth1/20
            self.create_test_case(
                name="nd_snoop_batch_configure_interface_eth1_20",
                method="PUT",
                url="/api/v1/nd-snoop/interfaces/eth1%2f20",
                category="nd_snoop_interface_management",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_interface_eth1_20_batch', {
                    "ndSnoopPortTrustEnable": False,
                    "ndSnoopPortMaxBinding": 3
                }),
                description="批量配置接口 - eth1/20"
            ),
            
            # 批量配置多個接口 - eth1/21
            self.create_test_case(
                name="nd_snoop_batch_configure_interface_eth1_21",
                method="PUT",
                url="/api/v1/nd-snoop/interfaces/eth1%2f21",
                category="nd_snoop_interface_management",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_interface_eth1_21_batch', {
                    "ndSnoopPortTrustEnable": True,
                    "ndSnoopPortMaxBinding": 4
                }),
                description="批量配置接口 - eth1/21"
            ),
            
            # 驗證接口ND Snoop配置更新
            self.create_test_case(
                name="nd_snoop_verify_interface_configuration_update",
                method="GET",
                url="/api/v1/nd-snoop/interfaces/eth1%2f1",
                category="nd_snoop_interface_management",
                module="nd_snoop",
                description="驗證接口ND Snoop配置更新"
            ),
            
            # 驗證trunk1接口配置更新
            self.create_test_case(
                name="nd_snoop_verify_trunk1_interface_configuration_update",
                method="GET",
                url="/api/v1/nd-snoop/interfaces/trunk1",
                category="nd_snoop_interface_management",
                module="nd_snoop",
                description="驗證trunk1接口配置更新"
            )
        ]
    
    def get_nd_snoop_binding_table_management_tests(self) -> List[APITestCase]:
        """ND Snoop Binding Table Management API 測試案例"""
        return [
            # 獲取所有動態用戶綁定表條目
            self.create_test_case(
                name="nd_snoop_get_all_binding_entries",
                method="GET",
                url="/api/v1/nd-snoop/bindings",
                category="nd_snoop_binding_table_management",
                module="nd_snoop",
                description="獲取所有動態用戶綁定表條目"
            ),
            
            # 多次獲取綁定表以檢查一致性
            self.create_test_case(
                name="nd_snoop_get_binding_entries_consistency_check",
                method="GET",
                url="/api/v1/nd-snoop/bindings",
                category="nd_snoop_binding_table_management",
                module="nd_snoop",
                description="多次獲取綁定表以檢查一致性"
            ),
            
            # 驗證綁定表響應格式
            self.create_test_case(
                name="nd_snoop_verify_binding_table_response_format",
                method="GET",
                url="/api/v1/nd-snoop/bindings",
                category="nd_snoop_binding_table_management",
                module="nd_snoop",
                description="驗證綁定表響應格式"
            ),
            
            # 檢查綁定表條目完整性
            self.create_test_case(
                name="nd_snoop_check_binding_entries_completeness",
                method="GET",
                url="/api/v1/nd-snoop/bindings",
                category="nd_snoop_binding_table_management",
                module="nd_snoop",
                description="檢查綁定表條目完整性"
            ),
            
            # 清除所有動態用戶地址綁定表條目
            self.create_test_case(
                name="nd_snoop_clear_all_binding_entries",
                method="PUT",
                url="/api/v1/nd-snoop/bindings:clear",
                category="nd_snoop_binding_table_management",
                module="nd_snoop",
                description="清除所有動態用戶地址綁定表條目"
            ),
            
            # 驗證綁定表清除結果
            self.create_test_case(
                name="nd_snoop_verify_binding_entries_cleared",
                method="GET",
                url="/api/v1/nd-snoop/bindings",
                category="nd_snoop_binding_table_management",
                module="nd_snoop",
                description="驗證綁定表清除結果"
            ),
            
            # 再次清除綁定表（確保操作冪等性）
            self.create_test_case(
                name="nd_snoop_clear_binding_entries_idempotent",
                method="PUT",
                url="/api/v1/nd-snoop/bindings:clear",
                category="nd_snoop_binding_table_management",
                module="nd_snoop",
                description="再次清除綁定表（確保操作冪等性）"
            ),
            
            # 驗證清除後的綁定表狀態
            self.create_test_case(
                name="nd_snoop_verify_binding_table_after_clear",
                method="GET",
                url="/api/v1/nd-snoop/bindings",
                category="nd_snoop_binding_table_management",
                module="nd_snoop",
                description="驗證清除後的綁定表狀態"
            )
        ]
    
    def get_nd_snoop_prefix_table_management_tests(self) -> List[APITestCase]:
        """ND Snoop Prefix Table Management API 測試案例"""
        return [
            # 獲取所有地址前綴表條目
            self.create_test_case(
                name="nd_snoop_get_all_prefix_entries",
                method="GET",
                url="/api/v1/nd-snoop/prefixes",
                category="nd_snoop_prefix_table_management",
                module="nd_snoop",
                description="獲取所有地址前綴表條目"
            ),
            
            # 多次獲取前綴表以檢查一致性
            self.create_test_case(
                name="nd_snoop_get_prefix_entries_consistency_check",
                method="GET",
                url="/api/v1/nd-snoop/prefixes",
                category="nd_snoop_prefix_table_management",
                module="nd_snoop",
                description="多次獲取前綴表以檢查一致性"
            ),
            
            # 驗證前綴表響應格式
            self.create_test_case(
                name="nd_snoop_verify_prefix_table_response_format",
                method="GET",
                url="/api/v1/nd-snoop/prefixes",
                category="nd_snoop_prefix_table_management",
                module="nd_snoop",
                description="驗證前綴表響應格式"
            ),
            
            # 檢查前綴表條目完整性
            self.create_test_case(
                name="nd_snoop_check_prefix_entries_completeness",
                method="GET",
                url="/api/v1/nd-snoop/prefixes",
                category="nd_snoop_prefix_table_management",
                module="nd_snoop",
                description="檢查前綴表條目完整性"
            ),
            
            # 清除地址前綴表條目
            self.create_test_case(
                name="nd_snoop_clear_all_prefix_entries",
                method="PUT",
                url="/api/v1/nd-snoop/prefixes:clear",
                category="nd_snoop_prefix_table_management",
                module="nd_snoop",
                description="清除地址前綴表條目"
            ),
            
            # 驗證前綴表清除結果
            self.create_test_case(
                name="nd_snoop_verify_prefix_entries_cleared",
                method="GET",
                url="/api/v1/nd-snoop/prefixes",
                category="nd_snoop_prefix_table_management",
                module="nd_snoop",
                description="驗證前綴表清除結果"
            ),
            
            # 再次清除前綴表（確保操作冪等性）
            self.create_test_case(
                name="nd_snoop_clear_prefix_entries_idempotent",
                method="PUT",
                url="/api/v1/nd-snoop/prefixes:clear",
                category="nd_snoop_prefix_table_management",
                module="nd_snoop",
                description="再次清除前綴表（確保操作冪等性）"
            ),
            
            # 驗證清除後的前綴表狀態
            self.create_test_case(
                name="nd_snoop_verify_prefix_table_after_clear",
                method="GET",
                url="/api/v1/nd-snoop/prefixes",
                category="nd_snoop_prefix_table_management",
                module="nd_snoop",
                description="驗證清除後的前綴表狀態"
            )
        ]
    
    def get_nd_snoop_advanced_operations_tests(self) -> List[APITestCase]:
        """ND Snoop Advanced Operations API 測試案例"""
        return [
            # 配置企業級ND Snoop環境
            self.create_test_case(
                name="nd_snoop_configure_enterprise_environment",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_advanced_operations",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_enterprise_environment', {
                    "ndSnoopEnable": True,
                    "ndSnoopAutodetect": True,
                    "ndSnoopPrefixTimeout": 1200,
                    "ndSnoopRetransmitCount": 3,
                    "ndSnoopRetransmitInterval": 5
                }),
                description="配置企業級ND Snoop環境"
            ),
            
            # 批量配置多個VLAN - VLAN 50
            self.create_test_case(
                name="nd_snoop_batch_configure_vlan_50",
                method="PUT",
                url="/api/v1/nd-snoop/vlans/50",
                category="nd_snoop_advanced_operations",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_batch_vlan_50', {
                    "ndSnoopVlanEnable": True
                }),
                description="批量配置VLAN 50"
            ),
            
            # 批量配置多個VLAN - VLAN 60
            self.create_test_case(
                name="nd_snoop_batch_configure_vlan_60",
                method="PUT",
                url="/api/v1/nd-snoop/vlans/60",
                category="nd_snoop_advanced_operations",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_batch_vlan_60', {
                    "ndSnoopVlanEnable": True
                }),
                description="批量配置VLAN 60"
            ),
            
            # 批量配置多個VLAN - VLAN 70
            self.create_test_case(
                name="nd_snoop_batch_configure_vlan_70",
                method="PUT",
                url="/api/v1/nd-snoop/vlans/70",
                category="nd_snoop_advanced_operations",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_batch_vlan_70', {
                    "ndSnoopVlanEnable": True
                }),
                description="批量配置VLAN 70"
            ),
            
            # 配置高安全性接口策略 - eth1/30
            self.create_test_case(
                name="nd_snoop_configure_high_security_interface_eth1_30",
                method="PUT",
                url="/api/v1/nd-snoop/interfaces/eth1%2f30",
                category="nd_snoop_advanced_operations",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_high_security_interface_eth1_30', {
                    "ndSnoopPortTrustEnable": False,
                    "ndSnoopPortMaxBinding": 1
                }),
                description="配置高安全性接口策略 - eth1/30"
            ),
            
            # 配置高性能接口策略 - eth1/40
            self.create_test_case(
                name="nd_snoop_configure_high_performance_interface_eth1_40",
                method="PUT",
                url="/api/v1/nd-snoop/interfaces/eth1%2f40",
                category="nd_snoop_advanced_operations",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_high_performance_interface_eth1_40', {
                    "ndSnoopPortTrustEnable": True,
                    "ndSnoopPortMaxBinding": 5
                }),
                description="配置高性能接口策略 - eth1/40"
            ),
            
            # 配置數據中心級ND Snoop策略
            self.create_test_case(
                name="nd_snoop_configure_datacenter_policy",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_advanced_operations",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_datacenter_policy', {
                    "ndSnoopEnable": True,
                    "ndSnoopAutodetect": False,
                    "ndSnoopPrefixTimeout": 1800,
                    "ndSnoopRetransmitCount": 5,
                    "ndSnoopRetransmitInterval": 10
                }),
                description="配置數據中心級ND Snoop策略"
            ),
            
            # 動態調整ND Snoop參數
            self.create_test_case(
                name="nd_snoop_dynamic_adjust_parameters",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_advanced_operations",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_dynamic_parameters', {
                    "ndSnoopEnable": True,
                    "ndSnoopAutodetect": True,
                    "ndSnoopPrefixTimeout": 300,
                    "ndSnoopRetransmitCount": 4,
                    "ndSnoopRetransmitInterval": 6
                }),
                description="動態調整ND Snoop參數"
            ),
            
            # 配置複雜的多層級策略
            self.create_test_case(
                name="nd_snoop_configure_complex_multilevel_policy",
                method="PUT",
                url="/api/v1/nd-snoop/interfaces/trunk2",
                category="nd_snoop_advanced_operations",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_complex_multilevel_policy', {
                    "ndSnoopPortTrustEnable": True,
                    "ndSnoopPortMaxBinding": 5
                }),
                description="配置複雜的多層級策略"
            ),
            
            # 執行綜合清理操作
            self.create_test_case(
                name="nd_snoop_comprehensive_cleanup_bindings",
                method="PUT",
                url="/api/v1/nd-snoop/bindings:clear",
                category="nd_snoop_advanced_operations",
                module="nd_snoop",
                description="執行綜合清理操作 - 綁定表"
            ),
            
            # 執行綜合清理操作
            self.create_test_case(
                name="nd_snoop_comprehensive_cleanup_prefixes",
                method="PUT",
                url="/api/v1/nd-snoop/prefixes:clear",
                category="nd_snoop_advanced_operations",
                module="nd_snoop",
                description="執行綜合清理操作 - 前綴表"
            ),
            
            # 驗證高級操作結果
            self.create_test_case(
                name="nd_snoop_verify_advanced_operations_results",
                method="GET",
                url="/api/v1/nd-snoop",
                category="nd_snoop_advanced_operations",
                module="nd_snoop",
                description="驗證高級操作結果"
            ),
            
            # 驗證VLAN高級配置結果
            self.create_test_case(
                name="nd_snoop_verify_vlan_advanced_results",
                method="GET",
                url="/api/v1/nd-snoop/vlans/50",
                category="nd_snoop_advanced_operations",
                module="nd_snoop",
                description="驗證VLAN高級配置結果"
            ),
            
            # 驗證接口高級配置結果
            self.create_test_case(
                name="nd_snoop_verify_interface_advanced_results",
                method="GET",
                url="/api/v1/nd-snoop/interfaces/eth1%2f30",
                category="nd_snoop_advanced_operations",
                module="nd_snoop",
                description="驗證接口高級配置結果"
            )
        ]
    
    def get_nd_snoop_error_handling_tests(self) -> List[APITestCase]:
        """ND Snoop Error Handling API 測試案例"""
        return [
            # 測試無效的前綴超時值 - 小於最小值
            self.create_test_case(
                name="nd_snoop_test_invalid_prefix_timeout_below_minimum",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_invalid_prefix_timeout_below_min', {
                    "ndSnoopEnable": True,
                    "ndSnoopPrefixTimeout": 2  # 小於最小值 (3)
                }),
                expected_status=400,
                description="測試無效的前綴超時值 - 小於最小值 (<3)"
            ),
            
            # 測試無效的前綴超時值 - 超出最大值
            self.create_test_case(
                name="nd_snoop_test_invalid_prefix_timeout_above_maximum",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_invalid_prefix_timeout_above_max', {
                    "ndSnoopEnable": True,
                    "ndSnoopPrefixTimeout": 2000  # 超出最大值 (1800)
                }),
                expected_status=400,
                description="測試無效的前綴超時值 - 超出最大值 (>1800)"
            ),
            
            # 測試無效的重傳次數 - 小於最小值
            self.create_test_case(
                name="nd_snoop_test_invalid_retransmit_count_below_minimum",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_invalid_retransmit_count_below_min', {
                    "ndSnoopEnable": True,
                    "ndSnoopRetransmitCount": 0  # 小於最小值 (1)
                }),
                expected_status=400,
                description="測試無效的重傳次數 - 小於最小值 (<1)"
            ),
            
            # 測試無效的重傳次數 - 超出最大值
            self.create_test_case(
                name="nd_snoop_test_invalid_retransmit_count_above_maximum",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_invalid_retransmit_count_above_max', {
                    "ndSnoopEnable": True,
                    "ndSnoopRetransmitCount": 10  # 超出最大值 (5)
                }),
                expected_status=400,
                description="測試無效的重傳次數 - 超出最大值 (>5)"
            ),
            
            # 測試無效的重傳間隔 - 小於最小值
            self.create_test_case(
                name="nd_snoop_test_invalid_retransmit_interval_below_minimum",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_invalid_retransmit_interval_below_min', {
                    "ndSnoopEnable": True,
                    "ndSnoopRetransmitInterval": 0  # 小於最小值 (1)
                }),
                expected_status=400,
                description="測試無效的重傳間隔 - 小於最小值 (<1)"
            ),
            
            # 測試無效的重傳間隔 - 超出最大值
            self.create_test_case(
                name="nd_snoop_test_invalid_retransmit_interval_above_maximum",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_invalid_retransmit_interval_above_max', {
                    "ndSnoopEnable": True,
                    "ndSnoopRetransmitInterval": 15  # 超出最大值 (10)
                }),
                expected_status=400,
                description="測試無效的重傳間隔 - 超出最大值 (>10)"
            ),
            
            # 測試無效的VLAN ID - 超出範圍
            self.create_test_case(
                name="nd_snoop_test_invalid_vlan_id_out_of_range",
                method="PUT",
                url="/api/v1/nd-snoop/vlans/5000",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_invalid_vlan_id', {
                    "ndSnoopVlanEnable": True
                }),
                expected_status=400,
                description="測試無效的VLAN ID - 超出範圍 (>4094)"
            ),
            
            # 測試無效的VLAN ID - 零
            self.create_test_case(
                name="nd_snoop_test_invalid_vlan_id_zero",
                method="PUT",
                url="/api/v1/nd-snoop/vlans/0",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_invalid_vlan_id_zero', {
                    "ndSnoopVlanEnable": True
                }),
                expected_status=400,
                description="測試無效的VLAN ID - 零"
            ),
            
            # 測試無效的接口ID格式
            self.create_test_case(
                name="nd_snoop_test_invalid_interface_id_format",
                method="GET",
                url="/api/v1/nd-snoop/interfaces/invalid_interface",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                expected_status=400,
                description="測試無效的接口ID格式"
            ),
            
            # 測試超出範圍的接口ID
            self.create_test_case(
                name="nd_snoop_test_out_of_range_interface_id",
                method="GET",
                url="/api/v1/nd-snoop/interfaces/eth9%2f99",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                expected_status=400,
                description="測試超出範圍的接口ID"
            ),
            
            # 測試無效的最大綁定數 - 小於最小值
            self.create_test_case(
                name="nd_snoop_test_invalid_max_binding_below_minimum",
                method="PUT",
                url="/api/v1/nd-snoop/interfaces/eth1%2f1",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_invalid_max_binding_below_min', {
                    "ndSnoopPortMaxBinding": 0  # 小於最小值 (1)
                }),
                expected_status=400,
                description="測試無效的最大綁定數 - 小於最小值 (<1)"
            ),
            
            # 測試無效的最大綁定數 - 超出最大值
            self.create_test_case(
                name="nd_snoop_test_invalid_max_binding_above_maximum",
                method="PUT",
                url="/api/v1/nd-snoop/interfaces/eth1%2f1",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_invalid_max_binding_above_max', {
                    "ndSnoopPortMaxBinding": 10  # 超出最大值 (5)
                }),
                expected_status=400,
                description="測試無效的最大綁定數 - 超出最大值 (>5)"
            ),
            
            # 測試無效的布爾值 - ND Snoop啟用狀態
            self.create_test_case(
                name="nd_snoop_test_invalid_boolean_enable_status",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_invalid_boolean_enable', {
                    "ndSnoopEnable": "yes"  # 無效布爾值
                }),
                expected_status=400,
                description="測試無效的布爾值 - ND Snoop啟用狀態"
            ),
            
            # 測試無效的布爾值 - 自動檢測狀態
            self.create_test_case(
                name="nd_snoop_test_invalid_boolean_autodetect_status",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_invalid_boolean_autodetect', {
                    "ndSnoopAutodetect": "on"  # 無效布爾值
                }),
                expected_status=400,
                description="測試無效的布爾值 - 自動檢測狀態"
            ),
            
            # 測試無效JSON格式 - 全局配置
            self.create_test_case(
                name="nd_snoop_test_invalid_json_global_config",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                body="invalid json format",
                expected_status=400,
                description="測試無效JSON格式 - 全局配置"
            ),
            
            # 測試無效JSON格式 - VLAN配置
            self.create_test_case(
                name="nd_snoop_test_invalid_json_vlan_config",
                method="PUT",
                url="/api/v1/nd-snoop/vlans/100",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                body="{ invalid json }",
                expected_status=400,
                description="測試無效JSON格式 - VLAN配置"
            ),
            
            # 測試無效JSON格式 - 接口配置
            self.create_test_case(
                name="nd_snoop_test_invalid_json_interface_config",
                method="PUT",
                url="/api/v1/nd-snoop/interfaces/eth1%2f1",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                body="{ invalid: json }",
                expected_status=400,
                description="測試無效JSON格式 - 接口配置"
            ),
            
            # 測試不存在的VLAN
            self.create_test_case(
                name="nd_snoop_test_nonexistent_vlan",
                method="PUT",
                url="/api/v1/nd-snoop/vlans/999",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_nonexistent_vlan', {
                    "ndSnoopVlanEnable": True
                }),
                expected_status=500,
                description="測試不存在的VLAN"
            ),
            
            # 恢復正常ND Snoop配置
            self.create_test_case(
                name="nd_snoop_restore_normal_configuration",
                method="PUT",
                url="/api/v1/nd-snoop",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                body=self.test_data.get('nd_snoop_restore_normal_config', {
                    "ndSnoopEnable": True,
                    "ndSnoopAutodetect": True,
                    "ndSnoopPrefixTimeout": 200,
                    "ndSnoopRetransmitCount": 5,
                    "ndSnoopRetransmitInterval": 5
                }),
                description="恢復正常ND Snoop配置"
            ),
            
            # 最終ND Snoop狀態檢查
            self.create_test_case(
                name="nd_snoop_final_status_check",
                method="GET",
                url="/api/v1/nd-snoop",
                category="nd_snoop_error_handling",
                module="nd_snoop",
                description="最終ND Snoop狀態檢查"
            )
        ]