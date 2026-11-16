import asyncio
import socket
from unittest.mock import AsyncMock,MagicMock, patch

import monitor


def test_check_port_online():
    """Test a successful TCP connection."""

    async def run_test():
        mock_writer = MagicMock()
        mock_writer.wait_closed = AsyncMock()

        with patch(
            "monitor.asyncio.open_connection",
            new=AsyncMock(return_value=(None, mock_writer)),
        ):
            result = await monitor.check_port("127.0.0.1", 443)

        assert result["status"] == "ONLINE"
        assert result["host"] == "127.0.0.1"
        assert result["port"] == 443
        assert result["response_time_ms"] is not None
        assert result["error"] is None

        mock_writer.close.assert_called_once()
        mock_writer.wait_closed.assert_awaited_once()

    asyncio.run(run_test())


def test_check_port_refused():
    """Test a connection refused error."""

    async def run_test():
        with patch(
            "monitor.asyncio.open_connection",
            new=AsyncMock(
                side_effect=ConnectionRefusedError("Connection refused")
            ),
        ):
            result = await monitor.check_port("127.0.0.1", 80)

        assert result["status"] == "REFUSED"
        assert result["error"] == "Connection refused"

    asyncio.run(run_test())


def test_check_port_timeout():
    """Test a connection timeout."""

    async def run_test():
        with patch(
            "monitor.asyncio.open_connection",
            new=AsyncMock(side_effect=TimeoutError),
        ):
            result = await monitor.check_port(
                "127.0.0.1",
                443,
                timeout=1,
            )

        assert result["status"] == "TIMEOUT"
        assert result["error"] == "Connection timed out"

    asyncio.run(run_test())


def test_check_port_dns_error():
    """Test a DNS resolution error."""

    async def run_test():
        dns_error = socket.gaierror("Name or service not known")

        with patch(
            "monitor.asyncio.open_connection",
            new=AsyncMock(side_effect=dns_error),
        ):
            result = await monitor.check_port("invalid-host", 80)

        assert result["status"] == "DNS_ERROR"
        assert result["error"] == str(dns_error)

    asyncio.run(run_test())


def test_run_monitoring():
    """Test that all configured ports are checked."""

    async def run_test():
        expected_ports = monitor.TARGET_PORTS

        with patch(
            "monitor.check_port",
            new_callable=AsyncMock,
        ) as mock_check:

            mock_check.return_value = {"status": "ONLINE"}

            results = await monitor.run_monitoring()

        assert mock_check.call_count == len(expected_ports)
        assert len(results) == len(expected_ports)

    asyncio.run(run_test())