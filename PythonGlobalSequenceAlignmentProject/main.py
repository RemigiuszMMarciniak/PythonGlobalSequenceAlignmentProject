import urllib
import matplotlib
import matplotlib.pyplot as plt
import requests
import numpy as np


def main():
    print("Hello in global sequence alignment program.")
    print("\nSelect 1st sequence \n")
    data_tuple = select_method()
    data_array_first = list(data_tuple[1])
    description_first = data_tuple[0]

    print(data_array_first)
    print("\nSelect 2nd sequence \n")
    data_tuple = select_method()
    data_array_second = list(data_tuple[1])
    description_second = data_tuple[0]

    print(list(data_array_second))

    print(list(data_array_first))

    points_tuple = choose_points()
    consistency_points = points_tuple[0]
    inconsistency_points = points_tuple[1]
    gap_points = points_tuple[2]

    print("consistency points: " + consistency_points + '\n' +
          "inconsistency points: " + inconsistency_points + '\n' +
          "gap points: " + gap_points + '\n')

    #generating optimal global sequence alignment

    #saving this alignment to a file with statistics

    #score table with optimal path

    #save this to a file


def choose_points():
    consistency_points = input("Insert consistency points:")
    inconsistency_points = input("Insert inconsistency points:")
    gap_points = input("Insert gap points:")
    return consistency_points, inconsistency_points, gap_points


def string_to_array(string):
    # converts string to 1D array
    string = string.upper()
    index = string.rfind('\n')

    # print(index)

    string_to_list = ""
    description = ""
    is_description_skipped = False
    for x in string:

        if x == "\n":
            is_description_skipped = True

        if is_description_skipped:
            string_to_list += x
        else:
            description += x

    # print(description)

    string_list = ""

    for x in string_to_list:
        if not x == "\n":
            # do not save
            string_list += x

    return description, list(string_list)


def manual_insert():
    user_input = input("Insert tag:")
    user_data = ">" + user_input + "\n"
    user_input = input("Enter DNA sequence")
    for x in user_input:
        user_data += x

        # print(x)
        # if len(user_data) % 80 == 0:
        #     user_data += "\n"

    return user_data


def read_file():
    file_name = input("Enter file name: ")
    with open(file_name) as file_object:
        contents = file_object.read()
        return contents


def read_file_from_web(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')
    print(text)
    return text


def select_method():
    print(
        "Select how do you want to reach the data: \n1. Insert the data manually. \n2. Read the data from a file. \n3. Read the data from the server")
    label = input("select:\n")
    while label != "1" or label != "2" or label != "3":
        if label == "1":
            print("Selected 1st option")
            user_data = manual_insert()
            # print(user_data)
            if user_data is not None:
                return string_to_array(user_data)
            break
        elif label == "2":
            print("Selected 2nd option")
            file = read_file()
            if file is not None:
                return string_to_array(file)
            # print(file)
            break
        elif label == "3":
            print("Selected 3rd option")
            db = 'nuccore'
            nuccore_id = input("Enter id:")
            # covid 2019 id = 1798174254
            url_address = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=%s&id=%s&rettype=fasta&retmode=text" % (
                db, nuccore_id)
            file = read_file_from_web(url_address)
            return string_to_array(file)
            break
        else:
            print("Please select correct method ")
            label = input("select:\n")


if __name__ == "__main__":
    main()

# might be usefull
# dot plot method
#     dot_plot = generate_dot_plot(data_array_first, data_array_second)
#     print(dot_plot)
#
#     # show dot plot
#     show_dot_plot(data_array_first, description_first, data_array_second, description_second, dot_plot)
#
#     # filtering
#     window_size = input("Enter window size: ")
#
#     threshold = input("Enter threshold: ")
#
#     window_size = int(str(window_size))
#
#     threshold = int(str(threshold))
#
#     # print(dot_plot)
#     # print(type(dot_plot))
#
#     # print(dot_plot)
#
#     filtered_dot_plot = filter_dot_plot(window_size, threshold, dot_plot)
#
#     print()
#
#     show_filtered_dot_plot(filtered_dot_plot)
#
#     # show matrix as a figure
#     # title,axes,legends,scale
#     file_name = input("Enter a graph name")
#
#     show_matrix_as_fig(filtered_dot_plot,description_second, description_first )
#
#     # save matrix to a graphical file
#     save_matrix_to_file(filtered_dot_plot, description_second, description_first, file_name)
#
#
# def show_matrix_as_fig(filtered_dot_plot, description_first, description_second):
#     plt.figure()
#     plt.title("Dot plot")
#     plt.xlabel(description_first)
#     plt.ylabel(description_second)
#     H = np.array(filtered_dot_plot)
#     plt.imshow(H)
#     plt.show()
#
#
# def save_matrix_to_file(filtered_dot_plot, description_first, description_second, file_name):
#     plt.figure()
#     plt.title("Dot plot")
#     description_first = description_first[:30]
#     # print(description_first)
#     description_second = description_second[:30]
#     # print(type(description_second))
#     # print(len(description_second))
#     # print(description_second)
#     plt.xlabel(description_first)
#     plt.ylabel(description_second)
#     # plt.legend()
#     H = np.array(filtered_dot_plot)
#     plt.imshow(H)
#     plt.savefig(file_name + '.png')
#
#
# def show_filtered_dot_plot(filtered_dot_plot):
#     for i in range(len(filtered_dot_plot)):
#         for j in range(len(filtered_dot_plot[i])):
#             print(filtered_dot_plot[i][j], end=' ')
#         print()
#
#
# def create_matrix_window(dot_plot, window_size, i, j):
#     matrix = [[0 for x1 in range(window_size)] for y1 in range(window_size)]
#     a = 0
#     for x in range(i, i + window_size):
#         b = 0
#         for y in range(j, j + window_size):
#             # print("X, Y: " + str(x) + " " + str(y))
#             # print("A, B: " + str(a) + " " + str(b))
#             # print("matrix: " + str(matrix[a][b]))
#             # print("dot_plot: " + str(dot_plot[x][y]))
#             matrix[a][b] = dot_plot[x][y]
#             b += 1
#         a += 1
#     return matrix
#
#
# def sum_diag(matrix):
#     counter = 0
#     for i in range(len(matrix)):
#         for j in range(len(matrix[i])):
#             if i == j:
#                 if matrix[i][j] == 1:
#                     counter += 1
#     return counter
#
#
# def filter_dot_plot(window_size, threshold, dot_plot):
#     filtered_dot_plot = [[0 for x in range(len(dot_plot[0]))] for y in range(len(dot_plot))]
#
#     # print("len: " + str(len(filtered_dot_plot)))
#     # print("len: " + str(len(filtered_dot_plot[0])))
#
#     for i in range(len(dot_plot) - window_size + 1):
#         for j in range(len(dot_plot[i]) - window_size + 1):
#             # window matrix
#             # print("i, j : " + str(i) + " " + str(j))
#             window_matrix = create_matrix_window(dot_plot, window_size, i, j)
#             # [i:i + window_size, j:j + window_size]
#             # print(" window matrix " + str(show_filtered_dot_plot(window_matrix)))
#
#             # print("i, j : " + str(i) + " " + str(j))
#
#             if sum_diag(window_matrix) >= window_size - threshold:
#                 # print("============")
#                 # show_filtered_dot_plot(filtered_dot_plot)
#                 for k in range(len(window_matrix)):
#                     # print("len : " + str(len(window_matrix)))
#                     # print("i, j : " + str(i) + " " + str(j))
#                     # print("k: " + str(k))
#                     # print("window matrix[k][k]: " + str(window_matrix[k][k]))
#                     # print("i, j /+k: " + str(i+k) + " " + str(j+k))
#                     # print("len: " + str(len(filtered_dot_plot[i+k])) + " len2: " + str(len(filtered_dot_plot[j+k])))
#                     # print("len3: " + str(len(filtered_dot_plot)))
#                     # print("len4: " + str(len(filtered_dot_plot[k])))
#                     # print("filtered dot plot: " + str(filtered_dot_plot[i + k][j + k]))
#                     filtered_dot_plot[i + k][j + k] = window_matrix[k][k]
#
#                 # print("============")
#
#     # for a1 in range(len(dot_plot)):
#     #     for a2 in range(len(dot_plot[a1])):
#     #         print(dot_plot[a1][a2], end=' ')
#     #     print()
#     #
#     # print()
#     # for a1 in range(len(filtered_dot_plot)):
#     #     for a2 in range(len(filtered_dot_plot[a1])):
#     #         print(filtered_dot_plot[a1][a2], end=' ')
#     #     print()
#
#     return filtered_dot_plot
#
#
# ###
#
# def show_dot_plot(data_array_first, name_first, data_array_second, name_second, dot_plot):
#     print("first sequence:")
#     print(name_first)
#     print(data_array_first)
#     print("second sequence")
#     print(name_second)
#     print(data_array_second)
#
#     # print(data_array_second)
#
#     for i in range(len(dot_plot)):
#         for j in range(len(dot_plot[i])):
#             print(dot_plot[i][j], end=' ')
#         print()
#
#
# def generate_dot_plot(array1, array2):
#     dot_plot = [[0 for i in range(len(array2))] for j in range(len(array1))]
#     # print(len(dot_plot))
#     # print(dot_plot)
#     # print(dot_plot[1][1])
#     # dot_plot[1][1] = 1
#     # print(dot_plot[1][1])
#     for i in range(len(array1)):
#         for j in range(len(array2)):
#             if array1[i] == array2[j]:
#                 dot_plot[i][j] = 1
#             else:
#                 dot_plot[i][j] = 0
#     return dot_plot
#
