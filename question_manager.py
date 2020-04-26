import os
import json
import sys

def to_answer(letter,c_len):
    letter = letter.upper()
    if len(letter) == 1 and 'A' <= letter <= 'Z':
        digit = ord(letter) - ord('A')
        if 0 <= digit < c_len:
            return digit, True
        else:
            return None, False
    elif letter == 'QUIT':
        return 'quit', False
    else :
        return None, False

def to_letter(n):
    return chr(ord('A') + n)

def ask_question(question, i):
    print('\n第{0}题：{1}'.format(i+1, question['question']))
    choices = question['choices']
    c_len = len(choices)
    for j in range(c_len):
        print('{0}:{1}'.format(to_letter(j),choices[j]))
    user_input = input('请输入答案：')
    user_answer, ok = to_answer(user_input,c_len)
    while not ok:
        if user_answer == 'quit':
            return 'quit'
        user_input = input('输入错误，请输入正确选项:')
        user_answer, ok = to_answer(user_input,c_len)
    if user_answer == question['answer']:
        return 'True'
    else :
        return 'False'

def read_question_file(filename):
    if not os.path.isfile(filename):
        return None
    with open(filename,'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except ValueError as e:
            print(e)
            print('加载题库出错！')
            return None

def get_filename(filename,ans_filename):
    filename = filename.split('\\')
    filename.pop()
    save_answer_file ='\\'.join(filename)+'\\'+ ans_filename
    f = open(save_answer_file,'w')
    f.close()
    return save_answer_file

def save_answer(filename,q_len,correct_count):
    save_answer_file=get_filename(filename,input('答题结束，保存答题进度，输入保存文件名：'))
    while not os.path.isfile(save_answer_file):
        save_answer_file =get_filename(filename,input('文件名错误，输入保存文件名：'))

    save_information ={}
    save_information['question_postion']=q_len
    save_information['correct_count']=correct_count
    with open(save_answer_file,'w',encoding='utf-8') as f:
        try:
            #save_information = json.dumps(save_information,indent=4,separators=(',',':'))
            json.dump(save_information,f)
            return save_answer_file, True
        except ValueError as e:
            print(e)
            return None,False


def main(argv):
    if len(argv) != 2:
        print('请指定题库文件！')
        sys.exit(-1)

    #定义题库列表 ，每道题目为一个字典
    filename = argv[1]
    question_json = read_question_file(filename)
    if not question_json:
        print('题库文件读取失败，请检查{0}文件'.format(filename))
        sys.exit(-1)
    question_name = question_json['question_name']
    question_list = question_json['question_list']
    print('题库文件：{}'.format(question_name))

    #遍历题库列表
    q_len = 0
    correct_count = 0
    accuracy = 0
    for i, q in enumerate(question_list):
        #展示题目、提示用户输入、判断答案
        user_answer_ok = ask_question(q, i)
        if user_answer_ok == 'True':
            correct_count += 1
        elif user_answer_ok == 'quit' :
            save_answer_file, ok = save_answer(filename,q_len,correct_count)
            pos = 0

            while not ok:
                print('答题进度保存失败')
                pos += 1
                if pos == 1:
                    break

            if q_len == 0:
                accuracy = 0
            else :
                accuracy = correct_count/q_len

            print('\n共回答{0}道题目，你答对了{1}题。正确率为{2:.2f}%.'.
                format(q_len,correct_count,accuracy*100))
            print('答题进度保存成功，保存至{}'.format(save_answer_file))
            with open(save_answer_file,'r') as f:
                print(json.load(f))
            sys.exit(0)

        #计算并展示正确率
        q_len += 1
        print('\n共回答{0}道题目，你答对了{1}题。正确率为{2:.2f}%.'.
            format(q_len,correct_count,correct_count/q_len*100))

if __name__ == '__main__':
    main(sys.argv)