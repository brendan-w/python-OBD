
import pytest


def pytest_addoption(parser):
    parser.addoption("--port", action="store", default=None,
                     help="device file for doing end-to-end testing")
