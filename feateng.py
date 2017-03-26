"""
Query the database, generate different sets of features, and save the results as a csv file.
"""
import sys
import pandas as pd
import sqlite3
import os

#define some standard data formatting operations shared across dataframes
def standard_formatting(df):
  """
  Apply standard formatting to dataframe.
  - Remove listings with >4,000sq_ft, price >$20,000, rooms >15, beds >8, baths > 6, 
    and one incorrect listing (listed rooms in building not rooms in apt).
  - Drop uninformative columns: data_id, scrape_date, link, address, realtor, borough.
  - Convert unit_type, and neighborhood to indicator variables (one-hot-encoding).
  - For sq_ft, rooms, baths, beds, and days_on_streeteasy, recode missing values to zero and add
    a new variable to flag missing values.
  
  Parameters
  ----------
  df: dataframe
    - Dataframe (observations x features) to be formatted. 
    
  Returns
  -------
  df: dataframe
    - the formatted dataframe
  """
  # remove variables outside of range and outliers
  df = df[df['sq_ft'] <= 4000]
  df = df[df['price'] <= 20000]
  df = df[df['rooms'] <= 15]
  df = df[df['beds'] <= 8]
  df = df[df['baths'] <= 6]
  df = df[df['data_id'] != 1965895]

  # drop columns
  drop_list = ['data_id', 'scrape_date', 'link', 'address', 'realtor', 'borough']
  for c in drop_list:
      if c in df.columns:
          df.drop(c, 1, inplace=True)
  # first we must convert categorical features to dummy variables "one-hot-encoding"
  ohe_feats = ['unit_type', 'neighborhood']
  for f in ohe_feats:
      df_dummy = pd.get_dummies(df[f], prefix=f)  # get dummy variables for this feature.
      df = df.drop([f], axis=1)                   # drop the old cateogircal column
      df = pd.concat((df, df_dummy), axis=1)      # append the dummy variables to df_reg
  # recode missing values from -1 to 0 and add a new feature for missing value.
  recode_list = ['sq_ft', 'rooms', 'baths', 'beds', 'days_on_streeteasy']
  for old_col in recode_list:
      new_col = "%s_miss" % (old_col)
      df[new_col] = 0  # add a new column of zeros
      df.set_value(df[old_col] == -1, new_col, 1)  # set new_col to 1 where old_col is missing
      df.set_value(df[old_col] == -1, old_col, 0)  # set old_col to zero where missing

  return df


def main(model_name,db_name,output_loc,train_table_name,test_table_name):
    """
    Query the requested table from the database.  Apply the requested formatting.
    Save the results in two csv files.
    [model_name]_[table_name]_feats.csv.      The feature dataframe (observations x features).
    [model_name]_[table_name]_target.csv.     The target variable dataframe (observations column vector).  
    
    Parameters
    ----------
    model_name: str
      - name of the model associated with this feature set.  For current implementation this is one of the following:
          'reduced' Reduced model
            - Exclude features from scraped data leaving only the following:
            - Beds, Neighborhood, Unit type features
          'scraped' Reduced model + scraped features (excl. amenities and transportation)
            - Sq_ft, days_on_streeteasy, rooms, baths
          'amen' Scraped model + amenities.
          'trans' Amen model + transportation
          'inter' Trans model + interaction terms
            - Include all features scraped from streeteasy.com and add interaction terms between
              neighborhood and square feet, rooms, bedrooms, bathrooms, and days on streeteasy.
    db_name: str
      - path to the database that will be queried.
    nhood_table: str
      - name of the table containing neighborhood names.
    output_loc: str
      - path to directory in which the output will be saved.  If the directory does not exist, 
        it will be created.
    train_table_name: str
      - name of table in database containing training data
    test_table_name: str
      - name of table in database containing testing data
    """
    #import the data from the database
    con = sqlite3.connect(db_name)                            # connect to the database
    df_train = pd.read_sql("SELECT * FROM %s" % (train_table_name), con)
    df_test = pd.read_sql("SELECT * FROM %s" % (test_table_name), con)
    # use only new listings in the test set not found in the training set
    df_test = df_test[~df_test['data_id'].isin(df_train['data_id'])]
    # create an 'test' column to indicate membership in test set, then combine
    df_train['test_set'] = 0
    df_test['test_set'] = 1
    df = pd.concat([df_train, df_test], axis=0)
    df = df.fillna(0)                             #if concat produced NaNs for train/test data, fill with 0

    #get some basic info about original dataframe
    nhood_list = df['neighborhood'].unique()
      #subway lines
    trans_list = ['line_A', 'line_C', 'line_E', 'line_B', 'line_D', 'line_F', 'line_M', 'line_G',
                'line_L', 'line_J', 'line_Z', 'line_N', 'line_Q', 'line_R', 'line_1', 'line_2',
                'line_3', 'line_4', 'line_5', 'line_6', 'line_7', 'line_S', 'LIRR', 'PATH']
      #amenitites
    amen_list = ['bike_room', 'board_approval_required', 'cats_and_dogs_allowed',
                 'central_air_conditioning', 'concierge', 'cold_storage', 'community_recreation_facilities',
                 'children_playroom', 'deck', 'dishwasher', 'doorman', 'elevator', 'full_time_doorman',
                 'furnished', 'garage_parking', 'green_building', 'gym', 'garden', 'guarantors_accepted',
                 'laundry_in_building', 'live_in_super', 'loft', 'package_room', 'parking_available',
                 'patio', 'pets_allowed', 'roof_deck', 'smoke_free', 'storage_available', 'sublet',
                 'terrace', 'virtual_doorman', 'washer_dryer_in_unit', 'waterview', 'waterfront']
    
    #run standard formatting
    df = standard_formatting(df)
    df = df.drop('index',1)
    
    #Begin engineering features data according to model_name
    if model_name == 'reduced':
        #get lists of features to exclude
        drop_cols = ['days_on_streeteasy','sq_ft','rooms','baths','sq_ft_miss','rooms_miss','baths_miss','days_on_streeteasy_miss']
        #drop variables
        df = df.drop(amen_list,axis=1)
        df = df.drop(trans_list,axis=1)
        df = df.drop(drop_cols,axis=1)
    elif model_name == 'scraped':
        #drop variables
        df = df.drop(amen_list,axis=1)
        df = df.drop(trans_list,axis=1)
    elif model_name == 'amen':
        df = df.drop(trans_list,axis=1)
    elif model_name == 'trans':
        print "no additional formatting"
    elif model_name == 'inter':
        #create interaction terms between rooms, beds, baths, sq_rt and neighborhood
        col_list = ['rooms', 'rooms_miss', 'beds', 'beds_miss', 'baths', 'baths_miss', 'sq_ft', 'sq_ft_miss',
                    'days_on_streeteasy', 'days_on_streeteasy_miss']
        for c in col_list:
            for n in nhood_list:
                new_col = '%s_%s' % (c, n)
                df[new_col] = df[c] * df['neighborhood_' + n]
    else:
        raise ValueError('Unrecognized input for model_name.')
                
    # split the features and target variable
    df_y = df['price'].to_frame()
    df_x = df.drop(['price'], 1)
    #close the database connection
    con.close()
    #save the engineered data as a csv file and the sql database.
    if not os.path.exists(output_loc):
      os.makedirs(output_loc)                  #make the directory if it does not exist
    df_y.to_csv('%s%s_target.csv' % (output_loc,model_name))
    df_x.to_csv('%s%s_feats.csv' % (output_loc,model_name))

if __name__ == '__main__':
    #check for input from command line
    if len(sys.argv) > 1:
        model_name = sys.argv[1]
    else:
        model_name = 'reduced'            #model name to be formatted
    if len(sys.argv) > 2:
        db_name = sys.argv[2]
    else:
        db_name = 'rentnyc_db'        #name of the database
    if len(sys.argv) > 3:
        output_loc = sys.argv[3]
    else:
        output_loc = 'csv_feateng/'   #name of the directory in which to save the otuput csv files.
    if len(sys.argv) > 4:
        train_table_name = sys.argv[4]
    else:
        train_table_name = 'train_data'
    if len(sys.argv) > 5:
        test_table_name = sys.argv[5]
    else:
        test_table_name = 'test_data'

    #execute main function
    main(model_name,db_name,output_loc,train_table_name,test_table_name)
