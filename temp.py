import pyupbit

access_key = ""
secret_key = ""
upbit = pyupbit.Upbit(access_key, secret_key)

# 잔고 조회
balances = upbit.get_balances()

for balance in balances:
 print(balance)