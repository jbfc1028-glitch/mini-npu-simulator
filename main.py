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
    filters = data["filters"]
    patterns = data["patterns"]

    total = 0
    passed = 0
    failed_cases = []

    for case_id, case in patterns.items():
        total += 1
        size = case_id.rsplit("_", 1)[0]

        filter_cross = filters[size]["cross"]
        filter_x = filters[size]["x"]
        pattern = case["input"]

        score_cross = calculate_mac(pattern, filter_cross)
        score_x = calculate_mac(pattern, filter_x)

        result = judge_pattern(score_cross, score_x)

        expected = case["expected"]

        if expected in ["+", "cross"]:
            expected = "Cross"
        elif expected == "x":
            expected = "X"

        if result == expected:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"
            failed_cases.append(case_id)

        print(f"\n테스트: {case_id}")
        print(f"Cross 점수: {score_cross:.4f}")
        print(f"X 점수: {score_x:.4f}")
        print(f"판정 결과: {result}")
        print(f"기대 정답: {expected}")
        print(f"테스트 결과: {status}")

    print("\n=== 테스트 요약 ===")
    print(f"전체 테스트: {total}")
    print(f"PASS: {passed}")
    print(f"FAIL: {len(failed_cases)}")

    if failed_cases:
        print("실패한 테스트:", ", ".join(failed_cases))

while True:
    print("\n=== Mini NPU Simulator ===")
    print("1. 직접 입력 모드")
    print("2. JSON 테스트 모드")
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


    elif choice == "0":
        print("프로그램을 종료합니다.")
        break

    else:
        print("잘못된 선택입니다. 다시 입력하세요.")
