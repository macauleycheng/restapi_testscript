#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ExcludedVlan 模組測試案例
包含流量分段會話管理、上行/下行接口配置、排除VLAN配置等相關API測試
支援會話創建、修改、刪除和查詢操作
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class EXCLUDED_VLANTests(BaseTests):
    """ExcludedVlan 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取ExcludedVlan模組支援的類別"""
        return [
            "excluded_vlan_session_management",
            "excluded_vlan_session_operations",
            "excluded_vlan_interface_config",
            "excluded_vlan_configuration",
            "excluded_vlan_advanced_operations"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有ExcludedVlan測試案例"""
        all_tests = []
        all_tests.extend(self.get_excluded_vlan_session_management_tests())
        all_tests.extend(self.get_excluded_vlan_session_operations_tests())
        all_tests.extend(self.get_excluded_vlan_interface_config_tests())
        all_tests.extend(self.get_excluded_vlan_configuration_tests())
        all_tests.extend(self.get_excluded_vlan_advanced_operations_tests())
        return all_tests
    
    def get_excluded_vlan_session_management_tests(self) -> List[APITestCase]:
        """ExcludedVlan Session Management API 測試案例"""
        return [
            # 獲取所有會話
            self.create_test_case(
                name="excluded_vlan_get_all_sessions",
                method="GET",
                url="/api/v1/excluded-vlan/sessions",
                category="excluded_vlan_session_management",
                module="excluded_vlan",
                description="獲取所有流量分段會話"
            ),
            
            # 創建基本會話 - 會話1
            self.create_test_case(
                name="excluded_vlan_create_session_1",
                method="POST",
                url="/api/v1/excluded-vlan/sessions",
                category="excluded_vlan_session_management",
                module="excluded_vlan",
                body=self.test_data.get('excluded_vlan_session_1', {
                    "sessionId": 1,
                    "excludedVlans": ["100"],
                    "uplinks": [
                        {"ifId": "eth1/1"}
                    ],
                    "downlinks": [
                        {"ifId": "eth1/2"},
                        {"ifId": "eth1/3"}
                    ]
                }),
                description="創建基本會話 - 會話1"
            ),
            
            # 創建多VLAN會話 - 會話2
            self.create_test_case(
                name="excluded_vlan_create_session_2_multi_vlan",
                method="POST",
                url="/api/v1/excluded-vlan/sessions",
                category="excluded_vlan_session_management",
                module="excluded_vlan",
                body=self.test_data.get('excluded_vlan_session_2_multi_vlan', {
                    "sessionId": 2,
                    "excludedVlans": ["200", "201", "202"],
                    "uplinks": [
                        {"ifId": "eth1/4"},
                        {"ifId": "eth1/5"}
                    ],
                    "downlinks": [
                        {"ifId": "eth1/6"},
                        {"ifId": "eth1/7"},
                        {"ifId": "eth1/8"}
                    ]
                }),
                description="創建多VLAN會話 - 會話2"
            ),
            
            # 創建Port Channel會話 - 會話3
            self.create_test_case(
                name="excluded_vlan_create_session_3_port_channel",
                method="POST",
                url="/api/v1/excluded-vlan/sessions",
                category="excluded_vlan_session_management",
                module="excluded_vlan",
                body=self.test_data.get('excluded_vlan_session_3_port_channel', {
                    "sessionId": 3,
                    "excludedVlans": ["300"],
                    "uplinks": [
                        {"ifId": "trunk1"}
                    ],
                    "downlinks": [
                        {"ifId": "eth1/10"},
                        {"ifId": "trunk2"}
                    ]
                }),
                description="創建Port Channel會話 - 會話3"
            ),
            
            # 創建最大會話 - 會話4
            self.create_test_case(
                name="excluded_vlan_create_session_4_max",
                method="POST",
                url="/api/v1/excluded-vlan/sessions",
                category="excluded_vlan_session_management",
                module="excluded_vlan",
                body=self.test_data.get('excluded_vlan_session_4_max', {
                    "sessionId": 4,
                    "excludedVlans": ["400", "401", "402", "403", "404", "405", "406", "407"],
                    "uplinks": [
                        {"ifId": "eth1/11"},
                        {"ifId": "eth1/12"}
                    ],
                    "downlinks": [
                        {"ifId": "eth1/13"},
                        {"ifId": "eth1/14"},
                        {"ifId": "eth1/15"},
                        {"ifId": "eth1/16"}
                    ]
                }),
                description="創建最大會話 - 會話4 (最多8個排除VLAN)"
            ),
            
            # 創建空接口會話
            self.create_test_case(
                name="excluded_vlan_create_session_empty_interfaces",
                method="POST",
                url="/api/v1/excluded-vlan/sessions",
                category="excluded_vlan_session_management",
                module="excluded_vlan",
                body=self.test_data.get('excluded_vlan_session_empty_interfaces', {
                    "sessionId": 1,
                    "excludedVlans": ["500"],
                    "uplinks": [],
                    "downlinks": []
                }),
                description="創建空接口會話 - 僅配置排除VLAN"
            ),
            
            # 測試無效會話ID - 超出範圍
            self.create_test_case(
                name="excluded_vlan_test_invalid_session_id_range",
                method="POST",
                url="/api/v1/excluded-vlan/sessions",
                category="excluded_vlan_session_management",
                module="excluded_vlan",
                body=self.test_data.get('excluded_vlan_invalid_session_id', {
                    "sessionId": 5,  # 超出範圍 1-4
                    "excludedVlans": ["100"]
                }),
                expected_status=400,
                description="測試無效會話ID - 超出範圍"
            ),
            
            # 測試重複會話ID
            self.create_test_case(
                name="excluded_vlan_test_duplicate_session_id",
                method="POST",
                url="/api/v1/excluded-vlan/sessions",
                category="excluded_vlan_session_management",
                module="excluded_vlan",
                body=self.test_data.get('excluded_vlan_duplicate_session', {
                    "sessionId": 1,  # 重複的會話ID
                    "excludedVlans": ["600"]
                }),
                expected_status=400,
                description="測試重複會話ID"
            ),
            
            # 驗證會話創建
            self.create_test_case(
                name="excluded_vlan_verify_sessions_created",
                method="GET",
                url="/api/v1/excluded-vlan/sessions",
                category="excluded_vlan_session_management",
                module="excluded_vlan",
                description="驗證會話創建結果"
            )
        ]
    
    def get_excluded_vlan_session_operations_tests(self) -> List[APITestCase]:
        """ExcludedVlan Session Operations API 測試案例"""
        return [
            # 獲取特定會話 - 會話1
            self.create_test_case(
                name="excluded_vlan_get_session_1",
                method="GET",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_session_operations",
                module="excluded_vlan",
                params={"sessionId": "1"},
                description="獲取特定會話 - 會話1"
            ),
            
            # 獲取特定會話 - 會話2
            self.create_test_case(
                name="excluded_vlan_get_session_2",
                method="GET",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_session_operations",
                module="excluded_vlan",
                params={"sessionId": "2"},
                description="獲取特定會話 - 會話2"
            ),
            
            # 獲取參數化會話
            self.create_test_case(
                name="excluded_vlan_get_parameterized_session",
                method="GET",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_session_operations",
                module="excluded_vlan",
                params={"sessionId": str(self.params.get('session_id', 1))},
                description=f"獲取參數化會話 - 會話{self.params.get('session_id', 1)}"
            ),
            
            # 更新會話 - 添加上行接口
            self.create_test_case(
                name="excluded_vlan_update_session_add_uplinks",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_session_operations",
                module="excluded_vlan",
                params={"sessionId": "1"},
                body=self.test_data.get('excluded_vlan_update_add_uplinks', {
                    "status": True,
                    "uplinks": [
                        {"ifId": "eth1/20"}
                    ]
                }),
                description="更新會話 - 添加上行接口"
            ),
            
            # 更新會話 - 添加下行接口
            self.create_test_case(
                name="excluded_vlan_update_session_add_downlinks",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_session_operations",
                module="excluded_vlan",
                params={"sessionId": "2"},
                body=self.test_data.get('excluded_vlan_update_add_downlinks', {
                    "status": True,
                    "downlinks": [
                        {"ifId": "eth1/21"},
                        {"ifId": "eth1/22"}
                    ]
                }),
                description="更新會話 - 添加下行接口"
            ),
            
            # 更新會話 - 刪除接口
            self.create_test_case(
                name="excluded_vlan_update_session_remove_interfaces",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_session_operations",
                module="excluded_vlan",
                params={"sessionId": "1"},
                body=self.test_data.get('excluded_vlan_update_remove_interfaces', {
                    "status": False,
                    "uplinks": [
                        {"ifId": "eth1/1"}
                    ]
                }),
                description="更新會話 - 刪除接口"
            ),
            
            # 更新會話 - 修改排除VLAN
            self.create_test_case(
                name="excluded_vlan_update_session_modify_vlans",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_session_operations",
                module="excluded_vlan",
                params={"sessionId": "3"},
                body=self.test_data.get('excluded_vlan_update_modify_vlans', {
                    "status": True,
                    "excludedVlans": ["350", "351"]
                }),
                description="更新會話 - 修改排除VLAN"
            ),
            
            # 更新會話 - 複合操作
            self.create_test_case(
                name="excluded_vlan_update_session_complex",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_session_operations",
                module="excluded_vlan",
                params={"sessionId": "2"},
                body=self.test_data.get('excluded_vlan_update_complex', {
                    "status": True,
                    "excludedVlans": ["250"],
                    "uplinks": [
                        {"ifId": "trunk3"}
                    ],
                    "downlinks": [
                        {"ifId": "eth1/25"}
                    ]
                }),
                description="更新會話 - 複合操作"
            ),
            
            # 測試無效會話ID查詢
            self.create_test_case(
                name="excluded_vlan_test_invalid_session_query",
                method="GET",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_session_operations",
                module="excluded_vlan",
                params={"sessionId": "10"},
                expected_status=400,
                description="測試無效會話ID查詢"
            ),
            
            # 驗證會話更新
            self.create_test_case(
                name="excluded_vlan_verify_session_updates",
                method="GET",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_session_operations",
                module="excluded_vlan",
                params={"sessionId": "1"},
                description="驗證會話更新結果"
            )
        ]
    
    def get_excluded_vlan_interface_config_tests(self) -> List[APITestCase]:
        """ExcludedVlan Interface Configuration API 測試案例"""
        return [
            # 配置單一上行接口會話
            self.create_test_case(
                name="excluded_vlan_config_single_uplink",
                method="POST",
                url="/api/v1/excluded-vlan/sessions",
                category="excluded_vlan_interface_config",
                module="excluded_vlan",
                body=self.test_data.get('excluded_vlan_single_uplink', {
                    "sessionId": 1,
                    "excludedVlans": ["700"],
                    "uplinks": [
                        {"ifId": "eth1/30"}
                    ]
                }),
                description="配置單一上行接口會話"
            ),
            
            # 配置多上行接口會話
            self.create_test_case(
                name="excluded_vlan_config_multi_uplinks",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_interface_config",
                module="excluded_vlan",
                params={"sessionId": "1"},
                body=self.test_data.get('excluded_vlan_multi_uplinks', {
                    "status": True,
                    "uplinks": [
                        {"ifId": "eth1/31"},
                        {"ifId": "eth1/32"},
                        {"ifId": "eth1/33"}
                    ]
                }),
                description="配置多上行接口會話"
            ),
            
            # 配置單一下行接口會話
            self.create_test_case(
                name="excluded_vlan_config_single_downlink",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_interface_config",
                module="excluded_vlan",
                params={"sessionId": "1"},
                body=self.test_data.get('excluded_vlan_single_downlink', {
                    "status": True,
                    "downlinks": [
                        {"ifId": "eth1/40"}
                    ]
                }),
                description="配置單一下行接口會話"
            ),
            
            # 配置多下行接口會話
            self.create_test_case(
                name="excluded_vlan_config_multi_downlinks",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_interface_config",
                module="excluded_vlan",
                params={"sessionId": "1"},
                body=self.test_data.get('excluded_vlan_multi_downlinks', {
                    "status": True,
                    "downlinks": [
                        {"ifId": "eth1/41"},
                        {"ifId": "eth1/42"},
                        {"ifId": "eth1/43"},
                        {"ifId": "eth1/44"}
                    ]
                }),
                description="配置多下行接口會話"
            ),
            
            # 配置混合接口類型
            self.create_test_case(
                name="excluded_vlan_config_mixed_interface_types",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_interface_config",
                module="excluded_vlan",
                params={"sessionId": "1"},
                body=self.test_data.get('excluded_vlan_mixed_interfaces', {
                    "status": True,
                    "uplinks": [
                        {"ifId": "eth1/50"},
                        {"ifId": "trunk10"}
                    ],
                    "downlinks": [
                        {"ifId": "eth1/51"},
                        {"ifId": "eth1/52"},
                        {"ifId": "trunk11"}
                    ]
                }),
                description="配置混合接口類型 (Ethernet + Port Channel)"
            ),
            
            # 測試無效接口ID
            self.create_test_case(
                name="excluded_vlan_test_invalid_interface_id",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_interface_config",
                module="excluded_vlan",
                params={"sessionId": "1"},
                body=self.test_data.get('excluded_vlan_invalid_interface', {
                    "status": True,
                    "uplinks": [
                        {"ifId": "invalid-interface"}
                    ]
                }),
                expected_status=400,
                description="測試無效接口ID"
            ),
            
            # 測試Port Channel範圍
            self.create_test_case(
                name="excluded_vlan_test_port_channel_range",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_interface_config",
                module="excluded_vlan",
                params={"sessionId": "1"},
                body=self.test_data.get('excluded_vlan_port_channel_range', {
                    "status": True,
                    "uplinks": [
                        {"ifId": "trunk26"},
                        {"ifId": "trunk1"}
                    ]
                }),
                description="測試Port Channel範圍 (trunk1-trunk26)"
            ),
            
            # 驗證接口配置
            self.create_test_case(
                name="excluded_vlan_verify_interface_config",
                method="GET",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_interface_config",
                module="excluded_vlan",
                params={"sessionId": "1"},
                description="驗證接口配置結果"
            )
        ]
    
    def get_excluded_vlan_configuration_tests(self) -> List[APITestCase]:
        """ExcludedVlan Configuration API 測試案例"""
        return [
            # 配置單一排除VLAN
            self.create_test_case(
                name="excluded_vlan_config_single_vlan",
                method="POST",
                url="/api/v1/excluded-vlan/sessions",
                category="excluded_vlan_configuration",
                module="excluded_vlan",
                body=self.test_data.get('excluded_vlan_single_vlan', {
                    "sessionId": 2,
                    "excludedVlans": ["800"],
                    "uplinks": [
                        {"ifId": "eth2/1"}
                    ],
                    "downlinks": [
                        {"ifId": "eth2/2"}
                    ]
                }),
                description="配置單一排除VLAN"
            ),
            
            # 配置多個排除VLAN
            self.create_test_case(
                name="excluded_vlan_config_multiple_vlans",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_configuration",
                module="excluded_vlan",
                params={"sessionId": "2"},
                body=self.test_data.get('excluded_vlan_multiple_vlans', {
                    "status": True,
                    "excludedVlans": ["801", "802", "803", "804"]
                }),
                description="配置多個排除VLAN"
            ),
            
            # 配置最大排除VLAN數量
            self.create_test_case(
                name="excluded_vlan_config_max_vlans",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_configuration",
                module="excluded_vlan",
                params={"sessionId": "2"},
                body=self.test_data.get('excluded_vlan_max_vlans', {
                    "status": True,
                    "excludedVlans": ["810", "811", "812", "813", "814", "815", "816", "817"]
                }),
                description="配置最大排除VLAN數量 (8個)"
            ),
            
            # 配置VLAN範圍 - 低VLAN ID
            self.create_test_case(
                name="excluded_vlan_config_low_vlan_range",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_configuration",
                module="excluded_vlan",
                params={"sessionId": "2"},
                body=self.test_data.get('excluded_vlan_low_range', {
                    "status": True,
                    "excludedVlans": ["1", "2", "10", "50"]
                }),
                description="配置VLAN範圍 - 低VLAN ID"
            ),
            
            # 配置VLAN範圍 - 高VLAN ID
            self.create_test_case(
                name="excluded_vlan_config_high_vlan_range",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_configuration",
                module="excluded_vlan",
                params={"sessionId": "2"},
                body=self.test_data.get('excluded_vlan_high_range', {
                    "status": True,
                    "excludedVlans": ["4000", "4050", "4090", "4094"]
                }),
                description="配置VLAN範圍 - 高VLAN ID (接近4094)"
            ),
            
            # 配置帶掩碼的VLAN
            self.create_test_case(
                name="excluded_vlan_config_vlan_with_mask",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_configuration",
                module="excluded_vlan",
                params={"sessionId": "2"},
                body=self.test_data.get('excluded_vlan_with_mask', {
                    "status": True,
                    "excludedVlans": ["100/4095", "200/4095"]
                }),
                description="配置帶掩碼的VLAN"
            ),
            
            # 測試超過最大VLAN數量
            self.create_test_case(
                name="excluded_vlan_test_exceed_max_vlans",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_configuration",
                module="excluded_vlan",
                params={"sessionId": "2"},
                body=self.test_data.get('excluded_vlan_exceed_max', {
                    "status": True,
                    "excludedVlans": ["900", "901", "902", "903", "904", "905", "906", "907", "908"]  # 9個VLAN，超過最大8個
                }),
                expected_status=400,
                description="測試超過最大VLAN數量"
            ),
            
            # 測試無效VLAN ID
            self.create_test_case(
                name="excluded_vlan_test_invalid_vlan_id",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_configuration",
                module="excluded_vlan",
                params={"sessionId": "2"},
                body=self.test_data.get('excluded_vlan_invalid_vlan', {
                    "status": True,
                    "excludedVlans": ["4095"]  # 超出範圍 1-4094
                }),
                expected_status=400,
                description="測試無效VLAN ID"
            ),
            
            # 驗證VLAN配置
            self.create_test_case(
                name="excluded_vlan_verify_vlan_config",
                method="GET",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_configuration",
                module="excluded_vlan",
                params={"sessionId": "2"},
                description="驗證排除VLAN配置結果"
            )
        ]
    
    def get_excluded_vlan_advanced_operations_tests(self) -> List[APITestCase]:
        """ExcludedVlan Advanced Operations API 測試案例"""
        return [
            # 創建完整配置會話
            self.create_test_case(
                name="excluded_vlan_create_complete_session",
                method="POST",
                url="/api/v1/excluded-vlan/sessions",
                category="excluded_vlan_advanced_operations",
                module="excluded_vlan",
                body=self.test_data.get('excluded_vlan_complete_session', {
                    "sessionId": 3,
                    "excludedVlans": ["1000", "1001", "1002"],
                    "uplinks": [
                        {"ifId": "eth3/1"},
                        {"ifId": "trunk20"}
                    ],
                    "downlinks": [
                        {"ifId": "eth3/2"},
                        {"ifId": "eth3/3"},
                        {"ifId": "eth3/4"},
                        {"ifId": "trunk21"}
                    ]
                }),
                description="創建完整配置會話"
            ),
            
            # 批量更新會話配置
            self.create_test_case(
                name="excluded_vlan_batch_update_session",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_advanced_operations",
                module="excluded_vlan",
                params={"sessionId": "3"},
                body=self.test_data.get('excluded_vlan_batch_update', {
                    "status": True,
                    "excludedVlans": ["1100", "1101"],
                    "uplinks": [
                        {"ifId": "eth3/10"}
                    ],
                    "downlinks": [
                        {"ifId": "eth3/11"},
                        {"ifId": "eth3/12"}
                    ]
                }),
                description="批量更新會話配置"
            ),
            
            # 清空會話接口
            self.create_test_case(
                name="excluded_vlan_clear_session_interfaces",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_advanced_operations",
                module="excluded_vlan",
                params={"sessionId": "3"},
                body=self.test_data.get('excluded_vlan_clear_interfaces', {
                    "status": False,
                    "uplinks": [
                        {"ifId": "eth3/1"},
                        {"ifId": "trunk20"},
                        {"ifId": "eth3/10"}
                    ],
                    "downlinks": [
                        {"ifId": "eth3/2"},
                        {"ifId": "eth3/3"},
                        {"ifId": "eth3/4"},
                        {"ifId": "trunk21"},
                        {"ifId": "eth3/11"},
                        {"ifId": "eth3/12"}
                    ]
                }),
                description="清空會話接口配置"
            ),
            
            # 重新配置會話
            self.create_test_case(
                name="excluded_vlan_reconfigure_session",
                method="PUT",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_advanced_operations",
                module="excluded_vlan",
                params={"sessionId": "3"},
                body=self.test_data.get('excluded_vlan_reconfigure', {
                    "status": True,
                    "excludedVlans": ["1200"],
                    "uplinks": [
                        {"ifId": "eth3/20"}
                    ],
                    "downlinks": [
                        {"ifId": "eth3/21"}
                    ]
                }),
                description="重新配置會話"
            ),
            
            # 刪除會話 - 會話1
            self.create_test_case(
                name="excluded_vlan_delete_session_1",
                method="DELETE",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_advanced_operations",
                module="excluded_vlan",
                params={"sessionId": "1"},
                description="刪除會話 - 會話1"
            ),
            
            # 刪除會話 - 會話2
            self.create_test_case(
                name="excluded_vlan_delete_session_2",
                method="DELETE",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_advanced_operations",
                module="excluded_vlan",
                params={"sessionId": "2"},
                description="刪除會話 - 會話2"
            ),
            
            # 刪除會話 - 會話3
            self.create_test_case(
                name="excluded_vlan_delete_session_3",
                method="DELETE",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_advanced_operations",
                module="excluded_vlan",
                params={"sessionId": "3"},
                description="刪除會話 - 會話3"
            ),
            
            # 測試刪除不存在的會話
            self.create_test_case(
                name="excluded_vlan_test_delete_nonexistent_session",
                method="DELETE",
                url="/api/v1/excluded-vlan/sessions/{sessionId}",
                category="excluded_vlan_advanced_operations",
                module="excluded_vlan",
                params={"sessionId": "10"},
                expected_status=400,
                description="測試刪除不存在的會話"
            ),
            
            # 驗證所有會話已刪除
            self.create_test_case(
                name="excluded_vlan_verify_all_sessions_deleted",
                method="GET",
                url="/api/v1/excluded-vlan/sessions",
                category="excluded_vlan_advanced_operations",
                module="excluded_vlan",
                description="驗證所有會話已刪除"
            ),
            
            # 重新創建測試會話
            self.create_test_case(
                name="excluded_vlan_recreate_test_session",
                method="POST",
                url="/api/v1/excluded-vlan/sessions",
                category="excluded_vlan_advanced_operations",
                module="excluded_vlan",
                body=self.test_data.get('excluded_vlan_recreate_session', {
                    "sessionId": 1,
                    "excludedVlans": ["2000"],
                    "uplinks": [
                        {"ifId": "eth4/1"}
                    ],
                    "downlinks": [
                        {"ifId": "eth4/2"}
                    ]
                }),
                description="重新創建測試會話"
            )
        ]