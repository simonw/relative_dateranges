import datetime, re

handlers = []

def parse_date(input, dt=None):
	for string_or_regex, fn in handlers:
		if isinstance(string_or_regex, basestring):
			if input == string_or_regex:
				return fn(dt, None)
		else:
			# It's a regex, try to match it
			m = string_or_regex.match(input)
			if m:
				return fn(dt, m)
	# If we get here, no match!
	assert False, 'bad input: %s' % input

def match(string_or_regex):
	def inner(fn):
		handlers.append((string_or_regex, fn))
		return fn
	return inner

@match('this_day')
@match('today')
def this_day(dt, m):
	return dt, dt

@match('this_week')
def this_week(dt, m):
	start = dt - datetime.timedelta(days = (dt.weekday() + 1))
	end = start + datetime.timedelta(days = 6)
	return start, end

@match('this_month')
def this_month(dt, m):
	start = dt.replace(day = 1)
	if start.month == 12:
		end = start.replace(month = 1, year = start.year + 1)
	else:
		end = start.replace(month = start.month + 1)
	end = end - datetime.timedelta(days = 1)
	return start, end

@match('this_year')
def this_year(dt, m):
	start = dt.replace(day = 1, month = 1)
	end = dt.replace(day = 31, month = 12)
	return start, end

@match(re.compile('^this_(\d+)_days$'))
def this_x_days(dt, m):
	n = int(m.group(1))
	start = dt
	end = start + datetime.timedelta(days = n - 1)
	return start, end

@match(re.compile('^this_(\d+)_weeks$'))
def this_x_weeks(dt, m):
	n = int(m.group(1))
	start = dt - datetime.timedelta(days = (dt.weekday() + 1))
	end = (start + datetime.timedelta(days = 7 * n)) - datetime.timedelta(days = 1)
	return start, end

@match(re.compile('^this_(\d+)_months$'))
def this_x_months(dt, m):
	n = int(m.group(1))
	years = n // 12
	months = n % 12
	start = dt.replace(day = 1)
	end = start.replace(
		month = start.month + months,
		year = start.year + years
	) - datetime.timedelta(days = 1)
	return start, end
