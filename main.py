import json
import time
def calculate_mac(pattern, filter_data):
    score = 0.0

    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score += pattern[i][j] * filter_data[i][j]

    return score

def judge_pattern(score_cross, score_x):
    epsilon = 1e-9

    if abs(score_cross - score_x) < epsilon:
        return "UNDECIDED"
    elif score_cross > score_x:
        return "Cross"
    else:
        return "X"

def input_matrix(name):
    print(f"\n{name} (3줄 입력, 공백 구분)")

    matrix = []

    while len(matrix) < 3:
        row = input(f"{len(matrix) + 1}번째 줄: ").split()

        if len(row) != 3:
            print("입력 형식 오류: 숫자 3개를 입력하세요.")
            continue

        try:
            numbers = [float(value) for value in row]
            matrix.append(numbers)
        except ValueError:
            print("입력 오류: 숫자만 입력하세요.")

    return matrix

def load_json():
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        print("JSON 파일 불러오기 성공!")
        return data

    except FileNotFoundError:
        print("오류: data.json 파일을 찾을 수 없습니다.")
        return None

    except json.JSONDecodeError:
        print("오류: JSON 파일 형식이 올바르지 않습니다.")
        return None


def run_json_tests(data):
    if not isinstance(data, dict):
        print("JSON 구조 오류: 최상위 데이터는 객체여야 합니다.")
        return

    filters = data.get("filters", {})
    patterns = data.get("patterns", {})


    total = 0
    passed = 0
    failed_cases = []

    if not isinstance(filters, dict) or not isinstance(patterns, dict):
        print("JSON 구조 오류: filters와 patterns는 객체여야 합니다.")
        return

    for case_id, case in patterns.items():
        total += 1

        try:
            if not isinstance(case, dict):
                raise ValueError("테스트 데이터가 객체가 아닙니다.")

            size_key = case_id.rsplit("_", 1)[0]
            size = int(size_key.split("_")[1])

            filter_cross = filters[size_key]["cross"]
            filter_x = filters[size_key]["x"]
            pattern = case["input"]

            if not validate_matrix(filter_cross, size):
                raise ValueError("Cross 필터의 크기 또는 값이 잘못되었습니다.")

            if not validate_matrix(filter_x, size):
                raise ValueError("X 필터의 크기 또는 값이 잘못되었습니다.")

            if not validate_matrix(pattern, size):
                raise ValueError("입력 패턴의 크기 또는 값이 잘못되었습니다.")

            score_cross = calculate_mac(pattern, filter_cross)
            score_x = calculate_mac(pattern, filter_x)

            result = judge_pattern(score_cross, score_x)

            expected = case["expected"]

            if expected in ["+", "cross"]:
                expected = "Cross"
            elif expected in ["x", "X"]:
                expected = "X"
            else:
                raise ValueError("기대 정답이 올바르지 않습니다.")

            if result == expected:
                status = "PASS"
                passed += 1
            else:
                status = "FAIL"
                failed_cases.append(f"{case_id}: 판정 불일치")

            print(f"\n테스트: {case_id}")
            print(f"Cross 점수: {score_cross:.4f}")
            print(f"X 점수: {score_x:.4f}")
            print(f"판정 결과: {result}")
            print(f"기대 정답: {expected}")
            print(f"테스트 결과: {status}")

        except (KeyError, ValueError, TypeError, IndexError) as error:
            failed_cases.append(f"{case_id}: {error}")
            print(f"\n테스트: {case_id}")
            print(f"테스트 결과: FAIL ({error})")

    print("\n=== 테스트 요약 ===")
    print(f"전체 테스트: {total}")
    print(f"PASS: {passed}")
    print(f"FAIL: {len(failed_cases)}")

    if failed_cases:
        print("\n실패한 테스트 목록:")
        for failed in failed_cases:
            print("-", failed)



def run_benchmark():
    sizes = [3, 5, 13, 25]
    repeat = 100

    print("\n=== MAC 성능 비교 ===")
    print(f"{'크기':<10} {'연산 횟수':<12} {'평균 시간(ms)':<15}")

    for size in sizes:
        pattern = [[1.0] * size for _ in range(size)]
        filter_data = [[1.0] * size for _ in range(size)]

        start_time = time.perf_counter()

        for _ in range(repeat):
            calculate_mac(pattern, filter_data)

        end_time = time.perf_counter()

        average_ms = (end_time - start_time) * 1000 / repeat
        operations = size * size

        print(f"{size}x{size:<7} {operations:<12} {average_ms:<15.6f}")
       

def validate_matrix(matrix, size):
    if not isinstance(matrix, list):
        return False

    if len(matrix) != size:
        return False

    for row in matrix:
        if not isinstance(row, list):
            return False

        if len(row) != size:
            return False

        for value in row:
            if type(value) not in (int, float):
                return False

    return True


while True:
    print("\n=== Mini NPU Simulator ===")
    print("1. 직접 입력 모드")
    print("2. JSON 테스트 모드")
    print("3. MAC 성능 비교")
    print("0. 종료")

    choice = input("선택: ")

    if choice == "1":
        filter_a = input_matrix("필터 A")
        filter_b = input_matrix("필터 B")
        pattern = input_matrix("패턴")

        
        start_time = time.perf_counter()

        score_a = calculate_mac(pattern, filter_a)
        score_b = calculate_mac(pattern, filter_b)

        end_time = time.perf_counter()

        elapsed_ms = (end_time - start_time) * 1000

        result = judge_pattern(score_a, score_b)


        print("\n=== MAC 연산 결과 ===")
        print("A 점수:", score_a)
        print("B 점수:", score_b)
        print(f"연산 시간: {elapsed_ms:.6f} ms")

        if result == "Cross":
            print("판정 결과: A")
        elif result == "X":
            print("판정 결과: B")
        else:
            print("판정 결과: UNDECIDED")

    
    elif choice == "2":
        data = load_json()

        if data is not None:
            run_json_tests(data)

    elif choice == "3":
        run_benchmark()

    elif choice == "0":
        print("프로그램을 종료합니다.")
        break

    else:
        print("잘못된 선택입니다. 다시 입력하세요.")

    