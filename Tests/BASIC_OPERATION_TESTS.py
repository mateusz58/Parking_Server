
from datetime import datetime
# for x in range(6):
#   print(x+1)
#



colors = [5, 7, 10, 12]
i = 0
while i < len(colors):
    print(colors[i])
    i += 1


def is_all_items_unique(input_list):
    first_element = input_list[0]
    for element in input_list:
        if element != first_element:
            return False

    return True


print(is_all_items_unique(colors))