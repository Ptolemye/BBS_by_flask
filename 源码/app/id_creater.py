import random
#用于生成15位的随机数字ID
def id_creater():
    random_string = ""
    for _ in range(15):
        random_number = random.randint(1, 9)
        random_string += str(random_number)
    return random_string