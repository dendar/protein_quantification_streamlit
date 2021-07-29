# core Pkgs
import streamlit as st

#EDA pkgs
import pandas as pd
import numpy as np

# data viz pkgs
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use("Agg")

stan_cur_conc = np.array([1.5 , 1.  , 0.75, 0.5 , 0.25, 0.])

def main():
    """protein guantification app streamlit"""
    
    st.title("protein guantification ")
    data = st.file_uploader("Upload Dataset", type = ["csv", "xlsx"])
    if data is not None:
        df = pd.read_csv(data,delimiter=',', header=None, skiprows=1, names=['LABEL','1','2','3','4','5','6','7','8','9','10','11','12'])
        st.dataframe(df)
        
        if st.checkbox("Show shape"):
            st.write(df.shape)
        #if st.checkbox("Show Columns"):
            #all_columns = df.columns.to_list()
            #st.write(all_columns)
            
        #if st.checkbox("Select Columns to Show"):
            #all_columns = df.columns.to_list()
            #select_columns = st.multiselect("Select Columns", all_columns)
            #new_df = df[select_columns]
            #st.dataframe(new_df)
            
        if st.checkbox("Select Columns to Show"):
            all_columns = df.columns.to_list()
            select_columns = st.multiselect("Select Columns", all_columns)
            new_df = df[select_columns]
            st.dataframe(new_df)    
            ran = range(len(new_df))
            #calculate standart curve average
            if st.checkbox("standart curve average"):
                        stand_cur_Ave = []
                        for col in range(len(new_df)):
                            mean = (new_df['1'][col]+new_df['2'][col]+new_df['3'][col])/3
                            stand_cur_Ave.append(mean)
                            
            stand_cur_Ave = np.array(stand_cur_Ave)
            st.write(stand_cur_Ave)
            fig, ax = plt.subplots(figsize=(10,8))
            plt.scatter(stan_cur_conc, stand_cur_Ave)
            plt.xlabel("Standard Curve Concentration", fontsize = 14)
            plt.ylabel("Standard Curve Average",fontsize = 14)
            st.pyplot(fig)
        
        #r_squared
        if st.checkbox("r_squared"):
            correlation_matrix = np.corrcoef(stan_cur_conc, stand_cur_Ave)
            correlation_xy = correlation_matrix[0,1]
            r_squared = correlation_xy**2
            st.write("r_squared: ", r_squared)

        if st.checkbox("data points"):
            fig, ax = plt.subplots(figsize=(10,8))
            plt.scatter(stan_cur_conc, stand_cur_Ave)
            m,b= np.polyfit(stan_cur_conc, stand_cur_Ave, 1)
            plt.plot(stan_cur_conc,m*stan_cur_conc+b)
            plt.xlabel("Standard Curve Concentration", fontsize = 14)
            plt.ylabel("Standard Curve Average",fontsize = 14)
            st.pyplot(fig)
            st.write("m value: ", m)
            st.write("b value: " ,b)
            
        #our sample
        sample = df[['4','5','6']]
        sample.rename(columns ={'4':"measurement1",'5':"measurement2",'6':"measurement3"}, inplace =True)

        sample1 = df[['7','8','9']]
        sample1.rename(columns ={'7':"measurement1",'8':"measurement2",'9':"measurement3"}, inplace =True)

        sample2 = df[['10','11','12']]
        sample2.rename(columns ={'10':"measurement1",'11':"measurement2",'12':"measurement3"}, inplace =True)
        our_sample = [sample, sample1, sample2]
        our_sample = pd.concat(our_sample) 
        #st.dataframe(our_sample)  
        
        #reset index so that each sample has a unique identifier

        our_sample.reset_index(drop=True, inplace = True)
        our_sample.index = our_sample.index.set_names(['Sample'])
        st.dataframe(our_sample)    
            
        measurement_average = []

        for sample in range(len(our_sample)):
            mean = (our_sample["measurement1"][sample]+our_sample["measurement2"][sample]+our_sample["measurement3"][sample])/3

            measurement_average.append(mean)
        measurement_average = np.array(measurement_average)
        st.write(measurement_average)
        
        
        def get_measurement_conc(y):
            protein_conc= []
            update_dilution = []
            for protein in y:
                protein_conc.append(round((protein-b)/m ,2))

                update_dilution.append(protein_conc*4)
                df1 = {"measurement_average":measurement_average,"protein_conc":protein_conc}
            return pd.DataFrame(df1)
        st.dataframe(get_measurement_conc(measurement_average))
  


        if st.checkbox("Show Summary"):
            st.write(df.describe())
        
    
    
if __name__ =="__main__":
    main()