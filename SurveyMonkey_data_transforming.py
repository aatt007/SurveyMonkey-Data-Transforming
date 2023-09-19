import pandas as pd

df=pd.read_excel('Raw_Data.xlsx', sheet_name='Edited')
print(df)


df=df.rename(columns={'Identify which division you work in.-Response':'Division Primary','Identify which division you work in.-Other (please specify)':'Division Secondary','Which of the following best describes your position level?-Response':'Position',  'Which generation are you apart of?-Response':'Generation',  'Please select the gender in which you identify.-Response':'Gender', 'Which duration range best aligns with your tenure at your company?-Response':'Tenure', 'Which of the following best describes your employment type?-Response':'Employment Type'})

df=df.drop(columns=['Start Date', 'End Date', 'Email Address','First Name', 'Last Name', 'Custom Data 1'])
print(df)
print(df.columns)

id_vars=list(df.columns[:8])
value_vars=list(df.columns[8:])
print(id_vars)

df_melted=pd.melt(df, id_vars=id_vars, var_name='Question+Subquestion', value_name='Answer')
print(df_melted)
print(df_melted.columns)

df_melted['Question']=df_melted['Question+Subquestion'].str.split('-').str[0]
df_melted=df_melted[['Respondent ID', 'Division Primary', 'Division Secondary', 'Position','Generation', 'Gender', 'Tenure', 'Employment Type','Question','Question+Subquestion', 'Answer']]
print(df_melted)
print(df_melted.columns)

df_melted_flitered=df_melted[df_melted['Answer'].notna()]
print(df_melted_flitered)
Total_Respondents=df_melted_flitered.groupby('Question')['Respondent ID'].nunique().reset_index()
Total_Respondents=Total_Respondents.rename(columns=({'Respondent ID':'Total Respondents'}))
print(Total_Respondents)

df_merge=df_melted.merge(Total_Respondents, how='left', on='Question')
print(df_merge)
print(df_merge.columns)


Same_Answer=df_melted_flitered.groupby(['Question+Subquestion','Answer'])['Respondent ID'].nunique().reset_index()

print(Same_Answer.columns)
Same_Answer=Same_Answer.rename(columns=({'Respondent ID':'Same Answer'}))
print(Same_Answer)

df_merge_final=df_merge.merge(Same_Answer, how='left', on=['Question+Subquestion', 'Answer'])
df_merge_final['Same Answer']=df_merge_final["Same Answer"].fillna(0)
print(df_merge_final)
print(df_merge_final.columns)
df_merge_final.to_excel('final_output.xlsx', index=False)