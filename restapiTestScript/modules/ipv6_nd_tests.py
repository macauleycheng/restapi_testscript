#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IPv6 ND (Neighbor Discovery) 模組測試案例
包含IPv6鄰居發現配置、VLAN管理、接口管理、鄰居表管理、前綴表管理等相關API測試
支援ND hop limit配置、VLAN級別ND配置、接口RA guard、靜態鄰居管理、前綴廣告等操作
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class IPV6_NDTests(BaseTests):
    """IPv6 ND 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取IPv6 ND模組支援的類別"""
        return [
            "ipv6_nd_global_configuration",
            "ipv6_nd_vlan_management",
            "ipv6_nd_interface_management",
            "ipv6_nd_neighbor_management",
            "ipv6_nd_prefix_management",
            "ipv6_nd_advanced_operations",
            "ipv6_nd_error_handling"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有IPv6 ND測試案例"""
        all_tests = []
        all_tests.extend(self.get_ipv6_nd_global_configuration_tests())
        all_tests.extend(self.get_ipv6_nd_vlan_management_tests())
        all_tests.extend(self.get_ipv6_nd_interface_management_tests())
        all_tests.extend(self.get_ipv6_nd_neighbor_management_tests())
        all_tests.extend(self.get_ipv6_nd_prefix_management_tests())
        all_tests.extend(self.get_ipv6_nd_advanced_operations_tests())
        all_tests.extend(self.get_ipv6_nd_error_handling_tests())
        return all_tests
    
    def get_ipv6_nd_global_configuration_tests(self) -> List[APITestCase]:
        """IPv6 ND Global Configuration API 測試案例"""
        return [
            # 獲取IPv6 ND hop limit
            self.create_test_case(
                name="ipv6_nd_get_hop_limit",
                method="GET",
                url="/api/v1/ipv6/nd",
                category="ipv6_nd_global_configuration",
                module="ipv6_nd",
                description="獲取IPv6 ND hop limit"
            ),
            
            # 設置IPv6 ND hop limit - 默認值
            self.create_test_case(
                name="ipv6_nd_set_hop_limit_default",
                method="PUT",
                url="/api/v1/ipv6/nd",
                category="ipv6_nd_global_configuration",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_hop_limit_default', {
                    "hopLimit": 64
                }),
                description="設置IPv6 ND hop limit - 默認值"
            ),
            
            # 設置IPv6 ND hop limit - 最小值
            self.create_test_case(
                name="ipv6_nd_set_hop_limit_minimum",
                method="PUT",
                url="/api/v1/ipv6/nd",
                category="ipv6_nd_global_configuration",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_hop_limit_minimum', {
                    "hopLimit": 1
                }),
                description="設置IPv6 ND hop limit - 最小值"
            ),
            
            # 設置IPv6 ND hop limit - 最大值
            self.create_test_case(
                name="ipv6_nd_set_hop_limit_maximum",
                method="PUT",
                url="/api/v1/ipv6/nd",
                category="ipv6_nd_global_configuration",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_hop_limit_maximum', {
                    "hopLimit": 255
                }),
                description="設置IPv6 ND hop limit - 最大值"
            ),
            
            # 設置IPv6 ND hop limit - 企業級配置
            self.create_test_case(
                name="ipv6_nd_set_hop_limit_enterprise",
                method="PUT",
                url="/api/v1/ipv6/nd",
                category="ipv6_nd_global_configuration",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_hop_limit_enterprise', {
                    "hopLimit": 128
                }),
                description="設置IPv6 ND hop limit - 企業級配置"
            ),
            
            # 驗證IPv6 ND hop limit更新
            self.create_test_case(
                name="ipv6_nd_verify_hop_limit_update",
                method="GET",
                url="/api/v1/ipv6/nd",
                category="ipv6_nd_global_configuration",
                module="ipv6_nd",
                description="驗證IPv6 ND hop limit更新"
            ),
            
            # 恢復IPv6 ND hop limit默認值
            self.create_test_case(
                name="ipv6_nd_restore_hop_limit_default",
                method="PUT",
                url="/api/v1/ipv6/nd",
                category="ipv6_nd_global_configuration",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_hop_limit_restore_default', {
                    "hopLimit": 64
                }),
                description="恢復IPv6 ND hop limit默認值"
            )
        ]
    
    def get_ipv6_nd_vlan_management_tests(self) -> List[APITestCase]:
        """IPv6 ND VLAN Management API 測試案例"""
        return [
            # 獲取VLAN 1的ND配置
            self.create_test_case(
                name="ipv6_nd_get_vlan_1_configuration",
                method="GET",
                url="/api/v1/ipv6/nd/vlans/1",
                category="ipv6_nd_vlan_management",
                module="ipv6_nd",
                description="獲取VLAN 1的ND配置"
            ),
            
            # 設置VLAN 1的ND配置 - 基本配置
            self.create_test_case(
                name="ipv6_nd_set_vlan_1_basic_configuration",
                method="PUT",
                url="/api/v1/ipv6/nd/vlans/1",
                category="ipv6_nd_vlan_management",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_vlan_1_basic_config', {
                    "dadAttemptsCount": 5,
                    "managedConfigFlagStatus": True,
                    "otherConfigFlagStatus": True,
                    "nsInterval": 30000,
                    "reachableTime": 1000,
                    "raMinInterval": 200,
                    "raMaxInterval": 1800,
                    "raLifetime": 8000,
                    "raPreferenceLevel": "high",
                    "raSuppressStatus": True
                }),
                description="設置VLAN 1的ND配置 - 基本配置"
            ),
            
            # 設置VLAN 100的ND配置 - 企業級配置
            self.create_test_case(
                name="ipv6_nd_set_vlan_100_enterprise_configuration",
                method="PUT",
                url="/api/v1/ipv6/nd/vlans/100",
                category="ipv6_nd_vlan_management",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_vlan_100_enterprise_config', {
                    "dadAttemptsCount": 3,
                    "managedConfigFlagStatus": False,
                    "otherConfigFlagStatus": False,
                    "nsInterval": 1000,
                    "reachableTime": 30000,
                    "raMinInterval": 198,
                    "raMaxInterval": 600,
                    "raLifetime": 1800,
                    "raPreferenceLevel": "medium",
                    "raSuppressStatus": False
                }),
                description="設置VLAN 100的ND配置 - 企業級配置"
            ),
            
            # 設置VLAN 200的ND配置 - 數據中心配置
            self.create_test_case(
                name="ipv6_nd_set_vlan_200_datacenter_configuration",
                method="PUT",
                url="/api/v1/ipv6/nd/vlans/200",
                category="ipv6_nd_vlan_management",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_vlan_200_datacenter_config', {
                    "dadAttemptsCount": 1,
                    "managedConfigFlagStatus": True,
                    "otherConfigFlagStatus": True,
                    "nsInterval": 3600000,
                    "reachableTime": 3600000,
                    "raMinInterval": 3,
                    "raMaxInterval": 4,
                    "raLifetime": 9000,
                    "raPreferenceLevel": "low",
                    "raSuppressStatus": False
                }),
                description="設置VLAN 200的ND配置 - 數據中心配置"
            ),
            
            # 設置VLAN 300的ND配置 - 最小值配置
            self.create_test_case(
                name="ipv6_nd_set_vlan_300_minimum_configuration",
                method="PUT",
                url="/api/v1/ipv6/nd/vlans/300",
                category="ipv6_nd_vlan_management",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_vlan_300_minimum_config', {
                    "dadAttemptsCount": 0,
                    "managedConfigFlagStatus": False,
                    "otherConfigFlagStatus": False,
                    "nsInterval": 1000,
                    "reachableTime": 0,
                    "raMinInterval": 3,
                    "raMaxInterval": 4,
                    "raLifetime": 0,
                    "raPreferenceLevel": "low",
                    "raSuppressStatus": True
                }),
                description="設置VLAN 300的ND配置 - 最小值配置"
            ),
            
            # 設置VLAN 400的ND配置 - 最大值配置
            self.create_test_case(
                name="ipv6_nd_set_vlan_400_maximum_configuration",
                method="PUT",
                url="/api/v1/ipv6/nd/vlans/400",
                category="ipv6_nd_vlan_management",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_vlan_400_maximum_config', {
                    "dadAttemptsCount": 600,
                    "managedConfigFlagStatus": True,
                    "otherConfigFlagStatus": True,
                    "nsInterval": 3600000,
                    "reachableTime": 3600000,
                    "raMinInterval": 1350,
                    "raMaxInterval": 1800,
                    "raLifetime": 9000,
                    "raPreferenceLevel": "high",
                    "raSuppressStatus": False
                }),
                description="設置VLAN 400的ND配置 - 最大值配置"
            ),
            
            # 驗證VLAN ND配置更新
            self.create_test_case(
                name="ipv6_nd_verify_vlan_configuration_update",
                method="GET",
                url="/api/v1/ipv6/nd/vlans/1",
                category="ipv6_nd_vlan_management",
                module="ipv6_nd",
                description="驗證VLAN ND配置更新"
            ),
            
            # 驗證VLAN 100配置更新
            self.create_test_case(
                name="ipv6_nd_verify_vlan_100_configuration_update",
                method="GET",
                url="/api/v1/ipv6/nd/vlans/100",
                category="ipv6_nd_vlan_management",
                module="ipv6_nd",
                description="驗證VLAN 100配置更新"
            )
        ]
    
    def get_ipv6_nd_interface_management_tests(self) -> List[APITestCase]:
        """IPv6 ND Interface Management API 測試案例"""
        return [
            # 獲取eth1/1接口的ND raguard配置
            self.create_test_case(
                name="ipv6_nd_get_interface_eth1_1_raguard",
                method="GET",
                url="/api/v1/ipv6/nd/interfaces/eth1%2f1",
                category="ipv6_nd_interface_management",
                module="ipv6_nd",
                description="獲取eth1/1接口的ND raguard配置"
            ),
            
            # 獲取eth1/2接口的ND raguard配置
            self.create_test_case(
                name="ipv6_nd_get_interface_eth1_2_raguard",
                method="GET",
                url="/api/v1/ipv6/nd/interfaces/eth1%2f2",
                category="ipv6_nd_interface_management",
                module="ipv6_nd",
                description="獲取eth1/2接口的ND raguard配置"
            ),
            
            # 獲取trunk1接口的ND raguard配置
            self.create_test_case(
                name="ipv6_nd_get_interface_trunk1_raguard",
                method="GET",
                url="/api/v1/ipv6/nd/interfaces/trunk1",
                category="ipv6_nd_interface_management",
                module="ipv6_nd",
                description="獲取trunk1接口的ND raguard配置"
            ),
            
            # 啟用eth1/1接口的RA guard
            self.create_test_case(
                name="ipv6_nd_enable_interface_eth1_1_raguard",
                method="PUT",
                url="/api/v1/ipv6/nd/interfaces/eth1%2f1",
                category="ipv6_nd_interface_management",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_interface_eth1_1_raguard_enable', {
                    "raguardStatus": True
                }),
                description="啟用eth1/1接口的RA guard"
            ),
            
            # 禁用eth1/2接口的RA guard
            self.create_test_case(
                name="ipv6_nd_disable_interface_eth1_2_raguard",
                method="PUT",
                url="/api/v1/ipv6/nd/interfaces/eth1%2f2",
                category="ipv6_nd_interface_management",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_interface_eth1_2_raguard_disable', {
                    "raguardStatus": False
                }),
                description="禁用eth1/2接口的RA guard"
            ),
            
            # 啟用trunk1接口的RA guard
            self.create_test_case(
                name="ipv6_nd_enable_interface_trunk1_raguard",
                method="PUT",
                url="/api/v1/ipv6/nd/interfaces/trunk1",
                category="ipv6_nd_interface_management",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_interface_trunk1_raguard_enable', {
                    "raguardStatus": True
                }),
                description="啟用trunk1接口的RA guard"
            ),
            
            # 批量配置多個接口 - eth1/10
            self.create_test_case(
                name="ipv6_nd_batch_configure_interface_eth1_10",
                method="PUT",
                url="/api/v1/ipv6/nd/interfaces/eth1%2f10",
                category="ipv6_nd_interface_management",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_interface_eth1_10_batch', {
                    "raguardStatus": True
                }),
                description="批量配置接口 - eth1/10"
            ),
            
            # 批量配置多個接口 - eth1/20
            self.create_test_case(
                name="ipv6_nd_batch_configure_interface_eth1_20",
                method="PUT",
                url="/api/v1/ipv6/nd/interfaces/eth1%2f20",
                category="ipv6_nd_interface_management",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_interface_eth1_20_batch', {
                    "raguardStatus": False
                }),
                description="批量配置接口 - eth1/20"
            ),
            
            # 驗證接口RA guard配置更新
            self.create_test_case(
                name="ipv6_nd_verify_interface_raguard_update",
                method="GET",
                url="/api/v1/ipv6/nd/interfaces/eth1%2f1",
                category="ipv6_nd_interface_management",
                module="ipv6_nd",
                description="驗證接口RA guard配置更新"
            ),
            
            # 驗證trunk1接口配置更新
            self.create_test_case(
                name="ipv6_nd_verify_trunk1_interface_update",
                method="GET",
                url="/api/v1/ipv6/nd/interfaces/trunk1",
                category="ipv6_nd_interface_management",
                module="ipv6_nd",
                description="驗證trunk1接口配置更新"
            )
        ]
    
    def get_ipv6_nd_neighbor_management_tests(self) -> List[APITestCase]:
        """IPv6 ND Neighbor Management API 測試案例"""
        return [
            # 獲取所有IPv6鄰居條目
            self.create_test_case(
                name="ipv6_nd_get_all_neighbor_entries",
                method="GET",
                url="/api/v1/ipv6/nd/neighbors",
                category="ipv6_nd_neighbor_management",
                module="ipv6_nd",
                description="獲取所有IPv6鄰居條目"
            ),
            
            # 添加靜態IPv6鄰居條目 - 基本條目
            self.create_test_case(
                name="ipv6_nd_add_static_neighbor_basic",
                method="POST",
                url="/api/v1/ipv6/nd/neighbors",
                category="ipv6_nd_neighbor_management",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_static_neighbor_basic', {
                    "type": "static",
                    "vlanId": 1,
                    "ipv6Address": "fe80::2e0:cff:fe9c:c000",
                    "linkLayerAddress": "30-65-14-01-11-8a"
                }),
                description="添加靜態IPv6鄰居條目 - 基本條目"
            ),
            
            # 添加靜態IPv6鄰居條目 - 企業級條目
            self.create_test_case(
                name="ipv6_nd_add_static_neighbor_enterprise",
                method="POST",
                url="/api/v1/ipv6/nd/neighbors",
                category="ipv6_nd_neighbor_management",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_static_neighbor_enterprise', {
                    "type": "static",
                    "vlanId": 100,
                    "ipv6Address": "2001:db8::1",
                    "linkLayerAddress": "aa-bb-cc-dd-ee-ff"
                }),
                description="添加靜態IPv6鄰居條目 - 企業級條目"
            ),
            
            # 添加靜態IPv6鄰居條目 - 數據中心條目
            self.create_test_case(
                name="ipv6_nd_add_static_neighbor_datacenter",
                method="POST",
                url="/api/v1/ipv6/nd/neighbors",
                category="ipv6_nd_neighbor_management",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_static_neighbor_datacenter', {
                    "type": "static",
                    "vlanId": 200,
                    "ipv6Address": "2001:db8:1::100",
                    "linkLayerAddress": "11-22-33-44-55-66"
                }),
                description="添加靜態IPv6鄰居條目 - 數據中心條目"
            ),
            
            # 獲取特定靜態IPv6鄰居條目
            self.create_test_case(
                name="ipv6_nd_get_specific_static_neighbor",
                method="GET",
                url="/api/v1/ipv6/nd/neighbors/types/static/ipv6-address/fe80::2e0:cff:fe9c:c000/vlans/1",
                category="ipv6_nd_neighbor_management",
                module="ipv6_nd",
                description="獲取特定靜態IPv6鄰居條目"
            ),
            
            # 獲取企業級靜態IPv6鄰居條目
            self.create_test_case(
                name="ipv6_nd_get_enterprise_static_neighbor",
                method="GET",
                url="/api/v1/ipv6/nd/neighbors/types/static/ipv6-address/2001:db8::1/vlans/100",
                category="ipv6_nd_neighbor_management",
                module="ipv6_nd",
                description="獲取企業級靜態IPv6鄰居條目"
            ),
            
            # 清除所有動態IPv6鄰居條目
            self.create_test_case(
                name="ipv6_nd_clear_all_dynamic_neighbors",
                method="PUT",
                url="/api/v1/ipv6/nd/neighbors/dynamic:clear",
                category="ipv6_nd_neighbor_management",
                module="ipv6_nd",
                body={},
                description="清除所有動態IPv6鄰居條目"
            ),
            
            # 驗證動態鄰居清除結果
            self.create_test_case(
                name="ipv6_nd_verify_dynamic_neighbors_cleared",
                method="GET",
                url="/api/v1/ipv6/nd/neighbors",
                category="ipv6_nd_neighbor_management",
                module="ipv6_nd",
                description="驗證動態鄰居清除結果"
            ),
            
            # 刪除特定靜態IPv6鄰居條目
            self.create_test_case(
                name="ipv6_nd_delete_specific_static_neighbor",
                method="DELETE",
                url="/api/v1/ipv6/nd/neighbors/types/static/ipv6-address/fe80::2e0:cff:fe9c:c000/vlans/1",
                category="ipv6_nd_neighbor_management",
                module="ipv6_nd",
                description="刪除特定靜態IPv6鄰居條目"
            ),
            
            # 刪除企業級靜態IPv6鄰居條目
            self.create_test_case(
                name="ipv6_nd_delete_enterprise_static_neighbor",
                method="DELETE",
                url="/api/v1/ipv6/nd/neighbors/types/static/ipv6-address/2001:db8::1/vlans/100",
                category="ipv6_nd_neighbor_management",
                module="ipv6_nd",
                description="刪除企業級靜態IPv6鄰居條目"
            ),
            
            # 刪除數據中心靜態IPv6鄰居條目
            self.create_test_case(
                name="ipv6_nd_delete_datacenter_static_neighbor",
                method="DELETE",
                url="/api/v1/ipv6/nd/neighbors/types/static/ipv6-address/2001:db8:1::100/vlans/200",
                category="ipv6_nd_neighbor_management",
                module="ipv6_nd",
                description="刪除數據中心靜態IPv6鄰居條目"
            ),
            
            # 驗證鄰居條目刪除結果
            self.create_test_case(
                name="ipv6_nd_verify_neighbor_entries_deleted",
                method="GET",
                url="/api/v1/ipv6/nd/neighbors",
                category="ipv6_nd_neighbor_management",
                module="ipv6_nd",
                description="驗證鄰居條目刪除結果"
            )
        ]
    
    def get_ipv6_nd_prefix_management_tests(self) -> List[APITestCase]:
        """IPv6 ND Prefix Management API 測試案例"""
        return [
            # 獲取所有IPv6前綴條目
            self.create_test_case(
                name="ipv6_nd_get_all_prefix_entries",
                method="GET",
                url="/api/v1/ipv6/nd/prefix/vlans",
                category="ipv6_nd_prefix_management",
                module="ipv6_nd",
                description="獲取所有IPv6前綴條目"
            ),
            
            # 添加IPv6前綴 - 基本前綴
            self.create_test_case(
                name="ipv6_nd_add_prefix_basic",
                method="POST",
                url="/api/v1/ipv6/nd/prefix/vlans",
                category="ipv6_nd_prefix_management",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_prefix_basic', {
                    "vlanId": 1,
                    "ipv6Prefix": "2011:1dbf::",
                    "ipv6PrefixLength": 35,
                    "validLifetime": 1000,
                    "preferredLifetime": 900,
                    "configureType": "no-autoconfig"
                }),
                description="添加IPv6前綴 - 基本前綴"
            ),
            
            # 添加IPv6前綴 - 企業級前綴
            self.create_test_case(
                name="ipv6_nd_add_prefix_enterprise",
                method="POST",
                url="/api/v1/ipv6/nd/prefix/vlans",
                category="ipv6_nd_prefix_management",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_prefix_enterprise', {
                    "vlanId": 100,
                    "ipv6Prefix": "2001:db8::",
                    "ipv6PrefixLength": 64,
                    "validLifetime": 7200,
                    "preferredLifetime": 3600,
                    "configureType": "off-link"
                }),
                description="添加IPv6前綴 - 企業級前綴"
            ),
            
            # 添加IPv6前綴 - 數據中心前綴
            self.create_test_case(
                name="ipv6_nd_add_prefix_datacenter",
                method="POST",
                url="/api/v1/ipv6/nd/prefix/vlans",
                category="ipv6_nd_prefix_management",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_prefix_datacenter', {
                    "vlanId": 200,
                    "ipv6Prefix": "2001:db8:1::",
                    "ipv6PrefixLength": 48,
                    "validLifetime": 4294967295,
                    "preferredLifetime": 4294967295
                }),
                description="添加IPv6前綴 - 數據中心前綴"
            ),
            
            # 添加IPv6前綴 - 最小生命週期
            self.create_test_case(
                name="ipv6_nd_add_prefix_minimum_lifetime",
                method="POST",
                url="/api/v1/ipv6/nd/prefix/vlans",
                category="ipv6_nd_prefix_management",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_prefix_minimum_lifetime', {
                    "vlanId": 300,
                    "ipv6Prefix": "2001:db8:2::",
                    "ipv6PrefixLength": 56,
                    "validLifetime": 0,
                    "preferredLifetime": 0,
                    "configureType": "no-autoconfig"
                }),
                description="添加IPv6前綴 - 最小生命週期"
            ),
            
            # 獲取特定IPv6前綴條目
            self.create_test_case(
                name="ipv6_nd_get_specific_prefix_entry",
                method="GET",
                url="/api/v1/ipv6/nd/prefix/vlans/1/ipv6-prefix/2011:1dbf::/ipv6-prefix-length/35",
                category="ipv6_nd_prefix_management",
                module="ipv6_nd",
                description="獲取特定IPv6前綴條目"
            ),
            
            # 獲取企業級IPv6前綴條目
            self.create_test_case(
                name="ipv6_nd_get_enterprise_prefix_entry",
                method="GET",
                url="/api/v1/ipv6/nd/prefix/vlans/100/ipv6-prefix/2001:db8::/ipv6-prefix-length/64",
                category="ipv6_nd_prefix_management",
                module="ipv6_nd",
                description="獲取企業級IPv6前綴條目"
            ),
            
            # 刪除特定IPv6前綴
            self.create_test_case(
                name="ipv6_nd_delete_specific_prefix",
                method="DELETE",
                url="/api/v1/ipv6/nd/prefix/vlans/1/ipv6-prefix/2011:1dbf::/ipv6-prefix-length/35",
                category="ipv6_nd_prefix_management",
                module="ipv6_nd",
                description="刪除特定IPv6前綴"
            ),
            
            # 刪除企業級IPv6前綴
            self.create_test_case(
                name="ipv6_nd_delete_enterprise_prefix",
                method="DELETE",
                url="/api/v1/ipv6/nd/prefix/vlans/100/ipv6-prefix/2001:db8::/ipv6-prefix-length/64",
                category="ipv6_nd_prefix_management",
                module="ipv6_nd",
                description="刪除企業級IPv6前綴"
            ),
            
            # 刪除數據中心IPv6前綴
            self.create_test_case(
                name="ipv6_nd_delete_datacenter_prefix",
                method="DELETE",
                url="/api/v1/ipv6/nd/prefix/vlans/200/ipv6-prefix/2001:db8:1::/ipv6-prefix-length/48",
                category="ipv6_nd_prefix_management",
                module="ipv6_nd",
                description="刪除數據中心IPv6前綴"
            ),
            
            # 刪除最小生命週期IPv6前綴
            self.create_test_case(
                name="ipv6_nd_delete_minimum_lifetime_prefix",
                method="DELETE",
                url="/api/v1/ipv6/nd/prefix/vlans/300/ipv6-prefix/2001:db8:2::/ipv6-prefix-length/56",
                category="ipv6_nd_prefix_management",
                module="ipv6_nd",
                description="刪除最小生命週期IPv6前綴"
            ),
            
            # 驗證前綴條目刪除結果
            self.create_test_case(
                name="ipv6_nd_verify_prefix_entries_deleted",
                method="GET",
                url="/api/v1/ipv6/nd/prefix/vlans",
                category="ipv6_nd_prefix_management",
                module="ipv6_nd",
                description="驗證前綴條目刪除結果"
            )
        ]
    
    def get_ipv6_nd_advanced_operations_tests(self) -> List[APITestCase]:
        """IPv6 ND Advanced Operations API 測試案例"""
        return [
            # 配置企業級IPv6 ND環境
            self.create_test_case(
                name="ipv6_nd_configure_enterprise_environment",
                method="PUT",
                url="/api/v1/ipv6/nd",
                category="ipv6_nd_advanced_operations",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_enterprise_environment', {
                    "hopLimit": 128
                }),
                description="配置企業級IPv6 ND環境"
            ),
            
            # 批量配置多個VLAN - VLAN 50
            self.create_test_case(
                name="ipv6_nd_batch_configure_vlan_50",
                method="PUT",
                url="/api/v1/ipv6/nd/vlans/50",
                category="ipv6_nd_advanced_operations",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_batch_vlan_50', {
                    "dadAttemptsCount": 3,
                    "managedConfigFlagStatus": True,
                    "otherConfigFlagStatus": False,
                    "nsInterval": 2000,
                    "reachableTime": 15000,
                    "raMinInterval": 100,
                    "raMaxInterval": 300,
                    "raLifetime": 1000,
                    "raPreferenceLevel": "medium",
                    "raSuppressStatus": False
                }),
                description="批量配置VLAN 50"
            ),
            
            # 批量配置多個VLAN - VLAN 60
            self.create_test_case(
                name="ipv6_nd_batch_configure_vlan_60",
                method="PUT",
                url="/api/v1/ipv6/nd/vlans/60",
                category="ipv6_nd_advanced_operations",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_batch_vlan_60', {
                    "dadAttemptsCount": 2,
                    "managedConfigFlagStatus": False,
                    "otherConfigFlagStatus": True,
                    "nsInterval": 5000,
                    "reachableTime": 20000,
                    "raMinInterval": 150,
                    "raMaxInterval": 450,
                    "raLifetime": 1500,
                    "raPreferenceLevel": "high",
                    "raSuppressStatus": True
                }),
                description="批量配置VLAN 60"
            ),
            
            # 配置高安全性接口策略
            self.create_test_case(
                name="ipv6_nd_configure_high_security_interfaces",
                method="PUT",
                url="/api/v1/ipv6/nd/interfaces/eth1%2f30",
                category="ipv6_nd_advanced_operations",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_high_security_interface', {
                    "raguardStatus": True
                }),
                description="配置高安全性接口策略"
            ),
            
            # 批量添加靜態鄰居 - 鄰居1
            self.create_test_case(
                name="ipv6_nd_batch_add_static_neighbor_1",
                method="POST",
                url="/api/v1/ipv6/nd/neighbors",
                category="ipv6_nd_advanced_operations",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_batch_static_neighbor_1', {
                    "type": "static",
                    "vlanId": 50,
                    "ipv6Address": "2001:db8:50::1",
                    "linkLayerAddress": "50-50-50-50-50-50"
                }),
                description="批量添加靜態鄰居 - 鄰居1"
            ),
            
            # 批量添加靜態鄰居 - 鄰居2
            self.create_test_case(
                name="ipv6_nd_batch_add_static_neighbor_2",
                method="POST",
                url="/api/v1/ipv6/nd/neighbors",
                category="ipv6_nd_advanced_operations",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_batch_static_neighbor_2', {
                    "type": "static",
                    "vlanId": 60,
                    "ipv6Address": "2001:db8:60::1",
                    "linkLayerAddress": "60-60-60-60-60-60"
                }),
                description="批量添加靜態鄰居 - 鄰居2"
            ),
            
            # 批量添加IPv6前綴 - 前綴1
            self.create_test_case(
                name="ipv6_nd_batch_add_prefix_1",
                method="POST",
                url="/api/v1/ipv6/nd/prefix/vlans",
                category="ipv6_nd_advanced_operations",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_batch_prefix_1', {
                    "vlanId": 50,
                    "ipv6Prefix": "2001:db8:50::",
                    "ipv6PrefixLength": 64,
                    "validLifetime": 3600,
                    "preferredLifetime": 1800,
                    "configureType": "no-autoconfig"
                }),
                description="批量添加IPv6前綴 - 前綴1"
            ),
            
            # 批量添加IPv6前綴 - 前綴2
            self.create_test_case(
                name="ipv6_nd_batch_add_prefix_2",
                method="POST",
                url="/api/v1/ipv6/nd/prefix/vlans",
                category="ipv6_nd_advanced_operations",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_batch_prefix_2', {
                    "vlanId": 60,
                    "ipv6Prefix": "2001:db8:60::",
                    "ipv6PrefixLength": 64,
                    "validLifetime": 7200,
                    "preferredLifetime": 3600,
                    "configureType": "off-link"
                }),
                description="批量添加IPv6前綴 - 前綴2"
            ),
            
            # 執行綜合清理操作 - 動態鄰居
            self.create_test_case(
                name="ipv6_nd_comprehensive_cleanup_dynamic_neighbors",
                method="PUT",
                url="/api/v1/ipv6/nd/neighbors/dynamic:clear",
                category="ipv6_nd_advanced_operations",
                module="ipv6_nd",
                body={},
                description="執行綜合清理操作 - 動態鄰居"
            ),
            
            # 驗證高級操作結果 - 全局配置
            self.create_test_case(
                name="ipv6_nd_verify_advanced_operations_global",
                method="GET",
                url="/api/v1/ipv6/nd",
                category="ipv6_nd_advanced_operations",
                module="ipv6_nd",
                description="驗證高級操作結果 - 全局配置"
            ),
            
            # 驗證高級操作結果 - VLAN配置
            self.create_test_case(
                name="ipv6_nd_verify_advanced_operations_vlan",
                method="GET",
                url="/api/v1/ipv6/nd/vlans/50",
                category="ipv6_nd_advanced_operations",
                module="ipv6_nd",
                description="驗證高級操作結果 - VLAN配置"
            ),
            
            # 驗證高級操作結果 - 接口配置
            self.create_test_case(
                name="ipv6_nd_verify_advanced_operations_interface",
                method="GET",
                url="/api/v1/ipv6/nd/interfaces/eth1%2f30",
                category="ipv6_nd_advanced_operations",
                module="ipv6_nd",
                description="驗證高級操作結果 - 接口配置"
            ),
            
            # 驗證高級操作結果 - 鄰居表
            self.create_test_case(
                name="ipv6_nd_verify_advanced_operations_neighbors",
                method="GET",
                url="/api/v1/ipv6/nd/neighbors",
                category="ipv6_nd_advanced_operations",
                module="ipv6_nd",
                description="驗證高級操作結果 - 鄰居表"
            ),
            
            # 驗證高級操作結果 - 前綴表
            self.create_test_case(
                name="ipv6_nd_verify_advanced_operations_prefixes",
                method="GET",
                url="/api/v1/ipv6/nd/prefix/vlans",
                category="ipv6_nd_advanced_operations",
                module="ipv6_nd",
                description="驗證高級操作結果 - 前綴表"
            )
        ]
    
    def get_ipv6_nd_error_handling_tests(self) -> List[APITestCase]:
        """IPv6 ND Error Handling API 測試案例"""
        return [
            # 測試無效的hop limit - 小於最小值
            self.create_test_case(
                name="ipv6_nd_test_invalid_hop_limit_below_minimum",
                method="PUT",
                url="/api/v1/ipv6/nd",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_invalid_hop_limit_below_min', {
                    "hopLimit": 0  # 小於最小值 (1)
                }),
                expected_status=400,
                description="測試無效的hop limit - 小於最小值 (<1)"
            ),
            
            # 測試無效的hop limit - 超出最大值
            self.create_test_case(
                name="ipv6_nd_test_invalid_hop_limit_above_maximum",
                method="PUT",
                url="/api/v1/ipv6/nd",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_invalid_hop_limit_above_max', {
                    "hopLimit": 256  # 超出最大值 (255)
                }),
                expected_status=400,
                description="測試無效的hop limit - 超出最大值 (>255)"
            ),
            
            # 測試無效的VLAN ID - 超出範圍
            self.create_test_case(
                name="ipv6_nd_test_invalid_vlan_id_out_of_range",
                method="PUT",
                url="/api/v1/ipv6/nd/vlans/5000",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_invalid_vlan_id', {
                    "dadAttemptsCount": 1
                }),
                expected_status=400,
                description="測試無效的VLAN ID - 超出範圍 (>4094)"
            ),
            
            # 測試無效的DAD嘗試次數 - 超出最大值
            self.create_test_case(
                name="ipv6_nd_test_invalid_dad_attempts_above_maximum",
                method="PUT",
                url="/api/v1/ipv6/nd/vlans/1",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_invalid_dad_attempts_above_max', {
                    "dadAttemptsCount": 700  # 超出最大值 (600)
                }),
                expected_status=400,
                description="測試無效的DAD嘗試次數 - 超出最大值 (>600)"
            ),
            
            # 測試無效的NS間隔 - 小於最小值
            self.create_test_case(
                name="ipv6_nd_test_invalid_ns_interval_below_minimum",
                method="PUT",
                url="/api/v1/ipv6/nd/vlans/1",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_invalid_ns_interval_below_min', {
                    "nsInterval": 500  # 小於最小值 (1000)
                }),
                expected_status=400,
                description="測試無效的NS間隔 - 小於最小值 (<1000)"
            ),
            
            # 測試無效的NS間隔 - 超出最大值
            self.create_test_case(
                name="ipv6_nd_test_invalid_ns_interval_above_maximum",
                method="PUT",
                url="/api/v1/ipv6/nd/vlans/1",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_invalid_ns_interval_above_max', {
                    "nsInterval": 4000000  # 超出最大值 (3600000)
                }),
                expected_status=400,
                description="測試無效的NS間隔 - 超出最大值 (>3600000)"
            ),
            
            # 測試無效的RA間隔 - 最小值大於最大值
            self.create_test_case(
                name="ipv6_nd_test_invalid_ra_interval_min_greater_than_max",
                method="PUT",
                url="/api/v1/ipv6/nd/vlans/1",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_invalid_ra_interval_min_greater_max', {
                    "raMinInterval": 1000,
                    "raMaxInterval": 500  # 最大值小於最小值
                }),
                expected_status=400,
                description="測試無效的RA間隔 - 最小值大於最大值"
            ),
            
            # 測試無效的RA最大間隔 - 小於最小值
            self.create_test_case(
                name="ipv6_nd_test_invalid_ra_max_interval_below_minimum",
                method="PUT",
                url="/api/v1/ipv6/nd/vlans/1",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_invalid_ra_max_interval_below_min', {
                    "raMaxInterval": 3  # 小於最小值 (4)
                }),
                expected_status=400,
                description="測試無效的RA最大間隔 - 小於最小值 (<4)"
            ),
            
            # 測試無效的RA最大間隔 - 超出最大值
            self.create_test_case(
                name="ipv6_nd_test_invalid_ra_max_interval_above_maximum",
                method="PUT",
                url="/api/v1/ipv6/nd/vlans/1",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_invalid_ra_max_interval_above_max', {
                    "raMaxInterval": 2000  # 超出最大值 (1800)
                }),
                expected_status=400,
                description="測試無效的RA最大間隔 - 超出最大值 (>1800)"
            ),
            
            # 測試無效的RA生命週期 - 超出最大值
            self.create_test_case(
                name="ipv6_nd_test_invalid_ra_lifetime_above_maximum",
                method="PUT",
                url="/api/v1/ipv6/nd/vlans/1",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_invalid_ra_lifetime_above_max', {
                    "raLifetime": 10000  # 超出最大值 (9000)
                }),
                expected_status=400,
                description="測試無效的RA生命週期 - 超出最大值 (>9000)"
            ),
            
            # 測試無效的RA偏好級別
            self.create_test_case(
                name="ipv6_nd_test_invalid_ra_preference_level",
                method="PUT",
                url="/api/v1/ipv6/nd/vlans/1",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_invalid_ra_preference_level', {
                    "raPreferenceLevel": "invalid"  # 無效偏好級別
                }),
                expected_status=400,
                description="測試無效的RA偏好級別 (非high/medium/low)"
            ),
            
            # 測試無效的接口ID格式
            self.create_test_case(
                name="ipv6_nd_test_invalid_interface_id_format",
                method="GET",
                url="/api/v1/ipv6/nd/interfaces/invalid_interface",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                expected_status=400,
                description="測試無效的接口ID格式"
            ),
            
            # 測試超出範圍的接口ID
            self.create_test_case(
                name="ipv6_nd_test_out_of_range_interface_id",
                method="GET",
                url="/api/v1/ipv6/nd/interfaces/eth9%2f99",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                expected_status=400,
                description="測試超出範圍的接口ID"
            ),
            
            # 測試無效的IPv6地址格式 - 鄰居
            self.create_test_case(
                name="ipv6_nd_test_invalid_ipv6_address_neighbor",
                method="POST",
                url="/api/v1/ipv6/nd/neighbors",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_invalid_ipv6_address_neighbor', {
                    "type": "static",
                    "vlanId": 1,
                    "ipv6Address": "invalid::ipv6::address",
                    "linkLayerAddress": "aa-bb-cc-dd-ee-ff"
                }),
                expected_status=400,
                description="測試無效的IPv6地址格式 - 鄰居"
            ),
            
            # 測試無效的MAC地址格式
            self.create_test_case(
                name="ipv6_nd_test_invalid_mac_address_format",
                method="POST",
                url="/api/v1/ipv6/nd/neighbors",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_invalid_mac_address_format', {
                    "type": "static",
                    "vlanId": 1,
                    "ipv6Address": "fe80::1",
                    "linkLayerAddress": "invalid-mac-address"
                }),
                expected_status=400,
                description="測試無效的MAC地址格式"
            ),
            
            # 測試無效的前綴長度 - 超出範圍
            self.create_test_case(
                name="ipv6_nd_test_invalid_prefix_length_out_of_range",
                method="POST",
                url="/api/v1/ipv6/nd/prefix/vlans",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_invalid_prefix_length_out_of_range', {
                    "vlanId": 1,
                    "ipv6Prefix": "2001:db8::",
                    "ipv6PrefixLength": 129,  # 超出範圍 (>128)
                    "validLifetime": 1000,
                    "preferredLifetime": 900
                }),
                expected_status=400,
                description="測試無效的前綴長度 - 超出範圍 (>128)"
            ),
            
            # 測試無效的生命週期 - 偏好生命週期大於有效生命週期
            self.create_test_case(
                name="ipv6_nd_test_invalid_lifetime_preferred_greater_than_valid",
                method="POST",
                url="/api/v1/ipv6/nd/prefix/vlans",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_invalid_lifetime_preferred_greater_valid', {
                    "vlanId": 1,
                    "ipv6Prefix": "2001:db8::",
                    "ipv6PrefixLength": 64,
                    "validLifetime": 1000,
                    "preferredLifetime": 2000  # 偏好生命週期大於有效生命週期
                }),
                expected_status=400,
                description="測試無效的生命週期 - 偏好生命週期大於有效生命週期"
            ),
            
            # 測試無效JSON格式 - 全局配置
            self.create_test_case(
                name="ipv6_nd_test_invalid_json_global_config",
                method="PUT",
                url="/api/v1/ipv6/nd",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body="invalid json format",
                expected_status=400,
                description="測試無效JSON格式 - 全局配置"
            ),
            
            # 測試無效JSON格式 - VLAN配置
            self.create_test_case(
                name="ipv6_nd_test_invalid_json_vlan_config",
                method="PUT",
                url="/api/v1/ipv6/nd/vlans/1",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body="{ invalid json }",
                expected_status=400,
                description="測試無效JSON格式 - VLAN配置"
            ),
            
            # 測試不存在的VLAN
            self.create_test_case(
                name="ipv6_nd_test_nonexistent_vlan",
                method="PUT",
                url="/api/v1/ipv6/nd/vlans/999",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_nonexistent_vlan', {
                    "dadAttemptsCount": 1
                }),
                expected_status=500,
                description="測試不存在的VLAN"
            ),
            
            # 測試不存在的鄰居條目 - 獲取
            self.create_test_case(
                name="ipv6_nd_test_nonexistent_neighbor_get",
                method="GET",
                url="/api/v1/ipv6/nd/neighbors/types/static/ipv6-address/fe80::nonexistent/vlans/1",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                expected_status=500,
                description="測試不存在的鄰居條目 - 獲取"
            ),
            
            # 測試不存在的鄰居條目 - 刪除
            self.create_test_case(
                name="ipv6_nd_test_nonexistent_neighbor_delete",
                method="DELETE",
                url="/api/v1/ipv6/nd/neighbors/types/static/ipv6-address/fe80::nonexistent/vlans/1",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                expected_status=500,
                description="測試不存在的鄰居條目 - 刪除"
            ),
            
            # 測試不存在的前綴條目 - 獲取
            self.create_test_case(
                name="ipv6_nd_test_nonexistent_prefix_get",
                method="GET",
                url="/api/v1/ipv6/nd/prefix/vlans/1/ipv6-prefix/2001:db8:nonexistent::/ipv6-prefix-length/64",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                expected_status=500,
                description="測試不存在的前綴條目 - 獲取"
            ),
            
            # 測試不存在的前綴條目 - 刪除
            self.create_test_case(
                name="ipv6_nd_test_nonexistent_prefix_delete",
                method="DELETE",
                url="/api/v1/ipv6/nd/prefix/vlans/1/ipv6-prefix/2001:db8:nonexistent::/ipv6-prefix-length/64",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                expected_status=500,
                description="測試不存在的前綴條目 - 刪除"
            ),
            
            # 恢復正常IPv6 ND配置
            self.create_test_case(
                name="ipv6_nd_restore_normal_configuration",
                method="PUT",
                url="/api/v1/ipv6/nd",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                body=self.test_data.get('ipv6_nd_restore_normal_config', {
                    "hopLimit": 64
                }),
                description="恢復正常IPv6 ND配置"
            ),
            
            # 最終IPv6 ND狀態檢查
            self.create_test_case(
                name="ipv6_nd_final_status_check",
                method="GET",
                url="/api/v1/ipv6/nd",
                category="ipv6_nd_error_handling",
                module="ipv6_nd",
                description="最終IPv6 ND狀態檢查"
            )
        ]