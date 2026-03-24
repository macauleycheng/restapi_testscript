#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLDP 模組測試案例
包含LLDP配置和遠程信息獲取相關API測試
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class LLDPTests(BaseTests):
    """LLDP 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取LLDP模組支援的類別"""
        return [
            "lldp_config",
            "lldp_remote_info"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有LLDP測試案例"""
        all_tests = []
        all_tests.extend(self.get_lldp_config_tests())
        all_tests.extend(self.get_lldp_remote_info_tests())
        return all_tests
    
    def get_lldp_config_tests(self) -> List[APITestCase]:
        """LLDP Configuration API 測試案例"""
        return [
            # 獲取LLDP配置
            self.create_test_case(
                name="lldp_get_configuration",
                method="GET",
                url="/api/v1/lldp",
                category="lldp_config",
                module="lldp",
                description="獲取LLDP配置信息"
            ),
            
            # 啟用LLDP並配置傳輸間隔
            self.create_test_case(
                name="lldp_enable_with_default_intervals",
                method="PUT",
                url="/api/v1/lldp",
                category="lldp_config",
                module="lldp",
                body=self.test_data.get('lldp_enable_default', {
                    "status": True,
                    "transmitInterval": 30,
                    "delayInterval": 2
                }),
                description="啟用LLDP並設置默認傳輸間隔"
            ),
            
            # 配置自定義LLDP參數
            self.create_test_case(
                name="lldp_configure_custom_intervals",
                method="PUT",
                url="/api/v1/lldp",
                category="lldp_config",
                module="lldp",
                body=self.test_data.get('lldp_custom_config', {
                    "status": True,
                    "transmitInterval": 60,
                    "delayInterval": 4
                }),
                description="配置自定義LLDP傳輸間隔"
            ),
            
            # 配置最小傳輸間隔
            self.create_test_case(
                name="lldp_configure_minimum_intervals",
                method="PUT",
                url="/api/v1/lldp",
                category="lldp_config",
                module="lldp",
                body=self.test_data.get('lldp_minimum_config', {
                    "status": True,
                    "transmitInterval": 5,
                    "delayInterval": 1
                }),
                description="配置最小LLDP傳輸間隔"
            ),
            
            # 配置最大傳輸間隔
            self.create_test_case(
                name="lldp_configure_maximum_intervals",
                method="PUT",
                url="/api/v1/lldp",
                category="lldp_config",
                module="lldp",
                body=self.test_data.get('lldp_maximum_config', {
                    "status": True,
                    "transmitInterval": 32768,
                    "delayInterval": 8192
                }),
                description="配置最大LLDP傳輸間隔"
            ),
            
            # 禁用LLDP
            self.create_test_case(
                name="lldp_disable",
                method="PUT",
                url="/api/v1/lldp",
                category="lldp_config",
                module="lldp",
                body=self.test_data.get('lldp_disable', {
                    "status": False,
                    "transmitInterval": 20,
                    "delayInterval": 1
                }),
                description="禁用LLDP功能"
            ),
            
            # 測試無效的延遲間隔配置 (4*txDelay > transmitInterval)
            self.create_test_case(
                name="lldp_configure_invalid_delay",
                method="PUT",
                url="/api/v1/lldp",
                category="lldp_config",
                module="lldp",
                body=self.test_data.get('lldp_invalid_delay', {
                    "status": True,
                    "transmitInterval": 10,
                    "delayInterval": 5  # 4*5=20 > 10, 應該失敗
                }),
                expected_status=400,
                description="測試無效延遲間隔配置 (4*txDelay > transmitInterval)"
            ),
            
            # 重新啟用LLDP以便後續測試
            self.create_test_case(
                name="lldp_re_enable_for_testing",
                method="PUT",
                url="/api/v1/lldp",
                category="lldp_config",
                module="lldp",
                body=self.test_data.get('lldp_re_enable', {
                    "status": True,
                    "transmitInterval": 30,
                    "delayInterval": 2
                }),
                description="重新啟用LLDP以便進行遠程信息測試"
            )
        ]
    
    def get_lldp_remote_info_tests(self) -> List[APITestCase]:
        """LLDP Remote Information API 測試案例"""
        return [
            # 獲取所有接口的LLDP遠程信息
            self.create_test_case(
                name="lldp_get_all_remote_info",
                method="GET",
                url="/api/v1/lldp/interfaces",
                category="lldp_remote_info",
                module="lldp",
                description="獲取所有接口的LLDP遠程信息"
            ),
            
            # 獲取特定接口的LLDP遠程信息 - eth1/3
            self.create_test_case(
                name="lldp_get_interface_eth1_3_remote_info",
                method="GET",
                url="/api/v1/lldp/interfaces/{id}",
                category="lldp_remote_info",
                module="lldp",
                params={"id": "eth1%2f3"},
                description="獲取接口 eth1/3 的LLDP遠程信息"
            ),
            
            # 獲取特定接口的LLDP遠程信息 - eth1/9
            self.create_test_case(
                name="lldp_get_interface_eth1_9_remote_info",
                method="GET",
                url="/api/v1/lldp/interfaces/{id}",
                category="lldp_remote_info",
                module="lldp",
                params={"id": "eth1%2f9"},
                description="獲取接口 eth1/9 的LLDP遠程信息"
            ),
            
            # 獲取參數化接口的LLDP遠程信息
            self.create_test_case(
                name="lldp_get_parameterized_interface_remote_info",
                method="GET",
                url="/api/v1/lldp/interfaces/{id}",
                category="lldp_remote_info",
                module="lldp",
                params={"id": self.params.get('interface_id', 'eth1%2f1')},
                description=f"獲取接口 {self.params.get('interface_id', 'eth1/1')} 的LLDP遠程信息"
            ),
            
            # 獲取多個接口的LLDP遠程信息
            self.create_test_case(
                name="lldp_get_interface_eth1_1_remote_info",
                method="GET",
                url="/api/v1/lldp/interfaces/{id}",
                category="lldp_remote_info",
                module="lldp",
                params={"id": "eth1%2f1"},
                description="獲取接口 eth1/1 的LLDP遠程信息"
            ),
            
            self.create_test_case(
                name="lldp_get_interface_eth1_2_remote_info",
                method="GET",
                url="/api/v1/lldp/interfaces/{id}",
                category="lldp_remote_info",
                module="lldp",
                params={"id": "eth1%2f2"},
                description="獲取接口 eth1/2 的LLDP遠程信息"
            ),
            
            self.create_test_case(
                name="lldp_get_interface_eth1_4_remote_info",
                method="GET",
                url="/api/v1/lldp/interfaces/{id}",
                category="lldp_remote_info",
                module="lldp",
                params={"id": "eth1%2f4"},
                description="獲取接口 eth1/4 的LLDP遠程信息"
            ),
            
            self.create_test_case(
                name="lldp_get_interface_eth1_5_remote_info",
                method="GET",
                url="/api/v1/lldp/interfaces/{id}",
                category="lldp_remote_info",
                module="lldp",
                params={"id": "eth1%2f5"},
                description="獲取接口 eth1/5 的LLDP遠程信息"
            ),
            
            # 獲取Trunk接口的LLDP遠程信息
            self.create_test_case(
                name="lldp_get_trunk_interface_remote_info",
                method="GET",
                url="/api/v1/lldp/interfaces/{id}",
                category="lldp_remote_info",
                module="lldp",
                params={"id": self.params.get('trunk_interface_id', 'trunk1')},
                description=f"獲取Trunk接口 {self.params.get('trunk_interface_id', 'trunk1')} 的LLDP遠程信息"
            ),
            
            # 獲取不存在接口的LLDP遠程信息 (應該返回404或空結果)
            self.create_test_case(
                name="lldp_get_nonexistent_interface_remote_info",
                method="GET",
                url="/api/v1/lldp/interfaces/{id}",
                category="lldp_remote_info",
                module="lldp",
                params={"id": "eth1%2f99"},
                expected_status=404,
                description="獲取不存在接口 eth1/99 的LLDP遠程信息 (測試錯誤處理)"
            ),
            
            # 定期檢查LLDP遠程信息更新
            self.create_test_case(
                name="lldp_monitor_remote_info_changes_1",
                method="GET",
                url="/api/v1/lldp/interfaces",
                category="lldp_remote_info",
                module="lldp",
                description="監控LLDP遠程信息變化 - 第1次檢查"
            ),
            
            self.create_test_case(
                name="lldp_monitor_remote_info_changes_2",
                method="GET",
                url="/api/v1/lldp/interfaces",
                category="lldp_remote_info",
                module="lldp",
                description="監控LLDP遠程信息變化 - 第2次檢查"
            ),
            
            # 驗證LLDP信息的完整性
            self.create_test_case(
                name="lldp_verify_complete_neighbor_info",
                method="GET",
                url="/api/v1/lldp/interfaces/{id}",
                category="lldp_remote_info",
                module="lldp",
                params={"id": "eth1%2f3"},
                description="驗證接口 eth1/3 的完整LLDP鄰居信息 (包含managementAddress、softwareRevision、serialNumber)"
            )
        ]