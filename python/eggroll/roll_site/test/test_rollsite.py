#
#  Copyright 2019 The Eggroll Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import unittest

from eggroll.roll_pair.roll_pair import RollPair
from eggroll.roll_pair.test.roll_pair_test_assets import get_debug_test_context
from eggroll.roll_site.roll_site import RollSiteContext

rp_context = get_debug_test_context(False)
options = {'runtime_conf_path': 'python/eggroll/roll_site/conf/role_conf.json',
           'server_conf_path': 'python/eggroll/roll_site/conf/server_conf.json',
           'transfer_conf_path': 'python/eggroll/roll_site/conf/transfer_conf.json'}


class TestRollSite(unittest.TestCase):
    def test_remote(self):
        context = RollSiteContext("atest", options=options, rp_ctx=rp_context)
        _tag = "Hello2"
        rs = context.load(name="RsaIntersectTransferVariable.rsa_pubkey", tag="{}".format(_tag))
        fp = open("testA.model", 'r')
        obj = fp.read(35)
        parties = [('host', '10002')]
        futures = rs.push(obj, parties)
        fp.close()
        for future in futures:
            role, party = future.result()
            print("result:", role, party)

    def test_get(self):
        context = RollSiteContext("atest", options=options, rp_ctx=rp_context)
        _tag = "Hello2"
        rs = context.load(name="RsaIntersectTransferVariable.rsa_pubkey", tag="{}".format(_tag))
        parties = [('host', '10002')]
        futures = rs.pull(parties)
        for future in futures:
            obj = future.result()
            if isinstance(obj, RollPair):
                key = 'hello'
                print("obj:", obj.get(key))
            else:
                print("obj:", obj)

    def test_remote_rollpair(self):
        data = [("k1", "v1"), ("k2", "v2"), ("k3", "v3"), ("k4", "v4"), ("k5", "v5"), ("k6", "v6")]
        context = RollSiteContext("atest2", options=options, rp_ctx=rp_context)
        rp_options = {'include_key': True}
        rp = rp_context.load("namespace", "name").put_all(data, options=rp_options)
        _tag = "Hello"
        rs = context.load(name="roll_pair_name.table", tag="roll_pair_tag")
        parties = [('host', '10002')]
        futures = rs.push(rp, parties)
        for future in futures:
            role, party = future.result()
            print("result:", role, party)

    def test_get_rollpair(self):
        context = RollSiteContext("atest2", options=options, rp_ctx=rp_context)

        _tag = "roll_pair_tag"

        rs = context.load(name="roll_pair_name.table", tag="{}".format(_tag))
        parties = [('host', '10002')]
        futures = rs.pull(parties)
        for future in futures:
            obj = future.result()
            if isinstance(obj, RollPair):
                key = "k1"
                print("obj:", obj.get(key))
            else:
                print("obj:", obj)