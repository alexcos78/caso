# -*- coding: utf-8 -*-

# Copyright 2014 Spanish National Research Council (CSIC)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Module containing a No-Op (No Operation) messenger that does nothing."""

from oslo_log import log

import caso.messenger

LOG = log.getLogger(__name__)


class NoopMessenger(caso.messenger.BaseMessenger):
    """Noop messenger that does nothing."""

    def push(self, records):
        """Push records to nowhere."""
        for record in records:
            LOG.info(f"nooping {record.uuid} for record {record.__class__}")
