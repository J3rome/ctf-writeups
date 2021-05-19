import requests

def create_user(sess, username, password, bankname):
	r = sess.post(host + "/register.php", data={'uname': username, 'password': password, 'bank':bankname, 'btn': "Register+me!"})

def login(sess, username, password):
	r = sess.post(host + "/admin.php", data={'uname': username, 'password':password, 'btn':'Submit'})

def get_dashboard(sess):
	r = sess.get(host + "/dashboard.php")
	return r.text.split("Welcome ")[-1].replace("<br><br><br>","\n")

def do_withdraw(sess, amount, password):
	r = sess.post(host + "/with.php", data={'amnt': amount, 'pswd': password, 'wth':'withdraw'})

def do_deposit(sess, amount, password):
	r = sess.post(host + "/depo.php", data={'amnt': amount, 'pswd': password, 'wth':'Deposit'})

def do_transfer(sess, amount, password, account_nb, bankname):
	r = sess.post(host + "/tra.php", data={'amnt': amount, 'pswd': password, 'acc': account_nb, 'tbnk' : bankname, 'wth':'Transfer'})

if __name__ == "__main__":
	host="http://battery.thm"
	username = "user"
	password = "password"
	bankname = "ABC"

	s = requests.Session()

	# Retrieve session id
	s.get(host + "/admin.php")

	create_user(s, username, password, bankname)
	login(s, username, password)
	print(get_dashboard(s))