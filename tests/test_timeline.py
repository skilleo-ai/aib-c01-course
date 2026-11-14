import unittest
from pipeline.timeline import build_timeline,map_time,map_highlight

class TimelineTests(unittest.TestCase):
    def test_long_wait_preserves_actions_and_remaps_highlight(self):
        t=build_timeline(40,[(5,35)])
        self.assertEqual(t[-1].edited_end,15)
        self.assertEqual(map_time(t,5),5)
        self.assertEqual(map_time(t,35),10)
        self.assertEqual(map_highlight(t,36,38),[11,13])
        self.assertEqual(t[0].speed,1)
        self.assertEqual(t[-1].speed,1)
    def test_short_wait_and_no_wait_unchanged(self):
        self.assertEqual(build_timeline(10,[(2,4)])[-1].edited_end,10)
        self.assertEqual(map_time(build_timeline(10,[]),10),10)
    def test_multiple_waits_and_boundaries(self):
        t=build_timeline(50,[(30,50),(0,20)])
        self.assertEqual(t[-1].edited_end,20)
        self.assertEqual(map_time(t,20),5)
        self.assertEqual(map_time(t,30),15)
        self.assertEqual(map_time(t,50),20)
    def test_invalid_waits_rejected(self):
        for waits in [[(4,3)],[(0,11)],[(-1,2)],[(1,5),(4,8)],[(2,float('nan'))]]:
            with self.subTest(waits=waits),self.assertRaises(ValueError):build_timeline(10,waits)
        for duration in [0,-1,float('inf'),float('nan')]:
            with self.assertRaises(ValueError):build_timeline(duration,[])
        with self.assertRaises(ValueError):map_time(build_timeline(10,[]),11)
        with self.assertRaises(ValueError):map_highlight(build_timeline(10,[]),4,3)
