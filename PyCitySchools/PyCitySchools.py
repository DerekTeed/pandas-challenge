# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete
#student_data.head()
#school_data_complete.head()

#Calculate the total number of schools for District, correct.
schoolCount = school_data.loc[(school_data['type'] == 'District')]
schoolCount = schoolCount["school_name"].count()
#schoolCount

#Calculate student total for district, correct.
districtDataComplete = school_data_complete.loc[(school_data_complete['type'] == 'District')]
studentCount = districtDataComplete["Student ID"].count()
#studentCount

#total budget for District schools only, correct but need to exclude the table output and just get the number
distinctSchools = school_data_complete.loc[:,["budget"]].drop_duplicates()
#distinctSchools = distinctSchools.loc[(distinctSchools['type'] == 'District')].drop_duplicates()
#distinctSchools
sumDistinctSchoolsBudget = distinctSchools.sum()
sumDistinctSchoolsBudget

#Calculate Math Scores for the District only, correct
avgMathScore = (districtDataComplete['math_score'].sum()/studentCount)/ 100
avgMathScore = "{:.2%}".format(avgMathScore)
#avgMathScore

#average math score for the District only. correct
avgReadingScore = (districtDataComplete['reading_score'].sum()/studentCount)
avgReadingScore = "{:.4}".format(avgReadingScore)
#avgReadingScore

#Calculate the percentage of students with a passing math score (70 or greater), correct but a string, not percent
#Good math score here with 26976 total math students
mathScore = districtDataComplete['math_score']#.count()
mathScore = districtDataComplete.loc[(districtDataComplete['math_score'] >= 70)]
mathScore70up = mathScore['Student ID'].count()  #17944
percMath70up = (mathScore70up/studentCount)
percMath70up = "{:.2%}".format(percMath70up)
#percMath70up

#Calculate the percentage of students with a passing math score (70 or greater), correct but a string, not percent
#Good math score here with 26976 total math students
readingScore = districtDataComplete['reading_score'].count() #26976
#readingScore
readingScore = districtDataComplete.loc[(districtDataComplete['reading_score'] >= 70)]
readingScore70up = readingScore['Student ID'].count()  #21825
readingScore70up
percReading70up = (readingScore70up/studentCount)
percReading70up = "{:.2%}".format(percReading70up)
#percReading70up

#Calculate the percentage of students who passed math and reading (% Overall Passing). Correct but string not percent
mathRow = districtDataComplete.loc[(districtDataComplete['math_score'] >= 70)]
readingRow = districtDataComplete.loc[(districtDataComplete['reading_score'] >= 70)]
mergeMathReading = pd.merge(mathRow, readingRow, how="inner", on=["Student ID", "Student ID"])
mergeMathReading = mergeMathReading['Student ID'].count()
mathReadPassPerc = mergeMathReading/studentCount
mathReadPassPerc = "{:.2%}".format(mathReadPassPerc)
#mathReadPassPerc


summary_df = pd.DataFrame({
"Total Schools": schoolCount,
"Total Students": studentCount,
"Total Budget": sumDistinctSchoolsBudget,
"Average Math Score": avgMathScore,
"Average Reading Score": avgReadingScore,
"% Passing Math": percMath70up,
"% Passing Reading": percReading70up,
"% Overall Passing": mathReadPassPerc
})
summary_df


schoolGroup = school_data_complete.loc[:,['school_name', 'type','Student ID','reading_score','math_score','budget', 'type']]

schoolGroup = schoolGroup.groupby(['school_name'])
schoolGroup1 = schoolGroup['Student ID'].count()
# #schoolGroup1["perStudentBudget"] = schoolGroup
schoolGroup1 = pd.DataFrame(schoolGroup1)
schoolGroup1['Student Count'] = schoolGroup1['Student ID']
del schoolGroup1['Student ID']

# #Average math Score, Correct
schoolGroup1['Avg Math'] = schoolGroup["math_score"].mean()
schoolGroup1["Avg Math"] = schoolGroup1["Avg Math"].astype(float).map("{:.2f}".format)

# #Average Reading Score, Correct
schoolGroup1['Avg Reading'] = schoolGroup["reading_score"].mean()
schoolGroup1["Avg Reading"] = schoolGroup1["Avg Reading"].astype(float).map("{:.2f}".format)

#Total Budget, correct
schoolGroup1['Total Budget'] = schoolGroup['budget'].max()

#Per Student Budget
schoolGroup1['Budget Per Student'] = schoolGroup1['Total Budget']/schoolGroup1['Student Count']
schoolGroup1['Budget Per Student'] = schoolGroup1['Budget Per Student'].astype(float).map("{:.2f}".format)

#Average Passing Math # for avg math score >70
pass_math = school_data_complete.loc[(school_data_complete['math_score'] > 70)]
pass_math = pass_math.groupby(['school_name']).count()
schoolGroup1['pass math'] = (pass_math['Student ID']/schoolGroup1['Student Count'])*100
schoolGroup1['pass math'] = schoolGroup1['pass math'].map("{:.2f}%".format)

pass_read = school_data_complete.loc[(school_data_complete['reading_score'] > 70)]
pass_read = pass_read.groupby(['school_name']).count()
schoolGroup1['pass reading'] = (pass_read['reading_score']/schoolGroup1['Student Count'])*100
schoolGroup1['pass reading'] = schoolGroup1['pass reading'].map("{:.2f}%".format)

both_pass = school_data_complete.loc[(school_data_complete['reading_score'] > 70) & (school_data_complete['math_score'] > 70)]
both_pass = both_pass.groupby(['school_name']).count()
schoolGroup1['Pass Read/Math'] = (both_pass['reading_score']/schoolGroup1['Student Count'])*100
schoolGroup1['Pass Read/Math'] = schoolGroup1['Pass Read/Math'].map("{:.2f}%".format)
print(schoolGroup1)


#top5 school overall passing, Cannot differential type
#schoolGroup['Type'] = schoolGroup['type']
schoolGroup2 = pd.DataFrame(schoolGroup1)
schoolGroup2['type'] = school_data['type'].max()
top_five = schoolGroup2.sort_values(['Pass Read/Math'],ascending=False)
#top_five.head()

bottom_five = schoolGroup2.sort_values(['Pass Read/Math'],ascending=True)
print(bottom_five.head())


#Math Scores by Grade
grade_group9 = school_data_complete.loc[(school_data_complete['grade'] == '9th')]
grade_group10 = school_data_complete.loc[(school_data_complete['grade'] == '10th')]
grade_group11 = school_data_complete.loc[(school_data_complete['grade'] == '11th')]
grade_group12 = school_data_complete.loc[(school_data_complete['grade'] == '12th')]

grade_group9 = grade_group9.groupby(['school_name'])
grade_group10 = grade_group10.groupby(['school_name'])
grade_group11 = grade_group11.groupby(['school_name'])
grade_group12 = grade_group12.groupby(['school_name'])

# schoolGroup1['Student Count'] = schoolGroup1['Student ID'] This gives me what I need,but no anme on top
grade_group9 = grade_group9['math_score'].mean()
grade_group10 = grade_group10['math_score'].mean()
grade_group11 = grade_group11['math_score'].mean()
grade_group12 = grade_group12['math_score'].mean()

school_grade_df = pd.DataFrame(grade_group9)
school_grade_df['9th Grade'] = school_grade_df['math_score']
school_grade_df['10th grade'] = grade_group10
school_grade_df['11th grade'] = grade_group11
school_grade_df['12th grade'] = grade_group12
del school_grade_df['math_score']
print(school_grade_df)

# Reading Scores
grade_group9 = school_data_complete.loc[(school_data_complete['grade'] == '9th')]
grade_group10 = school_data_complete.loc[(school_data_complete['grade'] == '10th')]
grade_group11 = school_data_complete.loc[(school_data_complete['grade'] == '11th')]
grade_group12 = school_data_complete.loc[(school_data_complete['grade'] == '12th')]

grade_group9 = grade_group9.groupby(['school_name'])
grade_group10 = grade_group10.groupby(['school_name'])
grade_group11 = grade_group11.groupby(['school_name'])
grade_group12 = grade_group12.groupby(['school_name'])

grade_group9 = grade_group9['reading_score'].mean()
grade_group10 = grade_group10['reading_score'].mean()
grade_group11 = grade_group11['reading_score'].mean()
grade_group12 = grade_group12['reading_score'].mean()

school_grade_df2 = pd.DataFrame(grade_group9)
school_grade_df2['9th Grade'] = school_grade_df2['reading_score']
school_grade_df2['10th grade'] = grade_group10
school_grade_df2['11th grade'] = grade_group11
school_grade_df2['12th grade'] = grade_group12
del school_grade_df2['reading_score']
print(school_grade_df2)

school_perf_df= pd.DataFrame(schoolGroup1)

school_perf_df['pass math'] = schoolGroup1['pass math'].map("{:.4}".format)
school_perf_df['pass reading'] = schoolGroup1['pass reading'].map("{:.4}".format)
#budget = budget[1:]
budget = schoolGroup1['Budget Per Student']
budget = budget.astype(float)
#sum1 = pd.to_numeric(sum1)
sum1 = school_perf_df['pass math']
sum2 = school_perf_df['pass reading']
#budget = school_perf_df['Budget Per Student']
budget = pd.to_numeric(budget)
sum1 = pd.to_numeric(sum1)
sum2 = pd.to_numeric(sum2)
#type(sum2[1])
sums = (sum1 + sum2)/2
school_perf_df['Avg Passing'] = sums.map("{:.3}%".format)
school_perf_df['Budget Per Student'] = budget.map("{:.4}".format)

bins = [0, 584, 629, 644, 675]
group_labels = ["$0-$584", "$585-$629", "$630-$644", "$645-$675"]
school_perf_df["Spending Groups"] = pd.cut(budget, bins, labels=group_labels, include_lowest=True)

del school_perf_df['Student Count']
del school_perf_df['Total Budget']
del school_perf_df['Pass Read/Math']
del school_perf_df['type']

print(school_perf_df)