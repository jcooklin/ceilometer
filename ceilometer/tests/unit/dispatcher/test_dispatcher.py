# Copyright 2015 Intel Corp.
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

from oslo_config import fixture
from oslotest import mockpatch

from ceilometer import dispatcher
from ceilometer.tests import base


class FakeMeterDispatcher(dispatcher.MeterDispatcherBase):
    def record_metering_data(self, data):
        pass


class FakeEventDispatcher(dispatcher.EventDispatcherBase):
    def record_events(self, events):
        pass


class TestDispatchManager(base.BaseTestCase):
    def setUp(self):
        super(TestDispatchManager, self).setUp()
        self.conf = self.useFixture(fixture.Config())
        self.conf.config(meter_dispatchers=['database', 'gnocchi'],
                         event_dispatchers=['database'])
        self.CONF = self.conf.conf
        self.useFixture(mockpatch.Patch(
            'ceilometer.dispatcher.gnocchi.GnocchiDispatcher',
            new=FakeMeterDispatcher))
        self.useFixture(mockpatch.Patch(
            'ceilometer.dispatcher.database.MeterDatabaseDispatcher',
            new=FakeMeterDispatcher))
        self.useFixture(mockpatch.Patch(
            'ceilometer.dispatcher.database.EventDatabaseDispatcher',
            new=FakeEventDispatcher))

    def test_load(self):
        sample_mg, event_mg = dispatcher.load_dispatcher_manager(self.CONF)
        self.assertEqual(2, len(list(sample_mg)))
        self.assertEqual(1, len(list(event_mg)))
