"""
Backward-compatible entry point for the courtroom simulation engine.

All logic lives in the ``courtroom_core`` package; import from there in new code.
"""

from __future__ import annotations

from courtroom_core import *  # noqa: F403
from courtroom_core import __all__
