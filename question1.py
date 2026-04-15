def encrypt(shift1: int, shift2: int):
    # Open file 
    with open('raw_text.txt','r') as f:
        print(f.read())
# # loop through file
# check từng ký tự trong file
# nếu lơwercase: a--> m: shift forward by shift1*shift2 positions
#                 n-->z: shift backward by shift1+shift2
# nếu uppercase: A--> M: backward by shift1 positions
#                 (N-Z): shift forward by shift2? positions
# else: unchanged

encrypt(1,2)