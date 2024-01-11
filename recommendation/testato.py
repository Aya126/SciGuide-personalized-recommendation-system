import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot
from scipy.sparse import csr_matrix
from sklearn.metrics import precision_score
from sklearn.metrics.pairwise import cosine_similarity

df= pd.read_excel('C:/Users/ayaas/OneDrive/Desktop/project/Registations.xlsx')
df['GradeID'] = df['GradeID'].astype(int)
df.drop(df[ (df['GradeID'] >= 12) | ( df['GradeID'] <= 0 ) ].index, inplace = True)
df['GradeID'] = 11 - df['GradeID']

Prerequisits= pd.read_excel('C:/Users/ayaas/OneDrive/Desktop/project/Prerequisits.xlsx')
M_M = pd.read_excel('C:/Users/ayaas/OneDrive/Desktop/project/Student_major_minor.xlsx')
Courses_in_spe= pd.read_excel('C:/Users/ayaas/OneDrive/Desktop/project/Courses_in_speciality.xlsx')
Offering= pd.read_excel('C:/Users/ayaas/OneDrive/Desktop/project/Offering.xlsx')



def predict(ID):
    ID = int(ID)

    # Convert random grades to meaningful grades

    Student = df.loc[df["SID2"] == ID]

    Semester = Student["Semester"].unique()
    df_train = Student[Student["Semester"] < Semester[-1]]

    offer = pd.read_excel('C:/Users/ayaas/OneDrive/Desktop/project/طرح المقررات.xlsx', sheet_name=str(Semester[-1]))

    student_courses = df_train['Course']
    student_grades = df_train['GradeID'].tolist()

    # Get Courses' Names
    IDs_Name_Courses = Offering
    IDs_Name_Courses = IDs_Name_Courses.drop(
        ['Semester', 'Credit'], axis=1).drop_duplicates()

    # Student => Major , Minor and Major and Minor Courses
    Major = M_M[M_M["SID"] == ID]["Major"]
    Minor = M_M[M_M["SID"] == ID]["Minor"]
    Major = Major.values.astype(int)[0]
    Minor = Minor.values.astype(int)[0]

    Major_courses = Courses_in_spe[Courses_in_spe["Specialty"]
                                   == Major]["Course"].unique().tolist()
    Minor_courses = Courses_in_spe[Courses_in_spe["Specialty"]
                                   == Minor]["Course"].unique().tolist()
    Major_Minor_Courses = Minor_courses + \
        list(set(Major_courses)-set(Minor_courses))

    # Get the offering for this specific student
    Major_Minor_offer = offer[offer["Course"].isin(Major_Minor_Courses)]
    Major_Minor_offer = Major_Minor_offer[~Major_Minor_offer['Course'].isin(
        student_courses.tolist())]
    prerequisits_Courses_offer = Prerequisits[Prerequisits["PrerequisitID"].isin(
        Major_Minor_Courses)]

    x = prerequisits_Courses_offer[prerequisits_Courses_offer["CourseID"].isin(
        Major_Minor_offer['Course'].tolist())]

    x = x[~x['PrerequisitID'].isin(student_courses.tolist())]
    offer_final = Major_Minor_offer[Major_Minor_offer.Course.isin(
        x["CourseID"].tolist()) == False]

    # Get the complusory and Major courses and specialty for student
    final = offer_final.merge(
        Courses_in_spe, "left", left_on='Course', right_on='Course').replace(np.nan,  0)
    if Major == Minor:
        final = final[final["Specialty"] == Major]
        final = final[final["IsMajor"] == 2].sort_values(
            "IsCompulsory", ascending=False)
    else:
        courses_Major = final[final["Specialty"] == Major]
        courses_Minor = final[final["Specialty"] == Minor]
        courses_Major = courses_Major[final["IsMajor"] == 1].sort_values(
            "IsCompulsory", ascending=False)
        courses_Minor = courses_Minor[final["IsMajor"] == 0].sort_values(
            "IsCompulsory", ascending=False)
        final = pd.concat([courses_Major, courses_Minor])

    # Get The year of the courses
    final['Year'] = final['Course'].astype(str).str[-3]

    # Get the most frequent Semester
    all_offering = pd.read_excel('C:/Users/ayaas/OneDrive/Desktop/project/Offering.xlsx')
    all_offering['Term'] = all_offering['Semester'].astype(str).str[-1]
    frequent_semester = pd.DataFrame(all_offering.groupby(
        'Course Name')['Term'].agg(pd.Series.mode))
    final = final.merge(frequent_semester, "left", left_on='إسم المقرر',
                        right_on='Course Name').replace(np.nan,  0)

    # Get the frequent Grade for each course
    most_freq_grade = pd.DataFrame(df.groupby(
        'Course').GradeID.agg(pd.Series.mode))
    for i in range(0, len(most_freq_grade['GradeID'])):
        most_freq_grade['GradeID'].iloc[i] = most_freq_grade['GradeID'].iloc[i].max()

    final = final.merge(most_freq_grade, "left", left_on='Course',
                        right_on='Course').replace(np.nan,  0)

    # Get number of mandatory opened courses
    if Major == Minor:
        mandatory_courses = Courses_in_spe[Courses_in_spe["Specialty"] == Major]
        mandatory_courses = mandatory_courses[mandatory_courses["IsMajor"] == 2]
        mandatory_courses = mandatory_courses[mandatory_courses["IsCompulsory"] == 1]
    else:
        mandatory_courses_Major = Courses_in_spe[Courses_in_spe["Specialty"] == Major]
        mandatory_courses_Major = mandatory_courses_Major[mandatory_courses_Major["IsMajor"] == 1]
        mandatory_courses_Major = mandatory_courses_Major[mandatory_courses_Major["IsCompulsory"] == 1]
        mandatory_courses_Minor = Courses_in_spe[Courses_in_spe["Specialty"] == Minor]
        mandatory_courses_Minor = mandatory_courses_Minor[mandatory_courses_Minor["IsMajor"] == 0]
        mandatory_courses_Minor = mandatory_courses_Minor[mandatory_courses_Minor["IsCompulsory"] == 1]
        mandatory_courses = pd.concat(
            [mandatory_courses_Major, mandatory_courses_Minor])
        mandatory_courses = mandatory_courses.drop_duplicates()

    # Get the number/names/Credit of open courses for each course
    prerequisits_courses = Prerequisits[Prerequisits['PrerequisitID'].isin(
        final['Course'].tolist())]
    prerequisits_courses = prerequisits_courses.drop(
        ['PrerequisitGroup', 'TakeTogether'], axis=1)
    prerequisits_courses = prerequisits_courses.merge(
        IDs_Name_Courses, "left", left_on='CourseID', right_on='Course').replace(np.nan,  0)
    prerequisits_courses = prerequisits_courses.drop(['Course'], axis=1)
    prerequisits_courses = prerequisits_courses[prerequisits_courses["Course Name"] != 0]

    prerequisits_courses['Types'] = -1
    prerequisits_courses.loc[prerequisits_courses['CourseID'].isin(
        list(set(Major_Minor_Courses))), ['Types']] = 0
    prerequisits_courses.loc[prerequisits_courses['CourseID'].isin(
        mandatory_courses['Course'].tolist()), ['Types']] = 1
    prerequisits_courses = prerequisits_courses.merge(
        Offering, "left", left_on='CourseID', right_on='Course')
    prerequisits_courses = prerequisits_courses.drop(
        columns=['Course', 'Semester', 'Course Name_y'], axis=1)
    prerequisits_courses.rename(
        columns={'Course Name_x': 'Course Name', 'Credit': 'Opened Credit'}, inplace=True)
    prerequisits_courses = prerequisits_courses.drop_duplicates()

    opened_courses = prerequisits_courses.groupby('PrerequisitID')[
        'CourseID'].count()
    Name_open_courses = (prerequisits_courses.groupby(['PrerequisitID'])).agg(
        {'Course Name': lambda x: x.tolist()}).reset_index()
    Name_open_courses.rename(
        columns={'Course Name': 'opened courses'}, inplace=True)
    all_types = prerequisits_courses.groupby(['PrerequisitID']).agg(
        {'Types': lambda x: x.tolist()}).reset_index()
    all_credit = prerequisits_courses.groupby(['PrerequisitID']).agg(
        {'Opened Credit': lambda x: x.tolist()}).reset_index()
    Name_open_courses = Name_open_courses.merge(
        all_types, "left", left_on='PrerequisitID', right_on='PrerequisitID')
    Name_open_courses = Name_open_courses.merge(
        all_credit, "left", left_on='PrerequisitID', right_on='PrerequisitID')

    final = final.merge(Name_open_courses, "left",
                        left_on='Course', right_on='PrerequisitID')

    final['opened courses'] = [
        [] if x is np.NaN else x for x in final['opened courses']]

    final['Types'] = [[] if x is np.NaN else x for x in final['Types']]

    final['Opened Credit'] = [
        [] if x == 0 else x for x in final['Opened Credit']]

    final = final.merge(opened_courses, "left", left_on='Course',
                        right_on='PrerequisitID').replace(np.nan,  0)
    final.rename(
        columns={'CourseID': 'Number of opened courses'}, inplace=True)

    # Get the number of Mandatory Courses
    final['Number Mandatory'] = 0
    for i in range(0, len(final['Course'])):
        final['Number Mandatory'][i] = final['Types'][i].count(1)

    # # Item_based
    coursematrix = df.pivot_table(
        index=['Course'], columns='SID2', values='GradeID')
    coursematrix[coursematrix >= 0] = 1
    coursematrix = coursematrix.replace(np.nan,  0)

    cos_sim = cosine_similarity(coursematrix)

    cosine_sim = pd.DataFrame(
        cos_sim, columns=coursematrix.index, index=coursematrix.index)

    sumOfSimilarities = pd.DataFrame(cosine_sim.sum())
    sumOfSimilarities.rename(columns={0: "Similarty"}, inplace=True)

    sim_prev_courses = cosine_sim[student_courses]
    sim_times_grade = sim_prev_courses * student_grades
    sim_sum = sim_prev_courses.sum(axis=1)
    sim_times_grade_sum = sim_times_grade.sum(axis=1)

    r = sim_times_grade_sum / sim_sum

    score_r = r.drop(student_courses.tolist()).sort_values(ascending=False)
    

    score = score_r.loc[final['Course']]
    score.name = 'score'

    final=final.merge(score,"left", on='Course')
    final= final.drop_duplicates(subset=['Course', 'IsMajor'])

    # Spliting courses

    courses_mandatroy = final[final['IsCompulsory'] == 1]
    courses_NOT_mandatroy = final[final['IsCompulsory'] == 0]
    courses_mandatroy = courses_mandatroy.sort_values(['Number Mandatory', 'Year', 'Number of opened courses'], ascending=[False, True, False])
    courses_NOT_mandatroy = courses_NOT_mandatroy.sort_values(['GradeID', 'Year', 'Number of opened courses'], ascending=[False, True, False])

    courses_man = []
    x = courses_mandatroy.to_dict('records')

    for course in x:
        # all_opened_info = zip([course['opened courses']],[course['Types']],[course['Opened Credit']])
        all_opened_info = list(zip(course['opened courses'], 
                                   course['Types'], 
                                   [] if course['Opened Credit'] == 0 else course['Opened Credit']
                                )
                            )
        
        print(all_opened_info)
        courses_man.append({
            'name': course['إسم المقرر'],
            'id': course['Course'],
            'credit': course['credit'],
            'program' : course['IsMajor'],
            'opens': int(course['Number of opened courses']),
            'Semester': course['Term'],
            'openedCourses': all_opened_info,
            # 'openedcourses': course['opened courses'],
            # 'Types': course['Types'],
            # 'OpenedCredit': course['Opened Credit'],
            'NumberMandatory': course['Number Mandatory'],
            'Grade': int(course['GradeID']),
            'Score': course['score'],
        })

    courses_not_man = []
    y = courses_NOT_mandatroy.to_dict('records')

    for course in y:
        all_opened_info = list(zip(course['opened courses'], 
                                   course['Types'], 
                                   [] if course['Opened Credit'] == 0 else course['Opened Credit']
                                )
                            )


        courses_not_man.append({

            'name': course['إسم المقرر'],
            'id': course['Course'],
            'credit': course['credit'],
            'program' : course['IsMajor'],
            'opens': int(course['Number of opened courses']),
            'Semester': course['Term'],
            'openedCourses': all_opened_info,
            # 'openedcourses': course['opened courses'],
            # 'Types': course['Types'],
            # 'OpenedCredit': course['Opened Credit'],
            'NumberMandatory': course['Number Mandatory'],
            'Grade': int(course['GradeID']),
            'Score': course['score'],



        })

    return courses_man,  courses_not_man

#  prediction=list(map(str,x))
# x=predict(80804131541)
# print(x)
