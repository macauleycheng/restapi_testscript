#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ACL 模組測試案例
包含IP ACL, MAC ACL, ARP ACL, IPv6 ACL, Interface Binding, TCAM Utilization相關API測試
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class ACLTests(BaseTests):
    """ACL 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取ACL模組支援的類別"""
        return [
            "ip_acl",
            "mac_acl", 
            "arp_acl",
            "ipv6_acl",
            "acl_interface",
            "tcam_utilization"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有ACL測試案例"""
        all_tests = []
        all_tests.extend(self.get_ip_acl_tests())
        all_tests.extend(self.get_mac_acl_tests())
        all_tests.extend(self.get_arp_acl_tests())
        all_tests.extend(self.get_ipv6_acl_tests())
        all_tests.extend(self.get_acl_interface_tests())
        all_tests.extend(self.get_tcam_utilization_tests())
        return all_tests
    
    def get_ip_acl_tests(self) -> List[APITestCase]:
        """IP ACL API 測試案例"""
        return [
            # 獲取所有IP ACL
            self.create_test_case(
                name="ip_acl_get_all",
                method="GET",
                url="/api/v1/acls/ip",
                category="ip_acl",
                module="acl",
                description="獲取所有IP ACL"
            ),
            
            # 創建標準IP ACL
            self.create_test_case(
                name="ip_acl_create_standard",
                method="POST",
                url="/api/v1/acls/ip",
                category="ip_acl",
                module="acl",
                body=self.test_data.get('ip_acl_standard', {
                    "name": "std_acl_1",
                    "type": "standard",
                    "aces": [
                        {
                            "access": "permit",
                            "sourceIpAddr": "192.168.1.10",
                            "sourceIpAddrBitmask": "255.255.255.255"
                        }
                    ]
                }),
                description="創建標準IP ACL"
            ),
            
            # 創建擴展IP ACL
            self.create_test_case(
                name="ip_acl_create_extended",
                method="POST",
                url="/api/v1/acls/ip",
                category="ip_acl",
                module="acl",
                body=self.test_data.get('ip_acl_extended', {
                    "name": "ext_acl_1",
                    "type": "extended",
                    "aces": [
                        {
                            "access": "permit",
                            "sourceIpAddr": "192.168.1.10",
                            "sourceIpAddrBitmask": "255.255.255.255",
                            "destIpAddr": "192.168.2.10",
                            "destIpAddrBitmask": "255.255.255.255",
                            "protocol": 6,
                            "dscp": 63,
                            "sourcePort": 100,
                            "sourcePortBitmask": 65535,
                            "destPort": 200,
                            "destPortBitmask": 65535,
                            "controlCode": 12,
                            "controlCodeBitmask": 12
                        }
                    ]
                }),
                description="創建擴展IP ACL"
            ),
            
            # 獲取特定IP ACL
            self.create_test_case(
                name="ip_acl_get_specific",
                method="GET",
                url="/api/v1/acls/ip/{aclName}",
                category="ip_acl",
                module="acl",
                params={"aclName": self.params.get('ip_acl_name', 'std_acl_1')},
                description=f"獲取IP ACL {self.params.get('ip_acl_name', 'std_acl_1')}"
            ),
            
            # 更新IP ACL
            self.create_test_case(
                name="ip_acl_update",
                method="PUT",
                url="/api/v1/acls/ip/{aclName}",
                category="ip_acl",
                module="acl",
                params={"aclName": self.params.get('ip_acl_name', 'std_acl_1')},
                body=self.test_data.get('ip_acl_update', {
                    "aces": [
                        {
                            "access": "permit",
                            "sourceIpAddr": "192.168.11.10",
                            "sourceIpAddrBitmask": "255.255.255.255"
                        }
                    ]
                }),
                description=f"更新IP ACL {self.params.get('ip_acl_name', 'std_acl_1')}"
            ),
            
            # 刪除IP ACL
            self.create_test_case(
                name="ip_acl_delete",
                method="DELETE",
                url="/api/v1/acls/ip/{aclName}",
                category="ip_acl",
                module="acl",
                params={"aclName": self.params.get('ip_acl_name_delete', 'test_acl')},
                description=f"刪除IP ACL {self.params.get('ip_acl_name_delete', 'test_acl')}"
            ),
            
            # 創建複雜擴展ACL (多個ACE)
            self.create_test_case(
                name="ip_acl_create_complex_extended",
                method="POST",
                url="/api/v1/acls/ip",
                category="ip_acl",
                module="acl",
                body=self.test_data.get('ip_acl_complex', {
                    "name": "complex_acl",
                    "type": "extended",
                    "aces": [
                        {
                            "access": "permit",
                            "sourceIpAddr": "192.168.1.0",
                            "sourceIpAddrBitmask": "255.255.255.0",
                            "destIpAddr": "10.0.0.0",
                            "destIpAddrBitmask": "255.0.0.0",
                            "protocol": 6,
                            "sourcePort": 80,
                            "sourcePortBitmask": 65535
                        },
                        {
                            "access": "deny",
                            "sourceIpAddr": "192.168.2.0",
                            "sourceIpAddrBitmask": "255.255.255.0",
                            "protocol": 17,
                            "destPort": 53,
                            "destPortBitmask": 65535
                        }
                    ]
                }),
                description="創建複雜擴展IP ACL (多個ACE)"
            ),
            
            # 測試無效參數
            self.create_test_case(
                name="ip_acl_create_invalid_params",
                method="POST",
                url="/api/v1/acls/ip",
                category="ip_acl",
                module="acl",
                body={
                    "name": "invalid_acl",
                    "type": "invalid_type"
                },
                expected_status=400,
                description="測試創建IP ACL時的無效參數處理"
            )
        ]
    
    def get_mac_acl_tests(self) -> List[APITestCase]:
        """MAC ACL API 測試案例"""
        return [
            # 獲取所有MAC ACL
            self.create_test_case(
                name="mac_acl_get_all",
                method="GET",
                url="/api/v1/acls/mac",
                category="mac_acl",
                module="acl",
                description="獲取所有MAC ACL"
            ),
            
            # 創建MAC ACL
            self.create_test_case(
                name="mac_acl_create",
                method="POST",
                url="/api/v1/acls/mac",
                category="mac_acl",
                module="acl",
                body=self.test_data.get('mac_acl_create', {
                    "name": "macAcl",
                    "aces": [
                        {
                            "access": "permit",
                            "sourceMacAddr": "00-e0-29-94-34-de",
                            "sourceMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "destMacAddr": "11-e0-29-94-34-de",
                            "destMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "sourceIpAddr": "192.168.2.10",
                            "sourceIpAddrBitmask": "255.255.255.255",
                            "destIpAddr": "192.168.2.11",
                            "destIpAddrBitmask": "255.255.255.255",
                            "vlanId": 100,
                            "vlanIdBitmask": 4095,
                            "protocol": 6,
                            "sourcePort": 100,
                            "sourcePortBitmask": 65535,
                            "destPort": 200,
                            "destPortBitmask": 65535
                        }
                    ]
                }),
                description="創建MAC ACL"
            ),
            
            # 獲取特定MAC ACL
            self.create_test_case(
                name="mac_acl_get_specific",
                method="GET",
                url="/api/v1/acls/mac/{aclName}",
                category="mac_acl",
                module="acl",
                params={"aclName": self.params.get('mac_acl_name', 'macAcl')},
                description=f"獲取MAC ACL {self.params.get('mac_acl_name', 'macAcl')}"
            ),
            
            # 更新MAC ACL
            self.create_test_case(
                name="mac_acl_update",
                method="PUT",
                url="/api/v1/acls/mac/{aclName}",
                category="mac_acl",
                module="acl",
                params={"aclName": self.params.get('mac_acl_name', 'macAcl')},
                body=self.test_data.get('mac_acl_update', {
                    "aces": [
                        {
                            "access": "permit",
                            "sourceMacAddr": "00-e0-29-94-34-de",
                            "sourceMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "destMacAddr": "11-e0-29-94-34-de",
                            "destMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "sourceIpAddr": "192.168.2.10",
                            "sourceIpAddrBitmask": "255.255.255.255",
                            "destIpAddr": "192.168.2.11",
                            "destIpAddrBitmask": "255.255.255.255",
                            "vlanId": 100,
                            "vlanIdBitmask": 4095,
                            "protocol": 6,
                            "sourcePort": 100,
                            "sourcePortBitmask": 65535,
                            "destPort": 200,
                            "destPortBitmask": 65535
                        }
                    ]
                }),
                description=f"更新MAC ACL {self.params.get('mac_acl_name', 'macAcl')}"
            ),
            
            # 刪除MAC ACL
            self.create_test_case(
                name="mac_acl_delete",
                method="DELETE",
                url="/api/v1/acls/mac/{aclName}",
                category="mac_acl",
                module="acl",
                params={"aclName": self.params.get('mac_acl_name_delete', 'macAcl')},
                description=f"刪除MAC ACL {self.params.get('mac_acl_name_delete', 'macAcl')}"
            ),
            
            # 創建帶有不同包格式的MAC ACL
            self.create_test_case(
                name="mac_acl_create_with_packet_format",
                method="POST",
                url="/api/v1/acls/mac",
                category="mac_acl",
                module="acl",
                body=self.test_data.get('mac_acl_packet_format', {
                    "name": "macAcl_tagged",
                    "aces": [
                        {
                            "access": "permit",
                            "pktFormat": "tagged-eth2",
                            "sourceMacAddr": "00-e0-29-94-34-de",
                            "sourceMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "destMacAddr": "11-e0-29-94-34-de",
                            "destMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "vlanId": 100,
                            "vlanIdBitmask": 4095,
                            "etherType": 2048,
                            "etherTypeBitmask": 65535
                        }
                    ]
                }),
                description="創建帶有特定包格式的MAC ACL"
            ),
            
            # 創建複雜MAC ACL (多個ACE)
            self.create_test_case(
                name="mac_acl_create_complex",
                method="POST",
                url="/api/v1/acls/mac",
                category="mac_acl",
                module="acl",
                body=self.test_data.get('mac_acl_complex', {
                    "name": "macAcl_complex",
                    "aces": [
                        {
                            "access": "permit",
                            "pktFormat": "all",
                            "sourceMacAddr": "00-e0-29-94-34-de",
                            "sourceMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "destMacAddr": "11-e0-29-94-34-de",
                            "destMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "vlanId": 100,
                            "vlanIdBitmask": 4095
                        },
                        {
                            "access": "deny",
                            "pktFormat": "all",
                            "sourceMacAddr": "66-e0-29-94-34-de",
                            "sourceMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "destMacAddr": "55-e0-29-94-34-de",
                            "destMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "vlanId": 100,
                            "vlanIdBitmask": 4095
                        }
                    ]
                }),
                description="創建複雜MAC ACL (多個ACE)"
            )
        ]
    
    def get_arp_acl_tests(self) -> List[APITestCase]:
        """ARP ACL API 測試案例"""
        return [
            # 獲取所有ARP ACL
            self.create_test_case(
                name="arp_acl_get_all",
                method="GET",
                url="/api/v1/acls/arp",
                category="arp_acl",
                module="acl",
                description="獲取所有ARP ACL"
            ),
            
            # 創建ARP ACL
            self.create_test_case(
                name="arp_acl_create",
                method="POST",
                url="/api/v1/acls/arp",
                category="arp_acl",
                module="acl",
                body=self.test_data.get('arp_acl_create', {
                    "name": "arpAcl",
                    "aces": [
                        {
                            "access": "permit",
                            "sourceIpAddr": "192.168.1.10",
                            "sourceIpAddrBitmask": "255.255.255.255",
                            "sourceMacAddr": "11-11-11-11-11-11",
                            "sourceMacAddrBitmask": "ff-ff-ff-ff-ff-ff"
                        }
                    ]
                }),
                description="創建ARP ACL"
            ),
            
            # 獲取特定ARP ACL
            self.create_test_case(
                name="arp_acl_get_specific",
                method="GET",
                url="/api/v1/acls/arp/{aclName}",
                category="arp_acl",
                module="acl",
                params={"aclName": self.params.get('arp_acl_name', 'arpAcl')},
                description=f"獲取ARP ACL {self.params.get('arp_acl_name', 'arpAcl')}"
            ),
            
            # 更新ARP ACL
            self.create_test_case(
                name="arp_acl_update",
                method="PUT",
                url="/api/v1/acls/arp/{aclName}",
                category="arp_acl",
                module="acl",
                params={"aclName": self.params.get('arp_acl_name', 'arpAcl')},
                body=self.test_data.get('arp_acl_update', {
                    "aces": [
                        {
                            "access": "permit",
                            "sourceIpAddr": "192.168.1.10",
                            "sourceIpAddrBitmask": "255.255.255.255",
                            "sourceMacAddr": "11-11-11-11-11-11",
                            "sourceMacAddrBitmask": "ff-ff-ff-ff-ff-ff"
                        }
                    ]
                }),
                description=f"更新ARP ACL {self.params.get('arp_acl_name', 'arpAcl')}"
            ),
            
            # 刪除ARP ACL
            self.create_test_case(
                name="arp_acl_delete",
                method="DELETE",
                url="/api/v1/acls/arp/{aclName}",
                category="arp_acl",
                module="acl",
                params={"aclName": self.params.get('arp_acl_name_delete', 'arpAcl')},
                description=f"刪除ARP ACL {self.params.get('arp_acl_name_delete', 'arpAcl')}"
            ),
            
            # 創建複雜ARP ACL
            self.create_test_case(
                name="arp_acl_create_complex",
                method="POST",
                url="/api/v1/acls/arp",
                category="arp_acl",
                module="acl",
                body=self.test_data.get('arp_acl_complex', {
                    "name": "arpAcl_complex",
                    "aces": [
                        {
                            "access": "permit",
                            "pktType": "request",
                            "sourceMacAddr": "00-e0-29-94-34-de",
                            "sourceMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "destMacAddr": "11-e0-29-94-34-de",
                            "destMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "sourceIpAddr": "192.168.5.1",
                            "sourceIpAddrBitmask": "255.255.255.0",
                            "destIpAddr": "192.168.5.2",
                            "destIpAddrBitmask": "255.255.255.255",
                            "logStatus": True
                        },
                        {
                            "access": "deny",
                            "pktType": "response",
                            "sourceMacAddr": "00-e0-29-94-34-de",
                            "sourceMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "sourceIpAddr": "192.168.5.11",
                            "sourceIpAddrBitmask": "255.255.255.0",
                            "logStatus": False
                        }
                    ]
                }),
                description="創建複雜ARP ACL (多個ACE)"
            )
        ]
    
    def get_ipv6_acl_tests(self) -> List[APITestCase]:
        """IPv6 ACL API 測試案例"""
        return [
            # 獲取所有IPv6 ACL
            self.create_test_case(
                name="ipv6_acl_get_all",
                method="GET",
                url="/api/v1/acls/ipv6",
                category="ipv6_acl",
                module="acl",
                description="獲取所有IPv6 ACL"
            ),
            
            # 創建標準IPv6 ACL
            self.create_test_case(
                name="ipv6_acl_create_standard",
                method="POST",
                url="/api/v1/acls/ipv6",
                category="ipv6_acl",
                module="acl",
                body=self.test_data.get('ipv6_acl_standard', {
                    "name": "std_ipv6_1",
                    "type": "standard",
                    "aces": [
                        {
                            "access": "permit",
                            "sourceIpAddr": "2100:DB9:2229::79",
                            "sourceIpAddrPrefixLen": 128
                        }
                    ]
                }),
                description="創建標準IPv6 ACL"
            ),
            
            # 創建擴展IPv6 ACL
            self.create_test_case(
                name="ipv6_acl_create_extended",
                method="POST",
                url="/api/v1/acls/ipv6",
                category="ipv6_acl",
                module="acl",
                body=self.test_data.get('ipv6_acl_extended', {
                    "name": "ext_ipv6_1",
                    "type": "extended",
                    "aces": [
                        {
                            "access": "permit",
                            "sourceIpAddr": "2009:DB9:2229::79",
                            "sourceIpAddrPrefixLen": 128,
                            "destIpAddr": "2009:DB9:2229::77",
                            "destIpAddrPrefixLen": 4,
                            "dscp": 0,
                            "nextHeader": 0,
                            "timeRange": "aaa"
                        }
                    ]
                }),
                description="創建擴展IPv6 ACL"
            ),
            
            # 獲取特定IPv6 ACL
            self.create_test_case(
                name="ipv6_acl_get_specific",
                method="GET",
                url="/api/v1/acls/ipv6/{aclName}",
                category="ipv6_acl",
                module="acl",
                params={"aclName": self.params.get('ipv6_acl_name', 'ext_ipv6_1')},
                description=f"獲取IPv6 ACL {self.params.get('ipv6_acl_name', 'ext_ipv6_1')}"
            ),
            
            # 更新IPv6 ACL
            self.create_test_case(
                name="ipv6_acl_update",
                method="PUT",
                url="/api/v1/acls/ipv6/{aclName}",
                category="ipv6_acl",
                module="acl",
                params={"aclName": self.params.get('ipv6_acl_name', 'ext_ipv6_1')},
                body=self.test_data.get('ipv6_acl_update', {
                    "aces": [
                        {
                            "access": "permit",
                            "sourceIpAddr": "2009:DB9:2229::99",
                            "sourceIpAddrPrefixLen": 128,
                            "destIpAddr": "2009:DB9:2229::77",
                            "destIpAddrPrefixLen": 4,
                            "dscp": 0,
                            "nextHeader": 0,
                            "timeRange": "aaa"
                        }
                    ]
                }),
                description=f"更新IPv6 ACL {self.params.get('ipv6_acl_name', 'ext_ipv6_1')}"
            ),
            
            # 刪除IPv6 ACL
            self.create_test_case(
                name="ipv6_acl_delete",
                method="DELETE",
                url="/api/v1/acls/ipv6/{aclName}",
                category="ipv6_acl",
                module="acl",
                params={"aclName": self.params.get('ipv6_acl_name_delete', 'test')},
                description=f"刪除IPv6 ACL {self.params.get('ipv6_acl_name_delete', 'test')}"
            ),
            
            # 創建複雜IPv6 ACL
            self.create_test_case(
                name="ipv6_acl_create_complex",
                method="POST",
                url="/api/v1/acls/ipv6",
                category="ipv6_acl",
                module="acl",
                body=self.test_data.get('ipv6_acl_complex', {
                    "name": "complex_ipv6",
                    "type": "extended",
                    "aces": [
                        {
                            "access": "permit",
                            "sourceIpAddr": "2009:DB9:2229::79",
                            "sourceIpAddrPrefixLen": 128,
                            "destIpAddr": "2009:DB9:2229::88",
                            "destIpAddrPrefixLen": 128,
                            "dscp": 0,
                            "nextHeader": 6,
                            "timeRange": ""
                        },
                        {
                            "access": "deny",
                            "sourceIpAddr": "2009:DB9:2229::80",
                            "sourceIpAddrPrefixLen": 64,
                            "dscp": 32,
                            "nextHeader": 17
                        }
                    ]
                }),
                description="創建複雜IPv6 ACL (多個ACE)"
            )
        ]
    
    def get_acl_interface_tests(self) -> List[APITestCase]:
        """ACL Interface Binding API 測試案例"""
        return [
            # 獲取所有接口的ACL綁定
            self.create_test_case(
                name="acl_interface_get_all",
                method="GET",
                url="/api/v1/acls/interfaces",
                category="acl_interface",
                module="acl",
                description="獲取所有接口的ACL綁定"
            ),
            
            # 獲取特定類型的ACL綁定
            self.create_test_case(
                name="acl_interface_get_by_type",
                method="GET",
                url="/api/v1/acls/interfaces",
                category="acl_interface",
                module="acl",
                params={"aclType": "ip"},
                description="獲取IP類型的ACL綁定"
            ),
            
            # 綁定IP ACL到接口
            self.create_test_case(
                name="acl_interface_bind_ip_acl",
                method="POST",
                url="/api/v1/acls/interfaces",
                category="acl_interface",
                module="acl",
                body=self.test_data.get('acl_interface_bind_ip', {
                    "ifId": "eth1/12",
                    "aclName": "standardAcl",
                    "aclType": "ip",
                    "isIngress": True
                }),
                description="綁定IP ACL到接口"
            ),
            
            # 綁定MAC ACL到接口
            self.create_test_case(
                name="acl_interface_bind_mac_acl",
                method="POST",
                url="/api/v1/acls/interfaces",
                category="acl_interface",
                module="acl",
                body=self.test_data.get('acl_interface_bind_mac', {
                    "ifId": "eth1/13",
                    "aclName": "macAcl",
                    "aclType": "mac",
                    "isIngress": True,
                    "counter": True
                }),
                description="綁定MAC ACL到接口"
            ),
            
            # 綁定IPv6 ACL到接口
            self.create_test_case(
                name="acl_interface_bind_ipv6_acl",
                method="POST",
                url="/api/v1/acls/interfaces",
                category="acl_interface",
                module="acl",
                body=self.test_data.get('acl_interface_bind_ipv6', {
                    "ifId": "eth1/14",
                    "aclName": "ext_ipv6_1",
                    "aclType": "ipv6",
                    "isIngress": False,
                    "counter": False,
                    "timeRange": "business_hours"
                }),
                description="綁定IPv6 ACL到接口"
            ),
            
            # 獲取特定接口和方向的ACL組
            self.create_test_case(
                name="acl_interface_get_specific_group",
                method="GET",
                url="/api/v1/acls/interfaces/{ifId}/directions/{isIngress}",
                category="acl_interface",
                module="acl",
                params={"ifId": self.params.get('interface_id', 'eth1%2f12'), "isIngress": True},
                description=f"獲取接口 {self.params.get('interface_id', 'eth1/12')} 入方向的ACL組"
            ),
            
            # 解綁接口ACL
            self.create_test_case(
                name="acl_interface_unbind",
                method="DELETE",
                url="/api/v1/acls/interfaces/{ifId}/directions/{isIngress}",
                category="acl_interface",
                module="acl",
                params={"ifId": self.params.get('interface_id', 'eth1%2f1'), "isIngress": True},
                description=f"解綁接口 {self.params.get('interface_id', 'eth1/1')} 入方向的ACL"
            ),
            
            # 綁定ACL到Trunk接口
            self.create_test_case(
                name="acl_interface_bind_trunk",
                method="POST",
                url="/api/v1/acls/interfaces",
                category="acl_interface",
                module="acl",
                body=self.test_data.get('acl_interface_bind_trunk', {
                    "ifId": "trunk1",
                    "aclName": "ext_acl_1",
                    "aclType": "ip",
                    "isIngress": True,
                    "counter": True
                }),
                description="綁定ACL到Trunk接口"
            ),
            
            # 綁定ACL到所有接口
            self.create_test_case(
                name="acl_interface_bind_all",
                method="POST",
                url="/api/v1/acls/interfaces",
                category="acl_interface",
                module="acl",
                body=self.test_data.get('acl_interface_bind_all', {
                    "ifId": "all",
                    "aclName": "global_acl",
                    "aclType": "ip",
                    "isIngress": True
                }),
                description="綁定ACL到所有接口"
            )
        ]
    
    def get_tcam_utilization_tests(self) -> List[APITestCase]:
        """TCAM Utilization API 測試案例"""
        return [
            # 獲取TCAM利用率參數
            self.create_test_case(
                name="tcam_utilization_get",
                method="GET",
                url="/api/v1/acls/tcam-utilization",
                category="tcam_utilization",
                module="acl",
                description="獲取TCAM利用率參數"
            ),
            
            # 多次獲取TCAM利用率以監控變化
            self.create_test_case(
                name="tcam_utilization_monitor_1",
                method="GET",
                url="/api/v1/acls/tcam-utilization",
                category="tcam_utilization",
                module="acl",
                description="監控TCAM利用率 - 第1次檢查"
            ),
            
            self.create_test_case(
                name="tcam_utilization_monitor_2",
                method="GET",
                url="/api/v1/acls/tcam-utilization",
                category="tcam_utilization",
                module="acl",
                description="監控TCAM利用率 - 第2次檢查"
            ),
            
            self.create_test_case(
                name="tcam_utilization_monitor_3",
                method="GET",
                url="/api/v1/acls/tcam-utilization",
                category="tcam_utilization",
                module="acl",
                description="監控TCAM利用率 - 第3次檢查"
            ),

            # 獲取所有IPv4 ACL
            self.create_test_case(
                name="acl_get_all_ipv4_acls",
                method="GET",
                url="/api/v1/acls/ipv4",
                category="acl_ipv4",
                module="acl",
                description="獲取所有IPv4 ACL"
            ),
            
            # 創建標準IPv4 ACL
            self.create_test_case(
                name="acl_create_standard_ipv4_acl",
                method="POST",
                url="/api/v1/acls/ipv4",
                category="acl_ipv4",
                module="acl",
                body=self.test_data.get('acl_standard_ipv4', {
                    "name": "std_acl_1",
                    "type": "standard",
                    "aces": [
                        {
                            "access": "permit",
                            "sourceIpAddr": "192.168.1.0",
                            "sourceIpAddrBitmask": "255.255.255.0"
                        }
                    ]
                }),
                description="創建標準IPv4 ACL"
            ),
            
            # 創建擴展IPv4 ACL
            self.create_test_case(
                name="acl_create_extended_ipv4_acl",
                method="POST",
                url="/api/v1/acls/ipv4",
                category="acl_ipv4",
                module="acl",
                body=self.test_data.get('acl_extended_ipv4', {
                    "name": "ext_acl_1",
                    "type": "extended",
                    "aces": [
                        {
                            "access": "permit",
                            "protocol": "tcp",
                            "sourceIpAddr": "192.168.1.0",
                            "sourceIpAddrBitmask": "255.255.255.0",
                            "destIpAddr": "10.0.0.0",
                            "destIpAddrBitmask": "255.0.0.0",
                            "sourcePort": 80,
                            "destPort": 443
                        }
                    ]
                }),
                description="創建擴展IPv4 ACL"
            ),
            
            # 創建複雜IPv4 ACL - 多條規則
            self.create_test_case(
                name="acl_create_complex_ipv4_acl",
                method="POST",
                url="/api/v1/acls/ipv4",
                category="acl_ipv4",
                module="acl",
                body=self.test_data.get('acl_complex_ipv4', {
                    "name": "complex_acl_1",
                    "type": "extended",
                    "aces": [
                        {
                            "access": "permit",
                            "protocol": "tcp",
                            "sourceIpAddr": "192.168.1.0",
                            "sourceIpAddrBitmask": "255.255.255.0",
                            "destIpAddr": "10.0.0.0",
                            "destIpAddrBitmask": "255.0.0.0",
                            "sourcePort": 80,
                            "destPort": 443
                        },
                        {
                            "access": "deny",
                            "protocol": "udp",
                            "sourceIpAddr": "172.16.0.0",
                            "sourceIpAddrBitmask": "255.240.0.0",
                            "destIpAddr": "0.0.0.0",
                            "destIpAddrBitmask": "0.0.0.0",
                            "sourcePort": 53,
                            "destPort": 0
                        }
                    ]
                }),
                description="創建複雜IPv4 ACL - 多條規則"
            ),
            
            # 獲取特定IPv4 ACL
            self.create_test_case(
                name="acl_get_specific_ipv4_acl",
                method="GET",
                url="/api/v1/acls/ipv4/{name}",
                category="acl_ipv4",
                module="acl",
                params={"name": "std_acl_1"},
                description="獲取特定IPv4 ACL"
            ),
            
            # 獲取參數化IPv4 ACL
            self.create_test_case(
                name="acl_get_parameterized_ipv4_acl",
                method="GET",
                url="/api/v1/acls/ipv4/{name}",
                category="acl_ipv4",
                module="acl",
                params={"name": self.params.get('ip_acl_name', 'std_acl_1')},
                description=f"獲取IPv4 ACL {self.params.get('ip_acl_name', 'std_acl_1')}"
            ),
            
            # 更新IPv4 ACL
            self.create_test_case(
                name="acl_update_ipv4_acl",
                method="PUT",
                url="/api/v1/acls/ipv4/{name}",
                category="acl_ipv4",
                module="acl",
                params={"name": "std_acl_1"},
                body=self.test_data.get('acl_update_ipv4', {
                    "name": "std_acl_1",
                    "type": "standard",
                    "aces": [
                        {
                            "access": "permit",
                            "sourceIpAddr": "192.168.1.0",
                            "sourceIpAddrBitmask": "255.255.255.0"
                        },
                        {
                            "access": "deny",
                            "sourceIpAddr": "192.168.2.0",
                            "sourceIpAddrBitmask": "255.255.255.0"
                        }
                    ]
                }),
                description="更新IPv4 ACL - 添加新規則"
            ),
            
            # 刪除IPv4 ACL
            self.create_test_case(
                name="acl_delete_ipv4_acl",
                method="DELETE",
                url="/api/v1/acls/ipv4/{name}",
                category="acl_ipv4",
                module="acl",
                params={"name": self.params.get('ip_acl_name_delete', 'test_acl')},
                description=f"刪除IPv4 ACL {self.params.get('ip_acl_name_delete', 'test_acl')}"
            ),
            
            # 測試無效IPv4 ACL名稱
            self.create_test_case(
                name="acl_test_invalid_ipv4_name",
                method="POST",
                url="/api/v1/acls/ipv4",
                category="acl_ipv4",
                module="acl",
                body=self.test_data.get('acl_invalid_name', {
                    "name": "",  # 空名稱
                    "type": "standard",
                    "aces": []
                }),
                expected_status=400,
                description="測試無效IPv4 ACL名稱"
            ),
            
            # 測試重複IPv4 ACL名稱
            self.create_test_case(
                name="acl_test_duplicate_ipv4_name",
                method="POST",
                url="/api/v1/acls/ipv4",
                category="acl_ipv4",
                module="acl",
                body=self.test_data.get('acl_duplicate_name', {
                    "name": "std_acl_1",  # 重複名稱
                    "type": "standard",
                    "aces": [
                        {
                            "access": "permit",
                            "sourceIpAddr": "10.0.0.0",
                            "sourceIpAddrBitmask": "255.0.0.0"
                        }
                    ]
                }),
                expected_status=400,
                description="測試重複IPv4 ACL名稱"
            )
        ]
    
    def get_acl_ipv6_tests(self) -> List[APITestCase]:
        """IPv6 ACL API 測試案例"""
        return [
            # 獲取所有IPv6 ACL
            self.create_test_case(
                name="acl_get_all_ipv6_acls",
                method="GET",
                url="/api/v1/acls/ipv6",
                category="acl_ipv6",
                module="acl",
                description="獲取所有IPv6 ACL"
            ),
            
            # 創建IPv6 ACL
            self.create_test_case(
                name="acl_create_ipv6_acl",
                method="POST",
                url="/api/v1/acls/ipv6",
                category="acl_ipv6",
                module="acl",
                body=self.test_data.get('acl_ipv6', {
                    "name": "ext_ipv6_1",
                    "aces": [
                        {
                            "access": "permit",
                            "protocol": "tcp",
                            "sourceIpv6Addr": "2001:db8::/32",
                            "destIpv6Addr": "fe80::/10",
                            "sourcePort": 80,
                            "destPort": 443
                        }
                    ]
                }),
                description="創建IPv6 ACL"
            ),
            
            # 創建複雜IPv6 ACL
            self.create_test_case(
                name="acl_create_complex_ipv6_acl",
                method="POST",
                url="/api/v1/acls/ipv6",
                category="acl_ipv6",
                module="acl",
                body=self.test_data.get('acl_complex_ipv6', {
                    "name": "complex_ipv6_1",
                    "aces": [
                        {
                            "access": "permit",
                            "protocol": "tcp",
                            "sourceIpv6Addr": "2001:db8::/32",
                            "destIpv6Addr": "fe80::/10",
                            "sourcePort": 80,
                            "destPort": 443
                        },
                        {
                            "access": "deny",
                            "protocol": "udp",
                            "sourceIpv6Addr": "fc00::/7",
                            "destIpv6Addr": "::/0",
                            "sourcePort": 53,
                            "destPort": 0
                        }
                    ]
                }),
                description="創建複雜IPv6 ACL"
            ),
            
            # 獲取特定IPv6 ACL
            self.create_test_case(
                name="acl_get_specific_ipv6_acl",
                method="GET",
                url="/api/v1/acls/ipv6/{name}",
                category="acl_ipv6",
                module="acl",
                params={"name": "ext_ipv6_1"},
                description="獲取特定IPv6 ACL"
            ),
            
            # 獲取參數化IPv6 ACL
            self.create_test_case(
                name="acl_get_parameterized_ipv6_acl",
                method="GET",
                url="/api/v1/acls/ipv6/{name}",
                category="acl_ipv6",
                module="acl",
                params={"name": self.params.get('ipv6_acl_name', 'ext_ipv6_1')},
                description=f"獲取IPv6 ACL {self.params.get('ipv6_acl_name', 'ext_ipv6_1')}"
            ),
            
            # 更新IPv6 ACL
            self.create_test_case(
                name="acl_update_ipv6_acl",
                method="PUT",
                url="/api/v1/acls/ipv6/{name}",
                category="acl_ipv6",
                module="acl",
                params={"name": "ext_ipv6_1"},
                body=self.test_data.get('acl_update_ipv6', {
                    "name": "ext_ipv6_1",
                    "aces": [
                        {
                            "access": "permit",
                            "protocol": "tcp",
                            "sourceIpv6Addr": "2001:db8::/32",
                            "destIpv6Addr": "fe80::/10",
                            "sourcePort": 80,
                            "destPort": 443
                        },
                        {
                            "access": "permit",
                            "protocol": "icmpv6",
                            "sourceIpv6Addr": "::/0",
                            "destIpv6Addr": "::/0"
                        }
                    ]
                }),
                description="更新IPv6 ACL - 添加ICMPv6規則"
            ),
            
            # 刪除IPv6 ACL
            self.create_test_case(
                name="acl_delete_ipv6_acl",
                method="DELETE",
                url="/api/v1/acls/ipv6/{name}",
                category="acl_ipv6",
                module="acl",
                params={"name": self.params.get('ipv6_acl_name_delete', 'test')},
                description=f"刪除IPv6 ACL {self.params.get('ipv6_acl_name_delete', 'test')}"
            ),
            
            # 測試無效IPv6地址
            self.create_test_case(
                name="acl_test_invalid_ipv6_address",
                method="POST",
                url="/api/v1/acls/ipv6",
                category="acl_ipv6",
                module="acl",
                body=self.test_data.get('acl_invalid_ipv6', {
                    "name": "invalid_ipv6",
                    "aces": [
                        {
                            "access": "permit",
                            "protocol": "tcp",
                            "sourceIpv6Addr": "invalid::address",
                            "destIpv6Addr": "fe80::/10"
                        }
                    ]
                }),
                expected_status=400,
                description="測試無效IPv6地址"
            )
        ]
    
    def get_acl_mac_tests(self) -> List[APITestCase]:
        """MAC ACL API 測試案例"""
        return [
            # 獲取所有MAC ACL
            self.create_test_case(
                name="acl_get_all_mac_acls",
                method="GET",
                url="/api/v1/acls/mac",
                category="acl_mac",
                module="acl",
                description="獲取所有MAC ACL"
            ),
            
            # 創建MAC ACL
            self.create_test_case(
                name="acl_create_mac_acl",
                method="POST",
                url="/api/v1/acls/mac",
                category="acl_mac",
                module="acl",
                body=self.test_data.get('acl_mac', {
                    "name": "macAcl",
                    "aces": [
                        {
                            "access": "permit",
                            "pktFormat": "all",
                            "sourceMacAddr": "00-e0-29-94-34-de",
                            "sourceMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "destMacAddr": "11-e0-29-94-34-de",
                            "destMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "sourceIpAddr": "0.0.0.0",
                            "sourceIpAddrBitmask": "0.0.0.0",
                            "destIpAddr": "0.0.0.0",
                            "destIpAddrBitmask": "0.0.0.0",
                            "vlanId": 100,
                            "vlanIdBitmask": 4095,
                            "etherType": 0,
                            "etherTypeBitmask": 0,
                            "protocol": 0,
                            "sourcePort": 0,
                            "sourcePortBitmask": 0,
                            "destPort": 0,
                            "destPortBitmask": 0,
                            "timeRange": ""
                        }
                    ]
                }),
                description="創建MAC ACL"
            ),
            
            # 創建複雜MAC ACL
            self.create_test_case(
                name="acl_create_complex_mac_acl",
                method="POST",
                url="/api/v1/acls/mac",
                category="acl_mac",
                module="acl",
                body=self.test_data.get('acl_complex_mac', {
                    "name": "complex_mac_acl",
                    "aces": [
                        {
                            "access": "permit",
                            "pktFormat": "ethernet_ii",
                            "sourceMacAddr": "00-11-22-33-44-55",
                            "sourceMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "destMacAddr": "aa-bb-cc-dd-ee-ff",
                            "destMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "vlanId": 200,
                            "vlanIdBitmask": 4095,
                            "etherType": 2048,
                            "etherTypeBitmask": 65535
                        },
                        {
                            "access": "deny",
                            "pktFormat": "all",
                            "sourceMacAddr": "00-00-00-00-00-00",
                            "sourceMacAddrBitmask": "00-00-00-00-00-00",
                            "destMacAddr": "ff-ff-ff-ff-ff-ff",
                            "destMacAddrBitmask": "ff-ff-ff-ff-ff-ff"
                        }
                    ]
                }),
                description="創建複雜MAC ACL"
            ),
            
            # 獲取特定MAC ACL
            self.create_test_case(
                name="acl_get_specific_mac_acl",
                method="GET",
                url="/api/v1/acls/mac/{name}",
                category="acl_mac",
                module="acl",
                params={"name": "macAcl"},
                description="獲取特定MAC ACL"
            ),
            
            # 獲取參數化MAC ACL
            self.create_test_case(
                name="acl_get_parameterized_mac_acl",
                method="GET",
                url="/api/v1/acls/mac/{name}",
                category="acl_mac",
                module="acl",
                params={"name": self.params.get('mac_acl_name', 'macAcl')},
                description=f"獲取MAC ACL {self.params.get('mac_acl_name', 'macAcl')}"
            ),
            
            # 更新MAC ACL
            self.create_test_case(
                name="acl_update_mac_acl",
                method="PUT",
                url="/api/v1/acls/mac/{name}",
                category="acl_mac",
                module="acl",
                params={"name": "macAcl"},
                body=self.test_data.get('acl_update_mac', {
                    "name": "macAcl",
                    "aces": [
                        {
                            "access": "permit",
                            "pktFormat": "all",
                            "sourceMacAddr": "00-e0-29-94-34-de",
                            "sourceMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "destMacAddr": "11-e0-29-94-34-de",
                            "destMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "vlanId": 100,
                            "vlanIdBitmask": 4095
                        },
                        {
                            "access": "deny",
                            "pktFormat": "ethernet_ii",
                            "sourceMacAddr": "00-11-22-33-44-55",
                            "sourceMacAddrBitmask": "ff-ff-ff-00-00-00",
                            "destMacAddr": "00-00-00-00-00-00",
                            "destMacAddrBitmask": "00-00-00-00-00-00"
                        }
                    ]
                }),
                description="更新MAC ACL - 添加拒絕規則"
            ),
            
            # 刪除MAC ACL
            self.create_test_case(
                name="acl_delete_mac_acl",
                method="DELETE",
                url="/api/v1/acls/mac/{name}",
                category="acl_mac",
                module="acl",
                params={"name": self.params.get('mac_acl_name_delete', 'macAcl')},
                description=f"刪除MAC ACL {self.params.get('mac_acl_name_delete', 'macAcl')}"
            ),
            
            # 測試無效MAC地址
            self.create_test_case(
                name="acl_test_invalid_mac_address",
                method="POST",
                url="/api/v1/acls/mac",
                category="acl_mac",
                module="acl",
                body=self.test_data.get('acl_invalid_mac', {
                    "name": "invalid_mac",
                    "aces": [
                        {
                            "access": "permit",
                            "pktFormat": "all",
                            "sourceMacAddr": "invalid-mac-address",
                            "sourceMacAddrBitmask": "ff-ff-ff-ff-ff-ff"
                        }
                    ]
                }),
                expected_status=400,
                description="測試無效MAC地址"
            )
        ]
    
    def get_acl_arp_tests(self) -> List[APITestCase]:
        """ARP ACL API 測試案例"""
        return [
            # 獲取所有ARP ACL
            self.create_test_case(
                name="acl_get_all_arp_acls",
                method="GET",
                url="/api/v1/acls/arp",
                category="acl_arp",
                module="acl",
                description="獲取所有ARP ACL"
            ),
            
            # 創建ARP ACL
            self.create_test_case(
                name="acl_create_arp_acl",
                method="POST",
                url="/api/v1/acls/arp",
                category="acl_arp",
                module="acl",
                body=self.test_data.get('acl_arp', {
                    "name": "arpAcl",
                    "aces": [
                        {
                            "access": "permit",
                            "senderIpAddr": "192.168.1.0",
                            "senderIpAddrBitmask": "255.255.255.0",
                            "senderMacAddr": "00-11-22-33-44-55",
                            "senderMacAddrBitmask": "ff-ff-ff-ff-ff-ff",
                            "targetIpAddr": "10.0.0.0",
                            "targetIpAddrBitmask": "255.0.0.0",
                            "targetMacAddr": "aa-bb-cc-dd-ee-ff",
                            "targetMacAddrBitmask": "ff-ff-ff-ff-ff-ff"
                        }
                    ]
                }),
                description="創建ARP ACL"
            ),
            
            # 創建複雜ARP ACL
            self.create_test_case(
                name="acl_create_complex_arp_acl",
                method="POST",
                url="/api/v1/acls/arp",
                category="acl_arp",
                module="acl",
                body=self.test_data.get('acl_complex_arp', {
                    "name": "complex_arp_acl",
                    "aces": [
                        {
                            "access": "permit",
                            "senderIpAddr": "192.168.1.0",
                            "senderIpAddrBitmask": "255.255.255.0",
                            "senderMacAddr": "00-11-22-33-44-55",
                            "senderMacAddrBitmask": "ff-ff-ff-ff-ff-ff"
                        },
                        {
                            "access": "deny",
                            "senderIpAddr": "172.16.0.0",
                            "senderIpAddrBitmask": "255.240.0.0",
                            "senderMacAddr": "00-00-00-00-00-00",
                            "senderMacAddrBitmask": "00-00-00-00-00-00"
                        }
                    ]
                }),
                description="創建複雜ARP ACL"
            ),
            
            # 獲取特定ARP ACL
            self.create_test_case(
                name="acl_get_specific_arp_acl",
                method="GET",
                url="/api/v1/acls/arp/{name}",
                category="acl_arp",
                module="acl",
                params={"name": "arpAcl"},
                description="獲取特定ARP ACL"
            ),
            
            # 獲取參數化ARP ACL
            self.create_test_case(
                name="acl_get_parameterized_arp_acl",
                method="GET",
                url="/api/v1/acls/arp/{name}",
                category="acl_arp",
                module="acl",
                params={"name": self.params.get('arp_acl_name', 'arpAcl')},
                description=f"獲取ARP ACL {self.params.get('arp_acl_name', 'arpAcl')}"
            ),
            
            # 更新ARP ACL
            self.create_test_case(
                name="acl_update_arp_acl",
                method="PUT",
                url="/api/v1/acls/arp/{name}",
                category="acl_arp",
                module="acl",
                params={"name": "arpAcl"},
                body=self.test_data.get('acl_update_arp', {
                    "name": "arpAcl",
                    "aces": [
                        {
                            "access": "permit",
                            "senderIpAddr": "192.168.1.0",
                            "senderIpAddrBitmask": "255.255.255.0",
                            "senderMacAddr": "00-11-22-33-44-55",
                            "senderMacAddrBitmask": "ff-ff-ff-ff-ff-ff"
                        },
                        {
                            "access": "permit",
                            "senderIpAddr": "192.168.2.0",
                            "senderIpAddrBitmask": "255.255.255.0",
                            "senderMacAddr": "00-aa-bb-cc-dd-ee",
                            "senderMacAddrBitmask": "ff-ff-ff-ff-ff-ff"
                        }
                    ]
                }),
                description="更新ARP ACL - 添加新規則"
            ),
            
            # 刪除ARP ACL
            self.create_test_case(
                name="acl_delete_arp_acl",
                method="DELETE",
                url="/api/v1/acls/arp/{name}",
                category="acl_arp",
                module="acl",
                params={"name": self.params.get('arp_acl_name_delete', 'arpAcl')},
                description=f"刪除ARP ACL {self.params.get('arp_acl_name_delete', 'arpAcl')}"
            )
        ]
    
    def get_acl_tcam_tests(self) -> List[APITestCase]:
        """TCAM Utilization API 測試案例"""
        return [
            # 獲取TCAM利用率參數
            self.create_test_case(
                name="acl_get_tcam_utilization",
                method="GET",
                url="/api/v1/acls/tcam-utilization",
                category="acl_tcam",
                module="acl",
                description="獲取TCAM利用率參數"
            ),
            
            # 監控TCAM利用率 - 第1次檢查
            self.create_test_case(
                name="acl_monitor_tcam_utilization_1",
                method="GET",
                url="/api/v1/acls/tcam-utilization",
                category="acl_tcam",
                module="acl",
                description="監控TCAM利用率 - 第1次檢查"
            ),
            
            # 監控TCAM利用率 - 第2次檢查
            self.create_test_case(
                name="acl_monitor_tcam_utilization_2",
                method="GET",
                url="/api/v1/acls/tcam-utilization",
                category="acl_tcam",
                module="acl",
                description="監控TCAM利用率 - 第2次檢查"
            ),
            
            # 監控TCAM利用率 - 第3次檢查
            self.create_test_case(
                name="acl_monitor_tcam_utilization_3",
                method="GET",
                url="/api/v1/acls/tcam-utilization",
                category="acl_tcam",
                module="acl",
                description="監控TCAM利用率 - 第3次檢查"
            ),
            
            # 檢查TCAM資源分配
            self.create_test_case(
                name="acl_check_tcam_resource_allocation",
                method="GET",
                url="/api/v1/acls/tcam-utilization",
                category="acl_tcam",
                module="acl",
                description="檢查TCAM資源分配"
            ),
            
            # 驗證TCAM使用情況
            self.create_test_case(
                name="acl_verify_tcam_usage",
                method="GET",
                url="/api/v1/acls/tcam-utilization",
                category="acl_tcam",
                module="acl",
                description="驗證TCAM使用情況"
            )
        ]