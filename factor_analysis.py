while True:
    num = int(input('请输入一个小于1000的整数：'))
    sum_num = num
    result = []
    for i in range(2,num):
        if num / i == 1:
            result.append(i)
            break
        while True:
            if num % i == 0:
                num = num/i
                result.append(i)
            else:
                break
    if result == []:
        print('{}不能因式分解'.format(sum_num))
    else:
        result_str = []
        for i in result:
            result_str.append(str(i))
        print('{0}='.format(int(sum_num)) + '*'.join(result_str))