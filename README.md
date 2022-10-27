# web_scrapping
### Background
To retrieve the structured data from the marketplace and use the data for the machine learning models.
Azure marketplace is one of the online stores that contains thousands of software applications and services that you can try, buy and deploy. The catalogue includes solutions for different industries and the apps are segregated into categories each and we can browse these apps specifically for each category by going to Homepage -> More -> Apps 
### Objectives
We need to build a tool to get all the apps details like category, sub-category, name, url, costing, ratings, reviews etc of each app and store the details in a spread sheet or a database based on the requirement.
### Tools and Packages
•	Python
•	Excel
•	Python Packages: requests, pandas, BeautifulSoup
### Approach
•	Install all the required packages listed above using pip.
•	Using python requests get the contents of the main page.
•	Using BeautifulSoup parse the response HTML content and get the Browse apps url
•	Using above url make a request and get all the apps and the left pane has all the categories using BeautifulSoup
•	Store all the categories in a list to be used later
•	Parse the list of the categories and get the list of all sub-categories and store in a list/dict
•	For each subcategory get the url with the page numbers and store them in a list.
•	Now parse through each of the link stored in the above step and retrieve all the apps specific to a subcategory page and scrap the data of each url.
•	Identify the tags to extract the information like Overview, Plans + Pricing , Rating + Reviews for each of the apps.
•	Create a data frame using pandas and define the columns that must be used to identify the data that needs to be stored.
•	Write the data frame to Excel sheet or Database based on the requirement.


