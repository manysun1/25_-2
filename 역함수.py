"""
역행렬 계산 프로그램
  1. 행렬 입력 (정수·분수·소수 입력 가능)
  2. 행렬식을 이용한 역행렬 계산
  3. 가우스-조던 소거법을 이용한 역행렬 계산
  4. 결과 출력 및 비교
  + 랜덤 행렬 생성, 메뉴 반복 실행
"""

import random
from fractions import Fraction


class SingularMatrixError(Exception):
    """역행렬이 존재하지 않을 때 발생하는 예외"""
    pass


# ---------------------------------------------------------------
# 1. 행렬 입력 기능
# ---------------------------------------------------------------
def input_size():
    """정수 n 입력"""
    while True:
        try:
            n = int(input("행렬의 크기 n을 입력하세요: "))
            if n >= 1:
                return n
        except ValueError:
            pass
        print("  [오류] 1 이상의 정수를 입력하세요.")


def input_matrix(n):
    """n×n 행렬을 행 단위로 입력받아 2차원 리스트로 반환"""
    print(f"{n} × {n} 행렬을 한 행씩 입력하세요. (공백 구분, 분수 1/2·소수 0.5 가능)")
    matrix = []
    while len(matrix) < n:
        tokens = input(f"  {len(matrix) + 1}행: ").split()
        if len(tokens) != n:
            print(f"  [오류] {n}개의 값을 입력해야 합니다.")
            continue
        try:
            matrix.append([Fraction(t) for t in tokens])
        except (ValueError, ZeroDivisionError):
            print("  [오류] 올바른 숫자를 입력하세요.")
    return matrix


def random_matrix(n):
    """-9 ~ 9 범위의 정수로 랜덤 행렬 생성"""
    return [[Fraction(random.randint(-9, 9)) for _ in range(n)] for _ in range(n)]


# ---------------------------------------------------------------
# 2. 행렬식을 이용한 역행렬 계산 기능
#    A^-1 = adj(A) / det(A)
# ---------------------------------------------------------------
def get_minor(m, row, col):
    """row행과 col열을 제거한 소행렬"""
    return [r[:col] + r[col + 1:] for i, r in enumerate(m) if i != row]


def determinant(m):
    """여인수 전개를 이용한 행렬식 계산 (재귀)"""
    n = len(m)
    if n == 1:
        return m[0][0]
    if n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    det = Fraction(0)
    for j in range(n):
        det += (-1) ** j * m[0][j] * determinant(get_minor(m, 0, j))
    return det


def inverse_by_determinant(m):
    """행렬식과 수반행렬을 이용한 역행렬 계산"""
    n = len(m)
    det = determinant(m)
    if det == 0:
        raise SingularMatrixError("행렬식이 0이므로 역행렬이 존재하지 않습니다.")
    if n == 1:
        return [[1 / det]]

    # 여인수행렬 C[i][j] = (-1)^(i+j) * det(M_ij)
    cofactor = [[(-1) ** (i + j) * determinant(get_minor(m, i, j))
                 for j in range(n)] for i in range(n)]
    # 수반행렬 adj(A) = C^T,  A^-1 = adj(A) / det(A)
    return [[cofactor[j][i] / det for j in range(n)] for i in range(n)]


# ---------------------------------------------------------------
# 3. 가우스-조던 소거법을 이용한 역행렬 계산 기능
#    [A | I]  →  행연산  →  [I | A^-1]
# ---------------------------------------------------------------
def inverse_by_gauss_jordan(m):
    """가우스-조던 소거법을 이용한 역행렬 계산"""
    n = len(m)
    # 증강행렬 [A | I]
    aug = [list(m[i]) + [Fraction(int(i == j)) for j in range(n)] for i in range(n)]

    for col in range(n):
        # 피벗 선택 (절댓값이 가장 큰 행)
        pivot_row = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if aug[pivot_row][col] == 0:
            raise SingularMatrixError("피벗이 0이므로 역행렬이 존재하지 않습니다.")

        # 행 교환
        aug[col], aug[pivot_row] = aug[pivot_row], aug[col]

        # 피벗을 1로 만들기
        pivot = aug[col][col]
        aug[col] = [x / pivot for x in aug[col]]

        # 같은 열의 나머지 원소를 0으로 만들기
        for r in range(n):
            if r != col:
                factor = aug[r][col]
                aug[r] = [a - factor * b for a, b in zip(aug[r], aug[col])]

    return [row[n:] for row in aug]


# ---------------------------------------------------------------
# 4. 결과 출력 및 비교 기능
# ---------------------------------------------------------------
def print_matrix(m):
    """행렬을 열 너비를 맞추어 출력"""
    cells = [[str(x) for x in row] for row in m]
    width = max(len(c) for row in cells for c in row)
    for row in cells:
        print("  [ " + "  ".join(c.rjust(width) for c in row) + " ]")
    print()


def run(A):
    print("\n[입력 행렬 A]")
    print_matrix(A)

    print("[방법 1] 행렬식을 이용한 역행렬")
    try:
        inv_det = inverse_by_determinant(A)
        print_matrix(inv_det)
    except SingularMatrixError as e:
        inv_det = None
        print(f"  [오류] {e}\n")

    print("[방법 2] 가우스-조던 소거법을 이용한 역행렬")
    try:
        inv_gj = inverse_by_gauss_jordan(A)
        print_matrix(inv_gj)
    except SingularMatrixError as e:
        inv_gj = None
        print(f"  [오류] {e}\n")

    print("[결과 비교]")
    if inv_det is not None and inv_gj is not None:
        if inv_det == inv_gj:
            print("  두 방법으로 구한 역행렬이 동일합니다.")
        else:
            print("  두 방법으로 구한 역행렬이 다릅니다.")
    elif inv_det is None and inv_gj is None:
        print("  두 방법 모두 역행렬이 존재하지 않는다고 판정했습니다.")
    else:
        print("  두 방법의 결과가 일치하지 않습니다.")
    print("-" * 50)


# ---------------------------------------------------------------
# 메인 (메뉴 반복 실행)
# ---------------------------------------------------------------
def main():
    while True:
        print("\n===== 역행렬 계산 프로그램 =====")
        print("1. 행렬 직접 입력")
        print("2. 랜덤 행렬 생성")
        print("0. 종료")
        choice = input("선택 >> ").strip()

        if choice == "1":
            run(input_matrix(input_size()))
        elif choice == "2":
            run(random_matrix(input_size()))
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("  [오류] 0, 1, 2 중에서 선택하세요.")


if __name__ == "__main__":
    main()