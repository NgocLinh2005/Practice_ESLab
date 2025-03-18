from pysat.solvers import Glucose3
import math

# Tạo bàn cờ
def generate_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]

# Liên kết biến mục tiêu với mã hóa nhị phân
def binary_encoding(clauses, target, new_variables):
    for i in range(len(new_variables)):
        clauses.append([-target, new_variables[i]])

# Sinh tất cả dãy nhị phân có độ dài n
def generate_binary_combinations(n):
    binary_combinations = []
    for i in range(1 << n):  # Sửa lỗi i << n
        binary_combinations.append(format(i, '0' + str(n) + 'b'))
    return binary_combinations

# Sinh biến mới để mã hóa nhị phân số nguyên
def generate_new_variables(end, length):
    return list(range(end + 1, end + math.ceil(math.log(length, 2)) + 1))  # Sửa lỗi tạo danh sách biến

# Ràng buộc tối đa một quân hậu trên mỗi hàng/cột/đường chéo
def at_most_one(clauses, new_variables, variables):
    if len(variables) <= 1:
        return
    
    # Tạo biến nhị phân mới
    temp_new_variables = generate_new_variables(n ** 2 + len(new_variables), len(variables))
    new_variables += temp_new_variables

    # Sinh tất cả chuỗi nhị phân
    binary_combinations = generate_binary_combinations(len(temp_new_variables))

    for i in range(len(variables)):
        combination = binary_combinations[i]
        temp_clause = []
        for j in range(len(combination)):
            if combination[j] == '1':
                temp_clause.append(temp_new_variables[j])
            else:
                temp_clause.append(-temp_new_variables[j])
        binary_encoding(clauses, variables[i], temp_clause)

# Ràng buộc đúng một quân hậu trên mỗi hàng/cột
def exactly_one(clauses, new_variables, variables):
    clauses.append(variables)
    at_most_one(clauses, new_variables, variables)

# Xử lý đường chéo chính (\) và đường chéo phụ (/)
def process_diagonals(n, variables, clauses, new_variables, direction):
    for diff in range(1 - n, n):
        diagonal = []
        for i in range(n):
            j = i + direction * diff
            if 0 <= j < n:
                diagonal.append(variables[i][j])
        
        if len(diagonal) > 1:
            at_most_one(clauses, new_variables, diagonal)

# Tạo mệnh đề SAT cho bài toán
def generate_clauses(n, variables):
    clauses = []
    new_variables = []

    # Hàng
    for i in range(n):
        exactly_one(clauses, new_variables, variables[i])

    # Cột
    for j in range(n):
        exactly_one(clauses, new_variables, [variables[i][j] for i in range(n)])

    # Đường chéo
    process_diagonals(n, variables, clauses, new_variables, direction=1)  # Đường chéo chính (\)
    process_diagonals(n, variables, clauses, new_variables, direction=-1) # Đường chéo phụ (/)

    return clauses, new_variables  # Trả về cả danh sách biến mới

# Giải bài toán N-Queens với SAT Solver
def solve_n_queens(n):
    variables = generate_variables(n)
    clauses = generate_clauses(n, variables)
    print(clauses)

    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    if solver.solve():
        model = solver.get_model()
        return [[int(model[i * n + j] > 0) for j in range(n)] for i in range(n)]
    else:
        return None


def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))


n = 4
solution = solve_n_queens(n)
print_solution(solution)

