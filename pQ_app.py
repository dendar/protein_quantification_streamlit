# core Pkgs
import streamlit as st

#EDA pkgs
import pandas as pd
import numpy as np

# data viz pkgs
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use("Agg")
#st.image("gomes1.png")
stan_cur_conc = np.array([1.5 , 1.  , 0.75, 0.5 , 0.25, 0.])

def main():
    """protein guantification app streamlit"""
    
   
    st.image("gomes1.png")
    
    st.title("Protein Quantification ")
    data = st.file_uploader("Upload Dataset", type = ["csv", "xlsx"])
    st.subheader("Please set up your quantification plate as shown below. Your samples should be set up in rows with replicas in columns")
    st.image("gomes2.png")
    
    
    
    if data is not None:
        df = pd.read_csv(data,delimiter=',', header=None, skiprows=1, 
                         #names=['LABEL','1','2','3','4','5','6','7','8','9','10','11','12']
                        )
        df.columns = list(map(str, df.columns))
        all(isinstance(column, str) for column in df.columns)
        st.dataframe(df)
        
        #Select Columns for Standard Curve Calculated
        #if st.checkbox("Select Columns to Show"):
        st.success("Standard Curve Calculations")
        all_columns = df.columns.tolist()
        select_columns = st.multiselect("Select Columns for Standard Curve", all_columns)
        new_df = df[select_columns]
        select_columns_len = len(select_columns)
        st.sidebar.image("gomes.png")



        stand_cur_Ave = []
        for col in range(len(new_df)):
            mean = sum(new_df.loc[col])/3#select_columns_len
            stand_cur_Ave.append(mean)

        stand_cur_Ave = np.array(stand_cur_Ave)
        #st.write(stand_cur_Ave)

        # fit a set of data points 
        fig, ax = plt.subplots(figsize=(10,8))
        plt.scatter(stan_cur_conc, stand_cur_Ave)
        m,b= np.polyfit(stan_cur_conc, stand_cur_Ave, 1)
        plt.plot(stan_cur_conc,m*stan_cur_conc+b)
        plt.xlabel("Standard Curve Concentration", fontsize = 14)
        plt.ylabel("Standard Curve Average",fontsize = 14);
        print("m value: ", m)
        print("b value: " ,b)
        #st.pyplot(fig)


        #stan_cur_conc = np.array([1.5 , 1.  , 0.75, 0.5 , 0.25, 0.])
        correlation_matrix = np.corrcoef(stan_cur_conc, stand_cur_Ave)
        correlation_xy = correlation_matrix[0,1]
        r_squared = correlation_xy**2
        #st.pyplot(fig)
            
        with st.form(key="form"):
            column1, column2, column3 = st.beta_columns(3)
            with column1:
                submit = st.form_submit_button(label = "Average Absorbance")
            with column2:
                submit1 = st.form_submit_button(label = "R_Squrared")
            with column3:
                submit2 = st.form_submit_button(label = "Standard Curve Graphic")
                
            if submit:
                st.write(stand_cur_Ave)
            if submit1:
                st.write(r_squared)
                
            
            if submit2:
                st.pyplot(fig)
                
            #sample calculations
        st.success("Sample Calculations")
        col1, col2 = st.beta_columns(2)

        with col1:
            with st.beta_expander("Select Columns for Sample Replicates"):
                df1 = df.drop(columns = new_df)
                all_column = df1.columns.to_list()


                select_columns = st.multiselect(" ", all_column)
                new_df1 = df[select_columns]
                st.dataframe(new_df1)
        with col2:
            with st.beta_expander("Avarage Absorbace"):
                sample_Ave = []
                for col in range(len(new_df1)):
                    mean = sum(new_df1.loc[col])/len(new_df1)
                    sample_Ave.append(mean)
                sample_Ave = np.array(sample_Ave)
                st.write(sample_Ave)
            with st.beta_expander("Protein Conc"):  
                #dilution = st.slider("update dilution")
                protein_conc= []
                #update_dilution = []
                for protein in sample_Ave:
                    protein_conc.append(round((protein-b)/m ,2))

                #update_dilution.append(protein_conc*dilution)
                #update_dilution = (protein_conc*dilution)
                df1 = {"protein_conc":protein_conc}
                md = pd.DataFrame(df1)
                st.write(md)
            #with st.beta_expander("dilution"): 
                dilution = st.slider("update dilution")
                update_dilution = (md*dilution)
                
                st.write(update_dilution)
                    
                
               
            
            
                   
            
            
if __name__ =="__main__":
    main()