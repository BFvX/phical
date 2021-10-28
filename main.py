#DEBUG MAIN
from numpy.lib.function_base import select
from note_solve import NoResult, solve_eqn, solve_pre
import time
from ocr import ocr_score
from solve import solve_n_export
from tqdm import tqdm
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.lexers import Lexer
from typing import Callable

class BinomialLexer(Lexer):
    correct_word_list: list[str]
    correct_style: str
    wrong_style: str

    def __init__(self, correct_word_list: list[str], correct_style: str = '#00ff00 bold', wrong_style: str = '#ff0000'):
        self.correct_word_list = correct_word_list
        self.correct_style = correct_style
        self.wrong_style = wrong_style

    def lex_document(self, document: Document) -> Callable[[int], StyleAndTextTuples]:

        def get_line(linenum: int) -> StyleAndTextTuples:
            try:
                line = document.lines[linenum]
                if line.strip() in self.correct_word_list:
                    return [(self.correct_style, line)]
                else:
                    return [(self.wrong_style, line)]
            except IndexError:
                return []

        return get_line

def ask_for_chart() -> str:
    # load databases
    songs = os.listdir('./Assets/Tracks')
    songs_completer = FuzzyWordCompleter(songs)
    songname_lexer = BinomialLexer(songs)
    first = True
    while True:
        selected_song = prompt('歌曲ID(可输入曲名或作者进行模糊搜索)? ' if first else '歌曲ID? ', completer=songs_completer,
                               lexer=songname_lexer)
        if selected_song in songs:
            break
        first = False
        print('歌曲ID不存在，请重新输入')
    difficulties = [file[6:-5] for file in os.listdir(os.path.join('./Assets/Tracks', selected_song)) if
                    'ans' not in file]
    difficulty_completer = FuzzyWordCompleter(difficulties)
    difficulty_lexer = BinomialLexer(difficulties)
    while True:
        selected_difficulty = prompt(f'难度({difficulties})? ', completer=difficulty_completer, lexer=difficulty_lexer)
        if selected_difficulty in difficulties:
            break
        print('难度不存在，请重新输入')
    return selected_song, selected_difficulty

def reduce(judge_list):
    #reduce bad
    i,j=1,0
    bad_list = [judge[1][2] for judge in judge_list]
    length = len(bad_list)
    try:
        while(i<length):
            #print(i,j)
            #print(bad_list)
            while(bad_list[i]>=bad_list[j]):
                i = i + 1
                j = i - 1
            while(bad_list[i]<bad_list[j]):
                bad_list[j] = bad_list[i]
                j = j - 1
            i = i + 1
            j = i - 1
    except IndexError:
        pass
    for i in range(length):
        judge_list[i][1][2] = bad_list[i]
    #reduce perfect and good
    for i in range(1,length):
        if min(judge_list[i][1]-judge_list[i-1][1])<0:
            judge_list[i][1] = judge_list[i-1][1]
    
    return judge_list

def theory(numOfNotes,judge):
    return round(1e6*(judge[0]+0.65*judge[1]+numOfNotes-sum(judge))/numOfNotes)

def accuracy(judge):
    return str(round((judge[0]+0.65*judge[1]+0.0*judge[2])/sum(judge)*100,2))+'%'

if __name__ == '__main__':
    judge_list = []

    #select_chart = input("选择的曲目")
    #select_level = input("选择的难度")
    select_chart,select_level = ask_for_chart()
    start_actual = int(input("实际第一个音符判定时间(ms)："))
    time_list = ocr_score()

    #TODO: 使用缓存
    note_list = solve_n_export(select_chart,select_level)
    note_iter = iter(sorted(note_list.items()))

    note_time,note_attr = next(note_iter)
    delta = start_actual - note_time
    numOfNotes = max(attr['i'] for attr in sorted(note_list.items(),reverse=True)[0][1]) + 1
    print('正在计算判定：')
    for t in tqdm(time_list):
        bad = 0
        while(note_time+delta<=t[0]):
            try:
                note_time,note_attr = next(note_iter)
            except StopIteration:
                break
        pa = max(attr['i'] for attr in note_attr) + 1
        score = t[1]
        try:
            judge_list.append([t[0],solve_eqn(numOfNotes,score,bad,pa)])
        except NoResult:
            pass
    
    judge_list = reduce(judge_list)

    now = time.time()
    index = 0
    os.system('cls')
    print('开始按时间输出判定计算结果：')
    while(1):
        if(1000*(time.time()-now)>judge_list[index][0]):
            print('\r')
            print(judge_list[index])
            print('theory='+str(theory(numOfNotes,judge_list[index][1])))
            print('acc='+accuracy(judge_list[index][1]))
            index = index + 1
        if not index < len(judge_list):
            break