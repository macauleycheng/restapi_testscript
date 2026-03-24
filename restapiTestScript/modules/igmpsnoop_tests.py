#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IGMP Snooping 模組測試案例
包含IGMP監聽配置、VLAN管理、查詢器配置、靜態路由器端口管理等相關API測試
支援全局IGMP Snooping、VLAN級別配置、查詢器功能、靜態路由器端口等操作
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class IGMPSNOOPTests(BaseTests):
    """IGMP Snooping 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取IGMP Snooping模組支援的類別"""
        return [
            "igmpsnoop_global_configuration",
            "igmpsnoop_vlan_management",
            "igmpsnoop_querier_management",
            "igmpsnoop_static_router_ports_management",
            "igmpsnoop_information_query",
            "igmpsnoop_advanced_operations",
            "igmpsnoop_error_handling"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有IGMP Snooping測試案例"""
        all_tests = []
        all_tests.extend(self.get_igmpsnoop_global_configuration_tests())
        all_tests.extend(self.get_igmpsnoop_vlan_management_tests())
        all_tests.extend(self.get_igmpsnoop_querier_management_tests())
        all_tests.extend(self.get_igmpsnoop_static_router_ports_management_tests())
        all_tests.extend(self.get_igmpsnoop_information_query_tests())
        all_tests.extend(self.get_igmpsnoop_advanced_operations_tests())
        all_tests.extend(self.get_igmpsnoop_error_handling_tests())
        return all_tests
    
    def get_igmpsnoop_global_configuration_tests(self) -> List[APITestCase]:
        """IGMP Snooping Global Configuration API 測試案例"""
        return [
            # 獲取全局IGMP Snooping配置
            self.create_test_case(
                name="igmpsnoop_get_global_configuration",
                method="GET",
                url="/api/v1/igmpsnp",
                category="igmpsnoop_global_configuration",
                module="igmpsnoop",
                description="獲取全局IGMP Snooping配置"
            ),
            
            # 啟用全局IGMP Snooping
            self.create_test_case(
                name="igmpsnoop_enable_global_snooping",
                method="PUT",
                url="/api/v1/igmpsnp",
                category="igmpsnoop_global_configuration",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_enable_global', {
                    "igmpSnpEnable": True
                }),
                description="啟用全局IGMP Snooping"
            ),
            
            # 禁用全局IGMP Snooping
            self.create_test_case(
                name="igmpsnoop_disable_global_snooping",
                method="PUT",
                url="/api/v1/igmpsnp",
                category="igmpsnoop_global_configuration",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_disable_global', {
                    "igmpSnpEnable": False
                }),
                description="禁用全局IGMP Snooping"
            ),
            
            # 重新啟用全局IGMP Snooping
            self.create_test_case(
                name="igmpsnoop_re_enable_global_snooping",
                method="PUT",
                url="/api/v1/igmpsnp",
                category="igmpsnoop_global_configuration",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_re_enable_global', {
                    "igmpSnpEnable": True
                }),
                description="重新啟用全局IGMP Snooping"
            ),
            
            # 驗證全局IGMP Snooping配置更新
            self.create_test_case(
                name="igmpsnoop_verify_global_configuration_update",
                method="GET",
                url="/api/v1/igmpsnp",
                category="igmpsnoop_global_configuration",
                module="igmpsnoop",
                description="驗證全局IGMP Snooping配置更新"
            )
        ]
    
    def get_igmpsnoop_vlan_management_tests(self) -> List[APITestCase]:
        """IGMP Snooping VLAN Management API 測試案例"""
        return [
            # 獲取所有VLAN的IGMP Snooping狀態
            self.create_test_case(
                name="igmpsnoop_get_all_vlans_status",
                method="GET",
                url="/api/v1/igmpsnp/vlans",
                category="igmpsnoop_vlan_management",
                module="igmpsnoop",
                description="獲取所有VLAN的IGMP Snooping狀態"
            ),
            
            # 獲取特定VLAN的IGMP Snooping狀態
            self.create_test_case(
                name="igmpsnoop_get_specific_vlan_status",
                method="GET",
                url="/api/v1/igmpsnp/vlans/1024",
                category="igmpsnoop_vlan_management",
                module="igmpsnoop",
                description="獲取VLAN 1024的IGMP Snooping狀態"
            ),
            
            # 啟用VLAN 1的IGMP Snooping
            self.create_test_case(
                name="igmpsnoop_enable_vlan_1_snooping",
                method="PUT",
                url="/api/v1/igmpsnp/vlans/1",
                category="igmpsnoop_vlan_management",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_enable_vlan_1', {
                    "igmpSnpEnable": True
                }),
                description="啟用VLAN 1的IGMP Snooping"
            ),
            
            # 啟用VLAN 100的IGMP Snooping
            self.create_test_case(
                name="igmpsnoop_enable_vlan_100_snooping",
                method="PUT",
                url="/api/v1/igmpsnp/vlans/100",
                category="igmpsnoop_vlan_management",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_enable_vlan_100', {
                    "igmpSnpEnable": True
                }),
                description="啟用VLAN 100的IGMP Snooping"
            ),
            
            # 啟用VLAN 1024的IGMP Snooping
            self.create_test_case(
                name="igmpsnoop_enable_vlan_1024_snooping",
                method="PUT",
                url="/api/v1/igmpsnp/vlans/1024",
                category="igmpsnoop_vlan_management",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_enable_vlan_1024', {
                    "igmpSnpEnable": True
                }),
                description="啟用VLAN 1024的IGMP Snooping"
            ),
            
            # 禁用VLAN 2的IGMP Snooping
            self.create_test_case(
                name="igmpsnoop_disable_vlan_2_snooping",
                method="PUT",
                url="/api/v1/igmpsnp/vlans/2",
                category="igmpsnoop_vlan_management",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_disable_vlan_2', {
                    "igmpSnpEnable": False
                }),
                description="禁用VLAN 2的IGMP Snooping"
            ),
            
            # 啟用VLAN 500的IGMP Snooping
            self.create_test_case(
                name="igmpsnoop_enable_vlan_500_snooping",
                method="PUT",
                url="/api/v1/igmpsnp/vlans/500",
                category="igmpsnoop_vlan_management",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_enable_vlan_500', {
                    "igmpSnpEnable": True
                }),
                description="啟用VLAN 500的IGMP Snooping"
            ),
            
            # 禁用VLAN 500的IGMP Snooping
            self.create_test_case(
                name="igmpsnoop_disable_vlan_500_snooping",
                method="PUT",
                url="/api/v1/igmpsnp/vlans/500",
                category="igmpsnoop_vlan_management",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_disable_vlan_500', {
                    "igmpSnpEnable": False
                }),
                description="禁用VLAN 500的IGMP Snooping"
            ),
            
            # 驗證VLAN IGMP Snooping配置
            self.create_test_case(
                name="igmpsnoop_verify_vlan_configuration",
                method="GET",
                url="/api/v1/igmpsnp/vlans",
                category="igmpsnoop_vlan_management",
                module="igmpsnoop",
                description="驗證VLAN IGMP Snooping配置"
            )
        ]
    
    def get_igmpsnoop_querier_management_tests(self) -> List[APITestCase]:
        """IGMP Snooping Querier Management API 測試案例"""
        return [
            # 獲取IGMP Snooping查詢器狀態
            self.create_test_case(
                name="igmpsnoop_get_querier_status",
                method="GET",
                url="/api/v1/igmpsnp/querier",
                category="igmpsnoop_querier_management",
                module="igmpsnoop",
                description="獲取IGMP Snooping查詢器狀態"
            ),
            
            # 啟用IGMP Snooping查詢器
            self.create_test_case(
                name="igmpsnoop_enable_querier",
                method="PUT",
                url="/api/v1/igmpsnp/querier",
                category="igmpsnoop_querier_management",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_enable_querier', {
                    "querierEnable": True
                }),
                description="啟用IGMP Snooping查詢器"
            ),
            
            # 禁用IGMP Snooping查詢器
            self.create_test_case(
                name="igmpsnoop_disable_querier",
                method="PUT",
                url="/api/v1/igmpsnp/querier",
                category="igmpsnoop_querier_management",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_disable_querier', {
                    "querierEnable": False
                }),
                description="禁用IGMP Snooping查詢器"
            ),
            
            # 重新啟用IGMP Snooping查詢器
            self.create_test_case(
                name="igmpsnoop_re_enable_querier",
                method="PUT",
                url="/api/v1/igmpsnp/querier",
                category="igmpsnoop_querier_management",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_re_enable_querier', {
                    "querierEnable": True
                }),
                description="重新啟用IGMP Snooping查詢器"
            ),
            
            # 驗證IGMP Snooping查詢器配置
            self.create_test_case(
                name="igmpsnoop_verify_querier_configuration",
                method="GET",
                url="/api/v1/igmpsnp/querier",
                category="igmpsnoop_querier_management",
                module="igmpsnoop",
                description="驗證IGMP Snooping查詢器配置"
            )
        ]
    
    def get_igmpsnoop_static_router_ports_management_tests(self) -> List[APITestCase]:
        """IGMP Snooping Static Router Ports Management API 測試案例"""
        return [
            # 獲取所有靜態路由器端口
            self.create_test_case(
                name="igmpsnoop_get_all_static_router_ports",
                method="GET",
                url="/api/v1/igmpsnp/static-router-ports",
                category="igmpsnoop_static_router_ports_management",
                module="igmpsnoop",
                description="獲取所有靜態路由器端口"
            ),
            
            # 獲取特定靜態路由器端口狀態 - eth1/1
            self.create_test_case(
                name="igmpsnoop_get_static_router_port_eth1_1",
                method="GET",
                url="/api/v1/igmpsnp/static-router-port/1/eth1%2f1",
                category="igmpsnoop_static_router_ports_management",
                module="igmpsnoop",
                description="獲取VLAN 1 eth1/1靜態路由器端口狀態"
            ),
            
            # 啟用VLAN 1 eth1/1靜態路由器端口
            self.create_test_case(
                name="igmpsnoop_enable_static_router_port_vlan1_eth1_1",
                method="PUT",
                url="/api/v1/igmpsnp/static-router-port/1/eth1%2f1",
                category="igmpsnoop_static_router_ports_management",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_enable_static_router_port_vlan1_eth1_1', {
                    "mrouterEnable": True
                }),
                description="啟用VLAN 1 eth1/1靜態路由器端口"
            ),
            
            # 啟用VLAN 1 eth1/2靜態路由器端口
            self.create_test_case(
                name="igmpsnoop_enable_static_router_port_vlan1_eth1_2",
                method="PUT",
                url="/api/v1/igmpsnp/static-router-port/1/eth1%2f2",
                category="igmpsnoop_static_router_ports_management",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_enable_static_router_port_vlan1_eth1_2', {
                    "mrouterEnable": True
                }),
                description="啟用VLAN 1 eth1/2靜態路由器端口"
            ),
            
            # 啟用VLAN 100 eth1/5靜態路由器端口
            self.create_test_case(
                name="igmpsnoop_enable_static_router_port_vlan100_eth1_5",
                method="PUT",
                url="/api/v1/igmpsnp/static-router-port/100/eth1%2f5",
                category="igmpsnoop_static_router_ports_management",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_enable_static_router_port_vlan100_eth1_5', {
                    "mrouterEnable": True
                }),
                description="啟用VLAN 100 eth1/5靜態路由器端口"
            ),
            
            # 啟用VLAN 200 trunk1靜態路由器端口
            self.create_test_case(
                name="igmpsnoop_enable_static_router_port_vlan200_trunk1",
                method="PUT",
                url="/api/v1/igmpsnp/static-router-port/200/trunk1",
                category="igmpsnoop_static_router_ports_management",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_enable_static_router_port_vlan200_trunk1', {
                    "mrouterEnable": True
                }),
                description="啟用VLAN 200 trunk1靜態路由器端口"
            ),
            
            # 禁用VLAN 1 eth1/2靜態路由器端口
            self.create_test_case(
                name="igmpsnoop_disable_static_router_port_vlan1_eth1_2",
                method="PUT",
                url="/api/v1/igmpsnp/static-router-port/1/eth1%2f2",
                category="igmpsnoop_static_router_ports_management",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_disable_static_router_port_vlan1_eth1_2', {
                    "mrouterEnable": False
                }),
                description="禁用VLAN 1 eth1/2靜態路由器端口"
            ),
            
            # 刪除VLAN 200 trunk1靜態路由器端口
            self.create_test_case(
                name="igmpsnoop_delete_static_router_port_vlan200_trunk1",
                method="DELETE",
                url="/api/v1/igmpsnp/static-router-port/200/trunk1",
                category="igmpsnoop_static_router_ports_management",
                module="igmpsnoop",
                description="刪除VLAN 200 trunk1靜態路由器端口"
            ),
            
            # 驗證靜態路由器端口配置
            self.create_test_case(
                name="igmpsnoop_verify_static_router_ports_configuration",
                method="GET",
                url="/api/v1/igmpsnp/static-router-ports",
                category="igmpsnoop_static_router_ports_management",
                module="igmpsnoop",
                description="驗證靜態路由器端口配置"
            )
        ]
    
    def get_igmpsnoop_information_query_tests(self) -> List[APITestCase]:
        """IGMP Snooping Information Query API 測試案例"""
        return [
            # 驗證IGMP Snooping響應格式
            self.create_test_case(
                name="igmpsnoop_verify_response_format",
                method="GET",
                url="/api/v1/igmpsnp",
                category="igmpsnoop_information_query",
                module="igmpsnoop",
                description="驗證IGMP Snooping響應格式"
            ),
            
            # 檢查IGMP Snooping配置完整性
            self.create_test_case(
                name="igmpsnoop_check_configuration_completeness",
                method="GET",
                url="/api/v1/igmpsnp/vlans",
                category="igmpsnoop_information_query",
                module="igmpsnoop",
                description="檢查IGMP Snooping配置完整性"
            ),
            
            # 多次查詢IGMP Snooping配置一致性
            self.create_test_case(
                name="igmpsnoop_multiple_query_consistency",
                method="GET",
                url="/api/v1/igmpsnp",
                category="igmpsnoop_information_query",
                module="igmpsnoop",
                description="多次查詢IGMP Snooping配置一致性"
            ),
            
            # IGMP Snooping查詢性能測試
            self.create_test_case(
                name="igmpsnoop_query_performance_test",
                method="GET",
                url="/api/v1/igmpsnp/vlans",
                category="igmpsnoop_information_query",
                module="igmpsnoop",
                description="IGMP Snooping查詢性能測試"
            ),
            
            # 檢查靜態路由器端口信息完整性
            self.create_test_case(
                name="igmpsnoop_check_static_router_ports_completeness",
                method="GET",
                url="/api/v1/igmpsnp/static-router-ports",
                category="igmpsnoop_information_query",
                module="igmpsnoop",
                description="檢查靜態路由器端口信息完整性"
            )
        ]
    
    def get_igmpsnoop_advanced_operations_tests(self) -> List[APITestCase]:
        """IGMP Snooping Advanced Operations API 測試案例"""
        return [
            # 配置企業級IGMP Snooping環境
            self.create_test_case(
                name="igmpsnoop_configure_enterprise_environment",
                method="PUT",
                url="/api/v1/igmpsnp",
                category="igmpsnoop_advanced_operations",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_enterprise_config', {
                    "igmpSnpEnable": True
                }),
                description="配置企業級IGMP Snooping環境"
            ),
            
            # 批量配置多個VLAN的IGMP Snooping
            self.create_test_case(
                name="igmpsnoop_batch_configure_multiple_vlans_1",
                method="PUT",
                url="/api/v1/igmpsnp/vlans/10",
                category="igmpsnoop_advanced_operations",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_batch_vlan_10', {
                    "igmpSnpEnable": True
                }),
                description="批量配置VLAN 10的IGMP Snooping"
            ),
            
            # 批量配置多個VLAN的IGMP Snooping - VLAN 20
            self.create_test_case(
                name="igmpsnoop_batch_configure_multiple_vlans_2",
                method="PUT",
                url="/api/v1/igmpsnp/vlans/20",
                category="igmpsnoop_advanced_operations",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_batch_vlan_20', {
                    "igmpSnpEnable": True
                }),
                description="批量配置VLAN 20的IGMP Snooping"
            ),
            
            # 批量配置多個VLAN的IGMP Snooping - VLAN 30
            self.create_test_case(
                name="igmpsnoop_batch_configure_multiple_vlans_3",
                method="PUT",
                url="/api/v1/igmpsnp/vlans/30",
                category="igmpsnoop_advanced_operations",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_batch_vlan_30', {
                    "igmpSnpEnable": True
                }),
                description="批量配置VLAN 30的IGMP Snooping"
            ),
            
            # 配置多個靜態路由器端口 - eth1/10
            self.create_test_case(
                name="igmpsnoop_configure_multiple_static_router_ports_1",
                method="PUT",
                url="/api/v1/igmpsnp/static-router-port/10/eth1%2f10",
                category="igmpsnoop_advanced_operations",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_static_port_vlan10_eth1_10', {
                    "mrouterEnable": True
                }),
                description="配置VLAN 10 eth1/10靜態路由器端口"
            ),
            
            # 配置多個靜態路由器端口 - eth1/11
            self.create_test_case(
                name="igmpsnoop_configure_multiple_static_router_ports_2",
                method="PUT",
                url="/api/v1/igmpsnp/static-router-port/20/eth1%2f11",
                category="igmpsnoop_advanced_operations",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_static_port_vlan20_eth1_11', {
                    "mrouterEnable": True
                }),
                description="配置VLAN 20 eth1/11靜態路由器端口"
            ),
            
            # 配置多個靜態路由器端口 - trunk2
            self.create_test_case(
                name="igmpsnoop_configure_multiple_static_router_ports_3",
                method="PUT",
                url="/api/v1/igmpsnp/static-router-port/30/trunk2",
                category="igmpsnoop_advanced_operations",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_static_port_vlan30_trunk2', {
                    "mrouterEnable": True
                }),
                description="配置VLAN 30 trunk2靜態路由器端口"
            ),
            
            # 動態調整IGMP Snooping配置
            self.create_test_case(
                name="igmpsnoop_dynamic_adjust_configuration",
                method="PUT",
                url="/api/v1/igmpsnp/querier",
                category="igmpsnoop_advanced_operations",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_dynamic_querier_config', {
                    "querierEnable": True
                }),
                description="動態調整IGMP Snooping查詢器配置"
            ),
            
            # 驗證高級操作結果
            self.create_test_case(
                name="igmpsnoop_verify_advanced_operations_results",
                method="GET",
                url="/api/v1/igmpsnp/vlans",
                category="igmpsnoop_advanced_operations",
                module="igmpsnoop",
                description="驗證高級操作結果"
            ),
            
            # 驗證靜態路由器端口高級配置結果
            self.create_test_case(
                name="igmpsnoop_verify_static_router_ports_advanced_results",
                method="GET",
                url="/api/v1/igmpsnp/static-router-ports",
                category="igmpsnoop_advanced_operations",
                module="igmpsnoop",
                description="驗證靜態路由器端口高級配置結果"
            )
        ]
    
    def get_igmpsnoop_error_handling_tests(self) -> List[APITestCase]:
        """IGMP Snooping Error Handling API 測試案例"""
        return [
            # 測試無效的VLAN ID - 超出範圍
            self.create_test_case(
                name="igmpsnoop_test_invalid_vlan_id_out_of_range",
                method="GET",
                url="/api/v1/igmpsnp/vlans/5000",
                category="igmpsnoop_error_handling",
                module="igmpsnoop",
                expected_status=400,
                description="測試無效的VLAN ID - 超出範圍 (>4094)"
            ),
            
            # 測試無效的VLAN ID - 零
            self.create_test_case(
                name="igmpsnoop_test_invalid_vlan_id_zero",
                method="GET",
                url="/api/v1/igmpsnp/vlans/0",
                category="igmpsnoop_error_handling",
                module="igmpsnoop",
                expected_status=400,
                description="測試無效的VLAN ID - 零"
            ),
            
            # 測試無效的布爾值 - 全局配置
            self.create_test_case(
                name="igmpsnoop_test_invalid_boolean_global",
                method="PUT",
                url="/api/v1/igmpsnp",
                category="igmpsnoop_error_handling",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_invalid_boolean_global', {
                    "igmpSnpEnable": "invalid_boolean"
                }),
                expected_status=400,
                description="測試無效的布爾值 - 全局配置"
            ),
            
            # 測試無效的布爾值 - VLAN配置
            self.create_test_case(
                name="igmpsnoop_test_invalid_boolean_vlan",
                method="PUT",
                url="/api/v1/igmpsnp/vlans/100",
                category="igmpsnoop_error_handling",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_invalid_boolean_vlan', {
                    "igmpSnpEnable": "yes"
                }),
                expected_status=400,
                description="測試無效的布爾值 - VLAN配置"
            ),
            
            # 測試無效的布爾值 - 查詢器配置
            self.create_test_case(
                name="igmpsnoop_test_invalid_boolean_querier",
                method="PUT",
                url="/api/v1/igmpsnp/querier",
                category="igmpsnoop_error_handling",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_invalid_boolean_querier', {
                    "querierEnable": 1
                }),
                expected_status=400,
                description="測試無效的布爾值 - 查詢器配置"
            ),
            
            # 測試無效的接口ID格式
            self.create_test_case(
                name="igmpsnoop_test_invalid_interface_id_format",
                method="GET",
                url="/api/v1/igmpsnp/static-router-port/1/invalid_interface",
                category="igmpsnoop_error_handling",
                module="igmpsnoop",
                expected_status=400,
                description="測試無效的接口ID格式"
            ),
            
            # 測試無效JSON格式 - 全局配置
            self.create_test_case(
                name="igmpsnoop_test_invalid_json_global",
                method="PUT",
                url="/api/v1/igmpsnp",
                category="igmpsnoop_error_handling",
                module="igmpsnoop",
                body="invalid json format",
                expected_status=400,
                description="測試無效JSON格式 - 全局配置"
            ),
            
            # 測試無效JSON格式 - VLAN配置
            self.create_test_case(
                name="igmpsnoop_test_invalid_json_vlan",
                method="PUT",
                url="/api/v1/igmpsnp/vlans/100",
                category="igmpsnoop_error_handling",
                module="igmpsnoop",
                body="{ invalid json }",
                expected_status=400,
                description="測試無效JSON格式 - VLAN配置"
            ),
            
            # 測試缺少必需參數 - 全局配置
            self.create_test_case(
                name="igmpsnoop_test_missing_required_params_global",
                method="PUT",
                url="/api/v1/igmpsnp",
                category="igmpsnoop_error_handling",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_missing_params_global', {}),
                expected_status=400,
                description="測試缺少必需參數 - 全局配置"
            ),
            
            # 測試缺少必需參數 - 靜態路由器端口
            self.create_test_case(
                name="igmpsnoop_test_missing_required_params_static_port",
                method="PUT",
                url="/api/v1/igmpsnp/static-router-port/1/eth1%2f1",
                category="igmpsnoop_error_handling",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_missing_params_static_port', {}),
                expected_status=400,
                description="測試缺少必需參數 - 靜態路由器端口"
            ),
            
            # 測試無效的參數名稱
            self.create_test_case(
                name="igmpsnoop_test_invalid_parameter_names",
                method="PUT",
                url="/api/v1/igmpsnp",
                category="igmpsnoop_error_handling",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_invalid_parameter_names', {
                    "invalidParameter": True,
                    "anotherInvalidParam": False
                }),
                expected_status=400,
                description="測試無效的參數名稱"
            ),
            
            # 測試刪除不存在的靜態路由器端口
            self.create_test_case(
                name="igmpsnoop_test_delete_nonexistent_static_port",
                method="DELETE",
                url="/api/v1/igmpsnp/static-router-port/999/eth1%2f99",
                category="igmpsnoop_error_handling",
                module="igmpsnoop",
                expected_status=500,
                description="測試刪除不存在的靜態路由器端口"
            ),
            
            # 恢復正常IGMP Snooping配置
            self.create_test_case(
                name="igmpsnoop_restore_normal_configuration",
                method="PUT",
                url="/api/v1/igmpsnp",
                category="igmpsnoop_error_handling",
                module="igmpsnoop",
                body=self.test_data.get('igmpsnoop_restore_normal_config', {
                    "igmpSnpEnable": True
                }),
                description="恢復正常IGMP Snooping配置"
            ),
            
            # 最終IGMP Snooping狀態檢查
            self.create_test_case(
                name="igmpsnoop_final_status_check",
                method="GET",
                url="/api/v1/igmpsnp",
                category="igmpsnoop_error_handling",
                module="igmpsnoop",
                description="最終IGMP Snooping狀態檢查"
            )
        ]