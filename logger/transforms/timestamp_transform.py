#!/usr/bin/env python3
"""Prepend a timestamp to a text record.
"""

import sys
sys.path.append('.')

from logger.utils import formats
from logger.utils import timestamp

from logger.transforms.transform import Transform

################################################################################
# If timestamp_format is not specified, use default format
class TimestampTransform(Transform):
  def __init__(self, time_format=timestamp.TIME_FORMAT):
    super().__init__(input_format=formats.Text, output_format=formats.Text)
    self.time_format = time_format

  
  # Prepend a timestamp
  def transform(self, record):
    if record is None:
      return None
    return timestamp.time_str(time_format=self.time_format) + ' ' + record