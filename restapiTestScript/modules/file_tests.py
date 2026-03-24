#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File 模組測試案例
包含文件管理、文件複製、配置保存、自動升級等相關API測試
支援配置文件、操作碼文件、文件複製、啟動文件管理、自動升級等操作
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class FILETests(BaseTests):
    """File 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取File模組支援的類別"""
        return [
            "file_information_query",
            "file_management_operations",
            "file_copy_operations",
            "file_configuration_management",
            "file_boot_management",
            "file_auto_upgrade_management",
            "file_advanced_operations",
            "file_error_handling"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有File測試案例"""
        all_tests = []
        all_tests.extend(self.get_file_information_query_tests())
        all_tests.extend(self.get_file_management_operations_tests())
        all_tests.extend(self.get_file_copy_operations_tests())
        all_tests.extend(self.get_file_configuration_management_tests())
        all_tests.extend(self.get_file_boot_management_tests())
        all_tests.extend(self.get_file_auto_upgrade_management_tests())
        all_tests.extend(self.get_file_advanced_operations_tests())
        all_tests.extend(self.get_file_error_handling_tests())
        return all_tests
    
    def get_file_information_query_tests(self) -> List[APITestCase]:
        """File Information Query API 測試案例"""
        return [
            # 獲取所有文件信息
            self.create_test_case(
                name="file_get_all_files",
                method="GET",
                url="/api/v1/file",
                category="file_information_query",
                module="file",
                description="獲取所有文件信息"
            ),
            
            # 獲取指定單元文件信息
            self.create_test_case(
                name="file_get_unit_files",
                method="GET",
                url="/api/v1/file?unitId=1",
                category="file_information_query",
                module="file",
                description="獲取指定單元文件信息"
            ),
            
            # 獲取配置文件信息
            self.create_test_case(
                name="file_get_config_files",
                method="GET",
                url="/api/v1/file?fileType=config",
                category="file_information_query",
                module="file",
                description="獲取配置文件信息"
            ),
            
            # 獲取操作碼文件信息
            self.create_test_case(
                name="file_get_opcode_files",
                method="GET",
                url="/api/v1/file?fileType=opcode",
                category="file_information_query",
                module="file",
                description="獲取操作碼文件信息"
            ),
            
            # 獲取特定文件詳細信息
            self.create_test_case(
                name="file_get_specific_file_info",
                method="GET",
                url="/api/v1/file/startup1.cfg/file-type/config",
                category="file_information_query",
                module="file",
                description="獲取特定文件詳細信息"
            ),
            
            # 驗證文件信息響應格式
            self.create_test_case(
                name="file_verify_response_format",
                method="GET",
                url="/api/v1/file",
                category="file_information_query",
                module="file",
                description="驗證文件信息響應格式"
            ),
            
            # 檢查文件信息完整性
            self.create_test_case(
                name="file_check_information_completeness",
                method="GET",
                url="/api/v1/file",
                category="file_information_query",
                module="file",
                description="檢查文件信息完整性"
            )
        ]
    
    def get_file_management_operations_tests(self) -> List[APITestCase]:
        """File Management Operations API 測試案例"""
        return [
            # 刪除配置文件
            self.create_test_case(
                name="file_delete_config_file",
                method="DELETE",
                url="/api/v1/file/test.cfg/file-type/config",
                category="file_management_operations",
                module="file",
                body=self.test_data.get('file_delete_config', {
                    "unitId": 1
                }),
                description="刪除配置文件"
            ),
            
            # 刪除操作碼文件
            self.create_test_case(
                name="file_delete_opcode_file",
                method="DELETE",
                url="/api/v1/file/old_version.bix/file-type/opcode",
                category="file_management_operations",
                module="file",
                body=self.test_data.get('file_delete_opcode', {
                    "unitId": 1
                }),
                description="刪除操作碼文件"
            ),
            
            # 驗證文件刪除結果
            self.create_test_case(
                name="file_verify_deletion_result",
                method="GET",
                url="/api/v1/file",
                category="file_management_operations",
                module="file",
                description="驗證文件刪除結果"
            ),
            
            # 檢查存儲空間狀態
            self.create_test_case(
                name="file_check_storage_space",
                method="GET",
                url="/api/v1/file",
                category="file_management_operations",
                module="file",
                description="檢查存儲空間狀態"
            )
        ]
    
    def get_file_copy_operations_tests(self) -> List[APITestCase]:
        """File Copy Operations API 測試案例"""
        return [
            # 獲取文件複製狀態
            self.create_test_case(
                name="file_get_copy_status",
                method="GET",
                url="/api/v1/file/copy",
                category="file_copy_operations",
                module="file",
                description="獲取文件複製狀態"
            ),
            
            # 文件到文件複製 - 配置文件
            self.create_test_case(
                name="file_copy_config_file_to_file",
                method="POST",
                url="/api/v1/file/copy",
                category="file_copy_operations",
                module="file",
                body=self.test_data.get('file_copy_config_to_file', {
                    "srcOperType": "file",
                    "destOperType": "file",
                    "fileType": "config",
                    "srcFileName": "startup1.cfg",
                    "destFileName": "backup.cfg"
                }),
                description="文件到文件複製 - 配置文件"
            ),
            
            # 文件到文件複製 - 操作碼文件
            self.create_test_case(
                name="file_copy_opcode_file_to_file",
                method="POST",
                url="/api/v1/file/copy",
                category="file_copy_operations",
                module="file",
                body=self.test_data.get('file_copy_opcode_to_file', {
                    "srcOperType": "file",
                    "destOperType": "file",
                    "fileType": "opcode",
                    "filePath": "/tmp/AS3000_52P_V07.12.18.bix",
                    "destFileName": "AS3000_52P_V07.12.18.bix"
                }),
                description="文件到文件複製 - 操作碼文件"
            ),
            
            # 文件到運行配置複製
            self.create_test_case(
                name="file_copy_file_to_running_config",
                method="POST",
                url="/api/v1/file/copy",
                category="file_copy_operations",
                module="file",
                body=self.test_data.get('file_copy_to_running_config', {
                    "srcOperType": "file",
                    "destOperType": "running-config",
                    "srcFileName": "startup1.cfg"
                }),
                description="文件到運行配置複製"
            ),
            
            # 文件到啟動配置複製
            self.create_test_case(
                name="file_copy_file_to_startup_config",
                method="POST",
                url="/api/v1/file/copy",
                category="file_copy_operations",
                module="file",
                body=self.test_data.get('file_copy_to_startup_config', {
                    "srcOperType": "file",
                    "destOperType": "startup-config",
                    "srcFileName": "running.cfg",
                    "destFileName": "startup1.cfg"
                }),
                description="文件到啟動配置複製"
            ),
            
            # 文件到TFTP服務器複製
            self.create_test_case(
                name="file_copy_file_to_tftp",
                method="POST",
                url="/api/v1/file/copy",
                category="file_copy_operations",
                module="file",
                body=self.test_data.get('file_copy_to_tftp', {
                    "srcOperType": "file",
                    "destOperType": "tftp",
                    "fileType": "config",
                    "serverIp": "192.168.1.175",
                    "srcFileName": "startup.cfg",
                    "destFileName": "backup.cfg"
                }),
                description="文件到TFTP服務器複製"
            ),
            
            # 文件到FTP服務器複製
            self.create_test_case(
                name="file_copy_file_to_ftp",
                method="POST",
                url="/api/v1/file/copy",
                category="file_copy_operations",
                module="file",
                body=self.test_data.get('file_copy_to_ftp', {
                    "srcOperType": "file",
                    "destOperType": "ftp",
                    "fileType": "opcode",
                    "serverIp": "192.168.1.175",
                    "srcFileName": "AS3000_52P_V08.27.10.06.bix",
                    "destFileName": "backup.bix",
                    "username": "ftpuser",
                    "password": "ftppass"
                }),
                description="文件到FTP服務器複製"
            ),
            
            # 文件到其他單元複製
            self.create_test_case(
                name="file_copy_file_to_unit",
                method="POST",
                url="/api/v1/file/copy",
                category="file_copy_operations",
                module="file",
                body=self.test_data.get('file_copy_to_unit', {
                    "srcOperType": "file",
                    "destOperType": "unit",
                    "fileType": "config",
                    "srcFileName": "startup.cfg",
                    "unitId": 2,
                    "destFileName": "sync.cfg"
                }),
                description="文件到其他單元複製"
            ),
            
            # TFTP到文件複製
            self.create_test_case(
                name="file_copy_tftp_to_file",
                method="POST",
                url="/api/v1/file/copy",
                category="file_copy_operations",
                module="file",
                body=self.test_data.get('file_copy_tftp_to_file', {
                    "srcOperType": "tftp",
                    "destOperType": "file",
                    "fileType": "opcode",
                    "serverIp": "192.168.1.175",
                    "srcFileName": "AS3000_52P_V07.23.18.13.bix",
                    "destFileName": "new_firmware.bix"
                }),
                description="TFTP到文件複製"
            ),
            
            # SFTP到啟動配置複製
            self.create_test_case(
                name="file_copy_sftp_to_startup_config",
                method="POST",
                url="/api/v1/file/copy",
                category="file_copy_operations",
                module="file",
                body=self.test_data.get('file_copy_sftp_to_startup', {
                    "srcOperType": "sftp",
                    "destOperType": "startup-config",
                    "serverIp": "192.168.1.175",
                    "srcFileName": "remote.cfg",
                    "destFileName": "startup_remote.cfg",
                    "username": "sftpuser",
                    "password": "sftppass"
                }),
                description="SFTP到啟動配置複製"
            ),
            
            # 檢查文件複製狀態
            self.create_test_case(
                name="file_check_copy_status",
                method="GET",
                url="/api/v1/file/copy",
                category="file_copy_operations",
                module="file",
                description="檢查文件複製狀態"
            )
        ]
    
    def get_file_configuration_management_tests(self) -> List[APITestCase]:
        """File Configuration Management API 測試案例"""
        return [
            # 保存運行配置到啟動配置
            self.create_test_case(
                name="file_save_running_to_startup_config",
                method="PUT",
                url="/api/v1/file/save-config",
                category="file_configuration_management",
                module="file",
                body=self.test_data.get('file_save_config', {
                    "startupFileName": "startup_backup.cfg"
                }),
                description="保存運行配置到啟動配置"
            ),
            
            # 保存配置到默認啟動文件
            self.create_test_case(
                name="file_save_config_to_default_startup",
                method="PUT",
                url="/api/v1/file/save-config",
                category="file_configuration_management",
                module="file",
                body=self.test_data.get('file_save_config_default', {
                    "startupFileName": "startup.cfg"
                }),
                description="保存配置到默認啟動文件"
            ),
            
            # 保存配置到自定義文件名
            self.create_test_case(
                name="file_save_config_to_custom_filename",
                method="PUT",
                url="/api/v1/file/save-config",
                category="file_configuration_management",
                module="file",
                body=self.test_data.get('file_save_config_custom', {
                    "startupFileName": "config_" + self.get_timestamp() + ".cfg"
                }),
                description="保存配置到自定義文件名"
            ),
            
            # 驗證配置保存結果
            self.create_test_case(
                name="file_verify_config_save_result",
                method="GET",
                url="/api/v1/file?fileType=config",
                category="file_configuration_management",
                module="file",
                description="驗證配置保存結果"
            )
        ]
    
    def get_file_boot_management_tests(self) -> List[APITestCase]:
        """File Boot Management API 測試案例"""
        return [
            # 獲取啟動文件信息
            self.create_test_case(
                name="file_get_boot_files_info",
                method="GET",
                url="/api/v1/file/boot",
                category="file_boot_management",
                module="file",
                description="獲取啟動文件信息"
            ),
            
            # 獲取指定單元啟動文件信息
            self.create_test_case(
                name="file_get_unit_boot_files_info",
                method="GET",
                url="/api/v1/file/boot?unitId=1",
                category="file_boot_management",
                module="file",
                description="獲取指定單元啟動文件信息"
            ),
            
            # 設置啟動配置文件
            self.create_test_case(
                name="file_set_startup_config_file",
                method="PUT",
                url="/api/v1/file/boot",
                category="file_boot_management",
                module="file",
                body=self.test_data.get('file_set_startup_config', {
                    "fileType": "config",
                    "fileName": "startup1.cfg"
                }),
                description="設置啟動配置文件"
            ),
            
            # 設置啟動操作碼文件
            self.create_test_case(
                name="file_set_startup_opcode_file",
                method="PUT",
                url="/api/v1/file/boot",
                category="file_boot_management",
                module="file",
                body=self.test_data.get('file_set_startup_opcode', {
                    "fileType": "opcode",
                    "fileName": "AS3000_52P_V08.27.10.06.bix"
                }),
                description="設置啟動操作碼文件"
            ),
            
            # 設置指定單元啟動文件
            self.create_test_case(
                name="file_set_unit_startup_file",
                method="PUT",
                url="/api/v1/file/boot",
                category="file_boot_management",
                module="file",
                body=self.test_data.get('file_set_unit_startup', {
                    "unitId": 1,
                    "fileType": "config",
                    "fileName": "unit1_startup.cfg"
                }),
                description="設置指定單元啟動文件"
            ),
            
            # 驗證啟動文件設置結果
            self.create_test_case(
                name="file_verify_boot_file_setting",
                method="GET",
                url="/api/v1/file/boot",
                category="file_boot_management",
                module="file",
                description="驗證啟動文件設置結果"
            )
        ]
    
    def get_file_auto_upgrade_management_tests(self) -> List[APITestCase]:
        """File Auto Upgrade Management API 測試案例"""
        return [
            # 獲取自動升級信息
            self.create_test_case(
                name="file_get_auto_upgrade_info",
                method="GET",
                url="/api/v1/file/auto-upgrade",
                category="file_auto_upgrade_management",
                module="file",
                description="獲取自動升級信息"
            ),
            
            # 啟用自動升級功能
            self.create_test_case(
                name="file_enable_auto_upgrade",
                method="PUT",
                url="/api/v1/file/auto-upgrade",
                category="file_auto_upgrade_management",
                module="file",
                body=self.test_data.get('file_enable_auto_upgrade', {
                    "opcodeStatus": True,
                    "opcodeDirUrl": "tftp://192.168.1.175/firmware/",
                    "reloadStatus": True
                }),
                description="啟用自動升級功能"
            ),
            
            # 配置FTP自動升級
            self.create_test_case(
                name="file_configure_ftp_auto_upgrade",
                method="PUT",
                url="/api/v1/file/auto-upgrade",
                category="file_auto_upgrade_management",
                module="file",
                body=self.test_data.get('file_ftp_auto_upgrade', {
                    "opcodeStatus": True,
                    "opcodeDirUrl": "ftp://admin:password@192.168.1.100/firmware/",
                    "reloadStatus": False
                }),
                description="配置FTP自動升級"
            ),
            
            # 禁用自動升級功能
            self.create_test_case(
                name="file_disable_auto_upgrade",
                method="PUT",
                url="/api/v1/file/auto-upgrade",
                category="file_auto_upgrade_management",
                module="file",
                body=self.test_data.get('file_disable_auto_upgrade', {
                    "opcodeStatus": False,
                    "reloadStatus": False
                }),
                description="禁用自動升級功能"
            ),
            
            # 配置自動重載設置
            self.create_test_case(
                name="file_configure_auto_reload",
                method="PUT",
                url="/api/v1/file/auto-upgrade",
                category="file_auto_upgrade_management",
                module="file",
                body=self.test_data.get('file_auto_reload_config', {
                    "opcodeStatus": True,
                    "opcodeDirUrl": "tftp://192.168.1.175/updates/",
                    "reloadStatus": True
                }),
                description="配置自動重載設置"
            ),
            
            # 驗證自動升級配置
            self.create_test_case(
                name="file_verify_auto_upgrade_configuration",
                method="GET",
                url="/api/v1/file/auto-upgrade",
                category="file_auto_upgrade_management",
                module="file",
                description="驗證自動升級配置"
            )
        ]
    
    def get_file_advanced_operations_tests(self) -> List[APITestCase]:
        """File Advanced Operations API 測試案例"""
        return [
            # 批量文件複製操作
            self.create_test_case(
                name="file_batch_copy_operations",
                method="POST",
                url="/api/v1/file/copy",
                category="file_advanced_operations",
                module="file",
                body=self.test_data.get('file_batch_copy_1', {
                    "srcOperType": "file",
                    "destOperType": "file",
                    "fileType": "config",
                    "srcFileName": "startup1.cfg",
                    "destFileName": "batch_backup_1.cfg"
                }),
                description="批量文件複製操作 - 第一個文件"
            ),
            
            # 批量文件複製操作 - 第二個文件
            self.create_test_case(
                name="file_batch_copy_operations_2",
                method="POST",
                url="/api/v1/file/copy",
                category="file_advanced_operations",
                module="file",
                body=self.test_data.get('file_batch_copy_2', {
                    "srcOperType": "file",
                    "destOperType": "file",
                    "fileType": "config",
                    "srcFileName": "Factory_Default_Config.cfg",
                    "destFileName": "batch_backup_2.cfg"
                }),
                description="批量文件複製操作 - 第二個文件"
            ),
            
            # 跨協議文件傳輸
            self.create_test_case(
                name="file_cross_protocol_transfer",
                method="POST",
                url="/api/v1/file/copy",
                category="file_advanced_operations",
                module="file",
                body=self.test_data.get('file_cross_protocol_transfer', {
                    "srcOperType": "tftp",
                    "destOperType": "ftp",
                    "fileType": "opcode",
                    "serverIp": "192.168.1.175",
                    "srcFileName": "source.bix",
                    "destFileName": "destination.bix",
                    "username": "ftpuser",
                    "password": "ftppass"
                }),
                description="跨協議文件傳輸 (TFTP到FTP)"
            ),
            
            # 多單元文件同步
            self.create_test_case(
                name="file_multi_unit_sync",
                method="POST",
                url="/api/v1/file/copy",
                category="file_advanced_operations",
                module="file",
                body=self.test_data.get('file_multi_unit_sync', {
                    "srcOperType": "file",
                    "destOperType": "unit",
                    "fileType": "config",
                    "srcFileName": "master_config.cfg",
                    "unitId": 2,
                    "destFileName": "synced_config.cfg"
                }),
                description="多單元文件同步"
            ),
            
            # 配置備份和恢復流程
            self.create_test_case(
                name="file_backup_and_restore_workflow",
                method="POST",
                url="/api/v1/file/copy",
                category="file_advanced_operations",
                module="file",
                body=self.test_data.get('file_backup_workflow', {
                    "srcOperType": "running-config",
                    "destOperType": "tftp",
                    "serverIp": "192.168.1.175",
                    "destFileName": "backup_" + self.get_timestamp() + ".cfg"
                }),
                description="配置備份和恢復流程"
            ),
            
            # 固件升級流程
            self.create_test_case(
                name="file_firmware_upgrade_workflow",
                method="POST",
                url="/api/v1/file/copy",
                category="file_advanced_operations",
                module="file",
                body=self.test_data.get('file_firmware_upgrade', {
                    "srcOperType": "tftp",
                    "destOperType": "file",
                    "fileType": "opcode",
                    "serverIp": "192.168.1.175",
                    "srcFileName": "latest_firmware.bix",
                    "destFileName": "upgrade_firmware.bix"
                }),
                description="固件升級流程"
            ),
            
            # 驗證高級操作結果
            self.create_test_case(
                name="file_verify_advanced_operations_results",
                method="GET",
                url="/api/v1/file",
                category="file_advanced_operations",
                module="file",
                description="驗證高級操作結果"
            )
        ]
    
    def get_file_error_handling_tests(self) -> List[APITestCase]:
        """File Error Handling API 測試案例"""
        return [
            # 測試刪除不存在的文件
            self.create_test_case(
                name="file_test_delete_nonexistent_file",
                method="DELETE",
                url="/api/v1/file/nonexistent.cfg/file-type/config",
                category="file_error_handling",
                module="file",
                body={"unitId": 1},
                expected_status=500,
                description="測試刪除不存在的文件"
            ),
            
            # 測試刪除啟動文件
            self.create_test_case(
                name="file_test_delete_startup_file",
                method="DELETE",
                url="/api/v1/file/startup.cfg/file-type/config",
                category="file_error_handling",
                module="file",
                body={"unitId": 1},
                expected_status=500,
                description="測試刪除啟動文件 (應該被拒絕)"
            ),
            
            # 測試刪除出廠默認配置文件
            self.create_test_case(
                name="file_test_delete_factory_default_config",
                method="DELETE",
                url="/api/v1/file/Factory_Default_Config.cfg/file-type/config",
                category="file_error_handling",
                module="file",
                body={"unitId": 1},
                expected_status=500,
                description="測試刪除出廠默認配置文件 (應該被拒絕)"
            ),
            
            # 測試無效的文件複製源類型
            self.create_test_case(
                name="file_test_invalid_copy_source_type",
                method="POST",
                url="/api/v1/file/copy",
                category="file_error_handling",
                module="file",
                body=self.test_data.get('file_invalid_source_type', {
                    "srcOperType": "invalid_source",
                    "destOperType": "file",
                    "fileType": "config",
                    "srcFileName": "test.cfg",
                    "destFileName": "dest.cfg"
                }),
                expected_status=400,
                description="測試無效的文件複製源類型"
            ),
            
            # 測試無效的文件複製目標類型
            self.create_test_case(
                name="file_test_invalid_copy_destination_type",
                method="POST",
                url="/api/v1/file/copy",
                category="file_error_handling",
                module="file",
                body=self.test_data.get('file_invalid_dest_type', {
                    "srcOperType": "file",
                    "destOperType": "invalid_destination",
                    "fileType": "config",
                    "srcFileName": "test.cfg",
                    "destFileName": "dest.cfg"
                }),
                expected_status=400,
                description="測試無效的文件複製目標類型"
            ),
            
            # 測試缺少必需參數的文件複製
            self.create_test_case(
                name="file_test_copy_missing_required_params",
                method="POST",
                url="/api/v1/file/copy",
                category="file_error_handling",
                module="file",
                body=self.test_data.get('file_copy_missing_params', {
                    "srcOperType": "file",
                    "destOperType": "tftp"
                    # 缺少 serverIp, srcFileName, destFileName, fileType
                }),
                expected_status=400,
                description="測試缺少必需參數的文件複製"
            ),
            
            # 測試無效的服務器IP地址
            self.create_test_case(
                name="file_test_invalid_server_ip",
                method="POST",
                url="/api/v1/file/copy",
                category="file_error_handling",
                module="file",
                body=self.test_data.get('file_invalid_server_ip', {
                    "srcOperType": "file",
                    "destOperType": "tftp",
                    "fileType": "config",
                    "serverIp": "invalid.ip.address",
                    "srcFileName": "test.cfg",
                    "destFileName": "dest.cfg"
                }),
                expected_status=500,
                description="測試無效的服務器IP地址"
            ),
            
            # 測試無效的單元ID
            self.create_test_case(
                name="file_test_invalid_unit_id",
                method="POST",
                url="/api/v1/file/copy",
                category="file_error_handling",
                module="file",
                body=self.test_data.get('file_invalid_unit_id', {
                    "srcOperType": "file",
                    "destOperType": "unit",
                    "fileType": "config",
                    "srcFileName": "test.cfg",
                    "unitId": 99,  # 超出範圍 (1-8)
                    "destFileName": "dest.cfg"
                }),
                expected_status=400,
                description="測試無效的單元ID (超出範圍1-8)"
            ),
            
            # 測試無效的文件類型
            self.create_test_case(
                name="file_test_invalid_file_type",
                method="POST",
                url="/api/v1/file/copy",
                category="file_error_handling",
                module="file",
                body=self.test_data.get('file_invalid_file_type', {
                    "srcOperType": "file",
                    "destOperType": "file",
                    "fileType": "invalid_type",
                    "srcFileName": "test.cfg",
                    "destFileName": "dest.cfg"
                }),
                expected_status=400,
                description="測試無效的文件類型"
            ),
            
            # 測試無效JSON格式
            self.create_test_case(
                name="file_test_invalid_json_format",
                method="POST",
                url="/api/v1/file/copy",
                category="file_error_handling",
                module="file",
                body="invalid json format",
                expected_status=400,
                description="測試無效JSON格式"
            ),
            
            # 測試設置不存在的啟動文件
            self.create_test_case(
                name="file_test_set_nonexistent_boot_file",
                method="PUT",
                url="/api/v1/file/boot",
                category="file_error_handling",
                module="file",
                body=self.test_data.get('file_nonexistent_boot_file', {
                    "fileType": "config",
                    "fileName": "nonexistent.cfg"
                }),
                expected_status=500,
                description="測試設置不存在的啟動文件"
            ),
            
            # 測試無效的自動升級URL
            self.create_test_case(
                name="file_test_invalid_auto_upgrade_url",
                method="PUT",
                url="/api/v1/file/auto-upgrade",
                category="file_error_handling",
                module="file",
                body=self.test_data.get('file_invalid_upgrade_url', {
                    "opcodeStatus": True,
                    "opcodeDirUrl": "invalid://invalid.url/path/",
                    "reloadStatus": True
                }),
                expected_status=400,
                description="測試無效的自動升級URL"
            ),
            
            # 恢復正常文件配置
            self.create_test_case(
                name="file_restore_normal_configuration",
                method="GET",
                url="/api/v1/file",
                category="file_error_handling",
                module="file",
                description="恢復正常文件配置"
            ),
            
            # 最終文件狀態檢查
            self.create_test_case(
                name="file_final_status_check",
                method="GET",
                url="/api/v1/file",
                category="file_error_handling",
                module="file",
                description="最終文件狀態檢查"
            )
        ]
    
    def get_timestamp(self) -> str:
        """獲取時間戳字符串"""
        import datetime
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")