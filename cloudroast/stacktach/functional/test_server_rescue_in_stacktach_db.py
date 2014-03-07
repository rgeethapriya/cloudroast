"""
Copyright 2014 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from cloudroast.stacktach.fixtures import StackTachComputeIntegration,\
    StackTachTestAssertionsFixture


class StackTachDBRescueServerTests(StackTachComputeIntegration,
                                   StackTachTestAssertionsFixture):
    """
    @summary: With Server Rescue, tests the entries created in StackTach DB.
    """

    @classmethod
    def setUpClass(cls):
        cls.create_and_rescue_server()
        cls.stacktach_events_for_server(cls.rescued_server)
        cls.event_launch_rescued_server = cls.event_launches[1]

    def test_launch_entry_on_rescue_server_response(self):
        """
        Verify the Launch parameters are being returned in the
        Server Rescue response
        """
        self.validate_attributes_in_launch_response(num_of_launch_entry=2)

    def test_launch_entry_fields_on_create_server(self):
        """
        Verify that the first Launch entry will have all expected fields
        after a Server Rescue
        """
        self.validate_launch_entry_field_values(server=self.rescued_server)

    def test_launch_entry_fields_on_rescue(self):
        """
        Verify that the second Launch entry will have all expected fields
        after a Server Rescue
        """
        self.validate_launch_entry_field_values(
            server=self.rescued_server,
            event_launch_server=self.event_launch_rescued_server,
            launched_at=self.launched_at_rescued_server)

    def test_exist_entry_on_rescue(self):
        """
        Verify the Exist parameters are correct after a Server Rescue
        """
        self.validate_attributes_in_exist_response()

    def test_exists_entry_fields_on_rescue_server_response(self):
        """
        Verify that the Exist entry will have all expected fields
        after Server Rescue
        """
        self.validate_exist_entry_field_values(server=self.rescued_server)

    def test_exist_launched_at_field_match_on_rescue(self):
        """
        Verify that the Exists entry launched_at matches the
        Launch entry launched_at for a Server Rescue
        """
        self.assertEqual(self.event_launch.launched_at,
                         self.event_exist.launched_at,
                         self.msg.format(
                             "launched_at",
                             self.event_launch.launched_at,
                             self.event_exist.launched_at,
                             self.exist_response.reason,
                             self.exist_response.content))

    def test_no_delete_entry_on_rescue_server_response(self):
        """Verify that there is no delete entry after a Server Rescue"""
        self.validate_no_deletes_entry_returned()
