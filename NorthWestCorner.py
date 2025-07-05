import InputData as data
def NWC(demand_arr, supply_arr,cost_matrix):
    formated_matrix = data.formatData(demand_arr,supply_arr,cost_matrix)
    j = 1
    for i in range(len(formated_matrix[0])):
        while formated_matrix[0][i] != 0:
            if formated_matrix[0][i] > formated_matrix[j][0]:
                formated_matrix[j][i + 1] = formated_matrix[j][0]
                formated_matrix[0][i] -= formated_matrix[j][0]
                formated_matrix[j][0] = 0
                j += 1
            if formated_matrix[0][i] == formated_matrix[j][0]:
                formated_matrix[j][i + 1] = formated_matrix[j][0]
                formated_matrix[0][i] = 0
                formated_matrix[j][0] = 0
                j += 1
                break
            if formated_matrix[0][i] < formated_matrix[j][0]:
                formated_matrix[j][i + 1] = formated_matrix[0][i]
                formated_matrix[j][0] -= formated_matrix[0][i]
                formated_matrix[0][i] = 0
                break
    for i in range(len(formated_matrix)):
        for a in range(len(formated_matrix[i])):
            if formated_matrix[i][a] == " ":
                formated_matrix[i][a] == 0
    nwc_matrix = []
    for i in range(1, len(formated_matrix)):
        nwc_matrix.append(formated_matrix[i][1:])
    return nwc_matrix

