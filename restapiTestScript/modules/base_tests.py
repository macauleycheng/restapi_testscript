#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基礎測試類，所有模組測試類的父類
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

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
    query_params: Optional[Dict[str, Any]] = None

class BaseTests(ABC):
    """所有測試模組的基礎類"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.params = config.get('test_parameters', {})
        self.test_data = config.get('test_data', {})
    
    @abstractmethod
    def get_all_tests(self) -> List[APITestCase]:
        """獲取所有測試案例"""
        pass
    
    @abstractmethod
    def get_categories(self) -> List[str]:
        """獲取模組支援的類別"""
        pass
    
    def create_test_case(self, name: str, method: str, url: str, category: str, 
                        module: str, description: str = "", params: Dict = None, query_params: Dict = None,
                        body: Dict = None, expected_status: int = 200) -> APITestCase:
        """創建測試案例的輔助方法"""
        return APITestCase(
            name=name,
            method=method,
            url=url,
            headers={},
            params=params,
            body=body,
            expected_status=expected_status,
            description=description,
            category=category,
            module=module,
            query_params=query_params
        )