#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNS 模組測試案例
包含DNS配置管理、域名解析、緩存管理等相關API測試
支援域名查找、域名服務器配置、主機記錄管理、DNS緩存清理等操作
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class DNSTests(BaseTests):
    """DNS 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取DNS模組支援的類別"""
        return [
            "dns_information_query",
            "dns_configuration_management",
            "dns_domain_management",
            "dns_nameserver_management", 
            "dns_host_records_management",
            "dns_cache_management",
            "dns_advanced_operations",
            "dns_error_handling"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有DNS測試案例"""
        all_tests = []
        all_tests.extend(self.get_dns_information_query_tests())
        all_tests.extend(self.get_dns_configuration_management_tests())
        all_tests.extend(self.get_dns_domain_management_tests())
        all_tests.extend(self.get_dns_nameserver_management_tests())
        all_tests.extend(self.get_dns_host_records_management_tests())
        all_tests.extend(self.get_dns_cache_management_tests())
        all_tests.extend(self.get_dns_advanced_operations_tests())
        all_tests.extend(self.get_dns_error_handling_tests())
        return all_tests
    
    def get_dns_information_query_tests(self) -> List[APITestCase]:
        """DNS Information Query API 測試案例"""
        return [
            # 獲取DNS信息
            self.create_test_case(
                name="dns_get_information",
                method="GET",
                url="/api/v1/dns",
                category="dns_information_query",
                module="dns",
                description="獲取DNS信息"
            ),
            
            # 驗證DNS響應格式
            self.create_test_case(
                name="dns_verify_response_format",
                method="GET",
                url="/api/v1/dns",
                category="dns_information_query",
                module="dns",
                description="驗證DNS響應格式"
            ),
            
            # 檢查DNS信息完整性
            self.create_test_case(
                name="dns_check_information_completeness",
                method="GET",
                url="/api/v1/dns",
                category="dns_information_query",
                module="dns",
                description="檢查DNS信息完整性"
            ),
            
            # 多次查詢DNS信息一致性
            self.create_test_case(
                name="dns_multiple_query_consistency",
                method="GET",
                url="/api/v1/dns",
                category="dns_information_query",
                module="dns",
                description="多次查詢DNS信息一致性"
            ),
            
            # DNS查詢性能測試
            self.create_test_case(
                name="dns_query_performance_test",
                method="GET",
                url="/api/v1/dns",
                category="dns_information_query",
                module="dns",
                description="DNS查詢性能測試"
            )
        ]
    
    def get_dns_configuration_management_tests(self) -> List[APITestCase]:
        """DNS Configuration Management API 測試案例"""
        return [
            # 啟用域名查找功能
            self.create_test_case(
                name="dns_enable_domain_lookup",
                method="PUT",
                url="/api/v1/dns",
                category="dns_configuration_management",
                module="dns",
                body=self.test_data.get('dns_enable_domain_lookup', {
                    "domainLookup": True,
                    "domainName": "company.com",
                    "domainLists": [
                        {"listName": "company.com.local"},
                        {"listName": "company.com.internal"}
                    ],
                    "nameServerInets": [
                        {"ip": "8.8.8.8"},
                        {"ip": "8.8.4.4"}
                    ]
                }),
                description="啟用域名查找功能"
            ),
            
            # 禁用域名查找功能
            self.create_test_case(
                name="dns_disable_domain_lookup",
                method="PUT",
                url="/api/v1/dns",
                category="dns_configuration_management",
                module="dns",
                body=self.test_data.get('dns_disable_domain_lookup', {
                    "domainLookup": False
                }),
                description="禁用域名查找功能"
            ),
            
            # 重新啟用域名查找
            self.create_test_case(
                name="dns_re_enable_domain_lookup",
                method="PUT",
                url="/api/v1/dns",
                category="dns_configuration_management",
                module="dns",
                body=self.test_data.get('dns_re_enable_domain_lookup', {
                    "domainLookup": True,
                    "domainName": "example.org"
                }),
                description="重新啟用域名查找"
            ),
            
            # 驗證DNS配置更新
            self.create_test_case(
                name="dns_verify_configuration_update",
                method="GET",
                url="/api/v1/dns",
                category="dns_configuration_management",
                module="dns",
                description="驗證DNS配置更新"
            )
        ]
    
    def get_dns_domain_management_tests(self) -> List[APITestCase]:
        """DNS Domain Management API 測試案例"""
        return [
            # 設置主域名
            self.create_test_case(
                name="dns_set_primary_domain",
                method="PUT",
                url="/api/v1/dns",
                category="dns_domain_management",
                module="dns",
                body=self.test_data.get('dns_primary_domain', {
                    "domainLookup": True,
                    "domainName": "primary.example.com",
                    "domainLists": [
                        {"listName": "primary.example.com"}
                    ]
                }),
                description="設置主域名"
            ),
            
            # 配置多個域名列表
            self.create_test_case(
                name="dns_configure_multiple_domains",
                method="PUT",
                url="/api/v1/dns",
                category="dns_domain_management",
                module="dns",
                body=self.test_data.get('dns_multiple_domains', {
                    "domainLookup": True,
                    "domainName": "multi.example.com",
                    "domainLists": [
                        {"listName": "sample.com.jp"},
                        {"listName": "sample.com.tw"},
                        {"listName": "sample.com"}
                    ]
                }),
                description="配置多個域名列表"
            ),
            
            # 設置企業域名
            self.create_test_case(
                name="dns_set_enterprise_domain",
                method="PUT",
                url="/api/v1/dns",
                category="dns_domain_management",
                module="dns",
                body=self.test_data.get('dns_enterprise_domain', {
                    "domainLookup": True,
                    "domainName": "enterprise.local",
                    "domainLists": [
                        {"listName": "hr.enterprise.local"},
                        {"listName": "it.enterprise.local"},
                        {"listName": "finance.enterprise.local"}
                    ]
                }),
                description="設置企業域名"
            ),
            
            # 配置國際化域名
            self.create_test_case(
                name="dns_configure_international_domains",
                method="PUT",
                url="/api/v1/dns",
                category="dns_domain_management",
                module="dns",
                body=self.test_data.get('dns_international_domains', {
                    "domainLookup": True,
                    "domainName": "global.company.com",
                    "domainLists": [
                        {"listName": "us.company.com"},
                        {"listName": "eu.company.com"},
                        {"listName": "asia.company.com"}
                    ]
                }),
                description="配置國際化域名"
            ),
            
            # 驗證域名配置
            self.create_test_case(
                name="dns_verify_domain_configuration",
                method="GET",
                url="/api/v1/dns",
                category="dns_domain_management",
                module="dns",
                description="驗證域名配置"
            )
        ]
    
    def get_dns_nameserver_management_tests(self) -> List[APITestCase]:
        """DNS Nameserver Management API 測試案例"""
        return [
            # 配置公共DNS服務器
            self.create_test_case(
                name="dns_configure_public_nameservers",
                method="PUT",
                url="/api/v1/dns",
                category="dns_nameserver_management",
                module="dns",
                body=self.test_data.get('dns_public_nameservers', {
                    "domainLookup": True,
                    "nameServerInets": [
                        {"ip": "8.8.8.8"},
                        {"ip": "8.8.4.4"}
                    ]
                }),
                description="配置公共DNS服務器 (Google & Cloudflare)"
            ),
            
            # 配置企業內部DNS服務器
            self.create_test_case(
                name="dns_configure_internal_nameservers",
                method="PUT",
                url="/api/v1/dns",
                category="dns_nameserver_management",
                module="dns",
                body=self.test_data.get('dns_internal_nameservers', {
                    "domainLookup": True,
                    "nameServerInets": [
                        {"ip": "192.168.1.10"},
                        {"ip": "192.168.1.11"},
                        {"ip": "10.0.0.53"}
                    ]
                }),
                description="配置企業內部DNS服務器"
            ),
            
            # 配置混合DNS服務器
            self.create_test_case(
                name="dns_configure_hybrid_nameservers",
                method="PUT",
                url="/api/v1/dns",
                category="dns_nameserver_management",
                module="dns",
                body=self.test_data.get('dns_hybrid_nameservers', {
                    "domainLookup": True,
                    "nameServerInets": [
                        {"ip": "192.168.96.6"},
                        {"ip": "192.168.112.5"},
                        {"ip": "8.8.8.8"}
                    ]
                }),
                description="配置混合DNS服務器 (內部+公共)"
            ),
            
            # 配置IPv6 DNS服務器
            self.create_test_case(
                name="dns_configure_ipv6_nameservers",
                method="PUT",
                url="/api/v1/dns",
                category="dns_nameserver_management",
                module="dns",
                body=self.test_data.get('dns_ipv6_nameservers', {
                    "domainLookup": True,
                    "nameServerInets": [
                        {"ip": "2001:4860:4860::8888"},
                        {"ip": "2001:4860:4860::8844"},
                        {"ip": "192.168.1.53"}
                    ]
                }),
                description="配置IPv6 DNS服務器"
            ),
            
            # 配置單一DNS服務器
            # (Failed to delete static DNS name server.)
            self.create_test_case(
                name="dns_configure_single_nameserver",
                method="PUT",
                url="/api/v1/dns",
                category="dns_nameserver_management",
                module="dns",
                body=self.test_data.get('dns_single_nameserver', {
                    "domainLookup": True,
                    "nameServerInets": [
                        {"ip": "10.1.0.20"}
                    ]
                }),
                description="配置單一DNS服務器"
            ),
            
            # 驗證DNS服務器配置
            self.create_test_case(
                name="dns_verify_nameserver_configuration",
                method="GET",
                url="/api/v1/dns",
                category="dns_nameserver_management",
                module="dns",
                description="驗證DNS服務器配置"
            )
        ]
    
    def get_dns_host_records_management_tests(self) -> List[APITestCase]:
        """DNS Host Records Management API 測試案例"""
        return [
            # 配置靜態主機記錄
            self.create_test_case(
                name="dns_configure_static_host_records",
                method="PUT",
                url="/api/v1/dns",
                category="dns_host_records_management",
                module="dns",
                body=self.test_data.get('dns_static_host_records', {
                    "domainLookup": True,
                    "hosts": [
                        {
                            "hostIp": "192.168.1.55",
                            "hostName": "server1.local"
                        },
                        {
                            "hostIp": "192.168.1.56", 
                            "hostName": "server2.local"
                        }
                    ]
                }),
                description="配置靜態主機記錄"
            ),
            
            # 配置Web服務器記錄
            self.create_test_case(
                name="dns_configure_web_server_records",
                method="PUT",
                url="/api/v1/dns",
                category="dns_host_records_management",
                module="dns",
                body=self.test_data.get('dns_web_server_records', {
                    "domainLookup": True,
                    "hosts": [
                        {
                            "hostIp": "192.168.115.16",
                            "hostName": "www.company.com"
                        },
                        {
                            "hostIp": "192.168.115.17",
                            "hostName": "mail.company.com"
                        },
                        {
                            "hostIp": "192.168.115.18",
                            "hostName": "ftp.company.com"
                        }
                    ]
                }),
                description="配置Web服務器記錄"
            ),
            
            # 配置數據庫服務器記錄
            self.create_test_case(
                name="dns_configure_database_server_records",
                method="PUT",
                url="/api/v1/dns",
                category="dns_host_records_management",
                module="dns",
                body=self.test_data.get('dns_database_server_records', {
                    "domainLookup": True,
                    "hosts": [
                        {
                            "hostIp": "10.0.1.100",
                            "hostName": "db-primary.internal"
                        },
                        {
                            "hostIp": "10.0.1.101",
                            "hostName": "db-secondary.internal"
                        }
                    ]
                }),
                description="配置數據庫服務器記錄"
            ),
            
            # 配置應用服務器記錄
            self.create_test_case(
                name="dns_configure_application_server_records",
                method="PUT",
                url="/api/v1/dns",
                category="dns_host_records_management",
                module="dns",
                body=self.test_data.get('dns_application_server_records', {
                    "domainLookup": True,
                    "hosts": [
                        {
                            "hostIp": "172.16.1.50",
                            "hostName": "app1.enterprise.local"
                        },
                        {
                            "hostIp": "172.16.1.51",
                            "hostName": "app2.enterprise.local"
                        },
                        {
                            "hostIp": "172.16.1.52",
                            "hostName": "api.enterprise.local"
                        }
                    ]
                }),
                description="配置應用服務器記錄"
            ),
            
            # 驗證主機記錄配置
            self.create_test_case(
                name="dns_verify_host_records_configuration",
                method="GET",
                url="/api/v1/dns",
                category="dns_host_records_management",
                module="dns",
                description="驗證主機記錄配置"
            )
        ]
    
    def get_dns_cache_management_tests(self) -> List[APITestCase]:
        """DNS Cache Management API 測試案例"""
        return [
            # 檢查DNS緩存狀態
            self.create_test_case(
                name="dns_check_cache_status",
                method="GET",
                url="/api/v1/dns",
                category="dns_cache_management",
                module="dns",
                description="檢查DNS緩存狀態"
            ),
            
            # 清理所有DNS緩存
            self.create_test_case(
                name="dns_clear_all_caches",
                method="PUT",
                url="/api/v1/dns/caches:clear",
                category="dns_cache_management",
                module="dns",
                body={},
                description="清理所有DNS緩存"
            ),
            
            # 驗證緩存清理結果
            self.create_test_case(
                name="dns_verify_cache_clear_result",
                method="GET",
                url="/api/v1/dns",
                category="dns_cache_management",
                module="dns",
                description="驗證緩存清理結果"
            ),
            
            # 重新配置DNS以生成新緩存
            # (Failed to delete static DNS name server.)
            self.create_test_case(
                name="dns_reconfigure_for_new_cache",
                method="PUT",
                url="/api/v1/dns",
                category="dns_cache_management",
                module="dns",
                body=self.test_data.get('dns_reconfigure_for_cache', {
                    "domainLookup": True,
                    "domainName": "cache-test.com",
                    "nameServerInets": [
                        {"ip": "8.8.8.8"}
                    ]
                }),
                description="重新配置DNS以生成新緩存"
            ),
            
            # 再次清理DNS緩存
            self.create_test_case(
                name="dns_clear_caches_again",
                method="PUT",
                url="/api/v1/dns/caches:clear",
                category="dns_cache_management",
                module="dns",
                body={},
                description="再次清理DNS緩存"
            ),
            
            # 最終緩存狀態檢查
            self.create_test_case(
                name="dns_final_cache_status_check",
                method="GET",
                url="/api/v1/dns",
                category="dns_cache_management",
                module="dns",
                description="最終緩存狀態檢查"
            )
        ]
    
    def get_dns_advanced_operations_tests(self) -> List[APITestCase]:
        """DNS Advanced Operations API 測試案例"""
        return [
            # 配置完整DNS環境
            # (Failed to delete static DNS name server.)
            self.create_test_case(
                name="dns_configure_complete_environment",
                method="PUT",
                url="/api/v1/dns",
                category="dns_advanced_operations",
                module="dns",
                body=self.test_data.get('dns_complete_environment', {
                    "domainLookup": True,
                    "domainName": "complete.example.com",
                    "domainLists": [
                        {"listName": "dev.complete.example.com"},
                        {"listName": "test.complete.example.com"},
                        {"listName": "prod.complete.example.com"}
                    ],
                    "nameServerInets": [
                        {"ip": "192.168.96.6"},
                        {"ip": "192.168.112.5"},
                        {"ip": "8.8.8.8"},
                        {"ip": "1.1.1.1"}
                    ],
                    "hosts": [
                        {"hostIp": "192.168.1.10", "hostName": "web.complete.example.com"},
                        {"hostIp": "192.168.1.11", "hostName": "db.complete.example.com"},
                        {"hostIp": "192.168.1.12", "hostName": "api.complete.example.com"}
                    ]
                }),
                description="配置完整DNS環境"
            ),
            
            # 批量配置主機記錄
            self.create_test_case(
                name="dns_batch_configure_host_records",
                method="PUT",
                url="/api/v1/dns",
                category="dns_advanced_operations",
                module="dns",
                body=self.test_data.get('dns_batch_host_records', {
                    "domainLookup": True,
                    "hosts": [
                        {"hostIp": "10.0.1.10", "hostName": "node1.cluster.local"},
                        {"hostIp": "10.0.1.11", "hostName": "node2.cluster.local"},
                        {"hostIp": "10.0.1.12", "hostName": "node3.cluster.local"},
                        {"hostIp": "10.0.1.13", "hostName": "node4.cluster.local"},
                        {"hostIp": "10.0.1.14", "hostName": "node5.cluster.local"}
                    ]
                }),
                description="批量配置主機記錄"
            ),
            
            # 動態調整DNS配置
            # (Failed to delete static DNS name server.)
            self.create_test_case(
                name="dns_dynamic_adjust_configuration",
                method="PUT",
                url="/api/v1/dns",
                category="dns_advanced_operations",
                module="dns",
                body=self.test_data.get('dns_dynamic_configuration', {
                    "domainLookup": True,
                    "domainName": "dynamic.local",
                    "nameServerInets": [
                        {"ip": "192.168.1.53"},
                        {"ip": "192.168.1.54"}
                    ]
                }),
                description="動態調整DNS配置"
            ),
            
            # 測試DNS配置切換
            # (Failed to delete static DNS name server.)
            self.create_test_case(
                name="dns_test_configuration_switching",
                method="PUT",
                url="/api/v1/dns",
                category="dns_advanced_operations",
                module="dns",
                body=self.test_data.get('dns_configuration_switching', {
                    "domainLookup": True,
                    "domainName": "switched.example.org",
                    "domainLists": [
                        {"listName": "new.switched.example.org"}
                    ],
                    "nameServerInets": [
                        {"ip": "9.9.9.9"},
                        {"ip": "149.112.112.112"}
                    ]
                }),
                description="測試DNS配置切換"
            ),
            
            # 驗證高級配置結果
            self.create_test_case(
                name="dns_verify_advanced_configuration_results",
                method="GET",
                url="/api/v1/dns",
                category="dns_advanced_operations",
                module="dns",
                description="驗證高級配置結果"
            ),
            
            # 清理高級配置緩存
            self.create_test_case(
                name="dns_clear_advanced_configuration_cache",
                method="PUT",
                url="/api/v1/dns/caches:clear",
                category="dns_advanced_operations",
                module="dns",
                body={},
                description="清理高級配置緩存"
            )
        ]
    
    def get_dns_error_handling_tests(self) -> List[APITestCase]:
        """DNS Error Handling API 測試案例"""
        return [
            # 測試無效IP地址格式
            self.create_test_case(
                name="dns_test_invalid_ip_format",
                method="PUT",
                url="/api/v1/dns",
                category="dns_error_handling",
                module="dns",
                body=self.test_data.get('dns_invalid_ip_format', {
                    "domainLookup": True,
                    "nameServerInets": [
                        {"ip": "invalid.ip.address"}
                    ]
                }),
                expected_status=500,
                description="測試無效IP地址格式"
            ),
            
            # 測試無效域名格式
            self.create_test_case(
                name="dns_test_invalid_domain_format",
                method="PUT",
                url="/api/v1/dns",
                category="dns_error_handling",
                module="dns",
                body=self.test_data.get('dns_invalid_domain_format', {
                    "domainLookup": True,
                    "domainName": "invalid..domain..name"
                }),
                expected_status=500,
                description="測試無效域名格式"
            ),
            
            # 測試超長域名
            self.create_test_case(
                name="dns_test_oversized_domain_name",
                method="PUT",
                url="/api/v1/dns",
                category="dns_error_handling",
                module="dns",
                body=self.test_data.get('dns_oversized_domain_name', {
                    "domainLookup": True,
                    "domainName": "a" * 128 + ".com"  # 超過127字符限制
                }),
                expected_status=200,
                description="測試超長域名 (超過127字符)"
            ),
            
            # 測試超長主機名
            self.create_test_case(
                name="dns_test_oversized_hostname",
                method="PUT",
                url="/api/v1/dns",
                category="dns_error_handling",
                module="dns",
                body=self.test_data.get('dns_oversized_hostname', {
                    "domainLookup": True,
                    "hosts": [
                        {
                            "hostIp": "192.168.1.100",
                            "hostName": "host" + "a" * 100 + ".local"  # 超過100字符限制
                        }
                    ]
                }),
                description="測試超長主機名 (超過100字符)"
            ),
            
            # 測試超過DNS服務器數量限制
            self.create_test_case(
                name="dns_test_exceed_nameserver_limit",
                method="PUT",
                url="/api/v1/dns",
                category="dns_error_handling",
                module="dns",
                body=self.test_data.get('dns_exceed_nameserver_limit', {
                    "domainLookup": True,
                    "nameServerInets": [
                        {"ip": "8.8.8.8"},
                        {"ip": "8.8.4.4"},
                        {"ip": "1.1.1.1"},
                        {"ip": "1.0.0.1"},
                        {"ip": "9.9.9.9"},
                        {"ip": "149.112.112.112"},
                        {"ip": "208.67.222.222"}  # 超過6個服務器限制
                    ]
                }),
                expected_status=500,
                description="測試超過DNS服務器數量限制 (超過6個)"
            ),
            
            # 測試無效JSON格式
            self.create_test_case(
                name="dns_test_invalid_json_format",
                method="PUT",
                url="/api/v1/dns",
                category="dns_error_handling",
                module="dns",
                body="invalid json format",
                expected_status=200,
                description="測試無效JSON格式"
            ),
            
            # 測試缺少必需參數
            self.create_test_case(
                name="dns_test_missing_required_parameters",
                method="PUT",
                url="/api/v1/dns",
                category="dns_error_handling",
                module="dns",
                body=self.test_data.get('dns_missing_required_params', {
                    "domainLookup": True,
                    "domainLists": [
                        {}  # 缺少listName
                    ]
                }),
                expected_status=200,
                description="測試缺少必需參數"
            ),
            
            # 測試空主機名
            self.create_test_case(
                name="dns_test_empty_hostname",
                method="PUT",
                url="/api/v1/dns",
                category="dns_error_handling",
                module="dns",
                body=self.test_data.get('dns_empty_hostname', {
                    "domainLookup": True,
                    "hosts": [
                        {
                            "hostIp": "192.168.1.100",
                            "hostName": ""  # 空主機名
                        }
                    ]
                }),
                description="測試空主機名"
            ),
            
            # 恢復正常DNS配置
            # (Failed to delete static DNS name server.)
            self.create_test_case(
                name="dns_restore_normal_configuration",
                method="PUT",
                url="/api/v1/dns",
                category="dns_error_handling",
                module="dns",
                body=self.test_data.get('dns_restore_normal_config', {
                    "domainLookup": True,
                    "domainName": "example.com",
                    "nameServerInets": [
                        {"ip": "8.8.8.8"}
                    ]
                }),
                description="恢復正常DNS配置"
            ),
            
            # 最終DNS狀態檢查
            self.create_test_case(
                name="dns_final_status_check",
                method="GET",
                url="/api/v1/dns",
                category="dns_error_handling",
                module="dns",
                description="最終DNS狀態檢查"
            )
        ]