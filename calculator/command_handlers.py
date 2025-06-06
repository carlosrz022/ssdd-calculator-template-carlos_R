"""Module containing the handler functions for CLI commands."""

import logging
import os
import sys

from calculator.server import Server


def calculator() -> None:
    """Handle for running the server for remote calculator."""
    logging.basicConfig(level=logging.DEBUG)

    cmd_name = os.path.basename(sys.argv[0])

    logger = logging.getLogger(cmd_name)
    logger.info("Running calculator server...")

    server = Server()
    sys.exit(server.main(sys.argv))


def kafka_worker() -> None:
    """Handle for running the Kafka worker for remote calculator."""
    logging.basicConfig(level=logging.DEBUG)

    cmd_name = os.path.basename(sys.argv[0])

    logger = logging.getLogger(cmd_name)
    logger.info("Running Kafka worker...")

    # Import dentro de la función para evitar dependencias circulares
    from calculator.kafka_worker import main  # pylint: disable=import-outside-toplevel
    sys.exit(main())

