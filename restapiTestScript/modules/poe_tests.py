#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POE (Power over Ethernet) 模組測試案例
包含POE接口配置和主電源信息獲取相關API測試
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class POETests(BaseTests):
    """POE 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取POE模組支援的類別"""
        return [
            "poe_interfaces",
            "poe_mainpower"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有POE測試案例"""
        all_tests = []
        all_tests.extend(self.get_poe_interfaces_tests())
        all_tests.extend(self.get_poe_mainpower_tests())
        return all_tests
    
    def get_poe_interfaces_tests(self) -> List[APITestCase]:
        """POE Interfaces API 測試案例"""
        return [
            # 獲取所有接口的POE配置
            self.create_test_case(
                name="poe_get_all_interfaces_config",
                method="GET",
                url="/api/v1/poe/interfaces",
                category="poe_interfaces",
                module="poe",
                description="獲取所有接口的POE配置"
            ),
            
            # 獲取特定接口的POE配置 - eth1/1
            self.create_test_case(
                name="poe_get_interface_eth1_1_config",
                method="GET",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": "eth1%2f1"},
                description="獲取接口 eth1/1 的POE配置"
            ),
            
            # 獲取特定接口的POE配置 - eth1/2
            self.create_test_case(
                name="poe_get_interface_eth1_2_config",
                method="GET",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": "eth1%2f2"},
                description="獲取接口 eth1/2 的POE配置"
            ),
            
            # 獲取特定接口的POE配置 - eth1/5
            self.create_test_case(
                name="poe_get_interface_eth1_5_config",
                method="GET",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": "eth1%2f5"},
                description="獲取接口 eth1/5 的POE配置"
            ),
            
            # 獲取參數化接口的POE配置
            self.create_test_case(
                name="poe_get_parameterized_interface_config",
                method="GET",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                description=f"獲取接口 {self.params.get('interface_id', 'eth1/1')} 的POE配置"
            ),
            
            # 啟用POE - 基本配置
            self.create_test_case(
                name="poe_enable_interface_basic",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                body=self.test_data.get('poe_enable_basic', {
                    "admin": True
                }),
                description=f"啟用接口 {self.params.get('interface_id', 'eth1/1')} 的POE - 基本配置"
            ),
            
            # 配置POE - 設置最大功率
            self.create_test_case(
                name="poe_configure_max_power",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                body=self.test_data.get('poe_max_power', {
                    "admin": True,
                    "maxPower": 30000
                }),
                description=f"配置接口 {self.params.get('interface_id', 'eth1/1')} POE最大功率為30W"
            ),
            
            # 配置POE - 設置中等功率
            self.create_test_case(
                name="poe_configure_medium_power",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": self.params.get('interface_id_2', 'eth1%2f2')},
                body=self.test_data.get('poe_medium_power', {
                    "admin": True,
                    "maxPower": 15000
                }),
                description=f"配置接口 {self.params.get('interface_id_2', 'eth1/2')} POE功率為15W"
            ),
            
            # 配置POE - 設置最小功率
            self.create_test_case(
                name="poe_configure_min_power",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": "eth1%2f3"},
                body=self.test_data.get('poe_min_power', {
                    "admin": True,
                    "maxPower": 3000
                }),
                description="配置接口 eth1/3 POE最小功率為3W"
            ),
            
            # 配置POE優先級 - 關鍵優先級
            self.create_test_case(
                name="poe_configure_critical_priority",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                body=self.test_data.get('poe_critical_priority', {
                    "admin": True,
                    "maxPower": 30000,
                    "priority": "critical"
                }),
                description=f"配置接口 {self.params.get('interface_id', 'eth1/1')} POE為關鍵優先級"
            ),
            
            # 配置POE優先級 - 高優先級
            self.create_test_case(
                name="poe_configure_high_priority",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": self.params.get('interface_id_2', 'eth1%2f2')},
                body=self.test_data.get('poe_high_priority', {
                    "admin": True,
                    "maxPower": 25000,
                    "priority": "high"
                }),
                description=f"配置接口 {self.params.get('interface_id_2', 'eth1/2')} POE為高優先級"
            ),
            
            # 配置POE優先級 - 低優先級
            self.create_test_case(
                name="poe_configure_low_priority",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": "eth1%2f3"},
                body=self.test_data.get('poe_low_priority', {
                    "admin": True,
                    "maxPower": 15000,
                    "priority": "low"
                }),
                description="配置接口 eth1/3 POE為低優先級"
            ),
            
            # 配置POE時間範圍 - 綁定時間範圍
            self.create_test_case(
                name="poe_configure_time_range",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                body=self.test_data.get('poe_with_time_range', {
                    "admin": True,
                    "maxPower": 30000,
                    "priority": "high",
                    "timeRange": "business_hours"
                }),
                description=f"配置接口 {self.params.get('interface_id', 'eth1/1')} POE綁定時間範圍"
            ),
            
            # 配置POE時間範圍 - 不同時間範圍
            self.create_test_case(
                name="poe_configure_different_time_range",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": self.params.get('interface_id_2', 'eth1%2f2')},
                body=self.test_data.get('poe_different_time_range', {
                    "admin": True,
                    "maxPower": 25000,
                    "priority": "high",
                    "timeRange": "night_shift"
                }),
                description=f"配置接口 {self.params.get('interface_id_2', 'eth1/2')} POE不同時間範圍"
            ),
            
            # 移除POE時間範圍綁定
            self.create_test_case(
                name="poe_remove_time_range_binding",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                body=self.test_data.get('poe_remove_time_range', {
                    "admin": True,
                    "maxPower": 30000,
                    "priority": "high",
                    "timeRange": ""
                }),
                description=f"移除接口 {self.params.get('interface_id', 'eth1/1')} POE時間範圍綁定"
            ),
            
            # 完整POE配置 - 所有參數
            self.create_test_case(
                name="poe_configure_complete_settings",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": "eth1%2f5"},
                body=self.test_data.get('poe_complete_config', {
                    "admin": True,
                    "maxPower": 25000,
                    "priority": "high",
                    "timeRange": "aaa"
                }),
                description="配置接口 eth1/5 完整POE設置"
            ),
            
            # 禁用POE
            self.create_test_case(
                name="poe_disable_interface",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": "eth1%2f4"},
                body=self.test_data.get('poe_disable', {
                    "admin": False
                }),
                description="禁用接口 eth1/4 的POE"
            ),
            
            # 重新啟用POE
            self.create_test_case(
                name="poe_re_enable_interface",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": "eth1%2f4"},
                body=self.test_data.get('poe_re_enable', {
                    "admin": True,
                    "maxPower": 20000,
                    "priority": "low"
                }),
                description="重新啟用接口 eth1/4 的POE"
            ),
            
            # 測試邊界值 - 最大功率邊界
            self.create_test_case(
                name="poe_test_max_power_boundary",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": "eth1%2f6"},
                body=self.test_data.get('poe_max_power_boundary', {
                    "admin": True,
                    "maxPower": 30000
                }),
                description="測試接口 eth1/6 POE最大功率邊界值"
            ),
            
            # 測試邊界值 - 最小功率邊界
            self.create_test_case(
                name="poe_test_min_power_boundary",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": "eth1%2f7"},
                body=self.test_data.get('poe_min_power_boundary', {
                    "admin": True,
                    "maxPower": 3000
                }),
                description="測試接口 eth1/7 POE最小功率邊界值"
            ),
            
            # 測試無效參數 - 功率超出上限
            self.create_test_case(
                name="poe_test_power_over_limit",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": "eth1%2f8"},
                body=self.test_data.get('poe_power_over_limit', {
                    "admin": True,
                    "maxPower": 35000  # 超出30000上限
                }),
                expected_status=400,
                description="測試接口 eth1/8 POE功率超出上限"
            ),
            
            # 測試無效參數 - 功率低於下限
            self.create_test_case(
                name="poe_test_power_under_limit",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": "eth1%2f9"},
                body=self.test_data.get('poe_power_under_limit', {
                    "admin": True,
                    "maxPower": 2000  # 低於3000下限
                }),
                expected_status=400,
                description="測試接口 eth1/9 POE功率低於下限"
            ),
            
            # 測試無效參數 - 無效優先級
            self.create_test_case(
                name="poe_test_invalid_priority",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": "eth1%2f10"},
                body=self.test_data.get('poe_invalid_priority', {
                    "admin": True,
                    "maxPower": 15000,
                    "priority": "invalid"  # 無效優先級
                }),
                expected_status=400,
                description="測試接口 eth1/10 無效POE優先級"
            ),
            
            # 測試無效參數 - 時間範圍名稱過長
            self.create_test_case(
                name="poe_test_time_range_too_long",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": "eth1%2f11"},
                body=self.test_data.get('poe_time_range_too_long', {
                    "admin": True,
                    "maxPower": 15000,
                    "priority": "low",
                    "timeRange": "this_time_range_name_is_way_too_long_and_exceeds_16_characters"
                }),
                expected_status=400,
                description="測試接口 eth1/11 時間範圍名稱過長"
            ),
            
            # 測試缺少必要參數
            self.create_test_case(
                name="poe_test_missing_required_param",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": "eth1%2f12"},
                body=self.test_data.get('poe_missing_param', {
                    "maxPower": 15000  # 缺少admin參數
                }),
                expected_status=400,
                description="測試接口 eth1/12 缺少必要參數"
            ),
            
            # 測試無效JSON格式
            self.create_test_case(
                name="poe_test_invalid_json",
                method="PUT",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": "eth1%2f13"},
                body='{"admin": true, "maxPower":}',  # 無效JSON
                expected_status=400,
                description="測試接口 eth1/13 無效JSON格式"
            ),
            
            # 獲取不存在接口的POE配置
            self.create_test_case(
                name="poe_get_nonexistent_interface",
                method="GET",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": "eth1%2f99"},
                expected_status=404,
                description="獲取不存在接口 eth1/99 的POE配置"
            ),
            
            # 批量檢查多個接口POE狀態
            self.create_test_case(
                name="poe_batch_check_interfaces_1",
                method="GET",
                url="/api/v1/poe/interfaces",
                category="poe_interfaces",
                module="poe",
                description="批量檢查所有接口POE狀態 - 第1次"
            ),
            
            self.create_test_case(
                name="poe_batch_check_interfaces_2",
                method="GET",
                url="/api/v1/poe/interfaces",
                category="poe_interfaces",
                module="poe",
                description="批量檢查所有接口POE狀態 - 第2次"
            ),
            
            # 驗證POE配置更新效果
            self.create_test_case(
                name="poe_verify_configuration_update",
                method="GET",
                url="/api/v1/poe/interfaces/{ifId}",
                category="poe_interfaces",
                module="poe",
                params={"ifId": "eth1%2f5"},
                description="驗證接口 eth1/5 POE配置更新效果"
            )
        ]
    
    def get_poe_mainpower_tests(self) -> List[APITestCase]:
        """POE Main Power API 測試案例"""
        return [
            # 獲取POE主電源信息
            self.create_test_case(
                name="poe_get_mainpower_info",
                method="GET",
                url="/api/v1/poe",
                category="poe_mainpower",
                module="poe",
                description="獲取POE主電源信息"
            ),
            
            # 監控POE主電源狀態 - 第1次檢查
            self.create_test_case(
                name="poe_monitor_mainpower_status_1",
                method="GET",
                url="/api/v1/poe",
                category="poe_mainpower",
                module="poe",
                description="監控POE主電源狀態 - 第1次檢查"
            ),
            
            # 監控POE主電源狀態 - 第2次檢查
            self.create_test_case(
                name="poe_monitor_mainpower_status_2",
                method="GET",
                url="/api/v1/poe",
                category="poe_mainpower",
                module="poe",
                description="監控POE主電源狀態 - 第2次檢查"
            ),
            
            # 監控POE主電源狀態 - 第3次檢查
            self.create_test_case(
                name="poe_monitor_mainpower_status_3",
                method="GET",
                url="/api/v1/poe",
                category="poe_mainpower",
                module="poe",
                description="監控POE主電源狀態 - 第3次檢查"
            ),
            
            # 檢查POE功率預算
            self.create_test_case(
                name="poe_check_power_budget",
                method="GET",
                url="/api/v1/poe",
                category="poe_mainpower",
                module="poe",
                description="檢查POE功率預算和分配"
            ),
            
            # 驗證POE軟件版本信息
            self.create_test_case(
                name="poe_verify_software_version",
                method="GET",
                url="/api/v1/poe",
                category="poe_mainpower",
                module="poe",
                description="驗證POE控制器軟件版本信息"
            ),
            
            # 檢查POE系統運行狀態
            self.create_test_case(
                name="poe_check_system_operation_status",
                method="GET",
                url="/api/v1/poe",
                category="poe_mainpower",
                module="poe",
                description="檢查POE系統運行狀態"
            ),
            
            # 監控POE功率消耗變化
            self.create_test_case(
                name="poe_monitor_power_consumption_1",
                method="GET",
                url="/api/v1/poe",
                category="poe_mainpower",
                module="poe",
                description="監控POE功率消耗變化 - 第1次"
            ),
            
            self.create_test_case(
                name="poe_monitor_power_consumption_2",
                method="GET",
                url="/api/v1/poe",
                category="poe_mainpower",
                module="poe",
                description="監控POE功率消耗變化 - 第2次"
            ),
            
            self.create_test_case(
                name="poe_monitor_power_consumption_3",
                method="GET",
                url="/api/v1/poe",
                category="poe_mainpower",
                module="poe",
                description="監控POE功率消耗變化 - 第3次"
            )
        ]