#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sqlalchemy.ext import declarative
import testtools

from neutron.db import standard_attr
from neutron.tests import base
from neutron.tests.unit import testlib_api


class StandardAttrTestCase(base.BaseTestCase):

    def _make_decl_base(self):
        # construct a new base so we don't interfere with the main
        # base used in the sql test fixtures
        return declarative.declarative_base(
            cls=standard_attr.model_base.NeutronBaseV2)

    def test_standard_attr_resource_model_map(self):
        rs_map = standard_attr.get_standard_attr_resource_model_map()
        base = self._make_decl_base()

        class MyModel(standard_attr.HasStandardAttributes,
                      standard_attr.model_base.HasId,
                      base):
            api_collections = ['my_resource', 'my_resource2']

        rs_map = standard_attr.get_standard_attr_resource_model_map()
        self.assertEqual(MyModel, rs_map['my_resource'])
        self.assertEqual(MyModel, rs_map['my_resource2'])

        class Dup(standard_attr.HasStandardAttributes,
                  standard_attr.model_base.HasId,
                  base):
            api_collections = ['my_resource']

        with testtools.ExpectedException(RuntimeError):
            standard_attr.get_standard_attr_resource_model_map()


class StandardAttrAPIImapctTestCase(testlib_api.SqlTestCase):
    """Test case to determine if a resource has had new fields exposed."""

    def test_api_collections_are_expected(self):
        # NOTE to reviewers. If this test is being modified, it means the
        # resources being extended by standard attr extensions have changed.
        # Ensure that the patch has made this discoverable to API users.
        # This means a new extension for a new resource or a new extension
        # indicating that an existing resource now has standard attributes.
        # Ensure devref list of resources is updated at
        # doc/source/devref/api_extensions.rst
        expected = ['subnets', 'trunks', 'routers', 'segments',
                    'security_group_rules', 'networks', 'policies',
                    'subnetpools', 'ports', 'security_groups', 'floatingips']
        self.assertEqual(
            set(expected),
            set(standard_attr.get_standard_attr_resource_model_map().keys())
        )
