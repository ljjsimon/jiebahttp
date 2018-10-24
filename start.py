#coding=utf8

import os
from flask import Flask
from flask import request
import json
import jieba
import jieba.posseg as pseg

fh = open('config.json', 'r')
config = fh.read()
fh.close

config = json.loads(config)
port = config['port']
if (os.path.exists(config['dict_file'])):
    jieba.load_userdict(config['dict_file'])

app = Flask(__name__)

@app.route('/cut', methods=['POST','GET'])
def cut():
    if request.method == 'POST':
        sentence = request.form.get('sentence', default='')
        cut_all = request.form.get('cut_all', type=bool, default=False)
        HMM = request.form.get('HMM', type=bool, default=False)
    else:
        sentence = request.args.get('sentence','')
        cut_all = True if request.args.get('cut_all', False) else False
        HMM = True if request.args.get('HMM', False) else False

    if (sentence == ''):
        return ''

    seg_list = jieba.cut(sentence,cut_all,HMM)
    word = []
    for w in seg_list:
        word.append(w)

    return json.dumps(word)

@app.route('/cut_for_search', methods=['POST','GET'])
def cut_for_search():
    if request.method == 'POST':
        sentence = request.form.get('sentence', default='')
        HMM = request.form.get('HMM', type=bool, default=False)
    else:
        sentence = request.args.get('sentence','')
        HMM = True if request.args.get('HMM', False) else False

    if (sentence == ''):
        return ''

    seg_list = jieba.cut_for_search(sentence,HMM)
    word = []
    for w in seg_list:
        word.append(w)

    return json.dumps(word)

@app.route('/posseg_cut', methods=['POST', 'GET'])
def posseg_cut():
    if request.method == 'POST':
        sentence = request.form.get('sentence', default='')
        HMM = request.form.get('HMM', type=bool, default=False)
    else:
        sentence = request.args.get('sentence','')
        HMM = True if request.args.get('HMM', False) else False

    if (sentence == ''):
        return ''

    seg_dict = pseg.cut(sentence, HMM)
    word = []
    for w,f in seg_dict:
        word.append({
            "word":w,
            "flag":f
        })

    return json.dumps(word)

@app.route('/tokenize',methods=['POST','GUT'])
def tokenize():
    if request.method == 'POST':
        sentence = request.form.get('sentence', default='')
        mode = request.form.get('mode',default='default')
        HMM = request.form.get('HMM', type=bool, default=False)
    else:
        sentence = request.args.get('sentence','')
        mode = request.args.get('mode','default')
        HMM = True if request.args.get('HMM', False) else False

    if (sentence == ''):
        return ''

    result = pseg.cut(sentence, HMM)
    word = []
    for tk in seg_dict:
        word.append({
            "word":tk[0],
            "start":tk[1],
            "end":tk[2]
        })

    return json.dumps(word)

if __name__ == '__main__':
    app.run(port=port)