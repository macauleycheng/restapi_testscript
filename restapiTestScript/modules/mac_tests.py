#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAC 模組測試案例
包含MAC地址表管理、老化配置、哈希查找深度、碰撞處理、MAC抖動檢測等相關API測試
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class MACTests(BaseTests):
    """MAC 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取MAC模組支援的類別"""
        return [
            "mac_aging",
            "mac_address_table",
            "mac_collisions",
            "mac_thrashing",
            "mac_hash_lookup"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有MAC測試案例"""
        all_tests = []
        all_tests.extend(self.get_mac_aging_tests())
        all_tests.extend(self.get_mac_address_table_tests())
        all_tests.extend(self.get_mac_collisions_tests())
        all_tests.extend(self.get_mac_thrashing_tests())
        all_tests.extend(self.get_mac_hash_lookup_tests())
        return all_tests
    
    def get_mac_aging_tests(self) -> List[APITestCase]:
        """MAC Aging API 測試案例"""
        return [
            # 獲取MAC老化時間和哈希查找深度
            self.create_test_case(
                name="mac_get_aging_config",
                method="GET",
                url="/api/v1/macs",
                category="mac_aging",
                module="mac",
                description="獲取MAC老化時間和哈希查找深度配置"
            ),
            
            # 啟用MAC老化 - 基本配置
            self.create_test_case(
                name="mac_enable_aging_basic",
                method="PUT",
                url="/api/v1/macs",
                category="mac_aging",
                module="mac",
                body=self.test_data.get('mac_aging_basic', {
                    "agingStatus": True,
                    "agingTime": 300,
                    "hashLookupDepth": 4
                }),
                description="啟用MAC老化 - 基本配置"
            ),
            
            # 啟用MAC老化 - 僅啟用狀態
            self.create_test_case(
                name="mac_enable_aging_only",
                method="PUT",
                url="/api/v1/macs",
                category="mac_aging",
                module="mac",
                body=self.test_data.get('mac_aging_enable_only', {
                    "agingStatus": True
                }),
                description="啟用MAC老化 - 僅啟用狀態"
            ),
            
            # 配置MAC老化時間 - 最小值
            self.create_test_case(
                name="mac_configure_min_aging_time",
                method="PUT",
                url="/api/v1/macs",
                category="mac_aging",
                module="mac",
                body=self.test_data.get('mac_aging_min_time', {
                    "agingStatus": True,
                    "agingTime": 6
                }),
                description="配置MAC老化時間 - 最小值 (6秒)"
            ),
            
            # 配置MAC老化時間 - 最大值
            self.create_test_case(
                name="mac_configure_max_aging_time",
                method="PUT",
                url="/api/v1/macs",
                category="mac_aging",
                module="mac",
                body=self.test_data.get('mac_aging_max_time', {
                    "agingStatus": True,
                    "agingTime": 7200
                }),
                description="配置MAC老化時間 - 最大值 (7200秒)"
            ),
            
            # 配置MAC老化時間 - 默認值
            self.create_test_case(
                name="mac_configure_default_aging_time",
                method="PUT",
                url="/api/v1/macs",
                category="mac_aging",
                module="mac",
                body=self.test_data.get('mac_aging_default_time', {
                    "agingStatus": True,
                    "agingTime": 300
                }),
                description="配置MAC老化時間 - 默認值 (300秒)"
            ),
            
            # 配置MAC老化時間 - 自定義值
            self.create_test_case(
                name="mac_configure_custom_aging_time",
                method="PUT",
                url="/api/v1/macs",
                category="mac_aging",
                module="mac",
                body=self.test_data.get('mac_aging_custom_time', {
                    "agingStatus": True,
                    "agingTime": 600
                }),
                description="配置MAC老化時間 - 自定義值 (600秒)"
            ),
            
            # 禁用MAC老化
            self.create_test_case(
                name="mac_disable_aging",
                method="PUT",
                url="/api/v1/macs",
                category="mac_aging",
                module="mac",
                body=self.test_data.get('mac_aging_disable', {
                    "agingStatus": False
                }),
                description="禁用MAC老化"
            ),
            
            # 重新啟用MAC老化
            self.create_test_case(
                name="mac_re_enable_aging",
                method="PUT",
                url="/api/v1/macs",
                category="mac_aging",
                module="mac",
                body=self.test_data.get('mac_aging_re_enable', {
                    "agingStatus": True,
                    "agingTime": 450
                }),
                description="重新啟用MAC老化"
            ),
            
            # 測試無效老化時間 - 低於最小值
            self.create_test_case(
                name="mac_test_invalid_aging_time_low",
                method="PUT",
                url="/api/v1/macs",
                category="mac_aging",
                module="mac",
                body=self.test_data.get('mac_aging_invalid_low', {
                    "agingStatus": True,
                    "agingTime": 3  # 低於範圍 6-7200
                }),
                expected_status=200,
                description="測試無效老化時間 - 低於最小值"
            ),
            
            # 測試無效老化時間 - 超過最大值
            self.create_test_case(
                name="mac_test_invalid_aging_time_high",
                method="PUT",
                url="/api/v1/macs",
                category="mac_aging",
                module="mac",
                body=self.test_data.get('mac_aging_invalid_high', {
                    "agingStatus": True,
                    "agingTime": 8000  # 超出範圍 6-7200
                }),
                expected_status=200,
                description="測試無效老化時間 - 超過最大值"
            ),
            
            # 驗證MAC老化配置更新
            self.create_test_case(
                name="mac_verify_aging_config",
                method="GET",
                url="/api/v1/macs",
                category="mac_aging",
                module="mac",
                description="驗證MAC老化配置更新"
            )
        ]
    
    def get_mac_hash_lookup_tests(self) -> List[APITestCase]:
        """MAC Hash Lookup API 測試案例"""
        return [
            # 配置哈希查找深度 - 最小值
            self.create_test_case(
                name="mac_configure_min_hash_depth",
                method="PUT",
                url="/api/v1/macs",
                category="mac_hash_lookup",
                module="mac",
                body=self.test_data.get('mac_hash_min_depth', {
                    "agingStatus": True,
                    "hashLookupDepth": 4
                }),
                description="配置哈希查找深度 - 最小值 (4)"
            ),
            
            # 配置哈希查找深度 - 最大值
            self.create_test_case(
                name="mac_configure_max_hash_depth",
                method="PUT",
                url="/api/v1/macs",
                category="mac_hash_lookup",
                module="mac",
                body=self.test_data.get('mac_hash_max_depth', {
                    "agingStatus": True,
                    "hashLookupDepth": 32
                }),
                description="配置哈希查找深度 - 最大值 (32)"
            ),
            
            # 配置哈希查找深度 - 中等值
            self.create_test_case(
                name="mac_configure_medium_hash_depth",
                method="PUT",
                url="/api/v1/macs",
                category="mac_hash_lookup",
                module="mac",
                body=self.test_data.get('mac_hash_medium_depth', {
                    "agingStatus": True,
                    "hashLookupDepth": 16
                }),
                description="配置哈希查找深度 - 中等值 (16)"
            ),
            
            # 配置哈希查找深度 - 自定義值
            self.create_test_case(
                name="mac_configure_custom_hash_depth",
                method="PUT",
                url="/api/v1/macs",
                category="mac_hash_lookup",
                module="mac",
                body=self.test_data.get('mac_hash_custom_depth', {
                    "agingStatus": True,
                    "hashLookupDepth": 8
                }),
                description="配置哈希查找深度 - 自定義值 (8)"
            ),
            
            # 完整配置 - 老化和哈希深度
            self.create_test_case(
                name="mac_complete_aging_hash_config",
                method="PUT",
                url="/api/v1/macs",
                category="mac_hash_lookup",
                module="mac",
                body=self.test_data.get('mac_complete_aging_hash', {
                    "agingStatus": True,
                    "agingTime": 100,
                    "hashLookupDepth": 8
                }),
                description="完整配置 - 老化和哈希深度"
            ),
            
            # 測試無效哈希深度 - 不是4的倍數
            self.create_test_case(
                name="mac_test_invalid_hash_depth_multiple",
                method="PUT",
                url="/api/v1/macs",
                category="mac_hash_lookup",
                module="mac",
                body=self.test_data.get('mac_hash_invalid_multiple', {
                    "agingStatus": True,
                    "hashLookupDepth": 7  # 不是4的倍數
                }),
                expected_status=500,
                description="測試無效哈希深度 - 不是4的倍數"
            ),
            
            # 測試無效哈希深度 - 超出範圍
            self.create_test_case(
                name="mac_test_invalid_hash_depth_range",
                method="PUT",
                url="/api/v1/macs",
                category="mac_hash_lookup",
                module="mac",
                body=self.test_data.get('mac_hash_invalid_range', {
                    "agingStatus": True,
                    "hashLookupDepth": 40  # 超出範圍 4-32
                }),
                expected_status=200,
                description="測試無效哈希深度 - 超出範圍"
            ),
            
            # 驗證哈希查找深度配置
            self.create_test_case(
                name="mac_verify_hash_lookup_config",
                method="GET",
                url="/api/v1/macs",
                category="mac_hash_lookup",
                module="mac",
                description="驗證哈希查找深度配置"
            )
        ]
    
    def get_mac_address_table_tests(self) -> List[APITestCase]:
        """MAC Address Table API 測試案例"""
        return [
            # 獲取所有MAC地址表條目
            self.create_test_case(
                name="mac_get_all_address_table_entries",
                method="GET",
                url="/api/v1/macs/mac-address-table",
                category="mac_address_table",
                module="mac",
                params={"startId": "1"},
                description="獲取所有MAC地址表條目"
            ),
            
            # 獲取MAC地址表條目 - 不同起始ID
            self.create_test_case(
                name="mac_get_address_table_entries_start_100",
                method="GET",
                url="/api/v1/macs/mac-address-table",
                category="mac_address_table",
                module="mac",
                params={"startId": "100"},
                description="獲取MAC地址表條目 - 起始ID 100"
            ),
            
            # 添加靜態MAC地址條目 - 基本配置
            self.create_test_case(
                name="mac_add_static_entry_basic",
                method="POST",
                url="/api/v1/macs/mac-address-table",
                category="mac_address_table",
                module="mac",
                body=self.test_data.get('mac_static_entry_basic', {
                    "macAddress": "00-e0-29-94-34-de",
                    "ifId": "eth1/1",
                    "vlanId": 1,
                    "lifetime": "delete-on-reset"
                }),
                description="添加靜態MAC地址條目 - 基本配置"
            ),
            
            # 添加靜態MAC地址條目 - 永久條目
            self.create_test_case(
                name="mac_add_static_entry_permanent",
                method="POST",
                url="/api/v1/macs/mac-address-table",
                category="mac_address_table",
                module="mac",
                body=self.test_data.get('mac_static_entry_permanent', {
                    "macAddress": "00-11-22-33-44-55",
                    "ifId": "eth1/2",
                    "vlanId": 100,
                    "lifetime": "permanent"
                }),
                description="添加靜態MAC地址條目 - 永久條目"
            ),
            
            # 添加靜態MAC地址條目 - Port Channel接口
            self.create_test_case(
                name="mac_add_static_entry_trunk",
                method="POST",
                url="/api/v1/macs/mac-address-table",
                category="mac_address_table",
                module="mac",
                body=self.test_data.get('mac_static_entry_trunk', {
                    "macAddress": "aa-bb-cc-dd-ee-ff",
                    "ifId": "trunk1",
                    "vlanId": 200,
                    "lifetime": "delete-on-reset"
                }),
                description="添加靜態MAC地址條目 - Port Channel接口"
            ),
            
            # 添加靜態MAC地址條目 - 不指定lifetime
            # self.create_test_case(
            #    name="mac_add_static_entry_no_lifetime",
            #    method="POST",
            #    url="/api/v1/macs/mac-address-table",
            #    category="mac_address_table",
            #    module="mac",
            #    body=self.test_data.get('mac_static_entry_no_lifetime', {
            #        "macAddress": "12-34-56-78-9a-bc",
            #        "ifId": "eth1/3",
            #        "vlanId": 300
            #    }),
            #    description="添加靜態MAC地址條目 - 不指定lifetime"
            # ),
            
            # 獲取特定MAC地址條目
            self.create_test_case(
                name="mac_get_specific_address_entry",
                method="GET",
                url="/api/v1/macs/mac-address-table/{macAddress}/vlans/{vlanId}",
                category="mac_address_table",
                module="mac",
                params={
                    "macAddress": "00-e0-00-00-00-01",
                    "vlanId": "1"
                },
                description="獲取特定MAC地址條目"
            ),
            
            # 獲取參數化MAC地址條目
            self.create_test_case(
                name="mac_get_parameterized_address_entry",
                method="GET",
                url="/api/v1/macs/mac-address-table/{macAddress}/vlans/{vlanId}",
                category="mac_address_table",
                module="mac",
                params={
                    "macAddress": self.params.get('mac_address', '00-11-22-33-44-55').replace(':', '-'),
                    "vlanId": str(self.params.get('vlan_id', 100))
                },
                description=f"獲取MAC地址 {self.params.get('mac_address', '00-11-22-33-44-55')} VLAN {self.params.get('vlan_id', 100)} 條目"
            ),
            
            # 刪除MAC地址條目
            self.create_test_case(
                name="mac_delete_address_entry",
                method="DELETE",
                url="/api/v1/macs/mac-address-table/{macAddress}/vlans/{vlanId}",
                category="mac_address_table",
                module="mac",
                params={
                    "macAddress": "00-e0-00-00-00-01",
                    "vlanId": "1"
                },
                description="刪除MAC地址條目"
            ),
            
            # 清除所有動態MAC地址條目
            self.create_test_case(
                name="mac_clear_all_dynamic_entries",
                method="PUT",
                url="/api/v1/macs/mac-address-table/dynamic:clear",
                category="mac_address_table",
                module="mac",
                body={},
                description="清除所有動態MAC地址條目"
            ),
            
            # 測試無效MAC地址格式
            # self.create_test_case(
            #     name="mac_test_invalid_mac_format",
            #     method="POST",
            #     url="/api/v1/macs/mac-address-table",
            #     category="mac_address_table",
            #     module="mac",
            #     body=self.test_data.get('mac_invalid_format', {
            #         "macAddress": "invalid-mac-address",
            #         "ifId": "eth1/1",
            #         "vlanId": 1
            #     }),
            #     expected_status=400,
            #     description="測試無效MAC地址格式"
            # ),
            
            # 測試無效VLAN ID
            # self.create_test_case(
            #     name="mac_test_invalid_vlan_id",
            #     method="POST",
            #     url="/api/v1/macs/mac-address-table",
            #     category="mac_address_table",
            #     module="mac",
            #     body=self.test_data.get('mac_invalid_vlan', {
            #         "macAddress": "00-11-22-33-44-55",
            #         "ifId": "eth1/1",
            #         "vlanId": 5000  # 超出範圍 1-4094
            #     }),
            #     expected_status=400,
            #     description="測試無效VLAN ID"
            # ),
            
            # 測試無效接口ID
            # self.create_test_case(
            #     name="mac_test_invalid_interface_id",
            #     method="POST",
            #     url="/api/v1/macs/mac-address-table",
            #     category="mac_address_table",
            #     module="mac",
            #     body=self.test_data.get('mac_invalid_interface', {
            #         "macAddress": "00-11-22-33-44-55",
            #         "ifId": "invalid-interface",
            #         "vlanId": 1
            #     }),
            #     expected_status=400,
            #     description="測試無效接口ID"
            # ),
            
            # 測試重複MAC地址條目
            self.create_test_case(
                name="mac_test_duplicate_entry",
                method="POST",
                url="/api/v1/macs/mac-address-table",
                category="mac_address_table",
                module="mac",
                body=self.test_data.get('mac_duplicate_entry', {
                    "macAddress": "00-e0-29-94-34-de",
                    "ifId": "eth1/1",
                    "vlanId": 1,
                    "lifetime": "permanent"
                }),
                expected_status=200,
                description="測試重複MAC地址條目"
            ),
            
            # 驗證MAC地址表更新
            self.create_test_case(
                name="mac_verify_address_table_update",
                method="GET",
                url="/api/v1/macs/mac-address-table",
                category="mac_address_table",
                module="mac",
                params={"startId": "1"},
                description="驗證MAC地址表更新"
            )
        ]
    
    def get_mac_collisions_tests(self) -> List[APITestCase]:
        """MAC Collisions API 測試案例"""
        return [
            # 獲取MAC碰撞列表
            self.create_test_case(
                name="mac_get_collisions_list",
                method="GET",
                url="/api/v1/macs/collisions",
                category="mac_collisions",
                module="mac",
                description="獲取MAC碰撞列表"
            ),
            
            # 清除所有MAC碰撞條目
            self.create_test_case(
                name="mac_clear_all_collisions",
                method="PUT",
                url="/api/v1/macs/collisions:clear",
                category="mac_collisions",
                module="mac",
                body={},
                description="清除所有MAC碰撞條目"
            ),
            
            # 再次獲取MAC碰撞列表 - 驗證清除效果
            self.create_test_case(
                name="mac_verify_collisions_cleared",
                method="GET",
                url="/api/v1/macs/collisions",
                category="mac_collisions",
                module="mac",
                description="驗證MAC碰撞條目已清除"
            ),
            
            # 監控MAC碰撞狀態
            self.create_test_case(
                name="mac_monitor_collisions_status",
                method="GET",
                url="/api/v1/macs/collisions",
                category="mac_collisions",
                module="mac",
                description="監控MAC碰撞狀態"
            )
        ]
    
    def get_mac_thrashing_tests(self) -> List[APITestCase]:
        """MAC Thrashing API 測試案例"""
        return [
            # 獲取所有接口MAC抖動設置
            self.create_test_case(
                name="mac_get_all_thrashing_settings",
                method="GET",
                url="/api/v1/macs/thrashing",
                category="mac_thrashing",
                module="mac",
                description="獲取所有接口MAC抖動設置"
            ),
            
            # 獲取特定接口MAC抖動設置
            self.create_test_case(
                name="mac_get_specific_thrashing_setting",
                method="GET",
                url="/api/v1/macs/thrashing/interface/{ifId}",
                category="mac_thrashing",
                module="mac",
                params={"ifId": "eth1/1"},
                description="獲取特定接口MAC抖動設置"
            ),
            
            # 獲取參數化接口MAC抖動設置
            self.create_test_case(
                name="mac_get_parameterized_thrashing_setting",
                method="GET",
                url="/api/v1/macs/thrashing/interface/{ifId}",
                category="mac_thrashing",
                module="mac",
                params={"ifId": self.params.get('interface_id', 'eth1/1')},
                description=f"獲取接口 {self.params.get('interface_id', 'eth1/1')} MAC抖動設置"
            ),
            
            # 配置接口MAC抖動 - 停止學習
            self.create_test_case(
                name="mac_configure_thrashing_stop_learning",
                method="PUT",
                url="/api/v1/macs/thrashing/interface/{ifId}",
                category="mac_thrashing",
                module="mac",
                params={"ifId": "eth1/1"},
                body=self.test_data.get('mac_thrashing_stop_learning', {
                    "status": True,
                    "action": "stop-learning"
                }),
                description="配置接口MAC抖動 - 停止學習"
            ),
            
            # 配置接口MAC抖動 - 端口禁用
            self.create_test_case(
                name="mac_configure_thrashing_port_disable",
                method="PUT",
                url="/api/v1/macs/thrashing/interface/{ifId}",
                category="mac_thrashing",
                module="mac",
                params={"ifId": "eth1/2"},
                body=self.test_data.get('mac_thrashing_port_disable', {
                    "status": True,
                    "action": "port-disable"
                }),
                description="配置接口MAC抖動 - 端口禁用"
            ),
            
            # 配置接口MAC抖動 - 鏈路斷開
            self.create_test_case(
                name="mac_configure_thrashing_link_down",
                method="PUT",
                url="/api/v1/macs/thrashing/interface/{ifId}",
                category="mac_thrashing",
                module="mac",
                params={"ifId": "eth1/3"},
                body=self.test_data.get('mac_thrashing_link_down', {
                    "status": True,
                    "action": "link-down"
                }),
                description="配置接口MAC抖動 - 鏈路斷開"
            ),
            
            # 配置Port Channel接口MAC抖動
            self.create_test_case(
                name="mac_configure_thrashing_trunk",
                method="PUT",
                url="/api/v1/macs/thrashing/interface/{ifId}",
                category="mac_thrashing",
                module="mac",
                params={"ifId": "trunk1"},
                body=self.test_data.get('mac_thrashing_trunk', {
                    "status": True,
                    "action": "stop-learning"
                }),
                description="配置Port Channel接口MAC抖動"
            ),
            
            # 禁用接口MAC抖動
            self.create_test_case(
                name="mac_disable_thrashing",
                method="PUT",
                url="/api/v1/macs/thrashing/interface/{ifId}",
                category="mac_thrashing",
                module="mac",
                params={"ifId": "eth1/1"},
                body=self.test_data.get('mac_thrashing_disable', {
                    "status": False
                }),
                description="禁用接口MAC抖動"
            ),
            
            # 重新啟用接口MAC抖動
            self.create_test_case(
                name="mac_re_enable_thrashing",
                method="PUT",
                url="/api/v1/macs/thrashing/interface/{ifId}",
                category="mac_thrashing",
                module="mac",
                params={"ifId": "eth1/1"},
                body=self.test_data.get('mac_thrashing_re_enable', {
                    "status": True,
                    "action": "port-disable"
                }),
                description="重新啟用接口MAC抖動"
            ),
            
            # 配置MAC抖動動作持續時間 - 最小值
            self.create_test_case(
                name="mac_configure_min_action_duration",
                method="PUT",
                url="/api/v1/macs/thrashing/action-duration",
                category="mac_thrashing",
                module="mac",
                body=self.test_data.get('mac_thrashing_min_duration', {
                    "actionDuration": 10
                }),
                description="配置MAC抖動動作持續時間 - 最小值 (10秒)"
            ),
            
            # 配置MAC抖動動作持續時間 - 最大值
            self.create_test_case(
                name="mac_configure_max_action_duration",
                method="PUT",
                url="/api/v1/macs/thrashing/action-duration",
                category="mac_thrashing",
                module="mac",
                body=self.test_data.get('mac_thrashing_max_duration', {
                    "actionDuration": 10000
                }),
                description="配置MAC抖動動作持續時間 - 最大值 (10000秒)"
            ),
            
            # 配置MAC抖動動作持續時間 - 永不停止
            self.create_test_case(
                name="mac_configure_never_stop_duration",
                method="PUT",
                url="/api/v1/macs/thrashing/action-duration",
                category="mac_thrashing",
                module="mac",
                body=self.test_data.get('mac_thrashing_never_stop', {
                    "actionDuration": 0
                }),
                description="配置MAC抖動動作持續時間 - 永不停止 (0)"
            ),
            
            # 配置MAC抖動動作持續時間 - 自定義值
            self.create_test_case(
                name="mac_configure_custom_action_duration",
                method="PUT",
                url="/api/v1/macs/thrashing/action-duration",
                category="mac_thrashing",
                module="mac",
                body=self.test_data.get('mac_thrashing_custom_duration', {
                    "actionDuration": 30
                }),
                description="配置MAC抖動動作持續時間 - 自定義值 (30秒)"
            ),
            
            # 測試無效動作類型
            self.create_test_case(
                name="mac_test_invalid_thrashing_action",
                method="PUT",
                url="/api/v1/macs/thrashing/interface/{ifId}",
                category="mac_thrashing",
                module="mac",
                params={"ifId": "eth1/1"},
                body=self.test_data.get('mac_thrashing_invalid_action', {
                    "status": True,
                    "action": "invalid-action"
                }),
                expected_status=400,
                description="測試無效MAC抖動動作類型"
            ),
            
            # 測試無效動作持續時間
            self.create_test_case(
                name="mac_test_invalid_action_duration",
                method="PUT",
                url="/api/v1/macs/thrashing/action-duration",
                category="mac_thrashing",
                module="mac",
                body=self.test_data.get('mac_thrashing_invalid_duration', {
                    "actionDuration": 15000  # 超出範圍 0, 10-10000
                }),
                expected_status=200,
                description="測試無效MAC抖動動作持續時間"
            ),
            
            # 測試無效接口ID
            self.create_test_case(
                name="mac_test_invalid_thrashing_interface",
                method="GET",
                url="/api/v1/macs/thrashing/interface/{ifId}",
                category="mac_thrashing",
                module="mac",
                params={"ifId": "invalid-interface"},
                expected_status=400,
                description="測試無效接口ID"
            ),
            
            # 驗證MAC抖動配置更新
            self.create_test_case(
                name="mac_verify_thrashing_config",
                method="GET",
                url="/api/v1/macs/thrashing",
                category="mac_thrashing",
                module="mac",
                description="驗證MAC抖動配置更新"
            )
        ]