from datetime import datetime, date
from typing import Literal, Union, Dict

def suffix_number(numbers: Union[int, float], 
                  specification_letter: Literal['', 'K', 'M', 'B']) -> Union[int, float]:
    """This method will apply the correct multiplication depending on the given specification.

    Args:
        numbers (Union[int, float]): number to multiply by the amount determined by `specification_letter`
        specification_letter (Literal['', 'K', 'M', 'B']): letter to specify multiplier

    Raises:
        ValueError: if the specification_letter does not match on of the four available, the method will fail

    Returns:
        Union[int, float]: the method returns the `number` corectly re-scaled
    """
    if(specification_letter == ""):
        return numbers
    elif(specification_letter == "K"):
        return numbers * 1E3
    elif(specification_letter == "M"):
        return numbers * 1E6
    elif(specification_letter == "B"):
        return numbers * 1E9
    else:
        raise ValueError(f'specification_letter should be either empty, K, M or B. Got {specification_letter} instead')


def month_string_to_number(string: str) -> int:
    """Function to get the string number from the month abbreviated.
    Youtube always uses this method.

    Args:
        string (str): string to check

    Raises:
        ValueError: if the string does not contain a month, than the method will fail

    Returns:
        [type]: int
    """
    m: Dict[str, int] = {
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
    out = m.get(s, None)
    if out is None:
        raise ValueError('Not a month')
    return out
        

def get_date_from_hour_mark(string: str) -> date:
    """When youtube uses the construct with hourly events, a little work is needed to get the correct date.

    Args:
        string ([type]): string to extract hour

    Returns:
        [type]: the correct date in `date` format
    """
    if (datetime.now().hour - int(string)) >= 0:
        return date.today()
    else:
        return date(date.today().year, date.today().month, date.today().day -1)
