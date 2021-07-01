#this code probably isnt pretty, deal with it!
#ill make it nicer later, maybe

try:
	import requests, queue, time, os, threading, ctypes
	from colorama import init, Fore
except:
	print("[!] Missing required libraries")
	input()
	exit()

#boop
clear = lambda: os.system("cls")
usernames = queue.Queue()
proxy_list = queue.Queue()
req = requests.Session()
lock = threading.Lock()
init()

#some vars
checked = 0
available = 0
errors = 0

#window title
ctypes.windll.kernel32.SetConsoleTitleW(f'Linked Multi Checker | Menu')

#text printing / random
def console_title():
	global checked
	global available
	global errors

	while True:
		ctypes.windll.kernel32.SetConsoleTitleW(f'Checked: {checked} | Available: {available} | Errors: {errors}')
		time.sleep(.1)

def title():
	print(f"""
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} Linked {Fore.RED}Username{Fore.RESET} Checker
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} Made by Krul""")

def modules():
		print(f"""
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}1{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Snapchat
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}2{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Anilist
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}3{Fore.LIGHTBLACK_EX}]{Fore.RESET} - WeHeartIt
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}4{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Origin
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}5{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Tap.Bio
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}6{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Beacons
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}7{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Liinks""")


#snapchat checking
def start_snapchat():
	clear()
	title()

	ctypes.windll.kernel32.SetConsoleTitleW(f'Linked Multi Checker | Snapchat')

	print(f"""
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}1{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Use proxies
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}2{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Proxyless""")
	print(f"\n {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} > ", end="")
	proxy_choice = int(input())

	if proxy_choice == 1:
		proxy_length = 0
		for proxy in open("proxies.txt", "r"):
			proxy_list.put(proxy.rstrip())
			proxy_length += 1
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Loaded {Fore.RED}{proxy_length}{Fore.RESET} proxies, press enter to continue")
		input()

	clear()
	title()
	print(f"\n {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Threads: ", end="")
	thread_count = int(input())
	print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Wordlist: ", end="")
	wordlist = input()
	wordlist_length = 0

	try:
		for username in open(wordlist, "r"):
			usernames.put(username.rstrip())
			wordlist_length += 1
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Loaded {Fore.RED}{wordlist_length}{Fore.RESET} usernames, press enter to start")
	except Exception as e:
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Failed to find {wordlist}, make sure it is in the same directory")

	input()
	clear()

	threading.Thread(target=console_title).start()

	for i in range(thread_count):
		threading.Thread(target=check_snapchat, args=(proxy_choice, )).start()

def check_snapchat(proxy_choice):
	global checked
	global available
	global errors

	headers = {
        "User-Agent":      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept":          "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer":         "https://accounts.snapchat.com/",
        "Cookie":          "xsrf_token=PlEcin8s5H600toD4Swngg; sc-cookies-accepted=true; web_client_id=b1e4a3c7-4a38-4c1a-9996-2c4f24f7f956; oauth_client_id=c2Nhbg==",
        "Connection":      "keep-alive",
        "Content-Type":    "application/x-www-form-urlencoded; charset=utf-8"
    	}

	while not usernames.empty():
		username = usernames.get()

		url = f"https://accounts.snapchat.com/accounts/get_username_suggestions?requested_username={username}&xsrf_token=PlEcin8s5H600toD4Swngg"

		try:
			if proxy_choice == 1:
				proxy = proxy_list.get()
				proxy_list.put(proxy)

				proxies = {
					'http':  f'http://{proxy}',
					'https': f'http://{proxy}',
					}

				r = req.post(url, headers=headers, proxies=proxies, timeout=5)

				while r.status_code != 200:
					r = req.post(url, headers=headers, proxies=proxies, timeout=5)
					errors += 1
			
			else:
				r = req.post(url, headers=headers, timeout=5)

				while r.status_code != 200:
					r = req.post(url, headers=headers, timeout=5)
					errors += 1

			res = r.json()

			if res['reference']['status_code'] == "OK":
				with lock:
					checked += 1
					print(f" {Fore.GREEN}[{Fore.RESET}{checked}{Fore.GREEN}]{Fore.RESET} - @{Fore.GREEN}{username}{Fore.RESET}")
					available += 1
					with open('results/snapchat.txt', "a") as prime:
						prime.write(f'{username}\n')
			else:
				with lock:
					checked += 1
					print(f" {Fore.RED}[{Fore.RESET}{checked}{Fore.RED}]{Fore.RESET} - @{Fore.RED}{username}{Fore.RESET}")

		except:
			errors += 1
			usernames.put(username)
			continue


#anilist checking
def start_anilist():
	clear()
	title()

	ctypes.windll.kernel32.SetConsoleTitleW(f'Linked Multi Checker | Anilist')

	print(f"""
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}1{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Use proxies
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}2{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Proxyless""")
	print(f"\n {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} > ", end="")
	proxy_choice = int(input())

	if proxy_choice == 1:
		proxy_length = 0
		for proxy in open("proxies.txt", "r"):
			proxy_list.put(proxy.rstrip())
			proxy_length += 1
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Loaded {Fore.RED}{proxy_length}{Fore.RESET} proxies, press enter to continue")
		input()

	clear()
	title()
	print(f"\n {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Threads: ", end="")
	thread_count = int(input())
	print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Wordlist: ", end="")
	wordlist = input()
	wordlist_length = 0

	try:
		for username in open(wordlist, "r"):
			usernames.put(username.rstrip())
			wordlist_length += 1
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Loaded {Fore.RED}{wordlist_length}{Fore.RESET} usernames, press enter to start")
	except Exception as e:
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Failed to find {wordlist}, make sure it is in the same directory")

	input()
	clear()

	threading.Thread(target=console_title).start()

	for i in range(thread_count):
		threading.Thread(target=check_anilist, args=(proxy_choice, )).start()

def check_anilist(proxy_choice):
	global checked
	global available
	global errors

	headers = {
		"Host":         "anilist.co",
		"schema":       "internal",
		"User-Agent":   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
		"Content-Type": "application/json"
		}

	while not usernames.empty():
		username = usernames.get()

		payload = {
			"query":     "mutation($name:String){CreateUser(userName:$name){id name about avatar{large}bannerImage unreadNotificationCount donatorTier donatorBadge moderatorRoles options{titleLanguage airingNotifications displayAdultContent profileColor notificationOptions{type enabled}}mediaListOptions{scoreFormat rowOrder animeList{customLists sectionOrder splitCompletedSectionByFormat advancedScoring advancedScoringEnabled}mangaList{customLists sectionOrder splitCompletedSectionByFormat advancedScoring advancedScoringEnabled}}}}",
			"variables": {"name":username}
			}

		url = "https://anilist.co/graphql"

		try:
			if proxy_choice == 1:
				proxy = proxy_list.get()
				proxy_list.put(proxy)

				proxies = {
					'http':  f'http://{proxy}',
					'https': f'http://{proxy}',
					}

				r = req.post(url, headers=headers, json=payload, proxies=proxies, timeout=5)

				while r.status_code != 400:
					r = req.post(url, headers=headers, json=payload, proxies=proxies, timeout=5)
					errors += 1
			
			else:
				r = req.post(url, headers=headers, json=payload, timeout=5)

				while r.status_code != 400:
					r = req.post(url, headers=headers, json=payload, timeout=5)
					errors += 1

			res = r.json()

			if "userName" not in res['errors'][0]['validation']:
				with lock:
					checked += 1
					print(f" {Fore.GREEN}[{Fore.RESET}{checked}{Fore.GREEN}]{Fore.RESET} - @{Fore.GREEN}{username}{Fore.RESET}")
					available += 1
					with open('results/anilist.txt', "a") as prime:
						prime.write(f'{username}\n')
			else:
				with lock:
					checked += 1
					print(f" {Fore.RED}[{Fore.RESET}{checked}{Fore.RED}]{Fore.RESET} - @{Fore.RED}{username}{Fore.RESET}")

		except:
			errors += 1
			usernames.put(username)
			continue


#weheartit
def start_whi():
	clear()
	title()
	print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} This module may have some false positives")

	ctypes.windll.kernel32.SetConsoleTitleW(f'Linked Multi Checker | WeHeartIt')

	print(f"""
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}1{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Use proxies
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}2{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Proxyless""")
	print(f"\n {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} > ", end="")
	proxy_choice = int(input())

	if proxy_choice == 1:
		proxy_length = 0
		for proxy in open("proxies.txt", "r"):
			proxy_list.put(proxy.rstrip())
			proxy_length += 1
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Loaded {Fore.RED}{proxy_length}{Fore.RESET} proxies, press enter to continue")
		input()

	clear()
	title()
	print(f"\n {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Threads: ", end="")
	thread_count = int(input())
	print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Wordlist: ", end="")
	wordlist = input()
	wordlist_length = 0

	try:
		for username in open(wordlist, "r"):
			usernames.put(username.rstrip())
			wordlist_length += 1
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Loaded {Fore.RED}{wordlist_length}{Fore.RESET} usernames, press enter to start")
	except Exception as e:
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Failed to find {wordlist}, make sure it is in the same directory")

	input()
	clear()

	threading.Thread(target=console_title).start()

	for i in range(thread_count):
		threading.Thread(target=check_whi, args=(proxy_choice, )).start()

def check_whi(proxy_choice):
	global checked
	global available
	global errors

	while not usernames.empty():
		username = usernames.get()

		url = f"https://weheartit.com/{username}" #im lazy so we use front end api

		try:
			if proxy_choice == 1:
				proxy = proxy_list.get()
				proxy_list.put(proxy)

				proxies = {
					'http':  f'http://{proxy}',
					'https': f'http://{proxy}',
					}

				r = req.get(url, proxies=proxies, timeout=5)
			
			else:
				r = req.get(url, timeout=5)

			if r.status_code == 404:
				with lock:
					checked += 1
					print(f" {Fore.GREEN}[{Fore.RESET}{checked}{Fore.GREEN}]{Fore.RESET} - @{Fore.GREEN}{username}{Fore.RESET}")
					available += 1
					with open('results/whi.txt', "a") as prime:
						prime.write(f'{username}\n')
			elif r.status_code == 200:
				with lock:
					checked += 1
					print(f" {Fore.RED}[{Fore.RESET}{checked}{Fore.RED}]{Fore.RESET} - @{Fore.RED}{username}{Fore.RESET}")	
			else:
				errors += 1
				usernames.put(username)

		except:
			errors += 1
			usernames.put(username)
			continue


#origin
def start_origin():
	clear()
	title()

	ctypes.windll.kernel32.SetConsoleTitleW(f'Linked Multi Checker | Origin')

	print(f"""
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}1{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Use proxies
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}2{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Proxyless""")
	print(f"\n {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} > ", end="")
	proxy_choice = int(input())

	if proxy_choice == 1:
		proxy_length = 0
		for proxy in open("proxies.txt", "r"):
			proxy_list.put(proxy.rstrip())
			proxy_length += 1
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Loaded {Fore.RED}{proxy_length}{Fore.RESET} proxies, press enter to continue")
		input()

	clear()
	title()
	print(f"\n {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Threads: ", end="")
	thread_count = int(input())
	print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Wordlist: ", end="")
	wordlist = input()
	wordlist_length = 0

	try:
		for username in open(wordlist, "r"):
			usernames.put(username.rstrip())
			wordlist_length += 1
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Loaded {Fore.RED}{wordlist_length}{Fore.RESET} usernames, press enter to start")
	except Exception as e:
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Failed to find {wordlist}, make sure it is in the same directory")

	input()
	clear()

	threading.Thread(target=console_title).start()

	for i in range(thread_count):
		threading.Thread(target=check_origin, args=(proxy_choice, )).start()

def check_origin(proxy_choice):
	global checked
	global available
	global errors

	while not usernames.empty():
		username = usernames.get()

		url = f"https://signin.ea.com/p/ajax/user/checkOriginId?requestorId=portal&originId={username}" #im lazy so we use front end api

		try:
			if proxy_choice == 1:
				proxy = proxy_list.get()
				proxy_list.put(proxy)

				proxies = {
					'http':  f'http://{proxy}',
					'https': f'http://{proxy}',
					}

				r = req.get(url, proxies=proxies, timeout=5)

				while r.status_code != 200:
					r = req.get(url, proxies=proxies, timeout=5)
					errors += 1
			
			else:
				r = req.get(url, timeout=5)

				while r.status_code != 200:
					r = req.get(url, timeout=5)
					errors += 1
				
			res = r.json()

			if res['status'] == True:
				with lock:
					checked += 1
					print(f" {Fore.GREEN}[{Fore.RESET}{checked}{Fore.GREEN}]{Fore.RESET} - @{Fore.GREEN}{username}{Fore.RESET}")
					available += 1
					with open('results/origin.txt', "a") as prime:
						prime.write(f'{username}\n')
			else:
				with lock:
					checked += 1
					print(f" {Fore.RED}[{Fore.RESET}{checked}{Fore.RED}]{Fore.RESET} - @{Fore.RED}{username}{Fore.RESET}")

		except:
			errors += 1
			usernames.put(username)
			continue


#tap.bio
def start_tap():
	clear()
	title()

	ctypes.windll.kernel32.SetConsoleTitleW(f'Linked Multi Checker | Tap.bio')

	print(f"""
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}1{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Use proxies
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}2{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Proxyless""")
	print(f"\n {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} > ", end="")
	proxy_choice = int(input())

	if proxy_choice == 1:
		proxy_length = 0
		for proxy in open("proxies.txt", "r"):
			proxy_list.put(proxy.rstrip())
			proxy_length += 1
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Loaded {Fore.RED}{proxy_length}{Fore.RESET} proxies, press enter to continue")
		input()

	clear()
	title()
	print(f"\n {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Threads: ", end="")
	thread_count = int(input())
	print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Wordlist: ", end="")
	wordlist = input()
	wordlist_length = 0

	try:
		for username in open(wordlist, "r"):
			usernames.put(username.rstrip())
			wordlist_length += 1
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Loaded {Fore.RED}{wordlist_length}{Fore.RESET} usernames, press enter to start")
	except Exception as e:
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Failed to find {wordlist}, make sure it is in the same directory")

	input()
	clear()

	threading.Thread(target=console_title).start()

	for i in range(thread_count):
		threading.Thread(target=check_tap, args=(proxy_choice, )).start()

def check_tap(proxy_choice):
	global checked
	global available
	global errors

	while not usernames.empty():
		username = usernames.get()

		payload = {
			"operationName":"usernameSearch",
			"variables":    {"username":username},
			"query":        "query usernameSearch($username: String!) {\n  publicAccount(username: $username) {\n    username\n    __typename\n  }\n}\n"
			}

		url = "https://api.tap.bio/graphql"

		try:
			if proxy_choice == 1:
				proxy = proxy_list.get()
				proxy_list.put(proxy)

				proxies = {
					'http':  f'http://{proxy}',
					'https': f'http://{proxy}',
					}

				r = req.post(url, json=payload, proxies=proxies, timeout=5)

				while r.status_code != 200:
					r = req.post(url, json=payload, proxies=proxies, timeout=5)
					errors += 1
			
			else:
				r = req.post(url, json=payload, timeout=5)

				while r.status_code != 200:
					r = req.post(url, json=payload, timeout=5)
					errors += 1

			res = r.json()

			if res['data']['publicAccount'] == None:
				with lock:
					checked += 1
					print(f" {Fore.GREEN}[{Fore.RESET}{checked}{Fore.GREEN}]{Fore.RESET} - @{Fore.GREEN}{username}{Fore.RESET}")
					available += 1
					with open('results/tapbio.txt', "a") as prime:
						prime.write(f'{username}\n')
			else:
				with lock:
					checked += 1
					print(f" {Fore.RED}[{Fore.RESET}{checked}{Fore.RED}]{Fore.RESET} - @{Fore.RED}{username}{Fore.RESET}")

		except:
			errors += 1
			usernames.put(username)
			continue


#beacons.ai
def start_beacons():
	clear()
	title()
	print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} This module may be slow to start due to API lag")

	ctypes.windll.kernel32.SetConsoleTitleW(f'Linked Multi Checker | Beacons.ai')

	print(f"""
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}1{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Use proxies
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}2{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Proxyless""")
	print(f"\n {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} > ", end="")
	proxy_choice = int(input())

	if proxy_choice == 1:
		proxy_length = 0
		for proxy in open("proxies.txt", "r"):
			proxy_list.put(proxy.rstrip())
			proxy_length += 1
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Loaded {Fore.RED}{proxy_length}{Fore.RESET} proxies, press enter to continue")
		input()

	clear()
	title()
	print(f"\n {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Threads: ", end="")
	thread_count = int(input())
	print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Wordlist: ", end="")
	wordlist = input()
	wordlist_length = 0

	try:
		for username in open(wordlist, "r"):
			usernames.put(username.rstrip())
			wordlist_length += 1
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Loaded {Fore.RED}{wordlist_length}{Fore.RESET} usernames, press enter to start")
	except Exception as e:
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Failed to find {wordlist}, make sure it is in the same directory")

	input()
	clear()

	threading.Thread(target=console_title).start()

	for i in range(thread_count):
		threading.Thread(target=check_beacons, args=(proxy_choice, )).start()

def check_beacons(proxy_choice):
	global checked
	global available
	global errors

	while not usernames.empty():
		username = usernames.get()

		payload = {
			"new_username":username,
			"action":      "check_if_username_taken"
			}

		url = "https://us-central1-beacons-sup.cloudfunctions.net/user_profile"

		try:
			if proxy_choice == 1:
				proxy = proxy_list.get()
				proxy_list.put(proxy)

				proxies = {
					'http':  f'http://{proxy}',
					'https': f'http://{proxy}',
					}

				r = req.post(url, json=payload, proxies=proxies, timeout=None)

				while r.status_code != 200:
					r = req.post(url, json=payload, proxies=proxies, timeout=None)
					errors += 1
			
			else:
				r = req.post(url, json=payload, timeout=None)

				while r.status_code != 200:
					r = req.post(url, json=payload, timeout=None)
					errors += 1

			res = r.json()

			if res['username_taken'] == False:
				with lock:
					checked += 1
					print(f" {Fore.GREEN}[{Fore.RESET}{checked}{Fore.GREEN}]{Fore.RESET} - @{Fore.GREEN}{username}{Fore.RESET}")
					available += 1
					with open('results/beacons.txt', "a") as prime:
						prime.write(f'{username}\n')
			else:
				with lock:
					checked += 1
					print(f" {Fore.RED}[{Fore.RESET}{checked}{Fore.RED}]{Fore.RESET} - @{Fore.RED}{username}{Fore.RESET}")

		except:
			errors += 1
			usernames.put(username)
			continue


#liinks.co
def start_liinks():
	clear()
	title()
	print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} This module may be slow to start due to API lag")

	ctypes.windll.kernel32.SetConsoleTitleW(f'Linked Multi Checker | Liinks.co')

	print(f"""
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}1{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Use proxies
 {Fore.LIGHTBLACK_EX}[{Fore.RESET}2{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Proxyless""")
	print(f"\n {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} > ", end="")
	proxy_choice = int(input())

	if proxy_choice == 1:
		proxy_length = 0
		for proxy in open("proxies.txt", "r"):
			proxy_list.put(proxy.rstrip())
			proxy_length += 1
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Loaded {Fore.RED}{proxy_length}{Fore.RESET} proxies, press enter to continue")
		input()

	clear()
	title()
	print(f"\n {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Threads: ", end="")
	thread_count = int(input())
	print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Wordlist: ", end="")
	wordlist = input()
	wordlist_length = 0

	try:
		for username in open(wordlist, "r"):
			usernames.put(username.rstrip())
			wordlist_length += 1
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Loaded {Fore.RED}{wordlist_length}{Fore.RESET} usernames, press enter to start")
	except Exception as e:
		print(f" {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} - Failed to find {wordlist}, make sure it is in the same directory")

	input()
	clear()

	threading.Thread(target=console_title).start()

	for i in range(thread_count):
		threading.Thread(target=check_liinks, args=(proxy_choice, )).start()

def check_liinks(proxy_choice):
	global checked
	global available
	global errors

	while not usernames.empty():
		username = usernames.get()

		payload = {
			"operationName":"getIsUserSlugUnique",
			"variables":{"slug":username},
			"query":"mutation getIsUserSlugUnique($slug: String!) {\n  isUserSlugUnique(slug: $slug)\n}\n"
			}

		url = "https://www.liinks.co/i/graphql"

		try:
			if proxy_choice == 1:
				proxy = proxy_list.get()
				proxy_list.put(proxy)

				proxies = {
					'http':  f'http://{proxy}',
					'https': f'http://{proxy}',
					}

				r = req.post(url, json=payload, proxies=proxies, timeout=None)

				while r.status_code != 200:
					r = req.post(url, json=payload, proxies=proxies, timeout=None)
					errors += 1
			
			else:
				r = req.post(url, json=payload, timeout=None)

				while r.status_code != 200:
					r = req.post(url, json=payload, timeout=None)
					errors += 1

			res = r.json()

			if res['data']['isUserSlugUnique'] == True:
				with lock:
					checked += 1
					print(f" {Fore.GREEN}[{Fore.RESET}{checked}{Fore.GREEN}]{Fore.RESET} - @{Fore.GREEN}{username}{Fore.RESET}")
					available += 1
					with open('results/liinks.txt', "a") as prime:
						prime.write(f'{username}\n')
			else:
				with lock:
					checked += 1
					print(f" {Fore.RED}[{Fore.RESET}{checked}{Fore.RED}]{Fore.RESET} - @{Fore.RED}{username}{Fore.RESET}")

		except:
			errors += 1
			usernames.put(username)
			continue



if __name__ == '__main__':
	clear()
	title()
	modules()

	print(f"\n {Fore.LIGHTBLACK_EX}[{Fore.RESET}>{Fore.LIGHTBLACK_EX}]{Fore.RESET} > ", end="")
	selection = int(input())

	if selection == 1:
		start_snapchat()
	elif selection == 2:
		start_anilist()
	elif selection == 3:
		start_whi()
	elif selection == 4:
		start_origin()
	elif selection == 5:
		start_tap()
	elif selection == 6:
		start_beacons()
	elif selection == 7:
		start_liinks()