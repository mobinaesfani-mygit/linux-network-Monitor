import json
import logging

import logger as logger_module


def test_json_formatter():
    """Test that log records are formatted as JSON."""

    formatter = logger_module.JsonFormatter()

    record = logging.LogRecord(
        name="network_monitor",
        level=logging.INFO,
        pathname="test.py",
        lineno=10,
        msg="Port check completed",
        args=(),
        exc_info=None,
    )

    record.host = "127.0.0.1"
    record.port = 443
    record.status = "ONLINE"
    record.response_time_ms = 12.5
    record.error = None

    result = formatter.format(record)
    data = json.loads(result)

    assert data["level"] == "INFO"
    assert data["message"] == "Port check completed"
    assert data["host"] == "127.0.0.1"
    assert data["port"] == 443
    assert data["status"] == "ONLINE"
    assert data["response_time_ms"] == 12.5
    assert data["error"] is None
    assert "timestamp" in data


def test_setup_logger_writes_to_file(tmp_path, monkeypatch):
    """Test that the logger writes JSON messages to a file."""

    log_file = tmp_path / "test.log"

    monkeypatch.setattr(
        logger_module,
        "LOG_FILE",
        str(log_file),
    )

    test_logger = logging.getLogger("network_monitor")

    # Remove old handlers before configuring the logger
    old_handlers = test_logger.handlers[:]

    for handler in old_handlers:
        test_logger.removeHandler(handler)
        handler.close()

    try:
        test_logger = logger_module.setup_logger()

        test_logger.info(
            "Test event",
            extra={
                "host": "127.0.0.1",
                "port": 80,
                "status": "ONLINE",
                "response_time_ms": 5.2,
            },
        )

        content = log_file.read_text(encoding="utf-8")
        data = json.loads(content.strip())

        assert data["message"] == "Test event"
        assert data["host"] == "127.0.0.1"
        assert data["port"] == 80
        assert data["status"] == "ONLINE"

    finally:
        for handler in test_logger.handlers[:]:
            test_logger.removeHandler(handler)
            handler.close()