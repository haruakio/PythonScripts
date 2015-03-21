# -*- coding: utf-8 -*-

import unittest
from pt2.EncodeRunner import *

class EncodeRunnerTest(unittest.TestCase):

    def test_checkBDChannels(self):
        fileName = "201501162300_エレメンタリー2 ホームズ＆ワトソン in NY ＃14 眠れる化石 _ＷＯＷＯＷプライム.ts"
        self.assertTrue(checkBSChannels(fileName))

        fileName = "201502131400_Fit For Fashion ＃5「献身」 _ＦＯＸスポーツエンタ.ts"
        self.assertFalse(checkBSChannels(fileName))

        fileName = "201503012200_【最新作】グランド・ブダペスト・ホ… _スターチャンネル１.ts"
        self.assertTrue(checkBSChannels(fileName))

if __name__ == '__main__':
    unittest.main()