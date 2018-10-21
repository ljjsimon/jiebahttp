#coding=utf8

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
if (config['dict_file'] != 'default'):
    jieba.load_userdict(config['dict_file'])


app = Flask(__name__)

@app.route('/cut', methods=['POST','GET'])
def cut():
    if request.method == 'POST':
        sentence = request.form['sentence']
        cut_all = True if request.form['cut_all'] else False
        HMM = True if request.form['HMM'] else False
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
        sentence = request.form['sentence']
        HMM = True if request.form['HMM'] else False
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
        sentence = request.form['sentence']
        HMM = True if request.form['HMM'] else False
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
        sentence = request.form['sentence']
        mode = "search" if request.form['mode'] == 'search' else 'default'
        HMM = True if request.form['HMM'] else False
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