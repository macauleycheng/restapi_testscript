#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
網路設備 REST API 統一測試框架
支援模組化管理的完整測試架構
"""

import json
import requests
import argparse
import sys
import os
import time
import importlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging
from urllib.parse import quote

from modules.aaa_tests import AAATests
from modules.dot1x_tests import DOT1XTests
from modules.loopback_detection_tests import LOOPBACK_DETECTIONTests
from modules.mac_tests import MACTests
from modules.ssh_tests import SSHTests
from modules.acl_tests import ACLTests
from modules.dhcp_tests import DHCPTests
from modules.lldp_tests import LLDPTests
from modules.link_aggregation_tests import LINK_AGGREGATIONTests
from modules.ntp_tests import NTPTests
from modules.poe_tests import POETests
from modules.snmp_tests import SNMPTests
from modules.static_route_tests import STATIC_ROUTETests
from modules.storm_control_tests import STORM_CONTROLTests
from modules.telnet_tests import TELNETTests
from modules.vlan_tests import VLANTests
from modules.ddm_tests import DDMTests
from modules.excluded_vlan_tests import EXCLUDED_VLANTests
from modules.arp_tests import ARPTests
from modules.bfd_tests import BFDTests
from modules.cluster_tests import CLUSTERTests
from modules.cos_tests import COSTests
from modules.device_tests import DEVICETests
from modules.dns_tests import DNSTests
from modules.dos_protection_tests import DOS_PROTECTIONTests
from modules.file_tests import FILETests
from modules.igmpsnoop_tests import IGMPSNOOPTests
from modules.interface_tests import INTERFACETests
from modules.ip_arp_inspection_tests import IP_ARP_INSPECTIONTests
from modules.ip_interface_tests import IP_INTERFACETests
from modules.ip_source_guard_tests import IP_SOURCE_GUARDTests
from modules.ipv6_interface_tests import IPV6_INTERFACETests
from modules.mgmt_ip_filter_tests import MGMT_IP_FILTERTests
from modules.nd_snoop_tests import ND_SNOOPTests
from modules.ipv6_nd_tests import IPV6_NDTests




class TestResult(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"

@dataclass
class APITestCase:
    name: str
    method: str
    url: str
    headers: Dict[str, str]
    params: Optional[Dict[str, Any]] = None
    body: Optional[Dict[str, Any]] = None
    expected_status: int = 200
    description: str = ""
    dependencies: List[str] = None
    category: str = "general"
    module: str = "general"

@dataclass
class TestReport:
    test_name: str
    result: TestResult
    status_code: int
    response_time: float
    error_message: str = ""
    response_data: Any = None
    category: str = "general"
    module: str = "general"
    url: str = ""
    body: Dict[str, Any] = None

class NetworkAPITester:
    def __init__(self, config_file: str = "network_config.json"):
        self.config = self.load_config(config_file)
        self.session = requests.Session()
        self.test_results: List[TestReport] = []
        self.modules = {}
        self.setup_logging()
        self.setup_authentication()
        self.load_modules()
        
    def setup_logging(self):
        """設置日誌記錄"""
        log_level = getattr(logging, self.config.get('log_level', 'INFO').upper())
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('network_api_test.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_authentication(self):
        """設置認證"""
        auth_config = self.config.get('authentication', {})
        if auth_config.get('type') == 'basic':
            self.session.auth = (auth_config['username'], auth_config['password'])
        elif auth_config.get('type') == 'token':
            self.session.headers.update({'Authorization': f"Bearer {auth_config['token']}"})

    def load_config(self, config_file: str) -> Dict:
        """載入配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"配置文件 {config_file} 不存在，使用預設配置")
            return self.get_default_config()
        except json.JSONDecodeError as e:
            print(f"配置文件格式錯誤: {e}，使用預設配置")
            return self.get_default_config()

    def get_default_config(self) -> Dict:
        """獲取預設配置"""
        return {
            "switch": {
                "protocol": "http",
                "host": "192.168.1.100",
                "port": 80
            },
            "authentication": {
                "type": "basic",
                "username": "admin",
                "password": "admin"
            },
            "default_headers": {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            "timeout": 30,
            "log_level": "INFO",
            "modules": ["dhcp", "vlan", "storm_control"]
        }

    # 在 get_test_modules 函數中添加
    def get_test_modules(self):
        """獲取所有測試模組"""
        return {
            'dhcp': DHCPTests,
            'vlan': VLANTests,
            'storm_control': STORM_CONTROLTests,
            'acl': ACLTests,
            'lldp': LLDPTests,
            'link_aggregation': LINK_AGGREGATIONTests,
            'ntp': NTPTests,
            'poe': POETests,
            'snmp': SNMPTests,
            'ssh': SSHTests,
            'static_route': STATIC_ROUTETests,
            'loopback_detection': LOOPBACK_DETECTIONTests,
            'mac': MACTests,
            'telnet': TELNETTests,
            'dot1x': DOT1XTests,
            'aaa': AAATests,
            'ddm': DDMTests,
            'excluded_vlan': EXCLUDED_VLANTests,
            'arp': ARPTests,
            'bfd': BFDTests,
            'cluster': CLUSTERTests,
            'cos': COSTests,
            'device': DEVICETests,
            'dns': DNSTests,
            'dos_protection': DOS_PROTECTIONTests,
            'file': FILETests,
            'igmpsnoop': IGMPSNOOPTests,
            'interface': INTERFACETests,
            'ip_arp_inspection': IP_ARP_INSPECTIONTests,
            'ip_interface': IP_INTERFACETests,
            'ip_source_guard': IP_SOURCE_GUARDTests,
            'ipv6_interface': IPV6_INTERFACETests,
            'mgmt_ip_filter': MGMT_IP_FILTERTests,
            'nd_snoop': ND_SNOOPTests,
            'ipv6_nd': IPV6_NDTests,
        }

    def load_modules(self):
        """動態載入測試模組"""
        #module_names = self.config.get('modules', ['dhcp', 'vlan', 'storm_control'])
        module_names = list(self.get_test_modules().keys())
        for module_name in module_names:
            try:
                module_file = f"modules/{module_name}_tests.py"
                if os.path.exists(module_file):
                    #print(f"載入模組文件: {module_file}")
                    #print(f"模組名稱: {module_name}")
                    spec = importlib.util.spec_from_file_location(f"{module_name}_tests", module_file)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # 獲取模組的測試類
                    class_name = f"{module_name.upper()}Tests"
                    if hasattr(module, class_name):
                        test_class = getattr(module, class_name)
                        self.modules[module_name] = test_class(self.config)
                        self.logger.info(f"成功載入模組: {module_name}")
                    else:
                        self.logger.warning(f"模組 {module_name} 中找不到類 {class_name}")
                else:
                    self.logger.warning(f"模組文件不存在: {module_file}")
            except Exception as e:
                self.logger.error(f"載入模組 {module_name} 失敗: {e}")

    def get_base_url(self) -> str:
        """獲取基礎URL"""
        switch_config = self.config['switch']
        protocol = switch_config.get('protocol', 'http')
        host = switch_config['host']
        port = switch_config.get('port', 80)
        return f"{protocol}://{host}:{port}"

    def replace_url_params(self, url: str, params: Dict[str, Any]) -> str:
        """替換URL中的參數"""
        if not params:
            return url
        
        for key, value in params.items():
            placeholder = f"{{{key}}}"
            if placeholder in url:
                # URL編碼特殊字符，特別處理MAC地址和接口ID
                if any(keyword in key.lower() for keyword in ['mac', 'ifid', 'id', 'interface']):
                    encoded_value = quote(str(value), safe='')
                else:
                    encoded_value = str(value)
                url = url.replace(placeholder, encoded_value)
        return url

    def execute_test_case(self, test_case: APITestCase) -> TestReport:
        """執行單個測試案例"""
        start_time = time.time()
        
        try:
            # 構建完整URL
            full_url = self.get_base_url() + test_case.url
            
            # 替換URL中的參數
            if test_case.params:
                full_url = self.replace_url_params(full_url, test_case.params)
            
            # 設置請求頭
            headers = {**self.config.get('default_headers', {}), **test_case.headers}
            
            # 執行HTTP請求
            response = self.session.request(
                method=test_case.method,
                url=full_url,
                headers=headers,
                json=test_case.body,
                timeout=self.config.get('timeout', 30)
            )
            
            response_time = time.time() - start_time
            
            # 判斷測試結果
            if response.status_code == test_case.expected_status:
                result = TestResult.PASS
                error_message = ""
            else:
                result = TestResult.FAIL
                error_message = f"期望狀態碼 {test_case.expected_status}, 實際 {response.status_code}"
            
            # 嘗試解析響應JSON
            try:
                response_data = response.json() if response.content else None
            except:
                response_data = response.text if response.content else None
            
            return TestReport(
                test_name=test_case.name,
                result=result,
                status_code=response.status_code,
                response_time=response_time,
                error_message=error_message,
                response_data=response_data,
                category=test_case.category,
                module=test_case.module,
                url=full_url,
                body=test_case.body
            )
            
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            return TestReport(
                test_name=test_case.name,
                result=TestResult.FAIL,
                status_code=0,
                response_time=response_time,
                error_message=f"請求異常: {str(e)}",
                category=test_case.category,
                module=test_case.module
            )

    def get_all_test_cases(self) -> List[APITestCase]:
        """獲取所有測試案例"""
        all_tests = []
        
        for module_name, module_instance in self.modules.items():
            try:
                module_tests = module_instance.get_all_tests()
                all_tests.extend(module_tests)
                self.logger.debug(f"從模組 {module_name} 載入了 {len(module_tests)} 個測試案例")
            except Exception as e:
                self.logger.error(f"從模組 {module_name} 獲取測試案例失敗: {e}")
        
        return all_tests

    def get_available_modules(self) -> List[str]:
        """獲取可用的模組列表"""
        return list(self.modules.keys())

    def get_available_categories(self) -> Dict[str, List[str]]:
        """獲取可用的類別列表"""
        categories = {}
        for module_name, module_instance in self.modules.items():
            try:
                module_categories = module_instance.get_categories()
                categories[module_name] = module_categories
            except Exception as e:
                self.logger.error(f"從模組 {module_name} 獲取類別失敗: {e}")
                categories[module_name] = []
        return categories

    def run_tests(self, modules: List[str] = None, categories: List[str] = None, specific_tests: List[str] = None):
        """運行測試"""
        all_test_cases = self.get_all_test_cases()
        
        # 過濾測試案例
        if modules:
            all_test_cases = [tc for tc in all_test_cases if tc.module in modules]
        
        if categories:
            all_test_cases = [tc for tc in all_test_cases if tc.category in categories]
        
        if specific_tests:
            all_test_cases = [tc for tc in all_test_cases if tc.name in specific_tests]
        
        self.logger.info(f"開始執行 {len(all_test_cases)} 個測試案例")
        
        # 按模組和類別分組執行測試
        modules_dict = {}
        for test_case in all_test_cases:
            if test_case.module not in modules_dict:
                modules_dict[test_case.module] = {}
            if test_case.category not in modules_dict[test_case.module]:
                modules_dict[test_case.module][test_case.category] = []
            modules_dict[test_case.module][test_case.category].append(test_case)
        
        # 執行測試
        for module, categories_dict in modules_dict.items():
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"執行 {module.upper()} 模組測試")
            self.logger.info(f"{'='*60}")
            
            for category, test_cases in categories_dict.items():
                self.logger.info(f"\n--- {category.upper()} 測試 ---")
                
                for test_case in test_cases:
                    self.logger.info(f"執行測試: {test_case.name}")
                    result = self.execute_test_case(test_case)
                    self.test_results.append(result)
                    
                    # 輸出測試結果
                    status_icon = "V" if result.result == TestResult.PASS else "X"
                    self.logger.info(
                        f"{status_icon} {result.test_name}: {result.result.value} "
                        f"({result.status_code}, {result.response_time:.2f}s)"
                    )
                    
                    if result.error_message:
                        self.logger.error(f"  錯誤: {result.error_message}")
                    
                    # 添加延遲避免請求過於頻繁
                    time.sleep(self.config.get('request_delay', 0.1))

    def generate_report(self, output_file: str = "network_test_report.json"):
        """生成測試報告"""
        # 按模組和類別統計
        module_stats = {}
        category_stats = {}
        
        for result in self.test_results:
            # 模組統計
            if result.module not in module_stats:
                module_stats[result.module] = {"total": 0, "passed": 0, "failed": 0, "skipped": 0}
            
            module_stats[result.module]["total"] += 1
            if result.result == TestResult.PASS:
                module_stats[result.module]["passed"] += 1
            elif result.result == TestResult.FAIL:
                module_stats[result.module]["failed"] += 1
            else:
                module_stats[result.module]["skipped"] += 1
            
            # 類別統計
            if result.category not in category_stats:
                category_stats[result.category] = {"total": 0, "passed": 0, "failed": 0, "skipped": 0}
            
            category_stats[result.category]["total"] += 1
            if result.result == TestResult.PASS:
                category_stats[result.category]["passed"] += 1
            elif result.result == TestResult.FAIL:
                category_stats[result.category]["failed"] += 1
            else:
                category_stats[result.category]["skipped"] += 1
        
        report_data = {
            "summary": {
                "total": len(self.test_results),
                "passed": len([r for r in self.test_results if r.result == TestResult.PASS]),
                "failed": len([r for r in self.test_results if r.result == TestResult.FAIL]),
                "skipped": len([r for r in self.test_results if r.result == TestResult.SKIP]),
                "modules": module_stats,
                "categories": category_stats
            },
            "results": [
                {
                    "test_name": r.test_name,
                    "module": r.module,
                    "category": r.category,
                    "test_url": r.url,
                    "test_body": r.body,
                    "result": r.result.value,
                    "status_code": r.status_code,
                    "response_time": r.response_time,
                    "error_message": r.error_message,
                    "response_data": r.response_data
                }
                for r in self.test_results
            ]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"測試報告已生成: {output_file}")
        return report_data

def main():
    parser = argparse.ArgumentParser(description='網路設備 REST API 統一測試框架')
    parser.add_argument('--config', '-c', default='network_config.json', help='配置文件路徑')
    parser.add_argument('--modules', '-m', nargs='+', help='指定要測試的模組')
    parser.add_argument('--categories', '-cat', nargs='+', help='指定要測試的API類別')
    parser.add_argument('--tests', '-t', nargs='+', help='指定要執行的測試案例')
    parser.add_argument('--output', '-o', default='network_test_report.json', help='測試報告輸出文件')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有可用的測試案例')
    parser.add_argument('--list-modules', action='store_true', help='列出所有可用的模組')
    parser.add_argument('--list-categories', action='store_true', help='列出所有可用的類別')
    
    args = parser.parse_args()
    
    # 創建測試器實例
    tester = NetworkAPITester(args.config)
    
    # 列出模組
    if args.list_modules:
        modules = tester.get_available_modules()
        print("可用的模組數量:" + str(len(modules)))
        print("可用的模組:")
        for module in modules:
            all_tests = tester.get_all_test_cases()
            count = len([t for t in all_tests if t.module == module])
            print(f"  {module}: {count} 個測試案例")
        return
    
    # 列出類別
    if args.list_categories:
        categories = tester.get_available_categories()
        print("可用的類別:")
        for module, cats in categories.items():
            print(f"\n{module.upper()} 模組:")
            for category in cats:
                all_tests = tester.get_all_test_cases()
                count = len([t for t in all_tests if t.category == category])
                print(f"  {category}: {count} 個測試案例")
        return
    
    # 列出測試案例
    if args.list:
        all_tests = tester.get_all_test_cases()
        print("可用的測試案例:")
        current_module = None
        current_category = None
        
        for test in sorted(all_tests, key=lambda x: (x.module, x.category, x.name)):
            if test.module != current_module:
                print(f"\n{'='*50}")
                print(f"{test.module.upper()} 模組")
                print(f"{'='*50}")
                current_module = test.module
                current_category = None
            
            if test.category != current_category:
                print(f"\n--- {test.category.upper()} ---")
                current_category = test.category
            
            print(f"  {test.name}: {test.description}")
        return
    
    # 運行測試
    tester.run_tests(args.modules, args.categories, args.tests)
    
    # 生成報告
    report = tester.generate_report(args.output)
    
    # 輸出摘要
    summary = report['summary']
    print(f"\n{'='*60}")
    print(f"測試摘要:")
    print(f"總計: {summary['total']}")
    print(f"通過: {summary['passed']}")
    print(f"失敗: {summary['failed']}")
    print(f"跳過: {summary['skipped']}")
    
    print(f"\n按模組統計:")
    for module, stats in summary['modules'].items():
        print(f"  {module.upper()}: {stats['passed']}/{stats['total']} 通過")
    
    print(f"\n按類別統計:")
    for category, stats in summary['categories'].items():
        print(f"  {category}: {stats['passed']}/{stats['total']} 通過")
    
    # 返回適當的退出碼
    sys.exit(0 if summary['failed'] == 0 else 1)

if __name__ == "__main__":
    main()