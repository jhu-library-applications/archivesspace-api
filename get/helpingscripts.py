

def collect_value(dictionary, tc_property, log):
    if dictionary:
        value = dictionary.get(tc_property)
        if value:
            log[tc_property] = value
