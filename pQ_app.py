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
        df = pd.read_csv(data,delimiter=',', header=None, skiprows=1, 
                         #names=['LABEL','1','2','3','4','5','6','7','8','9','10','11','12']
                        )
        df.columns = list(map(str, df.columns))
        all(isinstance(column, str) for column in df.columns)
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
            
            #st.write(new_df.columns)
            #calculate standart curve average
            #for i in range(len(new_df)):
                #st.write(sum(new_df.loc[i])/3)
                
        #if st.checkbox("standart curve average"):
            
            stand_cur_Ave = []
            for col in range(len(new_df)):
                mean = sum(new_df.loc[col])/3
                stand_cur_Ave.append(mean)

            stand_cur_Ave = np.array(stand_cur_Ave)
            #st.write(stand_cur_Ave)
            fig, ax = plt.subplots(figsize=(10,8))
            plt.scatter(stan_cur_conc, stand_cur_Ave)
            plt.xlabel("Standard Curve Concentration", fontsize = 14)
            plt.ylabel("Standard Curve Average",fontsize = 14)
            
            
           
            
   
            # fit a set of data points 
            plt.scatter(stan_cur_conc, stand_cur_Ave)
            m,b= np.polyfit(stan_cur_conc, stand_cur_Ave, 1)
            plt.plot(stan_cur_conc,m*stan_cur_conc+b)
            plt.xlabel("Standard Curve Concentration", fontsize = 14)
            plt.ylabel("Standard Curve Average",fontsize = 14);
            print("m value: ", m)
            print("b value: " ,b)
            
            #stan_cur_conc = np.array([1.5 , 1.  , 0.75, 0.5 , 0.25, 0.])
            correlation_matrix = np.corrcoef(stan_cur_conc, stand_cur_Ave)
            correlation_xy = correlation_matrix[0,1]
            r_squared = correlation_xy**2
            #st.pyplot(fig)
        with st.form(key = "form"):
            column1, column2, column3 = st.beta_columns(3)
            with column1:
                submit = st.form_submit_button(label = "Standard Curve Average")
            with column2:
                submit1 = st.form_submit_button(label = "R_Squrared")
              
            with column3:
                submit2 = st.form_submit_button(label = "Standard Curve Graphic1")
            if submit:
                st.write(stand_cur_Ave)
            if submit1:
                st.write(r_squared)
                
            
            if submit2:
                st.pyplot(fig)
            
            
if __name__ =="__main__":
    main()