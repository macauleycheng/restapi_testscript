#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
User Privilege REST API 測試腳本
測試所有用戶權限相關的 API 端點
"""

import getpass
import hashlib

import requests
import json
import sys
from typing import Dict, Any

class UserPrivilegeAPITester:
    def __init__(self, base_url: str = "http://localhost", username: str = None, password: str = None):
        """
        初始化測試器
        
        Args:
            base_url: API 基礎 URL
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password        
        self.session = requests.Session()
        self.test_results = []
        # 設定認證
        self._setup_authentication()
        
    def _setup_authentication(self):
        """設定認證方式"""
        if self.username and self.password:
            # 使用 HTTP Basic Authentication
            self.session.auth = (self.username, self.password)
            print(f"✅ 已設定 HTTP Basic 認證 (使用者: {self.username})")
            
            # 也可以設定 headers 方式的認證
            # import base64
            # credentials = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
            # self.session.headers.update({'Authorization': f'Basic {credentials}'})
            

    def log_test(self, test_name: str, success: bool, response: requests.Response = None, error: str = None):
        """記錄測試結果"""
        result = {
            'test_name': test_name,
            'success': success,
            'status_code': response.status_code if response else None,
            'error': error
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if response:
            print(f"    狀態碼: {response.status_code}")
        if error:
            print(f"    錯誤: {error}")
        print()

    def test_get_all_privileged_passwords(self):
        """測試 1.1: 獲取所有特權密碼"""
        try:
            url = f"{self.base_url}/api/v1/users/password"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                print(f"    返回的密碼數量: {len(data.get('result', {}).get('passwords', []))}")
                
            self.log_test("獲取所有特權密碼", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取所有特權密碼", False, error=str(e))
            return None

    def test_add_privileged_password(self):
        """測試 1.2: 添加特權密碼"""
        try:
            url = f"{self.base_url}/api/v1/users/password"
            payload = {
                "encryptedType": 0,
                "password": "test123",
                "privilege": 14
            }
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            self.log_test("添加特權密碼 (privilege 14)", success, response)
            return success
            
        except Exception as e:
            self.log_test("添加特權密碼 (privilege 14)", False, error=str(e))
            return False

    def test_get_specific_privileged_password(self, privilege: int = 15):
        """測試 1.3: 獲取特定特權密碼"""
        try:
            url = f"{self.base_url}/api/v1/users/password/privilege/{privilege}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                print(f"    特權等級: {data.get('result', {}).get('privilege')}")
                
            self.log_test(f"獲取特權密碼 (privilege {privilege})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取特權密碼 (privilege {privilege})", False, error=str(e))
            return None

    def test_update_privileged_password(self, privilege: int = 15):
        """測試 1.4: 更新特權密碼"""
        try:
            url = f"{self.base_url}/api/v1/users/password/privilege/{privilege}"
            payload = {
                "encryptedType": 0,
                "password": "newpass123"
            }
            
            response = self.session.put(url, json=payload)
            success = response.status_code == 200
            
            self.log_test(f"更新特權密碼 (privilege {privilege})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"更新特權密碼 (privilege {privilege})", False, error=str(e))
            return False

    def test_delete_privileged_password(self, privilege: int = 14):
        """測試 1.5: 刪除特權密碼"""
        try:
            url = f"{self.base_url}/api/v1/users/password/privilege/{privilege}"
            response = self.session.delete(url)
            
            success = response.status_code == 200
            
            self.log_test(f"刪除特權密碼 (privilege {privilege})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"刪除特權密碼 (privilege {privilege})", False, error=str(e))
            return False

    def test_get_all_usernames(self):
        """測試 1.6: 獲取所有用戶名"""
        try:
            url = f"{self.base_url}/api/v1/users/usernames"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                users = data.get('result', {}).get('userAuths', [])
                print(f"    用戶數量: {len(users)}")
                for user in users:
                    print(f"    - {user.get('username')} (type: {user.get('type')}, privilege: {user.get('privilege')})")
                
            self.log_test("獲取所有用戶名", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("獲取所有用戶名", False, error=str(e))
            return None

    def test_add_username_access_level(self):
        """測試 1.7a: 添加用戶名 (access-level 類型)"""
        try:
            url = f"{self.base_url}/api/v1/users/usernames"
            payload = {
                "username": "testuser1",
                "type": "access-level",
                "privilege": 10
            }
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            self.log_test("添加用戶名 (access-level)", success, response)
            return success
            
        except Exception as e:
            self.log_test("添加用戶名 (access-level)", False, error=str(e))
            return False

    def test_add_username_no_password(self):
        """測試 1.7b: 添加用戶名 (no-password 類型)"""
        try:
            url = f"{self.base_url}/api/v1/users/usernames"
            payload = {
                "username": "testuser2",
                "type": "no-password"
            }
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            self.log_test("添加用戶名 (no-password)", success, response)
            return success
            
        except Exception as e:
            self.log_test("添加用戶名 (no-password)", False, error=str(e))
            return False

    def test_add_username_with_password(self):
        """測試 1.7c: 添加用戶名 (password 類型)"""
        try:
            url = f"{self.base_url}/api/v1/users/usernames"
            payload = {
                "username": "testuser3",
                "type": "password",
                "encryptedType": 0,
                "password": "testpass123"
            }
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            self.log_test("添加用戶名 (password)", success, response)
            return success
            
        except Exception as e:
            self.log_test("添加用戶名 (password)", False, error=str(e))
            return False

    def test_get_specific_username(self, username: str = "testuser1"):
        """測試 1.8: 獲取特定用戶名"""
        try:
            url = f"{self.base_url}/api/v1/users/usernames/name/{username}"
            response = self.session.get(url)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                result = data.get('result', {})
                print(f"    用戶名: {result.get('username')}")
                print(f"    類型: {result.get('type')}")
                print(f"    特權等級: {result.get('privilege')}")
                
            self.log_test(f"獲取用戶名 ({username})", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test(f"獲取用戶名 ({username})", False, error=str(e))
            return None

    def test_delete_username(self, username: str = "testuser1"):
        """測試 1.9: 刪除用戶名"""
        try:
            url = f"{self.base_url}/api/v1/users/usernames/name/{username}"
            response = self.session.delete(url)
            
            success = response.status_code == 200
            
            self.log_test(f"刪除用戶名 ({username})", success, response)
            return success
            
        except Exception as e:
            self.log_test(f"刪除用戶名 ({username})", False, error=str(e))
            return False

    def test_generate_encrypted_key(self):
        """測試 1.10: 生成密碼加密密鑰"""
        try:
            url = f"{self.base_url}/api/v1/users/usernames/password/encrypted-key"
            payload = {
                "password": "testpassword123"
            }
            
            response = self.session.post(url, json=payload)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                key = data.get('result', {}).get('key')
                print(f"    生成的加密密鑰: {key}")
                
            self.log_test("生成密碼加密密鑰", success, response)
            return response.json() if success else None
            
        except Exception as e:
            self.log_test("生成密碼加密密鑰", False, error=str(e))
            return None

    def run_all_tests(self):
        """執行所有測試"""
        print("=" * 60)
        print("開始執行 User Privilege API 測試")
        print("=" * 60)
        
        # 1. 基本查詢測試
        print("\n📋 基本查詢測試")
        print("-" * 30)
        self.test_get_all_privileged_passwords()
        self.test_get_specific_privileged_password(15)
        self.test_get_all_usernames()
        
        # 2. 創建操作測試
        print("\n➕ 創建操作測試")
        print("-" * 30)
        self.test_add_privileged_password()
        self.test_add_username_access_level()
        self.test_add_username_no_password()
        self.test_add_username_with_password()
        
        # 3. 更新操作測試
        print("\n✏️ 更新操作測試")
        print("-" * 30)
        self.test_update_privileged_password(15)
        
        # 4. 查詢新創建的資源
        print("\n🔍 查詢新創建的資源")
        print("-" * 30)
        self.test_get_specific_username("testuser1")
        self.test_get_specific_username("testuser2")
        self.test_get_specific_username("testuser3")
        
        # 5. 工具功能測試
        print("\n🔧 工具功能測試")
        print("-" * 30)
        self.test_generate_encrypted_key()
        
        # 6. 刪除操作測試
        print("\n🗑️ 刪除操作測試")
        print("-" * 30)
        self.test_delete_username("testuser1")
        self.test_delete_username("testuser2")
        self.test_delete_username("testuser3")
        self.test_delete_privileged_password(14)
        
        # 7. 測試結果統計
        self.print_test_summary()

    def print_test_summary(self):
        """打印測試結果摘要"""
        print("\n" + "=" * 60)
        print("測試結果摘要")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"總測試數: {total_tests}")
        print(f"通過: {passed_tests} ✅")
        print(f"失敗: {failed_tests} ❌")
        print(f"成功率: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n失敗的測試:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test_name']}")
                    if result['error']:
                        print(f"    錯誤: {result['error']}")


def get_credentials():
    """取得使用者認證資訊"""
    print("\n🔐 認證設定")
    print("-" * 20)
    
    username = input("使用者名稱: ").strip()
    if username:
        password = getpass.getpass("密碼: ")
        m = hashlib.md5(password.encode('utf-8'))
        # Get the hash in a hexadecimal format
        password = m.hexdigest()
        return username, password
    else:
        print("未輸入使用者名稱，將使用無認證模式")
        return None, None
           

def main():
    """主函數"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = input("請輸入 API 基礎 URL (預設: http://localhost): ").strip()
        if not base_url:
            base_url = "http://localhost"
    
    print(f"使用 API 基礎 URL: {base_url}")
    # 獲取認證資訊
    username, password = get_credentials()

    # 創建測試器並執行測試
    tester = UserPrivilegeAPITester(base_url, username, password)
    tester.run_all_tests()

if __name__ == "__main__":
    main()