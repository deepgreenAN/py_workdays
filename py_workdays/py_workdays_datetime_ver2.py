import datetime
from datetime import timedelta
from pytz import timezone
from itertools import zip_longest

from .py_workdays_ver4 import option, check_workday_jp, get_near_workday_jp, get_next_workday_jp, get_previous_workday_jp, get_workdays_jp


def get_timezone_datetime_like(select_datetime, like_datetime):
    """
    指定したdatetimeのタイムゾーンを別のdatetimeのものに変換
    select_datetime: datetime.datetime
        タイムゾーンを変換したいdatetime
    like_datetime: datetime.datetime
        一致させたいタイムゾーンを持つdatetime
    """
    like_datetime_is_aware = like_datetime.tzinfo is not None
    if like_datetime_is_aware:
        like_timezone = timezone(str(like_datetime.tzinfo))
    
    select_datetime_is_aware = select_datetime.tzinfo is not None
    
    if not like_datetime_is_aware and not select_datetime_is_aware:# select_datetime, like_datetimeがどちらもnaiveな場合
        return select_datetime
    elif like_datetime_is_aware and not select_datetime_is_aware:# like_datetimeのみがawareな場合
        return like_timezone.localize(select_datetime)
    elif not like_datetime_is_aware and select_datetime_is_aware:# select_datetimeのみがawareな場合
        return select_datetime.replace(tzinfo=None)
    elif like_datetime_is_aware and select_datetime_is_aware:# select_datetime, like_datetimeがどちらもawareな場合
        if str(like_datetime.tzinfo) != str(select_datetime.tzinfo):
            return select_datetime.astimezone(like_timezone)
        else:
            return select_datetime


def check_workday_intraday_jp(select_datetime):
    """
    与えられたdatetime.datetimeが営業日・営業時間内であるかどうかを出力する
    select_datetime: datetime.datetime
        入力するdatetime
    """
    assert isinstance(select_datetime, datetime.datetime)

    select_date = select_datetime.date()
    # 休日であるかどうか
    is_holiday = (option.holidays_date_array==select_date).sum() > 0
    
    # 休日曜日であるかどうか
    is_holiday_weekday = select_date.weekday() in set(option.holiday_weekdays)
    
    # 営業時間であるかどうか
    select_time = select_datetime.time()
    is_intraday = any([one_borders[0] <= select_time and select_time < one_borders[1] for one_borders in option.intraday_borders])
    
    is_workday_intraday = not any([is_holiday, is_holiday_weekday, not is_intraday])
    return is_workday_intraday


def get_next_border_workday_intraday_jp(select_datetime):
    """
    引数のdatetime.datetimeに最も近い後の営業時間を境界シンボルと共に返す
    Paremeters
    ----------
    select_datetime: datetime.datetime
        指定する日時
        
    Returns
    -------
    out_datetime: datetime.datetime
        営業時間境界の日時
    boder_symbol: str
        out_datetimeが開始か終了かを示す文字列
            "border_start": 営業時間の開始時刻
            "border_end": 営業時間の終了時刻
    """
    assert isinstance(select_datetime, datetime.datetime)
    select_date = select_datetime.date()    
    if check_workday_jp(select_date):  # 営業日の場合
        select_time = select_datetime.time()
        if check_workday_intraday_jp(select_datetime):  # 営業日・営業時間の場合
            border_ends = [one_borders[1] for one_borders in option.intraday_borders]
            bigger_border_ends = [one_border for one_border in border_ends if one_border > select_time]
            out_time = min(bigger_border_ends)
            out_datetime = datetime.datetime(select_date.year,
                                             select_date.month,
                                             select_date.day,
                                             out_time.hour,
                                             out_time.minute,
                                             out_time.second
                                            )
            out_datetime = get_timezone_datetime_like(out_datetime, select_datetime)
            return out_datetime, "border_end"          
        else:
            border_starts = [one_borders[0] for one_borders in option.intraday_borders]
            bigger_border_starts = [one_border for one_border in border_starts if one_border > select_time]
            if len(bigger_border_starts) > 0:  # 指定時間より遅い営業時間の開始ボーダーがある場合
                out_time = min(bigger_border_starts)
                out_datetime = datetime.datetime(select_date.year,
                                                 select_date.month,
                                                 select_date.day,
                                                 out_time.hour,
                                                 out_time.minute,
                                                 out_time.second
                                                )
                out_datetime = get_timezone_datetime_like(out_datetime, select_datetime)
                return out_datetime, "border_start"
            else:  # 指定時間より遅い営業時間が存在しない場合
                out_date = get_next_workday_jp(select_date)  # 次の営業日
                out_time = min(border_starts)
                out_datetime = datetime.datetime(out_date.year,
                                                 out_date.month,
                                                 out_date.day,
                                                 out_time.hour,
                                                 out_time.minute,
                                                 out_time.second
                                                )
                out_datetime = get_timezone_datetime_like(out_datetime, select_datetime)
                return out_datetime, "border_start"

            
    else:  # 営業日でない場合
        border_starts = [one_borders[0] for one_borders in option.intraday_borders]
        out_date = get_near_workday_jp(select_date, is_after=True)
        out_time = min(border_starts)
        out_datetime = datetime.datetime(out_date.year,
                                         out_date.month,
                                         out_date.day,
                                         out_time.hour,
                                         out_time.minute,
                                         out_time.second
                                        )
        out_datetime = get_timezone_datetime_like(out_datetime, select_datetime)
        return out_datetime, "border_start"


def get_previous_border_workday_intraday_jp(select_datetime, force_is_end=False):
    """
    引数のdatetime.datetimeに最も近い前の営業時間を境界シンボルと共に返す
    Paremeters
    ----------
    select_datetime: datetime.datetime
        指定する日時
    force_is_end: bool
        終了境界だった場合にその営業時間の開始境界を求めるどうか
        
    Returns
    -------
    out_datetime: datetime.datetime
        営業時間境界の日時
    boder_symbol: str
        out_datetimeが開始か終了かを示す文字列
            "border_start": 営業時間の開始時刻
            "border_end": 営業時間の終了時刻
    """
    assert isinstance(select_datetime, datetime.datetime)
    select_date = select_datetime.date()
    select_time = select_datetime.time()
    if check_workday_jp(select_date):  # 営業日の場合
        border_starts = [one_borders[0] for one_borders in option.intraday_borders] 
        if check_workday_intraday_jp(select_datetime) and not any([one_border==select_time for one_border in border_starts]):  # 営業時間・営業日かつ開始境界でない場合
            smaller_border_starts = [one_border for one_border in border_starts if one_border < select_time]
            out_time = max(smaller_border_starts)
            out_datetime = datetime.datetime(select_date.year,
                                             select_date.month,
                                             select_date.day,
                                             out_time.hour,
                                             out_time.minute,
                                             out_time.second
                                            )
            out_datetime = get_timezone_datetime_like(out_datetime, select_datetime)
            return out_datetime, "border_start"                    
        else:
            border_ends = [one_borders[1] for one_borders in option.intraday_borders]
            smaller_border_ends = [one_border for one_border in border_ends if one_border <= select_time]
            # force_is_endがTrueで終了境界と同じ場合，その開始境界を返す．
            if force_is_end:
                if any([one_border==select_time for one_border in border_ends]):
                    border_starts = [one_borders[0] for one_borders in option.intraday_borders]
                    smaller_border_starts = [one_border for one_border in border_starts if one_border < select_time]
                    out_time = max(smaller_border_starts)
                    out_datetime = datetime.datetime(select_date.year,
                                                     select_date.month,
                                                     select_date.day,
                                                     out_time.hour,
                                                     out_time.minute,
                                                     out_time.second
                                                    )
                    out_datetime = get_timezone_datetime_like(out_datetime, select_datetime)
                    return out_datetime, "border_start"                     
            
            if len(smaller_border_ends) > 0:  # 指定時間より早い営業時間の終了ボーダーがある場合
                out_time = max(smaller_border_ends)
                out_datetime = datetime.datetime(select_date.year,
                                                 select_date.month,
                                                 select_date.day,
                                                 out_time.hour,
                                                 out_time.minute,
                                                 out_time.second
                                                )
                out_datetime = get_timezone_datetime_like(out_datetime, select_datetime)
                return out_datetime, "border_end"
            else:  # 指定時間より早い営業時間が存在しない場合
                out_date = get_previous_workday_jp(select_date)  # 前の営業日
                out_time = max(border_ends)
                out_datetime = datetime.datetime(out_date.year,
                                                 out_date.month,
                                                 out_date.day,
                                                 out_time.hour,
                                                 out_time.minute,
                                                 out_time.second
                                                )
                out_datetime = get_timezone_datetime_like(out_datetime, select_datetime)
                return out_datetime, "border_end"
            
    else:  # 営業日でない場合
        border_ends = [one_borders[1] for one_borders in option.intraday_borders]
        out_date = get_near_workday_jp(select_date, is_after=False)
        out_time = max(border_ends)
        out_datetime = datetime.datetime(out_date.year,
                                         out_date.month,
                                         out_date.day,
                                         out_time.hour,
                                         out_time.minute,
                                         out_time.second
                                        )
        out_datetime = get_timezone_datetime_like(out_datetime, select_datetime)
        return out_datetime, "border_end"


def get_near_workday_intraday_jp(select_datetime, is_after=True):
    """
    引数のdatetime.datetimeが営業日・営業時間の場合はそのまま，そうでない場合は最も近い境界を境界シンボルとともに返す．
    Paremeters
    ----------
    select_datetime: datetime.datetime
        指定する日時
    is_after: bool
        後ろを探索するかどうか
        
    Returns
    -------
    out_datetime: datetime.datetime
        営業日・営業時間（あるいはボーダー）の日時
    boder_symbol: str
        out_datetimeがボーダーであるか・そうだとして開始か終了かを示す文字列
            "border_intra": 営業時間内
            "border_start": 営業時間の開始時刻
            "border_end": 営業時間の終了時刻
    """
    assert isinstance(select_datetime, datetime.datetime)
    #from IPython.core.debugger import Pdb; Pdb().set_trace()
    
    if check_workday_intraday_jp(select_datetime):
        return select_datetime, "border_intra"
    else:
        if is_after:
            return get_next_border_workday_intraday_jp(select_datetime)
        else:
            return get_previous_border_workday_intraday_jp(select_datetime)


def get_borders_workday_intraday(start_datetime, end_datetime):
    """
    指定期間中の営業日・営業時間のボーダーをシンボルと共に返す
    Parameters
    ----------
    start_datetime: datetime.datetime
        期間の開始日時
    end_datetime: datetime.datetime
        期間の終了日時
    
    Returns
    -------
    border_list: list of tuple
        out_datetime: datetime.datetime
            営業日・営業時間（あるいはボーダー）の日時
        boder_symbol: str
            out_datetimeがボーダーであるか・そうだとして開始か終了かを示す文字列
                "border_intra": 営業時間内
                "border_start": 営業時間の開始時刻
                "border_end": 営業時間の終了時刻   
    """
    out_list = []
    border_starts = [one_borders[0] for one_borders in option.intraday_borders]
    border_ends = [one_borders[1] for one_borders in option.intraday_borders]
    start_date = start_datetime.date()
    end_date = end_datetime.date()
    
    #開始時刻が営業日に入っている場合
    if check_workday_jp(start_date):
        start_time = start_datetime.time()
        bigger_border_starts = [one_border for one_border in border_starts if one_border >= start_time]
        bigger_border_ends = [one_border for one_border in border_ends if one_border >= start_time]
        # 開始時刻に最も近い終了境界
        if check_workday_intraday_jp(start_datetime) and len(bigger_border_ends) > 0:
            start_border_time = min(bigger_border_ends)
            bigger_border_ends.remove(start_border_time)  # 開始境界と終了境界のセットを残すため
            start_border_datetime = datetime.datetime(start_datetime.year,
                                                      start_datetime.month,
                                                      start_datetime.day,
                                                      start_border_time.hour,
                                                      start_border_time.minute,
                                                      start_border_time.second
                                                     )
            start_border_datetime = get_timezone_datetime_like(start_border_datetime, start_datetime)
            out_list.append((start_border_datetime, "border_end"))
        
        # それ以外のその日の境界
        for one_start_border_time, one_end_border_time in zip_longest(bigger_border_starts, bigger_border_ends):
            if one_start_border_time is not None:
                one_start_border_datetime =  datetime.datetime(start_date.year,
                                                               start_date.month,
                                                               start_date.day,
                                                               one_start_border_time.hour,
                                                               one_start_border_time.minute,
                                                               one_start_border_time.second
                                                              )
                one_start_border_datetime = get_timezone_datetime_like(one_start_border_datetime, start_datetime)
                out_list.append((one_start_border_datetime, "border_start"))
            
            if one_end_border_time is not None:
                one_end_border_datetime =  datetime.datetime(start_date.year,
                                                             start_date.month,
                                                             start_date.day,
                                                             one_end_border_time.hour,
                                                             one_end_border_time.minute,
                                                             one_end_border_time.second
                                                            )
                one_end_border_datetime = get_timezone_datetime_like(one_end_border_datetime, start_datetime)
                out_list.append((one_end_border_datetime, "border_end"))       
    
    #開始時刻から終了時刻までの営業日
    workdays = get_workdays_jp(start_date+timedelta(days=1), end_date-timedelta(days=1), end_include=True)
    
    for workday in workdays:
        for one_start_border_time, one_end_border_time in zip(border_starts, border_ends):
            one_start_border_datetime =  datetime.datetime(workday.year,
                                                           workday.month,
                                                           workday.day,
                                                           one_start_border_time.hour,
                                                           one_start_border_time.minute,
                                                           one_start_border_time.second
                                                          )
            one_start_border_datetime = get_timezone_datetime_like(one_start_border_datetime, start_datetime)
            out_list.append((one_start_border_datetime, "border_start"))
            
            
            one_end_border_datetime =  datetime.datetime(workday.year,
                                                         workday.month,
                                                         workday.day,
                                                         one_end_border_time.hour,
                                                         one_end_border_time.minute,
                                                         one_end_border_time.second
                                                        )
            one_end_border_datetime = get_timezone_datetime_like(one_end_border_datetime, start_datetime)
            out_list.append((one_end_border_datetime, "border_end"))
    
    # 終了時刻が営業日・営業時間に入っている場合
    if check_workday_jp(end_date):
        end_time = end_datetime.time()
        smaller_border_ends = [one_border for one_border in border_ends if one_border < end_time]  # 終了時刻を含めない
        smaller_border_starts = [one_border for one_border in border_starts if one_border < end_time]  # 終了時刻を含めない
        if check_workday_intraday_jp(end_datetime) and len(smaller_border_starts) > 0:
            end_border_time = max(smaller_border_starts)
            smaller_border_starts.remove(end_border_time)
            end_border_datetime = datetime.datetime(end_datetime.year,
                                                    end_datetime.month,
                                                    end_datetime.day,
                                                    end_border_time.hour,
                                                    end_border_time.minute,
                                                    end_border_time.second
                                                    )
            end_border_datetime = get_timezone_datetime_like(end_border_datetime, end_datetime)
            out_list.append((end_border_datetime, "border_start"))
            
        # それ以外のその日の境界
        for one_start_border_time, one_end_border_time in zip_longest(smaller_border_starts, smaller_border_ends):
            if one_start_border_time is not None:
                one_start_border_datetime =  datetime.datetime(end_date.year,
                                                               end_date.month,
                                                               end_date.day,
                                                               one_start_border_time.hour,
                                                               one_start_border_time.minute,
                                                               one_start_border_time.second
                                                              )
                one_start_border_datetime = get_timezone_datetime_like(one_start_border_datetime, start_datetime)
                out_list.append((one_start_border_datetime, "border_start"))
            
            if one_end_border_time is not None:
                one_end_border_datetime =  datetime.datetime(end_date.year,
                                                             end_date.month,
                                                             end_date.day,
                                                             one_end_border_time.hour,
                                                             one_end_border_time.minute,
                                                             one_end_border_time.second
                                                            )
                one_end_border_datetime = get_timezone_datetime_like(one_end_border_datetime, start_datetime)
                out_list.append((one_end_border_datetime, "border_end"))
                
        # 最後にソート
        out_list.sort(key=lambda one_tuple: one_tuple[0])  # timeの方でソート
        
    return out_list


def time_to_delta(_time):
    """
    datetime.timeをdatetime.deltatimeに変更する
    """
    return timedelta(hours=_time.hour, minutes=_time.minute, seconds=_time.second)


def add_workday_intraday_datetime(select_datetime, delta_time):
    """
    営業日・営業時間を考慮しdatetime.datetimeを追加する
    select_datetime: datetime.datetime
        指定する日時
    delta_time: datetime.timedelta
        追加するtimedelta
    """
    assert delta_time >= timedelta(seconds=0)
    all_delta_time = delta_time
    one_workday_delta_time = timedelta(seconds=0)
    for one_borders in option.intraday_borders:
        one_workday_delta_time += time_to_delta(one_borders[1]) - time_to_delta(one_borders[0])  # ボーダーの重なりは考慮しないことに注意
    
    select_date = select_datetime.date()
    borders_starts = [one_borders[0] for one_borders in option.intraday_borders]
    next_border_datetime, next_border_symbol = get_next_border_workday_intraday_jp(select_datetime)
    
    if check_workday_intraday_jp(select_datetime) and next_border_symbol=="border_end":  # select_datetimeが営業時間内にある場合
        delta_select_date_intraday = (next_border_datetime - select_datetime)
        
        if all_delta_time < delta_select_date_intraday: # 残りがその営業時間内以下の場合
            out_datetime = select_datetime + all_delta_time
            return out_datetime
        elif all_delta_time==delta_select_date_intraday:  # 残りがその営業時間と同じ場合
            out_datetime, out_datetime_symbol = get_next_border_workday_intraday_jp(select_datetime + all_delta_time)
            assert out_datetime_symbol=="border_start"
            return out_datetime
        else:
            all_delta_time -= delta_select_date_intraday  # 営業時間分を減らす
    
    if next_border_datetime.date()==select_date:  # その日の営業時間がまだ残っている場合
        next_border_time = next_border_datetime.time()
        bigger_intraday_index = [i for i,one_border_start in enumerate(borders_starts) if next_border_time <=one_border_start]
        
        for index in bigger_intraday_index:
            delta_select_date_intraday = time_to_delta(option.intraday_borders[index][1]) - time_to_delta(option.intraday_borders[index][0])
            if all_delta_time <= delta_select_date_intraday:  # 残りがその営業時間内以下の場合
                out_datetime_start = datetime.datetime(year=select_date.year,
                                                       month=select_date.month,
                                                       day=select_date.day,
                                                       hour=option.intraday_borders[index][0].hour,
                                                       minute=option.intraday_borders[index][0].minute,
                                                       second=option.intraday_borders[index][0].second
                                                      )
                out_datetime_start = get_timezone_datetime_like(out_datetime_start, select_datetime)
                out_datetime = out_datetime_start + all_delta_time
                
                if all_delta_time==delta_select_date_intraday:  # 残りがその営業時間と同じ場合
                    out_datetime, out_datetime_symbol = get_next_border_workday_intraday_jp(out_datetime)
                    assert out_datetime_symbol=="border_start"
                
                return out_datetime
            else:
                all_delta_time -= delta_select_date_intraday  # 営業時間分を減らす

    add_day_number = 1  #追加が必要な営業日の日数
    
    while True: # 進める営業日を求め残りの時間を計算する
        if all_delta_time <= one_workday_delta_time:
            break
        all_delta_time -= one_workday_delta_time
        add_day_number += 1

    out_date = get_next_workday_jp(select_date, add_day_number)  # 出力する営業日
    
    for one_borders in option.intraday_borders:
        delta_out_date_intraday = time_to_delta(one_borders[1]) - time_to_delta(one_borders[0])
        if all_delta_time <= delta_out_date_intraday:  # 残りがその営業時間内以下の場合
            out_datetime_start = datetime.datetime(year=out_date.year,
                                                   month=out_date.month,
                                                   day=out_date.day,
                                                   hour=one_borders[0].hour,
                                                   minute=one_borders[0].minute,
                                                   second=one_borders[0].second
                                                  ) 
            out_datetime_start = get_timezone_datetime_like(out_datetime_start, select_datetime)
            out_datetime = out_datetime_start + all_delta_time
            
            if all_delta_time==delta_out_date_intraday:  # 残りがその営業時間と同じ場合
                out_datetime, out_datetime_symbol = get_next_border_workday_intraday_jp(out_datetime)
                assert out_datetime_symbol=="border_start"
            
            return out_datetime
        else:
            all_delta_time -= delta_out_date_intraday  # 営業時間分を減らす      


def sub_workday_intraday_datetime(select_datetime, delta_time):
    """
    営業日・営業時間を考慮しdatetime.datetimeを減らす
    select_datetime: datetime.datetime
        指定する日時
    delta_time: datetime.timedelta
        減算するtimedelta
    """
    #from IPython.core.debugger import Pdb; Pdb().set_trace()
    assert delta_time >= timedelta(seconds=0)
    all_delta_time = delta_time
    one_workday_delta_time = timedelta(seconds=0)
    for one_borders in option.intraday_borders:
        one_workday_delta_time += time_to_delta(one_borders[1]) - time_to_delta(one_borders[0])  # ボーダーの重なりは考慮しないことに注意
    
    select_date = select_datetime.date()
    borders_ends = [one_borders[1] for one_borders in option.intraday_borders]
    previous_border_datetime, previous_border_symbol = get_previous_border_workday_intraday_jp(select_datetime)
    if check_workday_intraday_jp(select_datetime) and previous_border_symbol=="border_start":  # select_datetimeが営業時間内にある場合
        delta_select_date_intraday = (select_datetime - previous_border_datetime)
        if all_delta_time <= delta_select_date_intraday: # 残りがその営業時間内以下の場合
            out_datetime = select_datetime - all_delta_time
            return out_datetime
        else:
            all_delta_time -= delta_select_date_intraday  # 営業時間分を減らす
    
    if previous_border_datetime.date()==select_date:  # その日の営業時間がまだ残っている場合
        previous_border_time = previous_border_datetime.time()
        smaller_intraday_index = [i for i,one_border_end in enumerate(borders_ends) if previous_border_time>=one_border_end]
        for index in smaller_intraday_index[::-1]:  # 逆順
            delta_select_date_intraday = time_to_delta(option.intraday_borders[index][1]) - time_to_delta(option.intraday_borders[index][0])
            if all_delta_time <= delta_select_date_intraday:  # 残りがその営業時間内以下の場合
                out_datetime_end = datetime.datetime(year=select_date.year,
                                                     month=select_date.month,
                                                     day=select_date.day,
                                                     hour=option.intraday_borders[index][1].hour,
                                                     minute=option.intraday_borders[index][1].minute,
                                                     second=option.intraday_borders[index][1].second
                                                    )
                out_datetime_end = get_timezone_datetime_like(out_datetime_end, select_datetime)
                out_datetime = out_datetime_end - all_delta_time
                return out_datetime
            else:
                all_delta_time -= delta_select_date_intraday  # 営業時間分を減らす

    sub_day_number = 1  #追加が必要な営業日の日数
    
    while True: # 進める営業日を求め残りの時間を計算する
        if all_delta_time <= one_workday_delta_time:
            break
        all_delta_time -= one_workday_delta_time
        sub_day_number += 1

    out_date = get_previous_workday_jp(select_date, sub_day_number)  # 出力する営業日
    
    for one_borders in option.intraday_borders[::-1]:  # 逆順
        delta_out_date_intraday = time_to_delta(one_borders[1]) - time_to_delta(one_borders[0])
        if all_delta_time <= delta_out_date_intraday:  # 残りがその営業時間内以下の場合
            out_datetime_end = datetime.datetime(year=out_date.year,
                                                 month=out_date.month,
                                                 day=out_date.day,
                                                 hour=one_borders[1].hour,
                                                 minute=one_borders[1].minute,
                                                 second=one_borders[1].second
                                                ) 
            out_datetime_end = get_timezone_datetime_like(out_datetime_end, select_datetime)
            out_datetime = out_datetime_end - all_delta_time
            return out_datetime
        else:
            all_delta_time -= delta_out_date_intraday  # 営業時間分を減らす     


def get_timedelta_workdays_intraday(start_datetime, end_datetime):
    """
    指定期間中の営業日・営業時間をtimedeltaとして出力
    start_datetime: datetime.datetime
        指定期間の開始日時
    end_datetime: datetime.datetime
        指定期間の終了日時
    """
    all_delta_time = timedelta(seconds=0)
    start_date = start_datetime.date()
    start_time = start_datetime.time()
    end_date = end_datetime.date()
    end_time = end_datetime.time()
    #from IPython.core.debugger import Pdb; Pdb().set_trace()
    
    border_starts = [one_borders[0] for one_borders in option.intraday_borders]
    border_ends = [one_borders[1] for one_borders in option.intraday_borders]
    
    one_workday_delta_time = timedelta(seconds=0)
    #start_datetimeについて
    for one_borders in option.intraday_borders:
        one_workday_delta_time += time_to_delta(one_borders[1]) - time_to_delta(one_borders[0])  # ボーダーの重なりは考慮しないことに注意
    
    if check_workday_jp(start_date):  # start_dateが営業日の場合
        if check_workday_intraday_jp(start_datetime):  # start_datetimeが営業時間内の場合
            bigger_border_ends = [one_border_end for one_border_end in border_ends if one_border_end > start_time]
            near_border_end = min(bigger_border_ends)
            all_delta_time += time_to_delta(near_border_end) - time_to_delta(start_time)
        
        bigger_intraday_index = [i for i,one_border_start in enumerate(border_starts) if start_time < one_border_start]
        for index in bigger_intraday_index:
            all_delta_time += time_to_delta(option.intraday_borders[index][1]) - time_to_delta(option.intraday_borders[index][0])
            
    
    #開始時刻から終了時刻までの営業日
    workdays = get_workdays_jp(start_date+timedelta(days=1), end_date-timedelta(days=1), end_include=True)
    for _ in range(len(workdays)):
        all_delta_time += one_workday_delta_time
        
    #end_datetimeについて
    if check_workday_jp(end_date):  # end_dateが営業日の場合
        if check_workday_intraday_jp(end_datetime):
            smaller_border_starts = [one_border_start for one_border_start in border_starts if one_border_start <= end_time]
            near_border_start = max(smaller_border_starts)
            all_delta_time += time_to_delta(end_time) - time_to_delta(near_border_start)
        
        smaller_intraday_index = [i for i,one_border_end in enumerate(border_ends) if one_border_end <= end_time]
        for index in smaller_intraday_index:
            all_delta_time += time_to_delta(option.intraday_borders[index][1]) - time_to_delta(option.intraday_borders[index][0])
        
    return all_delta_time

if __name__ == "__main__":
    pass