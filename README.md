# streeteasy_model

This Python code is used to analyze factors that impact the cost of rent in New York City and to model rental prices based on a range of factor including location, size, amenities, and proximity to public transportation.  A summary of the methods, analysis, and results is available on my [project blog](http://www.bradenpurcell.net/rentapp/).

## Data

The data were scraped from [streeteasy.com](http://streeteasy.com/) using code that is available in the [streeteasy_scrape](https://github.com/purcelba/streeteasy_scrape) repository. Rental listings were collected between 11/02/2016 and 1/31/2017 (~63,000 unique listings). All listings are formatted and saved in a SQLite database, *streeteasy_db.sqlite*, that is found in the /db directory. To facilitate model validation, the data are split into a *test_data* table, which includes new listings from the most recent 10 days (6,741 listings), and *train_data*, which includes the remaining data.  A complete description of all variables is found [here](https://github.com/purcelba/streeteasy_scrape).  


## Feature Engineering




## About

This Python code was used to analyze factors that impact the cost of rent in New York City and to model rental prices based on a range of factor including location, size, amenities, and proximity to public transportation.  The code was applied to rental listings collected between 11/02/2016 and 1/31/2017 (~63,000 unique listings).  

A SQLite database, db/streeteasy_db, contains the scraped and cleaned listing information (see [streeteasy_scrape](https://github.com/purcelba/streeteasy_scrape) for details on the data set and code for obtaining and formatting it).  Data scraped over multiple days are aggregated into a training set table, 'train_data', and a test set table, 'test_data' for cross validation.  The training data include data scraped from 10/30/2016 - 1/1/2017 and the test set includes data from 1/2/2017 - 1/11/2017 with all duplicates removed.  

Prior to modeling, a series of exploratory analyses were performed to inform feature engineering and model building.  The exploratory analyses are summarized in the Jupyter notebook, [exploratory_analysis.ipynb](https://github.com/purcelba/streeteasy_model/blob/master/notebooks/exploratory_analysis.ipynb).  

Model development is documented in the Jupyter notebook, [model_development.ipynb](https://github.com/purcelba/streeteasy_model/blob/master/notebooks/model_development.ipynb).  A series of models were evaluated that use L1-regularized regression based on different sets of features.  Code for generating the feature sets for these models is provided in [feateng.py](https://github.com/purcelba/streeteasy_model/blob/master/feateng.py).  This code can be easily modified to extend the model to new feature sets.  Preprocessed feature sets are provided in the /model_features directory as .csv files. 

