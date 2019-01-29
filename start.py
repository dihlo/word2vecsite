from collections import namedtuple
import gensim
from flask import Flask, render_template, redirect, url_for, request
from redis import Redis

from word2vec_conf import NOT_CHANGE_WORD

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

Message = namedtuple('Message', 'text tag')
messages = []

modelPath_wiki="./vectors/all.bin"
model = gensim.models.KeyedVectors.load_word2vec_format(modelPath_wiki, binary=True)

not_change_word = NOT_CHANGE_WORD

new_sentence = []

Message = namedtuple('Message', 'text tag')

out_text = []
out_accuracy = 0

@app.route('/', methods=['GET'])
def hello_world():
	return render_template('index.html', messages=messages)

@app.route('/add', methods=['POST'])
def add():
	messages.clear()
	text = request.form['text']
	i = 0
	while i < 10:
		new_sentence = []
		accuracy = 0
		lines = text.split(' ')
		for elem in lines:
			if elem in not_change_word:
				new_sentence.append(elem)
				accuracy += 1
			else:
				w1 = elem
				try:
					out_word = model.most_similar(positive=w1, topn=10)
					new_sentence.append(out_word[i][0])
					accuracy += out_word[i][1]					
				except KeyError:
					new_sentence = 'нету_одного_из_слов_в_словаре'
					accuracy += 0.0001
					break
		out_text = ' '.join(new_sentence)
		out_accuracy = accuracy/len(lines)
		messages.append(Message(out_text, out_accuracy))
		out_accuracy = 0
		i += 1
	messages.insert(0, Message(text, 1))	
	return redirect(url_for('hello_world'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)