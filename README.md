# streeteasy_model

This Python code is used to analyze factors that impact the cost of rent in New York City and to model rental prices based on a range of factor including location, size, amenities, and proximity to public transportation.  A summary of the methods, analysis, and results is available on my [project blog](http://www.bradenpurcell.net/rentapp/). The final model forms the backend of the [RentApp web application](https://purcelba.pythonanywhere.com/) for easy comparison of expected and actual rental values.

## Data

The data were scraped from [streeteasy.com](http://streeteasy.com/) using code that is available in the [streeteasy_scrape](https://github.com/purcelba/streeteasy_scrape) repository. Rental listings were collected between 11/02/2016 and 1/31/2017 (~63,000 unique listings). All listings are formatted and saved in a SQLite database, *streeteasy_db.sqlite*. To facilitate model validation, the data are split into a *test_data* table, which includes new listings from the most recent 10 days (6,741 listings), and *train_data*, which includes the remaining data.  A complete description of all variables is found [here](https://github.com/purcelba/streeteasy_scrape).  

## Data Exploration

All variables were plotted and cleaned to inform the modeling procedure.  Data exploration is summarized in the [exploratory_analysis notebook](https://github.com/purcelba/streeteasy_model/blob/master/exploratory_analysis.ipynb) or see the [project blog](http://www.bradenpurcell.net/rentapp/) for a brief overview. Briefly, each variable was tested for missing data, outliers, and possible erroneous values.  The distributions of each variable were plotted to test if transformations may be needed before modeling.  Rental price was plotted as a function of different variables to understand covariation.  

## Feature Engineering

Feature engineering is handled in **feateng.py**.  The training and test data sets are queried from the streeteasy_db database.  Uninformative features are dropped (e.g., listing id).  Missing values were set to zero and binary features were added to signify missing values.  Categorical variables were encoded with one-hot-feature encoding.  Outliers were dropped based on visual inspection.

To facilitate nested model testing, feateng.py accepts as an arguement one of the following strings indicating which features should be included:
- 'reduced' Reduced model. Only Bed rooms, neighborhood, unit type features
- 'scraped' Reduced model + scraped features. Additional features for square feet, days listed, rooms, and baths.
- 'amen' Scraped model + features indicating amenities.
- 'trans' Amen model + features indicating distance to nearby public transportation
- 'inter' Trans model + interation terms.  Includes all available features and adds interaction terms between neighborhood and several other variables (e.g., square feet, rooms, bedrooms, etc).

## Model Development and Evaluation

I used hierarchical model testing to evaluate a series of L1-regularized linear regression models with increasing complexity.  Models were evaluated using cross-validated R<sup>2</sup> and RMSE. A summary of the model development and evaluation is available in the [model_development](https://github.com/purcelba/streeteasy_model/blob/master/model_development.ipynb) notebook.


## Bootstrapping Confidence Intervals and Feature Importance

I used bootstrapping in order to quantify uncertainty in the goodness-of-fit statistics (R<sup>2</sup> and RMSE) and parameter estimates, as well as to quantify feature importance using a stability selection approach.  This process was accelerated using cluster computing to parallelize bootstrapping.  The code to implement this analysis is available in the [parallel_bootstrap](https://github.com/purcelba/parallel_bootstrap) repository.  A summary of the results are available in the [parallel_bootstrap_example.ipynb](https://github.com/purcelba/parallel_bootstrap/blob/master/parallel_bootstrap_example.ipynb) notebook.