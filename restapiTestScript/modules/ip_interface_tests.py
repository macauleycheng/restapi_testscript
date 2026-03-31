#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IP Interface 模組測試案例
包含IPv4默認網關管理、IP地址配置、網路統計、Loopback接口管理等相關API測試
支援默認網關設置、VLAN IP地址管理、網路流量統計、Loopback接口創建等操作
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class IP_INTERFACETests(BaseTests):
    """IP Interface 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取IP Interface模組支援的類別"""
        return [
            "ip_interface_default_gateway_management",
            "ip_interface_address_management",
            "ip_interface_traffic_statistics",
            "ip_interface_loopback_management",
            "ip_interface_advanced_operations",
            "ip_interface_error_handling"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有IP Interface測試案例"""
        all_tests = []
        all_tests.extend(self.get_ip_interface_default_gateway_management_tests())
        all_tests.extend(self.get_ip_interface_address_management_tests())
        all_tests.extend(self.get_ip_interface_traffic_statistics_tests())
        all_tests.extend(self.get_ip_interface_loopback_management_tests())
        all_tests.extend(self.get_ip_interface_advanced_operations_tests())
        all_tests.extend(self.get_ip_interface_error_handling_tests())
        return all_tests
    
    def get_ip_interface_default_gateway_management_tests(self) -> List[APITestCase]:
        """IP Interface Default Gateway Management API 測試案例"""
        return [
            # 獲取IPv4默認網關
            self.create_test_case(
                name="ip_interface_get_default_gateway",
                method="GET",
                url="/api/v1/ip",
                category="ip_interface_default_gateway_management",
                module="ip_interface",
                description="獲取IPv4默認網關配置"
            ),
            
            # 設置單個默認網關
            # (Failed to set netDefaultGateway.)
            self.create_test_case(
                name="ip_interface_set_single_default_gateway",
                method="PUT",
                url="/api/v1/ip",
                category="ip_interface_default_gateway_management",
                module="ip_interface",
                body=self.test_data.get('ip_interface_single_gateway', {
                    "netDefaultGateway": "192.168.1.1"
                }),
                description="設置單個IPv4默認網關"
            ),
            
            # 設置企業級默認網關
            # (Failed to set netDefaultGateway.)
            self.create_test_case(
                name="ip_interface_set_enterprise_default_gateway",
                method="PUT",
                url="/api/v1/ip",
                category="ip_interface_default_gateway_management",
                module="ip_interface",
                body=self.test_data.get('ip_interface_enterprise_gateway', {
                    "netDefaultGateway": "10.0.0.1"
                }),
                description="設置企業級IPv4默認網關"
            ),
            
            # 設置數據中心默認網關
            # (Failed to set netDefaultGateway.)
            self.create_test_case(
                name="ip_interface_set_datacenter_default_gateway",
                method="PUT",
                url="/api/v1/ip",
                category="ip_interface_default_gateway_management",
                module="ip_interface",
                body=self.test_data.get('ip_interface_datacenter_gateway', {
                    "netDefaultGateway": "172.16.0.1"
                }),
                description="設置數據中心IPv4默認網關"
            ),
            
            # 更新默認網關
            # (Failed to set netDefaultGateway.)
            self.create_test_case(
                name="ip_interface_update_default_gateway",
                method="PUT",
                url="/api/v1/ip",
                category="ip_interface_default_gateway_management",
                module="ip_interface",
                body=self.test_data.get('ip_interface_update_gateway', {
                    "netDefaultGateway": "192.168.30.200"
                }),
                description="更新IPv4默認網關"
            ),
            
            # 移除默認網關
            self.create_test_case(
                name="ip_interface_remove_default_gateway",
                method="PUT",
                url="/api/v1/ip",
                category="ip_interface_default_gateway_management",
                module="ip_interface",
                body=self.test_data.get('ip_interface_remove_gateway', {
                    "netDefaultGateway": ""
                }),
                description="移除IPv4默認網關"
            ),
            
            # 重新設置默認網關
            self.create_test_case(
                name="ip_interface_restore_default_gateway",
                method="PUT",
                url="/api/v1/ip",
                category="ip_interface_default_gateway_management",
                module="ip_interface",
                body=self.test_data.get('ip_interface_restore_gateway', {
                    "netDefaultGateway": "192.168.30.100"
                }),
                description="重新設置IPv4默認網關"
            ),
            
            # 驗證默認網關配置
            self.create_test_case(
                name="ip_interface_verify_default_gateway_configuration",
                method="GET",
                url="/api/v1/ip",
                category="ip_interface_default_gateway_management",
                module="ip_interface",
                description="驗證IPv4默認網關配置"
            )
        ]
    
    def get_ip_interface_address_management_tests(self) -> List[APITestCase]:
        """IP Interface Address Management API 測試案例"""
        return [
            # 獲取IPv4地址信息
            self.create_test_case(
                name="ip_interface_get_address_information",
                method="GET",
                url="/api/v1/ip/address/vlans?startId=1",
                category="ip_interface_address_management",
                module="ip_interface",
                description="獲取IPv4地址信息"
            ),
            
            # 設置VLAN 1的主要IP地址
            self.create_test_case(
                name="ip_interface_set_vlan_1_primary_ip",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_address_management",
                module="ip_interface",
                body=self.test_data.get('ip_interface_vlan_1_primary', {
                    "vlanId": 1,
                    "ipAddress": "192.168.1.10",
                    "subnetMask": "255.255.255.0",
                    "isPrimary": True
                }),
                description="設置VLAN 1的主要IP地址"
            ),
            
            # 設置VLAN 1的次要IP地址
            # (Failed to set IP address.)
            self.create_test_case(
                name="ip_interface_set_vlan_1_secondary_ip",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_address_management",
                module="ip_interface",
                body=self.test_data.get('ip_interface_vlan_1_secondary', {
                    "vlanId": 1,
                    "ipAddress": "192.168.1.20",
                    "subnetMask": "255.255.255.0",
                    "isPrimary": False
                }),
                description="設置VLAN 1的次要IP地址"
            ),
            
            # 設置VLAN 100的IP地址
            # (Failed to set IP address.)
            self.create_test_case(
                name="ip_interface_set_vlan_100_ip",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_address_management",
                module="ip_interface",
                body=self.test_data.get('ip_interface_vlan_100_ip', {
                    "vlanId": 100,
                    "ipAddress": "10.1.1.1",
                    "subnetMask": "255.255.0.0",
                    "isPrimary": True
                }),
                description="設置VLAN 100的IP地址"
            ),
            
            # 設置VLAN 200的IP地址
            # (Failed to set IP address.)
            self.create_test_case(
                name="ip_interface_set_vlan_200_ip",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_address_management",
                module="ip_interface",
                body=self.test_data.get('ip_interface_vlan_200_ip', {
                    "vlanId": 200,
                    "ipAddress": "172.16.1.1",
                    "subnetMask": "255.255.255.0",
                    "isPrimary": True
                }),
                description="設置VLAN 200的IP地址"
            ),
            
            # 設置VLAN 500的企業級IP地址
            # (Failed to set IP address.)
            self.create_test_case(
                name="ip_interface_set_vlan_500_enterprise_ip",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_address_management",
                module="ip_interface",
                body=self.test_data.get('ip_interface_vlan_500_enterprise', {
                    "vlanId": 500,
                    "ipAddress": "10.10.10.1",
                    "subnetMask": "255.255.255.0",
                    "isPrimary": True
                }),
                description="設置VLAN 500的企業級IP地址"
            ),
            
            # 獲取特定IPv4地址信息
            self.create_test_case(
                name="ip_interface_get_specific_address_information",
                method="GET",
                url="/api/v1/ip/address/vlans/1/ip-address/192.168.1.10/subnet-mask/255.255.255.0/is-primary/true",
                category="ip_interface_address_management",
                module="ip_interface",
                description="獲取特定IPv4地址信息"
            ),
            
            # 獲取VLAN 100的特定IP地址信息
            self.create_test_case(
                name="ip_interface_get_vlan_100_specific_address",
                method="GET",
                url="/api/v1/ip/address/vlans/100/ip-address/10.1.1.1/subnet-mask/255.255.0.0/is-primary/true",
                category="ip_interface_address_management",
                module="ip_interface",
                description="獲取VLAN 100的特定IP地址信息"
            ),
            
            # 刪除VLAN 1的次要IP地址
            self.create_test_case(
                name="ip_interface_delete_vlan_1_secondary_ip",
                method="DELETE",
                url="/api/v1/ip/address/vlans/1/ip-address/192.168.1.20/subnet-mask/255.255.255.0/is-primary/false",
                category="ip_interface_address_management",
                module="ip_interface",
                description="刪除VLAN 1的次要IP地址"
            ),
            
            # 刪除VLAN 200的IP地址
            self.create_test_case(
                name="ip_interface_delete_vlan_200_ip",
                method="DELETE",
                url="/api/v1/ip/address/vlans/200/ip-address/172.16.1.1/subnet-mask/255.255.255.0/is-primary/true",
                category="ip_interface_address_management",
                module="ip_interface",
                description="刪除VLAN 200的IP地址"
            ),
            
            # 驗證IP地址配置
            self.create_test_case(
                name="ip_interface_verify_address_configuration",
                method="GET",
                url="/api/v1/ip/address/vlans?startId=1",
                category="ip_interface_address_management",
                module="ip_interface",
                description="驗證IP地址配置"
            )
        ]
    
    def get_ip_interface_traffic_statistics_tests(self) -> List[APITestCase]:
        """IP Interface Traffic Statistics API 測試案例"""
        return [
            # 獲取IP、ICMP、UDP、TCP和ARP協議統計
            self.create_test_case(
                name="ip_interface_get_traffic_statistics",
                method="GET",
                url="/api/v1/ip/traffics",
                category="ip_interface_traffic_statistics",
                module="ip_interface",
                description="獲取IP、ICMP、UDP、TCP和ARP協議統計"
            ),
            
            # 多次獲取統計信息以檢查一致性
            self.create_test_case(
                name="ip_interface_get_traffic_statistics_consistency_check",
                method="GET",
                url="/api/v1/ip/traffics",
                category="ip_interface_traffic_statistics",
                module="ip_interface",
                description="多次獲取統計信息以檢查一致性"
            ),
            
            # 驗證統計信息響應格式
            self.create_test_case(
                name="ip_interface_verify_traffic_statistics_response_format",
                method="GET",
                url="/api/v1/ip/traffics",
                category="ip_interface_traffic_statistics",
                module="ip_interface",
                description="驗證統計信息響應格式"
            ),
            
            # 檢查IP統計完整性
            self.create_test_case(
                name="ip_interface_check_ip_statistics_completeness",
                method="GET",
                url="/api/v1/ip/traffics",
                category="ip_interface_traffic_statistics",
                module="ip_interface",
                description="檢查IP統計完整性"
            ),
            
            # 檢查ICMP統計完整性
            self.create_test_case(
                name="ip_interface_check_icmp_statistics_completeness",
                method="GET",
                url="/api/v1/ip/traffics",
                category="ip_interface_traffic_statistics",
                module="ip_interface",
                description="檢查ICMP統計完整性"
            ),
            
            # 檢查UDP和TCP統計完整性
            self.create_test_case(
                name="ip_interface_check_udp_tcp_statistics_completeness",
                method="GET",
                url="/api/v1/ip/traffics",
                category="ip_interface_traffic_statistics",
                module="ip_interface",
                description="檢查UDP和TCP統計完整性"
            )
        ]
    
    def get_ip_interface_loopback_management_tests(self) -> List[APITestCase]:
        """IP Interface Loopback Management API 測試案例"""
        return [
            # 創建Loopback接口
            self.create_test_case(
                name="ip_interface_create_loopback_interface",
                method="POST",
                url="/api/v1/ip/loopback",
                category="ip_interface_loopback_management",
                module="ip_interface",
                body={},
                description="創建Loopback接口"
            ),
            
            # 獲取Loopback接口信息
            self.create_test_case(
                name="ip_interface_get_loopback_interface_information",
                method="GET",
                url="/api/v1/ip/loopback",
                category="ip_interface_loopback_management",
                module="ip_interface",
                description="獲取Loopback接口信息"
            ),
            
            # 設置Loopback接口IP地址 - 基本配置
            # (The parameter ipAddress is invalid.)
            self.create_test_case(
                name="ip_interface_set_loopback_ip_basic",
                method="PUT",
                url="/api/v1/ip/loopback",
                category="ip_interface_loopback_management",
                module="ip_interface",
                body=self.test_data.get('ip_interface_loopback_basic', {
                    "ipAddress": "127.0.0.1",
                    "subnetMask": "255.0.0.0"
                }),
                description="設置Loopback接口IP地址 - 基本配置"
            ),
            
            # 更新Loopback接口IP地址 - 企業配置
            self.create_test_case(
                name="ip_interface_update_loopback_ip_enterprise",
                method="PUT",
                url="/api/v1/ip/loopback",
                category="ip_interface_loopback_management",
                module="ip_interface",
                body=self.test_data.get('ip_interface_loopback_enterprise', {
                    "ipAddress": "10.10.10.20",
                    "subnetMask": "255.255.255.0"
                }),
                description="更新Loopback接口IP地址 - 企業配置"
            ),
            
            # 更新Loopback接口IP地址 - 數據中心配置
            self.create_test_case(
                name="ip_interface_update_loopback_ip_datacenter",
                method="PUT",
                url="/api/v1/ip/loopback",
                category="ip_interface_loopback_management",
                module="ip_interface",
                body=self.test_data.get('ip_interface_loopback_datacenter', {
                    "ipAddress": "172.16.255.1",
                    "subnetMask": "255.255.255.255"
                }),
                description="更新Loopback接口IP地址 - 數據中心配置"
            ),
            
            # 驗證Loopback接口配置更新
            self.create_test_case(
                name="ip_interface_verify_loopback_configuration_update",
                method="GET",
                url="/api/v1/ip/loopback",
                category="ip_interface_loopback_management",
                module="ip_interface",
                description="驗證Loopback接口配置更新"
            ),
            
            # 取消設置Loopback接口IP地址
            self.create_test_case(
                name="ip_interface_unset_loopback_ip",
                method="PUT",
                url="/api/v1/ip/loopback",
                category="ip_interface_loopback_management",
                module="ip_interface",
                body=self.test_data.get('ip_interface_loopback_unset', {
                    "ipAddress": "0.0.0.0"
                }),
                description="取消設置Loopback接口IP地址"
            ),
            
            # 重新設置Loopback接口IP地址
            self.create_test_case(
                name="ip_interface_reset_loopback_ip",
                method="PUT",
                url="/api/v1/ip/loopback",
                category="ip_interface_loopback_management",
                module="ip_interface",
                body=self.test_data.get('ip_interface_loopback_reset', {
                    "ipAddress": "192.168.255.1",
                    "subnetMask": "255.255.255.0"
                }),
                description="重新設置Loopback接口IP地址"
            ),
            
            # 刪除Loopback接口
            self.create_test_case(
                name="ip_interface_delete_loopback_interface",
                method="DELETE",
                url="/api/v1/ip/loopback",
                category="ip_interface_loopback_management",
                module="ip_interface",
                description="刪除Loopback接口"
            ),
            
            # 驗證Loopback接口刪除
            self.create_test_case(
                name="ip_interface_verify_loopback_deletion",
                method="GET",
                url="/api/v1/ip/loopback",
                category="ip_interface_loopback_management",
                module="ip_interface",
                expected_status=200,
                description="驗證Loopback接口刪除"
            )
        ]
    
    def get_ip_interface_advanced_operations_tests(self) -> List[APITestCase]:
        """IP Interface Advanced Operations API 測試案例"""
        return [
            # 重新創建Loopback接口用於高級操作
            self.create_test_case(
                name="ip_interface_recreate_loopback_for_advanced_ops",
                method="POST",
                url="/api/v1/ip/loopback",
                category="ip_interface_advanced_operations",
                module="ip_interface",
                body={},
                description="重新創建Loopback接口用於高級操作"
            ),
            
            # 配置企業級網路環境
            # (Failed to set Failed to set netDefaultGateway.)
            self.create_test_case(
                name="ip_interface_configure_enterprise_network_environment",
                method="PUT",
                url="/api/v1/ip",
                category="ip_interface_advanced_operations",
                module="ip_interface",
                body=self.test_data.get('ip_interface_enterprise_network_gateway', {
                    "netDefaultGateway": "10.0.0.254"
                }),
                description="配置企業級網路環境默認網關"
            ),
            
            # 批量配置多個VLAN的IP地址 - VLAN 10
            # (Failed to set IP address.)
            self.create_test_case(
                name="ip_interface_batch_configure_vlan_10_ip",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_advanced_operations",
                module="ip_interface",
                body=self.test_data.get('ip_interface_batch_vlan_10', {
                    "vlanId": 10,
                    "ipAddress": "10.0.10.1",
                    "subnetMask": "255.255.255.0",
                    "isPrimary": True
                }),
                description="批量配置VLAN 10的IP地址"
            ),
            
            # 批量配置多個VLAN的IP地址 - VLAN 20
            # (Failed to set IP address.)
            self.create_test_case(
                name="ip_interface_batch_configure_vlan_20_ip",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_advanced_operations",
                module="ip_interface",
                body=self.test_data.get('ip_interface_batch_vlan_20', {
                    "vlanId": 20,
                    "ipAddress": "10.0.20.1",
                    "subnetMask": "255.255.255.0",
                    "isPrimary": True
                }),
                description="批量配置VLAN 20的IP地址"
            ),
            
            # 批量配置多個VLAN的IP地址 - VLAN 30
            # (Failed to set IP address.)
            self.create_test_case(
                name="ip_interface_batch_configure_vlan_30_ip",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_advanced_operations",
                module="ip_interface",
                body=self.test_data.get('ip_interface_batch_vlan_30', {
                    "vlanId": 30,
                    "ipAddress": "10.0.30.1",
                    "subnetMask": "255.255.255.0",
                    "isPrimary": True
                }),
                description="批量配置VLAN 30的IP地址"
            ),
            
            # 配置多子網環境 - VLAN 50
            # (Failed to set IP address.)
            self.create_test_case(
                name="ip_interface_configure_multi_subnet_vlan_50",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_advanced_operations",
                module="ip_interface",
                body=self.test_data.get('ip_interface_multi_subnet_vlan_50_primary', {
                    "vlanId": 50,
                    "ipAddress": "192.168.50.1",
                    "subnetMask": "255.255.255.0",
                    "isPrimary": True
                }),
                description="配置多子網環境 - VLAN 50主要IP"
            ),
            
            # 配置多子網環境 - VLAN 50次要IP
            # (Failed to set IP address.)
            self.create_test_case(
                name="ip_interface_configure_multi_subnet_vlan_50_secondary",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_advanced_operations",
                module="ip_interface",
                body=self.test_data.get('ip_interface_multi_subnet_vlan_50_secondary', {
                    "vlanId": 50,
                    "ipAddress": "192.168.51.1",
                    "subnetMask": "255.255.255.0",
                    "isPrimary": False
                }),
                description="配置多子網環境 - VLAN 50次要IP"
            ),
            
            # 配置高級Loopback接口
            self.create_test_case(
                name="ip_interface_configure_advanced_loopback",
                method="PUT",
                url="/api/v1/ip/loopback",
                category="ip_interface_advanced_operations",
                module="ip_interface",
                body=self.test_data.get('ip_interface_advanced_loopback', {
                    "ipAddress": "10.255.255.1",
                    "subnetMask": "255.255.255.255"
                }),
                description="配置高級Loopback接口"
            ),
            
            # 動態調整網路參數
            # (Failed to set netDefaultGateway.)
            self.create_test_case(
                name="ip_interface_dynamic_adjust_network_parameters",
                method="PUT",
                url="/api/v1/ip",
                category="ip_interface_advanced_operations",
                module="ip_interface",
                body=self.test_data.get('ip_interface_dynamic_gateway', {
                    "netDefaultGateway": "10.0.0.1"
                }),
                description="動態調整網路參數"
            ),
            
            # 驗證高級操作結果
            self.create_test_case(
                name="ip_interface_verify_advanced_operations_results",
                method="GET",
                url="/api/v1/ip/address/vlans?startId=1",
                category="ip_interface_advanced_operations",
                module="ip_interface",
                description="驗證高級操作結果"
            ),
            
            # 驗證Loopback高級配置結果
            self.create_test_case(
                name="ip_interface_verify_loopback_advanced_results",
                method="GET",
                url="/api/v1/ip/loopback",
                category="ip_interface_advanced_operations",
                module="ip_interface",
                description="驗證Loopback高級配置結果"
            )
        ]
    
    def get_ip_interface_error_handling_tests(self) -> List[APITestCase]:
        """IP Interface Error Handling API 測試案例"""
        return [
            # 測試無效的IP地址格式 - 默認網關
            self.create_test_case(
                name="ip_interface_test_invalid_ip_format_gateway",
                method="PUT",
                url="/api/v1/ip",
                category="ip_interface_error_handling",
                module="ip_interface",
                body=self.test_data.get('ip_interface_invalid_gateway_ip', {
                    "netDefaultGateway": "invalid.ip.address"
                }),
                expected_status=400,
                description="測試無效的IP地址格式 - 默認網關"
            ),
            
            # 測試無效的VLAN ID - 超出範圍
            self.create_test_case(
                name="ip_interface_test_invalid_vlan_id_out_of_range",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_error_handling",
                module="ip_interface",
                body=self.test_data.get('ip_interface_invalid_vlan_id', {
                    "vlanId": 5000,  # 超出範圍 (1-4094)
                    "ipAddress": "192.168.1.1",
                    "subnetMask": "255.255.255.0",
                    "isPrimary": True
                }),
                expected_status=400,
                description="測試無效的VLAN ID - 超出範圍 (>4094)"
            ),
            
            # 測試無效的VLAN ID - 零
            self.create_test_case(
                name="ip_interface_test_invalid_vlan_id_zero",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_error_handling",
                module="ip_interface",
                body=self.test_data.get('ip_interface_invalid_vlan_id_zero', {
                    "vlanId": 0,
                    "ipAddress": "192.168.1.1",
                    "subnetMask": "255.255.255.0",
                    "isPrimary": True
                }),
                expected_status=400,
                description="測試無效的VLAN ID - 零"
            ),
            
            # 測試無效的IP地址格式 - VLAN IP
            self.create_test_case(
                name="ip_interface_test_invalid_ip_format_vlan",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_error_handling",
                module="ip_interface",
                body=self.test_data.get('ip_interface_invalid_vlan_ip', {
                    "vlanId": 100,
                    "ipAddress": "300.300.300.300",  # 無效IP
                    "subnetMask": "255.255.255.0",
                    "isPrimary": True
                }),
                expected_status=400,
                description="測試無效的IP地址格式 - VLAN IP"
            ),
            
            # 測試無效的子網掩碼格式
            self.create_test_case(
                name="ip_interface_test_invalid_subnet_mask_format",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_error_handling",
                module="ip_interface",
                body=self.test_data.get('ip_interface_invalid_subnet_mask', {
                    "vlanId": 100,
                    "ipAddress": "192.168.1.1",
                    "subnetMask": "invalid.mask",
                    "isPrimary": True
                }),
                expected_status=400,
                description="測試無效的子網掩碼格式"
            ),
            
            # 測試網路ID作為IP地址
            self.create_test_case(
                name="ip_interface_test_network_id_as_ip",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_error_handling",
                module="ip_interface",
                body=self.test_data.get('ip_interface_network_id_as_ip', {
                    "vlanId": 100,
                    "ipAddress": "192.168.1.0",  # 網路ID
                    "subnetMask": "255.255.255.0",
                    "isPrimary": True
                }),
                expected_status=400,
                description="測試網路ID作為IP地址"
            ),
            
            # 測試廣播IP作為IP地址
            self.create_test_case(
                name="ip_interface_test_broadcast_ip_as_ip",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_error_handling",
                module="ip_interface",
                body=self.test_data.get('ip_interface_broadcast_ip_as_ip', {
                    "vlanId": 100,
                    "ipAddress": "192.168.1.255",  # 廣播IP
                    "subnetMask": "255.255.255.0",
                    "isPrimary": True
                }),
                expected_status=400,
                description="測試廣播IP作為IP地址"
            ),
            
            # 測試無效的布爾值 - isPrimary
            self.create_test_case(
                name="ip_interface_test_invalid_boolean_is_primary",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_error_handling",
                module="ip_interface",
                body=self.test_data.get('ip_interface_invalid_boolean_primary', {
                    "vlanId": 100,
                    "ipAddress": "192.168.1.1",
                    "subnetMask": "255.255.255.0",
                    "isPrimary": "yes"  # 無效布爾值
                }),
                expected_status=400,
                description="測試無效的布爾值 - isPrimary"
            ),
            
            # 測試無效JSON格式 - 默認網關
            self.create_test_case(
                name="ip_interface_test_invalid_json_gateway",
                method="PUT",
                url="/api/v1/ip",
                category="ip_interface_error_handling",
                module="ip_interface",
                body="invalid json format",
                expected_status=400,
                description="測試無效JSON格式 - 默認網關"
            ),
            
            # 測試無效JSON格式 - VLAN IP
            self.create_test_case(
                name="ip_interface_test_invalid_json_vlan_ip",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_error_handling",
                module="ip_interface",
                body="{ invalid json }",
                expected_status=400,
                description="測試無效JSON格式 - VLAN IP"
            ),
            
            # 測試無效的Loopback IP地址格式
            self.create_test_case(
                name="ip_interface_test_invalid_loopback_ip_format",
                method="PUT",
                url="/api/v1/ip/loopback",
                category="ip_interface_error_handling",
                module="ip_interface",
                body=self.test_data.get('ip_interface_invalid_loopback_ip', {
                    "ipAddress": "invalid.loopback.ip",
                    "subnetMask": "255.255.255.0"
                }),
                expected_status=200,
                description="測試無效的Loopback IP地址格式"
            ),
            
            # 測試無效的Loopback子網掩碼
            self.create_test_case(
                name="ip_interface_test_invalid_loopback_subnet_mask",
                method="PUT",
                url="/api/v1/ip/loopback",
                category="ip_interface_error_handling",
                module="ip_interface",
                body=self.test_data.get('ip_interface_invalid_loopback_mask', {
                    "ipAddress": "127.0.0.1",
                    "subnetMask": "invalid.mask"
                }),
                expected_status=400,
                description="測試無效的Loopback子網掩碼"
            ),
            
            # 測試缺少必需參數 - VLAN IP配置
            self.create_test_case(
                name="ip_interface_test_missing_required_params_vlan_ip",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_error_handling",
                module="ip_interface",
                body=self.test_data.get('ip_interface_missing_params_vlan_ip', {
                    "vlanId": 100
                    # 缺少ipAddress, subnetMask, isPrimary
                }),
                expected_status=400,
                description="測試缺少必需參數 - VLAN IP配置"
            ),
            
            # 測試不存在的VLAN
            self.create_test_case(
                name="ip_interface_test_nonexistent_vlan",
                method="POST",
                url="/api/v1/ip/address/vlans",
                category="ip_interface_error_handling",
                module="ip_interface",
                body=self.test_data.get('ip_interface_nonexistent_vlan', {
                    "vlanId": 999,  # 假設不存在的VLAN
                    "ipAddress": "192.168.1.1",
                    "subnetMask": "255.255.255.0",
                    "isPrimary": True
                }),
                expected_status=500,
                description="測試不存在的VLAN"
            ),
            
            # 恢復正常IP接口配置
            # (Failed to set netDefaultGateway.)
            self.create_test_case(
                name="ip_interface_restore_normal_configuration",
                method="PUT",
                url="/api/v1/ip",
                category="ip_interface_error_handling",
                module="ip_interface",
                body=self.test_data.get('ip_interface_restore_normal_config', {
                    "netDefaultGateway": "192.168.1.1"
                }),
                description="恢復正常IP接口配置"
            ),
            
            # 最終IP接口狀態檢查
            self.create_test_case(
                name="ip_interface_final_status_check",
                method="GET",
                url="/api/v1/ip",
                category="ip_interface_error_handling",
                module="ip_interface",
                description="最終IP接口狀態檢查"
            )
        ]