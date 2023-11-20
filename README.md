# programming_teamproject
import pandas as pd

class FlowerShop:
    def __init__(self, flower_data):
        self.flower_data = flower_data
        self.categories = list(self.flower_data['카테고리'].unique())
        self.cart = []

    def show_categories(self):
        print("카테고리 목록:")
        for category in self.categories:
            print(category, end='  ')
        print("\n")

    def show_flowers(self, category):
        category_flowers = self.flower_data[self.flower_data['카테고리'] == category]
        print(f"{category} 카테고리의 꽃 목록:")
        for index, row in category_flowers.iterrows():
            print(f"{row['꽃 이름']} - 가격 등급: {row['가격 등급']}")
        print("\n")

    def select_flower(self, category, flower):
        quantity = int(input(f"선택한 {flower}의 수량을 입력하세요: "))
        price = self.calculate_price(flower, quantity)
        self.add_to_cart(category, flower, quantity, price)
        print(f"{flower} {quantity} 송이가 장바구니에 추가되었습니다.\n")

    def calculate_price(self, flower, quantity):
        flower_info = self.flower_data[self.flower_data['꽃 이름'] == flower].iloc[0]
        price_grade = flower_info['가격 등급']

        if price_grade == 'A':
            return quantity * 3000
        elif price_grade == 'B':
            return quantity * 2000
        elif price_grade == 'C':
            return quantity * 1000
        else:
            print("가격 등급이 잘못 지정되었습니다.")

    def add_to_cart(self, category, flower, quantity, price):
        self.cart.append({'category': category, 'flower': flower, 'quantity': quantity, 'price': price})

    def show_cart(self):
        print("장바구니:")
        for item in self.cart:
            print(f"{item['flower']} ({item['quantity']} 송이) - ${item['price']}")
        total_price = sum(item['price'] for item in self.cart)
        print(f"\n총 가격: ${total_price}\n")

    def checkout(self):
        print("결제 창")
        payment_method = input("결제 방식을 선택하세요 (카드 또는 현금): ")
        if payment_method.lower() == '카드':
            print("카드 결제가 완료되었습니다.")
        elif payment_method.lower() == '현금':
            print("현금 결제가 완료되었습니다.")
        else:
            print("잘못된 결제 방식입니다. 다시 시도해주세요.")


def main():
    # CSV 파일에서 데이터 읽어오기
    flower_data = pd.read_csv('/Users/seoyunho/Desktop/프로그래밍응용/프로그래밍응용 팀플/꽃 자료 최종 (2).csv')


    flower_shop = FlowerShop(flower_data)

    while True:
        print("\n=== 꽃 구매 키오스크 ===")
        flower_shop.show_categories()

        selected_category = input("카테고리를 선택하세요 (종료: q): ")
        if selected_category.lower() == 'q':
            break

        if selected_category in flower_shop.categories:
            flower_shop.show_flowers(selected_category)
            selected_flower = input("꽃을 선택하세요: ")
            flower_shop.select_flower(selected_category, selected_flower)
        else:
            print("잘못된 카테고리입니다. 다시 선택해주세요.")

    flower_shop.show_cart()
    flower_shop.checkout()


if __name__ == "__main__":
    main()
