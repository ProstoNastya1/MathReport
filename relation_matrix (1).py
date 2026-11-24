A = [1, 2, 3, 4, 5]


def read_matrix():
    matrix = []
    print("0과 1로 이루어진 5×5 관계행렬을 입력하세요.")
    print("각 행의 숫자 5개를 공백으로 구분하세요.")
    for element in A:
        while True:
            values = input(f"{element}행 > ").split()
            if len(values) == len(A) and all(v in ("0", "1") for v in values):
                matrix.append([int(v) for v in values])
                break
            print("입력 오류. 0 또는 1을 정확히 5개 입력하세요.")
    return matrix


def is_reflexive(matrix):
    return all(matrix[i][i] == 1 for i in range(len(matrix)))


def is_symmetric(matrix):
    n = len(matrix)
    return all(matrix[i][j] == matrix[j][i]
               for i in range(n) for j in range(i + 1, n))


def is_transitive(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if matrix[i][j] and matrix[j][k] and not matrix[i][k]:
                    return False
    return True


def equivalence_class(matrix, row):
    return [element for j, element in enumerate(A) if matrix[row][j]]


def print_classes(matrix):
    print("원소별 동치류")
    for i, element in enumerate(A):
        members = ", ".join(map(str, equivalence_class(matrix, i)))
        print(f"[{element}] = {{{members}}}")


def reflexive_closure(matrix):
    result = [row[:] for row in matrix]
    for i in range(len(result)):
        result[i][i] = 1
    return result


def symmetric_closure(matrix):
    n = len(matrix)
    return [[matrix[i][j] | matrix[j][i] for j in range(n)]
            for i in range(n)]


def transitive_closure(matrix):
    result = [row[:] for row in matrix]
    n = len(result)
    # 중간 정점 k를 경유하는 경로를 차례로 반영한다.
    for k in range(n):
        for i in range(n):
            if result[i][k]:
                for j in range(n):
                    if result[k][j]:
                        result[i][j] = 1
    return result


def equivalence_closure(matrix):
    return transitive_closure(symmetric_closure(reflexive_closure(matrix)))


def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))


def relation_properties(matrix):
    return is_reflexive(matrix), is_symmetric(matrix), is_transitive(matrix)


def print_result(matrix, properties):
    for name, holds in zip(("반사", "대칭", "추이"), properties):
        print(f"{name} 관계 {'O' if holds else 'X'}")

    if all(properties):
        print("동치 관계입니다.")
        print_classes(matrix)
    else:
        print("동치 관계가 아니므로 동치류를 출력하지 않습니다.")


def main():
    try:
        matrix = read_matrix()
    except EOFError:
        print("\n입력이 끝났습니다. 5개 행이 필요합니다.")
        return

    print("\n[원래 관계의 판정]")
    properties = relation_properties(matrix)
    print_result(matrix, properties)
    if all(properties):
        return

    closures = (
        ("반사 폐포", reflexive_closure),
        ("대칭 폐포", symmetric_closure),
        ("추이 폐포", transitive_closure),
    )
    for (name, close), holds in zip(closures, properties):
        if not holds:
            result = close(matrix)
            print(f"\n[{name}]")
            print("변환 전")
            print_matrix(matrix)
            print("변환 후")
            print_matrix(result)
            print_result(result, relation_properties(result))

    print("\n[추가 기능 | 최소 동치 폐포]")
    result = equivalence_closure(matrix)
    print_matrix(result)
    print_result(result, relation_properties(result))


if __name__ == "__main__":
    main()
