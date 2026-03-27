#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Loopback Detection 模組測試案例
包含環路檢測全局配置、接口配置、狀態監控等相關API測試
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class LOOPBACK_DETECTIONTests(BaseTests):
    """Loopback Detection 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取Loopback Detection模組支援的類別"""
        return [
            "lbd_global",
            "lbd_interface",
            "lbd_monitoring",
            "lbd_recovery"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有Loopback Detection測試案例"""
        all_tests = []
        all_tests.extend(self.get_lbd_global_tests())
        all_tests.extend(self.get_lbd_interface_tests())
        all_tests.extend(self.get_lbd_monitoring_tests())
        all_tests.extend(self.get_lbd_recovery_tests())
        return all_tests
    
    def get_lbd_global_tests(self) -> List[APITestCase]:
        """Loopback Detection Global API 測試案例"""
        return [
            # 獲取環路檢測全局配置
            self.create_test_case(
                name="lbd_get_global_config",
                method="GET",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                description="獲取環路檢測全局配置"
            ),
            
            # 啟用環路檢測 - 基本配置
            self.create_test_case(
                name="lbd_enable_basic",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_basic_config', {
                    "status": True,
                    "interval": 100,
                    "recover": 0,
                    "action": "block",
                    "trap": "both"
                }),
                description="啟用環路檢測 - 基本配置"
            ),
            
            # 啟用環路檢測 - 僅啟用狀態
            self.create_test_case(
                name="lbd_enable_only",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_enable_only', {
                    "status": True
                }),
                description="啟用環路檢測 - 僅啟用狀態"
            ),
            
            # 配置傳輸間隔 - 最小值
            self.create_test_case(
                name="lbd_configure_min_interval",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_min_interval', {
                    "status": True,
                    "interval": 1
                }),
                description="配置傳輸間隔 - 最小值 (1秒)"
            ),
            
            # 配置傳輸間隔 - 最大值
            self.create_test_case(
                name="lbd_configure_max_interval",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_max_interval', {
                    "status": True,
                    "interval": 32767
                }),
                description="配置傳輸間隔 - 最大值 (32767秒)"
            ),
            
            # 配置傳輸間隔 - 中等值
            self.create_test_case(
                name="lbd_configure_medium_interval",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_medium_interval', {
                    "status": True,
                    "interval": 60
                }),
                description="配置傳輸間隔 - 中等值 (60秒)"
            ),
            
            # 配置恢復時間 - 禁用自動恢復
            self.create_test_case(
                name="lbd_configure_no_recovery",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_no_recovery', {
                    "status": True,
                    "interval": 100,
                    "recover": 0
                }),
                description="配置恢復時間 - 禁用自動恢復 (0)"
            ),
            
            # 配置恢復時間 - 最小值
            self.create_test_case(
                name="lbd_configure_min_recovery",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_min_recovery', {
                    "status": True,
                    "interval": 100,
                    "recover": 60
                }),
                description="配置恢復時間 - 最小值 (60秒)"
            ),
            
            # 配置恢復時間 - 最大值
            self.create_test_case(
                name="lbd_configure_max_recovery",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_max_recovery', {
                    "status": True,
                    "interval": 100,
                    "recover": 1000000
                }),
                description="配置恢復時間 - 最大值 (1000000秒)"
            ),
            
            # 配置恢復時間 - 中等值
            self.create_test_case(
                name="lbd_configure_medium_recovery",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_medium_recovery', {
                    "status": True,
                    "interval": 100,
                    "recover": 300
                }),
                description="配置恢復時間 - 中等值 (300秒)"
            ),
            
            # 配置保護動作 - 無動作
            self.create_test_case(
                name="lbd_configure_action_none",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_action_none', {
                    "status": True,
                    "interval": 100,
                    "action": "none"
                }),
                description="配置保護動作 - 無動作"
            ),
            
            # 配置保護動作 - 阻塞
            self.create_test_case(
                name="lbd_configure_action_block",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_action_block', {
                    "status": True,
                    "interval": 100,
                    "action": "block"
                }),
                description="配置保護動作 - 阻塞"
            ),
            
            # 配置保護動作 - 關閉
            self.create_test_case(
                name="lbd_configure_action_shutdown",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_action_shutdown', {
                    "status": True,
                    "interval": 100,
                    "action": "shutdown"
                }),
                description="配置保護動作 - 關閉"
            ),
            
            # 配置SNMP陷阱 - 無陷阱
            self.create_test_case(
                name="lbd_configure_trap_none",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_trap_none', {
                    "status": True,
                    "interval": 100,
                    "trap": "none"
                }),
                description="配置SNMP陷阱 - 無陷阱"
            ),
            
            # 配置SNMP陷阱 - 僅恢復
            self.create_test_case(
                name="lbd_configure_trap_recover",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_trap_recover', {
                    "status": True,
                    "interval": 100,
                    "trap": "recover"
                }),
                description="配置SNMP陷阱 - 僅恢復"
            ),
            
            # 配置SNMP陷阱 - 僅檢測
            self.create_test_case(
                name="lbd_configure_trap_detect",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_trap_detect', {
                    "status": True,
                    "interval": 100,
                    "trap": "detect"
                }),
                description="配置SNMP陷阱 - 僅檢測"
            ),
            
            # 配置SNMP陷阱 - 兩者都有
            self.create_test_case(
                name="lbd_configure_trap_both",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_trap_both', {
                    "status": True,
                    "interval": 100,
                    "trap": "both"
                }),
                description="配置SNMP陷阱 - 檢測和恢復"
            ),
            
            # 完整環路檢測配置
            self.create_test_case(
                name="lbd_complete_configuration",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_complete_config', {
                    "status": True,
                    "interval": 30,
                    "recover": 180,
                    "action": "block",
                    "trap": "both"
                }),
                description="完整環路檢測配置"
            ),
            
            # 禁用環路檢測
            self.create_test_case(
                name="lbd_disable",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_disable', {
                    "status": False
                }),
                description="禁用環路檢測"
            ),
            
            # 重新啟用環路檢測
            self.create_test_case(
                name="lbd_re_enable",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_re_enable', {
                    "status": True,
                    "interval": 50,
                    "recover": 120,
                    "action": "shutdown",
                    "trap": "detect"
                }),
                description="重新啟用環路檢測"
            ),
            
            # 測試無效傳輸間隔 - 超出範圍
            self.create_test_case(
                name="lbd_test_invalid_interval_high",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_invalid_interval_high', {
                    "status": True,
                    "interval": 40000  # 超出範圍 1-32767
                }),
                description="測試無效傳輸間隔 - 超出上限"
            ),
            
            # 測試無效傳輸間隔 - 低於範圍
            self.create_test_case(
                name="lbd_test_invalid_interval_low",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_invalid_interval_low', {
                    "status": True,
                    "interval": 0  # 低於範圍 1-32767
                }),
                description="測試無效傳輸間隔 - 低於下限"
            ),
            
            # 測試無效恢復時間 - 超出範圍
            self.create_test_case(
                name="lbd_test_invalid_recovery_high",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_invalid_recovery_high', {
                    "status": True,
                    "interval": 100,
                    "recover": 2000000  # 超出範圍 0, 60-1000000
                }),
                description="測試無效恢復時間 - 超出上限"
            ),
            
            # 測試無效恢復時間 - 在禁用範圍內
            self.create_test_case(
                name="lbd_test_invalid_recovery_range",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_invalid_recovery_range', {
                    "status": True,
                    "interval": 100,
                    "recover": 30  # 在無效範圍 1-59
                }),
                expected_status=500,
                description="測試無效恢復時間 - 在禁用範圍內"
            ),
            
            # 測試無效保護動作
            self.create_test_case(
                name="lbd_test_invalid_action",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_invalid_action', {
                    "status": True,
                    "interval": 100,
                    "action": "invalid"  # 無效動作
                }),
                expected_status=400,
                description="測試無效保護動作"
            ),
            
            # 測試無效陷阱模式
            self.create_test_case(
                name="lbd_test_invalid_trap",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                body=self.test_data.get('lbd_invalid_trap', {
                    "status": True,
                    "interval": 100,
                    "trap": "invalid"  # 無效陷阱模式
                }),
                expected_status=400,
                description="測試無效陷阱模式"
            ),
            
            # 驗證全局配置更新
            self.create_test_case(
                name="lbd_verify_global_config",
                method="GET",
                url="/api/v1/lbd",
                category="lbd_global",
                module="loopback_detection",
                description="驗證環路檢測全局配置更新"
            )
        ]
    
    def get_lbd_interface_tests(self) -> List[APITestCase]:
        """Loopback Detection Interface API 測試案例"""
        return [
            # 獲取所有接口環路檢測配置
            self.create_test_case(
                name="lbd_get_all_interfaces",
                method="GET",
                url="/api/v1/lbd/interfaces",
                category="lbd_interface",
                module="loopback_detection",
                description="獲取所有接口環路檢測配置"
            ),
            
            # 啟用單個接口環路檢測
            self.create_test_case(
                name="lbd_enable_single_interface",
                method="PUT",
                url="/api/v1/lbd/interfaces",
                category="lbd_interface",
                module="loopback_detection",
                body=self.test_data.get('lbd_enable_single_port', {
                    "status": True,
                    "ports": [1]
                }),
                description="啟用單個接口環路檢測"
            ),
            
            # 啟用多個接口環路檢測
            self.create_test_case(
                name="lbd_enable_multiple_interfaces",
                method="PUT",
                url="/api/v1/lbd/interfaces",
                category="lbd_interface",
                module="loopback_detection",
                body=self.test_data.get('lbd_enable_multiple_ports', {
                    "status": True,
                    "ports": [1, 2, 3]
                }),
                description="啟用多個接口環路檢測"
            ),
            
            # 啟用接口範圍環路檢測
            self.create_test_case(
                name="lbd_enable_interface_range",
                method="PUT",
                url="/api/v1/lbd/interfaces",
                category="lbd_interface",
                module="loopback_detection",
                body=self.test_data.get('lbd_enable_port_range', {
                    "status": True,
                    "ports": [5, 6, 7, 8, 9, 10]
                }),
                description="啟用接口範圍環路檢測"
            ),
            
            # 累積啟用接口環路檢測
            self.create_test_case(
                name="lbd_cumulative_enable_interfaces",
                method="PUT",
                url="/api/v1/lbd/interfaces",
                category="lbd_interface",
                module="loopback_detection",
                body=self.test_data.get('lbd_cumulative_enable', {
                    "status": True,
                    "ports": [20]  # 累積到之前的配置
                }),
                description="累積啟用接口環路檢測"
            ),
            
            # 禁用單個接口環路檢測
            self.create_test_case(
                name="lbd_disable_single_interface",
                method="PUT",
                url="/api/v1/lbd/interfaces",
                category="lbd_interface",
                module="loopback_detection",
                body=self.test_data.get('lbd_disable_single_port', {
                    "status": False,
                    "ports": [1]
                }),
                description="禁用單個接口環路檢測"
            ),
            
            # 禁用多個接口環路檢測
            self.create_test_case(
                name="lbd_disable_multiple_interfaces",
                method="PUT",
                url="/api/v1/lbd/interfaces",
                category="lbd_interface",
                module="loopback_detection",
                body=self.test_data.get('lbd_disable_multiple_ports', {
                    "status": False,
                    "ports": [2, 3]
                }),
                description="禁用多個接口環路檢測"
            ),
            
            # 禁用所有接口環路檢測
            self.create_test_case(
                name="lbd_disable_all_interfaces",
                method="PUT",
                url="/api/v1/lbd/interfaces",
                category="lbd_interface",
                module="loopback_detection",
                body=self.test_data.get('lbd_disable_all_ports', {
                    "status": False,
                    "ports": [5, 6, 7, 8, 9, 10, 20]
                }),
                description="禁用所有接口環路檢測"
            ),
            
            # 獲取特定接口環路檢測信息
            self.create_test_case(
                name="lbd_get_specific_interface",
                method="GET",
                url="/api/v1/lbd/interfaces/{id}",
                category="lbd_interface",
                module="loopback_detection",
                params={"id": "1"},
                description="獲取特定接口環路檢測信息"
            ),
            
            # 獲取參數化接口環路檢測信息
            self.create_test_case(
                name="lbd_get_parameterized_interface",
                method="GET",
                url="/api/v1/lbd/interfaces/{id}",
                category="lbd_interface",
                module="loopback_detection",
                params={"id": self.params.get('interface_port_id', '1')},
                description=f"獲取接口 {self.params.get('interface_port_id', '1')} 環路檢測信息"
            ),
            
            # 測試無效接口ID
            self.create_test_case(
                name="lbd_test_invalid_interface_id",
                method="GET",
                url="/api/v1/lbd/interfaces/{id}",
                category="lbd_interface",
                module="loopback_detection",
                params={"id": "999"},
                expected_status=400,
                description="測試無效接口ID"
            ),
            
            # 測試空接口列表
            self.create_test_case(
                name="lbd_test_empty_port_list",
                method="PUT",
                url="/api/v1/lbd/interfaces",
                category="lbd_interface",
                module="loopback_detection",
                body=self.test_data.get('lbd_empty_port_list', {
                    "status": True,
                    "ports": []
                }),
                expected_status=400,
                description="測試空接口列表"
            ),
            
            # 測試無效接口號
            self.create_test_case(
                name="lbd_test_invalid_port_number",
                method="PUT",
                url="/api/v1/lbd/interfaces",
                category="lbd_interface",
                module="loopback_detection",
                body=self.test_data.get('lbd_invalid_port_number', {
                    "status": True,
                    "ports": [0, -1, 999]  # 無效接口號
                }),
                expected_status=400,
                description="測試無效接口號"
            ),
            
            # 驗證接口配置更新
            self.create_test_case(
                name="lbd_verify_interface_config",
                method="GET",
                url="/api/v1/lbd/interfaces",
                category="lbd_interface",
                module="loopback_detection",
                description="驗證接口環路檢測配置更新"
            )
        ]
    
    def get_lbd_monitoring_tests(self) -> List[APITestCase]:
        """Loopback Detection Monitoring API 測試案例"""
        return [
            # 監控所有接口狀態
            self.create_test_case(
                name="lbd_monitor_all_interfaces",
                method="GET",
                url="/api/v1/lbd/interfaces",
                category="lbd_monitoring",
                module="loopback_detection",
                description="監控所有接口環路檢測狀態"
            ),
            
            # 監控特定接口狀態 - 正常接口
            self.create_test_case(
                name="lbd_monitor_normal_interface",
                method="GET",
                url="/api/v1/lbd/interfaces/{id}",
                category="lbd_monitoring",
                module="loopback_detection",
                params={"id": "1"},
                description="監控正常接口環路檢測狀態"
            ),
            
            # 監控特定接口狀態 - 環路接口
            self.create_test_case(
                name="lbd_monitor_looped_interface",
                method="GET",
                url="/api/v1/lbd/interfaces/{id}",
                category="lbd_monitoring",
                module="loopback_detection",
                params={"id": "2"},
                description="監控環路接口狀態"
            ),
            
            # 監控特定接口狀態 - 禁用接口
            self.create_test_case(
                name="lbd_monitor_disabled_interface",
                method="GET",
                url="/api/v1/lbd/interfaces/{id}",
                category="lbd_monitoring",
                module="loopback_detection",
                params={"id": "3"},
                description="監控禁用接口狀態"
            ),
            
            # 監控全局配置狀態
            self.create_test_case(
                name="lbd_monitor_global_status",
                method="GET",
                url="/api/v1/lbd",
                category="lbd_monitoring",
                module="loopback_detection",
                description="監控環路檢測全局狀態"
            ),
            
            # 定期監控接口狀態變化
            self.create_test_case(
                name="lbd_periodic_monitor_interfaces",
                method="GET",
                url="/api/v1/lbd/interfaces",
                category="lbd_monitoring",
                module="loopback_detection",
                description="定期監控接口狀態變化"
            ),
            
            # 監控接口操作狀態統計
            self.create_test_case(
                name="lbd_monitor_operation_statistics",
                method="GET",
                url="/api/v1/lbd/interfaces",
                category="lbd_monitoring",
                module="loopback_detection",
                description="監控接口操作狀態統計"
            ),
            
            # 監控環路檢測事件
            self.create_test_case(
                name="lbd_monitor_detection_events",
                method="GET",
                url="/api/v1/lbd",
                category="lbd_monitoring",
                module="loopback_detection",
                description="監控環路檢測事件"
            )
        ]
    
    def get_lbd_recovery_tests(self) -> List[APITestCase]:
        """Loopback Detection Recovery API 測試案例"""
        return [
            # 測試自動恢復功能 - 啟用自動恢復
            self.create_test_case(
                name="lbd_test_auto_recovery_enable",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_recovery",
                module="loopback_detection",
                body=self.test_data.get('lbd_auto_recovery_enable', {
                    "status": True,
                    "interval": 30,
                    "recover": 120,
                    "action": "block",
                    "trap": "both"
                }),
                description="測試自動恢復功能 - 啟用自動恢復"
            ),
            
            # 測試自動恢復功能 - 短恢復時間
            self.create_test_case(
                name="lbd_test_short_recovery_time",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_recovery",
                module="loopback_detection",
                body=self.test_data.get('lbd_short_recovery', {
                    "status": True,
                    "interval": 30,
                    "recover": 60,
                    "action": "block",
                    "trap": "recover"
                }),
                description="測試短恢復時間配置"
            ),
            
            # 測試自動恢復功能 - 長恢復時間
            self.create_test_case(
                name="lbd_test_long_recovery_time",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_recovery",
                module="loopback_detection",
                body=self.test_data.get('lbd_long_recovery', {
                    "status": True,
                    "interval": 30,
                    "recover": 600,
                    "action": "shutdown",
                    "trap": "both"
                }),
                description="測試長恢復時間配置"
            ),
            
            # 測試禁用自動恢復
            self.create_test_case(
                name="lbd_test_disable_auto_recovery",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_recovery",
                module="loopback_detection",
                body=self.test_data.get('lbd_disable_auto_recovery', {
                    "status": True,
                    "interval": 30,
                    "recover": 0,
                    "action": "block",
                    "trap": "detect"
                }),
                description="測試禁用自動恢復"
            ),
            
            # 測試恢復陷阱配置
            self.create_test_case(
                name="lbd_test_recovery_trap_config",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_recovery",
                module="loopback_detection",
                body=self.test_data.get('lbd_recovery_trap_config', {
                    "status": True,
                    "interval": 30,
                    "recover": 180,
                    "action": "block",
                    "trap": "recover"
                }),
                description="測試恢復陷阱配置"
            ),
            
            # 驗證恢復功能配置
            self.create_test_case(
                name="lbd_verify_recovery_config",
                method="GET",
                url="/api/v1/lbd",
                category="lbd_recovery",
                module="loopback_detection",
                description="驗證恢復功能配置"
            ),
            
            # 測試恢復後接口狀態
            self.create_test_case(
                name="lbd_test_post_recovery_interface_status",
                method="GET",
                url="/api/v1/lbd/interfaces",
                category="lbd_recovery",
                module="loopback_detection",
                description="測試恢復後接口狀態"
            ),
            
            # 測試不同保護動作的恢復行為
            self.create_test_case(
                name="lbd_test_recovery_with_different_actions",
                method="PUT",
                url="/api/v1/lbd",
                category="lbd_recovery",
                module="loopback_detection",
                body=self.test_data.get('lbd_recovery_different_actions', {
                    "status": True,
                    "interval": 30,
                    "recover": 90,
                    "action": "shutdown",
                    "trap": "both"
                }),
                description="測試不同保護動作的恢復行為"
            )
        ]