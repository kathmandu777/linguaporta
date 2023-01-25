import json
import sys
from time import sleep

import requests
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By

# ネットワーク読み込み待機時間
SLEEP_TIME = 0.05
CATEGORIES = {1: ("単語の意味", 1813), 2: ("空所補充", 1814)}


def login() -> None:
    user_id = input("ID: ")
    user_password = input("Password: ")

    id = driver.find_element(By.NAME, "id")
    password = driver.find_element(By.NAME, "password")

    id.clear()
    id.send_keys(user_id)
    password.send_keys(user_password)
    driver.find_element(By.ID, "btn-login").submit()

    sleep(SLEEP_TIME)


def select_cocet() -> None:
    for _ in range(5):
        try:  # TOPから開く
            driver.execute_script("document.sStudy.submit()")  # 本の選択画面へ移行
            driver.execute_script("select_reference('70')")  # cocet2600を選択
            sleep(SLEEP_TIME)
            return
        except BaseException:
            pass
        try:  # 解答終了時に開く
            driver.execute_script("document.Study.submit()")  # 本の選択画面へ移行
            driver.execute_script("select_reference('70')")  # cocet2600を選択
            sleep(SLEEP_TIME)
            return
        except BaseException:
            pass
    print("cocet2600の選択に失敗しました。")
    driver.quit()
    sys.exit()


def select_unit(category_start: int, unit_start: int) -> tuple[str, int, list]:  # (lesson_name, unit_id, db_data)
    unit_start = (unit_start - 1) // 25 + 1
    try:
        driver.execute_script(("select_unit('drill', '" + str(category_start + (unit_start - 1) * 4) + "', '');"))
    except BaseException:
        print("ユニットの選択に失敗しました。")
        driver.quit()
        sys.exit()

    sleep(SLEEP_TIME)
    lesson_name = driver.find_element(By.CLASS_NAME, "bloc-resp-lessonname").text
    try:
        units = requests.get(f"{SERVER_ORIGIN}/api/units/", headers=HEADER).json()
    except BaseException:
        print("DB serverに接続できませんでした。")
        driver.quit()
        sys.exit()

    if lesson_name in [x["name"] for x in units]:
        id: int = [x["id"] for x in units if x["name"] == lesson_name][0]
        db_data: list = requests.get(f"{SERVER_ORIGIN}/api/units/{id}/questions/", headers=HEADER).json()
        if len(db_data) == 25:
            print(f"DBに {lesson_name} のデータはすべて存在しました。")
        else:
            print(f"DBに {lesson_name} のデータは{len(db_data)}つ存在しました。")
        return lesson_name, id, db_data
    else:
        print(f"DBに{lesson_name}のデータは存在しませんでした")
        created_unit = requests.post(
            f"{SERVER_ORIGIN}/api/units/", data=json.dumps({"name": lesson_name}), headers=HEADER
        ).json()
        return lesson_name, created_unit["id"], []


def set_answer(category_id: int, question_number: int, db_data: list, history: dict[int, str]) -> str:
    if category_id == 1:
        # 選択肢の取得
        candidates = []
        candidates.append(driver.find_element(By.ID, "answer_0_0"))
        candidates.append(driver.find_element(By.ID, "answer_0_1"))
        candidates.append(driver.find_element(By.ID, "answer_0_2"))
        candidates.append(driver.find_element(By.ID, "answer_0_3"))
        candidates.append(driver.find_element(By.ID, "answer_0_4"))
        print(
            "選択肢: {}, {}, {}, {}, {}".format(
                candidates[0].get_attribute("value"),
                candidates[1].get_attribute("value"),
                candidates[2].get_attribute("value"),
                candidates[3].get_attribute("value"),
                candidates[4].get_attribute("value"),
            )
        )

        # 正解の取得
        if question_number in [x["number"] for x in db_data]:
            db_answer = [x["answer"] for x in db_data if x["number"] == question_number][0]
            choice_index = [x.get_attribute("value") for x in candidates].index(db_answer)
        elif question_number in history.keys():
            choice_index = [x.get_attribute("value") for x in candidates].index(history[question_number])
        else:
            choice_index = 0
        choice_text = candidates[choice_index].get_attribute("value")

        # 選択肢クリック
        for _ in range(10):
            try:
                candidates[choice_index].click()
                sleep(SLEEP_TIME)
                break
            except BaseException:
                print("can't click!!")
                sleep(SLEEP_TIME)

        return choice_text

    elif category_id == 2:
        if question_number in [x["number"] for x in db_data]:
            answer = [x["answer"] for x in db_data if x["number"] == question_number][0]
        elif question_number in history.keys():
            answer = history[question_number]
        else:
            answer = "tmp"
        input_box = driver.find_element(By.ID, "tabindex1")
        input_box.send_keys(answer)
        return answer

    raise Exception("category_idが不正です。")


def get_correct_answer(category_id: int) -> str:
    if category_id == 1:
        return driver.find_element(By.ID, "drill_form").text.replace("正解：", "")

    elif category_id == 2:
        return (driver.find_element(By.XPATH, "//*[@id='question_area']/div[3]/input").get_attribute("value")).replace(
            " ", ""
        )
    raise Exception("category_idが不正です。")


def solve(lesson_name: str, category_id: int, db_unit_id: int, db_data: list) -> None:
    history = {}
    while True:
        print(f"============= {lesson_name} =============")

        try:
            question_text = driver.find_element(By.ID, "qu02").text  # NOTE: 単語の意味と空所補充の場合はqu02
        except BaseException:
            print("このユニットは既に完了しています。")
            break
        print("問題:", question_text)

        question_number = int(driver.find_element(By.XPATH, "//*[contains(text(), '問題番号')]").text.replace("問題番号：", ""))
        print("問題番号:", question_number)

        answer = set_answer(category_id, question_number, db_data, history)

        # "解答する"ボタンのクリック
        for _ in range(10):
            try:
                driver.find_element(By.ID, "ans_submit").submit()
                sleep(SLEEP_TIME)
                break
            except BaseException:
                print("Can't click '解答する' button")
                sleep(SLEEP_TIME)

        # 正解と不正解の判定
        for i in range(300):  # NOTE: ここのサーバーの応答が遅いため、長めにしておく
            try:
                driver.find_element(By.ID, "true_msg")
                print("結果: 正解")
                requests.post(
                    f"{SERVER_ORIGIN}/api/units/{db_unit_id}/questions/",
                    data=json.dumps(
                        {
                            "number": question_number,
                            "text": question_text,
                            "answer": answer,
                        }
                    ),
                    headers=HEADER,
                )
                break
            except BaseException:
                pass

            try:
                driver.find_element(By.ID, "false_msg")
                # 解答を見る
                driver.find_element(By.CLASS_NAME, "btn-answer-view").submit()
                sleep(SLEEP_TIME * 2)  # NOTE: for文処理を挟んでいないため、長めにしておく
                correct_answer = get_correct_answer(category_id)
                print(f"結果: 不正解 ({correct_answer})")
                history[question_number] = correct_answer
                requests.post(
                    f"{SERVER_ORIGIN}/api/units/{db_unit_id}/questions/",
                    data=json.dumps(
                        {
                            "number": question_number,
                            "text": question_text,
                            "answer": correct_answer,
                        }
                    ),
                    headers=HEADER,
                )
                break
            except BaseException:
                pass

            if i % 5 == 0:  # NOTE: 毎回表示すると見づらいので、5回に1回表示
                print("correcting...")
            sleep(SLEEP_TIME)
        else:
            print("正解判定に失敗しました。")
            driver.quit()
            sys.exit()

        # 次へすすめる場合は進む、なければユニット終了
        try:
            driver.find_element(By.CLASS_NAME, "btn-problem-next").submit()
        except BaseException:
            return
        sleep(SLEEP_TIME)


if __name__ == "__main__":
    SERVER_ORIGIN = "https://linguaporta-mtzobacrda-an.a.run.app"  # NOTE: don't include slash at the end
    SERVER_ORIGIN = "http://localhost:8000"  # NOTE: don't include slash at the end
    for _ in range(3):
        api_key = input("API_KEY: ")
        HEADER = {"x-api-key": api_key}
        res = requests.get(f"{SERVER_ORIGIN}/api/units/", headers=HEADER)
        if res.status_code == 200:
            break
        print("API_KEYが不正です。再度入力して下さい。")
    else:
        print("失敗回数の上限に達しました。プログラムを終了します。")
        sys.exit()

    CHROMEDRIVER = "./chromedriver"  # change for your environment
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    chrome_service = service.Service(executable_path=CHROMEDRIVER)
    driver = webdriver.Chrome(service=chrome_service, options=options)

    driver.get("https://w5.linguaporta.jp/user/seibido/index.php")
    driver.set_window_size(720, 1280)

    for _ in range(3):
        try:
            login()
            break
        except BaseException:
            print("ログインに失敗しました。再度入力して下さい。")
    else:
        print("失敗回数の上限に達しました。プログラムを終了します。")
        driver.quit()
        sys.exit()

    print("学習するカテゴリーを選択してください。")
    for key, value in CATEGORIES.items():
        print(f"{key}: {value[0]}")
    while True:
        category_id = int(input("Category ID: "))
        if category_id in CATEGORIES.keys():
            break
        print("無効な番号です。入力しなおして下さい。")

    print("開始する番号を入力して下さい。(1-25の場合は1, 126-150の場合は126)")
    while True:
        start = int(input("Start: "))
        if start % 25 == 1:
            break
        else:
            print("無効な番号です。入力しなおして下さい。")

    print("終了する番号を入力して下さい。(1-25の場合は25, 126-150の場合は150)")
    while True:
        end = int(input("End: "))
        if end % 25 == 0:
            break
        else:
            print("無効な番号です。入力しなおして下さい。")

    while start <= end:
        select_cocet()
        print("現在のユニット:", str(start) + "-" + str(start + 24))
        lesson_name, unit_id, db_data = select_unit(CATEGORIES[category_id][1], start)
        solve(lesson_name, category_id, unit_id, db_data)
        print("##############################################")
        print(f"ユニット{start}-{start + 24}を完了しました。")
        print("##############################################")

        start += 25

    print("指定されたすべてのユニットの解答を完了しました。プログラムを終了します。")
    driver.quit()
    sys.exit()
