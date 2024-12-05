import random
import threading
import time

class Bank:
    def __init__(self):
        self.balance=0
        self.lock=threading.Lock()
    def deposit(self):
        self.lock.acquire()
        for i in range(100):
            val=random.randint(50,500)
            self.balance+=val
            print(f'Пополнение: {val}. Баланс: {self.balance}')
            if self.balance>=500 and self.lock.locked()==True:
                self.lock.release()
            time.sleep(0.001)
    def take(self):
        for i in range(100):
            val = random.randint(50, 500)
            print(f'Запрос на {val}')
            if val<=self.balance:
                self.balance -= val
                print(f'Снятие: {val}. Баланс: {self.balance}')
            else:
                print(f'Запрос отклонён, недостаточно средств')
                self.lock.acquire()
            time.sleep(0.001)

bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')