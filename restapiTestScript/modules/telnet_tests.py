#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telnet 模組測試案例
包含Telnet服務器配置、端口設置、會話管理、超時配置等相關API測試
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class TELNETTests(BaseTests):
    """Telnet 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取Telnet模組支援的類別"""
        return [
            "telnet_server",
            "telnet_configuration",
            "telnet_sessions",
            "telnet_security"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有Telnet測試案例"""
        all_tests = []
        all_tests.extend(self.get_telnet_server_tests())
        all_tests.extend(self.get_telnet_configuration_tests())
        all_tests.extend(self.get_telnet_sessions_tests())
        all_tests.extend(self.get_telnet_security_tests())
        return all_tests
    
    def get_telnet_server_tests(self) -> List[APITestCase]:
        """Telnet Server API 測試案例"""
        return [
            # 獲取Telnet服務器信息
            self.create_test_case(
                name="telnet_get_server_info",
                method="GET",
                url="/api/v1/telnet",
                category="telnet_server",
                module="telnet",
                description="獲取Telnet服務器信息"
            ),
            
            # 啟用Telnet服務器 - 基本配置
            self.create_test_case(
                name="telnet_enable_server_basic",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_server",
                module="telnet",
                body=self.test_data.get('telnet_basic_config', {
                    "telnetStatus": True,
                    "telnetPort": 23,
                    "maxSessions": 8,
                    "timeOut": 600
                }),
                description="啟用Telnet服務器 - 基本配置"
            ),
            
            # 啟用Telnet服務器 - 僅啟用狀態
            self.create_test_case(
                name="telnet_enable_server_only",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_server",
                module="telnet",
                body=self.test_data.get('telnet_enable_only', {
                    "telnetStatus": True
                }),
                description="啟用Telnet服務器 - 僅啟用狀態"
            ),
            
            # 禁用Telnet服務器
            self.create_test_case(
                name="telnet_disable_server",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_server",
                module="telnet",
                body=self.test_data.get('telnet_disable_server', {
                    "telnetStatus": False
                }),
                description="禁用Telnet服務器"
            ),
            
            # 重新啟用Telnet服務器
            self.create_test_case(
                name="telnet_re_enable_server",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_server",
                module="telnet",
                body=self.test_data.get('telnet_re_enable', {
                    "telnetStatus": True,
                    "telnetPort": 23,
                    "maxSessions": 5,
                    "timeOut": 300
                }),
                description="重新啟用Telnet服務器"
            ),
            
            # 驗證Telnet服務器狀態
            self.create_test_case(
                name="telnet_verify_server_status",
                method="GET",
                url="/api/v1/telnet",
                category="telnet_server",
                module="telnet",
                description="驗證Telnet服務器狀態"
            )
        ]
    
    def get_telnet_configuration_tests(self) -> List[APITestCase]:
        """Telnet Configuration API 測試案例"""
        return [
            # 配置Telnet端口 - 默認端口
            self.create_test_case(
                name="telnet_configure_default_port",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_configuration",
                module="telnet",
                body=self.test_data.get('telnet_default_port', {
                    "telnetStatus": True,
                    "telnetPort": 23
                }),
                description="配置Telnet端口 - 默認端口 (23)"
            ),
            
            # 配置Telnet端口 - 自定義端口
            self.create_test_case(
                name="telnet_configure_custom_port",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_configuration",
                module="telnet",
                body=self.test_data.get('telnet_custom_port', {
                    "telnetStatus": True,
                    "telnetPort": 2323
                }),
                description="配置Telnet端口 - 自定義端口 (2323)"
            ),
            
            # 配置Telnet端口 - 最小端口
            self.create_test_case(
                name="telnet_configure_min_port",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_configuration",
                module="telnet",
                body=self.test_data.get('telnet_min_port', {
                    "telnetStatus": True,
                    "telnetPort": 1
                }),
                description="配置Telnet端口 - 最小端口 (1)"
            ),
            
            # 配置Telnet端口 - 最大端口
            self.create_test_case(
                name="telnet_configure_max_port",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_configuration",
                module="telnet",
                body=self.test_data.get('telnet_max_port', {
                    "telnetStatus": True,
                    "telnetPort": 65535
                }),
                description="配置Telnet端口 - 最大端口 (65535)"
            ),
            
            # 配置超時 - 最小值
            self.create_test_case(
                name="telnet_configure_min_timeout",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_configuration",
                module="telnet",
                body=self.test_data.get('telnet_min_timeout', {
                    "telnetStatus": True,
                    "timeOut": 60
                }),
                description="配置Telnet超時 - 最小值 (60秒)"
            ),
            
            # 配置超時 - 最大值
            self.create_test_case(
                name="telnet_configure_max_timeout",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_configuration",
                module="telnet",
                body=self.test_data.get('telnet_max_timeout', {
                    "telnetStatus": True,
                    "timeOut": 65535
                }),
                description="配置Telnet超時 - 最大值 (65535秒)"
            ),
            
            # 配置超時 - 默認值
            self.create_test_case(
                name="telnet_configure_default_timeout",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_configuration",
                module="telnet",
                body=self.test_data.get('telnet_default_timeout', {
                    "telnetStatus": True,
                    "timeOut": 600
                }),
                description="配置Telnet超時 - 默認值 (600秒)"
            ),
            
            # 配置自定義超時
            self.create_test_case(
                name="telnet_configure_custom_timeout",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_configuration",
                module="telnet",
                body=self.test_data.get('telnet_custom_timeout', {
                    "telnetStatus": True,
                    "timeOut": 800
                }),
                description="配置Telnet超時 - 自定義值 (800秒)"
            ),
            
            # 測試無效端口 - 超出範圍
            self.create_test_case(
                name="telnet_test_invalid_port_high",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_configuration",
                module="telnet",
                body=self.test_data.get('telnet_invalid_port_high', {
                    "telnetStatus": True,
                    "telnetPort": 70000  # 超出範圍 1-65535
                }),
                expected_status=400,
                description="測試無效端口 - 超出上限"
            ),
            
            # 測試無效端口 - 低於範圍
            self.create_test_case(
                name="telnet_test_invalid_port_low",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_configuration",
                module="telnet",
                body=self.test_data.get('telnet_invalid_port_low', {
                    "telnetStatus": True,
                    "telnetPort": 0  # 低於範圍 1-65535
                }),
                expected_status=400,
                description="測試無效端口 - 低於下限"
            ),
            
            # 測試無效超時 - 低於最小值
            self.create_test_case(
                name="telnet_test_invalid_timeout_low",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_configuration",
                module="telnet",
                body=self.test_data.get('telnet_invalid_timeout_low', {
                    "telnetStatus": True,
                    "timeOut": 30  # 低於範圍 60-65535
                }),
                expected_status=400,
                description="測試無效超時 - 低於最小值"
            ),
            
            # 測試無效超時 - 超過最大值
            self.create_test_case(
                name="telnet_test_invalid_timeout_high",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_configuration",
                module="telnet",
                body=self.test_data.get('telnet_invalid_timeout_high', {
                    "telnetStatus": True,
                    "timeOut": 70000  # 超出範圍 60-65535
                }),
                expected_status=400,
                description="測試無效超時 - 超過最大值"
            ),
            
            # 驗證配置更新
            self.create_test_case(
                name="telnet_verify_configuration_update",
                method="GET",
                url="/api/v1/telnet",
                category="telnet_configuration",
                module="telnet",
                description="驗證Telnet配置更新"
            )
        ]
    
    def get_telnet_sessions_tests(self) -> List[APITestCase]:
        """Telnet Sessions API 測試案例"""
        return [
            # 配置最大會話數 - 最小值
            self.create_test_case(
                name="telnet_configure_min_sessions",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_sessions",
                module="telnet",
                body=self.test_data.get('telnet_min_sessions', {
                    "telnetStatus": True,
                    "maxSessions": 0
                }),
                description="配置最大會話數 - 最小值 (0)"
            ),
            
            # 配置最大會話數 - 單會話
            self.create_test_case(
                name="telnet_configure_single_session",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_sessions",
                module="telnet",
                body=self.test_data.get('telnet_single_session', {
                    "telnetStatus": True,
                    "maxSessions": 1
                }),
                description="配置最大會話數 - 單會話 (1)"
            ),
            
            # 配置最大會話數 - 中等值
            self.create_test_case(
                name="telnet_configure_medium_sessions",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_sessions",
                module="telnet",
                body=self.test_data.get('telnet_medium_sessions', {
                    "telnetStatus": True,
                    "maxSessions": 4
                }),
                description="配置最大會話數 - 中等值 (4)"
            ),
            
            # 配置最大會話數 - 最大值
            self.create_test_case(
                name="telnet_configure_max_sessions",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_sessions",
                module="telnet",
                body=self.test_data.get('telnet_max_sessions', {
                    "telnetStatus": True,
                    "maxSessions": 8
                }),
                description="配置最大會話數 - 最大值 (8)"
            ),
            
            # 測試無效會話數 - 超出範圍
            self.create_test_case(
                name="telnet_test_invalid_sessions_high",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_sessions",
                module="telnet",
                body=self.test_data.get('telnet_invalid_sessions_high', {
                    "telnetStatus": True,
                    "maxSessions": 10  # 超出範圍 0-8
                }),
                expected_status=400,
                description="測試無效會話數 - 超出範圍"
            ),
            
            # 測試無效會話數 - 負值
            self.create_test_case(
                name="telnet_test_invalid_sessions_negative",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_sessions",
                module="telnet",
                body=self.test_data.get('telnet_invalid_sessions_negative', {
                    "telnetStatus": True,
                    "maxSessions": -1  # 負值
                }),
                expected_status=400,
                description="測試無效會話數 - 負值"
            ),
            
            # 驗證會話配置
            self.create_test_case(
                name="telnet_verify_session_configuration",
                method="GET",
                url="/api/v1/telnet",
                category="telnet_sessions",
                module="telnet",
                description="驗證Telnet會話配置"
            )
        ]
    
    def get_telnet_security_tests(self) -> List[APITestCase]:
        """Telnet Security API 測試案例"""
        return [
            # 安全配置 - 限制會話和超時
            self.create_test_case(
                name="telnet_security_restricted_config",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_security",
                module="telnet",
                body=self.test_data.get('telnet_security_restricted', {
                    "telnetStatus": True,
                    "telnetPort": 23,
                    "maxSessions": 2,
                    "timeOut": 300
                }),
                description="安全配置 - 限制會話和超時"
            ),
            
            # 安全配置 - 自定義端口
            self.create_test_case(
                name="telnet_security_custom_port",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_security",
                module="telnet",
                body=self.test_data.get('telnet_security_custom_port', {
                    "telnetStatus": True,
                    "telnetPort": 2323,
                    "maxSessions": 3,
                    "timeOut": 180
                }),
                description="安全配置 - 自定義端口"
            ),
            
            # 安全配置 - 短超時
            self.create_test_case(
                name="telnet_security_short_timeout",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_security",
                module="telnet",
                body=self.test_data.get('telnet_security_short_timeout', {
                    "telnetStatus": True,
                    "telnetPort": 23,
                    "maxSessions": 5,
                    "timeOut": 120
                }),
                description="安全配置 - 短超時"
            ),
            
            # 安全配置 - 禁用Telnet（最安全）
            self.create_test_case(
                name="telnet_security_disable_service",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_security",
                module="telnet",
                body=self.test_data.get('telnet_security_disable', {
                    "telnetStatus": False
                }),
                description="安全配置 - 禁用Telnet服務"
            ),
            
            # 完整安全配置測試
            self.create_test_case(
                name="telnet_complete_security_config",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_security",
                module="telnet",
                body=self.test_data.get('telnet_complete_security', {
                    "telnetStatus": True,
                    "telnetPort": 2323,
                    "maxSessions": 2,
                    "timeOut": 300
                }),
                description="完整安全配置測試"
            ),
            
            # 恢復默認配置
            self.create_test_case(
                name="telnet_restore_default_config",
                method="PUT",
                url="/api/v1/telnet",
                category="telnet_security",
                module="telnet",
                body=self.test_data.get('telnet_restore_default', {
                    "telnetStatus": True,
                    "telnetPort": 23,
                    "maxSessions": 8,
                    "timeOut": 600
                }),
                description="恢復Telnet默認配置"
            ),
            
            # 驗證安全配置效果
            self.create_test_case(
                name="telnet_verify_security_config",
                method="GET",
                url="/api/v1/telnet",
                category="telnet_security",
                module="telnet",
                description="驗證Telnet安全配置效果"
            )
        ]