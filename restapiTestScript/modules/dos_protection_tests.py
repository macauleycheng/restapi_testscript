#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DoS Protection 模組測試案例
包含DoS攻擊防護配置、攻擊檢測、速率限制等相關API測試
支援Echo/Chargen攻擊、Smurf攻擊、TCP洪水攻擊、掃描攻擊、UDP洪水攻擊、WinNuke攻擊等防護
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class DOS_PROTECTIONTests(BaseTests):
    """DoS Protection 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取DoS Protection模組支援的類別"""
        return [
            "dos_protection_information_query",
            "dos_protection_configuration_management",
            "dos_protection_attack_types_management",
            "dos_protection_rate_limiting",
            "dos_protection_scan_attacks_management",
            "dos_protection_flood_attacks_management",
            "dos_protection_advanced_operations",
            "dos_protection_error_handling"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有DoS Protection測試案例"""
        all_tests = []
        all_tests.extend(self.get_dos_protection_information_query_tests())
        all_tests.extend(self.get_dos_protection_configuration_management_tests())
        all_tests.extend(self.get_dos_protection_attack_types_management_tests())
        all_tests.extend(self.get_dos_protection_rate_limiting_tests())
        all_tests.extend(self.get_dos_protection_scan_attacks_management_tests())
        all_tests.extend(self.get_dos_protection_flood_attacks_management_tests())
        all_tests.extend(self.get_dos_protection_advanced_operations_tests())
        all_tests.extend(self.get_dos_protection_error_handling_tests())
        return all_tests
    
    def get_dos_protection_information_query_tests(self) -> List[APITestCase]:
        """DoS Protection Information Query API 測試案例"""
        return [
            # 獲取DoS防護配置
            self.create_test_case(
                name="dos_protection_get_configuration",
                method="GET",
                url="/api/v1/security/dos-protection",
                category="dos_protection_information_query",
                module="dos_protection",
                description="獲取DoS防護配置"
            ),
            
            # 驗證DoS防護響應格式
            self.create_test_case(
                name="dos_protection_verify_response_format",
                method="GET",
                url="/api/v1/security/dos-protection",
                category="dos_protection_information_query",
                module="dos_protection",
                description="驗證DoS防護響應格式"
            ),
            
            # 檢查DoS防護配置完整性
            self.create_test_case(
                name="dos_protection_check_configuration_completeness",
                method="GET",
                url="/api/v1/security/dos-protection",
                category="dos_protection_information_query",
                module="dos_protection",
                description="檢查DoS防護配置完整性"
            ),
            
            # 多次查詢DoS防護配置一致性
            self.create_test_case(
                name="dos_protection_multiple_query_consistency",
                method="GET",
                url="/api/v1/security/dos-protection",
                category="dos_protection_information_query",
                module="dos_protection",
                description="多次查詢DoS防護配置一致性"
            ),
            
            # DoS防護查詢性能測試
            self.create_test_case(
                name="dos_protection_query_performance_test",
                method="GET",
                url="/api/v1/security/dos-protection",
                category="dos_protection_information_query",
                module="dos_protection",
                description="DoS防護查詢性能測試"
            )
        ]
    
    def get_dos_protection_configuration_management_tests(self) -> List[APITestCase]:
        """DoS Protection Configuration Management API 測試案例"""
        return [
            # 啟用所有DoS防護功能
            self.create_test_case(
                name="dos_protection_enable_all_protections",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_configuration_management",
                module="dos_protection",
                body=self.test_data.get('dos_protection_enable_all', {
                    "echoChargenStatus": True,
                    "echoChargenRate": 1000,
                    "smurfStatus": True,
                    "tcpFloodingStatus": True,
                    "tcpFloodingRate": 1000,
                    "tcpNullScanStatus": True,
                    "tcpSynFinScanStatus": True,
                    "tcpUdpPortZeroStatus": True,
                    "tcpXmasScanStatus": True,
                    "udpFloodingStatus": True,
                    "udpFloodingRate": 1000,
                    "winNukeStatus": True,
                    "winNukeRate": 1000
                }),
                description="啟用所有DoS防護功能"
            ),
            
            # 禁用所有DoS防護功能
            self.create_test_case(
                name="dos_protection_disable_all_protections",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_configuration_management",
                module="dos_protection",
                body=self.test_data.get('dos_protection_disable_all', {
                    "echoChargenStatus": False,
                    "smurfStatus": False,
                    "tcpFloodingStatus": False,
                    "tcpNullScanStatus": False,
                    "tcpSynFinScanStatus": False,
                    "tcpUdpPortZeroStatus": False,
                    "tcpXmasScanStatus": False,
                    "udpFloodingStatus": False,
                    "winNukeStatus": False
                }),
                description="禁用所有DoS防護功能"
            ),
            
            # 配置基本DoS防護
            self.create_test_case(
                name="dos_protection_configure_basic_protection",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_configuration_management",
                module="dos_protection",
                body=self.test_data.get('dos_protection_basic_config', {
                    "echoChargenStatus": True,
                    "echoChargenRate": 500,
                    "smurfStatus": True,
                    "tcpFloodingStatus": True,
                    "tcpFloodingRate": 800,
                    "udpFloodingStatus": True,
                    "udpFloodingRate": 600
                }),
                description="配置基本DoS防護"
            ),
            
            # 驗證DoS防護配置更新
            self.create_test_case(
                name="dos_protection_verify_configuration_update",
                method="GET",
                url="/api/v1/security/dos-protection",
                category="dos_protection_configuration_management",
                module="dos_protection",
                description="驗證DoS防護配置更新"
            )
        ]
    
    def get_dos_protection_attack_types_management_tests(self) -> List[APITestCase]:
        """DoS Protection Attack Types Management API 測試案例"""
        return [
            # 配置Echo/Chargen攻擊防護
            self.create_test_case(
                name="dos_protection_configure_echo_chargen",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_attack_types_management",
                module="dos_protection",
                body=self.test_data.get('dos_protection_echo_chargen', {
                    "echoChargenStatus": True,
                    "echoChargenRate": 1500
                }),
                description="配置Echo/Chargen攻擊防護"
            ),
            
            # 配置Smurf攻擊防護
            self.create_test_case(
                name="dos_protection_configure_smurf",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_attack_types_management",
                module="dos_protection",
                body=self.test_data.get('dos_protection_smurf', {
                    "smurfStatus": True
                }),
                description="配置Smurf攻擊防護"
            ),
            
            # 配置WinNuke攻擊防護
            self.create_test_case(
                name="dos_protection_configure_winnuke",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_attack_types_management",
                module="dos_protection",
                body=self.test_data.get('dos_protection_winnuke', {
                    "winNukeStatus": True,
                    "winNukeRate": 800
                }),
                description="配置WinNuke攻擊防護"
            ),
            
            # 禁用特定攻擊類型防護
            self.create_test_case(
                name="dos_protection_disable_specific_attacks",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_attack_types_management",
                module="dos_protection",
                body=self.test_data.get('dos_protection_disable_specific', {
                    "echoChargenStatus": False,
                    "winNukeStatus": False
                }),
                description="禁用特定攻擊類型防護"
            ),
            
            # 驗證攻擊類型配置
            self.create_test_case(
                name="dos_protection_verify_attack_types_configuration",
                method="GET",
                url="/api/v1/security/dos-protection",
                category="dos_protection_attack_types_management",
                module="dos_protection",
                description="驗證攻擊類型配置"
            )
        ]
    
    def get_dos_protection_rate_limiting_tests(self) -> List[APITestCase]:
        """DoS Protection Rate Limiting API 測試案例"""
        return [
            # 配置最小速率限制
            self.create_test_case(
                name="dos_protection_configure_minimum_rates",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_rate_limiting",
                module="dos_protection",
                body=self.test_data.get('dos_protection_minimum_rates', {
                    "echoChargenStatus": True,
                    "echoChargenRate": 64,
                    "tcpFloodingStatus": True,
                    "tcpFloodingRate": 64,
                    "udpFloodingStatus": True,
                    "udpFloodingRate": 64,
                    "winNukeStatus": True,
                    "winNukeRate": 64
                }),
                description="配置最小速率限制 (64 kbits/second)"
            ),
            
            # 配置最大速率限制
            self.create_test_case(
                name="dos_protection_configure_maximum_rates",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_rate_limiting",
                module="dos_protection",
                body=self.test_data.get('dos_protection_maximum_rates', {
                    "echoChargenStatus": True,
                    "echoChargenRate": 2000,
                    "tcpFloodingStatus": True,
                    "tcpFloodingRate": 2000,
                    "udpFloodingStatus": True,
                    "udpFloodingRate": 2000,
                    "winNukeStatus": True,
                    "winNukeRate": 2000
                }),
                description="配置最大速率限制 (2000 kbits/second)"
            ),
            
            # 配置中等速率限制
            self.create_test_case(
                name="dos_protection_configure_medium_rates",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_rate_limiting",
                module="dos_protection",
                body=self.test_data.get('dos_protection_medium_rates', {
                    "echoChargenStatus": True,
                    "echoChargenRate": 1000,
                    "tcpFloodingStatus": True,
                    "tcpFloodingRate": 1200,
                    "udpFloodingStatus": True,
                    "udpFloodingRate": 800,
                    "winNukeStatus": True,
                    "winNukeRate": 600
                }),
                description="配置中等速率限制"
            ),
            
            # 配置自定義速率限制
            self.create_test_case(
                name="dos_protection_configure_custom_rates",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_rate_limiting",
                module="dos_protection",
                body=self.test_data.get('dos_protection_custom_rates', {
                    "echoChargenStatus": True,
                    "echoChargenRate": 256,
                    "tcpFloodingStatus": True,
                    "tcpFloodingRate": 512,
                    "udpFloodingStatus": True,
                    "udpFloodingRate": 768,
                    "winNukeStatus": True,
                    "winNukeRate": 1024
                }),
                description="配置自定義速率限制"
            ),
            
            # 驗證速率限制配置
            self.create_test_case(
                name="dos_protection_verify_rate_limiting_configuration",
                method="GET",
                url="/api/v1/security/dos-protection",
                category="dos_protection_rate_limiting",
                module="dos_protection",
                description="驗證速率限制配置"
            )
        ]
    
    def get_dos_protection_scan_attacks_management_tests(self) -> List[APITestCase]:
        """DoS Protection Scan Attacks Management API 測試案例"""
        return [
            # 啟用所有掃描攻擊防護
            self.create_test_case(
                name="dos_protection_enable_all_scan_protections",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_scan_attacks_management",
                module="dos_protection",
                body=self.test_data.get('dos_protection_all_scan_protections', {
                    "tcpNullScanStatus": True,
                    "tcpSynFinScanStatus": True,
                    "tcpUdpPortZeroStatus": True,
                    "tcpXmasScanStatus": True
                }),
                description="啟用所有掃描攻擊防護"
            ),
            
            # 配置TCP Null掃描防護
            self.create_test_case(
                name="dos_protection_configure_tcp_null_scan",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_scan_attacks_management",
                module="dos_protection",
                body=self.test_data.get('dos_protection_tcp_null_scan', {
                    "tcpNullScanStatus": True
                }),
                description="配置TCP Null掃描防護"
            ),
            
            # 配置TCP SYN/FIN掃描防護
            self.create_test_case(
                name="dos_protection_configure_tcp_syn_fin_scan",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_scan_attacks_management",
                module="dos_protection",
                body=self.test_data.get('dos_protection_tcp_syn_fin_scan', {
                    "tcpSynFinScanStatus": True
                }),
                description="配置TCP SYN/FIN掃描防護"
            ),
            
            # 配置TCP/UDP Port Zero防護
            self.create_test_case(
                name="dos_protection_configure_tcp_udp_port_zero",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_scan_attacks_management",
                module="dos_protection",
                body=self.test_data.get('dos_protection_tcp_udp_port_zero', {
                    "tcpUdpPortZeroStatus": True
                }),
                description="配置TCP/UDP Port Zero防護"
            ),
            
            # 配置TCP Xmas掃描防護
            self.create_test_case(
                name="dos_protection_configure_tcp_xmas_scan",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_scan_attacks_management",
                module="dos_protection",
                body=self.test_data.get('dos_protection_tcp_xmas_scan', {
                    "tcpXmasScanStatus": True
                }),
                description="配置TCP Xmas掃描防護"
            ),
            
            # 禁用所有掃描攻擊防護
            self.create_test_case(
                name="dos_protection_disable_all_scan_protections",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_scan_attacks_management",
                module="dos_protection",
                body=self.test_data.get('dos_protection_disable_all_scan', {
                    "tcpNullScanStatus": False,
                    "tcpSynFinScanStatus": False,
                    "tcpUdpPortZeroStatus": False,
                    "tcpXmasScanStatus": False
                }),
                description="禁用所有掃描攻擊防護"
            ),
            
            # 驗證掃描攻擊防護配置
            self.create_test_case(
                name="dos_protection_verify_scan_attacks_configuration",
                method="GET",
                url="/api/v1/security/dos-protection",
                category="dos_protection_scan_attacks_management",
                module="dos_protection",
                description="驗證掃描攻擊防護配置"
            )
        ]
    
    def get_dos_protection_flood_attacks_management_tests(self) -> List[APITestCase]:
        """DoS Protection Flood Attacks Management API 測試案例"""
        return [
            # 配置TCP洪水攻擊防護
            self.create_test_case(
                name="dos_protection_configure_tcp_flooding",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_flood_attacks_management",
                module="dos_protection",
                body=self.test_data.get('dos_protection_tcp_flooding', {
                    "tcpFloodingStatus": True,
                    "tcpFloodingRate": 1500
                }),
                description="配置TCP洪水攻擊防護"
            ),
            
            # 配置UDP洪水攻擊防護
            self.create_test_case(
                name="dos_protection_configure_udp_flooding",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_flood_attacks_management",
                module="dos_protection",
                body=self.test_data.get('dos_protection_udp_flooding', {
                    "udpFloodingStatus": True,
                    "udpFloodingRate": 1200
                }),
                description="配置UDP洪水攻擊防護"
            ),
            
            # 配置高強度洪水攻擊防護
            self.create_test_case(
                name="dos_protection_configure_high_intensity_flooding",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_flood_attacks_management",
                module="dos_protection",
                body=self.test_data.get('dos_protection_high_intensity_flooding', {
                    "tcpFloodingStatus": True,
                    "tcpFloodingRate": 2000,
                    "udpFloodingStatus": True,
                    "udpFloodingRate": 2000
                }),
                description="配置高強度洪水攻擊防護"
            ),
            
            # 配置低強度洪水攻擊防護
            self.create_test_case(
                name="dos_protection_configure_low_intensity_flooding",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_flood_attacks_management",
                module="dos_protection",
                body=self.test_data.get('dos_protection_low_intensity_flooding', {
                    "tcpFloodingStatus": True,
                    "tcpFloodingRate": 64,
                    "udpFloodingStatus": True,
                    "udpFloodingRate": 64
                }),
                description="配置低強度洪水攻擊防護"
            ),
            
            # 禁用洪水攻擊防護
            self.create_test_case(
                name="dos_protection_disable_flooding_protections",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_flood_attacks_management",
                module="dos_protection",
                body=self.test_data.get('dos_protection_disable_flooding', {
                    "tcpFloodingStatus": False,
                    "udpFloodingStatus": False
                }),
                description="禁用洪水攻擊防護"
            ),
            
            # 驗證洪水攻擊防護配置
            self.create_test_case(
                name="dos_protection_verify_flood_attacks_configuration",
                method="GET",
                url="/api/v1/security/dos-protection",
                category="dos_protection_flood_attacks_management",
                module="dos_protection",
                description="驗證洪水攻擊防護配置"
            )
        ]
    
    def get_dos_protection_advanced_operations_tests(self) -> List[APITestCase]:
        """DoS Protection Advanced Operations API 測試案例"""
        return [
            # 配置企業級DoS防護策略
            self.create_test_case(
                name="dos_protection_configure_enterprise_policy",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_advanced_operations",
                module="dos_protection",
                body=self.test_data.get('dos_protection_enterprise_policy', {
                    "echoChargenStatus": True,
                    "echoChargenRate": 500,
                    "smurfStatus": True,
                    "tcpFloodingStatus": True,
                    "tcpFloodingRate": 1000,
                    "tcpNullScanStatus": True,
                    "tcpSynFinScanStatus": True,
                    "tcpUdpPortZeroStatus": True,
                    "tcpXmasScanStatus": True,
                    "udpFloodingStatus": True,
                    "udpFloodingRate": 800,
                    "winNukeStatus": True,
                    "winNukeRate": 600
                }),
                description="配置企業級DoS防護策略"
            ),
            
            # 配置高安全性DoS防護策略
            self.create_test_case(
                name="dos_protection_configure_high_security_policy",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_advanced_operations",
                module="dos_protection",
                body=self.test_data.get('dos_protection_high_security_policy', {
                    "echoChargenStatus": True,
                    "echoChargenRate": 128,
                    "smurfStatus": True,
                    "tcpFloodingStatus": True,
                    "tcpFloodingRate": 256,
                    "tcpNullScanStatus": True,
                    "tcpSynFinScanStatus": True,
                    "tcpUdpPortZeroStatus": True,
                    "tcpXmasScanStatus": True,
                    "udpFloodingStatus": True,
                    "udpFloodingRate": 192,
                    "winNukeStatus": True,
                    "winNukeRate": 128
                }),
                description="配置高安全性DoS防護策略"
            ),
            
            # 配置平衡性DoS防護策略
            self.create_test_case(
                name="dos_protection_configure_balanced_policy",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_advanced_operations",
                module="dos_protection",
                body=self.test_data.get('dos_protection_balanced_policy', {
                    "echoChargenStatus": True,
                    "echoChargenRate": 1000,
                    "smurfStatus": True,
                    "tcpFloodingStatus": True,
                    "tcpFloodingRate": 1000,
                    "tcpNullScanStatus": True,
                    "tcpSynFinScanStatus": True,
                    "tcpUdpPortZeroStatus": False,
                    "tcpXmasScanStatus": True,
                    "udpFloodingStatus": True,
                    "udpFloodingRate": 1000,
                    "winNukeStatus": False,
                    "winNukeRate": 1000
                }),
                description="配置平衡性DoS防護策略"
            ),
            
            # 動態調整DoS防護參數
            self.create_test_case(
                name="dos_protection_dynamic_adjust_parameters",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_advanced_operations",
                module="dos_protection",
                body=self.test_data.get('dos_protection_dynamic_parameters', {
                    "echoChargenRate": 750,
                    "tcpFloodingRate": 1250,
                    "udpFloodingRate": 900,
                    "winNukeRate": 700
                }),
                description="動態調整DoS防護參數"
            ),
            
            # 測試DoS防護策略切換
            self.create_test_case(
                name="dos_protection_test_policy_switching",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_advanced_operations",
                module="dos_protection",
                body=self.test_data.get('dos_protection_policy_switching', {
                    "echoChargenStatus": False,
                    "smurfStatus": True,
                    "tcpFloodingStatus": False,
                    "tcpNullScanStatus": False,
                    "tcpSynFinScanStatus": True,
                    "tcpUdpPortZeroStatus": True,
                    "tcpXmasScanStatus": False,
                    "udpFloodingStatus": False,
                    "winNukeStatus": True,
                    "winNukeRate": 1500
                }),
                description="測試DoS防護策略切換"
            ),
            
            # 驗證高級操作結果
            self.create_test_case(
                name="dos_protection_verify_advanced_operations_results",
                method="GET",
                url="/api/v1/security/dos-protection",
                category="dos_protection_advanced_operations",
                module="dos_protection",
                description="驗證高級操作結果"
            )
        ]
    
    def get_dos_protection_error_handling_tests(self) -> List[APITestCase]:
        """DoS Protection Error Handling API 測試案例"""
        return [
            # 測試無效速率值 - 低於最小值
            self.create_test_case(
                name="dos_protection_test_rate_below_minimum",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_error_handling",
                module="dos_protection",
                body=self.test_data.get('dos_protection_rate_below_minimum', {
                    "echoChargenStatus": True,
                    "echoChargenRate": 32  # 低於64的最小值
                }),
                expected_status=400,
                description="測試無效速率值 - 低於最小值64"
            ),
            
            # 測試無效速率值 - 高於最大值
            self.create_test_case(
                name="dos_protection_test_rate_above_maximum",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_error_handling",
                module="dos_protection",
                body=self.test_data.get('dos_protection_rate_above_maximum', {
                    "tcpFloodingStatus": True,
                    "tcpFloodingRate": 3000  # 高於2000的最大值
                }),
                expected_status=400,
                description="測試無效速率值 - 高於最大值2000"
            ),
            
            # 測試無效布爾值
            self.create_test_case(
                name="dos_protection_test_invalid_boolean_value",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_error_handling",
                module="dos_protection",
                body=self.test_data.get('dos_protection_invalid_boolean', {
                    "smurfStatus": "invalid_boolean"  # 無效的布爾值
                }),
                expected_status=400,
                description="測試無效布爾值"
            ),
            
            # 測試無效JSON格式
            self.create_test_case(
                name="dos_protection_test_invalid_json_format",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_error_handling",
                module="dos_protection",
                body="invalid json format",
                expected_status=400,
                description="測試無效JSON格式"
            ),
            
            # 測試空請求體
            self.create_test_case(
                name="dos_protection_test_empty_request_body",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_error_handling",
                module="dos_protection",
                body={},
                expected_status=400,
                description="測試空請求體"
            ),
            
            # 測試無效參數名稱
            self.create_test_case(
                name="dos_protection_test_invalid_parameter_names",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_error_handling",
                module="dos_protection",
                body=self.test_data.get('dos_protection_invalid_parameter_names', {
                    "invalidParameter": True,
                    "anotherInvalidParam": 1000
                }),
                expected_status=400,
                description="測試無效參數名稱"
            ),
            
            # 測試負數速率值
            self.create_test_case(
                name="dos_protection_test_negative_rate_value",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_error_handling",
                module="dos_protection",
                body=self.test_data.get('dos_protection_negative_rate', {
                    "udpFloodingStatus": True,
                    "udpFloodingRate": -100  # 負數速率值
                }),
                expected_status=400,
                description="測試負數速率值"
            ),
            
            # 測試零速率值
            self.create_test_case(
                name="dos_protection_test_zero_rate_value",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_error_handling",
                module="dos_protection",
                body=self.test_data.get('dos_protection_zero_rate', {
                    "winNukeStatus": True,
                    "winNukeRate": 0  # 零速率值
                }),
                expected_status=400,
                description="測試零速率值"
            ),
            
            # 測試字符串速率值
            self.create_test_case(
                name="dos_protection_test_string_rate_value",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_error_handling",
                module="dos_protection",
                body=self.test_data.get('dos_protection_string_rate', {
                    "echoChargenStatus": True,
                    "echoChargenRate": "invalid_rate"  # 字符串速率值
                }),
                expected_status=400,
                description="測試字符串速率值"
            ),
            
            # 恢復正常DoS防護配置
            self.create_test_case(
                name="dos_protection_restore_normal_configuration",
                method="PUT",
                url="/api/v1/security/dos-protection",
                category="dos_protection_error_handling",
                module="dos_protection",
                body=self.test_data.get('dos_protection_restore_normal_config', {
                    "echoChargenStatus": False,
                    "echoChargenRate": 1000,
                    "smurfStatus": True,
                    "tcpFloodingStatus": False,
                    "tcpFloodingRate": 1000,
                    "tcpNullScanStatus": True,
                    "tcpSynFinScanStatus": True,
                    "tcpUdpPortZeroStatus": True,
                    "tcpXmasScanStatus": True,
                    "udpFloodingStatus": False,
                    "udpFloodingRate": 1000,
                    "winNukeStatus": False,
                    "winNukeRate": 1000
                }),
                description="恢復正常DoS防護配置"
            ),
            
            # 最終DoS防護狀態檢查
            self.create_test_case(
                name="dos_protection_final_status_check",
                method="GET",
                url="/api/v1/security/dos-protection",
                category="dos_protection_error_handling",
                module="dos_protection",
                description="最終DoS防護狀態檢查"
            )
        ]