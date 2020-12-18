year = 1994

for month in range(8,9):
    for day in range(1,32):
        print(f"{month:02}{day:02}{year}")
        print(f"{month:02}{day:02}{str(year)[-2:]}")
        print(f"{month:02}/{day:02}/{year}")
        print(f"{month:02}/{day:02}/{str(year)[-2:]}")
        print(f"{month:02}-{day:02}-{year}")
        print(f"{month:02}-{day:02}-{str(year)[-2:]}")

        print(f"{month}{day}{year}")
        print(f"{month}{day}{str(year)[-2:]}")
        print(f"{month}/{day}/{year}")
        print(f"{month}/{day}/{str(year)[-2:]}")
        print(f"{month}-{day}-{year}")
        print(f"{month}-{day}-{str(year)[-2:]}")

