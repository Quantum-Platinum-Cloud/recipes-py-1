# Copyright 2020 The LUCI Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

from PB.recipe_modules.recipe_engine.cas import properties

DEPS = [
    'cipd',
    'path',
    'properties',
    'raw_io',
    'runtime',
    'step',
]

PROPERTIES = properties.InputProperties
