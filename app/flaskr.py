from flask import Flask,render_template, request, jsonify,  g, redirect, url_for

import urllib
from datetime import datetime
from bs4 import BeautifulSoup
from flask.ext.mysql import MySQL
 

app = Flask(__name__)
mysql=MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'code'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

def com(cur):
	cur.commit()

def insert(a,b,c,d):
 	con=mysql.connect()
	cur=con.cursor()
        sql = "insert into searchlist(code,time, price, price_change) values (%s,%s,%s,%s)"
        cur.execute(sql,(a,b,c,d))
	com(con)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search')
def search():
	k = request.args.get('k', "", type=str)
	try:
		html = urllib.urlopen("https://www.google.com/finance?q="+k+"&ei="+k)
        	soup = BeautifulSoup(html, "html.parser")
        	price = soup.find('meta', attrs={'itemprop':'price'})
        	change = soup.find('meta', attrs={'itemprop':'priceChange'})
        	symbol = soup.find('meta', attrs={'itemprop':'tickerSymbol'})
        	exchange = soup.find('meta', attrs={'itemprop':'exchange'})
        	code = str((exchange['content'])+":"+(symbol['content']))
        	time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		insert(code,time,price['content'],change['content'])
		
		return jsonify(result="Price : "+ price['content'] +", Price Change : "+ change['content'])
	except:
		return jsonify(result="code is not exist")

@app.route('/search_list')
def list():
	cursor = mysql.connect().cursor()
	cursor.execute('select * from searchlist')
	searchlist = cursor.fetchall()
	return render_template('list.html', searchlist=searchlist)

if __name__ == '__main__':
	app.run(debug=True)
