import jpholiday
from pytz import timezone
import datetime

import numpy as np
import pandas as pd
from pathlib import Path
from py_strict_list import StructureStrictList, strict_list_property
from .scraping import all_make_source


class JPHolidayGetter:
    """
    jpholidayを利用したHolidayGetter
    """
    def get_holidays(self, start_date, end_date, with_name=False):
        """
        期間を指定して祝日を取得．jpholidayを利用して祝日を取得している．

        start_date: datetime.date
            開始時刻のdate
        end_datetime: datetime.date
            終了時刻のdate
        with_name: bool
            休日の名前を出力するかどうか
        to_date: bool
            出力をdatetime.datetimeにするかdatetime.dateにするか
        """
        assert isinstance(start_date, datetime.date) and isinstance(end_date, datetime.date)
        assert not isinstance(start_date, datetime.datetime) and not isinstance(end_date, datetime.datetime)

        holidays_array = np.array(jpholiday.between(start_date, end_date))

        if not with_name:  # 祝日名がいらない場合
            return holidays_array[:,0].copy()

        return holidays_array


class CSVHolidayGetter:
    def __init__(self, csv_paths):
        if not isinstance(csv_paths, list):  # リストでないなら，リストにしておく
            csv_paths = [csv_paths]
            
        self.csv_paths = csv_paths
        
    def get_holidays(self, start_date, end_date, with_name=False):
        """
        期間を指定して祝日を取得．csvファイルを利用して祝日を取得している．

        start_date: datetime.date
            開始時刻のdate
        end_datetime: datetime.date
            終了時刻のdate
        with_name: bool
            休日の名前を出力するかどうか
        to_date: bool
            出力をdatetime.datetimeにするかdatetime.dateにするか
        """
        assert isinstance(start_date, datetime.date) and isinstance(end_date, datetime.date)
        assert not isinstance(start_date, datetime.datetime) and not isinstance(end_date, datetime.datetime)
        
        # datetime.dateをpd.Timestampに変換(datetime.dateは通常pd.DatetimeIndexと比較できないため)
        start_timestamp = pd.Timestamp(start_date)
        end_timestamp = pd.Timestamp(end_date)

        is_first = True
        is_multi = False

        for csv_path in self.csv_paths:
            if csv_path.exists():  # csvファイルが存在する場合
                holiday_df = pd.read_csv(csv_path, 
                                        header=None,
                                        names=["date", "holiday_name"],
                                        index_col="date",
                                        parse_dates=True
                                        )
            else:
                holiday_df = None

            if holiday_df is not None:
                if is_first:
                    left_df = holiday_df
                    is_first = False
                else:
                    is_multi = True

                if is_multi:
                    append_bool = ~holiday_df.index.isin(left_df.index)  # 左Dataframeに存在しない部分を追加
                    left_df = left_df.append(holiday_df.loc[append_bool])
                    left_df.sort_index(inplace=True)

        if is_first and not is_multi:  # 一度もNone以外が返ってこなかった場合
            if not with_name:  # 祝日名がいらない場合
                return np.array([])
            return np.array([[],[]])
        
        # 指定範囲内の祝日を取得
        holiday_in_span_index = (start_timestamp<=left_df.index)&(left_df.index<end_timestamp)
        holiday_in_span_df = left_df.loc[holiday_in_span_index]
        
        holiday_in_span_date_array = holiday_in_span_df.index.date
        holiday_in_span_name_array = holiday_in_span_df.loc[:,"holiday_name"].values
        holiday_in_span_array = np.stack([holiday_in_span_date_array,
                                          holiday_in_span_name_array
                                         ],
                                         axis=1
                                        )
        
        if not with_name:  # 祝日名がいらない場合
            return holiday_in_span_date_array
            
        return holiday_in_span_array


class Option():
    """
    オプションの指定のためのクラス
    holiday_start_year: int
        利用する休日の開始年
    holiday_end_year: int
        利用する休日の終了年
    backend: str
        休日取得のバックエンド．csvかjpholidayのいずれかが選べる
    csv_source_paths: list of str or pathlib.Path
        バックエンドをcsvにした場合の休日のソースcsvファイル
    holiday_weekdays: list of int
        休日曜日の整数のリスト
    intraday_borders: list of list of 2 datetime.time
        日中を指定する境界時間のリストのリスト
    """
    def __init__(self):
        self._holiday_start_year = datetime.datetime.now().year-5
        self._holiday_end_year = datetime.datetime.now().year
        
        self._backend = "csv"
        #self._csv_source_paths = StructureStrictList(Path("py_workdays/source/holiday_naikaku.csv"))
        self._csv_source_paths = StructureStrictList(Path(__file__).parent / Path("source/holiday_naikaku.csv"))
        self._csv_source_paths.hook_func.add(self.make_holidays)
        
        self.make_holiday_getter()  # HolidayGetterを作成
        self.make_holidays()  # アトリビュートに追加
        
        self._holiday_weekdays = StructureStrictList(5,6)  # 土曜日・日曜日
        self._intraday_borders = StructureStrictList([datetime.time(9,0), datetime.time(11,30)],
                                  [datetime.time(12,30), datetime.time(15,0)])
        
    csv_source_paths = strict_list_property("_csv_source_paths", include_outer_length=False)
    holiday_weekdays = strict_list_property("_holiday_weekdays", include_outer_length=False)
    intraday_borders = strict_list_property("_intraday_borders", include_outer_length=False)
    
    def make_holiday_getter(self):
        if self.backend == "jp_holiday":
            self._holiday_getter = JPHolidayGetter()
        elif self.backend == "csv":
            self._holiday_getter = CSVHolidayGetter(self.csv_source_paths)
        
    def make_holidays(self):
        """
        利用する休日のarrayとDatetimeIndexをアトリビュートとして作成．csv_pathを追加したときにも呼ぶ
        """
        self._holidays_date_array = self._holiday_getter.get_holidays(start_date=datetime.date(self.holiday_start_year,1,1),
                                                    end_date=datetime.date(self.holiday_end_year,12,31),
                                                    with_name=False,
                                                   )
        self._holidays_datetimeindex =  pd.DatetimeIndex(self._holidays_date_array)
        
    @property
    def holiday_start_year(self):
        return self._holiday_start_year
    
    @holiday_start_year.setter
    def holiday_start_year(self, year):
        assert isinstance(year,int)
        self._holiday_start_year = year
        self.make_holidays()  # アトリビュートに追加
    
    @property
    def holiday_end_year(self):
        return self._holiday_end_year

    @holiday_end_year.setter
    def holiday_end_year(self, year):
        assert isinstance(year,int)
        self._holiday_end_year = year
        self.make_holidays()  # アトリビュートに追加
    
    @property
    def backend(self):
        return self._backend
    
    @backend.setter
    def backend(self, backend_str):
        if backend_str not in ("jp_holiday","csv"):
            raise Exception("backend must be 'jp_holiday' or 'csv'.")
        self._backend = backend_str
        self.make_holiday_getter()  # HolidayGetterを作成
        self.make_holidays()  # 休日の作成
    
    @property
    def holidays_date_array(self):
        return self._holidays_date_array
    
    @property
    def holidays_datetimeindex(self):
        return self._holidays_datetimeindex


# Optionの作成
option = Option()


def initialize_source():
    """
    csvのソースを初期化する．インストール時の開始時に呼ぶようにする．
    """
    all_make_source()
    option.__init__()  # optionの初期化


def get_holidays(start_date, end_date, with_name=False, independent=False):
        """
        期間を指定して祝日を取得．

        start_date: datetime.date
            開始時刻のdate
        end_datetime: datetime.date
            終了時刻のdate
        with_name: bool
            休日の名前を出力するかどうか
        to_date: bool
            出力をdatetime.datetimeにするかdatetime.dateにするか
        independent: bool，default:False
            休日をoptionから独立させるかどうか．FalseならばOption内で保持する休日が取得される
        """
        assert isinstance(start_date, datetime.date) and isinstance(end_date, datetime.date)
        assert not isinstance(start_date, datetime.datetime) and not isinstance(end_date, datetime.datetime)
        
        if not independent:
            # datetime.dateをpd.Timestampに変換(datetime.dateは通常pd.DatetimeIndexと比較できないため)
            start_timestamp = pd.Timestamp(start_date)
            end_timestamp = pd.Timestamp(end_date)

            holidays_in_span_index = (start_timestamp<=option.holidays_datetimeindex)&(option.holidays_datetimeindex<end_timestamp)  # DatetimeIndexを使うことに注意
            holidays_in_span_array = option.holidays_date_array[holidays_in_span_index]  # ndarrayを使うtamp(end_date)

            return holidays_in_span_array
        else:
            if option.backend == "jp_holiday":
                holiday_getter = JPHolidayGetter()
            elif option.backend == "csv":
                holiday_getter = CSVHolidayGetter(option.csv_source_paths)
                
            holidays_array = holiday_getter.get_holidays(start_date=start_date,
                                                         end_date=end_date,
                                                         with_name=with_name
                                                        ) 
            return  holidays_array


def get_workdays(start_date, end_date, return_as="date", closed="left"):
    """
    営業日を取得
    
    start_date: datetime.date
        開始時刻のdate
    end_datetime: datetime.date
        終了時刻のdate
    return_as: str, defalt: 'dt'
        返り値の形式
        - 'dt':pd.DatetimeIndex
        - 'date': datetime.date array
    closed: 境界について
        - 'left':開始境界を含める
        - 'right':終了境界を含める
        - None:どちらも含める
    """
    assert isinstance(start_date, datetime.date) and isinstance(end_date, datetime.date)
    assert not isinstance(start_date, datetime.datetime) and not isinstance(end_date, datetime.datetime)
    # 返り値の形式の指定
    return_as_set = {"dt", "date"}
    if not return_as in return_as_set:
        raise Exception("return_as must be any in {}".format(return_as_set))
        
    # datetime.dateをpd.Timestampに変換(datetime.dateは通常pd.DatetimeIndexと比較できないため)
    start_timestamp = pd.Timestamp(start_date)
    end_timestamp = pd.Timestamp(end_date)
    
    # 期間中のdatetimeのarrayを取得
    days_datetimeindex = pd.date_range(start=start_date, end=end_date, freq="D", closed=closed)  # 最終日も含める

    
    # 期間中のholidayを取得
    holidays_in_span_index = (start_timestamp<=option.holidays_datetimeindex)&(option.holidays_datetimeindex<=end_timestamp)  # DatetimeIndexを使うことに注意
    holidays_in_span_datetimeindex = option.holidays_datetimeindex[holidays_in_span_index]
    
    
    # 休日に含まれないもの，さらに土日に含まれないもののboolインデックスを取得
    holiday_bool_array = days_datetimeindex.isin(holidays_in_span_datetimeindex)  # 休日であるかのブール
    
    days_weekday_array = days_datetimeindex.weekday.values
    holiday_weekday_each_bool_arrays = [days_weekday_array==weekday for weekday in option.holiday_weekdays]  # inを使うのを回避
    holiday_weekday_bool_array = np.logical_or.reduce(holiday_weekday_each_bool_arrays)  # 休日曜日
    
    workdays_bool_array = (~holiday_bool_array)&(~holiday_weekday_bool_array)  # 休日でなく休日曜日でない
    
    workdays_datetimeindex = days_datetimeindex[workdays_bool_array].copy()
    if return_as=="dt":
        return workdays_datetimeindex
    elif return_as=="date":
        return workdays_datetimeindex.date


def get_not_workdays(start_date, end_date, return_as="date", closed="left"):
    """
    非営業日を取得(土日or祝日)
    
    start_date: datetime.date
        開始時刻のdate
    end_datetime: datetime.date
        終了時刻のdate
    return_as: str, defalt: 'dt'
        返り値の形式
        - 'dt':pd.DatetimeIndex
        - 'date': datetime.date array
    closed: 境界について
        - 'left':開始境界を含める
        - 'right':終了境界を含める
        - None:どちらも含める
    """
    assert isinstance(start_date, datetime.date) and isinstance(end_date, datetime.date)
    assert not isinstance(start_date, datetime.datetime) and not isinstance(end_date, datetime.datetime)
    # 返り値の形式の指定
    return_as_set = {"dt", "date"}
    if not return_as in return_as_set:
        raise Exception("return_as must be any in {}".format(return_as_set))
    
    # datetime.dateをpd.Timestampに変換(datetime.dateは通常pd.DatetimeIndexと比較できないため)
    start_timestamp = pd.Timestamp(start_date)
    end_timestamp = pd.Timestamp(end_date)

    # 期間中のdatetimeのarrayを取得
    days_datetimeindex = pd.date_range(start=start_date, end=end_date, freq="D", closed=closed)  # 最終日も含める

    
    # 期間中のholidayを取得
    holidays_in_span_index = (start_timestamp<=option.holidays_datetimeindex)&(option.holidays_datetimeindex<=end_timestamp)  # DatetimeIndexを使うことに注意
    holidays_in_span_datetimeindex = option.holidays_datetimeindex[holidays_in_span_index]
    
    # 休日に含まれないもの，さらに休日曜日に含まれないもののboolインデックスを取得
    holiday_bool_array = days_datetimeindex.isin(holidays_in_span_datetimeindex)  # 休日であるかのブール
    
    days_weekday_array = days_datetimeindex.weekday.values
    holiday_weekday_each_bool_arrays = [days_weekday_array==weekday for weekday in option.holiday_weekdays]  # inを使うのを回避
    holiday_weekday_bool_array = np.logical_or.reduce(holiday_weekday_each_bool_arrays)  # 休日曜日
    
    not_workdays_bool_array = holiday_bool_array | holiday_weekday_bool_array  # 休日あるいは休日曜日
    
    not_workdays_datetimeindex = days_datetimeindex[not_workdays_bool_array].copy()
    if return_as=="dt":
        return not_workdays_datetimeindex
    elif return_as=="date":
        return not_workdays_datetimeindex.date
    

def check_workday(select_date):
    """
    与えられたdatetime.dateが営業日であるかどうかを出力する
    select_date: datetime.date
        入力するdate
    """
    assert isinstance(select_date, datetime.date)
    assert not isinstance(select_date, datetime.datetime)
    # 休日であるかどうか
    is_holiday = (option.holidays_date_array==select_date).sum() > 0
    
    # 休日曜日であるかどうか
    is_holiday_weekday = select_date.weekday() in set(option.holiday_weekdays)
    
    is_workday = not any([is_holiday, is_holiday_weekday])
    
    return is_workday


def iter_and_repeat(iterable):
    """
    最初は普通のイテレーターで終了した場合に同じものを返すイテレーター
    """
    iterable = iter(iterable)
    is_end = False
    while True:
        if not is_end:
            try:
                item = next(iterable)
                yield item
            except StopIteration:
                last_item = item
                is_end = True
        else:
            yield last_item


def get_next_workday(select_date, days=1, return_as="date"):
    """
    指定した日数後の営業日を取得
    select_date: datetime.date
        指定する日時
    days: int
        日数
    return_as: str, defalt: 'dt'
        返り値の形式
        - 'dt':pd.Timstamp
        - 'datetime': datetime.datetime array
    """
    #from IPython.core.debugger import Pdb; Pdb().set_trace()
    assert isinstance(select_date, datetime.date)
    assert not isinstance(select_date, datetime.datetime)
    # 返り値の形式の指定
    return_as_set = {"dt", "date"}
    if not return_as in return_as_set:
        raise Exception("return_as must be any in {}".format(return_as_set))
        
    if days <= 0 or not isinstance(days, int):
        raise Exception("select_days is must be integer > 0")
        
    holiday_weekdays_set = set(option.holiday_weekdays)  #setにした方が高速？

    if (option.holidays_date_array==select_date).sum() > 0:  #selet_day が休日の場合
        holiday_bigger_select_index = (option.holidays_date_array<select_date).sum()
    else:  # select_dayが休日でない場合
        holiday_bigger_select_index = (option.holidays_date_array<=select_date).sum()
        
    if holiday_bigger_select_index>=len(option.holidays_date_array):  # select_date以降の休日が存在しない場合
        holiday_bigger_select_index = -1
        
    holiday_iter = iter_and_repeat(iter(option.holidays_date_array[holiday_bigger_select_index:]))
    def days_gen(select_date):
        add_days = 0  # select_dateを含める
        while True:
            yield select_date + datetime.timedelta(days=add_days)
            add_days += 1
    days_iter = days_gen(select_date)

    # 以下二つのイテレーターを比較し，one_dayが休日に含まれる場合カウントし，カウントが指定に達した場合終了する
    one_day = next(days_iter)
    one_holiday = next(holiday_iter)
    if holiday_bigger_select_index!=-1:  # select_date以降の休日が存在しない場合
        assert(one_day <= one_holiday)  # これを満たさないと祝日検出ができない

    # 最初はwhileの外で，さらに初日がworkdaysでもカウントしない
    if one_day==one_holiday:
        one_holiday = next(holiday_iter)   

    one_day = next(days_iter)
    counter = 0

    while True:
        if one_day==one_holiday:  #その日が祝日である
            one_holiday = next(holiday_iter)
        else:
            if not one_day.weekday() in holiday_weekdays_set:  #その日が休日曜日である
                counter += 1  # カウンターをインクリメント

        if counter>= days:
            break

        one_day = next(days_iter)
        
    if return_as=="date":
        return one_day
    elif return_as=="dt":
        return pd.Timestamp(one_day)

def get_previous_workday(select_date, days=1, return_as="date"):
    """
    指定した日数前の営業日を取得
    select_date: datetime.date
        指定する日時
    days: int
        日数
    return_as: str, defalt: 'dt'
        返り値の形式
        - 'dt':pd.Timstamp
        - 'datetime': datetime.datetime array
    """
    #from IPython.core.debugger import Pdb; Pdb().set_trace()
    assert isinstance(select_date, datetime.date)
    assert not isinstance(select_date, datetime.datetime)
    # 返り値の形式の指定
    return_as_set = {"dt", "date"}
    if not return_as in return_as_set:
        raise Exception("return_as must be any in {}".format(return_as_set))
        
    if days <= 0 or not isinstance(days, int):
        raise Exception("select_days is must be integer > 0")
        
    holiday_weekdays_set = set(option.holiday_weekdays)  #setにした方が高速？

    if (option.holidays_date_array==select_date).sum() > 0:  #selet_day が休日の場合
        holiday_bigger_select_index = (option.holidays_date_array[::-1]>select_date).sum()
    else:  # select_dayが休日でない場合
        holiday_bigger_select_index = (option.holidays_date_array[::-1]>=select_date).sum()
        
    if holiday_bigger_select_index>=len(option.holidays_date_array):  # select_date以前の休日が存在しない場合
        holiday_bigger_select_index = -1

    holiday_iter = iter_and_repeat(iter(option.holidays_date_array[::-1][holiday_bigger_select_index:]))
    def days_gen(select_date):
        add_days = 0  # select_dateを含める
        while True:
            yield select_date + datetime.timedelta(days=add_days)
            add_days -= 1
    days_iter = days_gen(select_date)

    # 以下二つのイテレーターを比較し，one_dayが休日に含まれる場合カウントし，カウントが指定に達した場合終了する
    one_day = next(days_iter)
    one_holiday = next(holiday_iter)
    if holiday_bigger_select_index!=-1:  # select_date以前の休日が存在しない場合
        assert(one_day >= one_holiday)  # これを満たさないと祝日検出ができない

    # 最初はwhileの外で，さらに初日がworkdaysでもカウントしない
    if one_day==one_holiday:
        one_holiday = next(holiday_iter)   

    one_day = next(days_iter)
    counter = 0

    while True:
        if one_day==one_holiday:  #その日が祝日である
            one_holiday = next(holiday_iter)
        else:
            if not one_day.weekday() in holiday_weekdays_set:  #その日が休日曜日である
                counter += 1  # カウンターをインクリメント

        if counter>= days:
            break

        one_day = next(days_iter)
        
    if return_as=="date":
        return one_day
    elif return_as=="dt":
        return pd.Timestamp(one_day)


def get_near_workday(select_date, is_after=True, return_as="date"):
    """
    引数の最近の営業日を取得
    select_date: datetime.date
        指定する日時
    is_aftaer: bool
        指定日時の後が前か
    return_as: str, defalt: 'dt'
        返り値の形式
        - 'dt':pd.Timstamp
        - 'datetime': datetime.datetime array
    """
    assert isinstance(select_date, datetime.date)
    assert not isinstance(select_date, datetime.datetime)
    # 返り値の形式の指定
    return_as_set = {"dt", "date"}
    if not return_as in return_as_set:
        raise Exception("return_as must be any in {}".format(return_as_set))
        
    
    if check_workday(select_date):  # 指定日が営業日である場合
        out_date = select_date
        if return_as=="date":
            return out_date
        elif return_as=="dt":
            return pd.Timestamp(out_date)
    else:
        if is_after:
            return get_next_workday(select_date, days=1, return_as=return_as)
        else:
            return get_previous_workday(select_date, days=1, return_as=return_as)


def get_workdays_number(start_date, days, return_as="date"):
    """
    指定した日数分の営業日を取得
    start_date: datetime.date
        開始日時
    days: int
        日数
    return_as: str, defalt: 'dt'
        返り値の形式
        - 'dt':pd.Timstamp
        - 'datetime': datetime.datetime array
    """
    assert isinstance(start_date, datetime.date)
    assert not isinstance(start_date, datetime.datetime)
    #get_next_workdayでは初日はworkdayに含めないので，初日がworkdayならclosedをleftにする
    if days > 0:
        is_initial_day_workday = check_workday(start_date)
        end_date = get_next_workday(start_date, days=days, return_as="date")
        if is_initial_day_workday:  # 初日がworkdayの場合
            return get_workdays(start_date, end_date, return_as=return_as, closed="left")
        else:
            return get_workdays(start_date, end_date, return_as=return_as, closed=None)
    else:
        is_initial_day_workday = check_workday(start_date)
        end_date = get_previous_workday(start_date, days=abs(days), return_as="date")
        is_initial_day_workday = check_workday(start_date)
        if is_initial_day_workday:
            return get_workdays(end_date, start_date, return_as=return_as, closed="right")[::-1]
        else:
            return get_workdays(end_date, start_date, return_as=return_as, closed=None)[::-1]
        

if __name__ == "__main__":
    import pickle
    ##########################
    ### get_holidays
    ##########################
    
    start_date = datetime.date(2019, 1, 1)
    end_date = datetime.date(2020, 12, 31)

    holidays = get_holidays(start_date, end_date, with_name=False)
    print(holidays)

    
    ##########################
    ### get_workdays
    ##########################

    start_date = datetime.datetime(2019, 1, 1)
    end_date = datetime.datetime(2019, 12, 31)

    workdays = get_workdays(start_date, end_date, return_as="date", end_include=False)
    print("workdays:",workdays)

    
    ##########################
    ### get_not_workdays
    ##########################

    start_datetime = datetime.date(2019, 1, 1)
    end_datetime = datetime.date(2019, 12, 31)

    not_workdays = get_not_workdays(start_date, end_date, return_as="dt")
    print("not_workdays:",not_workdays)

    
    ##########################
    ### check_workday
    ##########################
    
    select_date = datetime.date(2019, 1, 4)
    print(check_workday(select_date))


    ##########################
    ### get_next_workday
    ##########################

    jst_timezone = timezone("Asia/Tokyo")
    select_datetime = jst_timezone.localize(datetime.datetime(2020, 1, 1, 0, 0, 0))

    next_workday = get_next_workday(select_datetime, days=6, return_as="dt")
    print("next workday",next_workday)

    # データの作成
    with open("aware_stock_df.pickle", "rb") as f:
        aware_stock_df = pickle.load(f)

    print("aware_stock_df",aware_stock_df)

    with open("naive_stock_df.pickle", "rb") as f:
        naive_stock_df = pickle.load(f)

    print("naive_stock_df at 9:00",naive_stock_df.at_time(datetime.time(9,0)))
