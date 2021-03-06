import imaplib
import verifier

from time import sleep

verificationUrls = []
mails = [
	['neko@nulled.systems', '471!T1Z%6Y12Nyj'],
]

for email in mails:
	email, password = email
	mail = imaplib.IMAP4_SSL('nulled.systems',993)
	print('Attempting: {0}'.format(email))
	try:
		mail.login(email, password)
		print('Valid: {0}'.format(email))
	except Exception as e:
		print(e)
		#print('Invalid: {0}:{1}'.format(email, password))
		continue
	mail.list()
	mail.select("inbox")

	result, data = mail.uid('search', None, '(HEADER Subject "Verify Email")')
	iterData = data[0].decode('utf-8').split(' ')
	r, d = mail.uid('fetch', ','.join(iterData), '(RFC822)')

	for b in d:
		try:
			b = b[1].decode('utf-8')
		except:
			continue
		verificationUrls.append(str(b).split('<a href="')[2].split('"')[0].split('=')[1])

	mail.uid('STORE', ','.join(iterData) , '+FLAGS', '(\Deleted)')  
	mail.expunge() 

	print('Parsed: {0}'.format(email))

print('[+] Got {0} verification URLs'.format(len(verificationUrls)))

emailVerifier = verifier.main(verificationUrls)
