#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IP ARP Inspection 模組測試案例
包含動態ARP檢查配置、VLAN管理、接口信任狀態、統計信息、日誌管理等相關API測試
支援全局ARP檢查、VLAN級別配置、接口信任設置、速率限制、日誌記錄等操作
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class IP_ARP_INSPECTIONTests(BaseTests):
    """IP ARP Inspection 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取IP ARP Inspection模組支援的類別"""
        return [
            "ip_arp_inspection_global_configuration",
            "ip_arp_inspection_vlan_management",
            "ip_arp_inspection_interface_management",
            "ip_arp_inspection_statistics_management",
            "ip_arp_inspection_log_management",
            "ip_arp_inspection_ignore_source_port_management",
            "ip_arp_inspection_advanced_operations",
            "ip_arp_inspection_error_handling"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有IP ARP Inspection測試案例"""
        all_tests = []
        all_tests.extend(self.get_ip_arp_inspection_global_configuration_tests())
        all_tests.extend(self.get_ip_arp_inspection_vlan_management_tests())
        all_tests.extend(self.get_ip_arp_inspection_interface_management_tests())
        all_tests.extend(self.get_ip_arp_inspection_statistics_management_tests())
        all_tests.extend(self.get_ip_arp_inspection_log_management_tests())
        all_tests.extend(self.get_ip_arp_inspection_ignore_source_port_management_tests())
        all_tests.extend(self.get_ip_arp_inspection_advanced_operations_tests())
        all_tests.extend(self.get_ip_arp_inspection_error_handling_tests())
        return all_tests
    
    def get_ip_arp_inspection_global_configuration_tests(self) -> List[APITestCase]:
        """IP ARP Inspection Global Configuration API 測試案例"""
        return [
            # 獲取全局ARP檢查配置
            self.create_test_case(
                name="ip_arp_inspection_get_global_configuration",
                method="GET",
                url="/api/v1/dynamic-arp-inspection",
                category="ip_arp_inspection_global_configuration",
                module="ip_arp_inspection",
                description="獲取全局動態ARP檢查配置"
            ),
            
            # 啟用全局ARP檢查並配置基本驗證
            self.create_test_case(
                name="ip_arp_inspection_enable_global_with_basic_validation",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection",
                category="ip_arp_inspection_global_configuration",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_enable_global_basic', {
                    "status": True,
                    "logNumber": 255,
                    "logInterval": 2000,
                    "globalSrcMacValidation": True,
                    "globalDestMacValidation": True,
                    "globalIpAddrValidation": True,
                    "globalSrcInterfaceValidation": False,
                    "globalIpAllowZerosValidation": True
                }),
                description="啟用全局ARP檢查並配置基本驗證"
            ),
            
            # 配置高級驗證選項
            self.create_test_case(
                name="ip_arp_inspection_configure_advanced_validation",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection",
                category="ip_arp_inspection_global_configuration",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_advanced_validation', {
                    "status": True,
                    "logNumber": 128,
                    "logInterval": 1000,
                    "globalSrcMacValidation": True,
                    "globalDestMacValidation": False,
                    "globalIpAddrValidation": True,
                    "globalSrcInterfaceValidation": True,
                    "globalIpAllowZerosValidation": False
                }),
                description="配置高級驗證選項"
            ),
            
            # 配置日誌設置
            self.create_test_case(
                name="ip_arp_inspection_configure_logging_settings",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection",
                category="ip_arp_inspection_global_configuration",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_logging_settings', {
                    "status": True,
                    "logNumber": 64,
                    "logInterval": 500,
                    "globalSrcMacValidation": True,
                    "globalDestMacValidation": True,
                    "globalIpAddrValidation": False,
                    "globalSrcInterfaceValidation": False,
                    "globalIpAllowZerosValidation": False
                }),
                description="配置日誌設置"
            ),
            
            # 禁用全局ARP檢查
            self.create_test_case(
                name="ip_arp_inspection_disable_global",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection",
                category="ip_arp_inspection_global_configuration",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_disable_global', {
                    "status": False
                }),
                description="禁用全局動態ARP檢查"
            ),
            
            # 重新啟用全局ARP檢查
            self.create_test_case(
                name="ip_arp_inspection_re_enable_global",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection",
                category="ip_arp_inspection_global_configuration",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_re_enable_global', {
                    "status": True,
                    "logNumber": 100,
                    "logInterval": 1500,
                    "globalSrcMacValidation": True,
                    "globalDestMacValidation": True,
                    "globalIpAddrValidation": True,
                    "globalSrcInterfaceValidation": True,
                    "globalIpAllowZerosValidation": True
                }),
                description="重新啟用全局動態ARP檢查"
            ),
            
            # 驗證全局配置更新
            self.create_test_case(
                name="ip_arp_inspection_verify_global_configuration_update",
                method="GET",
                url="/api/v1/dynamic-arp-inspection",
                category="ip_arp_inspection_global_configuration",
                module="ip_arp_inspection",
                description="驗證全局配置更新"
            )
        ]
    
    def get_ip_arp_inspection_vlan_management_tests(self) -> List[APITestCase]:
        """IP ARP Inspection VLAN Management API 測試案例"""
        return [
            # 獲取所有VLAN的ARP檢查狀態
            self.create_test_case(
                name="ip_arp_inspection_get_all_vlans_status",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/vlans?startId=1",
                category="ip_arp_inspection_vlan_management",
                module="ip_arp_inspection",
                description="獲取所有VLAN的ARP檢查狀態"
            ),
            
            # 獲取特定VLAN的ARP檢查狀態
            self.create_test_case(
                name="ip_arp_inspection_get_specific_vlan_status",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/vlans/100",
                category="ip_arp_inspection_vlan_management",
                module="ip_arp_inspection",
                description="獲取VLAN 100的ARP檢查狀態"
            ),
            
            # 配置VLAN 1的ARP檢查 - 靜態模式
            self.create_test_case(
                name="ip_arp_inspection_configure_vlan_1_static",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/vlans/1",
                category="ip_arp_inspection_vlan_management",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_vlan_1_static', {
                    "status": True,
                    "arpAclName": "arp_acl_vlan1",
                    "arpAclStatus": "static"
                }),
                description="配置VLAN 1的ARP檢查 - 靜態模式"
            ),
            
            # 配置VLAN 100的ARP檢查 - 動態模式
            self.create_test_case(
                name="ip_arp_inspection_configure_vlan_100_dynamic",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/vlans/100",
                category="ip_arp_inspection_vlan_management",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_vlan_100_dynamic', {
                    "status": True,
                    "arpAclName": "arp_acl_vlan100",
                    "arpAclStatus": "dynamic"
                }),
                description="配置VLAN 100的ARP檢查 - 動態模式"
            ),
            
            # 配置VLAN 200的ARP檢查 - 僅啟用
            self.create_test_case(
                name="ip_arp_inspection_configure_vlan_200_enable_only",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/vlans/200",
                category="ip_arp_inspection_vlan_management",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_vlan_200_enable', {
                    "status": True
                }),
                description="配置VLAN 200的ARP檢查 - 僅啟用"
            ),
            
            # 配置VLAN 500的ARP檢查 - 完整配置
            self.create_test_case(
                name="ip_arp_inspection_configure_vlan_500_full",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/vlans/500",
                category="ip_arp_inspection_vlan_management",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_vlan_500_full', {
                    "status": True,
                    "arpAclName": "enterprise_arp_acl",
                    "arpAclStatus": "static"
                }),
                description="配置VLAN 500的ARP檢查 - 完整配置"
            ),
            
            # 禁用VLAN 200的ARP檢查
            self.create_test_case(
                name="ip_arp_inspection_disable_vlan_200",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/vlans/200",
                category="ip_arp_inspection_vlan_management",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_vlan_200_disable', {
                    "status": False
                }),
                description="禁用VLAN 200的ARP檢查"
            ),
            
            # 更新VLAN 100的ACL配置
            self.create_test_case(
                name="ip_arp_inspection_update_vlan_100_acl",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/vlans/100",
                category="ip_arp_inspection_vlan_management",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_vlan_100_update_acl', {
                    "status": True,
                    "arpAclName": "updated_arp_acl",
                    "arpAclStatus": "static"
                }),
                description="更新VLAN 100的ACL配置"
            ),
            
            # 驗證VLAN配置
            self.create_test_case(
                name="ip_arp_inspection_verify_vlan_configuration",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/vlans?startId=1",
                category="ip_arp_inspection_vlan_management",
                module="ip_arp_inspection",
                description="驗證VLAN配置"
            )
        ]
    
    def get_ip_arp_inspection_interface_management_tests(self) -> List[APITestCase]:
        """IP ARP Inspection Interface Management API 測試案例"""
        return [
            # 獲取所有接口的ARP檢查狀態
            self.create_test_case(
                name="ip_arp_inspection_get_all_interfaces_status",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/interfaces",
                category="ip_arp_inspection_interface_management",
                module="ip_arp_inspection",
                description="獲取所有接口的ARP檢查狀態"
            ),
            
            # 獲取特定接口的ARP檢查狀態 - eth1/1
            self.create_test_case(
                name="ip_arp_inspection_get_specific_interface_eth1_1",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/interfaces/eth1%2f1",
                category="ip_arp_inspection_interface_management",
                module="ip_arp_inspection",
                description="獲取eth1/1接口的ARP檢查狀態"
            ),
            
            # 配置eth1/1接口為信任狀態
            self.create_test_case(
                name="ip_arp_inspection_configure_eth1_1_trusted",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/interfaces/eth1%2f1",
                category="ip_arp_inspection_interface_management",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_eth1_1_trusted', {
                    "trustStatus": True,
                    "rateLimit": 15
                }),
                description="配置eth1/1接口為信任狀態"
            ),
            
            # 配置eth1/2接口為不信任狀態並設置速率限制
            self.create_test_case(
                name="ip_arp_inspection_configure_eth1_2_untrusted_with_rate_limit",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/interfaces/eth1%2f2",
                category="ip_arp_inspection_interface_management",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_eth1_2_untrusted_rate_limit', {
                    "trustStatus": False,
                    "rateLimit": 10
                }),
                description="配置eth1/2接口為不信任狀態並設置速率限制"
            ),
            
            # 配置eth1/5接口高速率限制
            self.create_test_case(
                name="ip_arp_inspection_configure_eth1_5_high_rate_limit",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/interfaces/eth1%2f5",
                category="ip_arp_inspection_interface_management",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_eth1_5_high_rate_limit', {
                    "trustStatus": True,
                    "rateLimit": 100
                }),
                description="配置eth1/5接口高速率限制"
            ),
            
            # 配置trunk1接口為信任狀態
            self.create_test_case(
                name="ip_arp_inspection_configure_trunk1_trusted",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/interfaces/trunk1",
                category="ip_arp_inspection_interface_management",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_trunk1_trusted', {
                    "trustStatus": True,
                    "rateLimit": 50
                }),
                description="配置trunk1接口為信任狀態"
            ),
            
            # 配置trunk2接口為不信任狀態
            self.create_test_case(
                name="ip_arp_inspection_configure_trunk2_untrusted",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/interfaces/trunk2",
                category="ip_arp_inspection_interface_management",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_trunk2_untrusted', {
                    "trustStatus": False,
                    "rateLimit": 25
                }),
                description="配置trunk2接口為不信任狀態"
            ),
            
            # 設置接口無速率限制 - eth1/10
            self.create_test_case(
                name="ip_arp_inspection_configure_eth1_10_no_rate_limit",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/interfaces/eth1%2f10",
                category="ip_arp_inspection_interface_management",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_eth1_10_no_rate_limit', {
                    "trustStatus": True,
                    "rateLimit": 4294967295  # 無速率限制
                }),
                description="設置eth1/10接口無速率限制"
            ),
            
            # 驗證接口配置
            self.create_test_case(
                name="ip_arp_inspection_verify_interface_configuration",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/interfaces",
                category="ip_arp_inspection_interface_management",
                module="ip_arp_inspection",
                description="驗證接口配置"
            )
        ]
    
    def get_ip_arp_inspection_statistics_management_tests(self) -> List[APITestCase]:
        """IP ARP Inspection Statistics Management API 測試案例"""
        return [
            # 獲取ARP檢查統計信息
            self.create_test_case(
                name="ip_arp_inspection_get_statistics",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/statistics",
                category="ip_arp_inspection_statistics_management",
                module="ip_arp_inspection",
                description="獲取ARP檢查統計信息"
            ),
            
            # 多次獲取統計信息以檢查一致性
            self.create_test_case(
                name="ip_arp_inspection_get_statistics_consistency_check",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/statistics",
                category="ip_arp_inspection_statistics_management",
                module="ip_arp_inspection",
                description="多次獲取統計信息以檢查一致性"
            ),
            
            # 驗證統計信息響應格式
            self.create_test_case(
                name="ip_arp_inspection_verify_statistics_response_format",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/statistics",
                category="ip_arp_inspection_statistics_management",
                module="ip_arp_inspection",
                description="驗證統計信息響應格式"
            )
        ]
    
    def get_ip_arp_inspection_log_management_tests(self) -> List[APITestCase]:
        """IP ARP Inspection Log Management API 測試案例"""
        return [
            # 獲取ARP檢查日誌 - 從起始ID 1開始
            self.create_test_case(
                name="ip_arp_inspection_get_logs_from_start",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/log?startId=1",
                category="ip_arp_inspection_log_management",
                module="ip_arp_inspection",
                description="獲取ARP檢查日誌 - 從起始ID 1開始"
            ),
            
            # 獲取特定VLAN的ARP檢查日誌
            self.create_test_case(
                name="ip_arp_inspection_get_logs_specific_vlan",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/log?startId=1&vlan=1",
                category="ip_arp_inspection_log_management",
                module="ip_arp_inspection",
                description="獲取VLAN 1的ARP檢查日誌"
            ),
            
            # 獲取特定接口的ARP檢查日誌
            self.create_test_case(
                name="ip_arp_inspection_get_logs_specific_interface",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/log?startId=1&ifId=eth1%2f1",
                category="ip_arp_inspection_log_management",
                module="ip_arp_inspection",
                description="獲取eth1/1接口的ARP檢查日誌"
            ),
            
            # 獲取特定VLAN和接口的ARP檢查日誌
            self.create_test_case(
                name="ip_arp_inspection_get_logs_vlan_and_interface",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/log?startId=1&ifId=eth1%2f1&vlan=1",
                category="ip_arp_inspection_log_management",
                module="ip_arp_inspection",
                description="獲取VLAN 1和eth1/1接口的ARP檢查日誌"
            ),
            
            # 獲取不同起始ID的日誌
            self.create_test_case(
                name="ip_arp_inspection_get_logs_different_start_id",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/log?startId=10",
                category="ip_arp_inspection_log_management",
                module="ip_arp_inspection",
                description="獲取不同起始ID的日誌"
            ),
            
            # 驗證日誌響應格式
            self.create_test_case(
                name="ip_arp_inspection_verify_log_response_format",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/log?startId=1",
                category="ip_arp_inspection_log_management",
                module="ip_arp_inspection",
                description="驗證日誌響應格式"
            )
        ]
    
    def get_ip_arp_inspection_ignore_source_port_management_tests(self) -> List[APITestCase]:
        """IP ARP Inspection Ignore Source Port Management API 測試案例"""
        return [
            # 獲取忽略源端口檢查的VLAN配置
            self.create_test_case(
                name="ip_arp_inspection_get_ignore_source_port_config",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/ignore-source-port",
                category="ip_arp_inspection_ignore_source_port_management",
                module="ip_arp_inspection",
                description="獲取忽略源端口檢查的VLAN配置"
            ),
            
            # 配置忽略源端口檢查 - 單個VLAN
            self.create_test_case(
                name="ip_arp_inspection_configure_ignore_source_port_single_vlan",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/ignore-source-port",
                category="ip_arp_inspection_ignore_source_port_management",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_ignore_source_port_single', {
                    "ignore": True,
                    "vlans": [100]
                }),
                description="配置忽略源端口檢查 - 單個VLAN"
            ),
            
            # 配置忽略源端口檢查 - 多個VLAN和範圍
            self.create_test_case(
                name="ip_arp_inspection_configure_ignore_source_port_multiple_vlans",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/ignore-source-port",
                category="ip_arp_inspection_ignore_source_port_management",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_ignore_source_port_multiple', {
                    "ignore": True,
                    "vlans": [
                        8,
                        {
                            "start": 35,
                            "end": 36
                        },
                        88
                    ]
                }),
                description="配置忽略源端口檢查 - 多個VLAN和範圍"
            ),
            
            # 配置忽略源端口檢查 - 複雜VLAN範圍
            self.create_test_case(
                name="ip_arp_inspection_configure_ignore_source_port_complex_ranges",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/ignore-source-port",
                category="ip_arp_inspection_ignore_source_port_management",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_ignore_source_port_complex', {
                    "ignore": True,
                    "vlans": [
                        1,
                        {
                            "start": 10,
                            "end": 20
                        },
                        50,
                        {
                            "start": 100,
                            "end": 200
                        },
                        500
                    ]
                }),
                description="配置忽略源端口檢查 - 複雜VLAN範圍"
            ),
            
            # 禁用忽略源端口檢查
            self.create_test_case(
                name="ip_arp_inspection_disable_ignore_source_port",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/ignore-source-port",
                category="ip_arp_inspection_ignore_source_port_management",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_disable_ignore_source_port', {
                    "ignore": False,
                    "vlans": []
                }),
                description="禁用忽略源端口檢查"
            ),
            
            # 重新啟用忽略源端口檢查
            self.create_test_case(
                name="ip_arp_inspection_re_enable_ignore_source_port",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/ignore-source-port",
                category="ip_arp_inspection_ignore_source_port_management",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_re_enable_ignore_source_port', {
                    "ignore": True,
                    "vlans": [
                        1,
                        {
                            "start": 3,
                            "end": 6
                        },
                        8,
                        12
                    ]
                }),
                description="重新啟用忽略源端口檢查"
            ),
            
            # 驗證忽略源端口配置
            self.create_test_case(
                name="ip_arp_inspection_verify_ignore_source_port_configuration",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/ignore-source-port",
                category="ip_arp_inspection_ignore_source_port_management",
                module="ip_arp_inspection",
                description="驗證忽略源端口配置"
            )
        ]
    
    def get_ip_arp_inspection_advanced_operations_tests(self) -> List[APITestCase]:
        """IP ARP Inspection Advanced Operations API 測試案例"""
        return [
            # 配置企業級ARP檢查環境
            self.create_test_case(
                name="ip_arp_inspection_configure_enterprise_environment",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection",
                category="ip_arp_inspection_advanced_operations",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_enterprise_config', {
                    "status": True,
                    "logNumber": 256,
                    "logInterval": 3600,
                    "globalSrcMacValidation": True,
                    "globalDestMacValidation": True,
                    "globalIpAddrValidation": True,
                    "globalSrcInterfaceValidation": True,
                    "globalIpAllowZerosValidation": False
                }),
                description="配置企業級ARP檢查環境"
            ),
            
            # 批量配置多個VLAN的ARP檢查 - VLAN 10
            self.create_test_case(
                name="ip_arp_inspection_batch_configure_vlan_10",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/vlans/10",
                category="ip_arp_inspection_advanced_operations",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_batch_vlan_10', {
                    "status": True,
                    "arpAclName": "batch_acl_10",
                    "arpAclStatus": "dynamic"
                }),
                description="批量配置VLAN 10的ARP檢查"
            ),
            
            # 批量配置多個VLAN的ARP檢查 - VLAN 20
            self.create_test_case(
                name="ip_arp_inspection_batch_configure_vlan_20",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/vlans/20",
                category="ip_arp_inspection_advanced_operations",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_batch_vlan_20', {
                    "status": True,
                    "arpAclName": "batch_acl_20",
                    "arpAclStatus": "static"
                }),
                description="批量配置VLAN 20的ARP檢查"
            ),
            
            # 批量配置多個接口的信任狀態 - eth1/20
            self.create_test_case(
                name="ip_arp_inspection_batch_configure_interface_eth1_20",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/interfaces/eth1%2f20",
                category="ip_arp_inspection_advanced_operations",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_batch_interface_eth1_20', {
                    "trustStatus": True,
                    "rateLimit": 30
                }),
                description="批量配置eth1/20接口的信任狀態"
            ),
            
            # 批量配置多個接口的信任狀態 - eth1/21
            self.create_test_case(
                name="ip_arp_inspection_batch_configure_interface_eth1_21",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/interfaces/eth1%2f21",
                category="ip_arp_inspection_advanced_operations",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_batch_interface_eth1_21', {
                    "trustStatus": False,
                    "rateLimit": 5
                }),
                description="批量配置eth1/21接口的信任狀態"
            ),
            
            # 配置高安全性ARP檢查策略
            self.create_test_case(
                name="ip_arp_inspection_configure_high_security_policy",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection",
                category="ip_arp_inspection_advanced_operations",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_high_security_policy', {
                    "status": True,
                    "logNumber": 256,
                    "logInterval": 60,
                    "globalSrcMacValidation": True,
                    "globalDestMacValidation": True,
                    "globalIpAddrValidation": True,
                    "globalSrcInterfaceValidation": True,
                    "globalIpAllowZerosValidation": False
                }),
                description="配置高安全性ARP檢查策略"
            ),
            
            # 動態調整ARP檢查參數
            self.create_test_case(
                name="ip_arp_inspection_dynamic_adjust_parameters",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection",
                category="ip_arp_inspection_advanced_operations",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_dynamic_parameters', {
                    "status": True,
                    "logNumber": 128,
                    "logInterval": 1800,
                    "globalSrcMacValidation": True,
                    "globalDestMacValidation": False,
                    "globalIpAddrValidation": True,
                    "globalSrcInterfaceValidation": False,
                    "globalIpAllowZerosValidation": True
                }),
                description="動態調整ARP檢查參數"
            ),
            
            # 驗證高級操作結果
            self.create_test_case(
                name="ip_arp_inspection_verify_advanced_operations_results",
                method="GET",
                url="/api/v1/dynamic-arp-inspection",
                category="ip_arp_inspection_advanced_operations",
                module="ip_arp_inspection",
                description="驗證高級操作結果"
            ),
            
            # 驗證VLAN高級配置結果
            self.create_test_case(
                name="ip_arp_inspection_verify_vlan_advanced_results",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/vlans?startId=1",
                category="ip_arp_inspection_advanced_operations",
                module="ip_arp_inspection",
                description="驗證VLAN高級配置結果"
            ),
            
            # 驗證接口高級配置結果
            self.create_test_case(
                name="ip_arp_inspection_verify_interface_advanced_results",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/interfaces",
                category="ip_arp_inspection_advanced_operations",
                module="ip_arp_inspection",
                description="驗證接口高級配置結果"
            )
        ]
    
    def get_ip_arp_inspection_error_handling_tests(self) -> List[APITestCase]:
        """IP ARP Inspection Error Handling API 測試案例"""
        return [
            # 測試無效的VLAN ID - 超出範圍
            self.create_test_case(
                name="ip_arp_inspection_test_invalid_vlan_id_out_of_range",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/vlans/5000",
                category="ip_arp_inspection_error_handling",
                module="ip_arp_inspection",
                expected_status=400,
                description="測試無效的VLAN ID - 超出範圍 (>4094)"
            ),
            
            # 測試無效的VLAN ID - 零
            self.create_test_case(
                name="ip_arp_inspection_test_invalid_vlan_id_zero",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/vlans/0",
                category="ip_arp_inspection_error_handling",
                module="ip_arp_inspection",
                expected_status=400,
                description="測試無效的VLAN ID - 零"
            ),
            
            # 測試無效的接口ID格式
            self.create_test_case(
                name="ip_arp_inspection_test_invalid_interface_id_format",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/interfaces/invalid_interface",
                category="ip_arp_inspection_error_handling",
                module="ip_arp_inspection",
                expected_status=400,
                description="測試無效的接口ID格式"
            ),
            
            # 測試無效的日誌數量 - 超出範圍
            self.create_test_case(
                name="ip_arp_inspection_test_invalid_log_number_out_of_range",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection",
                category="ip_arp_inspection_error_handling",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_invalid_log_number', {
                    "status": True,
                    "logNumber": 300  # 超出範圍 (0-256)
                }),
                expected_status=400,
                description="測試無效的日誌數量 - 超出範圍 (>256)"
            ),
            
            # 測試無效的日誌間隔 - 超出範圍
            self.create_test_case(
                name="ip_arp_inspection_test_invalid_log_interval_out_of_range",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection",
                category="ip_arp_inspection_error_handling",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_invalid_log_interval', {
                    "status": True,
                    "logInterval": 90000  # 超出範圍 (0-86400)
                }),
                expected_status=400,
                description="測試無效的日誌間隔 - 超出範圍 (>86400)"
            ),
            
            # 測試無效的速率限制 - 超出範圍
            self.create_test_case(
                name="ip_arp_inspection_test_invalid_rate_limit_out_of_range",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/interfaces/eth1%2f1",
                category="ip_arp_inspection_error_handling",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_invalid_rate_limit', {
                    "trustStatus": True,
                    "rateLimit": 800  # 超出範圍 (0-750, 4294967295)
                }),
                expected_status=400,
                description="測試無效的速率限制 - 超出範圍 (>750且≠4294967295)"
            ),
            
            # 測試無效的布爾值 - 全局狀態
            self.create_test_case(
                name="ip_arp_inspection_test_invalid_boolean_global_status",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection",
                category="ip_arp_inspection_error_handling",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_invalid_boolean_status', {
                    "status": "invalid_boolean"
                }),
                expected_status=400,
                description="測試無效的布爾值 - 全局狀態"
            ),
            
            # 測試無效的布爾值 - 驗證選項
            self.create_test_case(
                name="ip_arp_inspection_test_invalid_boolean_validation",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection",
                category="ip_arp_inspection_error_handling",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_invalid_boolean_validation', {
                    "status": True,
                    "globalSrcMacValidation": "yes"
                }),
                expected_status=400,
                description="測試無效的布爾值 - 驗證選項"
            ),
            
            # 測試無效的ACL狀態
            self.create_test_case(
                name="ip_arp_inspection_test_invalid_acl_status",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/vlans/100",
                category="ip_arp_inspection_error_handling",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_invalid_acl_status', {
                    "status": True,
                    "arpAclName": "test_acl",
                    "arpAclStatus": "invalid_status"
                }),
                expected_status=400,
                description="測試無效的ACL狀態 (非static/dynamic)"
            ),
            
            # 測試無效JSON格式 - 全局配置
            self.create_test_case(
                name="ip_arp_inspection_test_invalid_json_global",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection",
                category="ip_arp_inspection_error_handling",
                module="ip_arp_inspection",
                body="invalid json format",
                expected_status=400,
                description="測試無效JSON格式 - 全局配置"
            ),
            
            # 測試無效JSON格式 - VLAN配置
            self.create_test_case(
                name="ip_arp_inspection_test_invalid_json_vlan",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/vlans/100",
                category="ip_arp_inspection_error_handling",
                module="ip_arp_inspection",
                body="{ invalid json }",
                expected_status=400,
                description="測試無效JSON格式 - VLAN配置"
            ),
            
            # 測試無效的起始ID - 超出範圍
            self.create_test_case(
                name="ip_arp_inspection_test_invalid_start_id_out_of_range",
                method="GET",
                url="/api/v1/dynamic-arp-inspection/log?startId=300",
                category="ip_arp_inspection_error_handling",
                module="ip_arp_inspection",
                expected_status=400,
                description="測試無效的起始ID - 超出範圍 (>256)"
            ),
            
            # 測試無效的VLAN範圍 - 起始大於結束
            self.create_test_case(
                name="ip_arp_inspection_test_invalid_vlan_range",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/ignore-source-port",
                category="ip_arp_inspection_error_handling",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_invalid_vlan_range', {
                    "ignore": True,
                    "vlans": [
                        {
                            "start": 50,
                            "end": 30  # 起始大於結束
                        }
                    ]
                }),
                expected_status=400,
                description="測試無效的VLAN範圍 - 起始大於結束"
            ),
            
            # 測試缺少必需參數 - 忽略源端口配置
            self.create_test_case(
                name="ip_arp_inspection_test_missing_required_params_ignore_source_port",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection/ignore-source-port",
                category="ip_arp_inspection_error_handling",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_missing_params_ignore_source_port', {}),
                expected_status=400,
                description="測試缺少必需參數 - 忽略源端口配置"
            ),
            
            # 恢復正常ARP檢查配置
            self.create_test_case(
                name="ip_arp_inspection_restore_normal_configuration",
                method="PUT",
                url="/api/v1/dynamic-arp-inspection",
                category="ip_arp_inspection_error_handling",
                module="ip_arp_inspection",
                body=self.test_data.get('ip_arp_inspection_restore_normal_config', {
                    "status": True,
                    "logNumber": 100,
                    "logInterval": 1000,
                    "globalSrcMacValidation": True,
                    "globalDestMacValidation": True,
                    "globalIpAddrValidation": True,
                    "globalSrcInterfaceValidation": True,
                    "globalIpAllowZerosValidation": True
                }),
                description="恢復正常ARP檢查配置"
            ),
            
            # 最終ARP檢查狀態檢查
            self.create_test_case(
                name="ip_arp_inspection_final_status_check",
                method="GET",
                url="/api/v1/dynamic-arp-inspection",
                category="ip_arp_inspection_error_handling",
                module="ip_arp_inspection",
                description="最終ARP檢查狀態檢查"
            )
        ]