#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SNMP 模組測試案例
包含SNMP服務器配置、社區管理、主機管理、接口配置、SNMPv3配置等相關API測試
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class SNMPTests(BaseTests):
    """SNMP 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取SNMP模組支援的類別"""
        return [
            "snmp_server",
            "snmp_communities",
            "snmp_hosts",
            "snmp_interfaces",
            "snmpv3_engine_ids",
            "snmpv3_groups",
            "snmpv3_users",
            "snmpv3_views",
            "snmp_notify"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有SNMP測試案例"""
        all_tests = []
        all_tests.extend(self.get_snmp_server_tests())
        all_tests.extend(self.get_snmp_communities_tests())
        all_tests.extend(self.get_snmp_hosts_tests())
        all_tests.extend(self.get_snmp_interfaces_tests())
        all_tests.extend(self.get_snmpv3_engine_ids_tests())
        all_tests.extend(self.get_snmpv3_groups_tests())
        all_tests.extend(self.get_snmpv3_users_tests())
        all_tests.extend(self.get_snmpv3_views_tests())
        all_tests.extend(self.get_snmp_notify_tests())
        return all_tests
    
    def get_snmp_server_tests(self) -> List[APITestCase]:
        """SNMP Server API 測試案例"""
        return [
            # 獲取SNMP服務器信息
            self.create_test_case(
                name="snmp_get_server_info",
                method="GET",
                url="/api/v1/snmp",
                category="snmp_server",
                module="snmp",
                description="獲取SNMP服務器配置信息"
            ),
            
            # 更新SNMP服務器基本配置
            self.create_test_case(
                name="snmp_update_basic_config",
                method="PUT",
                url="/api/v1/snmp",
                category="snmp_server",
                module="snmp",
                body=self.test_data.get('snmp_basic_config', {
                    "agentStatus": True,
                    "contact": "admin@company.com",
                    "location": "Data Center Room 1",
                    "authentication": True,
                    "linkUpDown": True
                }),
                description="更新SNMP服務器基本配置"
            ),
            
            # 啟用所有SNMP陷阱
            self.create_test_case(
                name="snmp_enable_all_traps",
                method="PUT",
                url="/api/v1/snmp",
                category="snmp_server",
                module="snmp",
                body=self.test_data.get('snmp_enable_all_traps', {
                    "agentStatus": True,
                    "contact": "network-admin@company.com",
                    "location": "Main Office",
                    "authentication": True,
                    "linkUpDown": True,
                    "ethernetCfm": True,
                    "macNotify": True,
                    "macNotifyInterval": 30
                }),
                description="啟用所有SNMP陷阱功能"
            ),
            
            # 配置MAC通知間隔
            self.create_test_case(
                name="snmp_configure_mac_notify_interval",
                method="PUT",
                url="/api/v1/snmp",
                category="snmp_server",
                module="snmp",
                body=self.test_data.get('snmp_mac_notify_config', {
                    "agentStatus": True,
                    "macNotify": True,
                    "macNotifyInterval": 60
                }),
                description="配置MAC通知間隔為60秒"
            ),
            
            # 禁用SNMP代理
            self.create_test_case(
                name="snmp_disable_agent",
                method="PUT",
                url="/api/v1/snmp",
                category="snmp_server",
                module="snmp",
                body=self.test_data.get('snmp_disable_agent', {
                    "agentStatus": False
                }),
                description="禁用SNMP代理"
            ),
            
            # 重新啟用SNMP代理
            self.create_test_case(
                name="snmp_re_enable_agent",
                method="PUT",
                url="/api/v1/snmp",
                category="snmp_server",
                module="snmp",
                body=self.test_data.get('snmp_re_enable_agent', {
                    "agentStatus": True,
                    "contact": "test@example.com",
                    "location": "Test Lab"
                }),
                description="重新啟用SNMP代理"
            )
        ]
    
    def get_snmp_communities_tests(self) -> List[APITestCase]:
        """SNMP Communities API 測試案例"""
        return [
            # 獲取所有SNMP社區
            self.create_test_case(
                name="snmp_get_all_communities",
                method="GET",
                url="/api/v1/snmp/communities",
                category="snmp_communities",
                module="snmp",
                description="獲取所有SNMP社區"
            ),
            
            # 添加只讀社區
            self.create_test_case(
                name="snmp_add_readonly_community",
                method="POST",
                url="/api/v1/snmp/communities",
                category="snmp_communities",
                module="snmp",
                body=self.test_data.get('snmp_readonly_community', {
                    "communityName": "readonly",
                    "accessLevel": "read-only"
                }),
                description="添加只讀SNMP社區"
            ),
            
            # 添加讀寫社區
            self.create_test_case(
                name="snmp_add_readwrite_community",
                method="POST",
                url="/api/v1/snmp/communities",
                category="snmp_communities",
                module="snmp",
                body=self.test_data.get('snmp_readwrite_community', {
                    "communityName": "readwrite",
                    "accessLevel": "read/write"
                }),
                description="添加讀寫SNMP社區"
            ),
            
            # 添加測試社區
            self.create_test_case(
                name="snmp_add_test_community",
                method="POST",
                url="/api/v1/snmp/communities",
                category="snmp_communities",
                module="snmp",
                body=self.test_data.get('snmp_test_community', {
                    "communityName": "testcommunity",
                    "accessLevel": "read-only"
                }),
                description="添加測試SNMP社區"
            ),
            
            # 獲取特定社區 - public
            self.create_test_case(
                name="snmp_get_public_community",
                method="GET",
                url="/api/v1/snmp/communities/{communityName}",
                category="snmp_communities",
                module="snmp",
                params={"communityName": "public"},
                description="獲取public社區信息"
            ),
            
            # 獲取特定社區 - readonly
            self.create_test_case(
                name="snmp_get_readonly_community",
                method="GET",
                url="/api/v1/snmp/communities/{communityName}",
                category="snmp_communities",
                module="snmp",
                params={"communityName": "readonly"},
                description="獲取readonly社區信息"
            ),
            
            # 獲取參數化社區
            self.create_test_case(
                name="snmp_get_parameterized_community",
                method="GET",
                url="/api/v1/snmp/communities/{communityName}",
                category="snmp_communities",
                module="snmp",
                params={"communityName": self.params.get('community_name', 'public')},
                description=f"獲取社區 {self.params.get('community_name', 'public')} 信息"
            ),
            
            # 刪除測試社區
            self.create_test_case(
                name="snmp_delete_test_community",
                method="DELETE",
                url="/api/v1/snmp/communities/{communityName}",
                category="snmp_communities",
                module="snmp",
                params={"communityName": "testcommunity"},
                description="刪除測試SNMP社區"
            ),
            
            # 測試獲取不存在的社區
            self.create_test_case(
                name="snmp_get_nonexistent_community",
                method="GET",
                url="/api/v1/snmp/communities/{communityName}",
                category="snmp_communities",
                module="snmp",
                params={"communityName": "nonexistent"},
                expected_status=404,
                description="測試獲取不存在的社區"
            )
        ]
    
    def get_snmp_hosts_tests(self) -> List[APITestCase]:
        """SNMP Hosts API 測試案例"""
        return [
            # 獲取所有SNMP陷阱主機
            self.create_test_case(
                name="snmp_get_all_trap_hosts",
                method="GET",
                url="/api/v1/snmp/hosts",
                category="snmp_hosts",
                module="snmp",
                description="獲取所有SNMP陷阱主機"
            ),
            
            # 添加SNMPv1陷阱主機
            self.create_test_case(
                name="snmp_add_v1_trap_host",
                method="POST",
                url="/api/v1/snmp/hosts",
                category="snmp_hosts",
                module="snmp",
                body=self.test_data.get('snmp_v1_trap_host', {
                    "ip": "192.168.1.100",
                    "inform": False,
                    "retryCount": 3,
                    "timeout": 1500,
                    "communityName": "public",
                    "securityModel": "v1",
                    "udpPort": 162
                }),
                description="添加SNMPv1陷阱主機"
            ),
            
            # 添加SNMPv2陷阱主機
            self.create_test_case(
                name="snmp_add_v2_trap_host",
                method="POST",
                url="/api/v1/snmp/hosts",
                category="snmp_hosts",
                module="snmp",
                body=self.test_data.get('snmp_v2_trap_host', {
                    "ip": "192.168.1.101",
                    "inform": True,
                    "retryCount": 5,
                    "timeout": 2000,
                    "communityName": "readonly",
                    "securityModel": "v2",
                    "udpPort": 162
                }),
                description="添加SNMPv2陷阱主機"
            ),
            
            # 添加SNMPv3陷阱主機
            self.create_test_case(
                name="snmp_add_v3_trap_host",
                method="POST",
                url="/api/v1/snmp/hosts",
                category="snmp_hosts",
                module="snmp",
                body=self.test_data.get('snmp_v3_trap_host', {
                    "ip": "192.168.1.102",
                    "inform": True,
                    "retryCount": 3,
                    "timeout": 1600,
                    "communityName": "testuser",
                    "securityModel": "v3",
                    "securityLevel": "auth",
                    "udpPort": 162
                }),
                description="添加SNMPv3陷阱主機"
            ),
            
            # 獲取特定陷阱主機
            self.create_test_case(
                name="snmp_get_specific_trap_host",
                method="GET",
                url="/api/v1/snmp/hosts/{ip}",
                category="snmp_hosts",
                module="snmp",
                params={"ip": "192.168.1.100"},
                description="獲取特定陷阱主機信息"
            ),
            
            # 獲取參數化陷阱主機
            self.create_test_case(
                name="snmp_get_parameterized_trap_host",
                method="GET",
                url="/api/v1/snmp/hosts/{ip}",
                category="snmp_hosts",
                module="snmp",
                params={"ip": self.params.get('trap_host_ip', '192.168.1.101')},
                description=f"獲取陷阱主機 {self.params.get('trap_host_ip', '192.168.1.101')} 信息"
            ),
            
            # 刪除陷阱主機
            self.create_test_case(
                name="snmp_delete_trap_host",
                method="DELETE",
                url="/api/v1/snmp/hosts/{ip}",
                category="snmp_hosts",
                module="snmp",
                params={"ip": "192.168.1.102"},
                description="刪除SNMP陷阱主機"
            ),
            
            # 測試無效IP地址
            self.create_test_case(
                name="snmp_test_invalid_trap_host_ip",
                method="POST",
                url="/api/v1/snmp/hosts",
                category="snmp_hosts",
                module="snmp",
                body=self.test_data.get('snmp_invalid_ip_host', {
                    "ip": "999.999.999.999",
                    "communityName": "public",
                    "securityModel": "v1"
                }),
                expected_status=400,
                description="測試添加無效IP地址的陷阱主機"
            )
        ]
    
    def get_snmp_interfaces_tests(self) -> List[APITestCase]:
        """SNMP Interfaces API 測試案例"""
        return [
            # 獲取所有接口SNMP端口陷阱狀態
            self.create_test_case(
                name="snmp_get_all_interfaces_trap_status",
                method="GET",
                url="/api/v1/snmp/interfaces",
                category="snmp_interfaces",
                module="snmp",
                description="獲取所有接口SNMP端口陷阱狀態"
            ),
            
            # 獲取特定接口陷阱狀態 - eth1/1
            self.create_test_case(
                name="snmp_get_interface_eth1_1_trap_status",
                method="GET",
                url="/api/v1/snmp/interfaces/{ifId}",
                category="snmp_interfaces",
                module="snmp",
                params={"ifId": "eth1%2f1"},
                description="獲取接口 eth1/1 SNMP陷阱狀態"
            ),
            
            # 獲取特定接口陷阱狀態 - eth1/2
            self.create_test_case(
                name="snmp_get_interface_eth1_2_trap_status",
                method="GET",
                url="/api/v1/snmp/interfaces/{ifId}",
                category="snmp_interfaces",
                module="snmp",
                params={"ifId": "eth1%2f2"},
                description="獲取接口 eth1/2 SNMP陷阱狀態"
            ),
            
            # 啟用接口MAC認證陷阱
            self.create_test_case(
                name="snmp_enable_interface_mac_trap",
                method="PUT",
                url="/api/v1/snmp/interfaces/{ifId}",
                category="snmp_interfaces",
                module="snmp",
                params={"ifId": "eth1%2f1"},
                body=self.test_data.get('snmp_enable_mac_trap', {
                    "macNotify": True
                }),
                description="啟用接口 eth1/1 MAC認證陷阱"
            ),
            
            # 禁用接口MAC認證陷阱
            self.create_test_case(
                name="snmp_disable_interface_mac_trap",
                method="PUT",
                url="/api/v1/snmp/interfaces/{ifId}",
                category="snmp_interfaces",
                module="snmp",
                params={"ifId": "eth1%2f2"},
                body=self.test_data.get('snmp_disable_mac_trap', {
                    "macNotify": False
                }),
                description="禁用接口 eth1/2 MAC認證陷阱"
            ),
            
            # 配置參數化接口陷阱
            self.create_test_case(
                name="snmp_configure_parameterized_interface_trap",
                method="PUT",
                url="/api/v1/snmp/interfaces/{ifId}",
                category="snmp_interfaces",
                module="snmp",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                body=self.test_data.get('snmp_param_interface_trap', {
                    "macNotify": True
                }),
                description=f"配置接口 {self.params.get('interface_id', 'eth1/1')} SNMP陷阱"
            )
        ]
    
    def get_snmpv3_engine_ids_tests(self) -> List[APITestCase]:
        """SNMPv3 Engine IDs API 測試案例"""
        return [
            # 獲取本地引擎ID
            self.create_test_case(
                name="snmpv3_get_local_engine_id",
                method="GET",
                url="/api/v1/snmpv3/engine-ids/local",
                category="snmpv3_engine_ids",
                module="snmp",
                description="獲取SNMPv3本地引擎ID"
            ),
            
            # 更新本地引擎ID
            self.create_test_case(
                name="snmpv3_update_local_engine_id",
                method="PUT",
                url="/api/v1/snmpv3/engine-ids/local",
                category="snmpv3_engine_ids",
                module="snmp",
                body=self.test_data.get('snmpv3_local_engine_id', {
                    "engineId": "8000010303A82BB5893A600012"
                }),
                description="更新SNMPv3本地引擎ID"
            ),
            
            # 獲取所有遠程引擎ID
            self.create_test_case(
                name="snmpv3_get_all_remote_engine_ids",
                method="GET",
                url="/api/v1/snmpv3/engine-ids/remote",
                category="snmpv3_engine_ids",
                module="snmp",
                description="獲取所有SNMPv3遠程引擎ID"
            ),
            
            # 添加遠程引擎ID
            self.create_test_case(
                name="snmpv3_add_remote_engine_id",
                method="POST",
                url="/api/v1/snmpv3/engine-ids/remote",
                category="snmpv3_engine_ids",
                module="snmp",
                body=self.test_data.get('snmpv3_remote_engine_id', {
                    "engineIp": "192.168.1.19",
                    "engineId": "8000010303A82BB5893A600000"
                }),
                description="添加SNMPv3遠程引擎ID"
            ),
            
            # 獲取特定遠程引擎
            self.create_test_case(
                name="snmpv3_get_specific_remote_engine",
                method="GET",
                url="/api/v1/snmpv3/engine-ids/remote/{engineIp}",
                category="snmpv3_engine_ids",
                module="snmp",
                params={"engineIp": "192.168.1.19"},
                description="獲取特定SNMPv3遠程引擎"
            ),
            
            # 刪除遠程引擎ID
            self.create_test_case(
                name="snmpv3_delete_remote_engine_id",
                method="DELETE",
                url="/api/v1/snmpv3/engine-ids/remote/{engineIp}",
                category="snmpv3_engine_ids",
                module="snmp",
                params={"engineIp": "192.168.1.19"},
                description="刪除SNMPv3遠程引擎ID"
            )
        ]
    
    def get_snmpv3_groups_tests(self) -> List[APITestCase]:
        """SNMPv3 Groups API 測試案例"""
        return [
            # 獲取所有SNMP組
            self.create_test_case(
                name="snmpv3_get_all_groups",
                method="GET",
                url="/api/v1/snmpv3/groups",
                category="snmpv3_groups",
                module="snmp",
                description="獲取所有SNMPv3組"
            ),
            
            # 添加SNMPv2組
            self.create_test_case(
                name="snmpv3_add_v2_group",
                method="POST",
                url="/api/v1/snmpv3/groups",
                category="snmpv3_groups",
                module="snmp",
                body=self.test_data.get('snmpv3_v2_group', {
                    "groupName": "v2group",
                    "securityModel": "v2",
                    "readView": "defaultview",
                    "writeView": "writeview"
                }),
                description="添加SNMPv2組"
            ),
            
            # 添加SNMPv3組 - 認證模式
            self.create_test_case(
                name="snmpv3_add_v3_auth_group",
                method="POST",
                url="/api/v1/snmpv3/groups",
                category="snmpv3_groups",
                module="snmp",
                body=self.test_data.get('snmpv3_v3_auth_group', {
                    "groupName": "v3authgroup",
                    "securityModel": "v3",
                    "securityLevel": "auth",
                    "readView": "defaultview",
                    "writeView": "writeview",
                    "notifyView": "notifyview"
                }),
                description="添加SNMPv3組 - 認證模式"
            ),
            
            # 添加SNMPv3組 - 隱私模式
            self.create_test_case(
                name="snmpv3_add_v3_priv_group",
                method="POST",
                url="/api/v1/snmpv3/groups",
                category="snmpv3_groups",
                module="snmp",
                body=self.test_data.get('snmpv3_v3_priv_group', {
                    "groupName": "v3privgroup",
                    "securityModel": "v3",
                    "securityLevel": "priv",
                    "readView": "defaultview",
                    "writeView": "writeview",
                    "notifyView": "notifyview"
                }),
                description="添加SNMPv3組 - 隱私模式"
            ),
            
            # 獲取特定組 - v2
            self.create_test_case(
                name="snmpv3_get_v2_group",
                method="GET",
                url="/api/v1/snmpv3/groups/{groupName}/security-model/{securityModel}",
                category="snmpv3_groups",
                module="snmp",
                params={"groupName": "v2group", "securityModel": "v2"},
                description="獲取SNMPv2組信息"
            ),
            
            # 獲取特定組 - v3 auth
            self.create_test_case(
                name="snmpv3_get_v3_auth_group",
                method="GET",
                url="/api/v1/snmpv3/groups/{groupName}/security-model/{securityModel}",
                category="snmpv3_groups",
                module="snmp",
                params={"groupName": "v3authgroup", "securityModel": "v3"},
                query_params={"securityLevel": "auth"},
                description="獲取SNMPv3認證組信息"
            ),
            
            # 刪除SNMP組
            self.create_test_case(
                name="snmpv3_delete_group",
                method="DELETE",
                url="/api/v1/snmpv3/groups/{groupName}/security-model/{securityModel}",
                category="snmpv3_groups",
                module="snmp",
                params={"groupName": "v3privgroup", "securityModel": "v3"},
                query_params={"securityLevel": "priv"},
                description="刪除SNMPv3組"
            )
        ]
    
    def get_snmpv3_users_tests(self) -> List[APITestCase]:
        """SNMPv3 Users API 測試案例"""
        return [
            # 獲取所有SNMP用戶
            self.create_test_case(
                name="snmpv3_get_all_users",
                method="GET",
                url="/api/v1/snmpv3/users",
                category="snmpv3_users",
                module="snmp",
                description="獲取所有SNMPv3用戶"
            ),
            
            # 添加SNMPv3用戶 - 無認證
            self.create_test_case(
                name="snmpv3_add_noauth_user",
                method="POST",
                url="/api/v1/snmpv3/users",
                category="snmpv3_users",
                module="snmp",
                body=self.test_data.get('snmpv3_noauth_user', {
                    "userName": "noauthuser",
                    "groupName": "v2group",
                    "securityModel": "v3"
                }),
                description="添加SNMPv3用戶 - 無認證"
            ),
            
            # 添加SNMPv3用戶 - MD5認證
            self.create_test_case(
                name="snmpv3_add_md5_auth_user",
                method="POST",
                url="/api/v1/snmpv3/users",
                category="snmpv3_users",
                module="snmp",
                body=self.test_data.get('snmpv3_md5_auth_user', {
                    "userName": "md5user",
                    "groupName": "v3authgroup",
                    "securityModel": "v3",
                    "authType": "md5",
                    "authPassword": "authpass123"
                }),
                description="添加SNMPv3用戶 - MD5認證"
            ),
            
            # 添加SNMPv3用戶 - SHA認證
            self.create_test_case(
                name="snmpv3_add_sha_auth_user",
                method="POST",
                url="/api/v1/snmpv3/users",
                category="snmpv3_users",
                module="snmp",
                body=self.test_data.get('snmpv3_sha_auth_user', {
                    "userName": "shauser",
                    "groupName": "v3authgroup",
                    "securityModel": "v3",
                    "authType": "sha",
                    "authPassword": "shapass123"
                }),
                description="添加SNMPv3用戶 - SHA認證"
            ),
            
            # 添加SNMPv3用戶 - 帶隱私加密
            self.create_test_case(
                name="snmpv3_add_priv_user",
                method="POST",
                url="/api/v1/snmpv3/users",
                category="snmpv3_users",
                module="snmp",
                body=self.test_data.get('snmpv3_priv_user', {
                    "userName": "privuser",
                    "groupName": "v3privgroup",
                    "securityModel": "v3",
                    "authType": "md5",
                    "authPassword": "authpass123",
                    "privType": "des56",
                    "privPassword": "privpass123"
                }),
                description="添加SNMPv3用戶 - 帶隱私加密"
            ),
            
            # 添加遠程SNMPv3用戶
            self.create_test_case(
                name="snmpv3_add_remote_user",
                method="POST",
                url="/api/v1/snmpv3/users",
                category="snmpv3_users",
                module="snmp",
                body=self.test_data.get('snmpv3_remote_user', {
                    "userName": "remoteuser",
                    "groupName": "v3authgroup",
                    "remoteIp": "192.168.1.55",
                    "securityModel": "v3",
                    "authType": "md5",
                    "authPassword": "remotepass123"
                }),
                description="添加遠程SNMPv3用戶"
            ),
            
            # 獲取特定用戶
            self.create_test_case(
                name="snmpv3_get_specific_user",
                method="GET",
                url="/api/v1/snmpv3/users/{userName}/security-model/{securityModel}",
                category="snmpv3_users",
                module="snmp",
                params={"userName": "md5user", "securityModel": "v3"},
                description="獲取特定SNMPv3用戶信息"
            ),
            
            # 獲取遠程用戶
            self.create_test_case(
                name="snmpv3_get_remote_user",
                method="GET",
                url="/api/v1/snmpv3/users/{userName}/security-model/{securityModel}",
                category="snmpv3_users",
                module="snmp",
                params={"userName": "remoteuser", "securityModel": "v3"},
                query_params={"remoteIp": "192.168.1.55"},
                description="獲取遠程SNMPv3用戶信息"
            ),
            
            # 生成加密密鑰 - 本地用戶
            self.create_test_case(
                name="snmpv3_generate_local_encrypted_key",
                method="POST",
                url="/api/v1/snmpv3/users/encrypted-key",
                category="snmpv3_users",
                module="snmp",
                body=self.test_data.get('snmpv3_local_encrypted_key', {
                    "userType": "local",
                    "securityLevel": "authPriv",
                    "authType": "md5",
                    "authPassword": "01234567",
                    "privType": "3des",
                    "privPassword": "01234567"
                }),
                description="生成本地用戶加密密鑰"
            ),
            
            # 刪除SNMPv3用戶
            self.create_test_case(
                name="snmpv3_delete_user",
                method="DELETE",
                url="/api/v1/snmpv3/users/{userName}/security-model/{securityModel}",
                category="snmpv3_users",
                module="snmp",
                params={"userName": "privuser", "securityModel": "v3"},
                description="刪除SNMPv3用戶"
            ),
            
            # 刪除遠程用戶
            self.create_test_case(
                name="snmpv3_delete_remote_user",
                method="DELETE",
                url="/api/v1/snmpv3/users/{userName}/security-model/{securityModel}",
                category="snmpv3_users",
                module="snmp",
                params={"userName": "remoteuser", "securityModel": "v3"},
                query_params={"remoteIp": "192.168.1.55"},
                description="刪除遠程SNMPv3用戶"
            )
        ]
    
    def get_snmpv3_views_tests(self) -> List[APITestCase]:
        """SNMPv3 Views API 測試案例"""
        return [
            # 獲取所有SNMP視圖
            self.create_test_case(
                name="snmpv3_get_all_views",
                method="GET",
                url="/api/v1/snmpv3/views",
                category="snmpv3_views",
                module="snmp",
                description="獲取所有SNMPv3視圖"
            ),
            
            # 添加包含視圖
            self.create_test_case(
                name="snmpv3_add_included_view",
                method="POST",
                url="/api/v1/snmpv3/views",
                category="snmpv3_views",
                module="snmp",
                body=self.test_data.get('snmpv3_included_view', {
                    "viewName": "systemview",
                    "viewSubtree": "1.3.6.1.2.1.1",
                    "viewType": "included"
                }),
                description="添加包含SNMPv3視圖"
            ),
            
            # 添加排除視圖
            self.create_test_case(
                name="snmpv3_add_excluded_view",
                method="POST",
                url="/api/v1/snmpv3/views",
                category="snmpv3_views",
                module="snmp",
                body=self.test_data.get('snmpv3_excluded_view', {
                    "viewName": "restrictview",
                    "viewSubtree": "1.3.6.1.2.1.11",
                    "viewType": "excluded"
                }),
                description="添加排除SNMPv3視圖"
            ),
            
            # 添加接口視圖
            self.create_test_case(
                name="snmpv3_add_interface_view",
                method="POST",
                url="/api/v1/snmpv3/views",
                category="snmpv3_views",
                module="snmp",
                body=self.test_data.get('snmpv3_interface_view', {
                    "viewName": "ifEntry.2",
                    "viewSubtree": "1.3.6.1.2.1.2.2.1.2",
                    "viewType": "included"
                }),
                description="添加接口SNMPv3視圖"
            ),
            
            # 獲取特定視圖
            self.create_test_case(
                name="snmpv3_get_specific_view",
                method="GET",
                url="/api/v1/snmpv3/views/{viewName}/view-subtree/{viewSubtree}",
                category="snmpv3_views",
                module="snmp",
                params={"viewName": "systemview", "viewSubtree": "1.3.6.1.2.1.1"},
                description="獲取特定SNMPv3視圖"
            ),
            
            # 刪除SNMP視圖
            self.create_test_case(
                name="snmpv3_delete_view",
                method="DELETE",
                url="/api/v1/snmpv3/views/{viewName}/view-subtree/{viewSubtree}",
                category="snmpv3_views",
                module="snmp",
                params={"viewName": "restrictview", "viewSubtree": "1.3.6.1.2.1.11"},
                description="刪除SNMPv3視圖"
            )
        ]
    
    def get_snmp_notify_tests(self) -> List[APITestCase]:
        """SNMP Notify API 測試案例"""
        return [
            # 獲取通知日誌運行狀態
            self.create_test_case(
                name="snmp_get_notify_log_status",
                method="GET",
                url="/api/v1/snmp/nlm",
                category="snmp_notify",
                module="snmp",
                description="獲取SNMP通知日誌運行狀態"
            ),
            
            # 啟用/禁用指定通知日誌
            self.create_test_case(
                name="snmp_set_notify_log_status",
                method="PUT",
                url="/api/v1/snmp/nlm",
                category="snmp_notify",
                module="snmp",
                body=self.test_data.get('snmp_notify_log_config', {
                    "filterName": "A1"
                }),
                description="設置SNMP通知日誌狀態"
            ),
            
            # 獲取所有配置的通知日誌
            self.create_test_case(
                name="snmp_get_all_notify_filters",
                method="GET",
                url="/api/v1/snmp/notify/filters",
                category="snmp_notify",
                module="snmp",
                description="獲取所有配置的SNMP通知過濾器"
            ),
            
            # 添加SNMP通知日誌
            self.create_test_case(
                name="snmp_add_notify_filter",
                method="POST",
                url="/api/v1/snmp/notify/filters",
                category="snmp_notify",
                module="snmp",
                body=self.test_data.get('snmp_notify_filter', {
                    "profileName": "testprofile",
                    "profileIp": "10.1.19.23"
                }),
                description="添加SNMP通知過濾器"
            ),
            
            # 獲取配置的通知日誌
            self.create_test_case(
                name="snmp_get_specific_notify_filter",
                method="GET",
                url="/api/v1/snmp/notify/filters/profile-ip/{profileIp}",
                category="snmp_notify",
                module="snmp",
                params={"profileIp": "10.1.19.23"},
                description="獲取特定SNMP通知過濾器"
            ),
            
            # 刪除SNMP通知日誌
            self.create_test_case(
                name="snmp_delete_notify_filter",
                method="DELETE",
                url="/api/v1/snmp/notify/filters/profile-ip/{profileIp}",
                category="snmp_notify",
                module="snmp",
                params={"profileIp": "10.1.19.23"},
                description="刪除SNMP通知過濾器"
            )
        ]