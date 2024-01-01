manufacturing_year = ['2015', '2015', '2018', '2016', '2020', '2016', '1998', '2014', '2010', '2012', '2007', '2017', '1995 or older', '2019', '2015', '2012', '2016', '2016', '2006', '2013', '2014', '1995 or older', '2016', '2021', '2021', '2014', '2016', '2023', '2022', '2014', '2012', '2018', '2018', '2019', '2018', '2023', '1997', '2020', '2017', '2011', '2017', '2014', '2016', '2020', '2005', '2014', '2019', '2014', '2018', '2012', '2015', '2016', '2022', '2014', '2011', '2015', '2020', '2013', '2011', '2019', '2017', '2023', '2017', '2018', '2017']
result = []
for item in manufacturing_year:
    for x in item.split(' '):
        try:
            result.append(int(x))
        except Exception as _:
            continue

print(result)