year = 1994

for month in range(8,9):
    for day in range(1,32):
        print(f"{day:02}{month:02}{year}")
        print(f"{day:02}{month:02}{str(year)[-2:]}")
        print(f"{day:02}/{month:02}/{year}")
        print(f"{day:02}/{month:02}/{str(year)[-2:]}")
        print(f"{day}{month}{year}")
        print(f"{day}{month}{str(year)[-2:]}")
        print(f"{day}/{month}/{year}")
        print(f"{day}/{month}/{str(year)[-2:]}")
