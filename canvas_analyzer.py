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
    print("Name:", user_dict['name'])
    print()
    print("Title:", user_dict['title'])
    print()
    print("Email:", user_dict['primary_email'])
    print()
    print("Bio:", user_dict['bio'])
    print()
def filter_available_courses(course_list):
    for course in course_list:
        course['workflow_state'] = "available"
    return course_list
def print_courses(course_list):
    for course in course_list:
        print("Course name:", course['name'])
        print("Course ID:", course['id'])
        print()
def get_course_ids(course_list):
    course_id = []
    for course in course_list:
        course_id.append(course['id'])
    return course_id
def choose_course(course_ids):
    selected_course_id = int(input("Please enter a valid course id"))
    while selected_course_id not in course_ids:
        selected_course_id = int(input("Please enter a valid course id"))
    for id in course_ids:
        if id == selected_course_id:
            return id
def summarize_points(submissions):
    possible_point_sum = 0
    submission_points = 0
    group_weight = 0
    for assignment in submissions:
        if assignment['score'] == None:
            pass
        else:
            possible_point_sum = possible_point_sum + assignment['assignment']['points_possible']
            submission_points = submission_points + assignment['score']
            group_weight = group_weight + assignment['assignment']['group']['group_weight']
    print()
    print("Possible Points:", possible_point_sum * group_weight)
    print("Points Obtained", submission_points*group_weight)
    print("Current Grade:", 100*(submission_points/possible_point_sum))
    print()
def summarize_groups(submissions):
    for submission in submissions:
        print("Group:", submission['assignment']['group']['name'])
        if submission['score'] == None:
            print("No Grade")
            print()
        else:
            print("Grade", 100*submission['score']/submission['assignment']['group']['group_weight'])
            print()
def plot_scores(submissions):
    scores = []
    for submission in submissions:
        if submission['score'] != None:
            scores.append(100*submission['score']/submission['assignment']['points_possible'])
    plt.hist(scores)
    plt.title("Grade Distribtions")
    plt.xlabel("Grades")
    plt.ylabel("Number of Assignments")
    plt.show()
def plot_grade_trends(submissions):
    print(submissions)
    max_points = 0
    max_points_list = []
    running_sum_max = 0
    low_points = 0
    low_points_list = []
    running_sum_low = 0
    high_points = 0
    high_points_list = []
    running_sum_high = 0
    max_score = 0
    for submission in submissions:
        max_points = 100 * submission['assignment']['points_possible'] \
                     * submission['assignment']['group']['group_weight']
        max_points_list.append(max_points)
        if submission['score'] == None:
            low_points = 0
            high_points = submission['assignment']['points_possible']
            low_points_list.append(low_points)
            high_points_list.append(high_points)
        elif submission['score'] != None:
            low_points = 100 * submission['score'] * submission['assignment']['group']['group_weight']
            high_points = low_points
            low_points_list.append(low_points)
            high_points_list.append(high_points)
    for point in max_points_list:
        running_sum_max = running_sum_max + point
    for point in low_points_list:
        running_sum_low = running_sum_low + point
    for point in high_points_list:
        running_sum_high = running_sum_high + point
    max_score = running_sum_max / 100
    print(running_sum_max)
    print(running_sum_low)
    print(running_sum_high)
    print(max_score)
    for point in max_points_list:
        point = point / max_score
    for point in low_points_list:
        point = point / max_score
    for point in high_points_list:
        point = point / max_score
    plt.plot(high_points_list, label="High")
    plt.plot(low_points_list, label="Low")
    plt.plot(max_points_list, label="Max")
    plt.title("Grade Trends")
    plt.legend()
    plt.show()
def main(name):
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
