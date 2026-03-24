#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COS 模組測試案例
包含COS隊列管理、接口默認優先級、QoS映射等相關API測試
支援隊列模式配置、權重設置、優先級映射、DSCP映射、信任模式等操作
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class COSTests(BaseTests):
    """COS 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取COS模組支援的類別"""
        return [
            "cos_queue_management",
            "cos_queue_configuration",
            "cos_interface_priority",
            "cos_qos_mapping",
            "cos_qos_configuration",
            "cos_advanced_operations"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有COS測試案例"""
        all_tests = []
        all_tests.extend(self.get_cos_queue_management_tests())
        all_tests.extend(self.get_cos_queue_configuration_tests())
        all_tests.extend(self.get_cos_interface_priority_tests())
        all_tests.extend(self.get_cos_qos_mapping_tests())
        all_tests.extend(self.get_cos_qos_configuration_tests())
        all_tests.extend(self.get_cos_advanced_operations_tests())     
        return all_tests
    
    def get_cos_queue_management_tests(self) -> List[APITestCase]:
        """COS Queue Management API 測試案例"""
        return [
            # 獲取隊列模式和權重
            self.create_test_case(
                name="cos_get_queue_mode_and_weight",
                method="GET",
                url="/api/v1/cos/queues",
                category="cos_queue_management",
                module="cos",
                description="獲取隊列模式和權重"
            ),
            
            # 設置隊列模式 - WRR模式
            self.create_test_case(
                name="cos_set_queue_mode_wrr",
                method="PUT",
                url="/api/v1/cos/queues",
                category="cos_queue_management",
                module="cos",
                body=self.test_data.get('cos_queue_wrr_mode', {
                    "queueMode": "wrr",
                    "queues": [
                        {"property": 0, "weight": 1},
                        {"property": 0, "weight": 2},
                        {"property": 0, "weight": 3},
                        {"property": 0, "weight": 4},
                        {"property": 0, "weight": 5},
                        {"property": 0, "weight": 6},
                        {"property": 0, "weight": 7},
                        {"property": 0, "weight": 8}
                    ]
                }),
                description="設置隊列模式 - WRR模式"
            ),
            
            # 設置隊列模式 - Strict模式
            self.create_test_case(
                name="cos_set_queue_mode_strict",
                method="PUT",
                url="/api/v1/cos/queues",
                category="cos_queue_management",
                module="cos",
                body=self.test_data.get('cos_queue_strict_mode', {
                    "queueMode": "strict",
                    "queues": [
                        {"property": 1, "weight": 1},
                        {"property": 1, "weight": 1},
                        {"property": 1, "weight": 1},
                        {"property": 1, "weight": 1},
                        {"property": 1, "weight": 1},
                        {"property": 1, "weight": 1},
                        {"property": 1, "weight": 1},
                        {"property": 1, "weight": 1}
                    ]
                }),
                description="設置隊列模式 - Strict模式"
            ),
            
            # 設置隊列模式 - Strict-WRR混合模式
            self.create_test_case(
                name="cos_set_queue_mode_strict_wrr",
                method="PUT",
                url="/api/v1/cos/queues",
                category="cos_queue_management",
                module="cos",
                body=self.test_data.get('cos_queue_strict_wrr_mode', {
                    "queueMode": "strict-wrr",
                    "queues": [
                        {"property": 0, "weight": 10},
                        {"property": 0, "weight": 20},
                        {"property": 0, "weight": 30},
                        {"property": 0, "weight": 40},
                        {"property": 0, "weight": 50},
                        {"property": 0, "weight": 60},
                        {"property": 1, "weight": 1},
                        {"property": 1, "weight": 1}
                    ]
                }),
                description="設置隊列模式 - Strict-WRR混合模式"
            ),
            
            # 驗證隊列模式設置
            self.create_test_case(
                name="cos_verify_queue_mode_setting",
                method="GET",
                url="/api/v1/cos/queues",
                category="cos_queue_management",
                module="cos",
                description="驗證隊列模式設置"
            )
        ]
    
    def get_cos_queue_configuration_tests(self) -> List[APITestCase]:
        """COS Queue Configuration API 測試案例"""
        return [
            # 配置均等權重WRR
            self.create_test_case(
                name="cos_config_equal_weight_wrr",
                method="PUT",
                url="/api/v1/cos/queues",
                category="cos_queue_configuration",
                module="cos",
                body=self.test_data.get('cos_equal_weight_wrr', {
                    "queueMode": "wrr",
                    "queues": [
                        {"property": 0, "weight": 10},
                        {"property": 0, "weight": 10},
                        {"property": 0, "weight": 10},
                        {"property": 0, "weight": 10},
                        {"property": 0, "weight": 10},
                        {"property": 0, "weight": 10},
                        {"property": 0, "weight": 10},
                        {"property": 0, "weight": 10}
                    ]
                }),
                description="配置均等權重WRR"
            ),
            
            # 配置遞增權重WRR
            self.create_test_case(
                name="cos_config_incremental_weight_wrr",
                method="PUT",
                url="/api/v1/cos/queues",
                category="cos_queue_configuration",
                module="cos",
                body=self.test_data.get('cos_incremental_weight_wrr', {
                    "queueMode": "wrr",
                    "queues": [
                        {"property": 0, "weight": 5},
                        {"property": 0, "weight": 10},
                        {"property": 0, "weight": 15},
                        {"property": 0, "weight": 20},
                        {"property": 0, "weight": 25},
                        {"property": 0, "weight": 30},
                        {"property": 0, "weight": 35},
                        {"property": 0, "weight": 40}
                    ]
                }),
                description="配置遞增權重WRR"
            ),
            
            # 配置高優先級Strict隊列
            self.create_test_case(
                name="cos_config_high_priority_strict",
                method="PUT",
                url="/api/v1/cos/queues",
                category="cos_queue_configuration",
                module="cos",
                body=self.test_data.get('cos_high_priority_strict', {
                    "queueMode": "strict-wrr",
                    "queues": [
                        {"property": 0, "weight": 5},
                        {"property": 0, "weight": 10},
                        {"property": 0, "weight": 15},
                        {"property": 0, "weight": 20},
                        {"property": 0, "weight": 25},
                        {"property": 0, "weight": 30},
                        {"property": 1, "weight": 1},
                        {"property": 1, "weight": 1}
                    ]
                }),
                description="配置高優先級Strict隊列 (隊列6,7為Strict)"
            ),
            
            # 配置最大權重值
            self.create_test_case(
                name="cos_config_max_weight_values",
                method="PUT",
                url="/api/v1/cos/queues",
                category="cos_queue_configuration",
                module="cos",
                body=self.test_data.get('cos_max_weight_values', {
                    "queueMode": "wrr",
                    "queues": [
                        {"property": 0, "weight": 255},
                        {"property": 0, "weight": 255},
                        {"property": 0, "weight": 255},
                        {"property": 0, "weight": 255},
                        {"property": 0, "weight": 255},
                        {"property": 0, "weight": 255},
                        {"property": 0, "weight": 255},
                        {"property": 0, "weight": 255}
                    ]
                }),
                description="配置最大權重值 (255)"
            ),
            
            # 配置最小權重值
            self.create_test_case(
                name="cos_config_min_weight_values",
                method="PUT",
                url="/api/v1/cos/queues",
                category="cos_queue_configuration",
                module="cos",
                body=self.test_data.get('cos_min_weight_values', {
                    "queueMode": "wrr",
                    "queues": [
                        {"property": 0, "weight": 1},
                        {"property": 0, "weight": 1},
                        {"property": 0, "weight": 1},
                        {"property": 0, "weight": 1},
                        {"property": 0, "weight": 1},
                        {"property": 0, "weight": 1},
                        {"property": 0, "weight": 1},
                        {"property": 0, "weight": 1}
                    ]
                }),
                description="配置最小權重值 (1)"
            ),
            
            # 驗證隊列配置
            self.create_test_case(
                name="cos_verify_queue_configuration",
                method="GET",
                url="/api/v1/cos/queues",
                category="cos_queue_configuration",
                module="cos",
                description="驗證隊列配置"
            )
        ]
    
    def get_cos_interface_priority_tests(self) -> List[APITestCase]:
        """COS Interface Priority API 測試案例"""
        return [
            # 獲取接口默認優先級 - eth1/5
            self.create_test_case(
                name="cos_get_interface_priority_eth1_5",
                method="GET",
                url="/api/v1/cos/interfaces/eth1%2f5/default-priority",
                category="cos_interface_priority",
                module="cos",
                description="獲取接口默認優先級 - eth1/5"
            ),
            
            # 設置接口默認優先級 - eth1/5 優先級0
            self.create_test_case(
                name="cos_set_interface_priority_eth1_5_0",
                method="PUT",
                url="/api/v1/cos/interfaces/eth1%2f5/default-priority",
                category="cos_interface_priority",
                module="cos",
                body=self.test_data.get('cos_interface_priority_0', {
                    "priority": 0
                }),
                description="設置接口默認優先級 - eth1/5 優先級0"
            ),
            
            # 設置接口默認優先級 - eth1/5 優先級3
            self.create_test_case(
                name="cos_set_interface_priority_eth1_5_3",
                method="PUT",
                url="/api/v1/cos/interfaces/eth1%2f5/default-priority",
                category="cos_interface_priority",
                module="cos",
                body=self.test_data.get('cos_interface_priority_3', {
                    "priority": 3
                }),
                description="設置接口默認優先級 - eth1/5 優先級3"
            ),
            
            # 設置接口默認優先級 - eth1/5 最高優先級7
            self.create_test_case(
                name="cos_set_interface_priority_eth1_5_7",
                method="PUT",
                url="/api/v1/cos/interfaces/eth1%2f5/default-priority",
                category="cos_interface_priority",
                module="cos",
                body=self.test_data.get('cos_interface_priority_7', {
                    "priority": 7
                }),
                description="設置接口默認優先級 - eth1/5 最高優先級7"
            ),
            
            # 獲取接口默認優先級 - eth1/1
            self.create_test_case(
                name="cos_get_interface_priority_eth1_1",
                method="GET",
                url="/api/v1/cos/interfaces/eth1%2f1/default-priority",
                category="cos_interface_priority",
                module="cos",
                description="獲取接口默認優先級 - eth1/1"
            ),
            
            # 設置接口默認優先級 - eth1/1 優先級5
            self.create_test_case(
                name="cos_set_interface_priority_eth1_1_5",
                method="PUT",
                url="/api/v1/cos/interfaces/eth1%2f1/default-priority",
                category="cos_interface_priority",
                module="cos",
                body=self.test_data.get('cos_interface_priority_5', {
                    "priority": 5
                }),
                description="設置接口默認優先級 - eth1/1 優先級5"
            ),
            
            # 設置Trunk接口默認優先級 - trunk1
            self.create_test_case(
                name="cos_set_trunk_priority_trunk1",
                method="PUT",
                url="/api/v1/cos/interfaces/trunk1/default-priority",
                category="cos_interface_priority",
                module="cos",
                body=self.test_data.get('cos_trunk_priority_4', {
                    "priority": 4
                }),
                description="設置Trunk接口默認優先級 - trunk1 優先級4"
            ),
            
            # 獲取參數化接口優先級
            self.create_test_case(
                name="cos_get_parameterized_interface_priority",
                method="GET",
                url="/api/v1/cos/interfaces/{ifId}/default-priority",
                category="cos_interface_priority",
                module="cos",
                params={"ifId": self.params.get('cos_interface_id', 'eth1%2f5')},
                description=f"獲取參數化接口優先級 - {self.params.get('cos_interface_id', 'eth1/5')}"
            ),
            
            # 驗證接口優先級設置
            self.create_test_case(
                name="cos_verify_interface_priority_settings",
                method="GET",
                url="/api/v1/cos/interfaces/eth1%2f5/default-priority",
                category="cos_interface_priority",
                module="cos",
                description="驗證接口優先級設置"
            )
        ]
    
    def get_cos_qos_mapping_tests(self) -> List[APITestCase]:
        """COS QoS Mapping API 測試案例"""
        return [
            # 獲取QoS映射 - eth1/5
            self.create_test_case(
                name="cos_get_qos_mapping_eth1_5",
                method="GET",
                url="/api/v1/cos/interfaces/eth1%2f5/qos-map",
                category="cos_qos_mapping",
                module="cos",
                description="獲取QoS映射 - eth1/5"
            ),
            
            # 設置QoS映射 - COS信任模式
            self.create_test_case(
                name="cos_set_qos_mapping_cos_trust",
                method="PUT",
                url="/api/v1/cos/interfaces/eth1%2f5/qos-map",
                category="cos_qos_mapping",
                module="cos",
                body=self.test_data.get('cos_qos_mapping_cos_trust', {
                    "cosToDscp": [
                        {"cos": 7, "cfi": 1, "phb": 0, "dropPrecedence": 0},
                        {"cos": 7, "cfi": 0, "phb": 1, "dropPrecedence": 3}
                    ],
                    "dscpToDscp": [
                        {"dscp": 0, "phb": 0, "dropPrecedence": 0},
                        {"dscp": 1, "phb": 0, "dropPrecedence": 1}
                    ],
                    "dscpToQueue": [
                        {"phb": 0, "queue": 2},
                        {"phb": 1, "queue": 0}
                    ],
                    "classificationMode": "cos"
                }),
                description="設置QoS映射 - COS信任模式"
            ),
            
            # 設置QoS映射 - DSCP信任模式
            self.create_test_case(
                name="cos_set_qos_mapping_dscp_trust",
                method="PUT",
                url="/api/v1/cos/interfaces/eth1%2f5/qos-map",
                category="cos_qos_mapping",
                module="cos",
                body=self.test_data.get('cos_qos_mapping_dscp_trust', {
                    "cosToDscp": [
                        {"cos": 0, "cfi": 0, "phb": 0, "dropPrecedence": 0},
                        {"cos": 1, "cfi": 0, "phb": 1, "dropPrecedence": 0}
                    ],
                    "dscpToDscp": [
                        {"dscp": 46, "phb": 7, "dropPrecedence": 0},
                        {"dscp": 34, "phb": 6, "dropPrecedence": 0}
                    ],
                    "dscpToQueue": [
                        {"phb": 7, "queue": 7},
                        {"phb": 6, "queue": 6}
                    ],
                    "classificationMode": "dscp"
                }),
                description="設置QoS映射 - DSCP信任模式"
            ),
            
            # 設置QoS映射 - IP-PREC信任模式
            self.create_test_case(
                name="cos_set_qos_mapping_ip_prec_trust",
                method="PUT",
                url="/api/v1/cos/interfaces/eth1%2f5/qos-map",
                category="cos_qos_mapping",
                module="cos",
                body=self.test_data.get('cos_qos_mapping_ip_prec_trust', {
                    "cosToDscp": [
                        {"cos": 5, "cfi": 0, "phb": 5, "dropPrecedence": 0},
                        {"cos": 6, "cfi": 0, "phb": 6, "dropPrecedence": 0}
                    ],
                    "dscpToDscp": [
                        {"dscp": 40, "phb": 5, "dropPrecedence": 0},
                        {"dscp": 48, "phb": 6, "dropPrecedence": 0}
                    ],
                    "dscpToQueue": [
                        {"phb": 5, "queue": 5},
                        {"phb": 6, "queue": 6}
                    ],
                    "classificationMode": "ip-prec"
                }),
                description="設置QoS映射 - IP-PREC信任模式"
            ),
            
            # 驗證QoS映射設置
            self.create_test_case(
                name="cos_verify_qos_mapping_settings",
                method="GET",
                url="/api/v1/cos/interfaces/eth1%2f5/qos-map",
                category="cos_qos_mapping",
                module="cos",
                description="驗證QoS映射設置"
            )
        ]
    
    def get_cos_qos_configuration_tests(self) -> List[APITestCase]:
        """COS QoS Configuration API 測試案例"""
        return [
            # 配置語音流量QoS - eth1/1
            self.create_test_case(
                name="cos_config_voice_traffic_qos",
                method="PUT",
                url="/api/v1/cos/interfaces/eth1%2f1/qos-map",
                category="cos_qos_configuration",
                module="cos",
                body=self.test_data.get('cos_voice_traffic_qos', {
                    "cosToDscp": [
                        {"cos": 5, "cfi": 0, "phb": 7, "dropPrecedence": 0}
                    ],
                    "dscpToDscp": [
                        {"dscp": 46, "phb": 7, "dropPrecedence": 0}
                    ],
                    "dscpToQueue": [
                        {"phb": 7, "queue": 7}
                    ],
                    "classificationMode": "dscp"
                }),
                description="配置語音流量QoS - eth1/1"
            ),
            
            # 配置視頻流量QoS - eth1/2
            self.create_test_case(
                name="cos_config_video_traffic_qos",
                method="PUT",
                url="/api/v1/cos/interfaces/eth1%2f2/qos-map",
                category="cos_qos_configuration",
                module="cos",
                body=self.test_data.get('cos_video_traffic_qos', {
                    "cosToDscp": [
                        {"cos": 4, "cfi": 0, "phb": 6, "dropPrecedence": 0}
                    ],
                    "dscpToDscp": [
                        {"dscp": 34, "phb": 6, "dropPrecedence": 0}
                    ],
                    "dscpToQueue": [
                        {"phb": 6, "queue": 6}
                    ],
                    "classificationMode": "dscp"
                }),
                description="配置視頻流量QoS - eth1/2"
            ),
            
            # 配置數據流量QoS - eth1/3
            self.create_test_case(
                name="cos_config_data_traffic_qos",
                method="PUT",
                url="/api/v1/cos/interfaces/eth1%2f3/qos-map",
                category="cos_qos_configuration",
                module="cos",
                body=self.test_data.get('cos_data_traffic_qos', {
                    "cosToDscp": [
                        {"cos": 0, "cfi": 0, "phb": 0, "dropPrecedence": 0},
                        {"cos": 1, "cfi": 0, "phb": 1, "dropPrecedence": 0}
                    ],
                    "dscpToDscp": [
                        {"dscp": 0, "phb": 0, "dropPrecedence": 0},
                        {"dscp": 8, "phb": 1, "dropPrecedence": 0}
                    ],
                    "dscpToQueue": [
                        {"phb": 0, "queue": 0},
                        {"phb": 1, "queue": 1}
                    ],
                    "classificationMode": "dscp"
                }),
                description="配置數據流量QoS - eth1/3"
            ),
            
            # 配置管理流量QoS - eth1/4
            self.create_test_case(
                name="cos_config_management_traffic_qos",
                method="PUT",
                url="/api/v1/cos/interfaces/eth1%2f4/qos-map",
                category="cos_qos_configuration",
                module="cos",
                body=self.test_data.get('cos_management_traffic_qos', {
                    "cosToDscp": [
                        {"cos": 6, "cfi": 0, "phb": 6, "dropPrecedence": 0}
                    ],
                    "dscpToDscp": [
                        {"dscp": 48, "phb": 6, "dropPrecedence": 0}
                    ],
                    "dscpToQueue": [
                        {"phb": 6, "queue": 6}
                    ],
                    "classificationMode": "dscp"
                }),
                description="配置管理流量QoS - eth1/4"
            ),
            
            # 配置Trunk接口QoS - trunk1
            self.create_test_case(
                name="cos_config_trunk_qos",
                method="PUT",
                url="/api/v1/cos/interfaces/trunk1/qos-map",
                category="cos_qos_configuration",
                module="cos",
                body=self.test_data.get('cos_trunk_qos', {
                    "cosToDscp": [
                        {"cos": 0, "cfi": 0, "phb": 0, "dropPrecedence": 0},
                        {"cos": 1, "cfi": 0, "phb": 1, "dropPrecedence": 0},
                        {"cos": 2, "cfi": 0, "phb": 2, "dropPrecedence": 0},
                        {"cos": 3, "cfi": 0, "phb": 3, "dropPrecedence": 0},
                        {"cos": 4, "cfi": 0, "phb": 4, "dropPrecedence": 0},
                        {"cos": 5, "cfi": 0, "phb": 5, "dropPrecedence": 0},
                        {"cos": 6, "cfi": 0, "phb": 6, "dropPrecedence": 0},
                        {"cos": 7, "cfi": 0, "phb": 7, "dropPrecedence": 0}
                    ],
                    "classificationMode": "cos"
                }),
                description="配置Trunk接口QoS - trunk1"
            ),
            
            # 驗證所有QoS配置
            self.create_test_case(
                name="cos_verify_all_qos_configurations",
                method="GET",
                url="/api/v1/cos/interfaces/eth1%2f1/qos-map",
                category="cos_qos_configuration",
                module="cos",
                description="驗證所有QoS配置"
            )
        ]
    
    def get_cos_advanced_operations_tests(self) -> List[APITestCase]:
        """COS Advanced Operations API 測試案例"""
        return [
            # 批量配置接口優先級
            self.create_test_case(
                name="cos_batch_config_interface_priorities",
                method="PUT",
                url="/api/v1/cos/interfaces/eth1%2f10/default-priority",
                category="cos_advanced_operations",
                module="cos",
                body=self.test_data.get('cos_batch_priority_1', {
                    "priority": 2
                }),
                description="批量配置接口優先級 - eth1/10"
            ),
            
            # 批量配置接口優先級 - eth1/11
            self.create_test_case(
                name="cos_batch_config_priority_eth1_11",
                method="PUT",
                url="/api/v1/cos/interfaces/eth1%2f11/default-priority",
                category="cos_advanced_operations",
                module="cos",
                body=self.test_data.get('cos_batch_priority_2', {
                    "priority": 3
                }),
                description="批量配置接口優先級 - eth1/11"
            ),
            
            # 批量配置接口優先級 - eth1/12
            self.create_test_case(
                name="cos_batch_config_priority_eth1_12",
                method="PUT",
                url="/api/v1/cos/interfaces/eth1%2f12/default-priority",
                category="cos_advanced_operations",
                module="cos",
                body=self.test_data.get('cos_batch_priority_3', {
                    "priority": 4
                }),
                description="批量配置接口優先級 - eth1/12"
            ),
            
            # 動態調整隊列權重
            self.create_test_case(
                name="cos_dynamic_adjust_queue_weights",
                method="PUT",
                url="/api/v1/cos/queues",
                category="cos_advanced_operations",
                module="cos",
                body=self.test_data.get('cos_dynamic_queue_weights', {
                    "queueMode": "wrr",
                    "queues": [
                        {"property": 0, "weight": 1},
                        {"property": 0, "weight": 4},
                        {"property": 0, "weight": 8},
                        {"property": 0, "weight": 16},
                        {"property": 0, "weight": 32},
                        {"property": 0, "weight": 64},
                        {"property": 0, "weight": 128},
                        {"property": 0, "weight": 255}
                    ]
                }),
                description="動態調整隊列權重 - 指數級增長"
            ),
            
            # 配置複雜QoS映射
            self.create_test_case(
                name="cos_config_complex_qos_mapping",
                method="PUT",
                url="/api/v1/cos/interfaces/eth1%2f20/qos-map",
                category="cos_advanced_operations",
                module="cos",
                body=self.test_data.get('cos_complex_qos_mapping', {
                    "cosToDscp": [
                        {"cos": 0, "cfi": 0, "phb": 0, "dropPrecedence": 0},
                        {"cos": 1, "cfi": 0, "phb": 1, "dropPrecedence": 1},
                        {"cos": 2, "cfi": 0, "phb": 2, "dropPrecedence": 0},
                        {"cos": 3, "cfi": 0, "phb": 3, "dropPrecedence": 1},
                        {"cos": 4, "cfi": 0, "phb": 4, "dropPrecedence": 0},
                        {"cos": 5, "cfi": 0, "phb": 5, "dropPrecedence": 0},
                        {"cos": 6, "cfi": 0, "phb": 6, "dropPrecedence": 0},
                        {"cos": 7, "cfi": 0, "phb": 7, "dropPrecedence": 0}
                    ],
                    "dscpToDscp": [
                        {"dscp": 0, "phb": 0, "dropPrecedence": 0},
                        {"dscp": 8, "phb": 1, "dropPrecedence": 1},
                        {"dscp": 16, "phb": 2, "dropPrecedence": 0},
                        {"dscp": 24, "phb": 3, "dropPrecedence": 1},
                        {"dscp": 32, "phb": 4, "dropPrecedence": 0},
                        {"dscp": 40, "phb": 5, "dropPrecedence": 0},
                        {"dscp": 48, "phb": 6, "dropPrecedence": 0},
                        {"dscp": 56, "phb": 7, "dropPrecedence": 0}
                    ],
                    "dscpToQueue": [
                        {"phb": 0, "queue": 0},
                        {"phb": 1, "queue": 1},
                        {"phb": 2, "queue": 2},
                        {"phb": 3, "queue": 3},
                        {"phb": 4, "queue": 4},
                        {"phb": 5, "queue": 5},
                        {"phb": 6, "queue": 6},
                        {"phb": 7, "queue": 7}
                    ],
                    "classificationMode": "dscp"
                }),
                description="配置複雜QoS映射 - 完整映射表"
            ),
            
            # 測試無效優先級值
            self.create_test_case(
                name="cos_test_invalid_priority_value",
                method="PUT",
                url="/api/v1/cos/interfaces/eth1%2f5/default-priority",
                category="cos_advanced_operations",
                module="cos",
                body=self.test_data.get('cos_invalid_priority', {
                    "priority": 8  # 超出範圍 0-7
                }),
                expected_status=400,
                description="測試無效優先級值"
            ),
            
            # 測試無效隊列權重
            self.create_test_case(
                name="cos_test_invalid_queue_weight",
                method="PUT",
                url="/api/v1/cos/queues",
                category="cos_advanced_operations",
                module="cos",
                body=self.test_data.get('cos_invalid_queue_weight', {
                    "queueMode": "wrr",
                    "queues": [
                        {"property": 0, "weight": 256}  # 超出範圍 1-255
                    ]
                }),
                expected_status=400,
                description="測試無效隊列權重"
            ),
            
            # 測試無效接口ID
            self.create_test_case(
                name="cos_test_invalid_interface_id",
                method="GET",
                url="/api/v1/cos/interfaces/invalid%2finterface/default-priority",
                category="cos_advanced_operations",
                module="cos",
                expected_status=500,
                description="測試無效接口ID"
            ),
            
            # 最終狀態檢查 - 隊列配置
            self.create_test_case(
                name="cos_final_state_check_queues",
                method="GET",
                url="/api/v1/cos/queues",
                category="cos_advanced_operations",
                module="cos",
                description="最終狀態檢查 - 隊列配置"
            ),
            
            # 最終狀態檢查 - 接口優先級
            self.create_test_case(
                name="cos_final_state_check_interface_priority",
                method="GET",
                url="/api/v1/cos/interfaces/eth1%2f5/default-priority",
                category="cos_advanced_operations",
                module="cos",
                description="最終狀態檢查 - 接口優先級"
            ),
            
            # 最終狀態檢查 - QoS映射
            self.create_test_case(
                name="cos_final_state_check_qos_mapping",
                method="GET",
                url="/api/v1/cos/interfaces/eth1%2f5/qos-map",
                category="cos_advanced_operations",
                module="cos",
                description="最終狀態檢查 - QoS映射"
            )
        ]