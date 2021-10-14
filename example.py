def welcome(Someone):
    print("hello!"+Someone.upper())

X=input("請輸入全數字或全英文字母: ")

if X.isdigit():
    print("你輸入的數字: "+X)
    X=int(X)
    if(X>0):
        Sum=0
        for i in range(1,X+1):
            Sum+=i
        print("1+2+3+...+"+str(X)+" 總合為: "+str(Sum))
elif X.isalpha():
    welcome(X)
else:
    print("請輸入全數字或全英文字母")