import datetime

#
# Function to get suffix.
# Youtube uses a specific set of abbreviations
#
def suffix_number(numbers, specification_letter):
    if(specification_letter == ""):
        return numbers
    if(specification_letter == "K"):
        return numbers * 1E3
    elif(specification_letter == "M"):
        return numbers * 1E6
    elif(specification_letter == "B"):
        return numbers * 1E9

#
# Function to get the string number from the month abbreviated.
# Youtube always uses this method.
#
def month_string_to_number(string):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
        'may':5,
        'jun':6,
        'jul':7,
        'aug':8,
        'sep':9,
        'oct':10,
        'nov':11,
        'dec':12
        }
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')
#
# When youtube uses the construct with hourly events,
# a little work is needed to get the correct date.
#
def get_date_from_hour_mark(string):
    if (datetime.datetime.now().hour - int(string)) >= 0:
        return datetime.date.today()
    else:
        return datetime.date(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day -1)
