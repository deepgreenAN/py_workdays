import unittest
import numpy as np
import datetime
import pandas as pd

from py_workdays import get_holidays_jp, get_workdays_jp, get_not_workdays_jp
from py_workdays import check_workday_jp, get_next_workday_jp, get_workdays_number_jp
from py_workdays import extract_workdays_jp, extract_intraday_jp, extract_workdays_intraday_jp
from py_workdays import option


def true_holidays_2021():
    holidays_list = [datetime.date(2021,1,1),
                     datetime.date(2021,1,11),
                     datetime.date(2021,2,11),
                     datetime.date(2021,2,23),
                     datetime.date(2021,3,20),
                     datetime.date(2021,4,29),
                     datetime.date(2021,5,3),
                     datetime.date(2021,5,4),
                     datetime.date(2021,5,5),
                     datetime.date(2021,7,22),
                     datetime.date(2021,7,23),
                     datetime.date(2021,8,8),
                     datetime.date(2021,8,9),  #振替
                     datetime.date(2021,9,20),
                     datetime.date(2021,9,23),
                     datetime.date(2021,11,3),
                     datetime.date(2021,11,23)
                    ]

    return np.array(holidays_list)


class TestWorkdays(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        option.holiday_start_year = 2021
        option.holiday_weekdays = [5,6]
        option.intraday_borders = [[datetime.time(9,0), datetime.time(11,30)],
                                   [datetime.time(12,30), datetime.time(15,0)]]
        
    def test_get_holidays(self):
        holidays_array = get_holidays_jp(datetime.date(2021,1,1), datetime.date(2022,1,1))
        self.assertTrue(np.array_equal(holidays_array, true_holidays_2021()))
        
    def test_related_workdays(self):
        # get_workdays_jp, get_not_workdays_Jp
        all_date = pd.date_range(datetime.date(2021,1,1), datetime.date(2021,12,31), freq="D").date
        all_weekdays = np.array([item.weekday() for item in all_date])
        
        is_hoildays = np.in1d(all_date, true_holidays_2021())  # 祝日
        is_hoilday_weekdays = np.logical_or.reduce([all_weekdays==holiday_weekday for holiday_weekday in option.holiday_weekdays])  # 祝日曜日
        
        is_not_workdays = is_hoildays | is_hoilday_weekdays
        is_workdays = (~is_hoildays) & (~is_hoilday_weekdays)
        
        true_not_workdays = all_date[is_not_workdays]
        true_workdays = all_date[is_workdays]
        
        workdays_array = get_workdays_jp(datetime.date(2021,1,1), datetime.date(2022,1,1))
        not_workdays_array = get_not_workdays_jp(datetime.date(2021,1,1), datetime.date(2022,1,1))
        
        self.assertTrue(np.array_equal(workdays_array, true_workdays))
        self.assertTrue(np.array_equal(not_workdays_array, true_not_workdays))
        
        # get_workdays_number_jp
        # 祝日始まり
        workdays_50_array = get_workdays_number_jp(datetime.date(2021,1,1), 50)
        self.assertTrue(np.array_equal(workdays_50_array, true_workdays[:50]))
        
        # 営業日始まり
        workdays_50_array = get_workdays_number_jp(datetime.date(2021,1,4), 50)  # 1月4日は一番最初の営業日
        self.assertTrue(np.array_equal(workdays_50_array, true_workdays[:50]))
        
        # check_workday_jp
        checked_workdays = [check_workday_jp(one_date) for one_date in true_workdays]
        self.assertTrue(all(checked_workdays))
        checked_not_workdays = [check_workday_jp(one_date) for one_date in true_not_workdays]
        self.assertFalse(any(checked_not_workdays))
        
        # get_next_workday_jp
        # 祝日始まり
        workdays_array = np.array([get_next_workday_jp(datetime.date(2021,1,1), i) for i in range(1,len(true_workdays)+1)])
        self.assertTrue(np.array_equal(workdays_array, true_workdays))
        # 営業日始まり
        workdays_array = np.array([get_next_workday_jp(datetime.date(2021,1,4), i) for i in range(1,len(true_workdays))])
        self.assertTrue(np.array_equal(workdays_array, true_workdays[1:]))   # get_next_workdaysは初日は含めないので
        
    def test_related_extract(self):
        all_date = pd.date_range(datetime.date(2021,1,1), datetime.date(2021,12,31), freq="D").date
        all_weekdays = np.array([item.weekday() for item in all_date])
        
        is_hoildays = np.in1d(all_date, true_holidays_2021())  # 祝日
        is_hoilday_weekdays = np.logical_or.reduce([all_weekdays==holiday_weekday for holiday_weekday in option.holiday_weekdays])  # 祝日曜日
        
        is_not_workdays = is_hoildays | is_hoilday_weekdays
        
        true_not_workdays = all_date[is_not_workdays] 
        
        
        dt_index = pd.date_range(datetime.datetime(2021,1,1,0,0,0), datetime.datetime(2021,12,31,23,59,0), freq="T")
        nan_df = pd.DataFrame(None, index=dt_index)
        nan_df["column1"] = np.nan
        extracted_df = extract_workdays_jp(nan_df)
        # 抽出したpd.DataFrameのdateが非営業日に含まれない
        self.assertFalse(np.any(np.in1d(extracted_df.index.date, true_not_workdays)))
        
        # 日中以外のある時間のデータの長さが0
        extracted_df = extract_intraday_jp(nan_df)
        self.assertEqual(len(extracted_df.at_time(datetime.time(8,0)).index),0)
        
        # 両方チェック
        extracted_df = extract_workdays_intraday_jp(nan_df)
        self.assertFalse(np.any(np.in1d(extracted_df.index.date, true_not_workdays)))
        self.assertEqual(len(extracted_df.at_time(datetime.time(8,0)).index),0)


class TestOption(unittest.TestCase):
    def test_make_workdays(self):
        #optionを設定するだけで休日が更新される．
        option.holiday_start_year = 2021
        option.holiday_end_year = 2021
        self.assertTrue(np.array_equal(option.holidays_date_array, true_holidays_2021()))


if __name__ == "__main__":
    unittest.main()