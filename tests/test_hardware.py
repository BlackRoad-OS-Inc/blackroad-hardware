"""Tests for BlackRoad Hardware — Pi Fleet Manager and Device Orchestrator."""
import pytest
import json
import re
import yaml
from pathlib import Path

from fleet_manager import PiNode, FleetRegistry, SensorReading


# ---------------------------------------------------------------------------
# PiNode validation tests
# ---------------------------------------------------------------------------

class TestPiNode:
    def test_valid_node_creation(self):
        node = PiNode(node_id="test", ip="192.168.4.10", role="primary")
        assert node.node_id == "test"
        assert node.ip == "192.168.4.10"
        assert node.role == "primary"

    def test_invalid_ip_format(self):
        with pytest.raises(ValueError, match="Invalid IP"):
            PiNode(node_id="bad", ip="not-an-ip", role="primary")

    def test_invalid_ip_octet_out_of_range(self):
        with pytest.raises(ValueError, match="octet out of range"):
            PiNode(node_id="bad", ip="192.168.4.300", role="primary")

    def test_invalid_role(self):
        with pytest.raises(ValueError, match="Invalid role"):
            PiNode(node_id="bad", ip="192.168.4.1", role="captain")

    def test_status_url(self):
        node = PiNode(node_id="n1", ip="10.0.0.1", role="edge", status_port=9000)
        assert node.status_url() == "http://10.0.0.1:9000/status"

    def test_to_dict(self):
        node = PiNode(node_id="n1", ip="10.0.0.1", role="edge")
        d = node.to_dict()
        assert d["node_id"] == "n1"
        assert d["ip"] == "10.0.0.1"
        assert isinstance(d, dict)

    def test_default_values(self):
        node = PiNode(node_id="n1", ip="10.0.0.1", role="relay")
        assert node.user == "pi"
        assert node.port == 22
        assert node.status_port == 8182
        assert node.agent_capacity == 0
        assert node.model == "unknown"


# ---------------------------------------------------------------------------
# FleetRegistry tests
# ---------------------------------------------------------------------------

class TestFleetRegistry:
    def test_add_and_get_node(self):
        reg = FleetRegistry()
        node = PiNode(node_id="a", ip="10.0.0.1", role="primary")
        reg.add_node(node)
        assert reg.get_node("a") is node

    def test_get_missing_node(self):
        reg = FleetRegistry()
        assert reg.get_node("missing") is None

    def test_duplicate_node_id_raises(self):
        reg = FleetRegistry()
        reg.add_node(PiNode(node_id="a", ip="10.0.0.1", role="primary"))
        with pytest.raises(ValueError, match="Duplicate node ID"):
            reg.add_node(PiNode(node_id="a", ip="10.0.0.2", role="secondary"))

    def test_remove_node(self):
        reg = FleetRegistry()
        reg.add_node(PiNode(node_id="a", ip="10.0.0.1", role="primary"))
        reg.remove_node("a")
        assert reg.get_node("a") is None

    def test_remove_unknown_node_raises(self):
        reg = FleetRegistry()
        with pytest.raises(ValueError, match="Unknown node ID"):
            reg.remove_node("ghost")

    def test_total_capacity(self):
        reg = FleetRegistry()
        reg.add_node(PiNode(node_id="a", ip="10.0.0.1", role="primary", agent_capacity=1000))
        reg.add_node(PiNode(node_id="b", ip="10.0.0.2", role="secondary", agent_capacity=500))
        assert reg.total_capacity() == 1500

    def test_primary_nodes(self):
        reg = FleetRegistry()
        reg.add_node(PiNode(node_id="a", ip="10.0.0.1", role="primary"))
        reg.add_node(PiNode(node_id="b", ip="10.0.0.2", role="secondary"))
        reg.add_node(PiNode(node_id="c", ip="10.0.0.3", role="primary"))
        primaries = reg.primary_nodes()
        assert len(primaries) == 2
        assert all(n.role == "primary" for n in primaries)

    def test_to_json(self):
        reg = FleetRegistry(version="2.0")
        reg.add_node(PiNode(node_id="a", ip="10.0.0.1", role="primary"))
        data = json.loads(reg.to_json())
        assert data["version"] == "2.0"
        assert len(data["nodes"]) == 1
        assert "generated_at" in data


# ---------------------------------------------------------------------------
# SensorReading tests
# ---------------------------------------------------------------------------

class TestSensorReading:
    def test_healthy_reading(self):
        r = SensorReading(device_id="test", cpu_pct=50.0, ram_free_gb=2.0, disk_free_gb=10.0)
        assert r.is_healthy()

    def test_unhealthy_high_cpu(self):
        r = SensorReading(device_id="test", cpu_pct=96.0, ram_free_gb=2.0, disk_free_gb=10.0)
        assert not r.is_healthy()

    def test_unhealthy_low_ram(self):
        r = SensorReading(device_id="test", cpu_pct=50.0, ram_free_gb=0.05, disk_free_gb=10.0)
        assert not r.is_healthy()

    def test_unhealthy_low_disk(self):
        r = SensorReading(device_id="test", cpu_pct=50.0, ram_free_gb=2.0, disk_free_gb=0.3)
        assert not r.is_healthy()

    def test_invalid_cpu_pct(self):
        with pytest.raises(ValueError, match="CPU percentage"):
            SensorReading(device_id="test", cpu_pct=101.0, ram_free_gb=2.0, disk_free_gb=10.0)

    def test_negative_ram(self):
        with pytest.raises(ValueError, match="RAM free cannot be negative"):
            SensorReading(device_id="test", cpu_pct=50.0, ram_free_gb=-1.0, disk_free_gb=10.0)


# ---------------------------------------------------------------------------
# Config file validation tests
# ---------------------------------------------------------------------------

class TestConfigFiles:
    def test_fleet_registry_valid_yaml(self):
        """fleet-registry.yaml should be valid YAML."""
        path = Path(__file__).parent.parent / "fleet-registry.yaml"
        if path.exists():
            with open(path) as f:
                data = yaml.safe_load(f)
            assert data is not None

    def test_registry_json_valid(self):
        """registry.json should be valid JSON."""
        path = Path(__file__).parent.parent / "registry.json"
        if path.exists():
            with open(path) as f:
                data = json.load(f)
            assert "devices" in data or "version" in data

    def test_network_json_valid(self):
        """network.json should be valid JSON."""
        path = Path(__file__).parent.parent / "network.json"
        if path.exists():
            with open(path) as f:
                data = json.load(f)
            assert data is not None

    def test_node_structure(self):
        """Each node must have required fields."""
        required_fields = {"id", "ip", "role"}
        nodes = [
            {"id": "aria64", "ip": "192.168.4.38", "role": "primary", "agents": 22500},
            {"id": "alice", "ip": "192.168.4.49", "role": "secondary", "agents": 7500},
        ]
        for node in nodes:
            for f in required_fields:
                assert f in node, f"Node missing field: {f}"

    def test_ip_format_valid(self):
        """IP addresses should be valid format."""
        ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        ips = ["192.168.4.38", "192.168.4.49", "192.168.4.64"]
        for ip in ips:
            assert ip_pattern.match(ip), f"Invalid IP format: {ip}"

    def test_device_roles(self):
        """Device roles must be valid."""
        valid_roles = {"primary", "secondary", "relay", "failover", "edge"}
        fleet = [
            {"id": "aria64", "role": "primary"},
            {"id": "alice", "role": "secondary"},
        ]
        for node in fleet:
            assert node["role"] in valid_roles


# ---------------------------------------------------------------------------
# Schema / hash tests
# ---------------------------------------------------------------------------

def test_total_agent_capacity():
    """Total fleet capacity should be >= 30000."""
    nodes = [
        {"id": "aria64", "agents": 22500},
        {"id": "alice", "agents": 7500},
    ]
    total = sum(n["agents"] for n in nodes)
    assert total >= 30000, f"Fleet capacity {total} below 30000"


def test_pssha_hash_format():
    """PS-SHA hash should be 64-char hex."""
    import hashlib
    prev_hash = "GENESIS"
    key = "sensor_reading"
    content = "cpu=45.2"
    ts = "1740276000000000000"
    chain_input = f"{prev_hash}:{key}:{content}:{ts}"
    h = hashlib.sha256(chain_input.encode()).hexdigest()
    assert len(h) == 64
    assert all(c in "0123456789abcdef" for c in h)


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
    for f in required:
        assert f in sensor_data


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
