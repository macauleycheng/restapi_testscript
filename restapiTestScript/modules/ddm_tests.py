#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DDM 模組測試案例
包含光模塊閾值配置、監控啟用/禁用、自動閾值配置等相關API測試
支援電流、接收功率、溫度、發送功率、電壓等參數的閾值管理
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class DDMTests(BaseTests):
    """DDM 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取DDM模組支援的類別"""
        return [
            "ddm_current_threshold",
            "ddm_rx_power_threshold", 
            "ddm_temperature_threshold",
            "ddm_tx_power_threshold",
            "ddm_voltage_threshold",
            "ddm_threshold_management",
            "ddm_monitor_control",
            "ddm_auto_threshold"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有DDM測試案例"""
        all_tests = []
        all_tests.extend(self.get_ddm_current_threshold_tests())
        all_tests.extend(self.get_ddm_rx_power_threshold_tests())
        all_tests.extend(self.get_ddm_temperature_threshold_tests())
        all_tests.extend(self.get_ddm_tx_power_threshold_tests())
        all_tests.extend(self.get_ddm_voltage_threshold_tests())
        all_tests.extend(self.get_ddm_threshold_management_tests())
        all_tests.extend(self.get_ddm_monitor_control_tests())
        all_tests.extend(self.get_ddm_auto_threshold_tests())
        return all_tests
    
    def get_ddm_current_threshold_tests(self) -> List[APITestCase]:
        """DDM Current Threshold API 測試案例"""
        return [
            # 更新電流閾值 - 基本配置
            self.create_test_case(
                name="ddm_update_current_threshold_basic",
                method="PUT",
                url="/api/v1/transceiver-threshold/current",
                category="ddm_current_threshold",
                module="ddm",
                body=self.test_data.get('ddm_current_threshold_basic', {
                    "high-alarm": 2500,
                    "high-warning": 2000,
                    "low-alarm": 100,
                    "low-warning": 200
                }),
                description="更新電流閾值 - 基本配置"
            ),
            
            # 更新電流閾值 - 最小值
            self.create_test_case(
                name="ddm_update_current_threshold_min",
                method="PUT",
                url="/api/v1/transceiver-threshold/current",
                category="ddm_current_threshold",
                module="ddm",
                body=self.test_data.get('ddm_current_threshold_min', {
                    "high-alarm": 100,
                    "high-warning": 100,
                    "low-alarm": 100,
                    "low-warning": 100
                }),
                description="更新電流閾值 - 最小值 (1.00mA)"
            ),
            
            # 更新電流閾值 - 最大值
            self.create_test_case(
                name="ddm_update_current_threshold_max",
                method="PUT",
                url="/api/v1/transceiver-threshold/current",
                category="ddm_current_threshold",
                module="ddm",
                body=self.test_data.get('ddm_current_threshold_max', {
                    "high-alarm": 25500,
                    "high-warning": 25000,
                    "low-alarm": 500,
                    "low-warning": 1000
                }),
                description="更新電流閾值 - 最大值 (255.00mA)"
            ),
            
            # 更新電流閾值 - 僅高告警
            self.create_test_case(
                name="ddm_update_current_threshold_high_alarm_only",
                method="PUT",
                url="/api/v1/transceiver-threshold/current",
                category="ddm_current_threshold",
                module="ddm",
                body=self.test_data.get('ddm_current_threshold_high_alarm_only', {
                    "high-alarm": 3000
                }),
                description="更新電流閾值 - 僅高告警"
            ),
            
            # 更新電流閾值 - 僅低告警
            self.create_test_case(
                name="ddm_update_current_threshold_low_alarm_only",
                method="PUT",
                url="/api/v1/transceiver-threshold/current",
                category="ddm_current_threshold",
                module="ddm",
                body=self.test_data.get('ddm_current_threshold_low_alarm_only', {
                    "low-alarm": 150
                }),
                description="更新電流閾值 - 僅低告警"
            ),
            
            # 更新電流閾值 - 警告閾值
            self.create_test_case(
                name="ddm_update_current_threshold_warnings",
                method="PUT",
                url="/api/v1/transceiver-threshold/current",
                category="ddm_current_threshold",
                module="ddm",
                body=self.test_data.get('ddm_current_threshold_warnings', {
                    "high-warning": 2200,
                    "low-warning": 180
                }),
                description="更新電流閾值 - 警告閾值"
            ),
            
            # 更新電流閾值 - 自定義配置
            self.create_test_case(
                name="ddm_update_current_threshold_custom",
                method="PUT",
                url="/api/v1/transceiver-threshold/current",
                category="ddm_current_threshold",
                module="ddm",
                body=self.test_data.get('ddm_current_threshold_custom', {
                    "high-alarm": 5000,
                    "high-warning": 4500,
                    "low-alarm": 300,
                    "low-warning": 500
                }),
                description="更新電流閾值 - 自定義配置"
            ),
            
            # 測試無效電流閾值 - 超出範圍
            self.create_test_case(
                name="ddm_test_invalid_current_threshold_range",
                method="PUT",
                url="/api/v1/transceiver-threshold/current",
                category="ddm_current_threshold",
                module="ddm",
                body=self.test_data.get('ddm_current_threshold_invalid_range', {
                    "high-alarm": 30000  # 超出範圍 100-25500
                }),
                expected_status=400,
                description="測試無效電流閾值 - 超出範圍"
            ),
            
            # 測試無效電流閾值 - 低於最小值
            self.create_test_case(
                name="ddm_test_invalid_current_threshold_below_min",
                method="PUT",
                url="/api/v1/transceiver-threshold/current",
                category="ddm_current_threshold",
                module="ddm",
                body=self.test_data.get('ddm_current_threshold_below_min', {
                    "low-alarm": 50  # 低於最小值 100
                }),
                expected_status=400,
                description="測試無效電流閾值 - 低於最小值"
            )
        ]
    
    def get_ddm_rx_power_threshold_tests(self) -> List[APITestCase]:
        """DDM RX Power Threshold API 測試案例"""
        return [
            # 更新接收功率閾值 - 基本配置
            self.create_test_case(
                name="ddm_update_rx_power_threshold_basic",
                method="PUT",
                url="/api/v1/transceiver-threshold/rx-power",
                category="ddm_rx_power_threshold",
                module="ddm",
                body=self.test_data.get('ddm_rx_power_threshold_basic', {
                    "high-alarm": 500,
                    "high-warning": 300,
                    "low-alarm": -2000,
                    "low-warning": -1500
                }),
                description="更新接收功率閾值 - 基本配置"
            ),
            
            # 更新接收功率閾值 - 最大值
            self.create_test_case(
                name="ddm_update_rx_power_threshold_max",
                method="PUT",
                url="/api/v1/transceiver-threshold/rx-power",
                category="ddm_rx_power_threshold",
                module="ddm",
                body=self.test_data.get('ddm_rx_power_threshold_max', {
                    "high-alarm": 9999,
                    "high-warning": 9000,
                    "low-alarm": -9000,
                    "low-warning": -8000
                }),
                description="更新接收功率閾值 - 最大值 (99.99dBm)"
            ),
            
            # 更新接收功率閾值 - 最小值
            self.create_test_case(
                name="ddm_update_rx_power_threshold_min",
                method="PUT",
                url="/api/v1/transceiver-threshold/rx-power",
                category="ddm_rx_power_threshold",
                module="ddm",
                body=self.test_data.get('ddm_rx_power_threshold_min', {
                    "high-alarm": -9999,
                    "high-warning": -9999,
                    "low-alarm": -9999,
                    "low-warning": -9999
                }),
                description="更新接收功率閾值 - 最小值 (-99.99dBm)"
            ),
            
            # 更新接收功率閾值 - 正值配置
            self.create_test_case(
                name="ddm_update_rx_power_threshold_positive",
                method="PUT",
                url="/api/v1/transceiver-threshold/rx-power",
                category="ddm_rx_power_threshold",
                module="ddm",
                body=self.test_data.get('ddm_rx_power_threshold_positive', {
                    "high-alarm": 1000,
                    "high-warning": 800,
                    "low-alarm": 200,
                    "low-warning": 400
                }),
                description="更新接收功率閾值 - 正值配置"
            ),
            
            # 更新接收功率閾值 - 負值配置
            self.create_test_case(
                name="ddm_update_rx_power_threshold_negative",
                method="PUT",
                url="/api/v1/transceiver-threshold/rx-power",
                category="ddm_rx_power_threshold",
                module="ddm",
                body=self.test_data.get('ddm_rx_power_threshold_negative', {
                    "high-alarm": -500,
                    "high-warning": -800,
                    "low-alarm": -3000,
                    "low-warning": -2500
                }),
                description="更新接收功率閾值 - 負值配置"
            ),
            
            # 更新接收功率閾值 - 零值配置
            self.create_test_case(
                name="ddm_update_rx_power_threshold_zero",
                method="PUT",
                url="/api/v1/transceiver-threshold/rx-power",
                category="ddm_rx_power_threshold",
                module="ddm",
                body=self.test_data.get('ddm_rx_power_threshold_zero', {
                    "high-alarm": 0,
                    "high-warning": -100,
                    "low-alarm": -1000,
                    "low-warning": -500
                }),
                description="更新接收功率閾值 - 零值配置"
            ),
            
            # 測試無效接收功率閾值 - 超出範圍
            self.create_test_case(
                name="ddm_test_invalid_rx_power_threshold_range",
                method="PUT",
                url="/api/v1/transceiver-threshold/rx-power",
                category="ddm_rx_power_threshold",
                module="ddm",
                body=self.test_data.get('ddm_rx_power_threshold_invalid_range', {
                    "high-alarm": 15000  # 超出範圍 -9999 to 9999
                }),
                expected_status=400,
                description="測試無效接收功率閾值 - 超出範圍"
            )
        ]
    
    def get_ddm_temperature_threshold_tests(self) -> List[APITestCase]:
        """DDM Temperature Threshold API 測試案例"""
        return [
            # 更新溫度閾值 - 基本配置
            self.create_test_case(
                name="ddm_update_temperature_threshold_basic",
                method="PUT",
                url="/api/v1/transceiver-threshold/temperature",
                category="ddm_temperature_threshold",
                module="ddm",
                body=self.test_data.get('ddm_temperature_threshold_basic', {
                    "high-alarm": 8500,
                    "high-warning": 8000,
                    "low-alarm": -1000,
                    "low-warning": -500
                }),
                description="更新溫度閾值 - 基本配置"
            ),
            
            # 更新溫度閾值 - 最高溫度
            self.create_test_case(
                name="ddm_update_temperature_threshold_max",
                method="PUT",
                url="/api/v1/transceiver-threshold/temperature",
                category="ddm_temperature_threshold",
                module="ddm",
                body=self.test_data.get('ddm_temperature_threshold_max', {
                    "high-alarm": 20000,
                    "high-warning": 19000,
                    "low-alarm": 18000,
                    "low-warning": 18500
                }),
                description="更新溫度閾值 - 最高溫度 (200°C)"
            ),
            
            # 更新溫度閾值 - 最低溫度
            self.create_test_case(
                name="ddm_update_temperature_threshold_min",
                method="PUT",
                url="/api/v1/transceiver-threshold/temperature",
                category="ddm_temperature_threshold",
                module="ddm",
                body=self.test_data.get('ddm_temperature_threshold_min', {
                    "high-alarm": -19000,
                    "high-warning": -19500,
                    "low-alarm": -20000,
                    "low-warning": -19800
                }),
                description="更新溫度閾值 - 最低溫度 (-200°C)"
            ),
            
            # 更新溫度閾值 - 室溫範圍
            self.create_test_case(
                name="ddm_update_temperature_threshold_room_temp",
                method="PUT",
                url="/api/v1/transceiver-threshold/temperature",
                category="ddm_temperature_threshold",
                module="ddm",
                body=self.test_data.get('ddm_temperature_threshold_room_temp', {
                    "high-alarm": 7000,
                    "high-warning": 6500,
                    "low-alarm": 0,
                    "low-warning": 500
                }),
                description="更新溫度閾值 - 室溫範圍 (0-70°C)"
            ),
            
            # 更新溫度閾值 - 工業級範圍
            self.create_test_case(
                name="ddm_update_temperature_threshold_industrial",
                method="PUT",
                url="/api/v1/transceiver-threshold/temperature",
                category="ddm_temperature_threshold",
                module="ddm",
                body=self.test_data.get('ddm_temperature_threshold_industrial', {
                    "high-alarm": 10000,
                    "high-warning": 9500,
                    "low-alarm": -4000,
                    "low-warning": -3500
                }),
                description="更新溫度閾值 - 工業級範圍 (-40°C to 100°C)"
            ),
            
            # 更新溫度閾值 - 零度配置
            self.create_test_case(
                name="ddm_update_temperature_threshold_zero",
                method="PUT",
                url="/api/v1/transceiver-threshold/temperature",
                category="ddm_temperature_threshold",
                module="ddm",
                body=self.test_data.get('ddm_temperature_threshold_zero', {
                    "high-alarm": 0,
                    "high-warning": -100,
                    "low-alarm": -500,
                    "low-warning": -300
                }),
                description="更新溫度閾值 - 零度配置"
            ),
            
            # 測試無效溫度閾值 - 超出範圍
            self.create_test_case(
                name="ddm_test_invalid_temperature_threshold_range",
                method="PUT",
                url="/api/v1/transceiver-threshold/temperature",
                category="ddm_temperature_threshold",
                module="ddm",
                body=self.test_data.get('ddm_temperature_threshold_invalid_range', {
                    "high-alarm": 25000  # 超出範圍 -20000 to 20000
                }),
                expected_status=400,
                description="測試無效溫度閾值 - 超出範圍"
            )
        ]
    
    def get_ddm_tx_power_threshold_tests(self) -> List[APITestCase]:
        """DDM TX Power Threshold API 測試案例"""
        return [
            # 更新發送功率閾值 - 基本配置
            self.create_test_case(
                name="ddm_update_tx_power_threshold_basic",
                method="PUT",
                url="/api/v1/transceiver-threshold/tx-power",
                category="ddm_tx_power_threshold",
                module="ddm",
                body=self.test_data.get('ddm_tx_power_threshold_basic', {
                    "high-alarm": 1000,
                    "high-warning": 800,
                    "low-alarm": -1000,
                    "low-warning": -500
                }),
                description="更新發送功率閾值 - 基本配置"
            ),
            
            # 更新發送功率閾值 - 高功率配置
            self.create_test_case(
                name="ddm_update_tx_power_threshold_high_power",
                method="PUT",
                url="/api/v1/transceiver-threshold/tx-power",
                category="ddm_tx_power_threshold",
                module="ddm",
                body=self.test_data.get('ddm_tx_power_threshold_high_power', {
                    "high-alarm": 9999,
                    "high-warning": 9500,
                    "low-alarm": 8000,
                    "low-warning": 8500
                }),
                description="更新發送功率閾值 - 高功率配置"
            ),
            
            # 更新發送功率閾值 - 低功率配置
            self.create_test_case(
                name="ddm_update_tx_power_threshold_low_power",
                method="PUT",
                url="/api/v1/transceiver-threshold/tx-power",
                category="ddm_tx_power_threshold",
                module="ddm",
                body=self.test_data.get('ddm_tx_power_threshold_low_power', {
                    "high-alarm": -1000,
                    "high-warning": -1500,
                    "low-alarm": -9999,
                    "low-warning": -9000
                }),
                description="更新發送功率閾值 - 低功率配置"
            ),
            
            # 更新發送功率閾值 - 標準光模塊
            self.create_test_case(
                name="ddm_update_tx_power_threshold_standard_sfp",
                method="PUT",
                url="/api/v1/transceiver-threshold/tx-power",
                category="ddm_tx_power_threshold",
                module="ddm",
                body=self.test_data.get('ddm_tx_power_threshold_standard_sfp', {
                    "high-alarm": 300,
                    "high-warning": 200,
                    "low-alarm": -800,
                    "low-warning": -600
                }),
                description="更新發送功率閾值 - 標準SFP光模塊"
            ),
            
            # 更新發送功率閾值 - 零值配置
            self.create_test_case(
                name="ddm_update_tx_power_threshold_zero",
                method="PUT",
                url="/api/v1/transceiver-threshold/tx-power",
                category="ddm_tx_power_threshold",
                module="ddm",
                body=self.test_data.get('ddm_tx_power_threshold_zero', {
                    "high-alarm": 0,
                    "high-warning": -50,
                    "low-alarm": -200,
                    "low-warning": -100
                }),
                description="更新發送功率閾值 - 零值配置"
            ),
            
            # 測試無效發送功率閾值 - 超出範圍
            self.create_test_case(
                name="ddm_test_invalid_tx_power_threshold_range",
                method="PUT",
                url="/api/v1/transceiver-threshold/tx-power",
                category="ddm_tx_power_threshold",
                module="ddm",
                body=self.test_data.get('ddm_tx_power_threshold_invalid_range', {
                    "low-alarm": -15000  # 超出範圍 -9999 to 9999
                }),
                expected_status=400,
                description="測試無效發送功率閾值 - 超出範圍"
            )
        ]
    
    def get_ddm_voltage_threshold_tests(self) -> List[APITestCase]:
        """DDM Voltage Threshold API 測試案例"""
        return [
            # 更新電壓閾值 - 基本配置
            self.create_test_case(
                name="ddm_update_voltage_threshold_basic",
                method="PUT",
                url="/api/v1/transceiver-threshold/voltage",
                category="ddm_voltage_threshold",
                module="ddm",
                body=self.test_data.get('ddm_voltage_threshold_basic', {
                    "high-alarm": 3500,
                    "high-warning": 3400,
                    "low-alarm": 3000,
                    "low-warning": 3100
                }),
                description="更新電壓閾值 - 基本配置 (3.3V標準)"
            ),
            
            # 更新電壓閾值 - 5V系統
            self.create_test_case(
                name="ddm_update_voltage_threshold_5v_system",
                method="PUT",
                url="/api/v1/transceiver-threshold/voltage",
                category="ddm_voltage_threshold",
                module="ddm",
                body=self.test_data.get('ddm_voltage_threshold_5v_system', {
                    "high-alarm": 5500,
                    "high-warning": 5300,
                    "low-alarm": 4700,
                    "low-warning": 4800
                }),
                description="更新電壓閾值 - 5V系統"
            ),
            
            # 更新電壓閾值 - 1.8V系統
            self.create_test_case(
                name="ddm_update_voltage_threshold_1v8_system",
                method="PUT",
                url="/api/v1/transceiver-threshold/voltage",
                category="ddm_voltage_threshold",
                module="ddm",
                body=self.test_data.get('ddm_voltage_threshold_1v8_system', {
                    "high-alarm": 2000,
                    "high-warning": 1950,
                    "low-alarm": 1650,
                    "low-warning": 1700
                }),
                description="更新電壓閾值 - 1.8V系統"
            ),
            
            # 更新電壓閾值 - 最大值配置
            self.create_test_case(
                name="ddm_update_voltage_threshold_max",
                method="PUT",
                url="/api/v1/transceiver-threshold/voltage",
                category="ddm_voltage_threshold",
                module="ddm",
                body=self.test_data.get('ddm_voltage_threshold_max', {
                    "high-alarm": 9999,
                    "high-warning": 9500,
                    "low-alarm": 8000,
                    "low-warning": 8500
                }),
                description="更新電壓閾值 - 最大值配置"
            ),
            
            # 更新電壓閾值 - 最小值配置
            self.create_test_case(
                name="ddm_update_voltage_threshold_min",
                method="PUT",
                url="/api/v1/transceiver-threshold/voltage",
                category="ddm_voltage_threshold",
                module="ddm",
                body=self.test_data.get('ddm_voltage_threshold_min', {
                    "high-alarm": -9000,
                    "high-warning": -9200,
                    "low-alarm": -9999,
                    "low-warning": -9800
                }),
                description="更新電壓閾值 - 最小值配置"
            ),
            
            # 更新電壓閾值 - 零值配置
            self.create_test_case(
                name="ddm_update_voltage_threshold_zero",
                method="PUT",
                url="/api/v1/transceiver-threshold/voltage",
                category="ddm_voltage_threshold",
                module="ddm",
                body=self.test_data.get('ddm_voltage_threshold_zero', {
                    "high-alarm": 100,
                    "high-warning": 50,
                    "low-alarm": -100,
                    "low-warning": -50
                }),
                description="更新電壓閾值 - 零值附近配置"
            ),
            
            # 測試無效電壓閾值 - 超出範圍
            self.create_test_case(
                name="ddm_test_invalid_voltage_threshold_range",
                method="PUT",
                url="/api/v1/transceiver-threshold/voltage",
                category="ddm_voltage_threshold",
                module="ddm",
                body=self.test_data.get('ddm_voltage_threshold_invalid_range', {
                    "high-alarm": 15000  # 超出範圍 -9999 to 9999
                }),
                expected_status=400,
                description="測試無效電壓閾值 - 超出範圍"
            )
        ]
    
    def get_ddm_threshold_management_tests(self) -> List[APITestCase]:
        """DDM Threshold Management API 測試案例"""
        return [
            # 刪除所有閾值配置
            self.create_test_case(
                name="ddm_delete_all_thresholds",
                method="DELETE",
                url="/api/v1/transceiver-threshold",
                category="ddm_threshold_management",
                module="ddm",
                description="刪除所有光模塊閾值配置"
            ),
            
            # 重新配置完整閾值 - 電流
            self.create_test_case(
                name="ddm_reconfigure_current_threshold_after_delete",
                method="PUT",
                url="/api/v1/transceiver-threshold/current",
                category="ddm_threshold_management",
                module="ddm",
                body=self.test_data.get('ddm_reconfigure_current_threshold', {
                    "high-alarm": 2000,
                    "high-warning": 1800,
                    "low-alarm": 200,
                    "low-warning": 300
                }),
                description="重新配置電流閾值 - 刪除後重建"
            ),
            
            # 重新配置完整閾值 - 溫度
            self.create_test_case(
                name="ddm_reconfigure_temperature_threshold_after_delete",
                method="PUT",
                url="/api/v1/transceiver-threshold/temperature",
                category="ddm_threshold_management",
                module="ddm",
                body=self.test_data.get('ddm_reconfigure_temperature_threshold', {
                    "high-alarm": 7500,
                    "high-warning": 7000,
                    "low-alarm": -500,
                    "low-warning": 0
                }),
                description="重新配置溫度閾值 - 刪除後重建"
            ),
            
            # 批量配置所有閾值類型
            self.create_test_case(
                name="ddm_batch_configure_all_thresholds",
                method="PUT",
                url="/api/v1/transceiver-threshold/current",
                category="ddm_threshold_management",
                module="ddm",
                body=self.test_data.get('ddm_batch_current_config', {
                    "high-alarm": 2500,
                    "high-warning": 2200,
                    "low-alarm": 150,
                    "low-warning": 200
                }),
                description="批量配置 - 電流閾值"
            ),
            
            # 驗證閾值配置完整性
            self.create_test_case(
                name="ddm_verify_threshold_integrity",
                method="PUT",
                url="/api/v1/transceiver-threshold/voltage",
                category="ddm_threshold_management",
                module="ddm",
                body=self.test_data.get('ddm_verify_voltage_config', {
                    "high-alarm": 3600,
                    "high-warning": 3500,
                    "low-alarm": 2900,
                    "low-warning": 3000
                }),
                description="驗證閾值配置完整性 - 電壓"
            )
        ]
    
    def get_ddm_monitor_control_tests(self) -> List[APITestCase]:
        """DDM Monitor Control API 測試案例"""
        return [
            # 啟用光模塊監控
            self.create_test_case(
                name="ddm_enable_transceiver_monitor",
                method="POST",
                url="/api/v1/transceiver-monitor",
                category="ddm_monitor_control",
                module="ddm",
                description="啟用光模塊監控功能"
            ),
            
            # 禁用光模塊監控
            self.create_test_case(
                name="ddm_disable_transceiver_monitor",
                method="DELETE",
                url="/api/v1/transceiver-monitor",
                category="ddm_monitor_control",
                module="ddm",
                description="禁用光模塊監控功能"
            ),
            
            # 重新啟用光模塊監控
            self.create_test_case(
                name="ddm_re_enable_transceiver_monitor",
                method="POST",
                url="/api/v1/transceiver-monitor",
                category="ddm_monitor_control",
                module="ddm",
                description="重新啟用光模塊監控功能"
            ),
            
            # 監控狀態切換測試
            self.create_test_case(
                name="ddm_monitor_status_toggle_test",
                method="DELETE",
                url="/api/v1/transceiver-monitor",
                category="ddm_monitor_control",
                module="ddm",
                description="監控狀態切換測試 - 禁用"
            ),
            
            # 最終啟用監控
            self.create_test_case(
                name="ddm_final_enable_monitor",
                method="POST",
                url="/api/v1/transceiver-monitor",
                category="ddm_monitor_control",
                module="ddm",
                description="最終啟用光模塊監控"
            )
        ]
    
    def get_ddm_auto_threshold_tests(self) -> List[APITestCase]:
        """DDM Auto Threshold API 測試案例"""
        return [
            # 啟用自動閾值配置
            self.create_test_case(
                name="ddm_enable_auto_threshold",
                method="POST",
                url="/api/v1/transceiver-threshold-auto",
                category="ddm_auto_threshold",
                module="ddm",
                description="啟用光模塊自動閾值配置"
            ),
            
            # 禁用自動閾值配置
            self.create_test_case(
                name="ddm_disable_auto_threshold",
                method="DELETE",
                url="/api/v1/transceiver-threshold-auto",
                category="ddm_auto_threshold",
                module="ddm",
                description="禁用光模塊自動閾值配置"
            ),
            
            # 重新啟用自動閾值配置
            self.create_test_case(
                name="ddm_re_enable_auto_threshold",
                method="POST",
                url="/api/v1/transceiver-threshold-auto",
                category="ddm_auto_threshold",
                module="ddm",
                description="重新啟用光模塊自動閾值配置"
            ),
            
            # 自動閾值狀態切換測試
            self.create_test_case(
                name="ddm_auto_threshold_toggle_test",
                method="DELETE",
                url="/api/v1/transceiver-threshold-auto",
                category="ddm_auto_threshold",
                module="ddm",
                description="自動閾值狀態切換測試"
            ),
            
            # 最終啟用自動閾值
            self.create_test_case(
                name="ddm_final_enable_auto_threshold",
                method="POST",
                url="/api/v1/transceiver-threshold-auto",
                category="ddm_auto_threshold",
                module="ddm",
                description="最終啟用自動閾值配置"
            )
        ]