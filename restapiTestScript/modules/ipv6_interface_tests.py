#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IPv6 Interface 模組測試案例
包含IPv6默認網關管理、IPv6地址配置、VLAN IPv6管理、網路統計、流量計數器等相關API測試
支援默認網關設置、IPv6地址類型管理、VLAN IPv6狀態配置、ICMPv6/UDPv6統計、流量計數器重置等操作
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class IPV6_INTERFACETests(BaseTests):
    """IPv6 Interface 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取IPv6 Interface模組支援的類別"""
        return [
            "ipv6_interface_default_gateway_management",
            "ipv6_interface_address_management",
            "ipv6_interface_vlan_management",
            "ipv6_interface_traffic_statistics",
            "ipv6_interface_traffic_counter_management",
            "ipv6_interface_advanced_operations",
            "ipv6_interface_error_handling"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有IPv6 Interface測試案例"""
        all_tests = []
        all_tests.extend(self.get_ipv6_interface_default_gateway_management_tests())
        all_tests.extend(self.get_ipv6_interface_address_management_tests())
        all_tests.extend(self.get_ipv6_interface_vlan_management_tests())
        all_tests.extend(self.get_ipv6_interface_traffic_statistics_tests())
        all_tests.extend(self.get_ipv6_interface_traffic_counter_management_tests())
        all_tests.extend(self.get_ipv6_interface_advanced_operations_tests())
        all_tests.extend(self.get_ipv6_interface_error_handling_tests())
        return all_tests
    
    def get_ipv6_interface_default_gateway_management_tests(self) -> List[APITestCase]:
        """IPv6 Interface Default Gateway Management API 測試案例"""
        return [
            # 獲取IPv6默認網關
            self.create_test_case(
                name="ipv6_interface_get_default_gateway",
                method="GET",
                url="/api/v1/ipv6",
                category="ipv6_interface_default_gateway_management",
                module="ipv6_interface",
                description="獲取IPv6默認網關配置"
            ),
            
            # 設置IPv6默認網關 - 鏈路本地地址
            self.create_test_case(
                name="ipv6_interface_set_link_local_default_gateway",
                method="PUT",
                url="/api/v1/ipv6",
                category="ipv6_interface_default_gateway_management",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_link_local_gateway', {
                    "defaultGateway": "fe80::269:3ef9:fe19:6780%1"
                }),
                description="設置IPv6默認網關 - 鏈路本地地址"
            ),
            
            # 設置IPv6默認網關 - 全球單播地址
            self.create_test_case(
                name="ipv6_interface_set_global_unicast_default_gateway",
                method="PUT",
                url="/api/v1/ipv6",
                category="ipv6_interface_default_gateway_management",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_global_unicast_gateway', {
                    "defaultGateway": "2001:db8::1"
                }),
                description="設置IPv6默認網關 - 全球單播地址"
            ),
            
            # 設置IPv6默認網關 - 企業級地址
            self.create_test_case(
                name="ipv6_interface_set_enterprise_default_gateway",
                method="PUT",
                url="/api/v1/ipv6",
                category="ipv6_interface_default_gateway_management",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_enterprise_gateway', {
                    "defaultGateway": "2001:db8:1000::1"
                }),
                description="設置IPv6默認網關 - 企業級地址"
            ),
            
            # 設置IPv6默認網關 - 數據中心地址
            self.create_test_case(
                name="ipv6_interface_set_datacenter_default_gateway",
                method="PUT",
                url="/api/v1/ipv6",
                category="ipv6_interface_default_gateway_management",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_datacenter_gateway', {
                    "defaultGateway": "fd00::1"
                }),
                description="設置IPv6默認網關 - 數據中心地址"
            ),
            
            # 更新IPv6默認網關
            self.create_test_case(
                name="ipv6_interface_update_default_gateway",
                method="PUT",
                url="/api/v1/ipv6",
                category="ipv6_interface_default_gateway_management",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_update_gateway', {
                    "defaultGateway": "fe80::1%1"
                }),
                description="更新IPv6默認網關"
            ),
            
            # 移除IPv6默認網關
            self.create_test_case(
                name="ipv6_interface_remove_default_gateway",
                method="PUT",
                url="/api/v1/ipv6",
                category="ipv6_interface_default_gateway_management",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_remove_gateway', {
                    "defaultGateway": ""
                }),
                description="移除IPv6默認網關"
            ),
            
            # 重新設置IPv6默認網關
            self.create_test_case(
                name="ipv6_interface_restore_default_gateway",
                method="PUT",
                url="/api/v1/ipv6",
                category="ipv6_interface_default_gateway_management",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_restore_gateway', {
                    "defaultGateway": "fe80::269:3ef9:fe19:6780%1"
                }),
                description="重新設置IPv6默認網關"
            ),
            
            # 驗證IPv6默認網關配置
            self.create_test_case(
                name="ipv6_interface_verify_default_gateway_configuration",
                method="GET",
                url="/api/v1/ipv6",
                category="ipv6_interface_default_gateway_management",
                module="ipv6_interface",
                description="驗證IPv6默認網關配置"
            )
        ]
    
    def get_ipv6_interface_address_management_tests(self) -> List[APITestCase]:
        """IPv6 Interface Address Management API 測試案例"""
        return [
            # 獲取IPv6地址信息
            self.create_test_case(
                name="ipv6_interface_get_address_information",
                method="GET",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_address_management",
                module="ipv6_interface",
                description="獲取IPv6地址信息"
            ),
            
            # 設置VLAN 1的鏈路本地地址
            self.create_test_case(
                name="ipv6_interface_set_vlan_1_link_local_address",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_address_management",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_vlan_1_link_local', {
                    "vlanId": 1,
                    "ipv6Address": "fe80::269:3ef9:fe19:6779",
                    "ipv6PrefixLength": 64,
                    "type": "link-local"
                }),
                description="設置VLAN 1的鏈路本地地址"
            ),
            
            # 設置VLAN 1的EUI-64地址
            self.create_test_case(
                name="ipv6_interface_set_vlan_1_eui64_address",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_address_management",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_vlan_1_eui64', {
                    "vlanId": 1,
                    "ipv6Address": "2001:0db8:0:1::",
                    "ipv6PrefixLength": 64,
                    "type": "eui-64"
                }),
                description="設置VLAN 1的EUI-64地址"
            ),
            
            # 設置VLAN 100的全球單播地址
            self.create_test_case(
                name="ipv6_interface_set_vlan_100_global_unicast_address",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_address_management",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_vlan_100_global_unicast', {
                    "vlanId": 100,
                    "ipv6Address": "2001:db8:2222:7272::72",
                    "ipv6PrefixLength": 96,
                    "type": "global-unicast"
                }),
                description="設置VLAN 100的全球單播地址"
            ),
            
            # 設置VLAN 200的企業級IPv6地址
            self.create_test_case(
                name="ipv6_interface_set_vlan_200_enterprise_address",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_address_management",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_vlan_200_enterprise', {
                    "vlanId": 200,
                    "ipv6Address": "2001:db8:1000::1",
                    "ipv6PrefixLength": 64,
                    "type": "global-unicast"
                }),
                description="設置VLAN 200的企業級IPv6地址"
            ),
            
            # 設置VLAN 500的數據中心IPv6地址
            self.create_test_case(
                name="ipv6_interface_set_vlan_500_datacenter_address",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_address_management",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_vlan_500_datacenter', {
                    "vlanId": 500,
                    "ipv6Address": "fd00::500:1",
                    "ipv6PrefixLength": 64,
                    "type": "global-unicast"
                }),
                description="設置VLAN 500的數據中心IPv6地址"
            ),
            
            # 獲取特定IPv6地址信息 - 鏈路本地
            self.create_test_case(
                name="ipv6_interface_get_specific_link_local_address",
                method="GET",
                url="/api/v1/ipv6/address/vlans/1/ipv6-address/fe80::269:3ef9:fe19:6779/ipv6-prefix-length/64/types/link-local",
                category="ipv6_interface_address_management",
                module="ipv6_interface",
                description="獲取特定IPv6地址信息 - 鏈路本地"
            ),
            
            # 獲取特定IPv6地址信息 - 全球單播
            self.create_test_case(
                name="ipv6_interface_get_specific_global_unicast_address",
                method="GET",
                url="/api/v1/ipv6/address/vlans/100/ipv6-address/2001:db8:2222:7272::72/ipv6-prefix-length/96/types/global-unicast",
                category="ipv6_interface_address_management",
                module="ipv6_interface",
                description="獲取特定IPv6地址信息 - 全球單播"
            ),
            
            # 刪除VLAN 100的IPv6地址
            self.create_test_case(
                name="ipv6_interface_delete_vlan_100_address",
                method="DELETE",
                url="/api/v1/ipv6/address/vlans/100/ipv6-address/2001:db8:2222:7272::72/ipv6-prefix-length/96/types/global-unicast",
                category="ipv6_interface_address_management",
                module="ipv6_interface",
                description="刪除VLAN 100的IPv6地址"
            ),
            
            # 刪除VLAN 200的IPv6地址
            self.create_test_case(
                name="ipv6_interface_delete_vlan_200_address",
                method="DELETE",
                url="/api/v1/ipv6/address/vlans/200/ipv6-address/2001:db8:1000::1/ipv6-prefix-length/64/types/global-unicast",
                category="ipv6_interface_address_management",
                module="ipv6_interface",
                description="刪除VLAN 200的IPv6地址"
            ),
            
            # 驗證IPv6地址配置
            self.create_test_case(
                name="ipv6_interface_verify_address_configuration",
                method="GET",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_address_management",
                module="ipv6_interface",
                description="驗證IPv6地址配置"
            )
        ]
    
    def get_ipv6_interface_vlan_management_tests(self) -> List[APITestCase]:
        """IPv6 Interface VLAN Management API 測試案例"""
        return [
            # 獲取VLAN 1的IPv6狀態和MTU
            self.create_test_case(
                name="ipv6_interface_get_vlan_1_status_mtu",
                method="GET",
                url="/api/v1/ipv6/vlans/1",
                category="ipv6_interface_vlan_management",
                module="ipv6_interface",
                description="獲取VLAN 1的IPv6狀態和MTU"
            ),
            
            # 獲取VLAN 100的IPv6狀態和MTU
            self.create_test_case(
                name="ipv6_interface_get_vlan_100_status_mtu",
                method="GET",
                url="/api/v1/ipv6/vlans/100",
                category="ipv6_interface_vlan_management",
                module="ipv6_interface",
                description="獲取VLAN 100的IPv6狀態和MTU"
            ),
            
            # 設置VLAN 1的IPv6狀態和MTU - 啟用
            self.create_test_case(
                name="ipv6_interface_set_vlan_1_enable_default_mtu",
                method="PUT",
                url="/api/v1/ipv6/vlans/1",
                category="ipv6_interface_vlan_management",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_vlan_1_enable_default_mtu', {
                    "ipv6Status": True,
                    "mtu": 1500
                }),
                description="設置VLAN 1的IPv6狀態和MTU - 啟用"
            ),
            
            # 設置VLAN 100的IPv6狀態和MTU - 最小MTU
            self.create_test_case(
                name="ipv6_interface_set_vlan_100_enable_min_mtu",
                method="PUT",
                url="/api/v1/ipv6/vlans/100",
                category="ipv6_interface_vlan_management",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_vlan_100_enable_min_mtu', {
                    "ipv6Status": True,
                    "mtu": 1280
                }),
                description="設置VLAN 100的IPv6狀態和MTU - 最小MTU"
            ),
            
            # 設置VLAN 200的IPv6狀態和MTU - 大MTU
            self.create_test_case(
                name="ipv6_interface_set_vlan_200_enable_large_mtu",
                method="PUT",
                url="/api/v1/ipv6/vlans/200",
                category="ipv6_interface_vlan_management",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_vlan_200_enable_large_mtu', {
                    "ipv6Status": True,
                    "mtu": 9000
                }),
                description="設置VLAN 200的IPv6狀態和MTU - 大MTU"
            ),
            
            # 設置VLAN 500的IPv6狀態和MTU - 企業級配置
            self.create_test_case(
                name="ipv6_interface_set_vlan_500_enterprise_config",
                method="PUT",
                url="/api/v1/ipv6/vlans/500",
                category="ipv6_interface_vlan_management",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_vlan_500_enterprise_config', {
                    "ipv6Status": True,
                    "mtu": 1500
                }),
                description="設置VLAN 500的IPv6狀態和MTU - 企業級配置"
            ),
            
            # 禁用VLAN 300的IPv6
            self.create_test_case(
                name="ipv6_interface_disable_vlan_300_ipv6",
                method="PUT",
                url="/api/v1/ipv6/vlans/300",
                category="ipv6_interface_vlan_management",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_vlan_300_disable', {
                    "ipv6Status": False
                }),
                description="禁用VLAN 300的IPv6"
            ),
            
            # 更新VLAN 100的MTU
            self.create_test_case(
                name="ipv6_interface_update_vlan_100_mtu",
                method="PUT",
                url="/api/v1/ipv6/vlans/100",
                category="ipv6_interface_vlan_management",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_vlan_100_update_mtu', {
                    "mtu": 1500
                }),
                description="更新VLAN 100的MTU"
            ),
            
            # 驗證VLAN IPv6配置更新
            self.create_test_case(
                name="ipv6_interface_verify_vlan_configuration_update",
                method="GET",
                url="/api/v1/ipv6/vlans/1",
                category="ipv6_interface_vlan_management",
                module="ipv6_interface",
                description="驗證VLAN IPv6配置更新"
            ),
            
            # 驗證VLAN 100配置更新
            self.create_test_case(
                name="ipv6_interface_verify_vlan_100_configuration_update",
                method="GET",
                url="/api/v1/ipv6/vlans/100",
                category="ipv6_interface_vlan_management",
                module="ipv6_interface",
                description="驗證VLAN 100配置更新"
            )
        ]
    
    def get_ipv6_interface_traffic_statistics_tests(self) -> List[APITestCase]:
        """IPv6 Interface Traffic Statistics API 測試案例"""
        return [
            # 獲取IPv6流量統計
            self.create_test_case(
                name="ipv6_interface_get_traffic_statistics",
                method="GET",
                url="/api/v1/ipv6/traffics",
                category="ipv6_interface_traffic_statistics",
                module="ipv6_interface",
                description="獲取IPv6流量統計"
            ),
            
            # 多次獲取統計信息以檢查一致性
            self.create_test_case(
                name="ipv6_interface_get_traffic_statistics_consistency_check",
                method="GET",
                url="/api/v1/ipv6/traffics",
                category="ipv6_interface_traffic_statistics",
                module="ipv6_interface",
                description="多次獲取統計信息以檢查一致性"
            ),
            
            # 驗證IPv6統計信息響應格式
            self.create_test_case(
                name="ipv6_interface_verify_traffic_statistics_response_format",
                method="GET",
                url="/api/v1/ipv6/traffics",
                category="ipv6_interface_traffic_statistics",
                module="ipv6_interface",
                description="驗證IPv6統計信息響應格式"
            ),
            
            # 檢查IPv6接收統計完整性
            self.create_test_case(
                name="ipv6_interface_check_ipv6_receive_statistics_completeness",
                method="GET",
                url="/api/v1/ipv6/traffics",
                category="ipv6_interface_traffic_statistics",
                module="ipv6_interface",
                description="檢查IPv6接收統計完整性"
            ),
            
            # 檢查IPv6發送統計完整性
            self.create_test_case(
                name="ipv6_interface_check_ipv6_send_statistics_completeness",
                method="GET",
                url="/api/v1/ipv6/traffics",
                category="ipv6_interface_traffic_statistics",
                module="ipv6_interface",
                description="檢查IPv6發送統計完整性"
            ),
            
            # 檢查ICMPv6統計完整性
            self.create_test_case(
                name="ipv6_interface_check_icmpv6_statistics_completeness",
                method="GET",
                url="/api/v1/ipv6/traffics",
                category="ipv6_interface_traffic_statistics",
                module="ipv6_interface",
                description="檢查ICMPv6統計完整性"
            ),
            
            # 檢查UDPv6統計完整性
            self.create_test_case(
                name="ipv6_interface_check_udpv6_statistics_completeness",
                method="GET",
                url="/api/v1/ipv6/traffics",
                category="ipv6_interface_traffic_statistics",
                module="ipv6_interface",
                description="檢查UDPv6統計完整性"
            )
        ]
    
    def get_ipv6_interface_traffic_counter_management_tests(self) -> List[APITestCase]:
        """IPv6 Interface Traffic Counter Management API 測試案例"""
        return [
            # 重置IPv6流量計數器
            self.create_test_case(
                name="ipv6_interface_reset_traffic_counters",
                method="PUT",
                url="/api/v1/ipv6/traffics:clear",
                category="ipv6_interface_traffic_counter_management",
                module="ipv6_interface",
                body={},
                description="重置IPv6流量計數器"
            ),
            
            # 驗證流量計數器重置結果
            self.create_test_case(
                name="ipv6_interface_verify_traffic_counters_reset",
                method="GET",
                url="/api/v1/ipv6/traffics",
                category="ipv6_interface_traffic_counter_management",
                module="ipv6_interface",
                description="驗證流量計數器重置結果"
            ),
            
            # 再次重置流量計數器（確保操作冪等性）
            self.create_test_case(
                name="ipv6_interface_reset_traffic_counters_idempotent",
                method="PUT",
                url="/api/v1/ipv6/traffics:clear",
                category="ipv6_interface_traffic_counter_management",
                module="ipv6_interface",
                body={},
                description="再次重置流量計數器（確保操作冪等性）"
            ),
            
            # 驗證計數器重置後的統計信息
            self.create_test_case(
                name="ipv6_interface_verify_statistics_after_reset",
                method="GET",
                url="/api/v1/ipv6/traffics",
                category="ipv6_interface_traffic_counter_management",
                module="ipv6_interface",
                description="驗證計數器重置後的統計信息"
            )
        ]
    
    def get_ipv6_interface_advanced_operations_tests(self) -> List[APITestCase]:
        """IPv6 Interface Advanced Operations API 測試案例"""
        return [
            # 配置企業級IPv6網路環境
            self.create_test_case(
                name="ipv6_interface_configure_enterprise_network_environment",
                method="PUT",
                url="/api/v1/ipv6",
                category="ipv6_interface_advanced_operations",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_enterprise_network_gateway', {
                    "defaultGateway": "2001:db8:1000::254"
                }),
                description="配置企業級IPv6網路環境默認網關"
            ),
            
            # 批量配置多個VLAN的IPv6地址 - VLAN 10
            self.create_test_case(
                name="ipv6_interface_batch_configure_vlan_10_address",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_advanced_operations",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_batch_vlan_10', {
                    "vlanId": 10,
                    "ipv6Address": "2001:db8:10::1",
                    "ipv6PrefixLength": 64,
                    "type": "global-unicast"
                }),
                description="批量配置VLAN 10的IPv6地址"
            ),
            
            # 批量配置多個VLAN的IPv6地址 - VLAN 20
            self.create_test_case(
                name="ipv6_interface_batch_configure_vlan_20_address",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_advanced_operations",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_batch_vlan_20', {
                    "vlanId": 20,
                    "ipv6Address": "2001:db8:20::1",
                    "ipv6PrefixLength": 64,
                    "type": "global-unicast"
                }),
                description="批量配置VLAN 20的IPv6地址"
            ),
            
            # 批量配置多個VLAN的IPv6地址 - VLAN 30
            self.create_test_case(
                name="ipv6_interface_batch_configure_vlan_30_address",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_advanced_operations",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_batch_vlan_30', {
                    "vlanId": 30,
                    "ipv6Address": "2001:db8:30::1",
                    "ipv6PrefixLength": 64,
                    "type": "global-unicast"
                }),
                description="批量配置VLAN 30的IPv6地址"
            ),
            
            # 批量配置VLAN IPv6狀態 - VLAN 10
            self.create_test_case(
                name="ipv6_interface_batch_configure_vlan_10_status",
                method="PUT",
                url="/api/v1/ipv6/vlans/10",
                category="ipv6_interface_advanced_operations",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_batch_vlan_10_status', {
                    "ipv6Status": True,
                    "mtu": 1500
                }),
                description="批量配置VLAN 10的IPv6狀態"
            ),
            
            # 批量配置VLAN IPv6狀態 - VLAN 20
            self.create_test_case(
                name="ipv6_interface_batch_configure_vlan_20_status",
                method="PUT",
                url="/api/v1/ipv6/vlans/20",
                category="ipv6_interface_advanced_operations",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_batch_vlan_20_status', {
                    "ipv6Status": True,
                    "mtu": 1500
                }),
                description="批量配置VLAN 20的IPv6狀態"
            ),
            
            # 配置多子網IPv6環境 - VLAN 50 EUI-64
            self.create_test_case(
                name="ipv6_interface_configure_multi_subnet_vlan_50_eui64",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_advanced_operations",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_multi_subnet_vlan_50_eui64', {
                    "vlanId": 50,
                    "ipv6Address": "2001:db8:50::",
                    "ipv6PrefixLength": 64,
                    "type": "eui-64"
                }),
                description="配置多子網IPv6環境 - VLAN 50 EUI-64"
            ),
            
            # 配置多子網IPv6環境 - VLAN 50全球單播
            self.create_test_case(
                name="ipv6_interface_configure_multi_subnet_vlan_50_global_unicast",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_advanced_operations",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_multi_subnet_vlan_50_global_unicast', {
                    "vlanId": 50,
                    "ipv6Address": "2001:db8:5000::1",
                    "ipv6PrefixLength": 64,
                    "type": "global-unicast"
                }),
                description="配置多子網IPv6環境 - VLAN 50全球單播"
            ),
            
            # 配置高級IPv6 MTU設置
            self.create_test_case(
                name="ipv6_interface_configure_advanced_mtu_settings",
                method="PUT",
                url="/api/v1/ipv6/vlans/50",
                category="ipv6_interface_advanced_operations",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_advanced_mtu_settings', {
                    "ipv6Status": True,
                    "mtu": 9000
                }),
                description="配置高級IPv6 MTU設置"
            ),
            
            # 動態調整IPv6網路參數
            self.create_test_case(
                name="ipv6_interface_dynamic_adjust_network_parameters",
                method="PUT",
                url="/api/v1/ipv6",
                category="ipv6_interface_advanced_operations",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_dynamic_gateway', {
                    "defaultGateway": "2001:db8::254"
                }),
                description="動態調整IPv6網路參數"
            ),
            
            # 驗證高級操作結果
            self.create_test_case(
                name="ipv6_interface_verify_advanced_operations_results",
                method="GET",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_advanced_operations",
                module="ipv6_interface",
                description="驗證高級操作結果"
            ),
            
            # 驗證VLAN高級配置結果
            self.create_test_case(
                name="ipv6_interface_verify_vlan_advanced_results",
                method="GET",
                url="/api/v1/ipv6/vlans/50",
                category="ipv6_interface_advanced_operations",
                module="ipv6_interface",
                description="驗證VLAN高級配置結果"
            )
        ]
    
    def get_ipv6_interface_error_handling_tests(self) -> List[APITestCase]:
        """IPv6 Interface Error Handling API 測試案例"""
        return [
            # 測試無效的IPv6地址格式 - 默認網關
            self.create_test_case(
                name="ipv6_interface_test_invalid_ipv6_format_gateway",
                method="PUT",
                url="/api/v1/ipv6",
                category="ipv6_interface_error_handling",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_invalid_gateway_ipv6', {
                    "defaultGateway": "invalid::ipv6::address"
                }),
                expected_status=400,
                description="測試無效的IPv6地址格式 - 默認網關"
            ),
            
            # 測試無效的VLAN ID - 超出範圍
            self.create_test_case(
                name="ipv6_interface_test_invalid_vlan_id_out_of_range",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_error_handling",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_invalid_vlan_id', {
                    "vlanId": 5000,  # 超出範圍 (1-4094)
                    "ipv6Address": "2001:db8::1",
                    "ipv6PrefixLength": 64,
                    "type": "global-unicast"
                }),
                expected_status=500,
                description="測試無效的VLAN ID - 超出範圍 (>4094)"
            ),
            
            # 測試無效的VLAN ID - 零
            self.create_test_case(
                name="ipv6_interface_test_invalid_vlan_id_zero",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_error_handling",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_invalid_vlan_id_zero', {
                    "vlanId": 0,
                    "ipv6Address": "2001:db8::1",
                    "ipv6PrefixLength": 64,
                    "type": "global-unicast"
                }),
                expected_status=500,
                description="測試無效的VLAN ID - 零"
            ),
            
            # 測試無效的IPv6地址格式 - VLAN IPv6
            self.create_test_case(
                name="ipv6_interface_test_invalid_ipv6_format_vlan",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_error_handling",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_invalid_vlan_ipv6', {
                    "vlanId": 100,
                    "ipv6Address": "invalid::ipv6::format",
                    "ipv6PrefixLength": 64,
                    "type": "global-unicast"
                }),
                expected_status=500,
                description="測試無效的IPv6地址格式 - VLAN IPv6"
            ),
            
            # 測試無效的IPv6前綴長度 - 超出範圍
            self.create_test_case(
                name="ipv6_interface_test_invalid_ipv6_prefix_length_out_of_range",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_error_handling",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_invalid_prefix_length', {
                    "vlanId": 100,
                    "ipv6Address": "2001:db8::1",
                    "ipv6PrefixLength": 200,  # 超出範圍 (0-128)
                    "type": "global-unicast"
                }),
                expected_status=500,
                description="測試無效的IPv6前綴長度 - 超出範圍 (>128)"
            ),
            
            # 測試無效的IPv6地址類型
            self.create_test_case(
                name="ipv6_interface_test_invalid_ipv6_address_type",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_error_handling",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_invalid_address_type', {
                    "vlanId": 100,
                    "ipv6Address": "2001:db8::1",
                    "ipv6PrefixLength": 64,
                    "type": "invalid-type"
                }),
                expected_status=500,
                description="測試無效的IPv6地址類型 (非eui-64/link-local/global-unicast)"
            ),
            
            # 測試無效的鏈路本地地址格式
            self.create_test_case(
                name="ipv6_interface_test_invalid_link_local_address_format",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_error_handling",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_invalid_link_local_format', {
                    "vlanId": 100,
                    "ipv6Address": "2001:db8::1",  # 不是鏈路本地地址
                    "ipv6PrefixLength": 64,
                    "type": "link-local"
                }),
                expected_status=500,
                description="測試無效的鏈路本地地址格式"
            ),
            
            # 測試無效的MTU值 - 小於最小值
            self.create_test_case(
                name="ipv6_interface_test_invalid_mtu_below_minimum",
                method="PUT",
                url="/api/v1/ipv6/vlans/100",
                category="ipv6_interface_error_handling",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_invalid_mtu_below_minimum', {
                    "ipv6Status": True,
                    "mtu": 1000  # 小於最小值 (1280)
                }),
                expected_status=500,
                description="測試無效的MTU值 - 小於最小值 (<1280)"
            ),
            
            # 測試無效的MTU值 - 超出最大值
            self.create_test_case(
                name="ipv6_interface_test_invalid_mtu_above_maximum",
                method="PUT",
                url="/api/v1/ipv6/vlans/100",
                category="ipv6_interface_error_handling",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_invalid_mtu_above_maximum', {
                    "ipv6Status": True,
                    "mtu": 70000  # 超出最大值 (65535)
                }),
                expected_status=500,
                description="測試無效的MTU值 - 超出最大值 (>65535)"
            ),
            
            # 測試無效的布爾值 - IPv6狀態
            self.create_test_case(
                name="ipv6_interface_test_invalid_boolean_ipv6_status",
                method="PUT",
                url="/api/v1/ipv6/vlans/100",
                category="ipv6_interface_error_handling",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_invalid_boolean_status', {
                    "ipv6Status": "yes",  # 無效布爾值
                    "mtu": 1500
                }),
                expected_status=500,
                description="測試無效的布爾值 - IPv6狀態"
            ),
            
            # 測試無效JSON格式 - 默認網關
            self.create_test_case(
                name="ipv6_interface_test_invalid_json_gateway",
                method="PUT",
                url="/api/v1/ipv6",
                category="ipv6_interface_error_handling",
                module="ipv6_interface",
                body="invalid json format",
                expected_status=500,
                description="測試無效JSON格式 - 默認網關"
            ),
            
            # 測試無效JSON格式 - VLAN IPv6
            self.create_test_case(
                name="ipv6_interface_test_invalid_json_vlan_ipv6",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_error_handling",
                module="ipv6_interface",
                body="{ invalid json }",
                expected_status=500,
                description="測試無效JSON格式 - VLAN IPv6"
            ),
            
            # 測試無效JSON格式 - VLAN狀態
            self.create_test_case(
                name="ipv6_interface_test_invalid_json_vlan_status",
                method="PUT",
                url="/api/v1/ipv6/vlans/100",
                category="ipv6_interface_error_handling",
                module="ipv6_interface",
                body="{ invalid: json }",
                expected_status=500,
                description="測試無效JSON格式 - VLAN狀態"
            ),
            
            # 測試缺少必需參數 - VLAN IPv6配置
            self.create_test_case(
                name="ipv6_interface_test_missing_required_params_vlan_ipv6",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_error_handling",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_missing_params_vlan_ipv6', {
                    "vlanId": 100
                    # 缺少ipv6Address, ipv6PrefixLength, type
                }),
                expected_status=500,
                description="測試缺少必需參數 - VLAN IPv6配置"
            ),
            
            # 測試不存在的VLAN
            self.create_test_case(
                name="ipv6_interface_test_nonexistent_vlan",
                method="POST",
                url="/api/v1/ipv6/address/vlans",
                category="ipv6_interface_error_handling",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_nonexistent_vlan', {
                    "vlanId": 999,  # 假設不存在的VLAN
                    "ipv6Address": "2001:db8::1",
                    "ipv6PrefixLength": 64,
                    "type": "global-unicast"
                }),
                expected_status=500,
                description="測試不存在的VLAN"
            ),
            
            # 恢復正常IPv6接口配置
            self.create_test_case(
                name="ipv6_interface_restore_normal_configuration",
                method="PUT",
                url="/api/v1/ipv6",
                category="ipv6_interface_error_handling",
                module="ipv6_interface",
                body=self.test_data.get('ipv6_interface_restore_normal_config', {
                    "defaultGateway": "fe80::269:3ef9:fe19:6780%1"
                }),
                description="恢復正常IPv6接口配置"
            ),
            
            # 最終IPv6接口狀態檢查
            self.create_test_case(
                name="ipv6_interface_final_status_check",
                method="GET",
                url="/api/v1/ipv6",
                category="ipv6_interface_error_handling",
                module="ipv6_interface",
                description="最終IPv6接口狀態檢查"
            )
        ]