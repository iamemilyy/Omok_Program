import time
import sys

BOARD_SIZE = 16

scores = {'X': 0, 'O': 0}

def switch_player():  # 플레이어 전환 함수
    global now_player
    if now_player == 'X':
        now_player = 'O'
    else:
        now_player = 'X'

def can_move(row, col):  # 돌을 둘 수 있는 위치인지 확인하는 함수
    if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
        return False
    if board[row][col] != ' ':
        return False
    return True

def board_full():  # 보드에 자리가 있는지 확인하는 함수
    for row in board:
        if ' ' in row:
            return False
    return True

def print_board():  # 오목판 출력
    print('   ', end='')  # 공백 출력
    for col in range(1, BOARD_SIZE + 1):  # 1부터 보드의 크기 만큼 열 번호 출력
        print('{:2}'.format(col), end=' ')
    print()
    for row in range(1, BOARD_SIZE + 1):  # 1부터 보드의 크기 만큼 행 번호 출력
        print('{:2}'.format(row), end='  ')

        # 돌 상태 출력
        for col in range(1, BOARD_SIZE + 1):
            print(board[row-1][col-1], end='  ')
        print()

# 게임 진행 함수
def play_game():
    while True:
        print_board()  # 보드 출력
        print("현재 플레이어:", now_player)
        move = input("돌을 둘 위치를 입력하세요(행과 열을 입력(예: 3 4)): ")
        move = move.split()
        if len(move) != 2:
            print("잘못된 입력입니다. 다시 입력해주세요.")
            continue
        row, col = map(int, move)  # 행과 열을 정수로 변환
        if not can_move(row-1, col-1):
            print("돌을 둘 수 없습니다. 다시 입력해주세요.")
            continue
        board[row-1][col-1] = now_player  # 보드에 돌을 놓음
        if check_winner(row-1, col-1):  # 승자가 결정된 경우 게임 종료
            print_board()
            print("게임 종료! {} 플레이어의 승리입니다.".format(now_player))
            scores[now_player] += 1  # 승자에게 1점 부여
            break
        elif board_full():  # 보드가 가득 찬 경우 게임 종료
            print_board()
            print("게임 종료! 무승부입니다.")
            break
        else:
            switch_player()  # 플레이어 전환

def check_winner(row, col):  # 승자 확인 함수
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # 가로, 세로, 대각선 방향
    # 첫 번째 요소는 수직 방향, 두 번째 요소는 수평 방향
    # 양수는 오른쪽 또는 위쪽으로 이동, 음수는 왼쪽 또는 아래쪽으로 이동
    for dr, dc in directions:  # directions에 있는 각 방향으로 이동하면서 승자를 확인
        count = 0  # 연속된 돌 개수(초기값=0)
        r, c = row, col  # r과 c변수는 현재위치인 row와 col로 초기화
        while True:  # 현재 방향으로 계속 이동(r과 c를 각각 dr과 dc만큼 한 칸씩 이동)
            r += dr
            c += dc
            if r < 0 or r >= BOARD_SIZE or c < 0 or c >= BOARD_SIZE:
                break  # 이동한 위치(r, c)가 보드판을 벗어나면 루프 종료
            if board[r][c] == now_player:
                count += 1  # 이동한 위치(r, c)가 현재 플레이어의 돌과 일치하면 count+1
            else:  # 돌의 위치가 다르면 현 방향으로의 검사를 중지하고 다른 방향으로 넘어가기
                break
        while True:  # 현재 방향으로 계속 이동(r과 c를 각각 dr과 dc만큼 한 칸씩 이동)
            r -= dr
            c -= dc
            if r < 0 or r >= BOARD_SIZE or c < 0 or c >= BOARD_SIZE:
                break  # 이동한 위치(r, c)가 보드판을 벗어나면 루프 종료
            if board[r][c] == now_player:
                count += 1  # 이동한 위치(r, c)가 현재 플레이어의 돌과 일치하면 count+1
            else:  # 돌의 위치가 다르면 현 방향으로의 검사를 중지하고 다른 방향으로 넘어가기
                break
        if count >= 5:  # 오목이 완성되면 True 반환
            return True
    return False

def play_again():  # 게임 재실행 여부 및 점수 안내 함수
    while True:
        print("현재 점수 - X: {}, O: {}".format(scores['X'], scores['O']))
        restart = input("한 판 더 플레이하시겠습니까? (예/아니오): ")
        if restart == '예':
            reset_board()
            return True
        elif restart == '아니오':
            x_score, o_score = calculate_score()  # 점수 계산
            print("=== 게임 종료 ===")
            print("X의 점수:", x_score)
            print("O의 점수:", o_score)
            break
        else:
            print("잘못된 입력입니다. 다시 입력해주세요.")
    return False

def calculate_score():  # 최종 점수
    x_score = scores['X']
    o_score = scores['O']
    return x_score, o_score

def reset_board():  # 게임 리셋 함수
    global board
    board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    global now_player
    now_player = 'X'

# 게임 시작
print("=== 오목 게임을 시작합니다 ===")
board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]  # 빈 오목판 생성, 2차원 리스트 사용
now_player = 'X'  # 플레이어 초기화
print_board()
print("현재 플레이어:", now_player)

while True:
    play_game()
    if not play_again():
        break