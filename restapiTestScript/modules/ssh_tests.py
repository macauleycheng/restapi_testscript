#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSH 模組測試案例
包含SSH服務器配置、公鑰管理、主機密鑰管理、連接監控等相關API測試
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class SSHTests(BaseTests):
    """SSH 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取SSH模組支援的類別"""
        return [
            "ssh_server",
            "ssh_public_keys",
            "ssh_host_keys",
            "ssh_connections"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有SSH測試案例"""
        all_tests = []
        all_tests.extend(self.get_ssh_server_tests())
        all_tests.extend(self.get_ssh_public_keys_tests())
        all_tests.extend(self.get_ssh_host_keys_tests())
        all_tests.extend(self.get_ssh_connections_tests())
        return all_tests
    
    def get_ssh_server_tests(self) -> List[APITestCase]:
        """SSH Server API 測試案例"""
        return [
            # 獲取SSH服務器信息
            self.create_test_case(
                name="ssh_get_server_info",
                method="GET",
                url="/api/v1/ssh",
                category="ssh_server",
                module="ssh",
                description="獲取SSH服務器配置信息"
            ),
            
            # 更新SSH服務器基本配置
            self.create_test_case(
                name="ssh_update_basic_config",
                method="PUT",
                url="/api/v1/ssh",
                category="ssh_server",
                module="ssh",
                body=self.test_data.get('ssh_basic_config', {
                    "sshServerStatus": True,
                    "sshTimeout": 120,
                    "sshAuthRetries": 3,
                    "sshKeySize": 768
                }),
                description="更新SSH服務器基本配置"
            ),
            
            # 啟用SSH服務器
            self.create_test_case(
                name="ssh_enable_server",
                method="PUT",
                url="/api/v1/ssh",
                category="ssh_server",
                module="ssh",
                body=self.test_data.get('ssh_enable_server', {
                    "sshServerStatus": True
                }),
                description="啟用SSH服務器"
            ),
            
            # 配置SSH超時時間 - 最小值
            self.create_test_case(
                name="ssh_configure_min_timeout",
                method="PUT",
                url="/api/v1/ssh",
                category="ssh_server",
                module="ssh",
                body=self.test_data.get('ssh_min_timeout', {
                    "sshServerStatus": True,
                    "sshTimeout": 1
                }),
                description="配置SSH超時時間為最小值 (1秒)"
            ),
            
            # 配置SSH超時時間 - 最大值
            self.create_test_case(
                name="ssh_configure_max_timeout",
                method="PUT",
                url="/api/v1/ssh",
                category="ssh_server",
                module="ssh",
                body=self.test_data.get('ssh_max_timeout', {
                    "sshServerStatus": True,
                    "sshTimeout": 120
                }),
                description="配置SSH超時時間為最大值 (120秒)"
            ),
            
            # 配置SSH認證重試次數 - 最小值
            self.create_test_case(
                name="ssh_configure_min_auth_retries",
                method="PUT",
                url="/api/v1/ssh",
                category="ssh_server",
                module="ssh",
                body=self.test_data.get('ssh_min_auth_retries', {
                    "sshServerStatus": True,
                    "sshAuthRetries": 1
                }),
                description="配置SSH認證重試次數為最小值 (1次)"
            ),
            
            # 配置SSH認證重試次數 - 最大值
            self.create_test_case(
                name="ssh_configure_max_auth_retries",
                method="PUT",
                url="/api/v1/ssh",
                category="ssh_server",
                module="ssh",
                body=self.test_data.get('ssh_max_auth_retries', {
                    "sshServerStatus": True,
                    "sshAuthRetries": 5
                }),
                description="配置SSH認證重試次數為最大值 (5次)"
            ),
            
            # 配置SSH密鑰大小 - 最小值
            self.create_test_case(
                name="ssh_configure_min_key_size",
                method="PUT",
                url="/api/v1/ssh",
                category="ssh_server",
                module="ssh",
                body=self.test_data.get('ssh_min_key_size', {
                    "sshServerStatus": True,
                    "sshKeySize": 512
                }),
                description="配置SSH密鑰大小為最小值 (512位)"
            ),
            
            # 配置SSH密鑰大小 - 最大值
            self.create_test_case(
                name="ssh_configure_max_key_size",
                method="PUT",
                url="/api/v1/ssh",
                category="ssh_server",
                module="ssh",
                body=self.test_data.get('ssh_max_key_size', {
                    "sshServerStatus": True,
                    "sshKeySize": 896
                }),
                description="配置SSH密鑰大小為最大值 (896位)"
            ),
            
            # 配置完整SSH設置
            self.create_test_case(
                name="ssh_configure_complete_settings",
                method="PUT",
                url="/api/v1/ssh",
                category="ssh_server",
                module="ssh",
                body=self.test_data.get('ssh_complete_config', {
                    "sshServerStatus": True,
                    "sshTimeout": 60,
                    "sshAuthRetries": 3,
                    "sshKeySize": 768
                }),
                description="配置完整SSH服務器設置"
            ),
            
            # 禁用SSH服務器
            self.create_test_case(
                name="ssh_disable_server",
                method="PUT",
                url="/api/v1/ssh",
                category="ssh_server",
                module="ssh",
                body=self.test_data.get('ssh_disable_server', {
                    "sshServerStatus": False
                }),
                description="禁用SSH服務器"
            ),
            
            # 重新啟用SSH服務器
            self.create_test_case(
                name="ssh_re_enable_server",
                method="PUT",
                url="/api/v1/ssh",
                category="ssh_server",
                module="ssh",
                body=self.test_data.get('ssh_re_enable_server', {
                    "sshServerStatus": True,
                    "sshTimeout": 90,
                    "sshAuthRetries": 4,
                    "sshKeySize": 768
                }),
                description="重新啟用SSH服務器"
            ),
            
            # 測試無效參數 - 超時時間超出範圍
            self.create_test_case(
                name="ssh_test_invalid_timeout",
                method="PUT",
                url="/api/v1/ssh",
                category="ssh_server",
                module="ssh",
                body=self.test_data.get('ssh_invalid_timeout', {
                    "sshServerStatus": True,
                    "sshTimeout": 150  # 超出範圍 1-120
                }),
                expected_status=400,
                description="測試無效SSH超時時間"
            ),
            
            # 測試無效參數 - 認證重試次數超出範圍
            self.create_test_case(
                name="ssh_test_invalid_auth_retries",
                method="PUT",
                url="/api/v1/ssh",
                category="ssh_server",
                module="ssh",
                body=self.test_data.get('ssh_invalid_auth_retries', {
                    "sshServerStatus": True,
                    "sshAuthRetries": 10  # 超出範圍 1-5
                }),
                expected_status=400,
                description="測試無效SSH認證重試次數"
            ),
            
            # 測試無效參數 - 密鑰大小超出範圍
            self.create_test_case(
                name="ssh_test_invalid_key_size",
                method="PUT",
                url="/api/v1/ssh",
                category="ssh_server",
                module="ssh",
                body=self.test_data.get('ssh_invalid_key_size', {
                    "sshServerStatus": True,
                    "sshKeySize": 1024  # 超出範圍 512-896
                }),
                expected_status=400,
                description="測試無效SSH密鑰大小"
            ),
            
            # 驗證SSH配置更新效果
            self.create_test_case(
                name="ssh_verify_configuration_update",
                method="GET",
                url="/api/v1/ssh",
                category="ssh_server",
                module="ssh",
                description="驗證SSH配置更新效果"
            )
        ]
    
    def get_ssh_public_keys_tests(self) -> List[APITestCase]:
        """SSH Public Keys API 測試案例"""
        return [
            # 獲取所有SSH用戶公鑰
            self.create_test_case(
                name="ssh_get_all_public_keys",
                method="GET",
                url="/api/v1/ssh/public-keys",
                category="ssh_public_keys",
                module="ssh",
                description="獲取所有SSH用戶公鑰"
            ),
            
            # 從TFTP服務器複製RSA公鑰
            self.create_test_case(
                name="ssh_copy_rsa_key_from_tftp",
                method="POST",
                url="/api/v1/ssh/public-keys",
                category="ssh_public_keys",
                module="ssh",
                body=self.test_data.get('ssh_copy_rsa_tftp', {
                    "srcOperType": "tftp",
                    "destOperType": "public-key",
                    "serverIp": "192.168.115.95",
                    "publicKeyType": "rsa",
                    "srcFileName": "rsa.pub",
                    "keyUserName": "testuser"
                }),
                description="從TFTP服務器複製RSA公鑰"
            ),
            
            # 從FTP服務器複製RSA公鑰
            self.create_test_case(
                name="ssh_copy_rsa_key_from_ftp",
                method="POST",
                url="/api/v1/ssh/public-keys",
                category="ssh_public_keys",
                module="ssh",
                body=self.test_data.get('ssh_copy_rsa_ftp', {
                    "srcOperType": "ftp",
                    "destOperType": "public-key",
                    "serverIp": "192.168.115.95",
                    "username": "ftpuser",
                    "password": "ftppass",
                    "publicKeyType": "rsa",
                    "srcFileName": "rsa_key.pub",
                    "keyUserName": "ftpuser"
                }),
                description="從FTP服務器複製RSA公鑰"
            ),
            
            # 獲取特定用戶公鑰 - admin
            self.create_test_case(
                name="ssh_get_admin_public_key",
                method="GET",
                url="/api/v1/ssh/public-keys/username/{username}",
                category="ssh_public_keys",
                module="ssh",
                params={"username": "admin"},
                description="獲取admin用戶的SSH公鑰"
            ),
            
            # 獲取特定用戶公鑰 - testuser
            self.create_test_case(
                name="ssh_get_testuser_public_key",
                method="GET",
                url="/api/v1/ssh/public-keys/username/{username}",
                category="ssh_public_keys",
                module="ssh",
                params={"username": "testuser"},
                description="獲取testuser用戶的SSH公鑰"
            ),
            
            # 獲取參數化用戶公鑰
            self.create_test_case(
                name="ssh_get_parameterized_user_public_key",
                method="GET",
                url="/api/v1/ssh/public-keys/username/{username}",
                category="ssh_public_keys",
                module="ssh",
                params={"username": self.params.get('ssh_username', 'admin')},
                description=f"獲取用戶 {self.params.get('ssh_username', 'admin')} 的SSH公鑰"
            ),
            
            # 刪除用戶RSA公鑰
            self.create_test_case(
                name="ssh_delete_user_rsa_key",
                method="DELETE",
                url="/api/v1/ssh/public-keys/username/{username}",
                category="ssh_public_keys",
                module="ssh",
                params={"username": "testuser"},
                body=self.test_data.get('ssh_delete_rsa_key', {
                    "publicKeyType": "rsa"
                }),
                description="刪除testuser用戶的RSA公鑰"
            ),
            
            # 刪除用戶所有公鑰
            self.create_test_case(
                name="ssh_delete_user_all_keys",
                method="DELETE",
                url="/api/v1/ssh/public-keys/username/{username}",
                category="ssh_public_keys",
                module="ssh",
                params={"username": "ftpuser"},
                description="刪除ftpuser用戶的所有公鑰"
            ),
            
            # 測試無效參數 - 無效服務器IP
            self.create_test_case(
                name="ssh_test_invalid_server_ip",
                method="POST",
                url="/api/v1/ssh/public-keys",
                category="ssh_public_keys",
                module="ssh",
                body=self.test_data.get('ssh_invalid_server_ip', {
                    "srcOperType": "tftp",
                    "destOperType": "public-key",
                    "serverIp": "999.999.999.999",
                    "publicKeyType": "rsa",
                    "srcFileName": "test.pub",
                    "keyUserName": "testuser"
                }),
                expected_status=400,
                description="測試無效服務器IP地址"
            ),
            
            # 測試無效參數 - 無效公鑰類型
            self.create_test_case(
                name="ssh_test_invalid_key_type",
                method="POST",
                url="/api/v1/ssh/public-keys",
                category="ssh_public_keys",
                module="ssh",
                body=self.test_data.get('ssh_invalid_key_type', {
                    "srcOperType": "tftp",
                    "destOperType": "public-key",
                    "serverIp": "192.168.115.95",
                    "publicKeyType": "invalid",
                    "srcFileName": "test.pub",
                    "keyUserName": "testuser"
                }),
                expected_status=400,
                description="測試無效公鑰類型"
            ),
            
            # 測試缺少必要參數
            self.create_test_case(
                name="ssh_test_missing_required_param",
                method="POST",
                url="/api/v1/ssh/public-keys",
                category="ssh_public_keys",
                module="ssh",
                body=self.test_data.get('ssh_missing_param', {
                    "srcOperType": "tftp",
                    "destOperType": "public-key",
                    "serverIp": "192.168.115.95",
                    "publicKeyType": "rsa"
                    # 缺少 srcFileName 和 keyUserName
                }),
                expected_status=400,
                description="測試缺少必要參數"
            ),
            
            # 測試獲取不存在用戶的公鑰
            self.create_test_case(
                name="ssh_get_nonexistent_user_key",
                method="GET",
                url="/api/v1/ssh/public-keys/username/{username}",
                category="ssh_public_keys",
                module="ssh",
                params={"username": "nonexistent"},
                expected_status=404,
                description="測試獲取不存在用戶的公鑰"
            )
        ]
    
    def get_ssh_host_keys_tests(self) -> List[APITestCase]:
        """SSH Host Keys API 測試案例"""
        return [
            # 獲取所有SSH主機密鑰
            self.create_test_case(
                name="ssh_get_all_host_keys",
                method="GET",
                url="/api/v1/ssh/host-keys",
                category="ssh_host_keys",
                module="ssh",
                description="獲取所有SSH主機密鑰"
            ),
            
            # 生成RSA主機密鑰
            self.create_test_case(
                name="ssh_generate_rsa_host_key",
                method="POST",
                url="/api/v1/ssh/host-keys",
                category="ssh_host_keys",
                module="ssh",
                body=self.test_data.get('ssh_generate_rsa_key', {
                    "keyType": "rsa"
                }),
                description="生成RSA主機密鑰"
            ),
            
            # 獲取RSA主機密鑰
            self.create_test_case(
                name="ssh_get_rsa_host_key",
                method="GET",
                url="/api/v1/ssh/host-keys/key-type/{keyType}",
                category="ssh_host_keys",
                module="ssh",
                params={"keyType": "rsa"},
                description="獲取RSA主機密鑰"
            ),
            
            # 獲取參數化主機密鑰
            self.create_test_case(
                name="ssh_get_parameterized_host_key",
                method="GET",
                url="/api/v1/ssh/host-keys/key-type/{keyType}",
                category="ssh_host_keys",
                module="ssh",
                params={"keyType": self.params.get('ssh_key_type', 'rsa')},
                description=f"獲取 {self.params.get('ssh_key_type', 'rsa')} 主機密鑰"
            ),
            
            # 保存SSH主機密鑰
            self.create_test_case(
                name="ssh_save_host_keys",
                method="PUT",
                url="/api/v1/ssh/host-keys:save",
                category="ssh_host_keys",
                module="ssh",
                body={},
                description="保存SSH主機密鑰到配置"
            ),
            
            # 刪除RSA主機密鑰
            self.create_test_case(
                name="ssh_delete_rsa_host_key",
                method="DELETE",
                url="/api/v1/ssh/host-keys/key-type/{keyType}",
                category="ssh_host_keys",
                module="ssh",
                params={"keyType": "rsa"},
                description="刪除RSA主機密鑰"
            ),
            
            # 重新生成RSA主機密鑰
            self.create_test_case(
                name="ssh_regenerate_rsa_host_key",
                method="POST",
                url="/api/v1/ssh/host-keys",
                category="ssh_host_keys",
                module="ssh",
                body=self.test_data.get('ssh_regenerate_rsa_key', {
                    "keyType": "rsa"
                }),
                description="重新生成RSA主機密鑰"
            ),
            
            # 測試無效密鑰類型
            self.create_test_case(
                name="ssh_test_invalid_host_key_type",
                method="POST",
                url="/api/v1/ssh/host-keys",
                category="ssh_host_keys",
                module="ssh",
                body=self.test_data.get('ssh_invalid_host_key_type', {
                    "keyType": "invalid"
                }),
                expected_status=400,
                description="測試無效主機密鑰類型"
            ),
            
            # 測試獲取不存在的密鑰類型
            self.create_test_case(
                name="ssh_get_nonexistent_key_type",
                method="GET",
                url="/api/v1/ssh/host-keys/key-type/{keyType}",
                category="ssh_host_keys",
                module="ssh",
                params={"keyType": "nonexistent"},
                expected_status=400,
                description="測試獲取不存在的密鑰類型"
            ),
            
            # 測試刪除不存在的密鑰類型
            self.create_test_case(
                name="ssh_delete_nonexistent_key_type",
                method="DELETE",
                url="/api/v1/ssh/host-keys/key-type/{keyType}",
                category="ssh_host_keys",
                module="ssh",
                params={"keyType": "nonexistent"},
                expected_status=400,
                description="測試刪除不存在的密鑰類型"
            ),
            
            # 驗證主機密鑰生成效果
            self.create_test_case(
                name="ssh_verify_host_key_generation",
                method="GET",
                url="/api/v1/ssh/host-keys",
                category="ssh_host_keys",
                module="ssh",
                description="驗證主機密鑰生成效果"
            ),
            
            # 再次保存主機密鑰
            self.create_test_case(
                name="ssh_save_host_keys_again",
                method="PUT",
                url="/api/v1/ssh/host-keys:save",
                category="ssh_host_keys",
                module="ssh",
                body={},
                description="再次保存SSH主機密鑰"
            )
        ]
    
    def get_ssh_connections_tests(self) -> List[APITestCase]:
        """SSH Connections API 測試案例"""
        return [
            # 獲取SSH連接信息
            self.create_test_case(
                name="ssh_get_connections_info",
                method="GET",
                url="/api/v1/ssh/connections",
                category="ssh_connections",
                module="ssh",
                description="獲取SSH連接信息"
            ),
            
            # 監控SSH連接狀態 - 第1次檢查
            self.create_test_case(
                name="ssh_monitor_connections_1",
                method="GET",
                url="/api/v1/ssh/connections",
                category="ssh_connections",
                module="ssh",
                description="監控SSH連接狀態 - 第1次檢查"
            ),
            
            # 監控SSH連接狀態 - 第2次檢查
            self.create_test_case(
                name="ssh_monitor_connections_2",
                method="GET",
                url="/api/v1/ssh/connections",
                category="ssh_connections",
                module="ssh",
                description="監控SSH連接狀態 - 第2次檢查"
            ),
            
            # 監控SSH連接狀態 - 第3次檢查
            self.create_test_case(
                name="ssh_monitor_connections_3",
                method="GET",
                url="/api/v1/ssh/connections",
                category="ssh_connections",
                module="ssh",
                description="監控SSH連接狀態 - 第3次檢查"
            ),
            
            # 檢查SSH連接詳細信息
            self.create_test_case(
                name="ssh_check_connection_details",
                method="GET",
                url="/api/v1/ssh/connections",
                category="ssh_connections",
                module="ssh",
                description="檢查SSH連接詳細信息"
            ),
            
            # 驗證SSH版本信息
            self.create_test_case(
                name="ssh_verify_version_info",
                method="GET",
                url="/api/v1/ssh/connections",
                category="ssh_connections",
                module="ssh",
                description="驗證SSH版本信息"
            ),
            
            # 檢查SSH加密算法
            self.create_test_case(
                name="ssh_check_encryption_algorithms",
                method="GET",
                url="/api/v1/ssh/connections",
                category="ssh_connections",
                module="ssh",
                description="檢查SSH加密算法"
            ),
            
            # 監控SSH連接變化
            self.create_test_case(
                name="ssh_monitor_connection_changes",
                method="GET",
                url="/api/v1/ssh/connections",
                category="ssh_connections",
                module="ssh",
                description="監控SSH連接變化"
            )
        ]