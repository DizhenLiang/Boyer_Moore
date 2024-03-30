#%%
import os
import re
# from boyer import boyer_moore_galil as boyer_moore
from q1 import boyer_moore_right_left as boyer_moore
# from q2 import q2 as boyer_moore
"""
Author: Raymond D'Souza
"""

"""
!!!!!!!!!! HAVE THIS IN YOUR ASSIGNMENT FOLDER !!!!
"""

"""
ASSUMPTIONS
    Boyer Moore algorithm file is booyerMoore.py
    Algorithm is named booyer_moore(txt, pat)

    Expected return is an list with '0' indexing and the first index of the pattern recognised
"""


#Retrieve Patterns
script_dir = os.path.dirname(__file__)


patterns = []
pat_path = os.path.join(script_dir,"Tests", "BoyerMoore_Pat.txt")

with open(pat_path, mode="r", encoding="utf-8-sig") as f:
    for line in f:
        if len(line) > 0:
            if line[0] != '#':
                patterns.append(line.strip())

#Retrieve texts
texts = []
text_path = os.path.join(script_dir, "Tests", "BoyerMoore_Text.txt")
with open(text_path, mode="r", encoding="utf-8-sig") as f:
    for line in f:
        if len(line) > 0:
            if line[0] != '#':
                texts.append(line.strip())
wrong = 0
correct=0
wrong_txt=[]
wrong_pat=[]
empty=0


for pat in patterns:
    for text in texts:
        #print(pat,text)
        bm_result = boyer_moore(text, pat)
        re_result = []
        for match in re.finditer(f'(?=({pat}))', text, flags=re.IGNORECASE):
            re_result.append(match.start())
        if len(re_result)==0 and len(bm_result)==0:
            empty+=1
        if (bm_result != re_result):
            print(f'    bm_result = {bm_result} \n    re_result={re_result}')
            print(f'text = {text}')
            print(f'pat = {pat}')
            print('fail')
            wrong+=1
            wrong_txt.append(text)
            wrong_pat.append(pat)
        else:
            # print(f'    bm_result = {bm_result} \n    re_result={re_result}')
            correct+=1

print(empty)
print("correct wrong: ",correct,wrong)
print(wrong_txt)
print(wrong_pat)


        #Use regex as the expected behaviour


# def boyer_moore(string, pat):
#     shift = 0
#     m=len(pat)
#     n=len(string)
#     bad = bad_chara(pat)
#     gs = good_suffix(pat)
#     mp = match_prefix(pat)

#     i=0
#     ans=[]
#     while i <= n-m:
#         counter=0
#         bad_shift=0
#         gs_mp_shift=0
#         mp_shift=0
#         # k = m-1-counter
#         while string[i+m-1-counter] == pat[m-1-counter] and counter<m:
#             # print(i+m-1-counter,m-1-counter)
#             # print("hahahhaha")
#             counter+=1
#             # print(counter)

#         # print(counter,'count')
#         if counter == m:
#             # print(str(i+1),'HAHA')
#             ans.append(i)
           
#             final_shift = m - mp[1]# +1 because the first index is length
#             i = i + final_shift
#             # print(str(final_shift),"exact_shift")
            
#         else:
#             k = m-1-counter 
#             # print(k,'k')
#             # mismatch_char = ord(string[i+m-1-counter])-97
#             mismatch_char = ord(string[i+k])-97
        
#             if bad[mismatch_char]== 0:
#                 bad_shift = 0
#             else:
#                 bad_shift = k - bad[mismatch_char][k] +1 # k - (bad[mismatch_char][k] - 1), minus 1 because at the bad_character, i plus 1

#             gs_mp_shift = m - gs[k+1]
#             match = 'used gs'
#             if gs[k+1] == 0:
#                 gs_mp_shift = m - mp[k+1]
#                 match='used mp'
   
#             # print(bad_shift,gs_mp_shift,f'shifts {match}')
#             final_shift = max(bad_shift, gs_mp_shift, mp_shift)
#             # print(i,final_shift,'hahaha')
#             i = i + final_shift
#             # print("b:" + str(final_shift))
#     return ans

