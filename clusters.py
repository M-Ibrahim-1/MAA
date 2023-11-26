import pandas as pd
from sklearn.preprocessing import StandardScaler

class Clusters:
    """
    Every object is a cluster of the Ensemble
    """
    n_clusters = 0
    clusters = []
    def __init__(self, maneuver, passengers):
        self.cluster_index = Clusters.n_clusters
        self.maneuver = maneuver
        self.passengers = passengers

    def add_cluster(self):
        pass

    def import_dataset(self, name_of_csv):
        pd.read_excel(name_of_csv)

    def Standarize(self):
        scaler = StandardScaler()
        standarized_data = scaler.fit_transform(self.df)
        standarized_data = pd.DataFrame(standarized_data, index=self.df.index, columns = self.df.columns)


    def remove_nan(self, threshold):
        """
        :threshold Defines the threshold for the percentage of NaN values
        """
        # Calculate the percentage of NaN values in each column
        nan_percentages = (self.df.isnull().sum() / len(self.df)) * 100
        # Get the columns that exceed the threshold and store them in a list
        columns_to_drop = nan_percentages[nan_percentages > threshold].index.tolist()
        # Drop the columns that have more than 1 percent NaN values
        self.df.drop(columns=columns_to_drop, inplace=True)


    def delete_features_by_substring(self, substrings_to_delete):
        """
        :substrings_to_delete List contains substrings
        Function removes columns which include these substrings in the columns names
        """
        # RdBus.L1.TyreScaling has the same values as time
        for substring in substrings_to_delete:
            # Filter columns that contain the specified substring
            filtered_columns = self.df.filter(like=substring).columns

            # Drop the filtered columns from the DataFrame
            self.df.drop(columns=filtered_columns, inplace=True)


    def convert_df_to_input_outout_df(df:pd.DataFrame):
        """
        This function takes a simulation result as input and forms it in a Input / output form
        it links each time sample to the next time sample
        we make two copies of the input dataframe one for input feature and the other for target values and we prefix the column name with I\P and O\P respectively
        we drop the first row of the target value and the last row of the feature input

        We go from this:
        ____________________________________________________
        Time    | Column 1 | Column 2 | . . . . | Column 3
        ____________________________________________________
        timestep|   ------------ Sample 1 ------------------
                |   ------------ Sample 2 ------------------
                |   ------------ Sample 3 ------------------
                |   
                |   
                |   ------------ Sample n ------------------

        TO THis:
        ______________________________________________________________________________________________________________________
        Time    | I\P_Column 1 | I\P_Column 2 | . . . . | I\P_Column n  | O\P_Column 1 | O\P_Column 2 | . . . . | O\P_Column n
        _______________________________________________________________________________________________________________________
        timestep| <-------------------- Sample 1 ---------------------> | <------------------- Sample 2 ---------------------->
                | <-------------------- Sample 2 ---------------------> | <------------------- Sample 3 ---------------------->
                | <-------------------- Sample 3 ---------------------> | <------------------- Sample 4 ---------------------->
                |                           :                                                     :
                |                           :                                                     :
                | <-------------------- Sample n-1 -------------------> | <------------------- Sample n ---------------------->
        
        """
        input_features = df.add_prefix('I/P_')
        input_features = input_features.drop(index=df.index[-1])
        
        targets = df.add_prefix('O/P_')
        targets = targets.drop(index=0)
        targets.index = [i for i in range(0,targets.shape[0])]
        # Concatenate the columns of both DataFrames
        combined_dataframe = pd.concat([input_features, targets], axis=1)
        return combined_dataframe, input_features, targets

