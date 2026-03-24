#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Static Route 模組測試案例
包含靜態路由管理、最大路徑配置等相關API測試
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class STATIC_ROUTETests(BaseTests):
    """Static Route 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取Static Route模組支援的類別"""
        return [
            "static_routes",
            "maximum_paths"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有Static Route測試案例"""
        all_tests = []
        all_tests.extend(self.get_static_routes_tests())
        all_tests.extend(self.get_maximum_paths_tests())
        return all_tests
    
    def get_static_routes_tests(self) -> List[APITestCase]:
        """Static Routes API 測試案例"""
        return [
            # 獲取所有靜態路由
            self.create_test_case(
                name="static_route_get_all_routes",
                method="GET",
                url="/api/v1/ip-routes",
                category="static_routes",
                module="static_route",
                description="獲取所有靜態路由"
            ),
            
            # 創建靜態路由 - 基本路由
            self.create_test_case(
                name="static_route_create_basic_route",
                method="POST",
                url="/api/v1/ip-routes",
                category="static_routes",
                module="static_route",
                body=self.test_data.get('static_route_basic', {
                    "destIp": "192.168.2.0",
                    "netMask": "255.255.255.0",
                    "nextHop": "192.168.1.2",
                    "distance": 2
                }),
                description="創建基本靜態路由"
            ),
            
            # 創建靜態路由 - 默認路由
            self.create_test_case(
                name="static_route_create_default_route",
                method="POST",
                url="/api/v1/ip-routes",
                category="static_routes",
                module="static_route",
                body=self.test_data.get('static_route_default', {
                    "destIp": "0.0.0.0",
                    "netMask": "0.0.0.0",
                    "nextHop": "192.168.1.1",
                    "distance": 1
                }),
                description="創建默認靜態路由"
            ),
            
            # 創建靜態路由 - 黑洞路由
            self.create_test_case(
                name="static_route_create_blackhole_route",
                method="POST",
                url="/api/v1/ip-routes",
                category="static_routes",
                module="static_route",
                body=self.test_data.get('static_route_blackhole', {
                    "destIp": "10.10.10.0",
                    "netMask": "255.255.255.0",
                    "nextHop": "0.0.0.0",
                    "distance": 1
                }),
                description="創建黑洞靜態路由"
            ),
            
            # 創建靜態路由 - 高距離值
            self.create_test_case(
                name="static_route_create_high_distance_route",
                method="POST",
                url="/api/v1/ip-routes",
                category="static_routes",
                module="static_route",
                body=self.test_data.get('static_route_high_distance', {
                    "destIp": "172.16.0.0",
                    "netMask": "255.240.0.0",
                    "nextHop": "192.168.1.3",
                    "distance": 200
                }),
                description="創建高距離值靜態路由"
            ),
            
            # 創建靜態路由 - 主機路由
            self.create_test_case(
                name="static_route_create_host_route",
                method="POST",
                url="/api/v1/ip-routes",
                category="static_routes",
                module="static_route",
                body=self.test_data.get('static_route_host', {
                    "destIp": "8.8.8.8",
                    "netMask": "255.255.255.255",
                    "nextHop": "192.168.1.1",
                    "distance": 1
                }),
                description="創建主機靜態路由"
            ),
            
            # 獲取特定靜態路由
            self.create_test_case(
                name="static_route_get_specific_route",
                method="GET",
                url="/api/v1/ip-routes/ip-addresses/{destIp}/net-mask/{netMask}/next-hop/{nextHop}",
                category="static_routes",
                module="static_route",
                params={
                    "destIp": "192.168.2.0",
                    "netMask": "255.255.255.0",
                    "nextHop": "192.168.1.2"
                },
                description="獲取特定靜態路由"
            ),
            
            # 獲取默認路由
            self.create_test_case(
                name="static_route_get_default_route",
                method="GET",
                url="/api/v1/ip-routes/ip-addresses/{destIp}/net-mask/{netMask}/next-hop/{nextHop}",
                category="static_routes",
                module="static_route",
                params={
                    "destIp": "0.0.0.0",
                    "netMask": "0.0.0.0",
                    "nextHop": "192.168.1.1"
                },
                description="獲取默認靜態路由"
            ),
            
            # 獲取黑洞路由
            self.create_test_case(
                name="static_route_get_blackhole_route",
                method="GET",
                url="/api/v1/ip-routes/ip-addresses/{destIp}/net-mask/{netMask}/next-hop/{nextHop}",
                category="static_routes",
                module="static_route",
                params={
                    "destIp": "10.10.10.0",
                    "netMask": "255.255.255.0",
                    "nextHop": "0.0.0.0"
                },
                description="獲取黑洞靜態路由"
            ),
            
            # 刪除靜態路由 - 基本路由
            self.create_test_case(
                name="static_route_delete_basic_route",
                method="DELETE",
                url="/api/v1/ip-routes/ip-addresses/{destIp}/net-mask/{netMask}/next-hop/{nextHop}",
                category="static_routes",
                module="static_route",
                params={
                    "destIp": "172.16.0.0",
                    "netMask": "255.240.0.0",
                    "nextHop": "192.168.1.3"
                },
                description="刪除基本靜態路由"
            ),
            
            # 刪除黑洞路由
            self.create_test_case(
                name="static_route_delete_blackhole_route",
                method="DELETE",
                url="/api/v1/ip-routes/ip-addresses/{destIp}/net-mask/{netMask}/next-hop/{nextHop}",
                category="static_routes",
                module="static_route",
                params={
                    "destIp": "10.10.10.0",
                    "netMask": "255.255.255.0",
                    "nextHop": "0.0.0.0"
                },
                description="刪除黑洞靜態路由"
            ),
            
            # 測試無效IP地址
            self.create_test_case(
                name="static_route_test_invalid_ip",
                method="POST",
                url="/api/v1/ip-routes",
                category="static_routes",
                module="static_route",
                body=self.test_data.get('static_route_invalid_ip', {
                    "destIp": "999.999.999.999",
                    "netMask": "255.255.255.0",
                    "nextHop": "192.168.1.1"
                }),
                expected_status=400,
                description="測試無效目標IP地址"
            ),
            
            # 測試無效網路遮罩
            self.create_test_case(
                name="static_route_test_invalid_netmask",
                method="POST",
                url="/api/v1/ip-routes",
                category="static_routes",
                module="static_route",
                body=self.test_data.get('static_route_invalid_netmask', {
                    "destIp": "192.168.3.0",
                    "netMask": "255.255.255.256",
                    "nextHop": "192.168.1.1"
                }),
                expected_status=400,
                description="測試無效網路遮罩"
            ),
            
            # 測試無效距離值
            self.create_test_case(
                name="static_route_test_invalid_distance",
                method="POST",
                url="/api/v1/ip-routes",
                category="static_routes",
                module="static_route",
                body=self.test_data.get('static_route_invalid_distance', {
                    "destIp": "192.168.4.0",
                    "netMask": "255.255.255.0",
                    "nextHop": "192.168.1.1",
                    "distance": 300  # 超出範圍 1-255
                }),
                expected_status=400,
                description="測試無效距離值"
            ),
            
            # 測試獲取不存在的路由
            self.create_test_case(
                name="static_route_get_nonexistent_route",
                method="GET",
                url="/api/v1/ip-routes/ip-addresses/{destIp}/net-mask/{netMask}/next-hop/{nextHop}",
                category="static_routes",
                module="static_route",
                params={
                    "destIp": "1.1.1.0",
                    "netMask": "255.255.255.0",
                    "nextHop": "192.168.1.99"
                },
                expected_status=404,
                description="測試獲取不存在的靜態路由"
            ),
            
            # 驗證路由表更新
            self.create_test_case(
                name="static_route_verify_route_table_update",
                method="GET",
                url="/api/v1/ip-routes",
                category="static_routes",
                module="static_route",
                description="驗證路由表更新效果"
            )
        ]
    
    def get_maximum_paths_tests(self) -> List[APITestCase]:
        """Maximum Paths API 測試案例"""
        return [
            # 獲取最大路徑數
            self.create_test_case(
                name="static_route_get_maximum_paths",
                method="GET",
                url="/api/v1/maximum-path",
                category="maximum_paths",
                module="static_route",
                description="獲取最大路徑數配置"
            ),
            
            # 設置最大路徑數 - 最小值
            self.create_test_case(
                name="static_route_set_min_maximum_paths",
                method="PUT",
                url="/api/v1/maximum-path",
                category="maximum_paths",
                module="static_route",
                body=self.test_data.get('maximum_path_min', {
                    "number": 1
                }),
                description="設置最大路徑數為最小值 (1)"
            ),
            
            # 設置最大路徑數 - 中等值
            self.create_test_case(
                name="static_route_set_medium_maximum_paths",
                method="PUT",
                url="/api/v1/maximum-path",
                category="maximum_paths",
                module="static_route",
                body=self.test_data.get('maximum_path_medium', {
                    "number": 4
                }),
                description="設置最大路徑數為中等值 (4)"
            ),
            
            # 設置最大路徑數 - 最大值
            self.create_test_case(
                name="static_route_set_max_maximum_paths",
                method="PUT",
                url="/api/v1/maximum-path",
                category="maximum_paths",
                module="static_route",
                body=self.test_data.get('maximum_path_max', {
                    "number": 8
                }),
                description="設置最大路徑數為最大值 (8)"
            ),
            
            # 測試無效最大路徑數 - 超出上限
            self.create_test_case(
                name="static_route_test_invalid_max_paths_high",
                method="PUT",
                url="/api/v1/maximum-path",
                category="maximum_paths",
                module="static_route",
                body=self.test_data.get('maximum_path_invalid_high', {
                    "number": 10  # 超出範圍 1-8
                }),
                expected_status=400,
                description="測試無效最大路徑數 - 超出上限"
            ),
            
            # 測試無效最大路徑數 - 低於下限
            self.create_test_case(
                name="static_route_test_invalid_max_paths_low",
                method="PUT",
                url="/api/v1/maximum-path",
                category="maximum_paths",
                module="static_route",
                body=self.test_data.get('maximum_path_invalid_low', {
                    "number": 0  # 低於範圍 1-8
                }),
                expected_status=400,
                description="測試無效最大路徑數 - 低於下限"
            ),
            
            # 驗證最大路徑數配置更新
            self.create_test_case(
                name="static_route_verify_maximum_paths_update",
                method="GET",
                url="/api/v1/maximum-path",
                category="maximum_paths",
                module="static_route",
                description="驗證最大路徑數配置更新效果"
            ),
            
            # 恢復默認最大路徑數
            self.create_test_case(
                name="static_route_restore_default_maximum_paths",
                method="PUT",
                url="/api/v1/maximum-path",
                category="maximum_paths",
                module="static_route",
                body=self.test_data.get('maximum_path_default', {
                    "number": 8
                }),
                description="恢復默認最大路徑數 (8)"
            )
        ]