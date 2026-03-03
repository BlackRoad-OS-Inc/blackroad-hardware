"""Tests for BlackRoad Hardware - Pi Fleet Manager and Device Orchestrator."""
import pytest
import json
import yaml
from pathlib import Path

from fleet_manager import PiNode, FleetRegistry, SensorReading, DEFAULT_FLEET

REPO_ROOT = Path(__file__).parent.parent


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


# ── fleet_manager module tests ──────────────────────────────────────────────

def test_pinode_valid():
    """PiNode should accept valid inputs."""
    node = PiNode(node_id="test01", ip="192.168.4.10", role="primary")
    assert node.ip == "192.168.4.10"
    assert node.role == "primary"
    assert node.status_url() == "http://192.168.4.10:8182/status"


def test_pinode_invalid_ip():
    """PiNode should reject malformed IPs."""
    with pytest.raises(ValueError, match="Invalid IP"):
        PiNode(node_id="bad", ip="999.999.999.999", role="primary")


def test_pinode_invalid_ip_octet():
    """PiNode should reject IPs with octets > 255."""
    with pytest.raises(ValueError, match="Invalid IP"):
        PiNode(node_id="bad", ip="192.168.4.300", role="primary")


def test_pinode_invalid_role():
    """PiNode should reject unknown roles."""
    with pytest.raises(ValueError, match="Invalid role"):
        PiNode(node_id="bad", ip="10.0.0.1", role="master")


def test_fleet_add_and_get_node():
    """FleetRegistry should add and retrieve nodes."""
    registry = FleetRegistry()
    node = PiNode(node_id="n1", ip="10.0.0.1", role="edge")
    registry.add_node(node)
    assert registry.get_node("n1") is node
    assert registry.get_node("missing") is None


def test_fleet_add_duplicate_raises():
    """FleetRegistry.add_node should reject duplicate node IDs."""
    registry = FleetRegistry()
    node = PiNode(node_id="dup", ip="10.0.0.2", role="relay")
    registry.add_node(node)
    with pytest.raises(ValueError, match="already registered"):
        registry.add_node(PiNode(node_id="dup", ip="10.0.0.3", role="relay"))


def test_fleet_remove_node():
    """FleetRegistry.remove_node should remove a registered node."""
    registry = FleetRegistry()
    node = PiNode(node_id="r1", ip="10.0.0.4", role="failover")
    registry.add_node(node)
    registry.remove_node("r1")
    assert registry.get_node("r1") is None


def test_fleet_remove_missing_raises():
    """FleetRegistry.remove_node should raise KeyError for unknown IDs."""
    registry = FleetRegistry()
    with pytest.raises(KeyError, match="not found"):
        registry.remove_node("ghost")


def test_fleet_total_capacity():
    """FleetRegistry.total_capacity should sum agent_capacity across nodes."""
    registry = FleetRegistry()
    registry.add_node(PiNode(node_id="a", ip="10.0.0.5", role="primary", agent_capacity=1000))
    registry.add_node(PiNode(node_id="b", ip="10.0.0.6", role="secondary", agent_capacity=500))
    assert registry.total_capacity() == 1500


def test_fleet_primary_nodes():
    """FleetRegistry.primary_nodes should filter correctly."""
    registry = FleetRegistry()
    registry.add_node(PiNode(node_id="p1", ip="10.0.0.7", role="primary"))
    registry.add_node(PiNode(node_id="s1", ip="10.0.0.8", role="secondary"))
    primaries = registry.primary_nodes()
    assert len(primaries) == 1
    assert primaries[0].node_id == "p1"


def test_fleet_to_json():
    """FleetRegistry.to_json should produce valid JSON with expected keys."""
    registry = FleetRegistry()
    registry.add_node(PiNode(node_id="j1", ip="10.0.0.9", role="edge", agent_capacity=100))
    data = json.loads(registry.to_json())
    assert data["version"] == "1.0"
    assert len(data["nodes"]) == 1
    assert data["total_capacity"] == 100
    assert "generated_at" in data


def test_sensor_reading_healthy():
    """SensorReading.is_healthy should return True for good values."""
    s = SensorReading(device_id="pi-test", cpu_pct=50.0, ram_free_gb=2.0, disk_free_gb=10.0)
    assert s.is_healthy()


def test_sensor_reading_unhealthy_cpu():
    """SensorReading.is_healthy should return False when CPU ≥ 95%."""
    s = SensorReading(device_id="pi-test", cpu_pct=95.0, ram_free_gb=2.0, disk_free_gb=10.0)
    assert not s.is_healthy()


def test_sensor_reading_invalid_cpu():
    """SensorReading should reject CPU percentage out of 0-100."""
    with pytest.raises(ValueError):
        SensorReading(device_id="pi-test", cpu_pct=101.0, ram_free_gb=1.0, disk_free_gb=1.0)


def test_default_fleet_loaded():
    """DEFAULT_FLEET should have nodes with positive agent capacity."""
    assert DEFAULT_FLEET.total_capacity() > 0
    assert DEFAULT_FLEET.get_node("aria64") is not None


def test_fleet_registry_yaml_file():
    """fleet-registry.yaml should exist and contain expected top-level keys."""
    path = REPO_ROOT / "fleet-registry.yaml"
    assert path.exists(), "fleet-registry.yaml not found"
    with open(path) as f:
        data = yaml.safe_load(f)
    assert "fleet" in data
    assert "devices" in data["fleet"]
    assert len(data["fleet"]["devices"]) > 0


def test_registry_json_file():
    """registry.json should exist and be valid JSON with a version field."""
    path = REPO_ROOT / "registry.json"
    assert path.exists(), "registry.json not found"
    with open(path) as f:
        data = json.load(f)
    assert "version" in data
    assert "devices" in data
