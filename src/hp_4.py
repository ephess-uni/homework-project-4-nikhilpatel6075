# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    new_list_of_dates = [datetime.strptime(olddate, "%Y-%m-%d").strftime('%d %b %Y') for olddate in old_dates]
    return new_list_of_dates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        
        raise TypeError()
    
    new_list_values = []
    
    dateStartss = datetime.strptime(start, '%Y-%m-%d')
    
    for p in range(n):
        
        new_list_values.append(dateStartss + timedelta(days=p))
        
    return new_list_values


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    v1 = len(values)
    z = date_range(start_date, len(v1))
    p = list(zip(z, values))
    return p


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    headerLine = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".
              split(','))
    
    late_Fees = defaultdict(float)
    
    with open(infile, 'r') as f:
        data = DictReader(f, fieldnames=headerLine)
        rows = [row for row in data]

    rows.pop(0)
       
    for x in rows:
       
        patronID = x['patron_id']
        
        date_due_on = datetime.strptime(x['date_due'], "%m/%d/%Y")
        
        date_returned_on = datetime.strptime(x['date_returned'], "%m/%d/%Y")
        
        number_of_late_days = (date_returned_on - date_due_on).days
        
        late_Fees[patronID]+= 0.25 * number_of_late_days if number_of_late_days > 0 else 0.0
        
                 
    finalLines = [
        {'patron_id': p, 'late_fees': f'{f:0.2f}'} for p, f in late_Fees.items()
    ]
    with open(outfile, 'w') as f:
        
        writer = DictWriter(f,['patron_id', 'late_fees'])
        writer.writeheader()
        writer.writerows(finalLines)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
