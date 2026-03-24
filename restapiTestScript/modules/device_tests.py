#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Device 模組測試案例
包含設備信息查詢、設備屬性驗證等相關API測試
支援設備類型、製造商、硬體版本、軟體版本、序列號、機箱ID等信息查詢
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class DEVICETests(BaseTests):
    """Device 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取Device模組支援的類別"""
        return [
            "device_information_query",
            "device_attributes_verification",
            "device_system_information",
            "device_hardware_information",
            "device_software_information",
            "device_network_information"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有Device測試案例"""
        all_tests = []
        all_tests.extend(self.get_device_information_query_tests())
        all_tests.extend(self.get_device_attributes_verification_tests())
        all_tests.extend(self.get_device_system_information_tests())
        all_tests.extend(self.get_device_hardware_information_tests())
        all_tests.extend(self.get_device_software_information_tests())
        all_tests.extend(self.get_device_network_information_tests())
        return all_tests
    
    def get_device_information_query_tests(self) -> List[APITestCase]:
        """Device Information Query API 測試案例"""
        return [
            # 獲取設備基本信息
            self.create_test_case(
                name="device_get_basic_information",
                method="GET",
                url="/api/v1/device",
                category="device_information_query",
                module="device",
                description="獲取設備基本信息"
            ),
            
            # 驗證設備信息響應格式
            self.create_test_case(
                name="device_verify_response_format",
                method="GET",
                url="/api/v1/device",
                category="device_information_query",
                module="device",
                description="驗證設備信息響應格式"
            ),
            
            # 檢查設備信息完整性
            self.create_test_case(
                name="device_check_information_completeness",
                method="GET",
                url="/api/v1/device",
                category="device_information_query",
                module="device",
                description="檢查設備信息完整性"
            ),
            
            # 多次查詢設備信息一致性
            self.create_test_case(
                name="device_multiple_query_consistency",
                method="GET",
                url="/api/v1/device",
                category="device_information_query",
                module="device",
                description="多次查詢設備信息一致性"
            ),
            
            # 設備信息查詢性能測試
            self.create_test_case(
                name="device_query_performance_test",
                method="GET",
                url="/api/v1/device",
                category="device_information_query",
                module="device",
                description="設備信息查詢性能測試"
            )
        ]
    
    def get_device_attributes_verification_tests(self) -> List[APITestCase]:
        """Device Attributes Verification API 測試案例"""
        return [
            # 驗證設備類型屬性
            self.create_test_case(
                name="device_verify_type_attribute",
                method="GET",
                url="/api/v1/device",
                category="device_attributes_verification",
                module="device",
                description="驗證設備類型屬性"
            ),
            
            # 驗證製造商屬性
            self.create_test_case(
                name="device_verify_manufacturer_attribute",
                method="GET",
                url="/api/v1/device",
                category="device_attributes_verification",
                module="device",
                description="驗證製造商屬性"
            ),
            
            # 驗證硬體版本屬性
            self.create_test_case(
                name="device_verify_hardware_version_attribute",
                method="GET",
                url="/api/v1/device",
                category="device_attributes_verification",
                module="device",
                description="驗證硬體版本屬性"
            ),
            
            # 驗證軟體版本屬性
            self.create_test_case(
                name="device_verify_software_version_attribute",
                method="GET",
                url="/api/v1/device",
                category="device_attributes_verification",
                module="device",
                description="驗證軟體版本屬性"
            ),
            
            # 驗證序列號屬性
            self.create_test_case(
                name="device_verify_serial_number_attribute",
                method="GET",
                url="/api/v1/device",
                category="device_attributes_verification",
                module="device",
                description="驗證序列號屬性"
            ),
            
            # 驗證機箱ID屬性
            self.create_test_case(
                name="device_verify_chassis_id_attribute",
                method="GET",
                url="/api/v1/device",
                category="device_attributes_verification",
                module="device",
                description="驗證機箱ID屬性"
            ),
            
            # 驗證所有屬性存在性
            self.create_test_case(
                name="device_verify_all_attributes_existence",
                method="GET",
                url="/api/v1/device",
                category="device_attributes_verification",
                module="device",
                description="驗證所有屬性存在性"
            ),
            
            # 驗證屬性數據類型
            self.create_test_case(
                name="device_verify_attributes_data_types",
                method="GET",
                url="/api/v1/device",
                category="device_attributes_verification",
                module="device",
                description="驗證屬性數據類型"
            )
        ]
    
    def get_device_system_information_tests(self) -> List[APITestCase]:
        """Device System Information API 測試案例"""
        return [
            # 分析設備類型信息
            self.create_test_case(
                name="device_analyze_type_information",
                method="GET",
                url="/api/v1/device",
                category="device_system_information",
                module="device",
                description="分析設備類型信息"
            ),
            
            # 檢查設備類型格式
            self.create_test_case(
                name="device_check_type_format",
                method="GET",
                url="/api/v1/device",
                category="device_system_information",
                module="device",
                description="檢查設備類型格式"
            ),
            
            # 驗證設備類型長度限制
            self.create_test_case(
                name="device_verify_type_length_limit",
                method="GET",
                url="/api/v1/device",
                category="device_system_information",
                module="device",
                description="驗證設備類型長度限制 (最大255字符)"
            ),
            
            # 分析製造商信息
            self.create_test_case(
                name="device_analyze_manufacturer_information",
                method="GET",
                url="/api/v1/device",
                category="device_system_information",
                module="device",
                description="分析製造商信息"
            ),
            
            # 檢查製造商名稱格式
            self.create_test_case(
                name="device_check_manufacturer_format",
                method="GET",
                url="/api/v1/device",
                category="device_system_information",
                module="device",
                description="檢查製造商名稱格式"
            ),
            
            # 驗證系統信息完整性
            self.create_test_case(
                name="device_verify_system_info_completeness",
                method="GET",
                url="/api/v1/device",
                category="device_system_information",
                module="device",
                description="驗證系統信息完整性"
            )
        ]
    
    def get_device_hardware_information_tests(self) -> List[APITestCase]:
        """Device Hardware Information API 測試案例"""
        return [
            # 分析硬體版本信息
            self.create_test_case(
                name="device_analyze_hardware_version",
                method="GET",
                url="/api/v1/device",
                category="device_hardware_information",
                module="device",
                description="分析硬體版本信息"
            ),
            
            # 檢查硬體版本格式
            self.create_test_case(
                name="device_check_hardware_version_format",
                method="GET",
                url="/api/v1/device",
                category="device_hardware_information",
                module="device",
                description="檢查硬體版本格式"
            ),
            
            # 驗證序列號格式
            self.create_test_case(
                name="device_verify_serial_number_format",
                method="GET",
                url="/api/v1/device",
                category="device_hardware_information",
                module="device",
                description="驗證序列號格式"
            ),
            
            # 分析序列號唯一性
            self.create_test_case(
                name="device_analyze_serial_number_uniqueness",
                method="GET",
                url="/api/v1/device",
                category="device_hardware_information",
                module="device",
                description="分析序列號唯一性"
            ),
            
            # 檢查機箱ID格式
            self.create_test_case(
                name="device_check_chassis_id_format",
                method="GET",
                url="/api/v1/device",
                category="device_hardware_information",
                module="device",
                description="檢查機箱ID格式 (CPU MAC)"
            ),
            
            # 驗證機箱ID MAC地址格式
            self.create_test_case(
                name="device_verify_chassis_id_mac_format",
                method="GET",
                url="/api/v1/device",
                category="device_hardware_information",
                module="device",
                description="驗證機箱ID MAC地址格式"
            ),
            
            # 分析硬體信息一致性
            self.create_test_case(
                name="device_analyze_hardware_info_consistency",
                method="GET",
                url="/api/v1/device",
                category="device_hardware_information",
                module="device",
                description="分析硬體信息一致性"
            )
        ]
    
    def get_device_software_information_tests(self) -> List[APITestCase]:
        """Device Software Information API 測試案例"""
        return [
            # 分析軟體版本信息
            self.create_test_case(
                name="device_analyze_software_version",
                method="GET",
                url="/api/v1/device",
                category="device_software_information",
                module="device",
                description="分析軟體版本信息"
            ),
            
            # 檢查軟體版本格式
            self.create_test_case(
                name="device_check_software_version_format",
                method="GET",
                url="/api/v1/device",
                category="device_software_information",
                module="device",
                description="檢查軟體版本格式"
            ),
            
            # 驗證軟體版本號結構
            self.create_test_case(
                name="device_verify_software_version_structure",
                method="GET",
                url="/api/v1/device",
                category="device_software_information",
                module="device",
                description="驗證軟體版本號結構 (例如: 1.0.0.6)"
            ),
            
            # 分析軟體版本兼容性
            self.create_test_case(
                name="device_analyze_software_compatibility",
                method="GET",
                url="/api/v1/device",
                category="device_software_information",
                module="device",
                description="分析軟體版本兼容性"
            ),
            
            # 檢查軟體更新狀態
            self.create_test_case(
                name="device_check_software_update_status",
                method="GET",
                url="/api/v1/device",
                category="device_software_information",
                module="device",
                description="檢查軟體更新狀態"
            ),
            
            # 驗證軟體信息完整性
            self.create_test_case(
                name="device_verify_software_info_completeness",
                method="GET",
                url="/api/v1/device",
                category="device_software_information",
                module="device",
                description="驗證軟體信息完整性"
            )
        ]
    
    def get_device_network_information_tests(self) -> List[APITestCase]:
        """Device Network Information API 測試案例"""
        return [
            # 分析設備網路身份
            self.create_test_case(
                name="device_analyze_network_identity",
                method="GET",
                url="/api/v1/device",
                category="device_network_information",
                module="device",
                description="分析設備網路身份"
            ),
            
            # 檢查設備網路配置
            self.create_test_case(
                name="device_check_network_configuration",
                method="GET",
                url="/api/v1/device",
                category="device_network_information",
                module="device",
                description="檢查設備網路配置"
            ),
            
            # 驗證設備管理接口
            self.create_test_case(
                name="device_verify_management_interface",
                method="GET",
                url="/api/v1/device",
                category="device_network_information",
                module="device",
                description="驗證設備管理接口"
            ),
            
            # 分析設備連接狀態
            self.create_test_case(
                name="device_analyze_connection_status",
                method="GET",
                url="/api/v1/device",
                category="device_network_information",
                module="device",
                description="分析設備連接狀態"
            ),
            
            # 檢查設備可達性
            self.create_test_case(
                name="device_check_reachability",
                method="GET",
                url="/api/v1/device",
                category="device_network_information",
                module="device",
                description="檢查設備可達性"
            ),
            
            # 驗證設備響應時間
            self.create_test_case(
                name="device_verify_response_time",
                method="GET",
                url="/api/v1/device",
                category="device_network_information",
                module="device",
                description="驗證設備響應時間"
            ),
            
            # 分析設備網路性能
            self.create_test_case(
                name="device_analyze_network_performance",
                method="GET",
                url="/api/v1/device",
                category="device_network_information",
                module="device",
                description="分析設備網路性能"
            ),
            
            # 檢查設備API可用性
            self.create_test_case(
                name="device_check_api_availability",
                method="GET",
                url="/api/v1/device",
                category="device_network_information",
                module="device",
                description="檢查設備API可用性"
            ),
            
            # 驗證設備服務狀態
            self.create_test_case(
                name="device_verify_service_status",
                method="GET",
                url="/api/v1/device",
                category="device_network_information",
                module="device",
                description="驗證設備服務狀態"
            ),
            
            # 最終設備狀態檢查
            self.create_test_case(
                name="device_final_status_check",
                method="GET",
                url="/api/v1/device",
                category="device_network_information",
                module="device",
                description="最終設備狀態檢查"
            )
        ]