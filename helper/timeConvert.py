from datetime import datetime,tzinfo


def convert_string_date_time(input):
    input = input.replace('Z', '').replace('T', ' ')
    input = datetime.strptime(input, '%Y-%m-%d %H:%M:%S')
    input = input.replace(tzinfo=None)
    return input







