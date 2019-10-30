"""
Project 4C
Canvas Analyzer
CISC108 Honors
Fall 2019

Access the Canvas Learning Management System and process learning analytics.

Edit this file to implement the project.
To test your current solution, run the `test_my_solution.py` file.
Refer to the instructions on Canvas for more information.

"I have neither given nor received help on this assignment."
author: Matthew Weis
"""
import canvas_requests
import datetime
import matplotlib.pyplot as plt
__version__ = 7

# 1) main
# 2) print_user_info
# 3) filter_available_courses
# 4) print_courses
# 5) get_course_ids
# 6) choose_course
# 7) summarize_points
# 8) summarize_groups
# 9) plot_scores
# 10) plot_grade_trends

# Keep any function tests inside this IF statement to ensure
# that your `test_my_solution.py` does not execute it.


def print_user_info(user_dict: dict):
    #Prints out basic information for the user
    print("Name:", user_dict['name'])
    print("Title:", user_dict['title'])
    print("Primary Email:", user_dict['primary_email'])
    print("Bio:", user_dict['bio'])

def filter_available_courses(course_list):
    #Returns all of the user's available canvas courses
    available_courses = []
    for course in course_list:
        if course['workflow_state'] == "available":
            available_courses.append(course)
    return available_courses

def print_courses(course_list):
    #Prints all of the users courses
    for course in course_list:
        print(course['id'], ":", course['name'])

def get_course_ids(course_list):
    #Returns a list containing all of the user's canvas courses' ID's
    course_id = []
    for course in course_list:
        course_id.append(course['id'])
    return course_id

def choose_course(course_ids):
    #Asks the user for to input a valid course ID and returns the chosen ID
    selected_course_id = int(input("Please enter a valid course id"))
    while selected_course_id not in course_ids:
        selected_course_id = int(input("Please enter a valid course id"))
    for id in course_ids:
        if id == selected_course_id:
            return id

def summarize_points(submissions):
    #Consumes a list of submission dictionaries and prints out the total amount of points possible, the points obtained,
    #and the current grade for the course
    possible_point_sum = 0
    submission_points = 0
    for assignment in submissions:
        if assignment['score'] != None:
            possible_point_sum = possible_point_sum + (assignment['assignment']['points_possible']*
                                                       assignment['assignment']['group']['group_weight'])
            submission_points = submission_points + (assignment['score']*assignment['assignment']['group']['group_weight'])
    print("Points Possible so far:", possible_point_sum)
    print("Points Obtained", submission_points)
    print("Current Grade:", round(100*(submission_points/possible_point_sum)))

def summarize_groups(submissions):
    #Consumes a List of submission dictionaries and prints out the name and unweighted grade for each group
    counts = {}
    possible = {}
    running_weight = 0
    for submission in submissions:
        if submission['score'] != None:
            if submission['assignment']['group']['name'] not in counts:
                counts[submission['assignment']['group']['name']] = submission['score']
                possible[submission['assignment']['group']['name']] = submission['assignment']['points_possible']
            else:
                counts[submission['assignment']['group']['name']] = counts[submission['assignment']['group']['name']] + submission['score']
                possible[submission['assignment']['group']['name']] = possible[submission['assignment']['group']['name']] + submission['assignment']['points_possible']
    for key in counts:
        print(key, ":", round(100*counts[key]/possible[key]))

def plot_scores(submissions):
    #Consumes a list of submission dictionaries and plots each submission grade on a bar graph
    scores = []
    for submission in submissions:
        if submission['score'] != None and submission['assignment']['points_possible'] != 0:
            scores.append(100*submission['score']/submission['assignment']['points_possible'])
    plt.hist(scores)
    plt.title("Distribution of Grades")
    plt.xlabel("Grades")
    plt.ylabel("Number of Assignments")
    plt.show()

def plot_grade_trends(submissions):
    #Consumes a list of Submission dictionaries and plots the grade trend of the submissions as a line plot
    print(submissions)
    max_points = 0
    max_points_list = []
    running_max_points_list = []
    final_max_points_list = []
    running_sum_max = 0
    low_points = 0
    low_points_list = []
    running_low_points_list = []
    final_low_points_list = []
    running_sum_low = 0
    high_points = 0
    high_points_list = []
    running_high_points_list = []
    final_high_points_list = []
    submissions_times = []
    running_sum_high = 0
    max_score = 0
    for submission in submissions:
        max_points = 100 * submission['assignment']['points_possible'] \
                     * submission['assignment']['group']['group_weight']
        max_points_list.append(max_points)
        if submission['score'] == None:
            low_points = 0
            high_points = 100 * submission['assignment']['points_possible'] * submission['assignment']['group']['group_weight']
            low_points_list.append(low_points)
            high_points_list.append(high_points)
        elif submission['score'] != None:
            low_points = 100 * submission['score'] * submission['assignment']['group']['group_weight']
            high_points = low_points
            low_points_list.append(low_points)
            high_points_list.append(high_points)
    for point in max_points_list:
        running_sum_max = running_sum_max + point
        running_max_points_list.append(running_sum_max)
    for point in low_points_list:
        running_sum_low = running_sum_low + point
        running_low_points_list.append(running_sum_low)
    for point in high_points_list:
        running_sum_high = running_sum_high + point
        running_high_points_list.append(running_sum_high)
    max_score = running_sum_max / 100
    for point in running_max_points_list:
        final_max_points_list.append(point / max_score)
    for point in running_low_points_list:
        final_low_points_list.append(point / max_score)
    for point in running_high_points_list:
        final_high_points_list.append(point / max_score)
    for submission in submissions:
        submission_time = datetime.datetime.strptime(submission['assignment']['due_at'], "%Y-%m-%dT%H:%M:%SZ")
        submissions_times.append(submission_time)
    plt.plot(submissions_times, final_high_points_list, label="Highest")
    plt.plot(submissions_times, final_low_points_list, label="Lowest")
    plt.plot(submissions_times, final_max_points_list, label="Maximum")
    plt.title("Grade Trend")
    plt.ylabel("Grade")
    plt.legend()
    plt.show()

def main(name):
    #The main function, executes all the other functions
    print_user_info(canvas_requests.get_user(name))
    print_courses(canvas_requests.get_courses(name))
    courses = filter_available_courses(canvas_requests.get_courses(name))
    course_ids = get_course_ids(canvas_requests.get_courses(name))
    selected_course = choose_course(course_ids)
    summarize_points(canvas_requests.get_submissions(name, selected_course))
    summarize_groups(canvas_requests.get_submissions(name, selected_course))
    plot_scores(canvas_requests.get_submissions(name, selected_course))
    plot_grade_trends(canvas_requests.get_submissions(name, selected_course))

if __name__ == "__main__":
    main('hermione')
    # main('ron')
    # main('harry')

    # https://community.canvaslms.com/docs/DOC-10806-4214724194
    # main('YOUR OWN CANVAS TOKEN (You know, if you want)')
