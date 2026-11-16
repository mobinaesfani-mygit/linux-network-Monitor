"""
Network monitoring module.

This module checks TCP port availability using asyncio.
It handles connection errors and records monitoring results.
"""

import asyncio
import socket
import time

from config import (
    TARGET_HOST,
    TARGET_PORTS,
    CONNECTION_TIMEOUT,
    MONITOR_INTERVAL,
    MAX_CONCURRENT_CHECKS,
)
from logger import setup_logger


logger = setup_logger()

semaphore = asyncio.Semaphore(MAX_CONCURRENT_CHECKS)


async def check_port(host, port, timeout=CONNECTION_TIMEOUT):
    """
    Check if a TCP port is reachable.

    Args:
        host: Target server hostname or IP address.
        port: TCP port number to check.
        timeout: Maximum connection time in seconds.

    Returns:
        dict: Connection status and response time.
    """

    start_time = time.perf_counter()
    writer = None

    result = {
        "host": host,
        "port": port,
        "status": None,
        "response_time_ms": None,
        "error": None,
    }

    try:
        async with semaphore:
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=timeout,
            )

        result["status"] = "ONLINE"

    except asyncio.CancelledError:
        raise

    except TimeoutError as error:
        result["status"] = "TIMEOUT"
        result["error"] = str(error) or "Connection timed out"

    except socket.gaierror as error:
        result["status"] = "DNS_ERROR"
        result["error"] = str(error)

    except ConnectionRefusedError as error:
        result["status"] = "REFUSED"
        result["error"] = str(error)

    except OSError as error:
        result["status"] = "NETWORK_ERROR"
        result["error"] = str(error)

    finally:
        if writer is not None:
            writer.close()

            try:
                await writer.wait_closed()
            except OSError:
                pass

        result["response_time_ms"] = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

    logger.info(
        "Port check completed",
        extra=result,
    )

    return result


async def run_monitoring():
    """
    Check all configured ports concurrently.

    Returns:
        list: Results of all port checks.
    """

    tasks = [
        check_port(TARGET_HOST, port)
        for port in TARGET_PORTS
    ]

    results = await asyncio.gather(*tasks)

    return results


async def monitor_loop():
    """
    Run network monitoring repeatedly.

    The program waits for MONITOR_INTERVAL seconds
    after each monitoring cycle.
    """

    logger.info("Network monitor started")

    try:
        while True:
            await run_monitoring()
            await asyncio.sleep(MONITOR_INTERVAL)

    except asyncio.CancelledError:
        logger.info("Network monitor stopped")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(monitor_loop())

    except KeyboardInterrupt:
        print("Network monitor stopped by user.")