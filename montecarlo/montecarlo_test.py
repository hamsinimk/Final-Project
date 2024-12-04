from montecarlo import DieClass
from montecarlo import GameClass
from montecarlo import AnalyzeClass
import unittest
import numpy as np
import pandas as pd


class DieGameAnalyzeTestSuite(unittest.TestCase):
    def test_01_init(self):
        mydie = DieClass(np.array([1,2,3,4,5,6]))
        self.assertTrue(isinstance(mydie, DieClass))
    
    def test_02_change_weight(self):
        mydie = DieClass(np.array([1,2,3,4,5,6]))
        mydie.change_weight(1, 2)
        weight_val1 = 2
        self.assertTrue(weight_val1 in mydie._die_df['weights'].values)
        self.assertTrue(isinstance(mydie._die_df, pd.DataFrame))
    
    def test_03_roll_dice(self):
        mydie = DieClass(np.array([1,2,3,4,5,6]))
        die1 = mydie.roll_die(5)
        actual = len(die1)
        expected = 5
        self.assertEqual(actual,expected)
        self.assertTrue(isinstance((die1), list))
    
    def test_04_die_state(self):
        mydie = DieClass(np.array([1,2,3,4,5,6]))
        self.assertTrue(isinstance(mydie.die_state(), pd.DataFrame))
    
    def test_05_init(self):
        mydie = [DieClass(np.array([1,2,3,4,5,6])), DieClass(np.array([1,2,3,4,5,6]))]
        mygame = GameClass(mydie)
        self.assertTrue(isinstance(mygame, GameClass))
    
    def test_06_play(self):
        mydie = [DieClass(np.array([1,2,3,4,5,6])), DieClass(np.array([1,2,3,4,5,6]))]
        mygame = GameClass(mydie)
        mygame.play(10)
        self.assertTrue(isinstance(mygame._play_df, pd.DataFrame))
    
    def test_07_recent_play(self):
        mydie = [DieClass(np.array([1,2,3,4,5,6])), DieClass(np.array([1,2,3,4,5,6]))]
        mygame = GameClass(mydie)
        mygame.play(10)
        self.assertTrue(isinstance(mygame.recent_play('narrow').index, pd.MultiIndex))
        self.assertFalse(isinstance(mygame.recent_play().index, pd.MultiIndex))
    
    def test_08_init(self):
        mydie = [DieClass(np.array([1,2,3,4,5,6])), DieClass(np.array([1,2,3,4,5,6]))]
        mygame = GameClass(mydie)
        mygame.play(10)
        myanalyze = AnalyzeClass(mygame)
        self.assertTrue(isinstance(myanalyze, AnalyzeClass))
    
    def test_09_jackpot(self):
        mydie = [DieClass(np.array([1])), DieClass(np.array([1]))]
        mygame = GameClass(mydie)
        mygame.play(10)
        myanalyze = AnalyzeClass(mygame)
        expected = 10
        actual = myanalyze.check_jackpot()
        self.assertTrue(isinstance(actual, int))
        self.assertEqual(actual,expected)
    
    def test_10_face_counts(self):
        mydie = [DieClass(np.array([1,2,3,4,5,6])), DieClass(np.array([1,2,3,4,5,6]))]
        mygame = GameClass(mydie)
        mygame.play(10)
        myanalyze = AnalyzeClass(mygame)
        self.assertFalse(isinstance(myanalyze.face_counts().index, pd.MultiIndex))
    
    def test_11_combo_count(self):
        mydie = [DieClass(np.array([1,2,3,4,5,6])), DieClass(np.array([1,2,3,4,5,6]))]
        mygame = GameClass(mydie)
        mygame.play(10)
        myanalyze = AnalyzeClass(mygame)
        self.assertTrue(isinstance(myanalyze.combo_count().index, pd.MultiIndex))
    
    def test_12_perm_count(self):
        mydie = [DieClass(np.array([1,2,3,4,5,6])), DieClass(np.array([1,2,3,4,5,6]))]
        mygame = GameClass(mydie)
        mygame.play(10)
        myanalyze = AnalyzeClass(mygame)
        self.assertTrue(isinstance(myanalyze.perm_count().index, pd.MultiIndex))
        
if __name__ == '__main__':
    unittest.main(verbosity=3)