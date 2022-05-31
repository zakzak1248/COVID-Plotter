import matplotlib.pyplot as plt
import requests
import datetime
from dataclasses import dataclass
import pprint
from matplotlib import pyplot


@dataclass
class COVIDpoint:
    date: datetime.date
    cases: int
    testing: int
    hosp: int
    death: int


def reqdata():
    url = "https://api.covidtracking.com/v2/us/daily.json"
    req = requests.get(url).json()['data']
    data = []
    for i in req:
        point = (COVIDpoint(datetime.datetime.strptime(i['date'], "%Y-%m-%d"),
                            i['cases']['total']['value'],
                            i['testing']['total']['value'],
                            i['outcomes']['hospitalized']['currently']['value'],
                            i['outcomes']['death']['total']['value'],
                            ))

        if point.cases is None: point.cases = 0
        if point.death is None: point.death = 0
        if point.hosp is None: point.hosp = 0
        if point.testing is None: point.testing = 0
        data.append(point)
    return data


def getdata():
    try:
        dataa = open("data.json", "r").read()
        if len(dataa) == 0:
            data = reqdata()
            open("data.json", "w").write(f"{data}")
        else:
            data = dict(dataa)
    except:
        data = reqdata()
        open("data.json", "w").write(f"{data}")

    return data


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.

    data = (getdata())
    from math import log
    getcol = lambda i: list(map(lambda j: getattr(j, i), data))

    pyplot.plot(getcol("date"), list(map(lambda i: None if i==0 else i, getcol("cases"))),   label="cases")
    pyplot.plot(getcol("date"), list(map(lambda i: None if i==0 else i, getcol("testing"))), label="testing")
    pyplot.plot(getcol("date"), list(map(lambda i: None if i==0 else i, getcol("hosp"))),    label="hospitalization")
    pyplot.plot(getcol("date"), list(map(lambda i: None if i==0 else i, getcol("death"))),   label="death")
    pyplot.yscale("log")
    pyplot.legend()
    pyplot.xlabel("Date")
    pyplot.xlabel("Logarithm count")
    pyplot.title("Date to COVID-19 cases, testing, hospitalization and death rate")
    pyplot.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
