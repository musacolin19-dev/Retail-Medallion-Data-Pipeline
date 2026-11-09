import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pipeline import transform

class TestMedallion(unittest.TestCase):
    def test_dedup_and_gold(self):
        rows = [{'order_id':'1','day':'2026-01-01','store':'A','quantity':'2','unit_price':'3.25'},
                {'order_id':'1','day':'2026-01-01','store':'A','quantity':'2','unit_price':'3.25'}]
        bronze,silver,gold,quarantine = transform(rows)
        self.assertEqual((len(bronze),len(silver),len(quarantine)),(2,1,1))
        self.assertEqual(gold[0]['revenue'],'6.50')
