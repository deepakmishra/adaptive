from problems.models import MCQQuestion, MCQAnswer
import random, json, sys, traceback

filename = "/Users/trapti/Downloads/mcq.json"

with open(filename,'r') as f:
    datastore = json.load(f)

s = set()

level_meta = {'Medium': {'score':4, 'min_sol':35, 'max_sol':50}, 'Very-Easy':{'score':1, 'min_sol':80, 'max_sol':100}, 'Hard':{'score':6, 'min_sol':0, 'max_sol':20}, 'Easy-Medium':{'score':3, 'min_sol':50, 'max_sol':65}, 'Easy':{'score':2, 'min_sol':65, 'max_sol':80}, 'Medium-Hard':{'score':5, 'min_sol':20, 'max_sol':35}}


for d in datastore:
    try:
        if str(d) in s:
            continue
        level = d['level']
        if not level.strip():
            level = 'Medium'
        score = level_meta[level]['score']
        min_sol = level_meta[level]['min_sol']
        max_sol = level_meta[level]['max_sol']
        sol = random.randint(min_sol,max_sol)
        avg_time = 15 + random.randint(0,100-sol)
        q = MCQQuestion(text=d['question'], score=score, solvability=sol, initial_average_time=avg_time)
        q.save()
        for option in d['options']:
            MCQAnswer(question=q,text=option['option'], correct=option['correct']).save()
        s.add(str(d))
    except:
        traceback.print_exc(file=sys.stdout)
        print d