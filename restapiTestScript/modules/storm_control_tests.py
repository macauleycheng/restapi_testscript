#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Storm Control 模組測試案例
包含廣播風暴控制、組播風暴控制、未知單播風暴控制等相關API測試
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class STORM_CONTROLTests(BaseTests):
    """Storm Control 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取Storm Control模組支援的類別"""
        return [
            "storm_control_ethernet",
            "storm_control_port_channel",
            "storm_control_broadcast",
            "storm_control_multicast", 
            "storm_control_unknown_unicast"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有Storm Control測試案例"""
        all_tests = []
        all_tests.extend(self.get_ethernet_storm_control_tests())
        all_tests.extend(self.get_port_channel_storm_control_tests())
        all_tests.extend(self.get_broadcast_storm_control_tests())
        all_tests.extend(self.get_multicast_storm_control_tests())
        all_tests.extend(self.get_unknown_unicast_storm_control_tests())
        return all_tests
    
    def get_ethernet_storm_control_tests(self) -> List[APITestCase]:
        """Ethernet接口風暴控制測試案例"""
        return [
            # 獲取Ethernet接口風暴控制信息
            self.create_test_case(
                name="storm_control_get_ethernet_info",
                method="GET",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_ethernet",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                description="獲取Ethernet接口風暴控制信息"
            ),
            
            # 獲取參數化Ethernet接口風暴控制信息
            self.create_test_case(
                name="storm_control_get_parameterized_ethernet_info",
                method="GET",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_ethernet",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                description=f"獲取接口 {self.params.get('interface_id', 'eth1/1')} 風暴控制信息"
            ),
            
            # 配置Ethernet接口風暴控制 - 啟用所有類型
            self.create_test_case(
                name="storm_control_configure_ethernet_all_enabled",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_ethernet",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                body=self.test_data.get('storm_control_all_enabled', {
                    "bcastStatus": True,
                    "bcastRate": 1000,
                    "mcastStatus": True,
                    "mcastRate": 1000,
                    "unknownUcastStatus": True,
                    "unknownUcastRate": 1000
                }),
                description="配置Ethernet接口 - 啟用所有風暴控制"
            ),
            
            # 配置Ethernet接口風暴控制 - 最小速率
            self.create_test_case(
                name="storm_control_configure_ethernet_min_rate",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_ethernet",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                body=self.test_data.get('storm_control_min_rate', {
                    "bcastStatus": True,
                    "bcastRate": 500,
                    "mcastStatus": True,
                    "mcastRate": 500,
                    "unknownUcastStatus": True,
                    "unknownUcastRate": 500
                }),
                description="配置Ethernet接口 - 最小速率風暴控制"
            ),
            
            # 配置Ethernet接口風暴控制 - 最大速率
            self.create_test_case(
                name="storm_control_configure_ethernet_max_rate",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_ethernet",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                body=self.test_data.get('storm_control_max_rate', {
                    "bcastStatus": True,
                    "bcastRate": 14881000,
                    "mcastStatus": True,
                    "mcastRate": 14881000,
                    "unknownUcastStatus": True,
                    "unknownUcastRate": 14881000
                }),
                description="配置Ethernet接口 - 最大速率風暴控制"
            ),
            
            # 禁用Ethernet接口所有風暴控制
            self.create_test_case(
                name="storm_control_disable_ethernet_all",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_ethernet",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                body=self.test_data.get('storm_control_all_disabled', {
                    "bcastStatus": False,
                    "mcastStatus": False,
                    "unknownUcastStatus": False
                }),
                description="禁用Ethernet接口所有風暴控制"
            ),
            
            # 測試無效Ethernet接口ID
            self.create_test_case(
                name="storm_control_test_invalid_ethernet_interface",
                method="GET",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_ethernet",
                module="storm_control",
                params={"ifId": "eth99%2f99"},
                expected_status=400,
                description="測試無效Ethernet接口ID"
            ),
            
            # 測試無效速率值 - 低於最小值
            self.create_test_case(
                name="storm_control_test_invalid_rate_low",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_ethernet",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                body=self.test_data.get('storm_control_invalid_rate_low', {
                    "bcastStatus": True,
                    "bcastRate": 100  # 低於最小值 500
                }),
                expected_status=400,
                description="測試無效速率值 - 低於最小值"
            ),
            
            # 測試無效速率值 - 超過最大值
            self.create_test_case(
                name="storm_control_test_invalid_rate_high",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_ethernet",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1')},
                body=self.test_data.get('storm_control_invalid_rate_high', {
                    "bcastStatus": True,
                    "bcastRate": 20000000  # 超過最大值 14881000
                }),
                expected_status=400,
                description="測試無效速率值 - 超過最大值"
            )
        ]
    
    def get_port_channel_storm_control_tests(self) -> List[APITestCase]:
        """Port Channel接口風暴控制測試案例"""
        return [
            # 獲取Port Channel接口風暴控制信息
            self.create_test_case(
                name="storm_control_get_port_channel_info",
                method="GET",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_port_channel",
                module="storm_control",
                params={"ifId": "trunk1"},
                description="獲取Port Channel接口風暴控制信息"
            ),
            
            # 獲取參數化Port Channel接口風暴控制信息
            self.create_test_case(
                name="storm_control_get_parameterized_port_channel_info",
                method="GET",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_port_channel",
                module="storm_control",
                params={"ifId": self.params.get('trunk_interface_id', 'trunk1')},
                description=f"獲取Port Channel {self.params.get('trunk_interface_id', 'trunk1')} 風暴控制信息"
            ),
            
            # 配置Port Channel接口風暴控制
            self.create_test_case(
                name="storm_control_configure_port_channel",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_port_channel",
                module="storm_control",
                params={"ifId": "trunk1"},
                body=self.test_data.get('storm_control_port_channel', {
                    "bcastStatus": True,
                    "bcastRate": 2000,
                    "mcastStatus": True,
                    "mcastRate": 2000,
                    "unknownUcastStatus": True,
                    "unknownUcastRate": 2000
                }),
                description="配置Port Channel接口風暴控制"
            ),
            
            # 測試無效Port Channel接口ID
            self.create_test_case(
                name="storm_control_test_invalid_port_channel_interface",
                method="GET",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_port_channel",
                module="storm_control",
                params={"ifId": "trunk99"},
                expected_status=400,
                description="測試無效Port Channel接口ID"
            ),
            
            # 禁用Port Channel風暴控制
            self.create_test_case(
                name="storm_control_disable_port_channel",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_port_channel",
                module="storm_control",
                params={"ifId": "trunk1"},
                body=self.test_data.get('storm_control_port_channel_disabled', {
                    "bcastStatus": False,
                    "mcastStatus": False,
                    "unknownUcastStatus": False
                }),
                description="禁用Port Channel風暴控制"
            )
        ]
    
    def get_broadcast_storm_control_tests(self) -> List[APITestCase]:
        """廣播風暴控制測試案例"""
        return [
            # 啟用廣播風暴控制 - 低速率
            self.create_test_case(
                name="storm_control_enable_broadcast_low_rate",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_broadcast",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f2')},
                body=self.test_data.get('storm_control_broadcast_low', {
                    "bcastStatus": True,
                    "bcastRate": 800
                }),
                description="啟用廣播風暴控制 - 低速率"
            ),
            
            # 啟用廣播風暴控制 - 中等速率
            self.create_test_case(
                name="storm_control_enable_broadcast_medium_rate",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_broadcast",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f2')},
                body=self.test_data.get('storm_control_broadcast_medium', {
                    "bcastStatus": True,
                    "bcastRate": 5000
                }),
                description="啟用廣播風暴控制 - 中等速率"
            ),
            
            # 啟用廣播風暴控制 - 高速率
            self.create_test_case(
                name="storm_control_enable_broadcast_high_rate",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_broadcast",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f2')},
                body=self.test_data.get('storm_control_broadcast_high', {
                    "bcastStatus": True,
                    "bcastRate": 10000000
                }),
                description="啟用廣播風暴控制 - 高速率"
            ),
            
            # 禁用廣播風暴控制
            self.create_test_case(
                name="storm_control_disable_broadcast",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_broadcast",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f2')},
                body=self.test_data.get('storm_control_broadcast_disabled', {
                    "bcastStatus": False
                }),
                description="禁用廣播風暴控制"
            ),
            
            # 驗證廣播風暴控制配置
            self.create_test_case(
                name="storm_control_verify_broadcast_config",
                method="GET",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_broadcast",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f2')},
                description="驗證廣播風暴控制配置"
            )
        ]
    
    def get_multicast_storm_control_tests(self) -> List[APITestCase]:
        """組播風暴控制測試案例"""
        return [
            # 啟用組播風暴控制 - 低速率
            self.create_test_case(
                name="storm_control_enable_multicast_low_rate",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_multicast",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f3')},
                body=self.test_data.get('storm_control_multicast_low', {
                    "mcastStatus": True,
                    "mcastRate": 600
                }),
                description="啟用組播風暴控制 - 低速率"
            ),
            
            # 啟用組播風暴控制 - 中等速率
            self.create_test_case(
                name="storm_control_enable_multicast_medium_rate",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_multicast",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f3')},
                body=self.test_data.get('storm_control_multicast_medium', {
                    "mcastStatus": True,
                    "mcastRate": 3000
                }),
                description="啟用組播風暴控制 - 中等速率"
            ),
            
            # 啟用組播風暴控制 - 高速率
            self.create_test_case(
                name="storm_control_enable_multicast_high_rate",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_multicast",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f3')},
                body=self.test_data.get('storm_control_multicast_high', {
                    "mcastStatus": True,
                    "mcastRate": 8000000
                }),
                description="啟用組播風暴控制 - 高速率"
            ),
            
            # 禁用組播風暴控制
            self.create_test_case(
                name="storm_control_disable_multicast",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_multicast",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f3')},
                body=self.test_data.get('storm_control_multicast_disabled', {
                    "mcastStatus": False
                }),
                description="禁用組播風暴控制"
            ),
            
            # 驗證組播風暴控制配置
            self.create_test_case(
                name="storm_control_verify_multicast_config",
                method="GET",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_multicast",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f3')},
                description="驗證組播風暴控制配置"
            )
        ]
    
    def get_unknown_unicast_storm_control_tests(self) -> List[APITestCase]:
        """未知單播風暴控制測試案例"""
        return [
            # 啟用未知單播風暴控制 - 低速率
            self.create_test_case(
                name="storm_control_enable_unknown_unicast_low_rate",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_unknown_unicast",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f4')},
                body=self.test_data.get('storm_control_unknown_unicast_low', {
                    "unknownUcastStatus": True,
                    "unknownUcastRate": 700
                }),
                description="啟用未知單播風暴控制 - 低速率"
            ),
            
            # 啟用未知單播風暴控制 - 中等速率
            self.create_test_case(
                name="storm_control_enable_unknown_unicast_medium_rate",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_unknown_unicast",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f4')},
                body=self.test_data.get('storm_control_unknown_unicast_medium', {
                    "unknownUcastStatus": True,
                    "unknownUcastRate": 4000
                }),
                description="啟用未知單播風暴控制 - 中等速率"
            ),
            
            # 啟用未知單播風暴控制 - 高速率
            self.create_test_case(
                name="storm_control_enable_unknown_unicast_high_rate",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_unknown_unicast",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f4')},
                body=self.test_data.get('storm_control_unknown_unicast_high', {
                    "unknownUcastStatus": True,
                    "unknownUcastRate": 12000000
                }),
                description="啟用未知單播風暴控制 - 高速率"
            ),
            
            # 禁用未知單播風暴控制
            self.create_test_case(
                name="storm_control_disable_unknown_unicast",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_unknown_unicast",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f4')},
                body=self.test_data.get('storm_control_unknown_unicast_disabled', {
                    "unknownUcastStatus": False
                }),
                description="禁用未知單播風暴控制"
            ),
            
            # 驗證未知單播風暴控制配置
            self.create_test_case(
                name="storm_control_verify_unknown_unicast_config",
                method="GET",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_unknown_unicast",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f4')},
                description="驗證未知單播風暴控制配置"
            ),
            
            # 測試組合配置 - 同時啟用多種風暴控制
            self.create_test_case(
                name="storm_control_test_combined_configuration",
                method="PUT",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_unknown_unicast",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f5')},
                body=self.test_data.get('storm_control_combined', {
                    "bcastStatus": True,
                    "bcastRate": 1500,
                    "mcastStatus": True,
                    "mcastRate": 1200,
                    "unknownUcastStatus": True,
                    "unknownUcastRate": 1800
                }),
                description="測試組合配置 - 同時啟用多種風暴控制"
            ),
            
            # 驗證組合配置效果
            self.create_test_case(
                name="storm_control_verify_combined_configuration",
                method="GET",
                url="/api/v1/storm-control/interfaces/{ifId}",
                category="storm_control_unknown_unicast",
                module="storm_control",
                params={"ifId": self.params.get('interface_id', 'eth1%2f5')},
                description="驗證組合配置效果"
            )
        ]