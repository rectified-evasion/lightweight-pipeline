"""Pipeline data representation to pass through the pipeline."""

# Authors: The Lightweight Pipeline developers
# SPDX-License-Identifier: BSD-3-Clause

from abc import ABC


class Pipeline_Data(ABC):
    """Data representation for the pipeline."""

    _config = None

    def __init__(self, config):
        self._config = config

    @property
    def config(self):
        """Configuration of the pipeline."""
        return self._config

    @config.setter
    def config(self, value):
        """Set the configuration of the pipeline."""
        self._config = value