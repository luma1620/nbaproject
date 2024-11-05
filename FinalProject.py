# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import requests
from bs4 import BeautifulSoup

# Load the MVP and Championship data
mvpDF = pd.read_csv("MVPs.csv")  # MVP data
championDF = pd.read_csv("Champions.csv")  # Championship data

# Select important columns from MVP data
mvpTable = mvpDF[["Player", "Age", "G", "Tm", "Year"]]

# Sort the MVP table by age
sortedMvpTable = mvpTable.sort_values("Age", ascending=False)

# Visualization of age and games played by MVPs
sb.catplot(x="Age", y="G", aspect=5, data=mvpDF, kind="bar").set_xticklabels(rotation=90)

# Display the plot
plt.show()

# Web scraping salaries using BeautifulSoup
def get_salary_data(year):
    salaryURL = f"https://hoopshype.com/salaries/players/{year}/"
    salaryPage = requests.get(salaryURL)
    salarySoup = BeautifulSoup(salaryPage.content, "html.parser")
    
    tableHolder = salarySoup.find_all('table')[0]
    rows = tableHolder.find_all('tr')
    
    # Collect player names and salaries
    playerTeamSalary = []
    for row in rows[1:]:
        player = row.find_all('td')[0].text.strip()
        salary = row.find_all('td')[1].text.strip().replace("$", "").replace(",", "")
        playerTeamSalary.append([player, float(salary)])
    
    # Create a DataFrame for salaries
    salaryDF = pd.DataFrame(playerTeamSalary, columns=["Player", "Salary"])
    
    return salaryDF

# Example of fetching salary data for the year 2022
salaryDF_2022 = get_salary_data(2022)

# Merge MVP and salary data
mergedMvpSalary = pd.merge(mvpDF, salaryDF_2022, on="Player", how="inner")

# Display top 5 highest-paid players who won MVP
top5_salaries = mergedMvpSalary.sort_values("Salary", ascending=False).head(5)
print(top5_salaries)

# Display another plot or analysis
sb.barplot(x="Player", y="Salary", data=top5_salaries)
plt.show()
