# streeteasy_model

Python code for analyzing and modeling real-estate data scraped from [streeteasy.com](http://streeteasy.com/) (see [streeteasy_scrape](https://github.com/purcelba/streeteasy_scrape)). A summary of these analyses is available in the project blog, [placeholder](LINK), and more details are provided in the Jupyter notebooks, [exploratory_analysis.ipynb](https://github.com/purcelba/streeteasy_model/blob/master/notebooks/exploratory_analysis.ipynb) and [model_development.ipynb](https://github.com/purcelba/streeteasy_model/blob/master/notebooks/model_development.ipynb).


## About

This Python code was used to analyze factors that impact the cost of rent in New York City and to model rental prices based on a range of factor including location, size, amenities, and proximity to public transportation.  The code was applied to rental listings collected between 11/02/2016 and 1/31/2017 (~63,000 unique listings). The long-term goal of this work is to develop a model-based web application to evalute the value of a rental unit by comparing it's listed price to the predicted price.  

A SQLite database, db/streeteasy_db, contains the scraped and cleaned listing information (see [streeteasy_scrape](https://github.com/purcelba/streeteasy_scrape) for details on the data set and code for obtaining and formatting it).  Data scraped over multiple days are aggregated into a training set table, 'train_data', and a test set table, 'test_data' for cross validation.  The training data include data scraped from 10/30/2016 - 1/1/2017 and the test set includes data from 1/2/2017 - 1/11/2017 with all duplicates removed.  

Prior to modeling, a series of exploratory analyses were performed to inform feature engineering and model building.  The exploratory analyses are summarized in the Jupyter notebook, [exploratory_analysis.ipynb](https://github.com/purcelba/streeteasy_model/blob/master/notebooks/exploratory_analysis.ipynb).  

Model development is documented in the Jupyter notebook, [model_development.ipynb](https://github.com/purcelba/streeteasy_model/blob/master/notebooks/model_development.ipynb).  A series of models were evaluated that use L1-regularized regression based on different sets of features.  Code for generating the feature sets for these models is provided in [feateng.py](https://github.com/purcelba/streeteasy_model/blob/master/feateng.py).  This code can be easily modified to extend the model to new feature sets.  Preprocessed feature sets are provided in the /model_features directory as .csv files. 

