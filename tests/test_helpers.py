"""
Test suite for XBOW scanner modules
"""

import pytest
from src.utils.helpers import (
    is_valid_ip,
    is_valid_cidr,
    is_valid_domain,
    parse_port_range,
    RiskLevel
)


class TestHelpers:
    """Test helper utilities"""
    
    def test_valid_ip(self):
        assert is_valid_ip("192.168.1.1") == True
        assert is_valid_ip("10.0.0.1") == True
        assert is_valid_ip("invalid") == False
    
    def test_valid_cidr(self):
        assert is_valid_cidr("192.168.1.0/24") == True
        assert is_valid_cidr("10.0.0.0/8") == True
        assert is_valid_cidr("invalid/24") == False
    
    def test_parse_port_range(self):
        ports = parse_port_range("80,443,1000-1005")
        assert 80 in ports
        assert 443 in ports
        assert 1000 in ports
        assert 1005 in ports
        assert len(ports) == 8


class TestRiskLevel:
    """Test risk level classification"""
    
    def test_severity_map(self):
        assert RiskLevel.SEVERITY_MAP["CRITICAL"] == 5
        assert RiskLevel.SEVERITY_MAP["HIGH"] == 4
        assert RiskLevel.SEVERITY_MAP["MEDIUM"] == 3


if __name__ == "__main__":
    pytest.main([__file__])
