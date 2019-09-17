import sqlite3
import easygui as eg

db = "House Prices.db"


class Table:
    def __init__(self, database):
        connection = sqlite3.connect(database)

        cursor = connection.cursor()

        data = cursor.execute("SELECT * FROM House_Prices")
        connection.commit()

        self.data = list(data)

    def avg_house_price_per_year(self, year):
        matches = 0
        total = 0
        for record in self.data:
            if str(year) in record[0]:
                matches += 1
                total += float(record[3])

        return round(total/matches, 2)

    def difference_in_prices_by_year(self, year1, year2):
        y1 = self.avg_house_price_per_year(year1)
        y2 = self.avg_house_price_per_year(year2)

        return y1-y2

    def avg_house_price_per_year_in_region(self, year, region):
        matches = 0
        total = 0
        for record in self.data:
            if str(year) in record[0] and region in record[1]:
                matches += 1
                total += float(record[3])

        return round(total/matches, 2)

    # only works beyond 1970 (annual change data missing <1970)
    def regions_price_growth(self, year, region):
        data = []
        for record in self.data:
            if str(year) in record[0] and region in record[1]:
                data.append(record[3])

        growth = float(data[len(data) - 1]) - float(data[0])

        return round(growth, 2)
    
    # only works beyond 1970 (annual change data missing <1970)
    def compare_regions_price_growth(self, year, region1, region2):
        region1_growth = self.regions_price_growth(year, region1)
        region2_growth = self.regions_price_growth(year, region2)

        if region1_growth > region2_growth:
            return [region1, region1_growth]

        else:
            return [region2, region2_growth]
        
    def highest_growing_region_in_year(self, year):
        # find all regions in year
        regions = []

        for record in self.data:
            if record[1] not in regions:
                regions.append(record[1])

        regional_growth = []
        for region in regions:
            regional_growth.append(int(self.regions_price_growth(year, region)))

        best_region_index = regional_growth.index(max(regional_growth))

        return regions[best_region_index]    
      
        
House_Prices = Table(db)

# GUI

option = eg.indexbox(msg="Choose an Option", title="Options",
                     choices=["Quit", "Avg House Prices Per Year", "Compare Avg Prices per year",
                              "Avg House Price by Region", "Compare Regional Price Growth"])

if option == 0:
    quit()

# avg prices per year
if option == 1:
    field_names = ["Year"]
    field_values = []

    msg = "Enter the year you want to find prices for."
    title = "Average House Prices per Year"

    field_values = eg.multenterbox(msg=msg, title=title, fields=field_names)

    try:
        price = House_Prices.avg_house_price_per_year(field_values[0])
        eg.buttonbox(msg="The average price for the year {y} was £{p}".format(y=field_values[0], p=price),
                     title="Price", choices=["OK"])

    except ZeroDivisionError:
        eg.buttonbox(msg="No such year in data set", title="Error", choices=["OK"])

# differences in prices by year
if option == 2:
    field_names = ["Year 1", "Year 2"]
    field_values = []

    msg = "Enter the years you want to find prices for."
    title = "Difference in Average House Prices by Year"

    field_values = eg.multenterbox(msg=msg, title=title, fields=field_names)

    try:
        price = House_Prices.difference_in_prices_by_year(field_values[0], field_values[1])
        eg.buttonbox(msg="The difference in average prices for the years {y1} & {y2} was £{p}"
                     .format(y1=field_values[0], y2=field_values[1], p=price),
                     title="Difference in prices by year", choices=["OK"])

    except ZeroDivisionError:
        eg.buttonbox(msg="No such year in data set", title="Error", choices=["OK"])

# avg house price by region
if option == 3:
    field_names = ["Year", "Region"]
    field_values = []

    msg = "Enter the year and region you want to find prices for."
    title = "Average House Prices by Region"

    field_values = eg.multenterbox(msg=msg, title=title, fields=field_names)

    try:
        price = House_Prices.avg_house_price_per_year_in_region(field_values[0], field_values[1])
        eg.buttonbox(msg="The average price for the region {r} in the year {y} was £{p}"
                     .format(r=field_values[1], y=field_values[0], p=price),
                     title="Average House Prices by Region", choices=["OK"])

    except ZeroDivisionError:
        eg.buttonbox(msg="No such year in data set", title="Error", choices=["OK"])

# Compare Regional Price Growth
if option == 4:
    field_names = ["Year", "Region 1", "Region 2"]
    field_values = []

    msg = "Enter the year and regions you want to find the best price growth for."
    title = "Compare Regional Price Growth"

    field_values = eg.multenterbox(msg=msg, title=title, fields=field_names)

    try:
        best_region_info = House_Prices.compare_regions_price_growth(field_values[0], field_values[1], field_values[2])
        eg.buttonbox(msg="The region with the best price growth in the year {y} was {r} with a growth of £{p}"
                     .format(r=best_region_info[0], y=field_values[0], p=best_region_info[1]),
                     title="Compare Regional Price Growth", choices=["OK"])

    except ZeroDivisionError:
        eg.buttonbox(msg="No such year in data set", title="Error", choices=["OK"])
