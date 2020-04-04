import urllib

def main():
    print("Welcome in global sequence alignment program.")
    while True:
        parameters = insert_parameters()
        insert_type = parameters[0]

        if insert_type == "manual":
            insert_type, seq1, label1, seq2, label2, mode, match_score, mismatch_score, gap_score, path_file_name, score_table_file_name = parameters
            print()
            print("###########################################")
            print(insert_type)
            print(seq1)
            print(label1)
            print(seq2)
            print(label2)
            print("###########################################")
            print()

        elif insert_type == "file":
            insert_type, fasta_name1, fasta_name2, mode, match_score, mismatch_score, gap_score, path_file_name, score_table_file_name = parameters
            print()
            print("###########################################")
            print(insert_type)
            print(fasta_name1)
            print(fasta_name2)
            print("###########################################")
            print()

            file1 = read_file(fasta_name1)
            if file1 is not None:
                file1 = string_to_array(file1)
                seq1 = file1[0]
                label1 = file1[1]
            else:
                print("################# ##### #################")
                print("################# ERROR #################")
                print("################# ##### #################")
                print("First file is empty")
            file2 = read_file(fasta_name2)
            if file2 is not None:
                file2 = string_to_array(file2)
                seq2 = file2[0]
                label2 = file2[1]
            else:
                print("################# ##### #################")
                print("################# ERROR #################")
                print("################# ##### #################")
                print("Second file is empty")

        else:
            insert_type, url1, url2, mode, match_score, mismatch_score, gap_score, path_file_name, score_table_file_name = parameters
            print()
            print("###########################################")
            print(insert_type)
            print(url1)
            print(url2)
            print("###########################################")
            print()

            # db = 'nuccore'
            # # covid 2019 id = 1798174254
            # url_address = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=%s&id=%s&rettype=fasta&retmode=text" % (
            #     db, nuccore_id)

            file1 = read_file_from_web(url1)
            file1 = string_to_array(file1)
            file2 = read_file_from_web(url2)
            file2 = string_to_array(file2)

            seq1 = file1[1]
            label1 = file1[0]
            seq2 = file2[1]
            label2 = file2[0]

        print("################# ####### #################")
        print("################# ####### #################")
        print("################# ####### #################")

        print(label1)
        print(seq1)
        print(label2)
        print(seq2)
        print(mode)
        print(match_score)
        print(mismatch_score)
        print(gap_score)
        print(path_file_name)
        print(score_table_file_name)
        print("################# ####### #################")
        print("################# SUCCESS #################")
        print("################# ####### #################")
        print("Data acquired properly.")

        ###
        # algorithms
        ###
        score_matrix, score, length, identity_count, gaps_count, optimal_path, i_path, j_path = \
            generate_optimal_global_sequence_alignment(seq1, seq2, mode, match_score, mismatch_score, gap_score)

        ###
        # functions to save the data to file

        save_data_to_files(score_matrix, i_path, j_path, score, length, identity_count, gaps_count, optimal_path, seq1,
                           seq2,
                           mode, match_score, mismatch_score, gap_score, path_file_name, score_table_file_name)

        print("################# ####### #################")
        print("################# SUCCESS #################")
        print("################# ####### #################")
        print("Global sequence alignment has just finished correctly")

        print("????????????????? ????????????????????????????????????? ?????????????????")
        print("????????????????? Do you want to run the program again? ?????????????????")
        print("????????????????? ????????????????????????????????????? ?????????????????")
        print("Type \"Y\" if you want to run the program again")
        if not (input(">>") == "Y"):
            break


###
# saving data
###
def save_data_to_files(score_matrix, i_path, j_path, score, length, identity_count, gaps_count, optimal_path, seq1,
                       seq2,
                       mode, match_score, mismatch_score, gap_score, path_file_name, score_table_file_name):
    description = "# 1: " + str("".join(seq1)) + '\n' + \
                  "# 2: " + str("".join(seq2)) + '\n' + \
                  "# Mode: " + str(mode) + '\n' + \
                  "# Match: " + str(match_score) + '\n' + \
                  "# Mismatch: " + str(mismatch_score) + '\n' + \
                  "# Gap: " + str(gap_score) + '\n' + \
                  "# Score: " + str(score) + '\n' + \
                  "# Length: " + str(length) + '\n' + \
                  "# Identity: " + str(identity_count) + "/" + str(length) + " (" + str(
        100 * (identity_count / length)) + "%)" + '\n' + \
                  "# Gaps: " + str(gaps_count) + "/" + str(length) + " (" + str(
        100 * (gaps_count / length)) + "%)" + '\n' + \
                  optimal_path
    print(description)

    f = open(path_file_name + "analysis.txt", "w+")
    f.write(description)
    f.close()

    score_table_raw = [["" for x in range(len(score_matrix[0]) + 1)] for y in range(len(score_matrix) + 1)]

    # print(len(score_matrix))
    # print(len(score_matrix[0]))
    # print(len(score_table_raw))
    # print(len(score_table_raw[0]))
    # print(score_table_raw)
    # print(score_matrix)

    # print("len score matrix " + str(len(score_matrix)))
    # print("len score raw table " + str(len(score_table_raw)))
    for x in range(len(score_matrix)):
        for y in range(len(score_matrix[x])):
            # print("x, y " + str(x) + " , " + str(y))
            score_table_raw[x][y] = score_matrix[x][y]
            for z in range(len(i_path)):
                if i_path[z] == x and j_path[z] == y:
                    score_table_raw[x][y] = str(score_table_raw[x][y]) + "*"

    print("ipath: " + str(i_path))
    print("jpath: " + str(j_path))


    for x in range(len(score_table_raw)):
        for y in range(len(score_table_raw[x])):
            print(score_table_raw[x][y], end=" ")
        print()

    score_matrix_to_be_shown = [["" for x in range(len(score_table_raw[0]) + 1)] for y in
                                range(len(score_table_raw) + 1)]
    # print(len(score_table_raw))
    # print(len(score_table_raw[0]))
    for x in range(len(score_table_raw)):
        for y in range(len(score_table_raw[0])):
            # print(str(x) + " x , y " + str(y))
            if x == 0 and y == 0:
                score_matrix_to_be_shown[x][y] = "#"
            if x == 0 and y == 1:
                score_matrix_to_be_shown[x][y] = "-"
            if x == 1 and y == 0:
                score_matrix_to_be_shown[x][y] = "-"
            elif x > 1 and y == 0:
                score_matrix_to_be_shown[x][y] = seq1[x - 2]
            elif x == 0 and y > 1:
                score_matrix_to_be_shown[x][y] = seq2[y - 2]
            elif x >= 1 and y >= 1:
                score_matrix_to_be_shown[x][y] = score_table_raw[x - 1][y - 1]
    score_matrix_to_string = ""
    for x in range(len(score_matrix_to_be_shown)):
        for y in range(len(score_matrix_to_be_shown[x])):
            #print(score_matrix_to_be_shown[x][y], end=" ")
            score_matrix_to_string = score_matrix_to_string + str(score_matrix_to_be_shown[x][y]) + " "
       # print()
        score_matrix_to_string = score_matrix_to_string + '\n'

    f = open(score_table_file_name + "score_table.txt", "w+")
    f.write(str(score_matrix_to_string))
    f.close()
###
# algorithms: global alignment
###
def generate_optimal_global_sequence_alignment(seq1, seq2, mode, match_score, mismatch_score, gap_score):
    # print("seq1 length " + str(len(seq1)))
    # print("seq2 length " + str(len(seq2)))
    score_matrix = [[0 for x in range(len(seq2) + 1)] for y in range(len(seq1) + 1)]
    score_matrix_displayed = [["" for x in range(len(seq2) + 2)] for y in range(len(seq1) + 2)]

    ###
    # optimal path
    ###

    if mode == "distance":

        # generate V table for Needleman-Wunsh algorithm (mode distance)
        for i in range(len(score_matrix)):
            for j in range(len(score_matrix[i])):
                if i == 0 and j == 0:
                    score_matrix[i][j] = 0
                else:
                    if i == 0 and j > 0:
                        score_matrix[i][j] = j * int(gap_score)
                    elif i > 0 and j == 0:
                        score_matrix[i][j] = i * int(gap_score)
                    elif i >= 1 and j >= 1:
                        del_score = score_matrix[i - 1][j] + int(gap_score)
                        ins_score = score_matrix[i][j - 1] + int(gap_score)
                        sub_score = score_matrix[i - 1][j - 1] + int(
                            int(mismatch_score) * bool(seq1[i - 1] != seq2[j - 1]))
                        # print(str(del_score) + " " + str(ins_score) + " " + str(sub_score))
                        score_matrix[i][j] = min(int(del_score), int(ins_score), int(sub_score))

        # for x in range(len(score_matrix)):
        #     for y in range(len(score_matrix[x])):
        #         print(score_matrix[x][y], end=" ")
        #     print()

        for x in range(len(score_matrix_displayed)):
            for y in range(len(score_matrix_displayed[x])):
                if x == 0 and y == 0:
                    score_matrix_displayed[x][y] = "#"
                if x == 0 and y == 1:
                    score_matrix_displayed[x][y] = "-"
                if x == 1 and y == 0:
                    score_matrix_displayed[x][y] = "-"
                elif x > 1 and y == 0:
                    score_matrix_displayed[x][y] = seq1[x - 2]
                elif x == 0 and y > 1:
                    score_matrix_displayed[x][y] = seq2[y - 2]
                elif x >= 1 and y >= 1:
                    score_matrix_displayed[x][y] = score_matrix[x - 1][y - 1]

        for x in range(len(score_matrix_displayed)):
            for y in range(len(score_matrix_displayed[x])):
                print(score_matrix_displayed[x][y], end=" ")
            print()

        aln1 = ""
        aln2 = ""
        i = len(score_matrix) - 1
        j = len(score_matrix[0]) - 1

        # print(str(i) + " i , j " + str(j))
        # print()
        # print(str(len(seq1)) + " len seq1 , len seq2 " + str(len(seq2)))

        i_path = []
        j_path = []

        while i >= 0 and j >= 0:
            print(str(i_path) + "<ipath jpath> " + str(j_path))
            if i == 0 and j == 0:
                i_path.append(i)
                j_path.append(j)
                break

            # print(str(i) + " i , j " + str(j))
            # print("score for i and j : " + str(score_matrix[i][j]))
            # print("score for i-1 and j-1 : " + str(score_matrix[i-1][j-1]))
            # print("score for i-1 and j : " + str(score_matrix[i-1][j]))
            # print("score for i and j-1 : " + str(score_matrix[i][j-1]))

            del_score = score_matrix[i - 1][j]
            ins_score = score_matrix[i][j - 1]
            sub_score = score_matrix[i - 1][j - 1]
            minimum_score = min(del_score, ins_score, sub_score)
            # print("##############")
            # print(del_score)
            # print(ins_score)
            # print(sub_score)
            # print(minimum_score)
            # print("##############")
            # print("aln1: " + str(aln1))
            # print("aln2: " + str(aln2))

            if minimum_score == sub_score:
                aln1 = seq1[i - 1] + aln1
                aln2 = seq2[j - 1] + aln2
                i_path.append(i)
                j_path.append(j)
                i = i - 1
                j = j - 1
            else:
                if minimum_score == del_score:
                    aln2 = "-" + aln2
                    aln1 = seq1[i - 1] + aln1
                    i_path.append(i)
                    j_path.append(j)
                    i = i - 1
                else:
                    aln2 = seq2[j - 1] + aln2
                    aln1 = "-" + aln1
                    i_path.append(i)
                    j_path.append(j)
                    j = j - 1

            # print("aln1: " + str(aln1))
            # print("aln2: " + str(aln2))

        identity = []
        for x in range(len(aln1)):
            if aln1[x] == aln2[x]:
                identity.append("|")
            else:
                identity.append("x")
        print("################# ####### #################")
        print("################# SUCCESS #################")
        print("################# ####### #################")
        print("Path has been generated succesfully.")
        print("aln1: " + str(aln1))
        print("      " + str("".join(identity)))
        print("aln2: " + str(aln2))
        print("i path: " + str(i_path))
        print("j path: " + str(j_path))

        # while i >= 0 and j >= 0:
        #     print(str(i) + " i , j " + str(j))
        #     print("score for i and j : " + str(score_matrix[i][j]))
        #     if i == 0 and j == 0:
        #         break
        #     else:
        #         if i > 0 and j > 0 and (score_matrix[i][j] == score_matrix[i - 1][j - 1] + int(mismatch_score) * (
        #                     seq1[i - 1] != seq2[j - 1])):
        #             aln1 = seq1[i - 1] + aln1
        #             aln2 = seq2[j - 1] + aln2
        #             i = i - 1
        #             j = j - 1
        #         else:
        #             if i > 0 and (score_matrix[i][j] == score_matrix[i-1][j] + int(gap_score)):
        #                 aln1 = "-" + aln1
        #                 aln2 = seq2[j-1] + aln2
        #                 j = j - 1
        #             elif j > 0 and (score_matrix[i][j] == score_matrix[i][j-1] + int(gap_score)):
        #                 aln1 = seq1[i-1] + aln1
        #                 aln2 = "-" + aln2
        #                 i = i - 1

    else:
        # generate V table for Needleman-Wunsh algorithm (mode similiarity)
        for i in range(len(score_matrix)):
            for j in range(len(score_matrix[i])):
                if i == 0 and j == 0:
                    score_matrix[i][j] = 0
                else:
                    if i == 0 and j > 0:
                        score_matrix[i][j] = j * int(gap_score)
                    elif i > 0 and j == 0:
                        score_matrix[i][j] = i * int(gap_score)
                    elif i >= 1 and j >= 1:
                        del_score = score_matrix[i - 1][j] + int(gap_score)
                        ins_score = score_matrix[i][j - 1] + int(gap_score)
                        sub_score = score_matrix[i - 1][j - 1] + int(
                            int(mismatch_score) * bool(seq1[i - 1] != seq2[j - 1]))
                        if seq1[i - 1] == seq2[j - 1]:
                            reward_score = score_matrix[i - 1][j - 1] + int(
                                int(match_score))
                            # print(str(del_score) + " " + str(ins_score) + " " + str(sub_score) + " " + str(reward_score))
                            score_matrix[i][j] = max(int(del_score), int(ins_score), int(sub_score), int(reward_score))
                            continue
                        # print(str(del_score) + " " + str(ins_score) + " " + str(sub_score))
                        score_matrix[i][j] = max(int(del_score), int(ins_score), int(sub_score))

        # for x in range(len(score_matrix)):
        #     for y in range(len(score_matrix[x])):
        #         print(score_matrix[x][y], end=" ")
        #     print()

        for x in range(len(score_matrix_displayed)):
            for y in range(len(score_matrix_displayed[x])):
                if x == 0 and y == 0:
                    score_matrix_displayed[x][y] = "#"
                if x == 0 and y == 1:
                    score_matrix_displayed[x][y] = "-"
                if x == 1 and y == 0:
                    score_matrix_displayed[x][y] = "-"
                elif x > 1 and y == 0:
                    score_matrix_displayed[x][y] = seq1[x - 2]
                elif x == 0 and y > 1:
                    score_matrix_displayed[x][y] = seq2[y - 2]
                elif x >= 1 and y >= 1:
                    score_matrix_displayed[x][y] = score_matrix[x - 1][y - 1]

        for x in range(len(score_matrix_displayed)):
            for y in range(len(score_matrix_displayed[x])):
                print(score_matrix_displayed[x][y], end=" ")
            print()

        aln1 = ""
        aln2 = ""
        i = len(score_matrix) - 1
        j = len(score_matrix[0]) - 1
        #
        # print(str(i) + " i , j " + str(j))
        # print()
        # print(str(len(seq1)) + " len seq1 , len seq2 " + str(len(seq2)))

        i_path = []
        j_path = []

        while i >= 0 and j >= 0:
            if i == 0 and j == 0:
                i_path.append(i)
                j_path.append(j)
                break

            # print(str(i) + " i , j " + str(j))
            # print("score for i and j : " + str(score_matrix[i][j]))
            # print("score for i-1 and j-1 : " + str(score_matrix[i-1][j-1]))
            # print("score for i-1 and j : " + str(score_matrix[i-1][j]))
            # print("score for i and j-1 : " + str(score_matrix[i][j-1]))

            del_score = score_matrix[i - 1][j]
            ins_score = score_matrix[i][j - 1]
            sub_or_reward_score = score_matrix[i - 1][j - 1]
            maximum_score = max(del_score, ins_score, sub_or_reward_score)
            # print("##############")
            # print(del_score)
            # print(ins_score)
            # print(sub_or_reward_score)
            # print(maximum_score)
            # print("##############")
            # print("aln1: " + str(aln1))
            # print("aln2: " + str(aln2))

            if maximum_score == sub_or_reward_score:
                aln1 = seq1[i - 1] + aln1
                aln2 = seq2[j - 1] + aln2
                i_path.append(i)
                j_path.append(j)
                i = i - 1
                j = j - 1
            else:
                if maximum_score == del_score:
                    aln2 = "-" + aln2
                    aln1 = seq1[i - 1] + aln1
                    i_path.append(i)
                    j_path.append(j)
                    i = i - 1
                else:
                    aln2 = seq2[j - 1] + aln2
                    aln1 = "-" + aln1
                    i_path.append(i)
                    j_path.append(j)
                    j = j - 1

            # print("aln1: " + str(aln1))
            # print("aln2: " + str(aln2))

        identity = []
        for x in range(len(aln1)):
            if aln1[x] == aln2[x]:
                identity.append("|")
            else:
                identity.append("x")
        print("################# ####### #################")
        print("################# SUCCESS #################")
        print("################# ####### #################")
        print("Path has been generated succesfully.")
        print("aln1: " + str(aln1))
        print("      " + str("".join(identity)))
        print("aln2: " + str(aln2))
        print("i path: " + str(i_path))
        print("j path: " + str(j_path))

    # statistics
    # match
    length = max(len(aln1), len(aln2))
    score = 0
    identity_count = 0
    gaps_count = 0
    for x in range(len(aln1)):
        if aln1[x] != aln2[x]:
            score = score + 1
        if aln1[x] == aln2[x]:
            identity_count = identity_count + 1
        if aln1[x] == "-":
            gaps_count = gaps_count + 1
        if aln2[x] == "-":
            gaps_count = gaps_count + 1

    optimal_path = aln1 + '\n' + "".join(identity) + '\n' + aln2
    return score_matrix, score, length, identity_count, gaps_count, optimal_path, i_path, j_path


def insert_parameters():
    ###
    # this function takes user input and initialize variables in order to proceed further.
    ###
    while True:
        print("#############################################")
        print("Insert parameters as shown below:")
        print(
            "manual,sequence1,label1,sequence2,label2,distance/similarity,match score, mismatch score, gap score, path file name, score table file name")
        print("or")
        print(
            "file,fasta_name1.txt, fasta_name2.txt,distance/similarity,match score, mismatch score, gap score, path file name,score table file name")
        print("or")
        print(
            "server,url1, url2,distance/similarity,match score, mismatch score, gap score, path file name,score table file name")
        print("example:")
        print("manual,ATATAC,1st,ATTAGC,2nd,distance,1,-1,-2,test1path,test1scoretable")
        print("example:")
        print("file,test1.txt,test2.txt,distance,1,-1,-2,test1path,test1scoretable")
        print("#############################################")

        parameters = input(">>")

        inserted_parameters = parameters.split(",")
        insert_type = inserted_parameters[0]

        if insert_type == "manual":
            print("################# ####### #################")
            print("################# SUCCESS #################")
            print("################# ####### #################")
            print("Manual insert type chosen")

            return inserted_parameters

        elif insert_type == "file":
            print("################# ####### #################")
            print("################# SUCCESS #################")
            print("################# ####### #################")
            print("File insert type chosen")

            return inserted_parameters

        elif insert_type == "server":
            print("################# ####### #################")
            print("################# SUCCESS #################")
            print("################# ####### #################")
            print("Server insert type chosen")

            return inserted_parameters

        else:
            print("################# ##### #################")
            print("################# ERROR #################")
            print("################# ##### #################")
            print("Wrong input parameters. Chose either manual, file or server")


def string_to_array(string):
    # converts string to 1D array
    # string = string.upper()
    # index = string.rfind('\n')
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

    return list(string_list), description


def read_file(file_name):
    with open(file_name) as file_object:
        contents = file_object.read()
        return contents


def read_file_from_web(url):
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')
    print(text)
    return text


if __name__ == "__main__":
    main()
