for year in range(1990, 2000):
	for month in range(1,13):
		for day in range(1,32):
			print(f"{day:02}{month:02}{year}")
			print(f"{day:02}{month:02}{str(year)[-2:]}")

