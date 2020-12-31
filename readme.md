# 営業日・営業時間のデータを取得
## requirements
- jpholiday
- pytz
- pandas
- numpy

## 使い方

```python
import datetime
import pickle
```


```python
from py_workdays import get_workdays_jp, check_workday_jp, extract_workdays_jp, extract_workdays_intraday_jp, option
```

### 営業日を取得


```python
start_date = datetime.date(2020,11,1)
end_date = datetime.date(2021,1,1)

get_workdays_jp(start_date, end_date, return_as="date")
```




    array([datetime.date(2020, 11, 2), datetime.date(2020, 11, 4),
           datetime.date(2020, 11, 5), datetime.date(2020, 11, 6),
           datetime.date(2020, 11, 9), datetime.date(2020, 11, 10),
           datetime.date(2020, 11, 11), datetime.date(2020, 11, 12),
           datetime.date(2020, 11, 13), datetime.date(2020, 11, 16),
           datetime.date(2020, 11, 17), datetime.date(2020, 11, 18),
           datetime.date(2020, 11, 19), datetime.date(2020, 11, 20),
           datetime.date(2020, 11, 24), datetime.date(2020, 11, 25),
           datetime.date(2020, 11, 26), datetime.date(2020, 11, 27),
           datetime.date(2020, 11, 30), datetime.date(2020, 12, 1),
           datetime.date(2020, 12, 2), datetime.date(2020, 12, 3),
           datetime.date(2020, 12, 4), datetime.date(2020, 12, 7),
           datetime.date(2020, 12, 8), datetime.date(2020, 12, 9),
           datetime.date(2020, 12, 10), datetime.date(2020, 12, 11),
           datetime.date(2020, 12, 14), datetime.date(2020, 12, 15),
           datetime.date(2020, 12, 16), datetime.date(2020, 12, 17),
           datetime.date(2020, 12, 18), datetime.date(2020, 12, 21),
           datetime.date(2020, 12, 22), datetime.date(2020, 12, 23),
           datetime.date(2020, 12, 24), datetime.date(2020, 12, 25),
           datetime.date(2020, 12, 28), datetime.date(2020, 12, 29),
           datetime.date(2020, 12, 30), datetime.date(2020, 12, 31)],
          dtype=object)



### 営業日かどうか判定 


```python
select_date = datetime.date(2020,1,1)

check_workday_jp(select_date)
```




    False



### 既存のデータフレームから営業日・営業時間(東京証券取引所)のものを取得 


```python
with open("aware_stock_df.pickle", "rb") as f:
    aware_stock_df = pickle.load(f)
    
aware_stock_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Open_6502</th>
      <th>High_6502</th>
      <th>Low_6502</th>
      <th>Close_6502</th>
      <th>Volume_6502</th>
    </tr>
    <tr>
      <th>timestamp</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-11-04 00:00:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-04 00:01:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-04 00:02:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-04 00:03:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-04 00:04:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2020-11-30 23:55:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-30 23:56:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-30 23:57:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-30 23:58:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2020-11-30 23:59:00+09:00</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>29520 rows × 5 columns</p>
</div>




```python
extracted_stock_df = extract_workdays_intraday_jp(aware_stock_df, return_as="df")
extracted_stock_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Open_6502</th>
      <th>High_6502</th>
      <th>Low_6502</th>
      <th>Close_6502</th>
      <th>Volume_6502</th>
    </tr>
    <tr>
      <th>timestamp</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-11-04 09:00:00+09:00</th>
      <td>2669.0</td>
      <td>2670.0</td>
      <td>2658.0</td>
      <td>2664.0</td>
      <td>93000.0</td>
    </tr>
    <tr>
      <th>2020-11-04 09:01:00+09:00</th>
      <td>2663.0</td>
      <td>2664.0</td>
      <td>2650.0</td>
      <td>2652.0</td>
      <td>17600.0</td>
    </tr>
    <tr>
      <th>2020-11-04 09:02:00+09:00</th>
      <td>2649.0</td>
      <td>2655.0</td>
      <td>2646.0</td>
      <td>2649.0</td>
      <td>19200.0</td>
    </tr>
    <tr>
      <th>2020-11-04 09:03:00+09:00</th>
      <td>2652.0</td>
      <td>2670.0</td>
      <td>2651.0</td>
      <td>2670.0</td>
      <td>31200.0</td>
    </tr>
    <tr>
      <th>2020-11-04 09:04:00+09:00</th>
      <td>2671.0</td>
      <td>2674.0</td>
      <td>2670.0</td>
      <td>2674.0</td>
      <td>12800.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2020-11-30 14:55:00+09:00</th>
      <td>2908.0</td>
      <td>2908.0</td>
      <td>2905.0</td>
      <td>2905.0</td>
      <td>26300.0</td>
    </tr>
    <tr>
      <th>2020-11-30 14:56:00+09:00</th>
      <td>2905.0</td>
      <td>2908.0</td>
      <td>2905.0</td>
      <td>2907.0</td>
      <td>21700.0</td>
    </tr>
    <tr>
      <th>2020-11-30 14:57:00+09:00</th>
      <td>2908.0</td>
      <td>2909.0</td>
      <td>2906.0</td>
      <td>2907.0</td>
      <td>27200.0</td>
    </tr>
    <tr>
      <th>2020-11-30 14:58:00+09:00</th>
      <td>2907.0</td>
      <td>2910.0</td>
      <td>2905.0</td>
      <td>2908.0</td>
      <td>42600.0</td>
    </tr>
    <tr>
      <th>2020-11-30 14:59:00+09:00</th>
      <td>2910.0</td>
      <td>2920.0</td>
      <td>2902.0</td>
      <td>2920.0</td>
      <td>146100.0</td>
    </tr>
  </tbody>
</table>
<p>5400 rows × 5 columns</p>
</div>



### 休日の探索期間

休日はデフォルトでは2015年から2021年のものを利用できる．オプションから変更できる


```python
# default
option.holidays_date_array[:5]  # 利用される休日
```




    array([datetime.date(2015, 1, 1), datetime.date(2015, 1, 12),
           datetime.date(2015, 2, 11), datetime.date(2015, 3, 21),
           datetime.date(2015, 4, 29)], dtype=object)




```python
option.holiday_start_year = 2000
option.holidays_date_array[:5]  # 利用される休日
```




    array([datetime.date(2000, 1, 1), datetime.date(2000, 1, 10),
           datetime.date(2000, 2, 11), datetime.date(2000, 3, 20),
           datetime.date(2000, 4, 29)], dtype=object)


