import csv
import pandas as pd
import numpy as np
from joblib import load
from sklearn.svm import SVR


def convert_to_csv(row):
    headers = ['name', 'enrollment number', 'sex', 'age', 'address', 'family size', 'parental cohabitation status', 'medu', 'fedu', 'mjob', 'fjob', 'reason', 'guardian', 'traveltime', 'studytime', 'failures', 'school support', 'family support', 'extra activities', 'nursery', 'higher', 'internet', 'family relationship', 'freetime', 'goout', 'health', 'absences', 'mid sem marks', 'end sem marks', 'attendance rate', 'class participation',
               'motivation', 'self-discipline', 'teacher quality', 'time management', 'peer influence', 'parental involvement', 'teacher-student relationship', 'stress levels', 'mental health', 'goal setting', 'learning resources', 'group study', 'time spent on homework', 'subject interest', 'classroom environment', 'test preparation', 'time spent on extracurricular activities', 'workload', 'degree', 'subject', 'subject code', 'semester']

    csv_filename = 'files/'+str(row.enrollment_number)+'.csv'

    subjects = row.subjects.split(',')
    subjects_codes = row.subjects_codes.split(',')

    with open(csv_filename, mode='w+', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        for subject, subject_code in zip(subjects, subjects_codes):
            writer.writerow([
                row.user.name,
                row.enrollment_number,
                row.sex,
                row.age,
                row.address,
                row.family_size,
                row.parent_status,
                row.mother_education,
                row.father_education,
                row.mother_job,
                row.father_job,
                row.reason,
                row.guardian,
                row.travel_time,
                row.study_time,
                row.failures,
                row.school_support,
                row.family_support,
                row.extra_activities,
                row.nursery,
                row.higher,
                row.internet,
                row.family_relationship,
                row.free_time,
                row.go_out,
                row.health,
                row.absences,
                row.mid_sem_marks,
                row.end_sem_marks,
                row.attendance_rate,
                row.class_participation,
                row.motivation,
                row.self_discipline,
                row.teacher_quality,
                row.time_management,
                row.peer_influence,
                row.parental_involvement,
                row.teacher_student_relationship,
                row.stress_level,
                row.mental_health,
                row.goal_setting,
                row.learning_resources,
                row.group_study,
                row.time_spent_on_homework,
                row.subject_interest,
                row.classroom_environment,
                row.test_preparation,
                row.time_spent_on_extracurricular_activities,
                row.workload,
                row.degree,
                # row.subjects,
                # row.subjects_codes,
                subject,
                subject_code,
                row.semester
            ])

    return csv_filename


def predict_grade(filename):
    # Load the saved model
    model1 = load(
        'core\\utils\\models_grade\\support_vector_regression.joblib')
    model2 = load('core\\utils\\models_grade\\random_forest.joblib')
    model3 = load('core\\utils\\models_grade\\elastic_net.joblib')
    model4 = load('core\\utils\\models_grade\\gradient_boosting.joblib')
    model5 = load('core\\utils\\models_grade\\extra_trees.joblib')
    model6 = load('core\\utils\\models_grade\\linear_regression.joblib')

    # Load and preprocess the new data
    stud = pd.read_csv(filename)
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    stud.iloc[:, 0] = le.fit_transform(stud.iloc[:, 0])
    stud.iloc[:, 1] = le.fit_transform(stud.iloc[:, 1])
    stud.iloc[:, 3] = le.fit_transform(stud.iloc[:, 3])
    stud.iloc[:, 4] = le.fit_transform(stud.iloc[:, 4])
    stud.iloc[:, 5] = le.fit_transform(stud.iloc[:, 5])
    stud.iloc[:, 8] = le.fit_transform(stud.iloc[:, 8])
    stud.iloc[:, 9] = le.fit_transform(stud.iloc[:, 9])
    stud.iloc[:, 10] = le.fit_transform(stud.iloc[:, 10])
    stud.iloc[:, 11] = le.fit_transform(stud.iloc[:, 11])
    stud.iloc[:, 15] = le.fit_transform(stud.iloc[:, 15])
    stud.iloc[:, 16] = le.fit_transform(stud.iloc[:, 16])
    stud.iloc[:, 17] = le.fit_transform(stud.iloc[:, 17])
    stud.iloc[:, 18] = le.fit_transform(stud.iloc[:, 18])
    stud.iloc[:, 19] = le.fit_transform(stud.iloc[:, 19])
    stud.iloc[:, 20] = le.fit_transform(stud.iloc[:, 20])
    stud.iloc[:, 21] = le.fit_transform(stud.iloc[:, 21])
    stud.iloc[:, 22] = le.fit_transform(stud.iloc[:, 22])
    stud = stud.drop(['mid sem marks'], axis='columns')

    stud = stud.drop('end sem marks', axis=1)

    # Make predictions using the loaded model
    # print(stud.columns)
    # Create a list of column names in the desired order
    desired_order = ['classroom environment', 'address', 'fjob', 'school support', 'semester', 'higher', 'teacher-student relationship', 'mjob', 'teacher quality', 'freetime', 'failures', 'fedu', 'subject interest', 'self-discipline', 'parental involvement', 'time spent on extracurricular activities', 'workload', 'age', 'medu', 'absences', 'health', 'learning resources',
                     'family support', 'mental health', 'name', 'time management', 'goal setting', 'family size', 'attendance rate', 'group study', 'extra activities', 'time spent on homework', 'stress levels', 'traveltime', 'internet', 'studytime', 'motivation', 'test preparation', 'peer influence', 'family relationship', 'nursery', 'reason', 'enrollment number', 'class participation', 'goout']

    # Create a new DataFrame with columns in the desired order
    df_new = stud[desired_order]
    predictions = model1.predict(df_new)
    predictions1 = model2.predict(df_new)
    predictions2 = model3.predict(df_new)
    predictions3 = model4.predict(df_new)
    predictions4 = model5.predict(df_new)
    predictions5 = model6.predict(df_new)

    # Print the predictions
    print(predictions)
    print(predictions1)
    print(predictions2)
    print(predictions3)
    print(predictions4)
    print(predictions5)

    max_marks = 70

    # Rescale the predicted value to the range of 0 to max_marks
    predicted_marks = predictions[0] * (max_marks/100)
    predicted_marks1 = predictions1[0] * (max_marks/100)
    predicted_marks2 = predictions2[0] * (max_marks/100)
    predicted_marks3 = predictions3[0] * (max_marks/100)
    predicted_marks4 = predictions4[0] * (max_marks/100)
    predicted_marks5 = predictions5[0] * (max_marks/100)
    # Round the predicted value to the nearest integer
    predicted_marks = round(predicted_marks)
    predicted_marks1 = round(predicted_marks1)
    predicted_marks2 = round(predicted_marks2)
    predicted_marks3 = round(predicted_marks3)
    predicted_marks4 = round(predicted_marks4)
    predicted_marks5 = round(predicted_marks5)

    # # Display the rescaled predicted value
    # print("The predicted end sem marks is:", predicted_marks)
    # print("The predicted end sem marks is:", predicted_marks1)
    # print("The predicted end sem marks is:", predicted_marks2)
    # print("The predicted end sem marks is:", predicted_marks3)
    # print("The predicted end sem marks is:", predicted_marks4)
    # print("The predicted end sem marks is:", predicted_marks5)

    return predicted_marks, predicted_marks1, predicted_marks2, predicted_marks3, predicted_marks4, predicted_marks5