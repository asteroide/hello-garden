import yaml
import datetime
from datetime import timedelta


def __add_timedelta(current, delta):
    print(f"__add_timedelta({current} , {delta})")
    __delta = None
    if "m" in delta:
        __delta = timedelta(months=int(delta.replace("m", "")))
    elif "d" in delta:
        __delta = timedelta(days=int(delta.replace("d", "")))
    else:
        __delta = timedelta(days=int(delta.replace("d", "")))
    return current + __delta


def update(data):
    for section in data['garden']:
        for key_s in data['garden'].keys():
            try:
                for vege in data['garden'][key_s]:
                    for key_v in vege.keys():
                        if 'duration' in vege[key_v]['date']:
                            try:
                                print(vege, key_v)
                                vege[key_v]['date']['end'] = __add_timedelta(vege[key_v]['date']['start'], vege[key_v]['date']['duration'])
                            except TypeError:
                                vege[key_v]['date']['start'] = vege[key_v]['date']['start']['date']['end']
                                vege[key_v]['date']['end'] = __add_timedelta(vege[key_v]['date']['start'], vege[key_v]['date']['duration'])
                        if type(vege[key_v]['date']['end']) is not datetime.date:
                            vege[key_v]['date']['end'] = __add_timedelta(vege[key_v]['date']['start'], vege[key_v]['date']['end'])
                        if type(vege[key_v]['date']['start']) is not datetime.date:
                            vege[key_v]['date']['start'] = vege[key_v]['date']['start']['date']['end']
            except TypeError:
                pass


def get_data(filename):
    data = yaml.load(open(filename), Loader=yaml.SafeLoader)
    update(data)
    return data
