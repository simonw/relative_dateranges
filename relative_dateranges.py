import datetime, re

handlers = []

class RelativeParseError(ValueError):
    pass

def parse_relative_daterange(input, dt=None):
    "Given a string e.g. tomorrow, next_5_days, this_year returns an inclusive date range tuple"
    dt = dt or datetime.date.today()
    for string_or_regex, fn in handlers:
        if isinstance(string_or_regex, basestring):
            # Exact string match
            if input == string_or_regex:
                return fn(dt)
        else:
            # It's a regex, try to match it
            m = string_or_regex.match(input)
            if m:
                return fn(dt, int(m.group(1)))
    # If we get here, no match!
    raise RelativeParseError('bad input: %s' % input)

def match(string_or_regex):
    def inner(fn):
        handlers.append((string_or_regex, fn))
        return fn
    return inner

def _add_months(dt, months):
    month = (((dt.month - 1) + months) % 12 ) + 1
    year  = dt.year + (((dt.month - 1) + months) // 12) 
    return datetime.date(year, month, 1)

@match('this_day')
@match('today')
def this_day(dt):
    return dt, dt

@match('this_week')
def this_week(dt):
    start = dt - datetime.timedelta(days = (dt.weekday() + 1))
    end = start + datetime.timedelta(days = 6)
    return start, end

@match('this_month')
def this_month(dt):
    start = dt.replace(day = 1)
    if start.month == 12:
        end = start.replace(month = 1, year = start.year + 1)
    else:
        end = start.replace(month = start.month + 1)
    end = end - datetime.timedelta(days = 1)
    return start, end

@match('this_year')
def this_year(dt):
    start = dt.replace(day = 1, month = 1)
    end = dt.replace(day = 31, month = 12)
    return start, end

@match(re.compile('^this_(\d+)_days$'))
def this_x_days(dt, n):
    start = dt
    end = start + datetime.timedelta(days = n - 1)
    return start, end

@match(re.compile('^this_(\d+)_weeks$'))
def this_x_weeks(dt, n):
    start = dt - datetime.timedelta(days = (dt.weekday() + 1))
    end = (start + datetime.timedelta(days = 7 * n)) - datetime.timedelta(days = 1)
    return start, end

@match(re.compile('^this_(\d+)_months$'))
def this_x_months(dt, n):
    start = dt.replace(day = 1)
    end = _add_months(start, n) - datetime.timedelta(days = 1)
    return start, end

@match(re.compile('^this_(\d+)_years$'))
def this_x_years(dt, n):
    start = dt.replace(day = 1, month = 1)
    end = dt.replace(day = 31, month = 12, year = start.year + (n - 1))
    return start, end

@match('next_day')
@match('tomorrow')
def next_day(dt):
    start = dt + datetime.timedelta(days = 1)
    return start, start

@match('previous_day')
@match('yesterday')
def previous_day(dt):
    start = dt - datetime.timedelta(days = 1)
    return start, start

@match(re.compile('^next_(\d+)_days$'))
def next_x_days(dt, n):
    start = next_day(dt)[0]
    end = start + datetime.timedelta(days = n - 1)
    return start, end

@match('next_week')
def next_week(dt):
    start, end = this_week(dt)
    start = start + datetime.timedelta(days = 7)
    end = end + datetime.timedelta(days = 7)
    return start, end

@match(re.compile('^next_(\d+)_weeks$'))
def next_n_weeks(dt, n):
    this_start, this_end = this_x_months(dt, n)
    start = next_month(this_start)[0]
    end = next_month(this_end)[1]
    return start, end

@match('next_month')
def next_month(dt):
    this_start, this_end = this_month(dt)
    start = this_end + datetime.timedelta(days = 1)
    return this_month(start)

@match(re.compile('^next_(\d+)_months$'))
def next_n_months(dt, n):
    this_start, this_end = this_x_months(dt, n)
    start = next_month(this_start)[0]
    end = next_month(this_end)[1]
    return start, end

@match('next_year')
def next_year(dt):
    this_start, this_end = this_year(dt)
    start = this_start.replace(year = this_start.year + 1)
    return this_year(start)

@match(re.compile('^next_(\d+)_years$'))
def next_n_years(dt, n):
    this_start, this_end = this_year(dt)
    start = this_start.replace(year = this_start.year + 1)
    end = start.replace(year = start.year + n)
    end = previous_day(end)[0]
    return start, end

@match(re.compile('^previous_(\d+)_days$'))
def previous_n_days(dt, n):
    end = previous_day(dt)[0]
    start = end - datetime.timedelta(days = n - 1)
    return start, end

@match(re.compile('^previous_(\d+)_weeks$'))
def previous_n_weeks(dt, n):
    this_week_start = this_week(dt)[0]
    start = this_week_start - datetime.timedelta(days = n * 7)
    return start, this_week_start - datetime.timedelta(days = 1)

@match('previous_week')
def previous_week(dt):
    return previous_n_weeks(dt, 1)

@match(re.compile('^previous_(\d+)_months$'))
def previous_n_months(dt, n):
    end = dt.replace(day = 1) - datetime.timedelta(days = 1)
    start = _add_months(end, -(n - 1)).replace(day = 1)
    return start, end

@match('previous_month')
def previous_month(dt):
    return previous_n_months(dt, 1)

@match(re.compile('^previous_(\d+)_years$'))
def previous_n_years(dt, n):
    end = dt.replace(day = 1, month = 1) - datetime.timedelta(days = 1)
    start = end.replace(day = 1, month = 1, year = end.year - (n - 1))
    return start, end

@match('previous_year')
def previous_year(dt):
    return previous_n_years(dt, 1)
