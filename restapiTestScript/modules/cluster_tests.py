#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cluster 模組測試案例
包含集群配置管理、成員管理、候選者管理等相關API測試
支援集群啟用/禁用、指揮官配置、IP池管理、成員增刪改查、候選者查詢等操作
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class CLUSTERTests(BaseTests):
    """Cluster 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取Cluster模組支援的類別"""
        return [
            "cluster_configuration_management",
            "cluster_member_management",
            "cluster_member_operations",
            "cluster_candidate_management",
            "cluster_advanced_operations",
            "cluster_error_handling"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有Cluster測試案例"""
        all_tests = []
        all_tests.extend(self.get_cluster_configuration_management_tests())
        all_tests.extend(self.get_cluster_member_management_tests())
        all_tests.extend(self.get_cluster_member_operations_tests())
        all_tests.extend(self.get_cluster_candidate_management_tests())
        all_tests.extend(self.get_cluster_advanced_operations_tests())
        all_tests.extend(self.get_cluster_error_handling_tests())
        return all_tests
    
    def get_cluster_configuration_management_tests(self) -> List[APITestCase]:
        """Cluster Configuration Management API 測試案例"""
        return [
            # 獲取集群配置
            self.create_test_case(
                name="cluster_get_configuration",
                method="GET",
                url="/api/v1/cluster",
                category="cluster_configuration_management",
                module="cluster",
                description="獲取集群配置"
            ),
            
            # 啟用集群功能 - 基本配置
            self.create_test_case(
                name="cluster_enable_basic",
                method="PUT",
                url="/api/v1/cluster",
                category="cluster_configuration_management",
                module="cluster",
                body=self.test_data.get('cluster_enable_basic', {
                    "clusterEnable": True,
                    "commanderEnable": False,
                    "ipPool": "10.254.254.1"
                }),
                description="啟用集群功能 - 基本配置"
            ),
            
            # 啟用指揮官模式
            self.create_test_case(
                name="cluster_enable_commander",
                method="PUT",
                url="/api/v1/cluster",
                category="cluster_configuration_management",
                module="cluster",
                body=self.test_data.get('cluster_enable_commander', {
                    "clusterEnable": True,
                    "commanderEnable": True,
                    "ipPool": "10.254.254.1"
                }),
                description="啟用指揮官模式"
            ),
            
            # 配置不同IP池 - 網段1
            self.create_test_case(
                name="cluster_config_ip_pool_subnet1",
                method="PUT",
                url="/api/v1/cluster",
                category="cluster_configuration_management",
                module="cluster",
                body=self.test_data.get('cluster_ip_pool_subnet1', {
                    "clusterEnable": True,
                    "commanderEnable": True,
                    "ipPool": "10.100.100.1"
                }),
                description="配置不同IP池 - 網段1"
            ),
            
            # 配置不同IP池 - 網段2
            self.create_test_case(
                name="cluster_config_ip_pool_subnet2",
                method="PUT",
                url="/api/v1/cluster",
                category="cluster_configuration_management",
                module="cluster",
                body=self.test_data.get('cluster_ip_pool_subnet2', {
                    "clusterEnable": True,
                    "commanderEnable": True,
                    "ipPool": "10.200.200.1"
                }),
                description="配置不同IP池 - 網段2"
            ),
            
            # 禁用指揮官模式但保持集群啟用
            self.create_test_case(
                name="cluster_disable_commander_keep_cluster",
                method="PUT",
                url="/api/v1/cluster",
                category="cluster_configuration_management",
                module="cluster",
                body=self.test_data.get('cluster_disable_commander', {
                    "clusterEnable": True,
                    "commanderEnable": False,
                    "ipPool": "10.254.254.2"
                }),
                description="禁用指揮官模式但保持集群啟用"
            ),
            
            # 驗證集群配置更新
            self.create_test_case(
                name="cluster_verify_configuration_update",
                method="GET",
                url="/api/v1/cluster",
                category="cluster_configuration_management",
                module="cluster",
                description="驗證集群配置更新"
            ),
            
            # 完全禁用集群功能
            self.create_test_case(
                name="cluster_disable_completely",
                method="PUT",
                url="/api/v1/cluster",
                category="cluster_configuration_management",
                module="cluster",
                body=self.test_data.get('cluster_disable_completely', {
                    "clusterEnable": False
                }),
                description="完全禁用集群功能"
            ),
            
            # 驗證集群完全禁用
            self.create_test_case(
                name="cluster_verify_completely_disabled",
                method="GET",
                url="/api/v1/cluster",
                category="cluster_configuration_management",
                module="cluster",
                description="驗證集群完全禁用"
            ),
            
            # 重新啟用集群 - 準備成員測試
            self.create_test_case(
                name="cluster_re_enable_for_member_tests",
                method="PUT",
                url="/api/v1/cluster",
                category="cluster_configuration_management",
                module="cluster",
                body=self.test_data.get('cluster_re_enable', {
                    "clusterEnable": True,
                    "commanderEnable": True,
                    "ipPool": "10.254.254.1"
                }),
                description="重新啟用集群 - 準備成員測試"
            )
        ]
    
    def get_cluster_member_management_tests(self) -> List[APITestCase]:
        """Cluster Member Management API 測試案例"""
        return [
            # 獲取所有集群成員
            self.create_test_case(
                name="cluster_get_all_members",
                method="GET",
                url="/api/v1/cluster-members",
                category="cluster_member_management",
                module="cluster",
                description="獲取所有集群成員"
            ),
            
            # 創建集群成員 - 成員1
            self.create_test_case(
                name="cluster_create_member_1",
                method="POST",
                url="/api/v1/cluster-members",
                category="cluster_member_management",
                module="cluster",
                body=self.test_data.get('cluster_member_1', {
                    "macAddress": "00-e0-0c-00-00-01",
                    "memberId": 1
                }),
                description="創建集群成員 - 成員1"
            ),
            
            # 創建集群成員 - 成員2
            self.create_test_case(
                name="cluster_create_member_2",
                method="POST",
                url="/api/v1/cluster-members",
                category="cluster_member_management",
                module="cluster",
                body=self.test_data.get('cluster_member_2', {
                    "macAddress": "00-e0-0c-00-00-02",
                    "memberId": 2
                }),
                description="創建集群成員 - 成員2"
            ),
            
            # 創建集群成員 - 成員3
            self.create_test_case(
                name="cluster_create_member_3",
                method="POST",
                url="/api/v1/cluster-members",
                category="cluster_member_management",
                module="cluster",
                body=self.test_data.get('cluster_member_3', {
                    "macAddress": "00-e0-0c-00-00-03",
                    "memberId": 3
                }),
                description="創建集群成員 - 成員3"
            ),
            
            # 創建集群成員 - 最大成員ID
            self.create_test_case(
                name="cluster_create_member_max_id",
                method="POST",
                url="/api/v1/cluster-members",
                category="cluster_member_management",
                module="cluster",
                body=self.test_data.get('cluster_member_max_id', {
                    "macAddress": "00-e0-0c-00-00-24",
                    "memberId": 36
                }),
                description="創建集群成員 - 最大成員ID (36)"
            ),
            
            # 創建集群成員 - 不同MAC格式
            self.create_test_case(
                name="cluster_create_member_different_mac_format",
                method="POST",
                url="/api/v1/cluster-members",
                category="cluster_member_management",
                module="cluster",
                body=self.test_data.get('cluster_member_different_mac', {
                    "macAddress": "aa-bb-cc-dd-ee-ff",
                    "memberId": 4
                }),
                description="創建集群成員 - 不同MAC格式"
            ),
            
            # 驗證成員創建結果
            self.create_test_case(
                name="cluster_verify_members_created",
                method="GET",
                url="/api/v1/cluster-members",
                category="cluster_member_management",
                module="cluster",
                description="驗證成員創建結果"
            ),
            
            # 驗證集群狀態更新
            self.create_test_case(
                name="cluster_verify_status_after_member_creation",
                method="GET",
                url="/api/v1/cluster",
                category="cluster_member_management",
                module="cluster",
                description="驗證集群狀態更新 - 成員數量"
            )
        ]
    
    def get_cluster_member_operations_tests(self) -> List[APITestCase]:
        """Cluster Member Operations API 測試案例"""
        return [
            # 獲取特定集群成員 - 成員1
            self.create_test_case(
                name="cluster_get_specific_member_1",
                method="GET",
                url="/api/v1/cluster-members/{memberId}",
                category="cluster_member_operations",
                module="cluster",
                params={"memberId": "1"},
                description="獲取特定集群成員 - 成員1"
            ),
            
            # 獲取特定集群成員 - 成員2
            self.create_test_case(
                name="cluster_get_specific_member_2",
                method="GET",
                url="/api/v1/cluster-members/{memberId}",
                category="cluster_member_operations",
                module="cluster",
                params={"memberId": "2"},
                description="獲取特定集群成員 - 成員2"
            ),
            
            # 獲取參數化集群成員
            self.create_test_case(
                name="cluster_get_parameterized_member",
                method="GET",
                url="/api/v1/cluster-members/{memberId}",
                category="cluster_member_operations",
                module="cluster",
                params={"memberId": str(self.params.get('cluster_member_id', 1))},
                description=f"獲取參數化集群成員 - 成員{self.params.get('cluster_member_id', 1)}"
            ),
            
            # 獲取最大ID成員
            self.create_test_case(
                name="cluster_get_max_id_member",
                method="GET",
                url="/api/v1/cluster-members/{memberId}",
                category="cluster_member_operations",
                module="cluster",
                params={"memberId": "36"},
                description="獲取最大ID成員 - 成員36"
            ),
            
            # 刪除集群成員 - 成員3
            self.create_test_case(
                name="cluster_delete_member_3",
                method="DELETE",
                url="/api/v1/cluster-members/{memberId}",
                category="cluster_member_operations",
                module="cluster",
                params={"memberId": "3"},
                description="刪除集群成員 - 成員3"
            ),
            
            # 刪除集群成員 - 成員4
            self.create_test_case(
                name="cluster_delete_member_4",
                method="DELETE",
                url="/api/v1/cluster-members/{memberId}",
                category="cluster_member_operations",
                module="cluster",
                params={"memberId": "4"},
                description="刪除集群成員 - 成員4"
            ),
            
            # 驗證成員刪除後狀態
            self.create_test_case(
                name="cluster_verify_members_after_deletion",
                method="GET",
                url="/api/v1/cluster-members",
                category="cluster_member_operations",
                module="cluster",
                description="驗證成員刪除後狀態"
            ),
            
            # 驗證集群狀態更新 - 成員數量減少
            self.create_test_case(
                name="cluster_verify_status_after_member_deletion",
                method="GET",
                url="/api/v1/cluster",
                category="cluster_member_operations",
                module="cluster",
                description="驗證集群狀態更新 - 成員數量減少"
            )
        ]
    
    def get_cluster_candidate_management_tests(self) -> List[APITestCase]:
        """Cluster Candidate Management API 測試案例"""
        return [
            # 獲取所有集群候選者
            self.create_test_case(
                name="cluster_get_all_candidates",
                method="GET",
                url="/api/v1/cluster/candidates",
                category="cluster_candidate_management",
                module="cluster",
                description="獲取所有集群候選者"
            ),
            
            # 添加更多成員以增加候選者發現機會
            self.create_test_case(
                name="cluster_add_member_for_candidates",
                method="POST",
                url="/api/v1/cluster-members",
                category="cluster_candidate_management",
                module="cluster",
                body=self.test_data.get('cluster_member_for_candidates_1', {
                    "macAddress": "00-e0-0c-00-00-10",
                    "memberId": 10
                }),
                description="添加成員以增加候選者發現機會 - 成員10"
            ),
            
            # 添加更多成員 - 成員11
            self.create_test_case(
                name="cluster_add_member_11_for_candidates",
                method="POST",
                url="/api/v1/cluster-members",
                category="cluster_candidate_management",
                module="cluster",
                body=self.test_data.get('cluster_member_for_candidates_2', {
                    "macAddress": "00-e0-0c-00-00-11",
                    "memberId": 11
                }),
                description="添加成員以增加候選者發現機會 - 成員11"
            ),
            
            # 再次獲取候選者 - 檢查是否有新候選者
            self.create_test_case(
                name="cluster_get_candidates_after_member_addition",
                method="GET",
                url="/api/v1/cluster/candidates",
                category="cluster_candidate_management",
                module="cluster",
                description="添加成員後獲取候選者"
            ),
            
            # 驗證候選者數量更新
            self.create_test_case(
                name="cluster_verify_candidates_count",
                method="GET",
                url="/api/v1/cluster",
                category="cluster_candidate_management",
                module="cluster",
                description="驗證候選者數量更新"
            )
        ]
    
    def get_cluster_advanced_operations_tests(self) -> List[APITestCase]:
        """Cluster Advanced Operations API 測試案例"""
        return [
            # 批量創建集群成員
            self.create_test_case(
                name="cluster_batch_create_members",
                method="POST",
                url="/api/v1/cluster-members",
                category="cluster_advanced_operations",
                module="cluster",
                body=self.test_data.get('cluster_batch_member_1', {
                    "macAddress": "00-e0-0c-00-01-01",
                    "memberId": 20
                }),
                description="批量創建集群成員 - 成員20"
            ),
            
            # 批量創建集群成員 - 成員21
            self.create_test_case(
                name="cluster_batch_create_member_21",
                method="POST",
                url="/api/v1/cluster-members",
                category="cluster_advanced_operations",
                module="cluster",
                body=self.test_data.get('cluster_batch_member_2', {
                    "macAddress": "00-e0-0c-00-01-02",
                    "memberId": 21
                }),
                description="批量創建集群成員 - 成員21"
            ),
            
            # 批量創建集群成員 - 成員22
            self.create_test_case(
                name="cluster_batch_create_member_22",
                method="POST",
                url="/api/v1/cluster-members",
                category="cluster_advanced_operations",
                module="cluster",
                body=self.test_data.get('cluster_batch_member_3', {
                    "macAddress": "00-e0-0c-00-01-03",
                    "memberId": 22
                }),
                description="批量創建集群成員 - 成員22"
            ),
            
            # 動態調整IP池
            self.create_test_case(
                name="cluster_dynamic_adjust_ip_pool",
                method="PUT",
                url="/api/v1/cluster",
                category="cluster_advanced_operations",
                module="cluster",
                body=self.test_data.get('cluster_dynamic_ip_pool', {
                    "clusterEnable": True,
                    "commanderEnable": False,
                    "ipPool": "10.254.254.100"
                }),
                description="動態調整IP池"
            ),
            
            # 切換指揮官模式
            self.create_test_case(
                name="cluster_toggle_commander_mode",
                method="PUT",
                url="/api/v1/cluster",
                category="cluster_advanced_operations",
                module="cluster",
                body=self.test_data.get('cluster_toggle_commander', {
                    "clusterEnable": True,
                    "commanderEnable": True,
                    "ipPool": "10.254.254.1"
                }),
                description="切換指揮官模式"
            ),
            
            # 驗證批量操作結果
            self.create_test_case(
                name="cluster_verify_batch_operations",
                method="GET",
                url="/api/v1/cluster-members",
                category="cluster_advanced_operations",
                module="cluster",
                description="驗證批量操作結果"
            ),
            
            # 驗證最終集群狀態
            self.create_test_case(
                name="cluster_verify_final_status",
                method="GET",
                url="/api/v1/cluster",
                category="cluster_advanced_operations",
                module="cluster",
                description="驗證最終集群狀態"
            ),
            
            # 批量刪除集群成員
            self.create_test_case(
                name="cluster_batch_delete_members",
                method="DELETE",
                url="/api/v1/cluster-members/{memberId}",
                category="cluster_advanced_operations",
                module="cluster",
                params={"memberId": "20"},
                description="批量刪除集群成員 - 成員20"
            ),
            
            # 批量刪除集群成員 - 成員21
            self.create_test_case(
                name="cluster_batch_delete_member_21",
                method="DELETE",
                url="/api/v1/cluster-members/{memberId}",
                category="cluster_advanced_operations",
                module="cluster",
                params={"memberId": "21"},
                description="批量刪除集群成員 - 成員21"
            ),
            
            # 最終狀態檢查
            self.create_test_case(
                name="cluster_final_state_check",
                method="GET",
                url="/api/v1/cluster",
                category="cluster_advanced_operations",
                module="cluster",
                description="最終狀態檢查"
            )
        ]
    
    def get_cluster_error_handling_tests(self) -> List[APITestCase]:
        """Cluster Error Handling API 測試案例"""
        return [
            # 測試無效成員ID - 超出範圍
            self.create_test_case(
                name="cluster_test_invalid_member_id_range",
                method="POST",
                url="/api/v1/cluster-members",
                category="cluster_error_handling",
                module="cluster",
                body=self.test_data.get('cluster_invalid_member_id', {
                    "macAddress": "00-e0-0c-00-00-ff",
                    "memberId": 37  # 超出範圍 1-36
                }),
                expected_status=400,
                description="測試無效成員ID - 超出範圍"
            ),
            
            # 測試重複成員ID
            self.create_test_case(
                name="cluster_test_duplicate_member_id",
                method="POST",
                url="/api/v1/cluster-members",
                category="cluster_error_handling",
                module="cluster",
                body=self.test_data.get('cluster_duplicate_member_id', {
                    "macAddress": "00-e0-0c-00-00-aa",
                    "memberId": 1  # 重複的成員ID
                }),
                expected_status=500,
                description="測試重複成員ID"
            ),
            
            # 測試無效MAC地址格式
            self.create_test_case(
                name="cluster_test_invalid_mac_format",
                method="POST",
                url="/api/v1/cluster-members",
                category="cluster_error_handling",
                module="cluster",
                body=self.test_data.get('cluster_invalid_mac_format', {
                    "macAddress": "invalid-mac-address",
                    "memberId": 30
                }),
                expected_status=400,
                description="測試無效MAC地址格式"
            ),
            
            # 測試獲取不存在的成員
            self.create_test_case(
                name="cluster_test_get_nonexistent_member",
                method="GET",
                url="/api/v1/cluster-members/{memberId}",
                category="cluster_error_handling",
                module="cluster",
                params={"memberId": "99"},
                expected_status=500,
                description="測試獲取不存在的成員"
            ),
            
            # 測試刪除不存在的成員
            self.create_test_case(
                name="cluster_test_delete_nonexistent_member",
                method="DELETE",
                url="/api/v1/cluster-members/{memberId}",
                category="cluster_error_handling",
                module="cluster",
                params={"memberId": "99"},
                expected_status=500,
                description="測試刪除不存在的成員"
            ),
            
            # 測試無效IP池格式
            self.create_test_case(
                name="cluster_test_invalid_ip_pool_format",
                method="PUT",
                url="/api/v1/cluster",
                category="cluster_error_handling",
                module="cluster",
                body=self.test_data.get('cluster_invalid_ip_pool', {
                    "clusterEnable": True,
                    "commanderEnable": True,
                    "ipPool": "invalid.ip.format"
                }),
                expected_status=400,
                description="測試無效IP池格式"
            ),
            
            # 測試在集群禁用時設置指揮官
            self.create_test_case(
                name="cluster_test_set_commander_when_cluster_disabled",
                method="PUT",
                url="/api/v1/cluster",
                category="cluster_error_handling",
                module="cluster",
                body=self.test_data.get('cluster_commander_when_disabled', {
                    "clusterEnable": False,
                    "commanderEnable": True
                }),
                expected_status=500,
                description="測試在集群禁用時設置指揮官"
            ),
            
            # 測試在集群禁用時設置IP池
            self.create_test_case(
                name="cluster_test_set_ip_pool_when_cluster_disabled",
                method="PUT",
                url="/api/v1/cluster",
                category="cluster_error_handling",
                module="cluster",
                body=self.test_data.get('cluster_ip_pool_when_disabled', {
                    "clusterEnable": False,
                    "ipPool": "10.254.254.1"
                }),
                expected_status=500,
                description="測試在集群禁用時設置IP池"
            ),
            
            # 測試無效JSON格式
            self.create_test_case(
                name="cluster_test_invalid_json_format",
                method="PUT",
                url="/api/v1/cluster",
                category="cluster_error_handling",
                module="cluster",
                body="invalid json format",
                expected_status=400,
                description="測試無效JSON格式"
            ),
            
            # 恢復正常集群配置
            self.create_test_case(
                name="cluster_restore_normal_config",
                method="PUT",
                url="/api/v1/cluster",
                category="cluster_error_handling",
                module="cluster",
                body=self.test_data.get('cluster_restore_normal', {
                    "clusterEnable": True,
                    "commanderEnable": True,
                    "ipPool": "10.254.254.1"
                }),
                description="恢復正常集群配置"
            )
        ]