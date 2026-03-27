#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface 模組測試案例
包含接口管理、接口配置、計數器統計、收發器管理、IP地址管理等相關API測試
支援以太網接口、Trunk接口、VLAN接口、接口統計、收發器閾值等操作
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class INTERFACETests(BaseTests):
    """Interface 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取Interface模組支援的類別"""
        return [
            "interface_information_query",
            "interface_configuration_management",
            "interface_counters_management",
            "interface_transceiver_management",
            "interface_ip_address_management",
            "interface_advanced_operations",
            "interface_error_handling"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有Interface測試案例"""
        all_tests = []
        all_tests.extend(self.get_interface_information_query_tests())
        all_tests.extend(self.get_interface_configuration_management_tests())
        all_tests.extend(self.get_interface_counters_management_tests())
        all_tests.extend(self.get_interface_transceiver_management_tests())
        all_tests.extend(self.get_interface_ip_address_management_tests())
        all_tests.extend(self.get_interface_advanced_operations_tests())
        all_tests.extend(self.get_interface_error_handling_tests())
        return all_tests
    
    def get_interface_information_query_tests(self) -> List[APITestCase]:
        """Interface Information Query API 測試案例"""
        return [
            # 獲取所有接口信息
            self.create_test_case(
                name="interface_get_all_interfaces",
                method="GET",
                url="/api/v1/interfaces",
                category="interface_information_query",
                module="interface",
                description="獲取所有接口信息"
            ),
            
            # 獲取特定以太網接口信息 - eth1/1
            self.create_test_case(
                name="interface_get_specific_ethernet_interface",
                method="GET",
                url="/api/v1/interfaces/eth1%2f1",
                category="interface_information_query",
                module="interface",
                description="獲取eth1/1接口詳細信息"
            ),
            
            # 獲取特定以太網接口信息 - eth1/2
            self.create_test_case(
                name="interface_get_ethernet_interface_eth1_2",
                method="GET",
                url="/api/v1/interfaces/eth1%2f2",
                category="interface_information_query",
                module="interface",
                description="獲取eth1/2接口詳細信息"
            ),
            
            # 獲取Trunk接口信息 - trunk1
            self.create_test_case(
                name="interface_get_trunk_interface",
                method="GET",
                url="/api/v1/interfaces/trunk1",
                category="interface_information_query",
                module="interface",
                description="獲取trunk1接口詳細信息"
            ),
            
            # 驗證接口信息響應格式
            self.create_test_case(
                name="interface_verify_response_format",
                method="GET",
                url="/api/v1/interfaces",
                category="interface_information_query",
                module="interface",
                description="驗證接口信息響應格式"
            ),
            
            # 檢查接口信息完整性
            self.create_test_case(
                name="interface_check_information_completeness",
                method="GET",
                url="/api/v1/interfaces/eth1%2f1",
                category="interface_information_query",
                module="interface",
                description="檢查接口信息完整性"
            ),
            
            # 多次查詢接口信息一致性
            self.create_test_case(
                name="interface_multiple_query_consistency",
                method="GET",
                url="/api/v1/interfaces",
                category="interface_information_query",
                module="interface",
                description="多次查詢接口信息一致性"
            )
        ]
    
    def get_interface_configuration_management_tests(self) -> List[APITestCase]:
        """Interface Configuration Management API 測試案例"""
        return [
            # 配置接口基本設置 - eth1/1
            self.create_test_case(
                name="interface_configure_basic_settings_eth1_1",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f1",
                category="interface_configuration_management",
                module="interface",
                body=self.test_data.get('interface_basic_config_eth1_1', {
                    "isEnabled": True,
                    "ifName": "test_port_1",
                    "flowControl": False,
                    "autoNegotiation": True,
                    "speedDuplexConfig": "1000full",
                    "powerSave": False
                }),
                description="配置eth1/1接口基本設置"
            ),
            
            # 配置接口VLAN設置 - eth1/2
            self.create_test_case(
                name="interface_configure_vlan_settings_eth1_2",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f2",
                category="interface_configuration_management",
                module="interface",
                body=self.test_data.get('interface_vlan_config_eth1_2', {
                    "isEnabled": True,
                    "vlanMode": "hybrid",
                    "pvid": 100,
                    "allowedVlanUntagged": [100, 200],
                    "allowedVlanTagged": [10, 20, {"start": 300, "end": 310}],
                    "ingressFilter": True,
                    "acceptableFrametype": "tagged"
                }),
                description="配置eth1/2接口VLAN設置"
            ),
            
            # 配置接口速率限制 - eth1/3
            self.create_test_case(
                name="interface_configure_rate_limiting_eth1_3",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f3",
                category="interface_configuration_management",
                module="interface",
                body=self.test_data.get('interface_rate_limiting_eth1_3', {
                    "isEnabled": True,
                    "ingressRateLimitStatus": True,
                    "ingressRateLimit": 500000,
                    "egressRateLimitStatus": True,
                    "egressRateLimit": 800000
                }),
                description="配置eth1/3接口速率限制"
            ),
            
            # 配置接口風暴控制 - eth1/4
            self.create_test_case(
                name="interface_configure_storm_control_eth1_4",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f4",
                category="interface_configuration_management",
                module="interface",
                body=self.test_data.get('interface_storm_control_eth1_4', {
                    "isEnabled": True,
                    "broadcastStorm": True,
                    "broadcastStormLimit": 1000,
                    "multicastStorm": True,
                    "multicastStormLimit": 800,
                    "unknownUnicastStorm": True,
                    "unknownUnicastStormLimit": 600
                }),
                description="配置eth1/4接口風暴控制"
            ),
            
            # 配置接口能力設置 - eth1/5
            self.create_test_case(
                name="interface_configure_capabilities_eth1_5",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f5",
                category="interface_configuration_management",
                module="interface",
                body=self.test_data.get('interface_capabilities_eth1_5', {
                    "isEnabled": True,
                    "autoNegotiation": True,
                    "capabilities": ["10half", "10full", "100half", "100full", "1000full"],
                    "mediaType": "sfp1000-forced"
                }),
                description="配置eth1/5接口能力設置"
            ),
            
            # 配置Trunk接口 - trunk1
            self.create_test_case(
                name="interface_configure_trunk_interface",
                method="PUT",
                url="/api/v1/interfaces/trunk1",
                category="interface_configuration_management",
                module="interface",
                body=self.test_data.get('interface_trunk_config', {
                    "isEnabled": True,
                    "ifName": "trunk_interface_1",
                    "vlanTrunking": True,
                    "lacp": True,
                    "allowedVlanTagged": [1, 10, 20, {"start": 100, "end": 200}]
                }),
                description="配置trunk1接口設置"
            ),
            
            # 禁用接口 - eth1/10
            self.create_test_case(
                name="interface_disable_interface_eth1_10",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f10",
                category="interface_configuration_management",
                module="interface",
                body=self.test_data.get('interface_disable_eth1_10', {
                    "isEnabled": False
                }),
                description="禁用eth1/10接口"
            ),
            
            # 驗證接口配置更新
            self.create_test_case(
                name="interface_verify_configuration_update",
                method="GET",
                url="/api/v1/interfaces/eth1%2f1",
                category="interface_configuration_management",
                module="interface",
                description="驗證接口配置更新"
            )
        ]
    
    def get_interface_counters_management_tests(self) -> List[APITestCase]:
        """Interface Counters Management API 測試案例"""
        return [
            # 獲取所有接口計數器信息
            self.create_test_case(
                name="interface_get_all_counters",
                method="GET",
                url="/api/v1/interfaces-counters",
                category="interface_counters_management",
                module="interface",
                description="獲取所有接口計數器信息"
            ),
            
            # 獲取特定接口計數器信息 - eth1/1
            self.create_test_case(
                name="interface_get_specific_counters_eth1_1",
                method="GET",
                url="/api/v1/interfaces/eth1%2f1/counters",
                category="interface_counters_management",
                module="interface",
                description="獲取eth1/1接口計數器信息"
            ),
            
            # 獲取特定接口計數器信息 - eth1/2
            self.create_test_case(
                name="interface_get_specific_counters_eth1_2",
                method="GET",
                url="/api/v1/interfaces/eth1%2f2/counters",
                category="interface_counters_management",
                module="interface",
                description="獲取eth1/2接口計數器信息"
            ),
            
            # 獲取Trunk接口計數器信息 - trunk1
            self.create_test_case(
                name="interface_get_trunk_counters",
                method="GET",
                url="/api/v1/interfaces/trunk1/counters",
                category="interface_counters_management",
                module="interface",
                description="獲取trunk1接口計數器信息"
            ),
            
            # 清除接口計數器 - eth1/1
            self.create_test_case(
                name="interface_clear_counters_eth1_1",
                method="PUT",
                url="/api/v1/interfaces-clear-counters/eth1%2f1",
                category="interface_counters_management",
                module="interface",
                body={},
                description="清除eth1/1接口計數器"
            ),
            
            # 清除接口計數器 - eth1/2
            self.create_test_case(
                name="interface_clear_counters_eth1_2",
                method="PUT",
                url="/api/v1/interfaces-clear-counters/eth1%2f2",
                category="interface_counters_management",
                module="interface",
                body={},
                description="清除eth1/2接口計數器"
            ),
            
            # 驗證計數器清除結果
            self.create_test_case(
                name="interface_verify_counters_cleared",
                method="GET",
                url="/api/v1/interfaces/eth1%2f1/counters",
                category="interface_counters_management",
                module="interface",
                description="驗證計數器清除結果"
            )
        ]
    
    def get_interface_transceiver_management_tests(self) -> List[APITestCase]:
        """Interface Transceiver Management API 測試案例"""
        return [
            # 獲取所有收發器信息
            self.create_test_case(
                name="interface_get_all_transceivers",
                method="GET",
                url="/api/v1/interfaces-transceiver",
                category="interface_transceiver_management",
                module="interface",
                description="獲取所有SFP接口收發器信息"
            ),
            
            # 獲取特定收發器信息 - eth1/49
            self.create_test_case(
                name="interface_get_specific_transceiver_eth1_49",
                method="GET",
                url="/api/v1/interfaces/eth1%2f49/transceiver",
                category="interface_transceiver_management",
                module="interface",
                description="獲取eth1/49收發器詳細信息"
            ),
            
            # 獲取特定收發器信息 - eth1/50
            self.create_test_case(
                name="interface_get_specific_transceiver_eth1_50",
                method="GET",
                url="/api/v1/interfaces/eth1%2f50/transceiver",
                category="interface_transceiver_management",
                module="interface",
                description="獲取eth1/50收發器詳細信息"
            ),
            
            # 配置收發器監控 - eth1/49
            self.create_test_case(
                name="interface_configure_transceiver_monitoring_eth1_49",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f49/transceiver",
                category="interface_transceiver_management",
                module="interface",
                body=self.test_data.get('interface_transceiver_monitoring_eth1_49', {
                    "transceiverMonitor": True,
                    "transceiverThresholdAuto": False,
                    "txBiasCurrentHighAlarm": 10000,
                    "txBiasCurrentHighWarning": 9000,
                    "txBiasCurrentLowAlarm": 600,
                    "txBiasCurrentLowWarning": 700,
                    "txPowerHighAlarm": -900,
                    "txPowerHighWarning": -950,
                    "txPowerLowAlarm": -1200,
                    "txPowerLowWarning": -1150
                }),
                description="配置eth1/49收發器監控和閾值"
            ),
            
            # 配置收發器溫度閾值 - eth1/50
            self.create_test_case(
                name="interface_configure_transceiver_temperature_eth1_50",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f50/transceiver",
                category="interface_transceiver_management",
                module="interface",
                body=self.test_data.get('interface_transceiver_temperature_eth1_50', {
                    "transceiverMonitor": True,
                    "transceiverThresholdAuto": False,
                    "temperatureHighAlarm": 7500,
                    "temperatureHighWarning": 7000,
                    "temperatureLowAlarm": -12300,
                    "temperatureLowWarning": 0,
                    "voltageHighAlarm": 350,
                    "voltageHighWarning": 345,
                    "voltageLowAlarm": 310,
                    "voltageLowWarning": 315
                }),
                description="配置eth1/50收發器溫度和電壓閾值"
            ),
            
            # 啟用自動閾值模式 - eth1/51
            self.create_test_case(
                name="interface_enable_auto_threshold_eth1_51",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f51/transceiver",
                category="interface_transceiver_management",
                module="interface",
                body=self.test_data.get('interface_auto_threshold_eth1_51', {
                    "transceiverMonitor": True,
                    "transceiverThresholdAuto": True
                }),
                description="啟用eth1/51收發器自動閾值模式"
            ),
            
            # 禁用收發器監控 - eth1/52
            self.create_test_case(
                name="interface_disable_transceiver_monitoring_eth1_52",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f52/transceiver",
                category="interface_transceiver_management",
                module="interface",
                body=self.test_data.get('interface_disable_transceiver_eth1_52', {
                    "transceiverMonitor": False,
                    "transceiverThresholdAuto": True
                }),
                description="禁用eth1/52收發器監控"
            ),
            
            # 驗證收發器配置
            self.create_test_case(
                name="interface_verify_transceiver_configuration",
                method="GET",
                url="/api/v1/interfaces/eth1%2f49/transceiver",
                category="interface_transceiver_management",
                module="interface",
                description="驗證收發器配置"
            )
        ]
    
    def get_interface_ip_address_management_tests(self) -> List[APITestCase]:
        """Interface IP Address Management API 測試案例"""
        return [
            # 創建L3接口 - vlan100
            self.create_test_case(
                name="interface_create_l3_interface_vlan100",
                method="POST",
                url="/api/v1/interfaces/vlan100",
                category="interface_ip_address_management",
                module="interface",
                body=self.test_data.get('interface_create_l3_vlan100', {
                    "ip": "192.168.100.1/24",
                    "role": "primary"
                }),
                description="創建vlan100 L3接口並設置主IP地址"
            ),
            
            # 創建L3接口 - vlan200
            self.create_test_case(
                name="interface_create_l3_interface_vlan200",
                method="POST",
                url="/api/v1/interfaces/vlan200",
                category="interface_ip_address_management",
                module="interface",
                body=self.test_data.get('interface_create_l3_vlan200', {
                    "ip": "192.168.200.1/24",
                    "role": "primary"
                }),
                description="創建vlan200 L3接口並設置主IP地址"
            ),
            
            # 添加次要IP地址 - vlan100
            self.create_test_case(
                name="interface_add_secondary_ip_vlan100",
                method="POST",
                url="/api/v1/interfaces/vlan100/ipaddrs",
                category="interface_ip_address_management",
                module="interface",
                body=self.test_data.get('interface_add_secondary_ip_vlan100', {
                    "ip": "192.168.101.1/24",
                    "role": "secondary"
                }),
                description="為vlan100添加次要IP地址"
            ),
            
            # 添加虛擬IP地址 - vlan200
            self.create_test_case(
                name="interface_add_virtual_ip_vlan200",
                method="POST",
                url="/api/v1/interfaces/vlan200/ipaddrs",
                category="interface_ip_address_management",
                module="interface",
                body=self.test_data.get('interface_add_virtual_ip_vlan200', {
                    "ip": "192.168.201.1/24",
                    "role": "virtual"
                }),
                description="為vlan200添加虛擬IP地址"
            ),
            
            # 添加多個IP地址 - vlan100
            self.create_test_case(
                name="interface_add_multiple_ips_vlan100",
                method="POST",
                url="/api/v1/interfaces/vlan100/ipaddrs",
                category="interface_ip_address_management",
                module="interface",
                body=self.test_data.get('interface_add_multiple_ips_vlan100', {
                    "ip": "10.1.1.1/16",
                    "role": "secondary"
                }),
                description="為vlan100添加多個IP地址"
            ),
            
            # 刪除IP地址 - vlan100次要IP
            self.create_test_case(
                name="interface_delete_secondary_ip_vlan100",
                method="DELETE",
                url="/api/v1/interfaces/vlan100/ipaddrs/192.168.101.1_24",
                category="interface_ip_address_management",
                module="interface",
                description="刪除vlan100的次要IP地址"
            ),
            
            # 刪除IP地址 - vlan200虛擬IP
            self.create_test_case(
                name="interface_delete_virtual_ip_vlan200",
                method="DELETE",
                url="/api/v1/interfaces/vlan200/ipaddrs/192.168.201.1_24",
                category="interface_ip_address_management",
                module="interface",
                description="刪除vlan200的虛擬IP地址"
            ),
            
            # 刪除L3接口 - vlan200
            self.create_test_case(
                name="interface_delete_l3_interface_vlan200",
                method="DELETE",
                url="/api/v1/interfaces/vlan200",
                category="interface_ip_address_management",
                module="interface",
                description="刪除vlan200 L3接口"
            ),
            
            # 驗證IP地址管理結果
            self.create_test_case(
                name="interface_verify_ip_address_management",
                method="GET",
                url="/api/v1/interfaces",
                category="interface_ip_address_management",
                module="interface",
                description="驗證IP地址管理結果"
            )
        ]
    
    def get_interface_advanced_operations_tests(self) -> List[APITestCase]:
        """Interface Advanced Operations API 測試案例"""
        return [
            # 配置企業級接口環境
            self.create_test_case(
                name="interface_configure_enterprise_environment",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f20",
                category="interface_advanced_operations",
                module="interface",
                body=self.test_data.get('interface_enterprise_config', {
                    "isEnabled": True,
                    "ifName": "enterprise_port",
                    "vlanMode": "trunk",
                    "allowedVlanTagged": [1, 10, 20, 30, {"start": 100, "end": 200}],
                    "flowControl": True,
                    "autoNegotiation": True,
                    "capabilities": ["1000full"],
                    "ingressRateLimitStatus": True,
                    "ingressRateLimit": 1000000,
                    "egressRateLimitStatus": True,
                    "egressRateLimit": 1000000
                }),
                description="配置企業級接口環境"
            ),
            
            # 批量配置多個接口 - eth1/21
            self.create_test_case(
                name="interface_batch_configure_eth1_21",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f21",
                category="interface_advanced_operations",
                module="interface",
                body=self.test_data.get('interface_batch_config_eth1_21', {
                    "isEnabled": True,
                    "ifName": "batch_port_21",
                    "vlanMode": "access",
                    "pvid": 21,
                    "allowedVlanUntagged": [21]
                }),
                description="批量配置接口 - eth1/21"
            ),
            
            # 批量配置多個接口 - eth1/22
            self.create_test_case(
                name="interface_batch_configure_eth1_22",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f22",
                category="interface_advanced_operations",
                module="interface",
                body=self.test_data.get('interface_batch_config_eth1_22', {
                    "isEnabled": True,
                    "ifName": "batch_port_22",
                    "vlanMode": "access",
                    "pvid": 22,
                    "allowedVlanUntagged": [22]
                }),
                description="批量配置接口 - eth1/22"
            ),
            
            # 配置鏈路聚合接口
            self.create_test_case(
                name="interface_configure_link_aggregation",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f25",
                category="interface_advanced_operations",
                module="interface",
                body=self.test_data.get('interface_link_aggregation_config', {
                    "isEnabled": True,
                    "channelGroup": 1,
                    "lacp": True
                }),
                description="配置鏈路聚合接口"
            ),
            
            # 配置高級VLAN設置
            self.create_test_case(
                name="interface_configure_advanced_vlan_settings",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f30",
                category="interface_advanced_operations",
                module="interface",
                body=self.test_data.get('interface_advanced_vlan_config', {
                    "isEnabled": True,
                    "vlanMode": "hybrid",
                    "pvid": 1,
                    "allowedVlanUntagged": [1, 100, 200],
                    "allowedVlanTagged": [10, 20, {"start": 300, "end": 400}, 500],
                    "ingressFilter": True,
                    "acceptableFrametype": "all",
                    "gvrp": True,
                    "forbiddenVlans": [999]
                }),
                description="配置高級VLAN設置"
            ),
            
            # 配置QoS和優先級設置
            self.create_test_case(
                name="interface_configure_qos_priority",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f35",
                category="interface_advanced_operations",
                module="interface",
                body=self.test_data.get('interface_qos_priority_config', {
                    "isEnabled": True,
                    "priority": 7,
                    "ingressRateLimitStatus": True,
                    "ingressRateLimit": 500000,
                    "egressRateLimitStatus": True,
                    "egressRateLimit": 800000
                }),
                description="配置QoS和優先級設置"
            ),
            
            # 動態調整接口參數
            self.create_test_case(
                name="interface_dynamic_adjust_parameters",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f40",
                category="interface_advanced_operations",
                module="interface",
                body=self.test_data.get('interface_dynamic_parameters', {
                    "isEnabled": True,
                    "speedDuplexConfig": "100full",
                    "autoNegotiation": False,
                    "flowControl": True,
                    "powerSave": True
                }),
                description="動態調整接口參數"
            ),
            
            # 驗證高級操作結果
            self.create_test_case(
                name="interface_verify_advanced_operations_results",
                method="GET",
                url="/api/v1/interfaces",
                category="interface_advanced_operations",
                module="interface",
                description="驗證高級操作結果"
            )
        ]
    
    def get_interface_error_handling_tests(self) -> List[APITestCase]:
        """Interface Error Handling API 測試案例"""
        return [
            # 測試無效的接口ID格式
            self.create_test_case(
                name="interface_test_invalid_interface_id_format",
                method="GET",
                url="/api/v1/interfaces/invalid_interface",
                category="interface_error_handling",
                module="interface",
                expected_status=400,
                description="測試無效的接口ID格式"
            ),
            
            # 測試超出範圍的接口ID - 端口號
            self.create_test_case(
                name="interface_test_out_of_range_port_number",
                method="GET",
                url="/api/v1/interfaces/eth1%2f99",
                category="interface_error_handling",
                module="interface",
                expected_status=400,
                description="測試超出範圍的端口號 (>52)"
            ),
            
            # 測試超出範圍的接口ID - 單元號
            self.create_test_case(
                name="interface_test_out_of_range_unit_number",
                method="GET",
                url="/api/v1/interfaces/eth9%2f1",
                category="interface_error_handling",
                module="interface",
                expected_status=400,
                description="測試超出範圍的單元號 (>8)"
            ),
            
            # 測試無效的Trunk ID
            self.create_test_case(
                name="interface_test_invalid_trunk_id",
                method="GET",
                url="/api/v1/interfaces/trunk99",
                category="interface_error_handling",
                module="interface",
                expected_status=400,
                description="測試無效的Trunk ID (>26)"
            ),
            
            # 測試無效的速度雙工配置
            self.create_test_case(
                name="interface_test_invalid_speed_duplex_config",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f1",
                category="interface_error_handling",
                module="interface",
                body=self.test_data.get('interface_invalid_speed_duplex', {
                    "speedDuplexConfig": "invalid_speed"
                }),
                expected_status=400,
                description="測試無效的速度雙工配置"
            ),
            
            # 測試無效的VLAN ID
            self.create_test_case(
                name="interface_test_invalid_vlan_id",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f1",
                category="interface_error_handling",
                module="interface",
                body=self.test_data.get('interface_invalid_vlan_id', {
                    "pvid": 5000  # 超出範圍 (1-4094)
                }),
                expected_status=400,
                description="測試無效的VLAN ID (>4094)"
            ),
            
            # 測試無效的速率限制值
            self.create_test_case(
                name="interface_test_invalid_rate_limit_value",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f1",
                category="interface_error_handling",
                module="interface",
                body=self.test_data.get('interface_invalid_rate_limit', {
                    "ingressRateLimitStatus": True,
                    "ingressRateLimit": -1000  # 負值
                }),
                expected_status=400,
                description="測試無效的速率限制值 (負值)"
            ),
            
            # 測試無效的風暴控制限制值
            self.create_test_case(
                name="interface_test_invalid_storm_control_limit",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f1",
                category="interface_error_handling",
                module="interface",
                body=self.test_data.get('interface_invalid_storm_control', {
                    "broadcastStorm": True,
                    "broadcastStormLimit": 100  # 低於最小值 (500)
                }),
                expected_status=400,
                description="測試無效的風暴控制限制值 (<500)"
            ),
            
            # 測試無效的優先級值
            self.create_test_case(
                name="interface_test_invalid_priority_value",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f1",
                category="interface_error_handling",
                module="interface",
                body=self.test_data.get('interface_invalid_priority', {
                    "priority": 10  # 超出範圍 (0-7)
                }),
                expected_status=400,
                description="測試無效的優先級值 (>7)"
            ),
            
            # 測試無效的通道組ID
            self.create_test_case(
                name="interface_test_invalid_channel_group_id",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f1",
                category="interface_error_handling",
                module="interface",
                body=self.test_data.get('interface_invalid_channel_group', {
                    "channelGroup": 30  # 超出範圍 (1-26)
                }),
                expected_status=400,
                description="測試無效的通道組ID (>26)"
            ),
            
            # 測試無效JSON格式
            self.create_test_case(
                name="interface_test_invalid_json_format",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f1",
                category="interface_error_handling",
                module="interface",
                body="invalid json format",
                expected_status=400,
                description="測試無效JSON格式"
            ),
            
            # 測試收發器閾值超出範圍 - 電流
            self.create_test_case(
                name="interface_test_transceiver_current_out_of_range",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f49/transceiver",
                category="interface_error_handling",
                module="interface",
                body=self.test_data.get('interface_transceiver_current_out_of_range', {
                    "transceiverMonitor": True,
                    "txBiasCurrentHighAlarm": 15000  # 超出範圍 (0-13100)
                }),
                expected_status=400,
                description="測試收發器電流閾值超出範圍 (>13100)"
            ),
            
            # 測試收發器閾值超出範圍 - 功率
            self.create_test_case(
                name="interface_test_transceiver_power_out_of_range",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f49/transceiver",
                category="interface_error_handling",
                module="interface",
                body=self.test_data.get('interface_transceiver_power_out_of_range', {
                    "transceiverMonitor": True,
                    "txPowerHighAlarm": 1000  # 超出範圍 (-4000-820)
                }),
                expected_status=400,
                description="測試收發器功率閾值超出範圍 (>820)"
            ),
            
            # 測試無效的IP地址格式
            self.create_test_case(
                name="interface_test_invalid_ip_address_format",
                method="POST",
                url="/api/v1/interfaces/vlan100",
                category="interface_error_handling",
                module="interface",
                body=self.test_data.get('interface_invalid_ip_format', {
                    "ip": "invalid.ip.address",
                    "role": "primary"
                }),
                expected_status=400,
                description="測試無效的IP地址格式"
            ),
            
            # 測試無效的IP地址角色
            self.create_test_case(
                name="interface_test_invalid_ip_role",
                method="POST",
                url="/api/v1/interfaces/vlan100",
                category="interface_error_handling",
                module="interface",
                body=self.test_data.get('interface_invalid_ip_role', {
                    "ip": "192.168.1.1/24",
                    "role": "invalid_role"
                }),
                expected_status=400,
                description="測試無效的IP地址角色"
            ),
            
            # 恢復正常接口配置
            self.create_test_case(
                name="interface_restore_normal_configuration",
                method="PUT",
                url="/api/v1/interfaces/eth1%2f1",
                category="interface_error_handling",
                module="interface",
                body=self.test_data.get('interface_restore_normal_config', {
                    "isEnabled": True,
                    "ifName": "eth1/1",
                    "autoNegotiation": True,
                    "speedDuplexConfig": "none",
                    "flowControl": False,
                    "powerSave": False
                }),
                description="恢復正常接口配置"
            ),
            
            # 最終接口狀態檢查
            self.create_test_case(
                name="interface_final_status_check",
                method="GET",
                url="/api/v1/interfaces",
                category="interface_error_handling",
                module="interface",
                description="最終接口狀態檢查"
            )
        ]