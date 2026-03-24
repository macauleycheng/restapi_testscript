#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NTP 模組測試案例
包含NTP配置和信息獲取相關API測試
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class NTPTests(BaseTests):
    """NTP 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取NTP模組支援的類別"""
        return [
            "ntp_config"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有NTP測試案例"""
        all_tests = []
        all_tests.extend(self.get_ntp_config_tests())
        return all_tests
    
    def get_ntp_config_tests(self) -> List[APITestCase]:
        """NTP Configuration API 測試案例"""
        return [
            # 獲取NTP信息
            self.create_test_case(
                name="ntp_get_information",
                method="GET",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                description="獲取NTP配置信息"
            ),
            
            # 啟用NTP客戶端 - 基本配置
            self.create_test_case(
                name="ntp_enable_basic_config",
                method="PUT",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                body=self.test_data.get('ntp_enable_basic', {
                    "ntpStatus": True,
                    "ntpAuthenticateStatus": False,
                    "ntpServers": [
                        {
                            "ipAddress": "192.168.1.175",
                            "version": 3
                        }
                    ]
                }),
                description="啟用NTP客戶端 - 基本配置"
            ),
            
            # 配置NTP服務器 - 單個服務器
            self.create_test_case(
                name="ntp_configure_single_server",
                method="PUT",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                body=self.test_data.get('ntp_single_server', {
                    "ntpStatus": True,
                    "ntpAuthenticateStatus": False,
                    "ntpServers": [
                        {
                            "ipAddress": "pool.ntp.org",
                            "version": 4
                        }
                    ]
                }),
                description="配置NTP服務器 - 單個服務器"
            ),
            
            # 配置NTP服務器 - 多個服務器
            self.create_test_case(
                name="ntp_configure_multiple_servers",
                method="PUT",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                body=self.test_data.get('ntp_multiple_servers', {
                    "ntpStatus": True,
                    "ntpAuthenticateStatus": False,
                    "ntpServers": [
                        {
                            "ipAddress": "192.168.1.175",
                            "version": 3
                        },
                        {
                            "ipAddress": "time.google.com",
                            "version": 4
                        },
                        {
                            "ipAddress": "pool.ntp.org",
                            "version": 4
                        }
                    ]
                }),
                description="配置NTP服務器 - 多個服務器"
            ),
            
            # 啟用NTP認證 - 帶認證密鑰
            self.create_test_case(
                name="ntp_enable_authentication",
                method="PUT",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                body=self.test_data.get('ntp_with_auth', {
                    "ntpStatus": True,
                    "ntpAuthenticateStatus": True,
                    "ntpServers": [
                        {
                            "ipAddress": "192.168.1.175",
                            "version": 3,
                            "keyId": 1
                        }
                    ],
                    "ntpAuthKeys": [
                        {
                            "keyId": 1,
                            "md5Key": "1234567890"
                        }
                    ]
                }),
                description="啟用NTP認證 - 帶認證密鑰"
            ),
            
            # 配置複雜NTP認證 - 多個密鑰
            self.create_test_case(
                name="ntp_configure_multiple_auth_keys",
                method="PUT",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                body=self.test_data.get('ntp_multiple_auth_keys', {
                    "ntpStatus": True,
                    "ntpAuthenticateStatus": True,
                    "ntpServers": [
                        {
                            "ipAddress": "192.168.1.175",
                            "version": 3,
                            "keyId": 1
                        },
                        {
                            "ipAddress": "192.168.1.176",
                            "version": 4,
                            "keyId": 2
                        }
                    ],
                    "ntpAuthKeys": [
                        {
                            "keyId": 1,
                            "md5Key": "837J34Q69G0477L18708P86779"
                        },
                        {
                            "keyId": 2,
                            "md5Key": "SecureKey123456789"
                        }
                    ]
                }),
                description="配置複雜NTP認證 - 多個密鑰"
            ),
            
            # 配置不同NTP版本
            self.create_test_case(
                name="ntp_configure_different_versions",
                method="PUT",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                body=self.test_data.get('ntp_different_versions', {
                    "ntpStatus": True,
                    "ntpAuthenticateStatus": False,
                    "ntpServers": [
                        {
                            "ipAddress": "192.168.1.175",
                            "version": 2
                        },
                        {
                            "ipAddress": "192.168.1.176",
                            "version": 3
                        },
                        {
                            "ipAddress": "192.168.1.177",
                            "version": 4
                        }
                    ]
                }),
                description="配置不同NTP版本 (v2, v3, v4)"
            ),
            
            # 配置最大密鑰ID
            self.create_test_case(
                name="ntp_configure_max_key_id",
                method="PUT",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                body=self.test_data.get('ntp_max_key_id', {
                    "ntpStatus": True,
                    "ntpAuthenticateStatus": True,
                    "ntpServers": [
                        {
                            "ipAddress": "192.168.1.175",
                            "version": 4,
                            "keyId": 65535
                        }
                    ],
                    "ntpAuthKeys": [
                        {
                            "keyId": 65535,
                            "md5Key": "MaxKeyIdTest123456789012345"
                        }
                    ]
                }),
                description="配置最大密鑰ID (65535)"
            ),
            
            # 配置最小密鑰ID
            self.create_test_case(
                name="ntp_configure_min_key_id",
                method="PUT",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                body=self.test_data.get('ntp_min_key_id', {
                    "ntpStatus": True,
                    "ntpAuthenticateStatus": True,
                    "ntpServers": [
                        {
                            "ipAddress": "192.168.1.175",
                            "version": 4,
                            "keyId": 1
                        }
                    ],
                    "ntpAuthKeys": [
                        {
                            "keyId": 1,
                            "md5Key": "MinKeyIdTest"
                        }
                    ]
                }),
                description="配置最小密鑰ID (1)"
            ),
            
            # 配置長MD5密鑰 (32字符)
            self.create_test_case(
                name="ntp_configure_long_md5_key",
                method="PUT",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                body=self.test_data.get('ntp_long_md5_key', {
                    "ntpStatus": True,
                    "ntpAuthenticateStatus": True,
                    "ntpServers": [
                        {
                            "ipAddress": "192.168.1.175",
                            "version": 4,
                            "keyId": 10
                        }
                    ],
                    "ntpAuthKeys": [
                        {
                            "keyId": 10,
                            "md5Key": "ThisIsA32CharacterLongMD5Key123"
                        }
                    ]
                }),
                description="配置長MD5密鑰 (32字符)"
            ),
            
            # 配置短MD5密鑰
            self.create_test_case(
                name="ntp_configure_short_md5_key",
                method="PUT",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                body=self.test_data.get('ntp_short_md5_key', {
                    "ntpStatus": True,
                    "ntpAuthenticateStatus": True,
                    "ntpServers": [
                        {
                            "ipAddress": "192.168.1.175",
                            "version": 4,
                            "keyId": 5
                        }
                    ],
                    "ntpAuthKeys": [
                        {
                            "keyId": 5,
                            "md5Key": "short"
                        }
                    ]
                }),
                description="配置短MD5密鑰"
            ),
            
            # 禁用NTP客戶端
            self.create_test_case(
                name="ntp_disable_client",
                method="PUT",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                body=self.test_data.get('ntp_disable', {
                    "ntpStatus": False,
                    "ntpAuthenticateStatus": False
                }),
                description="禁用NTP客戶端"
            ),
            
            # 禁用NTP認證但保持客戶端啟用
            self.create_test_case(
                name="ntp_disable_authentication_only",
                method="PUT",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                body=self.test_data.get('ntp_disable_auth_only', {
                    "ntpStatus": True,
                    "ntpAuthenticateStatus": False,
                    "ntpServers": [
                        {
                            "ipAddress": "192.168.1.175",
                            "version": 4
                        }
                    ]
                }),
                description="禁用NTP認證但保持客戶端啟用"
            ),
            
            # 重新啟用NTP - 恢復配置
            self.create_test_case(
                name="ntp_re_enable_with_config",
                method="PUT",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                body=self.test_data.get('ntp_re_enable', {
                    "ntpStatus": True,
                    "ntpAuthenticateStatus": True,
                    "ntpServers": [
                        {
                            "ipAddress": "192.168.1.175",
                            "version": 3,
                            "keyId": 1
                        }
                    ],
                    "ntpAuthKeys": [
                        {
                            "keyId": 1,
                            "md5Key": "837J34Q69G0477L18708P86779"
                        }
                    ]
                }),
                description="重新啟用NTP - 恢復配置"
            ),
            
            # 測試無效參數 - 無效IP地址
            self.create_test_case(
                name="ntp_test_invalid_ip_address",
                method="PUT",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                body=self.test_data.get('ntp_invalid_ip', {
                    "ntpStatus": True,
                    "ntpAuthenticateStatus": False,
                    "ntpServers": [
                        {
                            "ipAddress": "999.999.999.999",
                            "version": 4
                        }
                    ]
                }),
                expected_status=400,
                description="測試無效IP地址"
            ),
            
            # 測試無效參數 - 無效密鑰ID (超出範圍)
            self.create_test_case(
                name="ntp_test_invalid_key_id_range",
                method="PUT",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                body=self.test_data.get('ntp_invalid_key_id', {
                    "ntpStatus": True,
                    "ntpAuthenticateStatus": True,
                    "ntpServers": [
                        {
                            "ipAddress": "192.168.1.175",
                            "version": 4,
                            "keyId": 70000  # 超出範圍 1-65535
                        }
                    ],
                    "ntpAuthKeys": [
                        {
                            "keyId": 70000,
                            "md5Key": "InvalidKeyId"
                        }
                    ]
                }),
                expected_status=400,
                description="測試無效密鑰ID (超出範圍)"
            ),
            
            # 測試無效參數 - MD5密鑰過長 (超過32字符)
            self.create_test_case(
                name="ntp_test_md5_key_too_long",
                method="PUT",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                body=self.test_data.get('ntp_md5_key_too_long', {
                    "ntpStatus": True,
                    "ntpAuthenticateStatus": True,
                    "ntpServers": [
                        {
                            "ipAddress": "192.168.1.175",
                            "version": 4,
                            "keyId": 1
                        }
                    ],
                    "ntpAuthKeys": [
                        {
                            "keyId": 1,
                            "md5Key": "ThisMD5KeyIsWayTooLongAndExceeds32Characters"
                        }
                    ]
                }),
                expected_status=400,
                description="測試MD5密鑰過長 (超過32字符)"
            ),
            
            # 測試無效參數 - MD5密鑰包含空格
            self.create_test_case(
                name="ntp_test_md5_key_with_spaces",
                method="PUT",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                body=self.test_data.get('ntp_md5_key_with_spaces', {
                    "ntpStatus": True,
                    "ntpAuthenticateStatus": True,
                    "ntpServers": [
                        {
                            "ipAddress": "192.168.1.175",
                            "version": 4,
                            "keyId": 1
                        }
                    ],
                    "ntpAuthKeys": [
                        {
                            "keyId": 1,
                            "md5Key": "Key With Spaces"
                        }
                    ]
                }),
                expected_status=400,
                description="測試MD5密鑰包含空格"
            ),
            
            # 測試無效JSON格式
            self.create_test_case(
                name="ntp_test_invalid_json",
                method="PUT",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                body='{"ntpStatus": true, "invalidField":}',  # 無效JSON
                expected_status=400,
                description="測試無效JSON格式"
            ),
            
            # 驗證NTP配置更新後的狀態
            self.create_test_case(
                name="ntp_verify_configuration_update",
                method="GET",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                description="驗證NTP配置更新後的狀態"
            ),
            
            # 監控NTP同步狀態
            self.create_test_case(
                name="ntp_monitor_sync_status_1",
                method="GET",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                description="監控NTP同步狀態 - 第1次檢查"
            ),
            
            self.create_test_case(
                name="ntp_monitor_sync_status_2",
                method="GET",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                description="監控NTP同步狀態 - 第2次檢查"
            ),
            
            self.create_test_case(
                name="ntp_monitor_sync_status_3",
                method="GET",
                url="/api/v1/ntp",
                category="ntp_config",
                module="ntp",
                description="監控NTP同步狀態 - 第3次檢查"
            )
        ]