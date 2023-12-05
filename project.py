import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pandas as pd
import time
import threading
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# CSV 파일에서 데이터를 불러옴
df = pd.read_csv("꽃 자료 최종 (7).csv")
# 장바구니를 저장하는 딕셔너리
cart = {}
# 장바구니의 내용을 표시하는 표
cart_tree = None
# second_page를 전역 변수로 선언
second_page = None
# 관리자 모드에서 사용할 판매 데이터
sales_data = {}
admin_mode_counter = 0


def open_admin_mode():
    global admin_mode_counter
    admin_mode_counter += 1

    if admin_mode_counter == 3:
        # 카운터를 초기화
        admin_mode_counter = 0

        # 비밀번호 입력 창을 생성
        password_window = tk.Toplevel(root)
        password_window.title("관리자 인증")
        password_window.geometry("240x100+330+300")

        password_label = tk.Label(password_window, text="비밀번호를 입력하세요.")
        password_label.pack()

        password_entry = tk.Entry(password_window, show="*")
        password_entry.pack()

        def add_number(number):
            current = password_entry.get()
            password_entry.delete(0, tk.END)
            password_entry.insert(0, current + str(number))

        # 숫자 버튼을 생성
        for i in range(1, 10):
            button = tk.Button(
                password_window, text=str(i), command=lambda i=i: add_number(i)
            )
            button.pack(side="left")

        zero_button = tk.Button(
            password_window, text="0", command=lambda: add_number(0)
        )
        zero_button.pack(side="left")

        def backspace():
            current = password_entry.get()
            password_entry.delete(0, tk.END)
            password_entry.insert(0, current[:-1])

        backspace_button = tk.Button(password_window, text="←", command=backspace)
        backspace_button.pack(side="left")

        def check_password():
            password = password_entry.get()
            # password를 원하는 비밀번호로 변경 가능
            if password == "1111":
                password_window.destroy()

                admin_window = tk.Toplevel(root)
                admin_window.title("관리자 모드")
                admin_window.geometry("200x100+200+0")
                admin_label = tk.Label(admin_window, text="관리자 모드입니다.")
                admin_label.pack()
            else:
                messagebox.showerror("오류", "비밀번호가 틀렸습니다.")
            # 통계량 버튼을 추가
            stats_button = tk.Button(admin_window, text="통계량", command=show_statistics)
            stats_button.pack()

            # 날씨 변경 버튼을 추가
            weather_button = tk.Button(
                admin_window, text="날씨 변경", command=change_weather
            )
            weather_button.pack()

        password_button = tk.Button(password_window, text="확인", command=check_password)
        password_button.pack(side="left")


def show_statistics():
    # 판매 통계를 보여주는 새 창 생성
    stats_window = tk.Toplevel(root)
    stats_window.title("Sale Statics")

    # 판매 통계를 보여주는 표를 생성
    tree = ttk.Treeview(
        stats_window, columns=("category", "count", "total"), show="headings"
    )
    tree.heading("category", text="Category")
    tree.heading("count", text="Sale Quantity")
    tree.heading("total", text="Total Cost")
    tree.pack()

    # 판매 데이터를 표에 추가
    categories = []
    counts = []
    totals = []

    # 카테고리 이름을 한글에서 영어로 매핑하는 딕셔너리
    category_map = {
        "사랑": "Love",
        "감성": "Emotion",
        "감사": "Appreciation",
        "분위기": "Atmosphere",
        "회상": "Flashback",
        "탄생화": "Birth_flower",
        "기타": "Etc",
    }

    for category, data in sales_data.items():
        count, total = data
        tree.insert("", "end", values=(category, count, total))
        english_category = category_map.get(
            category, "Unknown"
        )  # 매핑 딕셔너리를 사용하여 한글 카테고리를 영어로 변환
        categories.append(english_category)
        counts.append(count)
        totals.append(total)

    # 막대 그래프 생성
    fig, axs = plt.subplots(1, 2, figsize=(20, 5))  # 1행 2열의 subplot 생성
    y_pos = np.arange(len(categories))

    # 카테고리별 판매 수량 그래프
    axs[0].bar(y_pos, counts, align="center", alpha=0.5)
    axs[0].set_xticks(y_pos)
    axs[0].set_xticklabels(categories)
    axs[0].set_ylabel("Sales Volume")  # Y축 이름을 영어로 변경
    axs[0].set_title("Sales Volume by Category")  # 그래프 제목을 영어로 변경

    # 카테고리별 총판매액 그래프
    axs[1].bar(y_pos, totals, align="center", alpha=0.5)
    axs[1].set_xticks(y_pos)
    axs[1].set_xticklabels(categories)
    axs[1].set_ylabel("Total Sales")  # Y축 이름을 영어로 변경
    axs[1].set_title("Total Sales by Category")  # 그래프 제목을 영어로 변경

    # 그래프를 판매 통계 창에 추가
    canvas = FigureCanvasTkAgg(fig, master=stats_window)
    canvas.draw()
    canvas.get_tk_widget().pack()


def change_weather():
    print("날씨 변경")


def create_second_page():
    global second_page
    second_page = tk.Toplevel(root)
    second_page.title("꽃 선택")
    second_page.geometry("540x720+200+0")
    tab_parent = ttk.Notebook(second_page)

    tabs = ["사랑", "감성", "감사", "분위기", "회상", "탄생화", "기타"]
    for tab in tabs:
        tab_frame = ttk.Frame(tab_parent, width=480, height=720)
        tab_parent.add(tab_frame, text=tab)

        # 스크롤바 추가
        # canvas의 높이를 제한
        canvas = tk.Canvas(tab_frame, height=500)
        scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 캔버스와 스크롤바를 탭 프레임에 추가
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 해당 탭의 카테고리에 해당하는 꽃들의 데이터를 가져옴
        flowers = df[df["카테고리"] == tab]
        # 각 꽃의 사진을 세 열로 출력
        for i in range(0, len(flowers), 3):
            for j in range(3):
                if i + j < len(flowers):
                    flower = flowers.iloc[i + j]
                    load = Image.open(flower["사진"])
                    render = ImageTk.PhotoImage(load)
                    img = tk.Label(scrollable_frame, image=render)
                    img.image = render
                    img.bind(
                        "<Button-1>", lambda e, f=flower: show_info(second_page, f)
                    )
                    img.grid(row=i, column=j)

                    # 사진 아래 꽃 이름과 꽃말을 추가
                    flower_name_label = tk.Label(
                        scrollable_frame, text=f"꽃 이름: {flower['꽃 이름']}"
                    )
                    flower_name_label.grid(row=i + 1, column=j)
                    flower_lang_label = tk.Label(
                        scrollable_frame, text=f"꽃말: {flower['꽃말']}"
                    )
                    flower_lang_label.grid(row=i + 2, column=j)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    tab_parent.pack(expand=1, fill="both")

    # 장바구니 정보를 보여줌
    cart_label = tk.Label(second_page, text="")
    cart_label.pack()
    update_cart(second_page)


def show_info(second_page, flower):
    info = tk.Toplevel(second_page)
    info.title("꽃 정보")
    info.geometry("300x400+280+100")

    load = Image.open(flower["사진"])
    render = ImageTk.PhotoImage(load)
    img = tk.Label(info, image=render)
    img.image = render
    img.pack()

    tk.Label(info, text=f"꽃 이름: {flower['꽃 이름']}").pack()
    tk.Label(info, text=f"꽃말: {flower['꽃말']}").pack()
    tk.Label(info, text=f"가격: {flower['가격']}").pack()

    num = tk.IntVar(value=1)
    tk.Label(info, text="수량:").pack()
    tk.Spinbox(info, from_=1, to=100, textvariable=num).pack()

    button_frame = tk.Frame(info)
    button_frame.pack(fill="x", expand=True)

    # 취소 버튼 추가
    cancel_button = tk.Button(button_frame, text="취소", command=info.destroy)
    cancel_button.pack(side="left", fill="x", expand=True)

    # 장바구니에 추가 버튼을 누르면 장바구니 업데이트 함수를 호출 후 팝업 창을 닫음
    add_button = tk.Button(
        button_frame,
        text="장바구니에 추가",
        command=lambda: (add_to_cart(flower, num.get(), second_page), info.destroy()),
    )
    add_button.pack(side="right", fill="x", expand=True)


def add_to_cart(flower, num, second_page):
    if flower["꽃 이름"] in cart:
        cart[flower["꽃 이름"]][1] += num
    else:
        cart[flower["꽃 이름"]] = [flower["가격"], num]
    # 장바구니 업데이트
    update_cart(second_page)


def remove_from_cart(event):
    global cart_tree, second_page
    # cart_tree가 None인 경우 함수를 종료
    if cart_tree is None:
        return
    # 클릭한 셀의 값을 가져옴
    item = cart_tree.identify("item", event.x, event.y)
    column = cart_tree.identify("column", event.x, event.y)
    value = cart_tree.set(item, column)
    # 값이 '삭제'일 경우에만 삭제
    if value == "삭제":
        # 클릭한 행의 꽃 이름을 가져옴
        flower_name = cart_tree.set(item, "#1")
        # 장바구니에서 꽃을 삭제
        del cart[flower_name]
        # 장바구니 업데이트
        update_cart(second_page)


def update_cart(second_page):
    global cart_tree
    # 기존의 장바구니 표를 삭제
    if cart_tree is not None:
        cart_tree.destroy()
    # 기존의 장바구니 표를 삭제
    if hasattr(second_page, "cart_frame"):
        second_page.cart_frame.destroy()

    # 장바구니의 내용을 표시하는 프레임을 생성
    cart_frame = tk.Frame(second_page)
    cart_frame.pack(side="bottom", anchor="w", padx=10, pady=10)  # 화면 하단에 배치합니다.

    # 결제하기 버튼을 추가
    if not cart:  # 장바구니에 꽃이 없을 때
        checkout_button = tk.Button(
            cart_frame, text="결제하기", height=15, state="disabled"
        )
        checkout_button.pack(side="right")

    else:
        checkout_button = tk.Button(
            cart_frame, text="결제하기", height=15, command=open_payment_window
        )
        checkout_button.pack(side="right")

    # 장바구니의 내용을 표시하는 표를 생성
    cart_tree = ttk.Treeview(
        cart_frame, columns=("flower", "num", "subtotal", "remove"), show="headings"
    )
    cart_tree.column("flower", width=100, anchor="center")
    cart_tree.column("num", width=100, anchor="center")
    cart_tree.column("subtotal", width=100, anchor="center")
    cart_tree.column("remove", width=100, anchor="center")
    cart_tree.heading("flower", text="꽃 이름")
    cart_tree.heading("num", text="구매 수량")
    cart_tree.heading("subtotal", text="소계")
    cart_tree.heading("remove", text="삭제")
    cart_tree.pack()

    total = 0

    for flower, (price, num) in cart.items():
        subtotal = price * num
        total += subtotal
        cart_tree.insert("", "end", values=(flower, num, subtotal, "삭제"))

    # 총합계를 표시하는 행을 추가
    cart_tree.insert("", "end", values=("", "총합계", total, ""))

    second_page.cart_frame = cart_frame

    # 트리뷰에 이벤트 연결
    cart_tree.bind("<Button-1>", remove_from_cart)


def open_payment_window():
    payment_window = tk.Toplevel()
    payment_window.geometry("500x500+280+100")

    # 카드 결제 버튼 추가
    card_payment_button = tk.Button(
        payment_window,
        text="카드 결제",
        command=show_card_insertion_screen,
        width=20,
        height=15,
    )
    card_payment_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # 바코드 결제 버튼 추가
    barcode_payment_button = tk.Button(
        payment_window,
        text="바코드 결제",
        command=show_barcode_recognition_screen,
        width=20,
        height=15,
    )
    barcode_payment_button.pack(side=tk.LEFT, padx=10, pady=10)


def barcode_payment():
    barcode_window = tk.Toplevel(root)
    barcode_window.title("바코드 결제")
    barcode_window.geometry("360x500+280+100")

    # PIL 라이브러리를 사용하여 이미지 로드
    barcode_image = Image.open("바코드_사진.png")
    barcode_image = ImageTk.PhotoImage(barcode_image)

    # 이미지 라벨 생성
    image_label = tk.Label(barcode_window, image=barcode_image)
    image_label.image = barcode_image  # 참조를 유지하기 위한 코드

    # 라벨 배치
    image_label.pack()

    barcode_window.mainloop()


def show_card_insertion_screen():
    card_insertion_window = tk.Toplevel()
    card_insertion_window.geometry("360x500+280+100")
    # PIL 라이브러리를 사용하여 이미지 로드
    card_image = Image.open("카드_사진.png")
    card_image = ImageTk.PhotoImage(card_image)

    # 이미지 라벨 생성
    image_label = tk.Label(card_insertion_window, image=card_image)
    image_label.image = card_image  # 참조를 유지하기 위한 코드

    # 라벨 배치
    image_label.pack()
    card_insertion_label = tk.Label(card_insertion_window, text="카드를 넣어주세요.")
    card_insertion_label.pack()

    def payment_confirmation():
        card_insertion_label.config(text="승인 중입니다.")
        time.sleep(3)
        card_insertion_label.config(text="결제가 완료되었습니다.")

        # 결제가 완료된 꽃을 집계
        for flower_name, (price, num) in cart.items():
            # flower_name을 이용하여 df에서 해당 꽃의 정보를 찾음
            flower_info = df[df["꽃 이름"] == flower_name].iloc[0]
            category = flower_info["카테고리"]

            if category in sales_data:
                sales_data[category][0] += num
                sales_data[category][1] += price * num
            else:
                sales_data[category] = [num, price * num]

        # 장바구니를 비움
        cart.clear()

    def start_payment():
        threading.Thread(target=payment_confirmation).start()

    confirm_button = tk.Button(card_insertion_window, text="확인", command=start_payment)
    confirm_button.pack(side="right", fill="x", expand=True)

    cancel_button = tk.Button(
        card_insertion_window, text="취소", command=card_insertion_window.destroy
    )
    cancel_button.pack(side="left", fill="x", expand=True)


global barcode_recognition_window


def show_barcode_recognition_screen():
    global barcode_recognition_window
    barcode_recognition_window = tk.Toplevel()
    barcode_recognition_window.geometry("360x500+280+100")

    barcode_recognition_label = tk.Label(
        barcode_recognition_window, text="바코드를 알맞은 위치에 대주세요."
    )
    barcode_recognition_label.pack()

    # 이미지 로드
    barcode_image = Image.open("바코드_사진.png")  # 이미지 파일 경로를 입력하세요.
    barcode_image = ImageTk.PhotoImage(barcode_image)

    # 이미지 라벨 생성
    image_label = tk.Label(barcode_recognition_window, image=barcode_image)
    image_label.image = barcode_image  # 참조를 유지하기 위한 코드

    # 라벨 배치
    image_label.pack()

    button_frame = tk.Frame(barcode_recognition_window)
    button_frame.pack(fill="x", expand=True)

    # 취소 버튼을 추가합니다.
    cancel_button = tk.Button(
        button_frame, text="취소", command=barcode_recognition_window.destroy
    )
    cancel_button.pack(side="left", fill="x", expand=True)

    # 확인 버튼을 추가합니다.
    confirm_button = tk.Button(button_frame, text="확인", command=confirm_barcode_payment)
    confirm_button.pack(side="right", fill="x", expand=True)

    barcode_recognition_window.mainloop()


def confirm_barcode_payment():
    global barcode_recognition_window
    # 결제가 완료된 꽃을 집계
    for flower_name, (price, num) in cart.items():
        # flower_name을 이용하여 df에서 해당 꽃의 정보를 찾음
        flower_info = df[df["꽃 이름"] == flower_name].iloc[0]
        category = flower_info["카테고리"]

        if category in sales_data:
            sales_data[category][0] += num
            sales_data[category][1] += price * num
        else:
            sales_data[category] = [num, price * num]

    # 장바구니를 비움
    cart.clear()
    # 바코드 인식 창을 닫음
    if barcode_recognition_window is not None:
        barcode_recognition_window.destroy()
        barcode_recognition_window = None


root = tk.Tk()
root.title("오직, 당신만을 위한 꽃")
root.geometry("480x720+200+0")

title_label = tk.Label(root, text="오직, 당신만을 위한 꽃")
title_label.pack(padx=10, pady=10)

create_button = tk.Button(root, text="만들기", command=create_second_page)
create_button.pack(padx=10, pady=10)

# '만들기'버튼의 '들'아래에 버튼 생성
management_button = tk.Button(root, command=open_admin_mode, relief=tk.FLAT)
management_button.pack()

root.mainloop()
