#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VLAN 模組測試案例
包含VLAN, Traffic Segmentation, Protocol VLAN, MAC VLAN, Voice VLAN等相關API測試
"""

from typing import List
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_tests import BaseTests, APITestCase

class VLANTests(BaseTests):
    """VLAN 模組測試類"""
    
    def get_categories(self) -> List[str]:
        """獲取VLAN模組支援的類別"""
        return [
            "traffic_segmentation",
            "vlan",
            "protocol_vlan",
            "mac_vlan",
            "voice_vlan",
            "dot1q_base",
            "dot1q_vlan",
            "dot1d_garp",
            "vlan_l3_interface"
        ]
    
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有VLAN測試案例"""
        all_tests = []
        all_tests.extend(self.get_traffic_segmentation_tests())
        all_tests.extend(self.get_vlan_tests())
        all_tests.extend(self.get_protocol_vlan_tests())
        all_tests.extend(self.get_mac_vlan_tests())
        all_tests.extend(self.get_voice_vlan_tests())
        all_tests.extend(self.get_dot1q_base_tests())
        all_tests.extend(self.get_dot1q_vlan_tests())
        all_tests.extend(self.get_dot1d_garp_tests())
        all_tests.extend(self.get_vlan_l3_interface_tests())
        return all_tests
    
    def get_traffic_segmentation_tests(self) -> List[APITestCase]:
        """Traffic Segmentation API 測試案例"""
        return [
            self.create_test_case(
                name="traffic_segmentation_get_setting",
                method="GET",
                url="/api/v1/traffic-segmentation",
                category="traffic_segmentation",
                module="vlan",
                description="獲取流量分段設置"
            ),
            self.create_test_case(
                name="traffic_segmentation_configure_global",
                method="PUT",
                url="/api/v1/traffic-segmentation",
                category="traffic_segmentation",
                module="vlan",
                body=self.test_data.get('traffic_segmentation_global', {"status": True}),
                description="配置流量分段全局設置"
            ),
            self.create_test_case(
                name="traffic_segmentation_get_all_sessions",
                method="GET",
                url="/api/v1/traffic-segmentation/sessions",
                category="traffic_segmentation",
                module="vlan",
                description="獲取所有流量分段會話"
            ),
            self.create_test_case(
                name="traffic_segmentation_create_session",
                method="POST",
                url="/api/v1/traffic-segmentation/sessions",
                category="traffic_segmentation",
                module="vlan",
                body=self.test_data.get('traffic_segmentation_session', {"sessionId": 1}),
                description="創建流量分段客戶端會話"
            ),
            self.create_test_case(
                name="traffic_segmentation_get_session",
                method="GET",
                url="/api/v1/traffic-segmentation/sessions/{sessionId}",
                category="traffic_segmentation",
                module="vlan",
                params={"sessionId": self.params.get('session_id', 1)},
                description=f"獲取流量分段會話 {self.params.get('session_id', 1)}"
            ),
            self.create_test_case(
                name="traffic_segmentation_delete_session",
                method="DELETE",
                url="/api/v1/traffic-segmentation/sessions/{sessionId}",
                category="traffic_segmentation",
                module="vlan",
                params={"sessionId": self.params.get('session_id', 1)},
                description=f"刪除流量分段會話 {self.params.get('session_id', 1)}"
            )
        ]
    
    def get_vlan_tests(self) -> List[APITestCase]:
        """VLAN API 測試案例"""
        return [
            self.create_test_case(
                name="vlan_get_all",
                method="GET",
                url="/api/v1/vlans",
                category="vlan",
                module="vlan",
                description="獲取所有VLAN"
            ),
            self.create_test_case(
                name="vlan_create",
                method="POST",
                url="/api/v1/vlans",
                category="vlan",
                module="vlan",
                body=self.test_data.get('vlan_create', {
                    "vlanId": 100,
                    "name": "TestVlan100"
                }),
                description="創建VLAN"
            ),
            self.create_test_case(
                name="vlan_get_specific",
                method="GET",
                url="/api/v1/vlans/{vlanId}",
                category="vlan",
                module="vlan",
                params={"vlanId": self.params.get('vlan_id', 100)},
                description=f"獲取VLAN {self.params.get('vlan_id', 100)}"
            ),
            self.create_test_case(
                name="vlan_update_members",
                method="PUT",
                url="/api/v1/vlans/{vlanId}",
                category="vlan",
                module="vlan",
                params={"vlanId": 100},
                body=self.test_data.get('vlan_members', {
                    "members": [
                        {"ifId": "eth1/1", "isTagged": False},
                        {"ifId": "eth1/2", "isTagged": True}
                    ]
                }),
                description=f"更新VLAN {self.params.get('vlan_id', 100)} 成員"
            ),
            self.create_test_case(
                name="vlan_remove_all_members",
                method="DELETE",
                url="/api/v1/vlans/{vlanId}/interfaces",
                category="vlan",
                module="vlan",
                params={"vlanId": 100},
                description=f"移除VLAN {self.params.get('vlan_id', 100)} 所有成員"
            ),
            self.create_test_case(
                name="vlan_remove_member",
                method="DELETE",
                url="/api/v1/vlans/{vlanId}/interfaces/{ifId}",
                category="vlan",
                module="vlan",
                params={"vlanId": 100, "ifId": self.params.get('interface_id', 'eth1/1')},
                description=f"從VLAN {self.params.get('vlan_id', 100)} 移除接口 {self.params.get('interface_id', 'eth1/1')}"
            ),
            self.create_test_case(
                name="vlan_delete",
                method="DELETE",
                url="/api/v1/vlans/{vlanId}",
                category="vlan",
                module="vlan",
                params={"vlanId": 100},
                description=f"刪除VLAN {self.params.get('vlan_id', 100)}"
            )
        ]
    
    def get_protocol_vlan_tests(self) -> List[APITestCase]:
        """Protocol VLAN API 測試案例"""
        return [
            # 獲取所有協議組
            self.create_test_case(
                name="protocol_vlan_get_all_groups",
                method="GET",
                url="/api/v1/protocol-vlan",
                category="protocol_vlan",
                module="vlan",
                description="獲取所有協議組"
            ),
            
            # 創建協議組
            self.create_test_case(
                name="protocol_vlan_create_group",
                method="POST",
                url="/api/v1/protocol-vlan",
                category="protocol_vlan",
                module="vlan",
                body=self.test_data.get('protocol_group', {
                    "frameType": "ethernet",
                    "protocolType": "ip",
                    "groupId": 1
                }),
                description="創建協議組"
            ),
            
            # 獲取特定協議組
            self.create_test_case(
                name="protocol_vlan_get_group",
                method="GET",
                url="/api/v1/protocol-vlan/frame-type/{frameType}/protocol-type/{protocolType}",
                category="protocol_vlan",
                module="vlan",
                params={"frameType": self.params.get('frame_type', 'ethernet'), "protocolType": self.params.get('protocol_type', 'ip')},
                description=f"獲取協議組 {self.params.get('frame_type', 'ethernet')}/{self.params.get('protocol_type', 'ip')}"
            ),
            
            # 更新協議組
            self.create_test_case(
                name="protocol_vlan_update_group",
                method="PUT",
                url="/api/v1/protocol-vlan/frame-type/{frameType}/protocol-type/{protocolType}",
                category="protocol_vlan",
                module="vlan",
                params={"frameType": self.params.get('frame_type', 'ethernet'), "protocolType": self.params.get('protocol_type', 'ip')},
                body={"groupId": 2},
                description=f"更新協議組 {self.params.get('frame_type', 'ethernet')}/{self.params.get('protocol_type', 'ip')}"
            ),
            
            # 刪除協議組
            self.create_test_case(
                name="protocol_vlan_delete_group",
                method="DELETE",
                url="/api/v1/protocol-vlan/frame-type/{frameType}/protocol-type/{protocolType}",
                category="protocol_vlan",
                module="vlan",
                params={"frameType": self.params.get('frame_type', 'ethernet'), "protocolType": self.params.get('protocol_type', 'ip')},
                description=f"刪除協議組 {self.params.get('frame_type', 'ethernet')}/{self.params.get('protocol_type', 'ip')}"
            ),
            
            # 獲取所有接口的協議組配置
            self.create_test_case(
                name="protocol_vlan_get_all_interfaces",
                method="GET",
                url="/api/v1/protocol-vlan/interfaces",
                category="protocol_vlan",
                module="vlan",
                description="獲取所有接口的協議組配置"
            ),
            
            # 映射協議組到VLAN接口
            self.create_test_case(
                name="protocol_vlan_map_interface",
                method="POST",
                url="/api/v1/protocol-vlan/interfaces",
                category="protocol_vlan",
                module="vlan",
                body=self.test_data.get('protocol_vlan_interface', {
                    "ifId": "eth1/1",
                    "groupId": 1,
                    "vlanId": 100
                }),
                description="映射協議組到VLAN接口"
            ),
            
            # 獲取特定接口的協議組配置
            self.create_test_case(
                name="protocol_vlan_get_interface_group",
                method="GET",
                url="/api/v1/protocol-vlan/interfaces/{ifId}/groups/{groupId}",
                category="protocol_vlan",
                module="vlan",
                params={"ifId": self.params.get('interface_id', "eth1/1"), "groupId": self.params.get('group_id', 1)},
                description=f"獲取接口 {self.params.get('interface_id', 'eth1/1')} 協議組 {self.params.get('group_id', 1)} 配置"
            ),
            
            # 更新接口協議組配置
            self.create_test_case(
                name="protocol_vlan_update_interface_group",
                method="PUT",
                url="/api/v1/protocol-vlan/interfaces/{ifId}/groups/{groupId}",
                category="protocol_vlan",
                module="vlan",
                params={"ifId": self.params.get('interface_id', 'eth1/1'), "groupId": self.params.get('group_id', 1)},
                body={"vlanId": 200, "priority": 1},
                description=f"更新接口 {self.params.get('interface_id', 'eth1/1')} 協議組 {self.params.get('group_id', 1)} 配置"
            ),

            # 刪除接口協議組配置
            self.create_test_case(
                name="protocol_vlan_delete_interface_group",
                method="DELETE",
                url="/api/v1/protocol-vlan/interfaces/{ifId}/groups/{groupId}",
                category="protocol_vlan",
                module="vlan",
                params={"ifId": self.params.get('interface_id', 'eth1/1'), "groupId": self.params.get('group_id', 1)},
                description=f"刪除接口 {self.params.get('interface_id', 'eth1/1')} 協議組 {self.params.get('group_id', 1)} 配置"
            )
        ]
    
    def get_mac_vlan_tests(self) -> List[APITestCase]:
        """MAC VLAN API 測試案例"""
        return [
            # 獲取所有MAC VLAN
            self.create_test_case(
                name="mac_vlan_get_all",
                method="GET",
                url="/api/v1/mac-vlan",
                category="mac_vlan",
                module="vlan",
                description="獲取所有MAC VLAN"
            ),
            
            # 添加MAC VLAN條目
            self.create_test_case(
                name="mac_vlan_add_entry",
                method="POST",
                url="/api/v1/mac-vlan",
                category="mac_vlan",
                module="vlan",
                body=self.test_data.get('mac_vlan_entry', {
                    "macAddr": "00-11-22-33-44-55",
                    "mask": "FF-FF-FF-FF-FF-FF",
                    "vlanId": 100
                }),
                description="添加MAC VLAN條目"
            ),
            
            # 獲取特定MAC VLAN條目
            self.create_test_case(
                name="mac_vlan_get_entry",
                method="GET",
                url="/api/v1/mac-vlan/mac-addr/{macAddr}/mask/{mask}",
                category="mac_vlan",
                module="vlan",
                params={"macAddr": self.params.get('mac_address', '00-11-22-33-44-55'), "mask": self.params.get('mac_mask', 'FF-FF-FF-FF-FF-FF')},
                description=f"獲取MAC VLAN條目 {self.params.get('mac_address', '00-11-22-33-44-55')}/{self.params.get('mac_mask', 'FF-FF-FF-FF-FF-FF')}"
            ),
            
            # 更新MAC VLAN條目
            self.create_test_case(
                name="mac_vlan_update_entry",
                method="PUT",
                url="/api/v1/mac-vlan/mac-addr/{macAddr}/mask/{mask}",
                category="mac_vlan",
                module="vlan",
                params={"macAddr": self.params.get('mac_address', '00-11-22-33-44-55'), "mask": self.params.get('mac_mask', 'FF-FF-FF-FF-FF-FF')},
                body=self.test_data.get('mac_vlan_update', {"vlanId": 200}),
                description=f"更新MAC VLAN條目 {self.params.get('mac_address', '00-11-22-33-44-55')}/{self.params.get('mac_mask', 'FF-FF-FF-FF-FF-FF')}"
            ),
            
            # 刪除MAC VLAN條目
            self.create_test_case(
                name="mac_vlan_delete_entry",
                method="DELETE",
                url="/api/v1/mac-vlan/mac-addr/{macAddr}/mask/{mask}",
                category="mac_vlan",
                module="vlan",
                params={"macAddr": self.params.get('mac_address', '00-11-22-33-44-55'), "mask": self.params.get('mac_mask', 'FF-FF-FF-FF-FF-FF')},
                description=f"刪除MAC VLAN條目 {self.params.get('mac_address', '00-11-22-33-44-55')}/{self.params.get('mac_mask', 'FF-FF-FF-FF-FF-FF')}"
            )
        ]
    
    def get_voice_vlan_tests(self) -> List[APITestCase]:
        """Voice VLAN API 測試案例"""
        return [
            # 獲取語音VLAN全局設置
            self.create_test_case(
                name="voice_vlan_get_global_setting",
                method="GET",
                url="/api/v1/voice-vlan",
                category="voice_vlan",
                module="vlan",
                description="獲取語音VLAN全局設置"
            ),
            
            # 配置語音VLAN全局設置
            self.create_test_case(
                name="voice_vlan_configure_global",
                method="PUT",
                url="/api/v1/voice-vlan",
                category="voice_vlan",
                module="vlan",
                body={"vlanId": 1, "status": True},
                description="配置語音VLAN全局設置"
            ),
            
            # 獲取語音VLAN OUI
            self.create_test_case(
                name="voice_vlan_get_oui",
                method="GET",
                url="/api/v1/voice-vlan/oui",
                category="voice_vlan",
                module="vlan",
                description="獲取語音VLAN OUI"
            ),
            
            # 添加OUI條目到語音VLAN
            self.create_test_case(
                name="voice_vlan_add_oui",
                method="POST",
                url="/api/v1/voice-vlan/oui",
                category="voice_vlan",
                module="vlan",
                body=self.test_data.get('voice_vlan_oui', {
                    "macAddr": "00-12-34-56-78-9A",
                    "mask": "FF-FF-FF-00-00-00"
                }),
                description="添加OUI條目到語音VLAN"
            ),
            
            # 獲取特定OUI條目
            self.create_test_case(
                name="voice_vlan_get_oui_entry",
                method="GET",
                url="/api/v1/voice-vlan/oui/mac-addr/{macAddr}/mask/{mask}",
                category="voice_vlan",
                module="vlan",
                params={"macAddr": self.params.get('oui_mac', '00-12-34-56-78-9A'), "mask": self.params.get('oui_mask', 'FF-FF-FF-00-00-00')},
                description=f"獲取OUI條目 {self.params.get('oui_mac', '00-12-34-56-78-9A')}/{self.params.get('oui_mask', 'FF-FF-FF-00-00-00')}"
            ),
            
            # 刪除OUI條目
            self.create_test_case(
                name="voice_vlan_delete_oui_entry",
                method="DELETE",
                url="/api/v1/voice-vlan/oui/mac-addr/{macAddr}/mask/{mask}",
                category="voice_vlan",
                module="vlan",
                params={"macAddr": self.params.get('oui_mac', '00-12-34-56-78-9A'), "mask": self.params.get('oui_mask', 'FF-FF-FF-00-00-00')},
                description=f"刪除OUI條目 {self.params.get('oui_mac', '00-12-34-56-78-9A')}/{self.params.get('oui_mask', 'FF-FF-FF-00-00-00')}"
            ),
            
            # 獲取所有接口的語音VLAN配置
            self.create_test_case(
                name="voice_vlan_get_all_interfaces",
                method="GET",
                url="/api/v1/voice-vlan/interfaces",
                category="voice_vlan",
                module="vlan",
                description="獲取所有接口的語音VLAN配置"
            ),
            
            # 獲取特定接口的語音VLAN配置
            self.create_test_case(
                name="voice_vlan_get_interface",
                method="GET",
                url="/api/v1/voice-vlan/interfaces/{ifId}",
                category="voice_vlan",
                module="vlan",
                params={"ifId": self.params.get('interface_id', 'eth1/1')},
                description=f"獲取接口 {self.params.get('interface_id', 'eth1/1')} 的語音VLAN配置"
            ),
            
            # 配置接口語音VLAN
            self.create_test_case(
                name="voice_vlan_configure_interface",
                method="PUT",
                url="/api/v1/voice-vlan/interfaces/{ifId}",
                category="voice_vlan",
                module="vlan",
                params={"ifId": self.params.get('interface_id', 'eth1/1')},
                body=self.test_data.get('voice_vlan_interface', {
                    "status": True,
                    "mode": "auto"
                }),
                description=f"配置接口 {self.params.get('interface_id', 'eth1/1')} 語音VLAN"
            )
        ]
    
    def get_dot1q_base_tests(self) -> List[APITestCase]:
        """Dot1Q Base API 測試案例"""
        return [
            # 獲取802.1Q基礎配置
            self.create_test_case(
                name="dot1q_base_get_config",
                method="GET",
                url="/api/v1/dot1q-base",
                category="dot1q_base",
                module="vlan",
                description="獲取802.1Q基礎配置"
            ),
            
            # 配置802.1Q基礎設置
            self.create_test_case(
                name="dot1q_base_configure",
                method="PUT",
                url="/api/v1/dot1q-base",
                category="dot1q_base",
                module="vlan",
                body={"gvrpStatus": True},
                description="配置802.1Q基礎設置"
            )
        ]
    
    def get_dot1q_vlan_tests(self) -> List[APITestCase]:
        """Dot1Q VLAN API 測試案例"""
        return [
            # 獲取所有接口的802.1Q VLAN配置
            self.create_test_case(
                name="dot1q_vlan_get_all_interfaces",
                method="GET",
                url="/api/v1/dot1q-vlan/interfaces",
                category="dot1q_vlan",
                module="vlan",
                description="獲取所有接口的802.1Q VLAN配置"
            ),
            
            # 獲取特定接口的802.1Q VLAN配置
            self.create_test_case(
                name="dot1q_vlan_get_interface",
                method="GET",
                url="/api/v1/dot1q-vlan/interfaces/{ifId}",
                category="dot1q_vlan",
                module="vlan",
                params={"ifId": self.params.get('interface_id', 'eth1/1')},
                description=f"獲取接口 {self.params.get('interface_id', 'eth1/1')} 的802.1Q VLAN配置"
            ),
            
            # 配置接口802.1Q VLAN
            self.create_test_case(
                name="dot1q_vlan_configure_interface",
                method="PUT",
                url="/api/v1/dot1q-vlan/interfaces/{ifId}",
                category="dot1q_vlan",
                module="vlan",
                params={"ifId": self.params.get('interface_id', 'eth1/1')},
                body=self.test_data.get('dot1q_vlan_interface', {
                    "pvid": 1,
                    "acceptableFrameTypes": "all",
                    "ingressFiltering": True
                }),
                description=f"配置接口 {self.params.get('interface_id', 'eth1/1')} 802.1Q VLAN"
            )
        ]
    
    def get_dot1d_garp_tests(self) -> List[APITestCase]:
        """Dot1D GARP API 測試案例"""
        return [
            # 獲取所有接口的GARP配置
            self.create_test_case(
                name="dot1d_garp_get_all_interfaces",
                method="GET",
                url="/api/v1/dot1d-garp/interfaces",
                category="dot1d_garp",
                module="vlan",
                description="獲取所有接口的GARP配置"
            ),
            
            # 獲取特定接口的GARP配置
            self.create_test_case(
                name="dot1d_garp_get_interface",
                method="GET",
                url="/api/v1/dot1d-garp/interfaces/{ifId}",
                category="dot1d_garp",
                module="vlan",
                params={"ifId": self.params.get('interface_id', 'eth1/1')},
                description=f"獲取接口 {self.params.get('interface_id', 'eth1/1')} 的GARP配置"
            ),
            
            # 配置接口GARP
            self.create_test_case(
                name="dot1d_garp_configure_interface",
                method="PUT",
                url="/api/v1/dot1d-garp/interfaces/{ifId}",
                category="dot1d_garp",
                module="vlan",
                params={"ifId": self.params.get('interface_id', 'eth1/1')},
                body=self.test_data.get('dot1d_garp_interface', {
                    "joinTime": 200,
                    "leaveTime": 600,
                    "leaveAllTime": 10000
                }),
                description=f"配置接口 {self.params.get('interface_id', 'eth1/1')} GARP"
            )
        ]
    
    def get_vlan_l3_interface_tests(self) -> List[APITestCase]:
        """VLAN L3 Interface API 測試案例"""
        return [
            # 創建VLAN L3接口
            self.create_test_case(
                name="vlan_l3_create_interface",
                method="POST",
                url="/api/v1/interface/vlans",
                category="vlan_l3_interface",
                module="vlan",
                body=self.test_data.get('vlan_l3_interface_create', {
                    "vlanId": 100
                }),
                description="創建VLAN L3接口"
            ),
            
            # 獲取特定VLAN L3接口
            self.create_test_case(
                name="vlan_l3_get_interface",
                method="GET",
                url="/api/v1/interface/vlans/{vlanId}",
                category="vlan_l3_interface",
                module="vlan",
                params={"vlanId": 100},
                description=f"獲取VLAN {self.params.get('vlan_id', 100)} L3接口"
            ),
            
            # 刪除VLAN L3接口
            self.create_test_case(
                name="vlan_l3_delete_interface",
                method="DELETE",
                url="/api/v1/interface/vlans/{vlanId}",
                category="vlan_l3_interface",
                module="vlan",
                params={"vlanId": 100},
                description=f"刪除VLAN {self.params.get('vlan_id', 100)} L3接口"
            ),
        ]