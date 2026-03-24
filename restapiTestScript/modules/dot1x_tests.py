#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
802.1X 模組測試案例
包含802.1X認證器全局配置、接口配置、統計信息、重新認證、EAPOL透傳、Supplicant配置等相關API測試
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class DOT1XTests(BaseTests):
    """802.1X 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取802.1X模組支援的類別"""
        return [
            "dot1x_global",
            "dot1x_interface",
            "dot1x_statistics",
            "dot1x_reauthentication",
            "dot1x_eapol",
            "dot1x_supplicant"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有802.1X測試案例"""
        all_tests = []
        all_tests.extend(self.get_dot1x_global_tests())
        all_tests.extend(self.get_dot1x_interface_tests())
        all_tests.extend(self.get_dot1x_statistics_tests())
        all_tests.extend(self.get_dot1x_reauthentication_tests())
        all_tests.extend(self.get_dot1x_eapol_tests())
        all_tests.extend(self.get_dot1x_supplicant_tests())
        return all_tests
    
    def get_dot1x_global_tests(self) -> List[APITestCase]:
        """802.1X Global API 測試案例"""
        return [
            # 獲取802.1X全局配置
            self.create_test_case(
                name="dot1x_get_global_config",
                method="GET",
                url="/api/v1/dot1x",
                category="dot1x_global",
                module="dot1x",
                description="獲取802.1X全局配置"
            ),
            
            # 啟用802.1X全局認證
            self.create_test_case(
                name="dot1x_enable_global_auth",
                method="PUT",
                url="/api/v1/dot1x",
                category="dot1x_global",
                module="dot1x",
                body=self.test_data.get('dot1x_enable_global', {
                    "systemAuthControlStatus": True
                }),
                description="啟用802.1X全局認證"
            ),
            
            # 禁用802.1X全局認證
            self.create_test_case(
                name="dot1x_disable_global_auth",
                method="PUT",
                url="/api/v1/dot1x",
                category="dot1x_global",
                module="dot1x",
                body=self.test_data.get('dot1x_disable_global', {
                    "systemAuthControlStatus": False
                }),
                description="禁用802.1X全局認證"
            ),
            
            # 重新啟用802.1X全局認證
            self.create_test_case(
                name="dot1x_re_enable_global_auth",
                method="PUT",
                url="/api/v1/dot1x",
                category="dot1x_global",
                module="dot1x",
                body=self.test_data.get('dot1x_re_enable_global', {
                    "systemAuthControlStatus": True
                }),
                description="重新啟用802.1X全局認證"
            ),
            
            # 設置802.1X全局和接口設置為默認值
            self.create_test_case(
                name="dot1x_set_default_config",
                method="PUT",
                url="/api/v1/dot1x:default",
                category="dot1x_global",
                module="dot1x",
                description="設置802.1X全局和接口設置為默認值"
            ),
            
            # 驗證全局配置更新
            self.create_test_case(
                name="dot1x_verify_global_config",
                method="GET",
                url="/api/v1/dot1x",
                category="dot1x_global",
                module="dot1x",
                description="驗證802.1X全局配置更新"
            )
        ]
    
    def get_dot1x_interface_tests(self) -> List[APITestCase]:
        """802.1X Interface API 測試案例"""
        return [
            # 獲取特定接口802.1X配置
            self.create_test_case(
                name="dot1x_get_interface_config",
                method="GET",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                description="獲取特定接口802.1X配置"
            ),
            
            # 獲取參數化接口802.1X配置
            self.create_test_case(
                name="dot1x_get_parameterized_interface_config",
                method="GET",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                description=f"獲取接口 {self.params.get('interface_id', 'eth1/1')} 802.1X配置"
            ),
            
            # 配置接口802.1X - 基本配置
            self.create_test_case(
                name="dot1x_configure_interface_basic",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                body=self.test_data.get('dot1x_interface_basic', {
                    "intrusionAction": "guest-vlan",
                    "maxReauthReq": 3,
                    "maxReq": 3,
                    "operationMode": "multi-host",
                    "maxMacCount": 10,
                    "portControl": "auto",
                    "quietPeriod": 65,
                    "reauthStatus": True,
                    "reauthPeriod": 100,
                    "suppTimeout": 100,
                    "txPeriod": 1000
                }),
                description="配置接口802.1X - 基本配置"
            ),
            
            # 配置接口802.1X - 單主機模式
            self.create_test_case(
                name="dot1x_configure_single_host_mode",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f1"},
                body=self.test_data.get('dot1x_single_host_mode', {
                    "operationMode": "single-host",
                    "portControl": "auto",
                    "intrusionAction": "block-traffic"
                }),
                description="配置接口802.1X - 單主機模式"
            ),
            
            # 配置接口802.1X - 多主機模式
            self.create_test_case(
                name="dot1x_configure_multi_host_mode",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                body=self.test_data.get('dot1x_multi_host_mode', {
                    "operationMode": "multi-host",
                    "maxMacCount": 5,
                    "portControl": "auto",
                    "intrusionAction": "guest-vlan"
                }),
                description="配置接口802.1X - 多主機模式"
            ),
            
            # 配置接口802.1X - MAC基礎認證模式
            self.create_test_case(
                name="dot1x_configure_mac_based_auth_mode",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f3"},
                body=self.test_data.get('dot1x_mac_based_auth_mode', {
                    "operationMode": "mac-based-auth",
                    "portControl": "auto",
                    "intrusionAction": "block-traffic"
                }),
                description="配置接口802.1X - MAC基礎認證模式"
            ),
            
            # 配置接口端口控制 - 自動
            self.create_test_case(
                name="dot1x_configure_port_control_auto",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f1"},
                body=self.test_data.get('dot1x_port_control_auto', {
                    "portControl": "auto"
                }),
                description="配置接口端口控制 - 自動"
            ),
            
            # 配置接口端口控制 - 強制授權
            self.create_test_case(
                name="dot1x_configure_port_control_force_authorized",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                body=self.test_data.get('dot1x_port_control_force_authorized', {
                    "portControl": "force-authorized"
                }),
                description="配置接口端口控制 - 強制授權"
            ),
            
            # 配置接口端口控制 - 強制未授權
            self.create_test_case(
                name="dot1x_configure_port_control_force_unauthorized",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f3"},
                body=self.test_data.get('dot1x_port_control_force_unauthorized', {
                    "portControl": "force-unauthorized"
                }),
                description="配置接口端口控制 - 強制未授權"
            ),
            
            # 配置入侵動作 - 阻塞流量
            self.create_test_case(
                name="dot1x_configure_intrusion_block_traffic",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f1"},
                body=self.test_data.get('dot1x_intrusion_block_traffic', {
                    "intrusionAction": "block-traffic"
                }),
                description="配置入侵動作 - 阻塞流量"
            ),
            
            # 配置入侵動作 - 訪客VLAN
            self.create_test_case(
                name="dot1x_configure_intrusion_guest_vlan",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                body=self.test_data.get('dot1x_intrusion_guest_vlan', {
                    "intrusionAction": "guest-vlan"
                }),
                description="配置入侵動作 - 訪客VLAN"
            ),
            
            # 配置重新認證 - 啟用
            self.create_test_case(
                name="dot1x_configure_reauthentication_enable",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f1"},
                body=self.test_data.get('dot1x_reauth_enable', {
                    "reauthStatus": True,
                    "reauthPeriod": 3600
                }),
                description="配置重新認證 - 啟用"
            ),
            
            # 配置重新認證 - 禁用
            self.create_test_case(
                name="dot1x_configure_reauthentication_disable",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                body=self.test_data.get('dot1x_reauth_disable', {
                    "reauthStatus": False
                }),
                description="配置重新認證 - 禁用"
            ),
            
            # 配置超時參數 - 最小值
            self.create_test_case(
                name="dot1x_configure_min_timeouts",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f1"},
                body=self.test_data.get('dot1x_min_timeouts', {
                    "quietPeriod": 1,
                    "suppTimeout": 1,
                    "txPeriod": 1,
                    "reauthPeriod": 1
                }),
                description="配置超時參數 - 最小值"
            ),
            
            # 配置超時參數 - 最大值
            self.create_test_case(
                name="dot1x_configure_max_timeouts",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                body=self.test_data.get('dot1x_max_timeouts', {
                    "quietPeriod": 65535,
                    "suppTimeout": 65535,
                    "txPeriod": 65535,
                    "reauthPeriod": 65535
                }),
                description="配置超時參數 - 最大值"
            ),
            
            # 配置最大請求次數 - 最小值
            self.create_test_case(
                name="dot1x_configure_min_max_requests",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f1"},
                body=self.test_data.get('dot1x_min_max_requests', {
                    "maxReq": 1,
                    "maxReauthReq": 1
                }),
                description="配置最大請求次數 - 最小值"
            ),
            
            # 配置最大請求次數 - 最大值
            self.create_test_case(
                name="dot1x_configure_max_max_requests",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                body=self.test_data.get('dot1x_max_max_requests', {
                    "maxReq": 10,
                    "maxReauthReq": 10
                }),
                description="配置最大請求次數 - 最大值"
            ),
            
            # 配置多主機模式最大MAC數量
            self.create_test_case(
                name="dot1x_configure_max_mac_count",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f1"},
                body=self.test_data.get('dot1x_max_mac_count', {
                    "operationMode": "multi-host",
                    "maxMacCount": 1024
                }),
                description="配置多主機模式最大MAC數量"
            ),
            
            # 測試無效接口ID
            self.create_test_case(
                name="dot1x_test_invalid_interface_id",
                method="GET",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "invalid-interface"},
                expected_status=400,
                description="測試無效接口ID"
            ),
            
            # 測試無效操作模式
            self.create_test_case(
                name="dot1x_test_invalid_operation_mode",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f1"},
                body=self.test_data.get('dot1x_invalid_operation_mode', {
                    "operationMode": "invalid-mode"
                }),
                expected_status=400,
                description="測試無效操作模式"
            ),
            
            # 測試無效端口控制
            self.create_test_case(
                name="dot1x_test_invalid_port_control",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f1"},
                body=self.test_data.get('dot1x_invalid_port_control', {
                    "portControl": "invalid-control"
                }),
                expected_status=400,
                description="測試無效端口控制"
            ),
            
            # 測試無效入侵動作
            self.create_test_case(
                name="dot1x_test_invalid_intrusion_action",
                method="PUT",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f1"},
                body=self.test_data.get('dot1x_invalid_intrusion_action', {
                    "intrusionAction": "invalid-action"
                }),
                expected_status=400,
                description="測試無效入侵動作"
            ),
            
            # 驗證接口配置更新
            self.create_test_case(
                name="dot1x_verify_interface_config",
                method="GET",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_interface",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                description="驗證接口802.1X配置更新"
            )
        ]
    
    def get_dot1x_statistics_tests(self) -> List[APITestCase]:
        """802.1X Statistics API 測試案例"""
        return [
            # 獲取接口802.1X統計信息
            self.create_test_case(
                name="dot1x_get_interface_statistics",
                method="GET",
                url="/api/v1/dot1x/statistics/interfaces/{ifId}",
                category="dot1x_statistics",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                description="獲取接口802.1X統計信息"
            ),
            
            # 獲取參數化接口統計信息
            self.create_test_case(
                name="dot1x_get_parameterized_interface_statistics",
                method="GET",
                url="/api/v1/dot1x/statistics/interfaces/{ifId}",
                category="dot1x_statistics",
                module="dot1x",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                description=f"獲取接口 {self.params.get('interface_id', 'eth1/1')} 802.1X統計信息"
            ),
            
            # 獲取多個接口統計信息
            self.create_test_case(
                name="dot1x_get_multiple_interface_statistics",
                method="GET",
                url="/api/v1/dot1x/statistics/interfaces/{ifId}",
                category="dot1x_statistics",
                module="dot1x",
                params={"ifId": "eth1%2f1"},
                description="獲取多個接口802.1X統計信息"
            ),
            
            # 測試無效接口統計查詢
            self.create_test_case(
                name="dot1x_test_invalid_statistics_interface",
                method="GET",
                url="/api/v1/dot1x/statistics/interfaces/{ifId}",
                category="dot1x_statistics",
                module="dot1x",
                params={"ifId": "invalid-interface"},
                expected_status=400,
                description="測試無效接口統計查詢"
            ),
            
            # 監控統計信息變化
            self.create_test_case(
                name="dot1x_monitor_statistics_changes",
                method="GET",
                url="/api/v1/dot1x/statistics/interfaces/{ifId}",
                category="dot1x_statistics",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                description="監控802.1X統計信息變化"
            )
        ]
    
    def get_dot1x_reauthentication_tests(self) -> List[APITestCase]:
        """802.1X Reauthentication API 測試案例"""
        return [
            # 強制重新認證特定接口
            self.create_test_case(
                name="dot1x_force_reauthentication",
                method="POST",
                url="/api/v1/dot1x/reauthenticate/interfaces/{ifId}",
                category="dot1x_reauthentication",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                description="強制重新認證特定接口"
            ),
            
            # 強制重新認證參數化接口
            self.create_test_case(
                name="dot1x_force_reauthentication_parameterized",
                method="POST",
                url="/api/v1/dot1x/reauthenticate/interfaces/{ifId}",
                category="dot1x_reauthentication",
                module="dot1x",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                description=f"強制重新認證接口 {self.params.get('interface_id', 'eth1/1')}"
            ),
            
            # 強制重新認證多個接口
            self.create_test_case(
                name="dot1x_force_reauthentication_multiple",
                method="POST",
                url="/api/v1/dot1x/reauthenticate/interfaces/{ifId}",
                category="dot1x_reauthentication",
                module="dot1x",
                params={"ifId": "eth1%2f1"},
                description="強制重新認證多個接口"
            ),
            
            # 測試無效接口重新認證
            self.create_test_case(
                name="dot1x_test_invalid_reauthentication_interface",
                method="POST",
                url="/api/v1/dot1x/reauthenticate/interfaces/{ifId}",
                category="dot1x_reauthentication",
                module="dot1x",
                params={"ifId": "invalid-interface"},
                expected_status=400,
                description="測試無效接口重新認證"
            ),
            
            # 驗證重新認證後狀態
            self.create_test_case(
                name="dot1x_verify_post_reauthentication_status",
                method="GET",
                url="/api/v1/dot1x/interfaces/{ifId}",
                category="dot1x_reauthentication",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                description="驗證重新認證後接口狀態"
            )
        ]
    
    def get_dot1x_eapol_tests(self) -> List[APITestCase]:
        """802.1X EAPOL API 測試案例"""
        return [
            # 獲取EAPOL透傳狀態
            self.create_test_case(
                name="dot1x_get_eapol_pass_through_status",
                method="GET",
                url="/api/v1/dot1x/eapol-pass-through",
                category="dot1x_eapol",
                module="dot1x",
                description="獲取EAPOL透傳狀態"
            ),
            
            # 啟用EAPOL透傳
            self.create_test_case(
                name="dot1x_enable_eapol_pass_through",
                method="PUT",
                url="/api/v1/dot1x/eapol-pass-through",
                category="dot1x_eapol",
                module="dot1x",
                body=self.test_data.get('dot1x_eapol_enable', {
                    "status": True
                }),
                description="啟用EAPOL透傳"
            ),
            
            # 禁用EAPOL透傳
            self.create_test_case(
                name="dot1x_disable_eapol_pass_through",
                method="PUT",
                url="/api/v1/dot1x/eapol-pass-through",
                category="dot1x_eapol",
                module="dot1x",
                body=self.test_data.get('dot1x_eapol_disable', {
                    "status": False
                }),
                description="禁用EAPOL透傳"
            ),
            
            # 重新啟用EAPOL透傳
            self.create_test_case(
                name="dot1x_re_enable_eapol_pass_through",
                method="PUT",
                url="/api/v1/dot1x/eapol-pass-through",
                category="dot1x_eapol",
                module="dot1x",
                body=self.test_data.get('dot1x_eapol_re_enable', {
                    "status": True
                }),
                description="重新啟用EAPOL透傳"
            ),
            
            # 驗證EAPOL透傳配置
            self.create_test_case(
                name="dot1x_verify_eapol_pass_through_config",
                method="GET",
                url="/api/v1/dot1x/eapol-pass-through",
                category="dot1x_eapol",
                module="dot1x",
                description="驗證EAPOL透傳配置"
            )
        ]
    
    def get_dot1x_supplicant_tests(self) -> List[APITestCase]:
        """802.1X Supplicant API 測試案例"""
        return [
            # 獲取Supplicant用戶名
            self.create_test_case(
                name="dot1x_get_supplicant_username",
                method="GET",
                url="/api/v1/dot1x/supplicant",
                category="dot1x_supplicant",
                module="dot1x",
                description="獲取Supplicant用戶名"
            ),
            
            # 設置Supplicant用戶名和密碼
            self.create_test_case(
                name="dot1x_set_supplicant_credentials",
                method="PUT",
                url="/api/v1/dot1x/supplicant",
                category="dot1x_supplicant",
                module="dot1x",
                body=self.test_data.get('dot1x_supplicant_credentials', {
                    "username": "steve",
                    "password": "excess"
                }),
                description="設置Supplicant用戶名和密碼"
            ),
            
            # 更新Supplicant用戶名
            self.create_test_case(
                name="dot1x_update_supplicant_username",
                method="PUT",
                url="/api/v1/dot1x/supplicant",
                category="dot1x_supplicant",
                module="dot1x",
                body=self.test_data.get('dot1x_supplicant_username_only', {
                    "username": "admin"
                }),
                description="更新Supplicant用戶名"
            ),
            
            # 更新Supplicant密碼
            self.create_test_case(
                name="dot1x_update_supplicant_password",
                method="PUT",
                url="/api/v1/dot1x/supplicant",
                category="dot1x_supplicant",
                module="dot1x",
                body=self.test_data.get('dot1x_supplicant_password_only', {
                    "password": "newpass"
                }),
                description="更新Supplicant密碼"
            ),
            
            # 獲取接口Supplicant屬性
            self.create_test_case(
                name="dot1x_get_supplicant_interface_properties",
                method="GET",
                url="/api/v1/dot1x/supplicant/interfaces/{ifId}",
                category="dot1x_supplicant",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                description="獲取接口Supplicant屬性"
            ),
            
            # 獲取參數化接口Supplicant屬性
            self.create_test_case(
                name="dot1x_get_parameterized_supplicant_interface",
                method="GET",
                url="/api/v1/dot1x/supplicant/interfaces/{ifId}",
                category="dot1x_supplicant",
                module="dot1x",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                description=f"獲取接口 {self.params.get('interface_id', 'eth1/1')} Supplicant屬性"
            ),
            
            # 配置接口Supplicant屬性 - 基本配置
            self.create_test_case(
                name="dot1x_configure_supplicant_interface_basic",
                method="PUT",
                url="/api/v1/dot1x/supplicant/interfaces/{ifId}",
                category="dot1x_supplicant",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                body=self.test_data.get('dot1x_supplicant_interface_basic', {
                    "maxStart": 10,
                    "paeSupplicant": True,
                    "authPeriod": 60,
                    "heldPeriod": 120,
                    "startPeriod": 60
                }),
                description="配置接口Supplicant屬性 - 基本配置"
            ),
            
            # 啟用接口Supplicant模式
            self.create_test_case(
                name="dot1x_enable_supplicant_mode",
                method="PUT",
                url="/api/v1/dot1x/supplicant/interfaces/{ifId}",
                category="dot1x_supplicant",
                module="dot1x",
                params={"ifId": "eth1%2f1"},
                body=self.test_data.get('dot1x_supplicant_enable', {
                    "paeSupplicant": True
                }),
                description="啟用接口Supplicant模式"
            ),
            
            # 禁用接口Supplicant模式
            self.create_test_case(
                name="dot1x_disable_supplicant_mode",
                method="PUT",
                url="/api/v1/dot1x/supplicant/interfaces/{ifId}",
                category="dot1x_supplicant",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                body=self.test_data.get('dot1x_supplicant_disable', {
                    "paeSupplicant": False
                }),
                description="禁用接口Supplicant模式"
            ),
            
            # 配置Supplicant超時參數 - 最小值
            self.create_test_case(
                name="dot1x_configure_supplicant_min_timeouts",
                method="PUT",
                url="/api/v1/dot1x/supplicant/interfaces/{ifId}",
                category="dot1x_supplicant",
                module="dot1x",
                params={"ifId": "eth1%2f1"},
                body=self.test_data.get('dot1x_supplicant_min_timeouts', {
                    "authPeriod": 1,
                    "heldPeriod": 1,
                    "startPeriod": 1
                }),
                description="配置Supplicant超時參數 - 最小值"
            ),
            
            # 配置Supplicant超時參數 - 最大值
            self.create_test_case(
                name="dot1x_configure_supplicant_max_timeouts",
                method="PUT",
                url="/api/v1/dot1x/supplicant/interfaces/{ifId}",
                category="dot1x_supplicant",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                body=self.test_data.get('dot1x_supplicant_max_timeouts', {
                    "authPeriod": 65535,
                    "heldPeriod": 65535,
                    "startPeriod": 65535
                }),
                description="配置Supplicant超時參數 - 最大值"
            ),
            
            # 配置最大啟動幀數 - 最小值
            self.create_test_case(
                name="dot1x_configure_supplicant_min_max_start",
                method="PUT",
                url="/api/v1/dot1x/supplicant/interfaces/{ifId}",
                category="dot1x_supplicant",
                module="dot1x",
                params={"ifId": "eth1%2f1"},
                body=self.test_data.get('dot1x_supplicant_min_max_start', {
                    "maxStart": 1
                }),
                description="配置最大啟動幀數 - 最小值"
            ),
            
            # 配置最大啟動幀數 - 最大值
            self.create_test_case(
                name="dot1x_configure_supplicant_max_max_start",
                method="PUT",
                url="/api/v1/dot1x/supplicant/interfaces/{ifId}",
                category="dot1x_supplicant",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                body=self.test_data.get('dot1x_supplicant_max_max_start', {
                    "maxStart": 65535
                }),
                description="配置最大啟動幀數 - 最大值"
            ),
            
            # 獲取接口Supplicant統計信息
            self.create_test_case(
                name="dot1x_get_supplicant_interface_statistics",
                method="GET",
                url="/api/v1/dot1x/supplicant/statistics/interfaces/{ifId}",
                category="dot1x_supplicant",
                module="dot1x",
                params={"ifId": "eth1%2f2"},
                description="獲取接口Supplicant統計信息"
            ),
            
            # 獲取參數化接口Supplicant統計信息
            self.create_test_case(
                name="dot1x_get_parameterized_supplicant_statistics",
                method="GET",
                url="/api/v1/dot1x/supplicant/statistics/interfaces/{ifId}",
                category="dot1x_supplicant",
                module="dot1x",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                description=f"獲取接口 {self.params.get('interface_id', 'eth1/1')} Supplicant統計信息"
            ),
            
            # 測試無效Supplicant用戶名長度
            self.create_test_case(
                name="dot1x_test_invalid_supplicant_username_length",
                method="PUT",
                url="/api/v1/dot1x/supplicant",
                category="dot1x_supplicant",
                module="dot1x",
                body=self.test_data.get('dot1x_supplicant_invalid_username', {
                    "username": "verylongusernamethatexceedslimit"  # 超過8字符
                }),
                expected_status=400,
                description="測試無效Supplicant用戶名長度"
            ),
            
            # 測試無效Supplicant密碼長度
            self.create_test_case(
                name="dot1x_test_invalid_supplicant_password_length",
                method="PUT",
                url="/api/v1/dot1x/supplicant",
                category="dot1x_supplicant",
                module="dot1x",
                body=self.test_data.get('dot1x_supplicant_invalid_password', {
                    "password": "verylongpasswordthatexceedslimit"  # 超過8字符
                }),
                expected_status=400,
                description="測試無效Supplicant密碼長度"
            ),
            
            # 測試無效Supplicant接口參數
            self.create_test_case(
                name="dot1x_test_invalid_supplicant_interface_params",
                method="PUT",
                url="/api/v1/dot1x/supplicant/interfaces/{ifId}",
                category="dot1x_supplicant",
                module="dot1x",
                params={"ifId": "eth1%2f1"},
                body=self.test_data.get('dot1x_supplicant_invalid_params', {
                    "maxStart": 70000,  # 超出範圍 1-65535
                    "authPeriod": 70000  # 超出範圍 1-65535
                }),
                expected_status=400,
                description="測試無效Supplicant接口參數"
            ),
            
            # 驗證Supplicant配置更新
            self.create_test_case(
                name="dot1x_verify_supplicant_config",
                method="GET",
                url="/api/v1/dot1x/supplicant",
                category="dot1x_supplicant",
                module="dot1x",
                description="驗證Supplicant配置更新"
            )
        ]