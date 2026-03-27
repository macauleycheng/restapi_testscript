#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Link Aggregation 模組測試案例
包含Link Aggregation全局設置、LACP Port Channel、LACP Interface、Static Port Channel相關API測試
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class LINK_AGGREGATIONTests(BaseTests):
    """Link Aggregation 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取Link Aggregation模組支援的類別"""
        return [
            "link_aggregation_global",
            "lacp_port_channels",
            "lacp_interfaces",
            "static_port_channels"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有Link Aggregation測試案例"""
        all_tests = []
        all_tests.extend(self.get_link_aggregation_global_tests())
        all_tests.extend(self.get_lacp_port_channels_tests())
        all_tests.extend(self.get_lacp_interfaces_tests())
        all_tests.extend(self.get_static_port_channels_tests())
        return all_tests
    
    def get_link_aggregation_global_tests(self) -> List[APITestCase]:
        """Link Aggregation Global Setting API 測試案例"""
        return [
            # 獲取Link Aggregation全局設置
            self.create_test_case(
                name="link_aggregation_get_global_setting",
                method="GET",
                url="/api/v1/link-aggregation",
                category="link_aggregation_global",
                module="link_aggregation",
                description="獲取Link Aggregation全局設置"
            ),
            
            # 配置負載均衡為源MAC地址
            self.create_test_case(
                name="link_aggregation_set_load_balance_src_mac",
                method="PUT",
                url="/api/v1/link-aggregation",
                category="link_aggregation_global",
                module="link_aggregation",
                body=self.test_data.get('link_aggregation_src_mac', {
                    "loadBalance": "src-mac"
                }),
                description="設置Link Aggregation負載均衡為源MAC地址"
            ),
            
            # 配置負載均衡為目標MAC地址
            self.create_test_case(
                name="link_aggregation_set_load_balance_dst_mac",
                method="PUT",
                url="/api/v1/link-aggregation",
                category="link_aggregation_global",
                module="link_aggregation",
                body=self.test_data.get('link_aggregation_dst_mac', {
                    "loadBalance": "dst-mac"
                }),
                description="設置Link Aggregation負載均衡為目標MAC地址"
            ),
            
            # 配置負載均衡為源和目標MAC地址
            self.create_test_case(
                name="link_aggregation_set_load_balance_src_dst_mac",
                method="PUT",
                url="/api/v1/link-aggregation",
                category="link_aggregation_global",
                module="link_aggregation",
                body=self.test_data.get('link_aggregation_src_dst_mac', {
                    "loadBalance": "src-dst-mac"
                }),
                description="設置Link Aggregation負載均衡為源和目標MAC地址"
            ),
            
            # 配置負載均衡為源IP地址
            self.create_test_case(
                name="link_aggregation_set_load_balance_src_ip",
                method="PUT",
                url="/api/v1/link-aggregation",
                category="link_aggregation_global",
                module="link_aggregation",
                body=self.test_data.get('link_aggregation_src_ip', {
                    "loadBalance": "src-ip"
                }),
                description="設置Link Aggregation負載均衡為源IP地址"
            ),
            
            # 配置負載均衡為目標IP地址
            self.create_test_case(
                name="link_aggregation_set_load_balance_dst_ip",
                method="PUT",
                url="/api/v1/link-aggregation",
                category="link_aggregation_global",
                module="link_aggregation",
                body=self.test_data.get('link_aggregation_dst_ip', {
                    "loadBalance": "dst-ip"
                }),
                description="設置Link Aggregation負載均衡為目標IP地址"
            ),
            
            # 配置負載均衡為源和目標IP地址
            self.create_test_case(
                name="link_aggregation_set_load_balance_src_dst_ip",
                method="PUT",
                url="/api/v1/link-aggregation",
                category="link_aggregation_global",
                module="link_aggregation",
                body=self.test_data.get('link_aggregation_src_dst_ip', {
                    "loadBalance": "src-dst-ip"
                }),
                description="設置Link Aggregation負載均衡為源和目標IP地址"
            )
        ]
    
    def get_lacp_port_channels_tests(self) -> List[APITestCase]:
        """LACP Port Channels API 測試案例"""
        return [
            # 獲取所有LACP Port Channel
            self.create_test_case(
                name="lacp_port_channels_get_all",
                method="GET",
                url="/api/v1/lacp/port-channels",
                category="lacp_port_channels",
                module="link_aggregation",
                description="獲取所有LACP Port Channel"
            ),
            
            # 獲取特定LACP Port Channel - Channel 1
            self.create_test_case(
                name="lacp_port_channels_get_channel_1",
                method="GET",
                url="/api/v1/lacp/port-channels/{channelId}",
                category="lacp_port_channels",
                module="link_aggregation",
                params={"channelId": 1},
                description="獲取LACP Port Channel 1"
            ),
            
            # 獲取特定LACP Port Channel - Channel 2
            self.create_test_case(
                name="lacp_port_channels_get_channel_2",
                method="GET",
                url="/api/v1/lacp/port-channels/{channelId}",
                category="lacp_port_channels",
                module="link_aggregation",
                params={"channelId": 2},
                description="獲取LACP Port Channel 2"
            ),
            
            # 獲取參數化LACP Port Channel
            self.create_test_case(
                name="lacp_port_channels_get_parameterized",
                method="GET",
                url="/api/v1/lacp/port-channels/{channelId}",
                category="lacp_port_channels",
                module="link_aggregation",
                params={"channelId": self.params.get('channel_id', 1)},
                description=f"獲取LACP Port Channel {self.params.get('channel_id', 1)}"
            ),
            
            # 更新LACP Port Channel - 設置系統優先級
            self.create_test_case(
                name="lacp_port_channels_update_system_priority",
                method="PUT",
                url="/api/v1/lacp/port-channels/{channelId}",
                category="lacp_port_channels",
                module="link_aggregation",
                params={"channelId": self.params.get('channel_id', 1)},
                body=self.test_data.get('lacp_channel_system_priority', {
                    "systemPriority": 32768
                }),
                description=f"更新LACP Port Channel {self.params.get('channel_id', 1)} 系統優先級"
            ),
            
            # 更新LACP Port Channel - 設置高系統優先級
            self.create_test_case(
                name="lacp_port_channels_update_high_priority",
                method="PUT",
                url="/api/v1/lacp/port-channels/{channelId}",
                category="lacp_port_channels",
                module="link_aggregation",
                params={"channelId": self.params.get('channel_id', 1)},
                body=self.test_data.get('lacp_channel_high_priority', {
                    "systemPriority": 1
                }),
                description=f"更新LACP Port Channel {self.params.get('channel_id', 1)} 為高優先級"
            ),
            
            # 更新LACP Port Channel - 設置低系統優先級
            self.create_test_case(
                name="lacp_port_channels_update_low_priority",
                method="PUT",
                url="/api/v1/lacp/port-channels/{channelId}",
                category="lacp_port_channels",
                module="link_aggregation",
                params={"channelId": self.params.get('channel_id', 1)},
                body=self.test_data.get('lacp_channel_low_priority', {
                    "systemPriority": 65535
                }),
                description=f"更新LACP Port Channel {self.params.get('channel_id', 1)} 為低優先級"
            ),
            
            # 獲取不存在的LACP Port Channel (錯誤處理測試)
            self.create_test_case(
                name="lacp_port_channels_get_nonexistent",
                method="GET",
                url="/api/v1/lacp/port-channels/{channelId}",
                category="lacp_port_channels",
                module="link_aggregation",
                params={"channelId": 99},
                description="獲取不存在的LACP Port Channel 99 (測試錯誤處理)"
            ),
            
            # 測試無效系統優先級
            self.create_test_case(
                name="lacp_port_channels_update_invalid_priority",
                method="PUT",
                url="/api/v1/lacp/port-channels/{channelId}",
                category="lacp_port_channels",
                module="link_aggregation",
                params={"channelId": self.params.get('channel_id', 1)},
                body=self.test_data.get('lacp_channel_invalid_priority', {
                    "systemPriority": 70000  # 超出範圍 1-65535
                }),
                description=f"測試LACP Port Channel {self.params.get('channel_id', 1)} 無效系統優先級"
            )
        ]
    
    def get_lacp_interfaces_tests(self) -> List[APITestCase]:
        """LACP Interfaces API 測試案例"""
        return [
            # 獲取特定接口的LACP配置 - eth1/1
            self.create_test_case(
                name="lacp_interfaces_get_eth1_1",
                method="GET",
                url="/api/v1/lacp/interfaces?ifId={ifId}",
                category="lacp_interfaces",
                module="link_aggregation",
                params={"ifId": "eth1%2f1"},
                description="獲取接口 eth1/1 的LACP配置"
            ),
            
            # 獲取特定接口的LACP配置 - eth1/2
            self.create_test_case(
                name="lacp_interfaces_get_eth1_2",
                method="GET",
                url="/api/v1/lacp/interfaces?ifId={ifId}",
                category="lacp_interfaces",
                module="link_aggregation",
                params={"ifId": "eth1%2f2"},
                description="獲取接口 eth1/2 的LACP配置"
            ),
            
            # 獲取參數化接口的LACP配置
            self.create_test_case(
                name="lacp_interfaces_get_parameterized",
                method="GET",
                url="/api/v1/lacp/interfaces?ifId={ifId}",
                category="lacp_interfaces",
                module="link_aggregation",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                description=f"獲取接口 {self.params.get('interface_id', 'eth1/1')} 的LACP配置"
            ),
            
            # 配置接口LACP - 設置為Active模式
            self.create_test_case(
                name="lacp_interfaces_configure_active_mode",
                method="PUT",
                url="/api/v1/lacp/interfaces?ifId={ifId}",
                category="lacp_interfaces",
                module="link_aggregation",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                body=self.test_data.get('lacp_interface_active', {
                    "channelId": 1,
                    "mode": "active",
                    "portPriority": 32768,
                    "timeout": "long"
                }),
                description=f"配置接口 {self.params.get('interface_id', 'eth1/1')} LACP為Active模式"
            ),
            
            # 配置接口LACP - 設置為Passive模式
            self.create_test_case(
                name="lacp_interfaces_configure_passive_mode",
                method="PUT",
                url="/api/v1/lacp/interfaces?ifId={ifId}",
                category="lacp_interfaces",
                module="link_aggregation",
                params={"ifId": self.params.get('interface_id_2', 'eth1%2f2')},
                body=self.test_data.get('lacp_interface_passive', {
                    "channelId": 1,
                    "mode": "passive",
                    "portPriority": 32768,
                    "timeout": "short"
                }),
                description=f"配置接口 {self.params.get('interface_id_2', 'eth1/2')} LACP為Passive模式"
            ),
            
            # 配置接口LACP - 設置高端口優先級
            self.create_test_case(
                name="lacp_interfaces_configure_high_port_priority",
                method="PUT",
                url="/api/v1/lacp/interfaces?ifId={ifId}",
                category="lacp_interfaces",
                module="link_aggregation",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                body=self.test_data.get('lacp_interface_high_priority', {
                    "channelId": 1,
                    "mode": "active",
                    "portPriority": 1,
                    "timeout": "long"
                }),
                description=f"配置接口 {self.params.get('interface_id', 'eth1/1')} LACP高端口優先級"
            ),
            
            # 配置接口LACP - 設置低端口優先級
            self.create_test_case(
                name="lacp_interfaces_configure_low_port_priority",
                method="PUT",
                url="/api/v1/lacp/interfaces?ifId={ifId}",
                category="lacp_interfaces",
                module="link_aggregation",
                params={"ifId": self.params.get('interface_id_2', 'eth1%2f2')},
                body=self.test_data.get('lacp_interface_low_priority', {
                    "channelId": 1,
                    "mode": "passive",
                    "portPriority": 65535,
                    "timeout": "short"
                }),
                description=f"配置接口 {self.params.get('interface_id_2', 'eth1/2')} LACP低端口優先級"
            ),
            
            # 配置接口LACP - 短超時
            self.create_test_case(
                name="lacp_interfaces_configure_short_timeout",
                method="PUT",
                url="/api/v1/lacp/interfaces?ifId={ifId}",
                category="lacp_interfaces",
                module="link_aggregation",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                body=self.test_data.get('lacp_interface_short_timeout', {
                    "channelId": 2,
                    "mode": "active",
                    "portPriority": 32768,
                    "timeout": "short"
                }),
                description=f"配置接口 {self.params.get('interface_id', 'eth1/1')} LACP短超時"
            ),
            
            # 配置接口LACP - 長超時
            self.create_test_case(
                name="lacp_interfaces_configure_long_timeout",
                method="PUT",
                url="/api/v1/lacp/interfaces?ifId={ifId}",
                category="lacp_interfaces",
                module="link_aggregation",
                params={"ifId": self.params.get('interface_id_2', 'eth1%2f2')},
                body=self.test_data.get('lacp_interface_long_timeout', {
                    "channelId": 2,
                    "mode": "passive",
                    "portPriority": 32768,
                    "timeout": "long"
                }),
                description=f"配置接口 {self.params.get('interface_id_2', 'eth1/2')} LACP長超時"
            ),
            
            # 測試無效Channel ID
            self.create_test_case(
                name="lacp_interfaces_configure_invalid_channel",
                method="PUT",
                url="/api/v1/lacp/interfaces?ifId={ifId}",
                category="lacp_interfaces",
                module="link_aggregation",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                body=self.test_data.get('lacp_interface_invalid_channel', {
                    "channelId": 99,  # 超出範圍 1-26
                    "mode": "active",
                    "portPriority": 32768,
                    "timeout": "long"
                }),
                description=f"測試接口 {self.params.get('interface_id', 'eth1/1')} 無效Channel ID"
            ),
            
            # 測試無效端口優先級
            self.create_test_case(
                name="lacp_interfaces_configure_invalid_port_priority",
                method="PUT",
                url="/api/v1/lacp/interfaces?ifId={ifId}",
                category="lacp_interfaces",
                module="link_aggregation",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                body=self.test_data.get('lacp_interface_invalid_priority', {
                    "channelId": 1,
                    "mode": "active",
                    "portPriority": 70000,  # 超出範圍 1-65535
                    "timeout": "long"
                }),
                description=f"測試接口 {self.params.get('interface_id', 'eth1/1')} 無效端口優先級"
            )
        ]
    
    def get_static_port_channels_tests(self) -> List[APITestCase]:
        """Static Port Channels API 測試案例"""
        return [
            # 獲取所有Static Port Channel
            self.create_test_case(
                name="static_port_channels_get_all",
                method="GET",
                url="/api/v1/static-port-channels",
                category="static_port_channels",
                module="link_aggregation",
                description="獲取所有Static Port Channel"
            ),
            
            # 創建Static Port Channel - Channel 3
            self.create_test_case(
                name="static_port_channels_create_channel_3",
                method="POST",
                url="/api/v1/static-port-channels",
                category="static_port_channels",
                module="link_aggregation",
                body=self.test_data.get('static_channel_create_3', {
                    "channelId": 3,
                    "members": [
                        {"ifId": "eth1/3"},
                        {"ifId": "eth1/4"}
                    ]
                }),
                description="創建Static Port Channel 3"
            ),
            
            # 創建Static Port Channel - Channel 4
            self.create_test_case(
                name="static_port_channels_create_channel_4",
                method="POST",
                url="/api/v1/static-port-channels",
                category="static_port_channels",
                module="link_aggregation",
                body=self.test_data.get('static_channel_create_4', {
                    "channelId": 4,
                    "members": [
                        {"ifId": "eth1/5"},
                        {"ifId": "eth1/6"},
                        {"ifId": "eth1/7"}
                    ]
                }),
                description="創建Static Port Channel 4 (3個成員)"
            ),
            
            # 創建參數化Static Port Channel
            self.create_test_case(
                name="static_port_channels_create_parameterized",
                method="POST",
                url="/api/v1/static-port-channels",
                category="static_port_channels",
                module="link_aggregation",
                body=self.test_data.get('static_channel_create_param', {
                    "channelId": self.params.get('static_channel_id', 5),
                    "members": [
                        {"ifId": self.params.get('interface_id', 'eth1/8')},
                        {"ifId": self.params.get('interface_id_2', 'eth1/9')}
                    ]
                }),
                description=f"創建參數化Static Port Channel {self.params.get('static_channel_id', 5)}"
            ),
            
            # 獲取特定Static Port Channel - Channel 3
            self.create_test_case(
                name="static_port_channels_get_channel_3",
                method="GET",
                url="/api/v1/static-port-channels/{channelId}",
                category="static_port_channels",
                module="link_aggregation",
                params={"channelId": 3},
                description="獲取Static Port Channel 3"
            ),
            
            # 獲取特定Static Port Channel - Channel 4
            self.create_test_case(
                name="static_port_channels_get_channel_4",
                method="GET",
                url="/api/v1/static-port-channels/{channelId}",
                category="static_port_channels",
                module="link_aggregation",
                params={"channelId": 4},
                description="獲取Static Port Channel 4"
            ),
            
            # 獲取參數化Static Port Channel
            self.create_test_case(
                name="static_port_channels_get_parameterized",
                method="GET",
                url="/api/v1/static-port-channels/{channelId}",
                category="static_port_channels",
                module="link_aggregation",
                params={"channelId": self.params.get('static_channel_id', 5)},
                description=f"獲取Static Port Channel {self.params.get('static_channel_id', 5)}"
            ),
            
            # 更新Static Port Channel - 添加成員
            self.create_test_case(
                name="static_port_channels_update_add_member",
                method="PUT",
                url="/api/v1/static-port-channels/{channelId}",
                category="static_port_channels",
                module="link_aggregation",
                params={"channelId": 3},
                body=self.test_data.get('static_channel_add_member', {
                    "members": [
                        {"ifId": "eth1/3"},
                        {"ifId": "eth1/4"},
                        {"ifId": "eth1/10"}
                    ]
                }),
                description="更新Static Port Channel 3 - 添加成員"
            ),
            
            # 更新Static Port Channel - 移除成員
            self.create_test_case(
                name="static_port_channels_update_remove_member",
                method="PUT",
                url="/api/v1/static-port-channels/{channelId}",
                category="static_port_channels",
                module="link_aggregation",
                params={"channelId": 4},
                body=self.test_data.get('static_channel_remove_member', {
                    "members": [
                        {"ifId": "eth1/5"},
                        {"ifId": "eth1/6"}
                    ]
                }),
                description="更新Static Port Channel 4 - 移除成員"
            ),
            
            # 更新參數化Static Port Channel
            self.create_test_case(
                name="static_port_channels_update_parameterized",
                method="PUT",
                url="/api/v1/static-port-channels/{channelId}",
                category="static_port_channels",
                module="link_aggregation",
                params={"channelId": self.params.get('static_channel_id', 5)},
                body=self.test_data.get('static_channel_update_param', {
                    "members": [
                        {"ifId": self.params.get('interface_id', 'eth1/8')},
                        {"ifId": self.params.get('interface_id_2', 'eth1/9')},
                        {"ifId": "eth1/11"}
                    ]
                }),
                description=f"更新參數化Static Port Channel {self.params.get('static_channel_id', 5)}"
            ),
            
            # 刪除Static Port Channel - Channel 3
            self.create_test_case(
                name="static_port_channels_delete_channel_3",
                method="DELETE",
                url="/api/v1/static-port-channels/{channelId}",
                category="static_port_channels",
                module="link_aggregation",
                params={"channelId": 3},
                description="刪除Static Port Channel 3"
            ),
            
            # 刪除Static Port Channel - Channel 4
            self.create_test_case(
                name="static_port_channels_delete_channel_4",
                method="DELETE",
                url="/api/v1/static-port-channels/{channelId}",
                category="static_port_channels",
                module="link_aggregation",
                params={"channelId": 4},
                description="刪除Static Port Channel 4"
            ),
            
            # 刪除參數化Static Port Channel
            self.create_test_case(
                name="static_port_channels_delete_parameterized",
                method="DELETE",
                url="/api/v1/static-port-channels/{channelId}",
                category="static_port_channels",
                module="link_aggregation",
                params={"channelId": self.params.get('static_channel_id', 5)},
                description=f"刪除參數化Static Port Channel {self.params.get('static_channel_id', 5)}"
            ),
            
            # 測試創建重複Channel ID
            self.create_test_case(
                name="static_port_channels_create_duplicate_channel",
                method="POST",
                url="/api/v1/static-port-channels",
                category="static_port_channels",
                module="link_aggregation",
                body=self.test_data.get('static_channel_duplicate', {
                    "channelId": 1,  # 假設已存在
                    "members": [
                        {"ifId": "eth1/12"}
                    ]
                }),
                expected_status=500,
                description="測試創建重複Channel ID (衝突處理)"
            ),
            
            # 測試無效Channel ID範圍
            self.create_test_case(
                name="static_port_channels_create_invalid_channel_id",
                method="POST",
                url="/api/v1/static-port-channels",
                category="static_port_channels",
                module="link_aggregation",
                body=self.test_data.get('static_channel_invalid_id', {
                    "channelId": 99,  # 超出範圍 1-26
                    "members": [
                        {"ifId": "eth1/13"}
                    ]
                }),
                expected_status=500,
                description="測試創建無效Channel ID範圍"
            ),
            
            # 獲取不存在的Static Port Channel
            self.create_test_case(
                name="static_port_channels_get_nonexistent",
                method="GET",
                url="/api/v1/static-port-channels/{channelId}",
                category="static_port_channels",
                module="link_aggregation",
                params={"channelId": 99},
                expected_status=500,
                description="獲取不存在的Static Port Channel 99 (測試錯誤處理)"
            )
        ]