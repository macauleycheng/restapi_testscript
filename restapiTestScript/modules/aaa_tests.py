#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AAA 模組測試案例
包含AAA會計更新、方法配置、服務器組管理、授權配置、會計配置、統計信息等相關API測試
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class AAATests(BaseTests):
    """AAA 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取AAA模組支援的類別"""
        return [
            "aaa_periodic_updates",
            "aaa_methods",
            "aaa_server_groups",
            "aaa_authorization",
            "aaa_accounting_dot1x",
            "aaa_accounting_commands",
            "aaa_accounting_exec",
            "aaa_statistics"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有AAA測試案例"""
        all_tests = []
        all_tests.extend(self.get_aaa_periodic_updates_tests())
        all_tests.extend(self.get_aaa_methods_tests())
        all_tests.extend(self.get_aaa_server_groups_tests())
        all_tests.extend(self.get_aaa_authorization_tests())
        all_tests.extend(self.get_aaa_accounting_dot1x_tests())
        all_tests.extend(self.get_aaa_accounting_commands_tests())
        all_tests.extend(self.get_aaa_accounting_exec_tests())
        all_tests.extend(self.get_aaa_statistics_tests())
        return all_tests
    
    def get_aaa_periodic_updates_tests(self) -> List[APITestCase]:
        """AAA Periodic Updates API 測試案例"""
        return [
            # 獲取AAA定期更新配置
            self.create_test_case(
                name="aaa_get_periodic_updates_config",
                method="GET",
                url="/api/v1/security/aaa",
                category="aaa_periodic_updates",
                module="aaa",
                description="獲取AAA定期更新配置"
            ),
            
            # 設置AAA定期更新 - 默認值
            self.create_test_case(
                name="aaa_set_periodic_updates_default",
                method="PUT",
                url="/api/v1/security/aaa",
                category="aaa_periodic_updates",
                module="aaa",
                body=self.test_data.get('aaa_periodic_updates_default', {
                    "update": 1
                }),
                description="設置AAA定期更新 - 默認值 (1分鐘)"
            ),
            
            # 設置AAA定期更新 - 自定義值
            self.create_test_case(
                name="aaa_set_periodic_updates_custom",
                method="PUT",
                url="/api/v1/security/aaa",
                category="aaa_periodic_updates",
                module="aaa",
                body=self.test_data.get('aaa_periodic_updates_custom', {
                    "update": 5
                }),
                description="設置AAA定期更新 - 自定義值 (5分鐘)"
            ),
            
            # 設置AAA定期更新 - 最大值
            self.create_test_case(
                name="aaa_set_periodic_updates_max",
                method="PUT",
                url="/api/v1/security/aaa",
                category="aaa_periodic_updates",
                module="aaa",
                body=self.test_data.get('aaa_periodic_updates_max', {
                    "update": 2147483647
                }),
                description="設置AAA定期更新 - 最大值"
            ),
            
            # 禁用AAA定期更新
            self.create_test_case(
                name="aaa_disable_periodic_updates",
                method="PUT",
                url="/api/v1/security/aaa",
                category="aaa_periodic_updates",
                module="aaa",
                body=self.test_data.get('aaa_periodic_updates_disable', {
                    "update": 0
                }),
                description="禁用AAA定期更新 (0分鐘)"
            ),
            
            # 重新啟用AAA定期更新
            self.create_test_case(
                name="aaa_re_enable_periodic_updates",
                method="PUT",
                url="/api/v1/security/aaa",
                category="aaa_periodic_updates",
                module="aaa",
                body=self.test_data.get('aaa_periodic_updates_re_enable', {
                    "update": 10
                }),
                description="重新啟用AAA定期更新 (10分鐘)"
            ),
            
            # 驗證定期更新配置
            self.create_test_case(
                name="aaa_verify_periodic_updates_config",
                method="GET",
                url="/api/v1/security/aaa",
                category="aaa_periodic_updates",
                module="aaa",
                description="驗證AAA定期更新配置"
            )
        ]
    
    def get_aaa_methods_tests(self) -> List[APITestCase]:
        """AAA Methods API 測試案例"""
        return [
            # 獲取所有AAA方法配置
            self.create_test_case(
                name="aaa_get_all_methods",
                method="GET",
                url="/api/v1/security/aaa/method",
                category="aaa_methods",
                module="aaa",
                description="獲取所有AAA方法配置"
            ),
            
            # 啟用802.1X會計方法 - RADIUS
            self.create_test_case(
                name="aaa_enable_dot1x_accounting_radius",
                method="POST",
                url="/api/v1/security/aaa/method",
                category="aaa_methods",
                module="aaa",
                body=self.test_data.get('aaa_dot1x_radius_method', {
                    "clientType": "dot1x",
                    "name": "default",
                    "groupName": "radius"
                }),
                description="啟用802.1X會計方法 - RADIUS"
            ),
            
            # 啟用802.1X會計方法 - 自定義組
            self.create_test_case(
                name="aaa_enable_dot1x_accounting_custom",
                method="POST",
                url="/api/v1/security/aaa/method",
                category="aaa_methods",
                module="aaa",
                body=self.test_data.get('aaa_dot1x_custom_method', {
                    "clientType": "dot1x",
                    "name": "default",
                    "groupName": "tps"
                }),
                description="啟用802.1X會計方法 - 自定義組"
            ),
            
            # 啟用EXEC會計方法 - TACACS+
            self.create_test_case(
                name="aaa_enable_exec_accounting_tacacs",
                method="POST",
                url="/api/v1/security/aaa/method",
                category="aaa_methods",
                module="aaa",
                body=self.test_data.get('aaa_exec_tacacs_method', {
                    "clientType": "exec",
                    "name": "default",
                    "groupName": "tacacs+"
                }),
                description="啟用EXEC會計方法 - TACACS+"
            ),
            
            # 啟用命令會計方法 - 特權級別1
            self.create_test_case(
                name="aaa_enable_commands_accounting_level1",
                method="POST",
                url="/api/v1/security/aaa/method",
                category="aaa_methods",
                module="aaa",
                body=self.test_data.get('aaa_commands_level1_method', {
                    "clientType": "commands",
                    "name": "default",
                    "groupName": "tacacs+",
                    "privilegeLevel": 1
                }),
                description="啟用命令會計方法 - 特權級別1"
            ),
            
            # 啟用命令會計方法 - 特權級別15
            self.create_test_case(
                name="aaa_enable_commands_accounting_level15",
                method="POST",
                url="/api/v1/security/aaa/method",
                category="aaa_methods",
                module="aaa",
                body=self.test_data.get('aaa_commands_level15_method', {
                    "clientType": "commands",
                    "name": "default",
                    "groupName": "radius",
                    "privilegeLevel": 15
                }),
                description="啟用命令會計方法 - 特權級別15"
            ),
            
            # 獲取特定會計方法 - 802.1X
            self.create_test_case(
                name="aaa_get_specific_dot1x_method",
                method="GET",
                url="/api/v1/security/aaa/method/{name}/client-types/{clientType}",
                category="aaa_methods",
                module="aaa",
                params={
                    "name": "default",
                    "clientType": "dot1x"
                },
                description="獲取特定會計方法 - 802.1X"
            ),
            
            # 獲取特定會計方法 - EXEC
            self.create_test_case(
                name="aaa_get_specific_exec_method",
                method="GET",
                url="/api/v1/security/aaa/method/{name}/client-types/{clientType}",
                category="aaa_methods",
                module="aaa",
                params={
                    "name": "default",
                    "clientType": "exec"
                },
                description="獲取特定會計方法 - EXEC"
            ),
            
            # 獲取特定會計方法 - 命令級別
            self.create_test_case(
                name="aaa_get_specific_commands_method",
                method="GET",
                url="/api/v1/security/aaa/method/{name}/client-types/{clientType}",
                category="aaa_methods",
                module="aaa",
                params={
                    "name": "default",
                    "clientType": "commands"
                },
                query_params={"privilegeLevel": "0"},
                description="獲取特定會計方法 - 命令級別0"
            ),
            
            # 禁用802.1X會計方法
            self.create_test_case(
                name="aaa_disable_dot1x_accounting",
                method="DELETE",
                url="/api/v1/security/aaa/method/{name}/client-types/{clientType}",
                category="aaa_methods",
                module="aaa",
                params={
                    "name": "tps",
                    "clientType": "dot1x"
                },
                description="禁用802.1X會計方法"
            ),
            
            # 禁用命令會計方法 - 帶特權級別
            self.create_test_case(
                name="aaa_disable_commands_accounting_with_privilege",
                method="DELETE",
                url="/api/v1/security/aaa/method/{name}/client-types/{clientType}",
                category="aaa_methods",
                module="aaa",
                params={
                    "name": "default",
                    "clientType": "commands"
                },
                body=self.test_data.get('aaa_commands_disable_privilege', {
                    "privilegeLevel": 1
                }),
                description="禁用命令會計方法 - 帶特權級別"
            ),
            
            # 測試無效客戶端類型
            self.create_test_case(
                name="aaa_test_invalid_client_type",
                method="POST",
                url="/api/v1/security/aaa/method",
                category="aaa_methods",
                module="aaa",
                body=self.test_data.get('aaa_invalid_client_type', {
                    "clientType": "invalid",
                    "name": "default",
                    "groupName": "radius"
                }),
                expected_status=400,
                description="測試無效客戶端類型"
            ),
            
            # 驗證方法配置更新
            self.create_test_case(
                name="aaa_verify_methods_config",
                method="GET",
                url="/api/v1/security/aaa/method",
                category="aaa_methods",
                module="aaa",
                description="驗證AAA方法配置更新"
            )
        ]
    
    def get_aaa_server_groups_tests(self) -> List[APITestCase]:
        """AAA Server Groups API 測試案例"""
        return [
            # 獲取所有服務器組信息
            self.create_test_case(
                name="aaa_get_all_server_groups",
                method="GET",
                url="/api/v1/security/aaa/groups",
                category="aaa_server_groups",
                module="aaa",
                description="獲取所有服務器組信息"
            ),
            
            # 創建RADIUS服務器組
            self.create_test_case(
                name="aaa_create_radius_server_group",
                method="POST",
                url="/api/v1/security/aaa/groups",
                category="aaa_server_groups",
                module="aaa",
                body=self.test_data.get('aaa_radius_server_group', {
                    "serverGroupType": "radius",
                    "groupName": "tps",
                    "servers": [
                        {
                            "authServerIndex": 1
                        }
                    ]
                }),
                description="創建RADIUS服務器組"
            ),
            
            # 創建TACACS+服務器組
            self.create_test_case(
                name="aaa_create_tacacs_server_group",
                method="POST",
                url="/api/v1/security/aaa/groups",
                category="aaa_server_groups",
                module="aaa",
                body=self.test_data.get('aaa_tacacs_server_group', {
                    "serverGroupType": "tacacs+",
                    "groupName": "tacacs_group",
                    "servers": [
                        {
                            "authServerIndex": 1
                        }
                    ]
                }),
                description="創建TACACS+服務器組"
            ),
            
            # 創建空服務器組
            self.create_test_case(
                name="aaa_create_empty_server_group",
                method="POST",
                url="/api/v1/security/aaa/groups",
                category="aaa_server_groups",
                module="aaa",
                body=self.test_data.get('aaa_empty_server_group', {
                    "serverGroupType": "radius",
                    "groupName": "empty_group",
                    "servers": []
                }),
                description="創建空服務器組"
            ),
            
            # 創建多服務器RADIUS組
            self.create_test_case(
                name="aaa_create_multi_radius_server_group",
                method="POST",
                url="/api/v1/security/aaa/groups",
                category="aaa_server_groups",
                module="aaa",
                body=self.test_data.get('aaa_multi_radius_server_group', {
                    "serverGroupType": "radius",
                    "groupName": "multi_radius",
                    "servers": [
                        {"authServerIndex": 1},
                        {"authServerIndex": 2},
                        {"authServerIndex": 3}
                    ]
                }),
                description="創建多服務器RADIUS組"
            ),
            
            # 獲取特定服務器組信息
            self.create_test_case(
                name="aaa_get_specific_server_group",
                method="GET",
                url="/api/v1/security/aaa/groups/{groupName}/server-group-types/{serverGroupType}",
                category="aaa_server_groups",
                module="aaa",
                params={
                    "groupName": "tps",
                    "serverGroupType": "radius"
                },
                description="獲取特定服務器組信息"
            ),
            
            # 修改服務器組 - 更新服務器列表
            self.create_test_case(
                name="aaa_modify_server_group_servers",
                method="PUT",
                url="/api/v1/security/aaa/groups/{groupName}/server-group-types/{serverGroupType}",
                category="aaa_server_groups",
                module="aaa",
                params={
                    "groupName": "tps",
                    "serverGroupType": "radius"
                },
                body=self.test_data.get('aaa_modify_server_group', {
                    "servers": [
                        {"authServerIndex": 2}
                    ]
                }),
                description="修改服務器組 - 更新服務器列表"
            ),
            
            # 修改服務器組 - 清空服務器
            self.create_test_case(
                name="aaa_modify_server_group_clear_servers",
                method="PUT",
                url="/api/v1/security/aaa/groups/{groupName}/server-group-types/{serverGroupType}",
                category="aaa_server_groups",
                module="aaa",
                params={
                    "groupName": "empty_group",
                    "serverGroupType": "radius"
                },
                body=self.test_data.get('aaa_clear_server_group', {
                    "servers": []
                }),
                description="修改服務器組 - 清空服務器"
            ),
            
            # 刪除服務器組
            self.create_test_case(
                name="aaa_delete_server_group",
                method="DELETE",
                url="/api/v1/security/aaa/groups/{groupName}/server-group-types/{serverGroupType}",
                category="aaa_server_groups",
                module="aaa",
                params={
                    "groupName": "tps",
                    "serverGroupType": "radius"
                },
                description="刪除服務器組"
            ),
            
            # 測試無效服務器組類型
            self.create_test_case(
                name="aaa_test_invalid_server_group_type",
                method="POST",
                url="/api/v1/security/aaa/groups",
                category="aaa_server_groups",
                module="aaa",
                body=self.test_data.get('aaa_invalid_server_group_type', {
                    "serverGroupType": "invalid",
                    "groupName": "test_group"
                }),
                expected_status=400,
                description="測試無效服務器組類型"
            ),
            
            # 測試無效服務器索引
            self.create_test_case(
                name="aaa_test_invalid_server_index",
                method="POST",
                url="/api/v1/security/aaa/groups",
                category="aaa_server_groups",
                module="aaa",
                body=self.test_data.get('aaa_invalid_server_index', {
                    "serverGroupType": "radius",
                    "groupName": "test_group",
                    "servers": [
                        {"authServerIndex": 10}  # 超出RADIUS範圍 1-5
                    ]
                }),
                expected_status=400,
                description="測試無效服務器索引"
            ),
            
            # 驗證服務器組配置
            self.create_test_case(
                name="aaa_verify_server_groups_config",
                method="GET",
                url="/api/v1/security/aaa/groups",
                category="aaa_server_groups",
                module="aaa",
                description="驗證服務器組配置"
            )
        ]
    
    def get_aaa_authorization_tests(self) -> List[APITestCase]:
        """AAA Authorization API 測試案例"""
        return [
            # 獲取所有EXEC授權配置
            self.create_test_case(
                name="aaa_get_all_authorization_exec",
                method="GET",
                url="/api/v1/security/aaa/authorization-exec",
                category="aaa_authorization",
                module="aaa",
                description="獲取所有EXEC授權配置"
            ),
            
            # 啟用EXEC授權 - 默認方法
            self.create_test_case(
                name="aaa_enable_authorization_exec_default",
                method="POST",
                url="/api/v1/security/aaa/authorization-exec",
                category="aaa_authorization",
                module="aaa",
                body=self.test_data.get('aaa_authorization_exec_default', {
                    "methodName": "default",
                    "groupName": "radius"
                }),
                description="啟用EXEC授權 - 默認方法"
            ),
            
            # 啟用EXEC授權 - 自定義方法
            self.create_test_case(
                name="aaa_enable_authorization_exec_custom",
                method="POST",
                url="/api/v1/security/aaa/authorization-exec",
                category="aaa_authorization",
                module="aaa",
                body=self.test_data.get('aaa_authorization_exec_custom', {
                    "methodName": "tps",
                    "groupName": "tacacs+"
                }),
                description="啟用EXEC授權 - 自定義方法"
            ),
            
            # 啟用EXEC授權 - 服務器組
            self.create_test_case(
                name="aaa_enable_authorization_exec_server_group",
                method="POST",
                url="/api/v1/security/aaa/authorization-exec",
                category="aaa_authorization",
                module="aaa",
                body=self.test_data.get('aaa_authorization_exec_server_group', {
                    "methodName": "custom_method",
                    "groupName": "custom_group"
                }),
                description="啟用EXEC授權 - 服務器組"
            ),
            
            # 獲取特定EXEC授權配置
            self.create_test_case(
                name="aaa_get_specific_authorization_exec",
                method="GET",
                url="/api/v1/security/aaa/authorization-exec/method-names/{methodName}",
                category="aaa_authorization",
                module="aaa",
                params={"methodName": "tps"},
                description="獲取特定EXEC授權配置"
            ),
            
            # 禁用EXEC授權
            self.create_test_case(
                name="aaa_disable_authorization_exec",
                method="DELETE",
                url="/api/v1/security/aaa/authorization-exec/method-names/{methodName}",
                category="aaa_authorization",
                module="aaa",
                params={"methodName": "tps"},
                description="禁用EXEC授權"
            ),
            
            # 測試無效方法名稱
            self.create_test_case(
                name="aaa_test_invalid_authorization_method_name",
                method="POST",
                url="/api/v1/security/aaa/authorization-exec",
                category="aaa_authorization",
                module="aaa",
                body=self.test_data.get('aaa_authorization_invalid_method', {
                    "methodName": "",  # 空方法名
                    "groupName": "radius"
                }),
                expected_status=400,
                description="測試無效授權方法名稱"
            ),
            
            # 驗證授權配置
            self.create_test_case(
                name="aaa_verify_authorization_config",
                method="GET",
                url="/api/v1/security/aaa/authorization-exec",
                category="aaa_authorization",
                module="aaa",
                description="驗證EXEC授權配置"
            )
        ]
    
    def get_aaa_accounting_dot1x_tests(self) -> List[APITestCase]:
        """AAA Accounting 802.1X API 測試案例"""
        return [
            # 獲取所有802.1X會計配置
            self.create_test_case(
                name="aaa_get_all_accounting_dot1x",
                method="GET",
                url="/api/v1/security/aaa/account-dot1x/interfaces",
                category="aaa_accounting_dot1x",
                module="aaa",
                description="獲取所有802.1X會計配置"
            ),
            
            # 應用802.1X會計方法到接口
            self.create_test_case(
                name="aaa_apply_accounting_dot1x_interface",
                method="POST",
                url="/api/v1/security/aaa/account-dot1x/interfaces",
                category="aaa_accounting_dot1x",
                module="aaa",
                body=self.test_data.get('aaa_accounting_dot1x_interface', {
                    "ifId": "eth1/1",
                    "methodName": "default"
                }),
                description="應用802.1X會計方法到接口"
            ),
            
            # 應用802.1X會計方法到多個接口
            self.create_test_case(
                name="aaa_apply_accounting_dot1x_multiple_interfaces",
                method="POST",
                url="/api/v1/security/aaa/account-dot1x/interfaces",
                category="aaa_accounting_dot1x",
                module="aaa",
                body=self.test_data.get('aaa_accounting_dot1x_interface2', {
                    "ifId": "eth1/2",
                    "methodName": "default"
                }),
                description="應用802.1X會計方法到多個接口"
            ),
            
            # 獲取特定接口802.1X會計配置
            self.create_test_case(
                name="aaa_get_specific_accounting_dot1x",
                method="GET",
                url="/api/v1/security/aaa/account-dot1x/interfaces/{ifId}",
                category="aaa_accounting_dot1x",
                module="aaa",
                params={"ifId": "eth1%2f1"},
                description="獲取特定接口802.1X會計配置"
            ),
            
            # 獲取參數化接口802.1X會計配置
            self.create_test_case(
                name="aaa_get_parameterized_accounting_dot1x",
                method="GET",
                url="/api/v1/security/aaa/account-dot1x/interfaces/{ifId}",
                category="aaa_accounting_dot1x",
                module="aaa",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                description=f"獲取接口 {self.params.get('interface_id', 'eth1/1')} 802.1X會計配置"
            ),
            
            # 禁用接口802.1X會計
            self.create_test_case(
                name="aaa_disable_accounting_dot1x_interface",
                method="DELETE",
                url="/api/v1/security/aaa/account-dot1x/interfaces/{ifId}",
                category="aaa_accounting_dot1x",
                module="aaa",
                params={"ifId": "eth1%2f1"},
                description="禁用接口802.1X會計"
            ),
            
            # 測試無效接口ID
            self.create_test_case(
                name="aaa_test_invalid_dot1x_interface_id",
                method="POST",
                url="/api/v1/security/aaa/account-dot1x/interfaces",
                category="aaa_accounting_dot1x",
                module="aaa",
                body=self.test_data.get('aaa_accounting_dot1x_invalid_interface', {
                    "ifId": "invalid-interface",
                    "methodName": "default"
                }),
                expected_status=400,
                description="測試無效802.1X會計接口ID"
            ),
            
            # 驗證802.1X會計配置
            self.create_test_case(
                name="aaa_verify_accounting_dot1x_config",
                method="GET",
                url="/api/v1/security/aaa/account-dot1x/interfaces",
                category="aaa_accounting_dot1x",
                module="aaa",
                description="驗證802.1X會計配置"
            )
        ]
    
    def get_aaa_accounting_commands_tests(self) -> List[APITestCase]:
        """AAA Accounting Commands API 測試案例"""
        return [
            # 獲取所有命令會計配置
            self.create_test_case(
                name="aaa_get_all_accounting_commands",
                method="GET",
                url="/api/v1/security/aaa/command-privileges/interfaces",
                category="aaa_accounting_commands",
                module="aaa",
                description="獲取所有命令會計配置"
            ),
            
            # 應用命令會計方法 - VTY級別0
            self.create_test_case(
                name="aaa_apply_accounting_commands_vty_level0",
                method="POST",
                url="/api/v1/security/aaa/command-privileges/interfaces",
                category="aaa_accounting_commands",
                module="aaa",
                body=self.test_data.get('aaa_accounting_commands_vty_level0', {
                    "level": 0,
                    "ifId": "vty",
                    "methodName": "default"
                }),
                description="應用命令會計方法 - VTY級別0"
            ),
            
            # 應用命令會計方法 - Console級別15
            self.create_test_case(
                name="aaa_apply_accounting_commands_console_level15",
                method="POST",
                url="/api/v1/security/aaa/command-privileges/interfaces",
                category="aaa_accounting_commands",
                module="aaa",
                body=self.test_data.get('aaa_accounting_commands_console_level15', {
                    "level": 15,
                    "ifId": "console",
                    "methodName": "default"
                }),
                description="應用命令會計方法 - Console級別15"
            ),
            
            # 應用命令會計方法 - 中等級別
            self.create_test_case(
                name="aaa_apply_accounting_commands_medium_level",
                method="POST",
                url="/api/v1/security/aaa/command-privileges/interfaces",
                category="aaa_accounting_commands",
                module="aaa",
                body=self.test_data.get('aaa_accounting_commands_medium_level', {
                    "level": 7,
                    "ifId": "vty",
                    "methodName": "default"
                }),
                description="應用命令會計方法 - 中等級別7"
            ),
            
            # 獲取特定命令會計配置
            self.create_test_case(
                name="aaa_get_specific_accounting_commands",
                method="GET",
                url="/api/v1/security/aaa/command-privileges/interfaces/{ifId}/levels/{level}",
                category="aaa_accounting_commands",
                module="aaa",
                params={
                    "ifId": "vty",
                    "level": "0"
                },
                description="獲取特定命令會計配置"
            ),
            
            # 獲取參數化命令會計配置
            self.create_test_case(
                name="aaa_get_parameterized_accounting_commands",
                method="GET",
                url="/api/v1/security/aaa/command-privileges/interfaces/{ifId}/levels/{level}",
                category="aaa_accounting_commands",
                module="aaa",
                params={
                    "ifId": self.params.get('line_type', 'vty'),
                    "level": str(self.params.get('privilege_level', 0))
                },
                description=f"獲取 {self.params.get('line_type', 'vty')} 級別 {self.params.get('privilege_level', 0)} 命令會計配置"
            ),
            
            # 禁用命令會計
            self.create_test_case(
                name="aaa_disable_accounting_commands",
                method="DELETE",
                url="/api/v1/security/aaa/command-privileges/interfaces/{ifId}/levels/{level}",
                category="aaa_accounting_commands",
                module="aaa",
                params={
                    "ifId": "vty",
                    "level": "0"
                },
                description="禁用命令會計"
            ),
            
            # 測試無效特權級別
            self.create_test_case(
                name="aaa_test_invalid_privilege_level",
                method="POST",
                url="/api/v1/security/aaa/command-privileges/interfaces",
                category="aaa_accounting_commands",
                module="aaa",
                body=self.test_data.get('aaa_accounting_commands_invalid_level', {
                    "level": 20,  # 超出範圍 0-15
                    "ifId": "vty",
                    "methodName": "default"
                }),
                expected_status=400,
                description="測試無效特權級別"
            ),
            
            # 測試無效線路類型
            self.create_test_case(
                name="aaa_test_invalid_line_type",
                method="POST",
                url="/api/v1/security/aaa/command-privileges/interfaces",
                category="aaa_accounting_commands",
                module="aaa",
                body=self.test_data.get('aaa_accounting_commands_invalid_line', {
                    "level": 0,
                    "ifId": "invalid-line",
                    "methodName": "default"
                }),
                expected_status=400,
                description="測試無效線路類型"
            ),
            
            # 驗證命令會計配置
            self.create_test_case(
                name="aaa_verify_accounting_commands_config",
                method="GET",
                url="/api/v1/security/aaa/command-privileges/interfaces",
                category="aaa_accounting_commands",
                module="aaa",
                description="驗證命令會計配置"
            )
        ]
    
    def get_aaa_accounting_exec_tests(self) -> List[APITestCase]:
        """AAA Accounting EXEC API 測試案例"""
        return [
            # 獲取所有EXEC會計配置
            self.create_test_case(
                name="aaa_get_all_accounting_exec",
                method="GET",
                url="/api/v1/security/aaa/exec/modes/{mode}/interfaces",
                category="aaa_accounting_exec",
                module="aaa",
                params={"mode": "accounting"},
                description="獲取所有EXEC會計配置"
            ),
            
            # 獲取所有EXEC授權配置
            self.create_test_case(
                name="aaa_get_all_exec_authorization",
                method="GET",
                url="/api/v1/security/aaa/exec/modes/{mode}/interfaces",
                category="aaa_accounting_exec",
                module="aaa",
                params={"mode": "authorization"},
                description="獲取所有EXEC授權配置"
            ),
            
            # 應用EXEC會計方法 - VTY
            self.create_test_case(
                name="aaa_apply_exec_accounting_vty",
                method="POST",
                url="/api/v1/security/aaa/exec/modes/{mode}/interfaces",
                category="aaa_accounting_exec",
                module="aaa",
                params={"mode": "accounting"},
                body=self.test_data.get('aaa_exec_accounting_vty', {
                    "ifId": "vty",
                    "methodName": "default"
                }),
                description="應用EXEC會計方法 - VTY"
            ),
            
            # 應用EXEC會計方法 - Console
            self.create_test_case(
                name="aaa_apply_exec_accounting_console",
                method="POST",
                url="/api/v1/security/aaa/exec/modes/{mode}/interfaces",
                category="aaa_accounting_exec",
                module="aaa",
                params={"mode": "accounting"},
                body=self.test_data.get('aaa_exec_accounting_console', {
                    "ifId": "console",
                    "methodName": "default"
                }),
                description="應用EXEC會計方法 - Console"
            ),
            
            # 應用EXEC授權方法 - VTY
            self.create_test_case(
                name="aaa_apply_exec_authorization_vty",
                method="POST",
                url="/api/v1/security/aaa/exec/modes/{mode}/interfaces",
                category="aaa_accounting_exec",
                module="aaa",
                params={"mode": "authorization"},
                body=self.test_data.get('aaa_exec_authorization_vty', {
                    "ifId": "vty",
                    "methodName": "tps"
                }),
                description="應用EXEC授權方法 - VTY"
            ),
            
            # 獲取特定EXEC會計配置
            self.create_test_case(
                name="aaa_get_specific_exec_accounting",
                method="GET",
                url="/api/v1/security/aaa/exec/modes/{mode}/interfaces/{ifId}",
                category="aaa_accounting_exec",
                module="aaa",
                params={
                    "mode": "accounting",
                    "ifId": "vty"
                },
                description="獲取特定EXEC會計配置"
            ),
            
            # 獲取特定EXEC授權配置
            self.create_test_case(
                name="aaa_get_specific_exec_authorization",
                method="GET",
                url="/api/v1/security/aaa/exec/modes/{mode}/interfaces/{ifId}",
                category="aaa_accounting_exec",
                module="aaa",
                params={
                    "mode": "authorization",
                    "ifId": "vty"
                },
                description="獲取特定EXEC授權配置"
            ),
            
            # 禁用EXEC會計
            self.create_test_case(
                name="aaa_disable_exec_accounting",
                method="DELETE",
                url="/api/v1/security/aaa/exec/modes/{mode}/interfaces/{ifId}",
                category="aaa_accounting_exec",
                module="aaa",
                params={
                    "mode": "accounting",
                    "ifId": "vty"
                },
                description="禁用EXEC會計"
            ),
            
            # 禁用EXEC授權
            self.create_test_case(
                name="aaa_disable_exec_authorization",
                method="DELETE",
                url="/api/v1/security/aaa/exec/modes/{mode}/interfaces/{ifId}",
                category="aaa_accounting_exec",
                module="aaa",
                params={
                    "mode": "authorization",
                    "ifId": "vty"
                },
                description="禁用EXEC授權"
            ),
            
            # 測試無效模式
            self.create_test_case(
                name="aaa_test_invalid_exec_mode",
                method="GET",
                url="/api/v1/security/aaa/exec/modes/{mode}/interfaces",
                category="aaa_accounting_exec",
                module="aaa",
                params={"mode": "invalid-mode"},
                expected_status=400,
                description="測試無效EXEC模式"
            ),
            
            # 驗證EXEC配置
            self.create_test_case(
                name="aaa_verify_exec_config",
                method="GET",
                url="/api/v1/security/aaa/exec/modes/{mode}/interfaces",
                category="aaa_accounting_exec",
                module="aaa",
                params={"mode": "accounting"},
                description="驗證EXEC會計配置"
            )
        ]
    
    def get_aaa_statistics_tests(self) -> List[APITestCase]:
        """AAA Statistics API 測試案例"""
        return [
            # 獲取所有會計統計信息
            self.create_test_case(
                name="aaa_get_all_account_statistics",
                method="GET",
                url="/api/v1/security/aaa/accounts/statistics",
                category="aaa_statistics",
                module="aaa",
                description="獲取所有會計統計信息"
            ),
            
            # 獲取802.1X會計統計信息
            self.create_test_case(
                name="aaa_get_dot1x_account_statistics",
                method="GET",
                url="/api/v1/security/aaa/accounts/statistics",
                category="aaa_statistics",
                module="aaa",
                query_params={"type": "dot1x"},
                description="獲取802.1X會計統計信息"
            ),
            
            # 獲取EXEC會計統計信息
            self.create_test_case(
                name="aaa_get_exec_account_statistics",
                method="GET",
                url="/api/v1/security/aaa/accounts/statistics",
                category="aaa_statistics",
                module="aaa",
                query_params={"type": "exec"},
                description="獲取EXEC會計統計信息"
            ),
            
            # 監控統計信息變化
            self.create_test_case(
                name="aaa_monitor_statistics_changes",
                method="GET",
                url="/api/v1/security/aaa/accounts/statistics",
                category="aaa_statistics",
                module="aaa",
                description="監控AAA統計信息變化"
            ),
            
            # 測試無效統計類型
            self.create_test_case(
                name="aaa_test_invalid_statistics_type",
                method="GET",
                url="/api/v1/security/aaa/accounts/statistics",
                category="aaa_statistics",
                module="aaa",
                query_params={"type": "invalid-type"},
                expected_status=400,
                description="測試無效統計類型"
            )
        ]