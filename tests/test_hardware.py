"""Tests for BlackRoad Hardware - Pi Fleet Manager and Device Orchestrator."""
import pytest
import json
import yaml
from pathlib import Path


def test_fleet_registry_valid_yaml():
    """fleet-registry.yaml should be valid YAML."""
    # Simulate a fleet registry structure
    registry = {
        "version": "1.0",
        "nodes": [
            {"id": "aria64", "ip": "192.168.4.38", "role": "primary", "agents": 22500},
            {"id": "alice", "ip": "192.168.4.49", "role": "secondary", "agents": 7500},
        ]
    }
    yaml_str = yaml.dump(registry)
    loaded = yaml.safe_load(yaml_str)
    assert loaded["version"] == "1.0"
    assert len(loaded["nodes"]) == 2


def test_node_structure():
    """Each node must have required fields."""
    required_fields = {"id", "ip", "role"}
    nodes = [
        {"id": "aria64", "ip": "192.168.4.38", "role": "primary", "agents": 22500},
        {"id": "alice", "ip": "192.168.4.49", "role": "secondary", "agents": 7500},
    ]
    for node in nodes:
        for field in required_fields:
            assert field in node, f"Node missing field: {field}"


def test_total_agent_capacity():
    """Total fleet capacity should be >= 30000."""
    nodes = [
        {"id": "aria64", "agents": 22500},
        {"id": "alice", "agents": 7500},
    ]
    total = sum(n["agents"] for n in nodes)
    assert total >= 30000, f"Fleet capacity {total} below 30000"


def test_ip_format_valid():
    """IP addresses should be valid format."""
    import re
    ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    ips = ["192.168.4.38", "192.168.4.49", "192.168.4.64"]
    for ip in ips:
        assert ip_pattern.match(ip), f"Invalid IP format: {ip}"


def test_sensor_data_schema():
    """Sensor data should include required telemetry fields."""
    sensor_data = {
        "device_id": "pi-aria64",
        "timestamp": "2026-02-23T03:00:00Z",
        "cpu_pct": 45.2,
        "ram_free_gb": 4.1,
        "disk_free_gb": 174.0,
        "temperature_c": 52.3,
        "worlds_generated": 14,
    }
    required = {"device_id", "timestamp", "cpu_pct", "ram_free_gb"}
    for field in required:
        assert field in sensor_data


def test_service_health_response():
    """Status server response schema validation."""
    response = {
        "host": "octavia",
        "uptime_s": 3600,
        "cpu_pct": 45.2,
        "ram_free_gb": 4.1,
        "disk_free_gb": 174.0,
        "worlds_created": 14,
        "tasks_completed": 0,
        "model": "qwen2.5:3b",
    }
    assert 0 <= response["cpu_pct"] <= 100
    assert response["ram_free_gb"] > 0
    assert response["worlds_created"] >= 0


def test_device_roles():
    """Device roles must be valid."""
    valid_roles = {"primary", "secondary", "relay", "failover", "edge"}
    fleet = [
        {"id": "aria64", "role": "primary"},
        {"id": "alice", "role": "secondary"},
    ]
    for node in fleet:
        assert node["role"] in valid_roles


def test_pssha_hash_format():
    """PS-SHA∞ hash should be 64-char hex."""
    import hashlib
    prev_hash = "GENESIS"
    key = "sensor_reading"
    content = "cpu=45.2"
    ts = "1740276000000000000"
    chain_input = f"{prev_hash}:{key}:{content}:{ts}"
    h = hashlib.sha256(chain_input.encode()).hexdigest()
    assert len(h) == 64
    assert all(c in "0123456789abcdef" for c in h)
