#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Management IP Filter 模組測試案例
包含管理IP過濾器配置、客戶端類型管理、IP地址範圍設置等相關API測試
支援HTTP、SNMP、Telnet客戶端類型過濾、IP地址範圍管理、過濾規則增刪改查等操作
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class MGMT_IP_FILTERTests(BaseTests):
    """Management IP Filter 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取Management IP Filter模組支援的類別"""
        return [
            "mgmt_ip_filter_basic_operations",
            "mgmt_ip_filter_client_type_management",
            "mgmt_ip_filter_address_range_management",
            "mgmt_ip_filter_advanced_operations",
            "mgmt_ip_filter_error_handling"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有Management IP Filter測試案例"""
        all_tests = []
        all_tests.extend(self.get_mgmt_ip_filter_basic_operations_tests())
        all_tests.extend(self.get_mgmt_ip_filter_client_type_management_tests())
        all_tests.extend(self.get_mgmt_ip_filter_address_range_management_tests())
        all_tests.extend(self.get_mgmt_ip_filter_advanced_operations_tests())
        all_tests.extend(self.get_mgmt_ip_filter_error_handling_tests())
        return all_tests
    
    def get_mgmt_ip_filter_basic_operations_tests(self) -> List[APITestCase]:
        """Management IP Filter Basic Operations API 測試案例"""
        return [
            # 獲取所有管理IP過濾器
            self.create_test_case(
                name="mgmt_ip_filter_get_all_filters",
                method="GET",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_basic_operations",
                module="mgmt_ip_filter",
                description="獲取所有管理IP過濾器配置"
            ),
            
            # 驗證初始過濾器狀態
            self.create_test_case(
                name="mgmt_ip_filter_verify_initial_state",
                method="GET",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_basic_operations",
                module="mgmt_ip_filter",
                description="驗證初始過濾器狀態"
            ),
            
            # 檢查過濾器響應格式
            self.create_test_case(
                name="mgmt_ip_filter_check_response_format",
                method="GET",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_basic_operations",
                module="mgmt_ip_filter",
                description="檢查過濾器響應格式"
            )
        ]
    
    def get_mgmt_ip_filter_client_type_management_tests(self) -> List[APITestCase]:
        """Management IP Filter Client Type Management API 測試案例"""
        return [
            # 添加HTTP客戶端過濾器
            self.create_test_case(
                name="mgmt_ip_filter_add_http_client_filter",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_client_type_management",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_http_client', {
                    "type": "http",
                    "startAddress": "192.168.2.30",
                    "endAddress": "192.168.2.50"
                }),
                description="添加HTTP客戶端過濾器"
            ),
            
            # 添加SNMP客戶端過濾器
            self.create_test_case(
                name="mgmt_ip_filter_add_snmp_client_filter",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_client_type_management",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_snmp_client', {
                    "type": "snmp",
                    "startAddress": "192.168.1.9",
                    "endAddress": "192.168.1.9"
                }),
                description="添加SNMP客戶端過濾器"
            ),
            
            # 添加Telnet客戶端過濾器
            self.create_test_case(
                name="mgmt_ip_filter_add_telnet_client_filter",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_client_type_management",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_telnet_client', {
                    "type": "telnet",
                    "startAddress": "192.168.66.1",
                    "endAddress": "192.168.66.10"
                }),
                description="添加Telnet客戶端過濾器"
            ),
            
            # 添加企業級HTTP過濾器
            self.create_test_case(
                name="mgmt_ip_filter_add_enterprise_http_filter",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_client_type_management",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_enterprise_http', {
                    "type": "http",
                    "startAddress": "10.0.0.1",
                    "endAddress": "10.0.0.100"
                }),
                description="添加企業級HTTP過濾器"
            ),
            
            # 添加數據中心SNMP過濾器
            self.create_test_case(
                name="mgmt_ip_filter_add_datacenter_snmp_filter",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_client_type_management",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_datacenter_snmp', {
                    "type": "snmp",
                    "startAddress": "172.16.1.1",
                    "endAddress": "172.16.1.50"
                }),
                description="添加數據中心SNMP過濾器"
            ),
            
            # 驗證客戶端類型過濾器添加結果
            self.create_test_case(
                name="mgmt_ip_filter_verify_client_type_filters_added",
                method="GET",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_client_type_management",
                module="mgmt_ip_filter",
                description="驗證客戶端類型過濾器添加結果"
            )
        ]
    
    def get_mgmt_ip_filter_address_range_management_tests(self) -> List[APITestCase]:
        """Management IP Filter Address Range Management API 測試案例"""
        return [
            # 獲取特定HTTP過濾器
            self.create_test_case(
                name="mgmt_ip_filter_get_specific_http_filter",
                method="GET",
                url="/api/v1/mgmt-ip-filter/client-type/http/start-address/192.168.2.30",
                category="mgmt_ip_filter_address_range_management",
                module="mgmt_ip_filter",
                description="獲取特定HTTP過濾器"
            ),
            
            # 獲取特定SNMP過濾器
            self.create_test_case(
                name="mgmt_ip_filter_get_specific_snmp_filter",
                method="GET",
                url="/api/v1/mgmt-ip-filter/client-type/snmp/start-address/192.168.1.9",
                category="mgmt_ip_filter_address_range_management",
                module="mgmt_ip_filter",
                description="獲取特定SNMP過濾器"
            ),
            
            # 獲取特定Telnet過濾器
            self.create_test_case(
                name="mgmt_ip_filter_get_specific_telnet_filter",
                method="GET",
                url="/api/v1/mgmt-ip-filter/client-type/telnet/start-address/192.168.66.1",
                category="mgmt_ip_filter_address_range_management",
                module="mgmt_ip_filter",
                description="獲取特定Telnet過濾器"
            ),
            
            # 更新HTTP過濾器地址範圍
            self.create_test_case(
                name="mgmt_ip_filter_update_http_filter_range",
                method="PUT",
                url="/api/v1/mgmt-ip-filter/client-type/http/start-address/192.168.2.30",
                category="mgmt_ip_filter_address_range_management",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_update_http_range', {
                    "endAddress": "192.168.2.100"
                }),
                description="更新HTTP過濾器地址範圍"
            ),
            
            # 更新Telnet過濾器地址範圍
            self.create_test_case(
                name="mgmt_ip_filter_update_telnet_filter_range",
                method="PUT",
                url="/api/v1/mgmt-ip-filter/client-type/telnet/start-address/192.168.66.1",
                category="mgmt_ip_filter_address_range_management",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_update_telnet_range', {
                    "endAddress": "192.168.66.50"
                }),
                description="更新Telnet過濾器地址範圍"
            ),
            
            # 更新企業級HTTP過濾器範圍
            self.create_test_case(
                name="mgmt_ip_filter_update_enterprise_http_range",
                method="PUT",
                url="/api/v1/mgmt-ip-filter/client-type/http/start-address/10.0.0.1",
                category="mgmt_ip_filter_address_range_management",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_update_enterprise_http_range', {
                    "endAddress": "10.0.0.200"
                }),
                description="更新企業級HTTP過濾器範圍"
            ),
            
            # 驗證地址範圍更新結果
            self.create_test_case(
                name="mgmt_ip_filter_verify_address_range_updates",
                method="GET",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_address_range_management",
                module="mgmt_ip_filter",
                description="驗證地址範圍更新結果"
            ),
            
            # 驗證特定更新的HTTP過濾器
            self.create_test_case(
                name="mgmt_ip_filter_verify_updated_http_filter",
                method="GET",
                url="/api/v1/mgmt-ip-filter/client-type/http/start-address/192.168.2.30",
                category="mgmt_ip_filter_address_range_management",
                module="mgmt_ip_filter",
                description="驗證特定更新的HTTP過濾器"
            )
        ]
    
    def get_mgmt_ip_filter_advanced_operations_tests(self) -> List[APITestCase]:
        """Management IP Filter Advanced Operations API 測試案例"""
        return [
            # 批量添加多個HTTP過濾器 - 過濾器1
            self.create_test_case(
                name="mgmt_ip_filter_batch_add_http_filter_1",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_advanced_operations",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_batch_http_1', {
                    "type": "http",
                    "startAddress": "192.168.10.1",
                    "endAddress": "192.168.10.50"
                }),
                description="批量添加HTTP過濾器 - 過濾器1"
            ),
            
            # 批量添加多個HTTP過濾器 - 過濾器2
            self.create_test_case(
                name="mgmt_ip_filter_batch_add_http_filter_2",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_advanced_operations",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_batch_http_2', {
                    "type": "http",
                    "startAddress": "192.168.20.1",
                    "endAddress": "192.168.20.100"
                }),
                description="批量添加HTTP過濾器 - 過濾器2"
            ),
            
            # 批量添加多個SNMP過濾器 - 過濾器1
            self.create_test_case(
                name="mgmt_ip_filter_batch_add_snmp_filter_1",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_advanced_operations",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_batch_snmp_1', {
                    "type": "snmp",
                    "startAddress": "192.168.30.10",
                    "endAddress": "192.168.30.20"
                }),
                description="批量添加SNMP過濾器 - 過濾器1"
            ),
            
            # 批量添加多個Telnet過濾器 - 過濾器1
            self.create_test_case(
                name="mgmt_ip_filter_batch_add_telnet_filter_1",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_advanced_operations",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_batch_telnet_1', {
                    "type": "telnet",
                    "startAddress": "192.168.40.1",
                    "endAddress": "192.168.40.25"
                }),
                description="批量添加Telnet過濾器 - 過濾器1"
            ),
            
            # 配置複雜的企業級過濾策略
            self.create_test_case(
                name="mgmt_ip_filter_configure_complex_enterprise_policy",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_advanced_operations",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_complex_enterprise_policy', {
                    "type": "http",
                    "startAddress": "10.1.0.1",
                    "endAddress": "10.1.255.255"
                }),
                description="配置複雜的企業級過濾策略"
            ),
            
            # 配置數據中心級過濾策略
            self.create_test_case(
                name="mgmt_ip_filter_configure_datacenter_policy",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_advanced_operations",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_datacenter_policy', {
                    "type": "snmp",
                    "startAddress": "172.16.0.1",
                    "endAddress": "172.16.255.255"
                }),
                description="配置數據中心級過濾策略"
            ),
            
            # 配置單一IP地址過濾器 - HTTP
            self.create_test_case(
                name="mgmt_ip_filter_configure_single_ip_http_filter",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_advanced_operations",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_single_ip_http', {
                    "type": "http",
                    "startAddress": "192.168.100.100"
                }),
                description="配置單一IP地址過濾器 - HTTP"
            ),
            
            # 配置單一IP地址過濾器 - SNMP
            self.create_test_case(
                name="mgmt_ip_filter_configure_single_ip_snmp_filter",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_advanced_operations",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_single_ip_snmp', {
                    "type": "snmp",
                    "startAddress": "192.168.200.200"
                }),
                description="配置單一IP地址過濾器 - SNMP"
            ),
            
            # 動態調整過濾器策略
            self.create_test_case(
                name="mgmt_ip_filter_dynamic_adjust_filter_policy",
                method="PUT",
                url="/api/v1/mgmt-ip-filter/client-type/http/start-address/192.168.10.1",
                category="mgmt_ip_filter_advanced_operations",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_dynamic_adjust_policy', {
                    "endAddress": "192.168.10.200"
                }),
                description="動態調整過濾器策略"
            ),
            
            # 驗證高級操作結果
            self.create_test_case(
                name="mgmt_ip_filter_verify_advanced_operations_results",
                method="GET",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_advanced_operations",
                module="mgmt_ip_filter",
                description="驗證高級操作結果"
            ),
            
            # 驗證批量過濾器配置
            self.create_test_case(
                name="mgmt_ip_filter_verify_batch_filter_configuration",
                method="GET",
                url="/api/v1/mgmt-ip-filter/client-type/http/start-address/192.168.10.1",
                category="mgmt_ip_filter_advanced_operations",
                module="mgmt_ip_filter",
                description="驗證批量過濾器配置"
            )
        ]
    
    def get_mgmt_ip_filter_error_handling_tests(self) -> List[APITestCase]:
        """Management IP Filter Error Handling API 測試案例"""
        return [
            # 測試無效的客戶端類型
            self.create_test_case(
                name="mgmt_ip_filter_test_invalid_client_type",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_invalid_client_type', {
                    "type": "invalid_type",
                    "startAddress": "192.168.1.1",
                    "endAddress": "192.168.1.10"
                }),
                expected_status=400,
                description="測試無效的客戶端類型 (非http/snmp/telnet)"
            ),
            
            # 測試無效的IP地址格式 - 起始地址
            self.create_test_case(
                name="mgmt_ip_filter_test_invalid_start_address_format",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_invalid_start_address', {
                    "type": "http",
                    "startAddress": "invalid.ip.address",
                    "endAddress": "192.168.1.10"
                }),
                expected_status=400,
                description="測試無效的IP地址格式 - 起始地址"
            ),
            
            # 測試無效的IP地址格式 - 結束地址
            self.create_test_case(
                name="mgmt_ip_filter_test_invalid_end_address_format",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_invalid_end_address', {
                    "type": "http",
                    "startAddress": "192.168.1.1",
                    "endAddress": "invalid.end.address"
                }),
                expected_status=400,
                description="測試無效的IP地址格式 - 結束地址"
            ),
            
            # 測試IP地址範圍錯誤 - 起始地址大於結束地址
            self.create_test_case(
                name="mgmt_ip_filter_test_invalid_ip_range_start_greater_than_end",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_invalid_ip_range', {
                    "type": "http",
                    "startAddress": "192.168.1.100",
                    "endAddress": "192.168.1.10"  # 結束地址小於起始地址
                }),
                expected_status=400,
                description="測試IP地址範圍錯誤 - 起始地址大於結束地址"
            ),
            
            # 測試超出IPv4地址範圍
            self.create_test_case(
                name="mgmt_ip_filter_test_out_of_ipv4_range",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_out_of_ipv4_range', {
                    "type": "http",
                    "startAddress": "300.300.300.300",  # 超出IPv4範圍
                    "endAddress": "192.168.1.10"
                }),
                expected_status=400,
                description="測試超出IPv4地址範圍"
            ),
            
            # 測試缺少必需參數 - 客戶端類型
            self.create_test_case(
                name="mgmt_ip_filter_test_missing_required_param_type",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_missing_type', {
                    "startAddress": "192.168.1.1",
                    "endAddress": "192.168.1.10"
                    # 缺少type參數
                }),
                expected_status=400,
                description="測試缺少必需參數 - 客戶端類型"
            ),
            
            # 測試缺少必需參數 - 起始地址
            self.create_test_case(
                name="mgmt_ip_filter_test_missing_required_param_start_address",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_missing_start_address', {
                    "type": "http",
                    "endAddress": "192.168.1.10"
                    # 缺少startAddress參數
                }),
                expected_status=400,
                description="測試缺少必需參數 - 起始地址"
            ),
            
            # 測試無效JSON格式 - 添加過濾器
            self.create_test_case(
                name="mgmt_ip_filter_test_invalid_json_add_filter",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                body="invalid json format",
                expected_status=400,
                description="測試無效JSON格式 - 添加過濾器"
            ),
            
            # 測試無效JSON格式 - 更新過濾器
            self.create_test_case(
                name="mgmt_ip_filter_test_invalid_json_update_filter",
                method="PUT",
                url="/api/v1/mgmt-ip-filter/client-type/http/start-address/192.168.1.1",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                body="{ invalid json }",
                expected_status=400,
                description="測試無效JSON格式 - 更新過濾器"
            ),
            
            # 測試不存在的過濾器 - 獲取
            self.create_test_case(
                name="mgmt_ip_filter_test_nonexistent_filter_get",
                method="GET",
                url="/api/v1/mgmt-ip-filter/client-type/http/start-address/999.999.999.999",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                expected_status=400,
                description="測試不存在的過濾器 - 獲取"
            ),
            
            # 測試不存在的過濾器 - 更新
            self.create_test_case(
                name="mgmt_ip_filter_test_nonexistent_filter_update",
                method="PUT",
                url="/api/v1/mgmt-ip-filter/client-type/http/start-address/999.999.999.999",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_nonexistent_filter_update', {
                    "endAddress": "192.168.1.10"
                }),
                expected_status=400,
                description="測試不存在的過濾器 - 更新"
            ),
            
            # 測試不存在的過濾器 - 刪除
            self.create_test_case(
                name="mgmt_ip_filter_test_nonexistent_filter_delete",
                method="DELETE",
                url="/api/v1/mgmt-ip-filter/client-type/http/start-address/999.999.999.999",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                expected_status=400,
                description="測試不存在的過濾器 - 刪除"
            ),
            
            # 測試重複添加相同過濾器
            self.create_test_case(
                name="mgmt_ip_filter_test_duplicate_filter_addition",
                method="POST",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                body=self.test_data.get('mgmt_ip_filter_duplicate_filter', {
                    "type": "http",
                    "startAddress": "192.168.2.30",  # 已存在的過濾器
                    "endAddress": "192.168.2.50"
                }),
                expected_status=400,
                description="測試重複添加相同過濾器"
            ),
            
            # 測試無效的URL編碼 - 客戶端類型
            self.create_test_case(
                name="mgmt_ip_filter_test_invalid_url_encoding_client_type",
                method="GET",
                url="/api/v1/mgmt-ip-filter/client-type/invalid%type/start-address/192.168.1.1",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                expected_status=400,
                description="測試無效的URL編碼 - 客戶端類型"
            ),
            
            # 測試無效的URL編碼 - IP地址
            self.create_test_case(
                name="mgmt_ip_filter_test_invalid_url_encoding_ip_address",
                method="GET",
                url="/api/v1/mgmt-ip-filter/client-type/http/start-address/invalid%ip",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                expected_status=400,
                description="測試無效的URL編碼 - IP地址"
            ),
            
            # 清理測試過濾器 - 刪除HTTP過濾器
            self.create_test_case(
                name="mgmt_ip_filter_cleanup_delete_http_filter",
                method="DELETE",
                url="/api/v1/mgmt-ip-filter/client-type/http/start-address/192.168.2.30",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                description="清理測試過濾器 - 刪除HTTP過濾器"
            ),
            
            # 清理測試過濾器 - 刪除SNMP過濾器
            self.create_test_case(
                name="mgmt_ip_filter_cleanup_delete_snmp_filter",
                method="DELETE",
                url="/api/v1/mgmt-ip-filter/client-type/snmp/start-address/192.168.1.9",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                description="清理測試過濾器 - 刪除SNMP過濾器"
            ),
            
            # 清理測試過濾器 - 刪除Telnet過濾器
            self.create_test_case(
                name="mgmt_ip_filter_cleanup_delete_telnet_filter",
                method="DELETE",
                url="/api/v1/mgmt-ip-filter/client-type/telnet/start-address/192.168.66.1",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                description="清理測試過濾器 - 刪除Telnet過濾器"
            ),
            
            # 最終管理IP過濾器狀態檢查
            self.create_test_case(
                name="mgmt_ip_filter_final_status_check",
                method="GET",
                url="/api/v1/mgmt-ip-filter",
                category="mgmt_ip_filter_error_handling",
                module="mgmt_ip_filter",
                description="最終管理IP過濾器狀態檢查"
            )
        ]