# SPDX-FileCopyrightText: 2010-2024 Ronny Pfannschmidt <opensource@ronnypfannschmidt.de>
# SPDX-FileCopyrightText: 2024-present Fabien Hermitte
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import os


def read_dist_name_from_setup_cfg(
    input_value: str | os.PathLike[str] = "setup.cfg",
) -> str | None:
    # minimal effort to read dist_name off setup.cfg metadata
    import configparser

    parser = configparser.ConfigParser()
    parser.read([input_value], encoding="utf-8")
    return parser.get("metadata", "name", fallback=None)
