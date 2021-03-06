#!/usr/bin/python
import unittest

import blivet.devicelibs.raid as raid
import blivet.errors as errors

class RaidTestCase(unittest.TestCase):

    def setUp(self):
        self.levels = raid.RAIDLevels()
        self.levels_none = raid.RAIDLevels(False)
        self.levels_some = raid.RAIDLevels(["mirror", 6])

    def testRaid(self):

        ##
        ## get_min_members
        ##
        # pass
        self.assertEqual(raid.RAID0.min_members, 2)
        self.assertEqual(raid.RAID1.min_members, 2)
        self.assertEqual(raid.RAID5.min_members, 3)
        self.assertEqual(raid.RAID6.min_members, 4)
        self.assertEqual(raid.RAID10.min_members, 4)

        ##
        ## get_max_spares
        ##
        # pass
        self.assertEqual(raid.RAID0.get_max_spares(5), 0)
        self.assertEqual(raid.RAID1.get_max_spares(5), 3)
        self.assertEqual(raid.RAID5.get_max_spares(5), 2)
        self.assertEqual(raid.RAID6.get_max_spares(5), 1)
        self.assertEqual(raid.RAID10.get_max_spares(5), 1)

        ##
        ## raidLevel
        ##
        # pass
        self.assertIs(self.levels.raidLevel(10), raid.RAID10)
        self.assertIs(self.levels.raidLevel("6"), raid.RAID6)
        self.assertIs(self.levels.raidLevel("RAID5"), raid.RAID5)
        self.assertIs(self.levels.raidLevel("raid4"), raid.RAID4)
        self.assertIs(self.levels.raidLevel("mirror"), raid.RAID1)
        self.assertIs(self.levels.raidLevel("stripe"), raid.RAID0)

        self.assertRaises(errors.RaidError, self.levels.raidLevel, "bogus")

        ##
        ## get_max_spares
        ##
        self.assertEqual(raid.RAID0.get_max_spares(1000), 0)
        self.assertEqual(raid.RAID1.get_max_spares(2), 0)

        self.assertRaises(errors.RaidError, raid.RAID0.get_max_spares, 0)

        ##
        ## get_base_member_size
        ##
        self.assertEqual(raid.RAID0.get_base_member_size(4,2), 2)
        self.assertEqual(raid.RAID1.get_base_member_size(4,2), 4)
        self.assertEqual(raid.RAID4.get_base_member_size(4,4), 2)
        self.assertEqual(raid.RAID5.get_base_member_size(4,4), 2)
        self.assertEqual(raid.RAID6.get_base_member_size(4,4), 2)
        self.assertEqual(raid.RAID10.get_base_member_size(4,4), 2)
        self.assertEqual(raid.RAID10.get_base_member_size(4,5), 2)
        self.assertEqual(raid.RAID10.get_base_member_size(5,5), 3)

        self.assertRaises(errors.RaidError, raid.RAID10.get_base_member_size,
                          4, 3)
        self.assertRaises(errors.RaidError, raid.RAID10.get_base_member_size,
                          -4, 4)

        ##
        ## get_raw_array_size
        ##
        self.assertEqual(raid.RAID0.get_raw_array_size(4, 2), 8)
        self.assertEqual(raid.RAID1.get_raw_array_size(4, 2), 2)
        self.assertEqual(raid.RAID4.get_raw_array_size(4, 2), 6)
        self.assertEqual(raid.RAID5.get_raw_array_size(4, 2), 6)
        self.assertEqual(raid.RAID6.get_raw_array_size(4, 2), 4)
        self.assertEqual(raid.RAID10.get_raw_array_size(4, 2), 4)
        self.assertEqual(raid.RAID10.get_raw_array_size(5, 2), 4)

        ##
        ## get_recommended_stride
        ##
        self.assertIsNone(raid.RAID1.get_recommended_stride(32))
        self.assertIsNone(raid.RAID6.get_recommended_stride(32))
        self.assertIsNone(raid.RAID10.get_recommended_stride(32))

        self.assertEqual(raid.RAID0.get_recommended_stride(4), 64)
        self.assertEqual(raid.RAID4.get_recommended_stride(4), 48)
        self.assertEqual(raid.RAID5.get_recommended_stride(4), 48)

        self.assertRaises(errors.RaidError, raid.RAID10.get_recommended_stride, 1)


        ##
        ## names
        ##
        self.assertListEqual(raid.RAID0.names,
           ["raid0", "stripe", "RAID0", "0", 0])
        self.assertListEqual(raid.RAID10.names,
           ["raid10", "RAID10", "10", 10])


        ##
        ## __init__
        ##
        self.assertRaisesRegexp(errors.RaidError,
                                "invalid RAID level",
                                self.levels_none.raidLevel, 10)

        self.assertRaisesRegexp(errors.RaidError,
                                "invalid RAID level",
                                self.levels_some.raidLevel, 10)

        self.assertRaisesRegexp(errors.RaidError,
                                "invalid standard RAID level descriptor",
                                raid.RAIDLevels, ["raid3.1415"])
