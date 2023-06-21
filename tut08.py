from datetime import datetime
start_time = datetime.now()
def getBatsman(player):
	for person in all_players:
		if player in person:
			return person
def getBowler(player):
	for person in all_players:
		if player in person:
			return person
def scorecard():
	#made two lists which contain all the players of team India and team pakistan
	team_india = ['Rohit Sharma (c)', 'KL Rahul', 'Virat Kohli', 'Suryakumar Yadav', 'Dinesh Karthik (wk)', 'Hardik Pandya', 'Ravindra Jadeja', 'Bhuvneshwar Kumar', 'Avesh Khan', 'Yuzvendra Chahal', 'Arshdeep Singh']
	team_pakistan = ['Babar Azam (c)', 'Mohammad Rizwan (wk)', 'Fakhar Zaman', 'Iftikhar Ahmed', 'Khushdil Shah', 'Asif Ali', 'Shadab Khan', 'Mohammad Nawaz', 'Naseem Shah', 'Haris Rauf', 'Shahnawaz Dahani']
	global all_players
	all_players = team_india + team_pakistan
	#Dictionary containing details of innings1 and innings2
	#the total team run,wicket and balls are there inside dictionary.
	#other than above mentioned there is a bowling,batting and extras dictionary foe storing details of bowling,batting and extras details.
	inns1 = {'run': 0, 'wicket': 0, 'balls': 0, 'bowling': {player : {'run': 0, 'balls': 0, 'maiden': 0, 'wicket': 0, 'nb': 0, 'wide': 0} for player in team_india},'batting': {player : {'balls': 0,'run': 0, '4s': 0, '6s': 0, 'status': ''} for player in team_pakistan}, 'extras': {'bye': 0, 'nb': 0, 'lb': 0, 'wide': 0, 'p': 0}, 'did_not_bat': team_pakistan.copy(), 'fall_of_wicket': [], 'powerplay': 0}
	inns2 = {'run': 0, 'wicket': 0, 'balls': 0, 'bowling': {player : {'run': 0, 'balls': 0, 'maiden': 0, 'wicket': 0, 'nb': 0, 'wide': 0} for player in team_pakistan},'batting': {player : {'balls': 0,'run': 0,'4s': 0, '6s': 0, 'status': ''} for player in team_india}, 'extras': {'bye': 0, 'nb': 0, 'lb': 0, 'wide': 0, 'p': 0}, 'did_not_bat': team_india.copy(), 'fall_of_wicket': [], 'powerplay': 0}
	run_initial=-1
	try:
		with open('india_inns2.txt', 'r') as innings2, open('pak_inns1.txt', 'r') as innings1, open('scorecard.txt', 'w') as output:
			#reading the commentary text files
			commentary1 = innings1.readlines()
			commentary2 = innings2.readlines()
			innings=1
			for inns, lines in zip([inns1, inns2], [commentary1, commentary2]):	
				for info in [line for line in lines if line.strip()]:
					#finding the batsmans name from the lines
					try:
						batter = getBatsman(info.split(",")[0].split(" ", 1)[1].split("to")[1].strip())
					except:
						print("Error while getting batsman details")
					#removing batsman from the whole list of batsman if he came for batting
					if batter in inns['did_not_bat']:
						inns['did_not_bat'].remove(batter)
					#finding the bowler from commentary lines
					try:
						bowler = getBowler(info.split(",")[0].split(" ", 1)[1].split("to")[0].strip())
					except:
						print("Error while getting bowler details")
					#finding maiden over.
					#getting runs when its start of bowling
					if inns['bowling'][bowler]['balls']%6==0:
						run_initial=inns['bowling'][bowler]['run']
					#finding the runs scored from commentary 
					runs = info.split(",")[1].strip()
					over_number=info.split(",")[0].split(" ", 1)[0].strip()
					#if the commentary says no run, number of balls is increased by 1,
					#no.of balls faced by batsman is increased by 1, his batting status is not out and no.of bowls by bowlwer also increased by 1
									#when a batsman is out
					#wicket count is added by 1
					#the wicket count of bowler is inceased by 1
					if runs.split(" ")[0].strip() == "out":
						inns['balls'] += 1
						inns['wicket'] += 1	
						inns['bowling'][bowler]['wicket'] += 1
						inns['bowling'][bowler]['balls'] += 1
						inns['batting'][batter]['balls'] += 1
				
						#the below line used to store the fall of wicket status.
						inns['fall_of_wicket'].append(f"{inns['run']}-{inns['wicket']} ({batter}, {over_number})")
						#when batsman out by caught out
						#bowler name is added to status
						if runs.startswith('out Caught by'):
							inns['batting'][batter]['status'] = f"c {runs.split('!!')[0].split('out Caught by', 1)[1].strip()} b {bowler}"
						#when batsman out by lbw
						#bowler name is added to status
						elif runs.startswith('out Lbw!!'):
							inns['batting'][batter]['status'] = f"lbw b {bowler}"
						#when batsman out by bowled
						#bowler name is added to status
						elif runs.startswith('out Bowled!!'):
							inns['batting'][batter]['status'] = f"b {bowler}"
					elif runs == "no run":
						inns['balls']+=1
						inns['batting'][batter]['balls']+=1
						inns['batting'][batter]['status']="not out"
						inns['bowling'][bowler]['balls']+=1

					#when number of runs is 1,2 or other integers, the number of runs scored is added to the total, batsmans and bowlers dictionary
					elif runs.find('run')!= -1:
						for n in range(0,7):
							if runs == str(n)+" run":
								inns['balls'] += 1
								inns['run'] += n
								inns['bowling'][bowler]['run'] += n
								inns['bowling'][bowler]['balls'] += 1
								inns['batting'][batter]['run'] += n
								inns['batting'][batter]['balls'] += 1
								inns['batting'][batter]['status']="not out"
					#when the commentary says four, 4 runs is added

					elif runs == "FOUR":
						
						inns['balls'] += 1
						inns['run'] += 4
						inns['bowling'][bowler]['run'] += 4
						inns['bowling'][bowler]['balls'] += 1
						inns['batting'][batter]['run'] += 4
						inns['batting'][batter]['balls'] += 1
						inns['batting'][batter]['4s'] += 1
						inns['batting'][batter]['status']="not out"
					#when the commentary says six, 6 runs is added to the total runs
					elif runs == "SIX":
						inns['balls'] += 1
						inns['run'] += 6
						inns['bowling'][bowler]['run'] += 6
						inns['bowling'][bowler]['balls'] += 1					
						inns['batting'][batter]['run'] += 6
						inns['batting'][batter]['status']="not out"
						inns['batting'][batter]['balls'] += 1
						inns['batting'][batter]['6s'] += 1

					#finding extras from the commentry
					#when its a bye or legbye, no.of balls increased by 1 

					elif  runs == "leg bye" or runs == "bye" :
						inns['balls'] += 1
						inns['bowling'][bowler]['balls'] += 1
						inns['batting'][batter]['balls'] += 1
						inns['batting'][batter]['status']="not out"
						#when the team got run by bye,it is added to total runs 
						run = info.split(",")[2].strip()
						if(run == 'no run'):
							continue
						#when its a bye four 4 runs is added
						elif(run == 'FOUR'):
							inns['run'] += 4
							if runs == "bye":
								inns['extras']['bye'] += 4
							else:
								inns['extras']['lb'] += 4
						#when its a 1,2,3 or 4 runs by bye it is added to runs
						elif run.find('run')!= -1: 
							for n in range(1,5):
								if(run == str(n)+' run'):
									inns['run'] += n
									if runs == "bye":
										inns['extras']['bye'] += n
									else:
										inns['extras']['lb'] += n
					#when its a no ball 
					elif runs == "no ball":
						inns['run']+=1
						inns['bowling'][bowler]['nb']+=1
						inns['bowling'][bowler]['run']+=1
						inns['extras']['nb'] += 1
						inns['batting'][batter]['status']="not out"
					#when its a wide and 1 runs, 1 is added to total run
					elif runs == "wide":
						inns['run']+=1
						inns['extras']['wide'] += 1
						inns['bowling'][bowler]['run'] += 1
						inns['bowling'][bowler]['wide'] += 1
						inns['batting'][batter]['status']="not out"
					#when its a wide and more than 1 runs, it is added to total run
					elif runs.find('wides')!=-1:
						for n in range(2,6):
							if runs == str(n)+' wides':
								inns['run'] += n
								inns['extras']['wide'] += n
								inns['bowling'][bowler]['run'] += n
								inns['bowling'][bowler]['wide'] += n
						inns['batting'][batter]['status']="not out"
					#When it is 36 balls, the run is added to powerplay run
					if(inns['balls']==36):
						inns['powerplay'] = inns['run']
					#when its end of over, %6 gives zero and if the run is same as initial run, maiden is increased by 1
					if inns['bowling'][bowler]['balls']%6==0:
						if inns['bowling'][bowler]['run']==run_initial:
							inns['bowling'][bowler]['maiden']+=1	
					
				#Printing scores of Pakistan innings
				if innings==1:
					print(f"{'Pakistan innings' : <50}{f'''{inns['run']}-{inns['wicket']} ({over_number} Ov)''' : >95}", file=output)
					print(" ",file=output)
					innings+=1
				#when the loops runs for second time to print Indian innings, this prints
				elif(innings==2):
					print(f"{'Indian innings' : <50}{f'''{inns['run']}-{inns['wicket']} ({over_number} Ov)''' : >95}", file=output)
					print(" ",file=output)
				#printing the heading batter and the headings like R,B,4s,6s etc
				print(f"{'Batter' : <50}{'' : <55}{'R' : ^8}{'B' : ^8}{'4s' : ^8}{'6s' : ^8}{'SR' : ^12}", file=output)
				print(" ",file=output)
				#printing the batting scorecard
				#<means used for left alingning, ^ for centre aligning and > for right alignment
				for batsman, data in inns['batting'].items():
					if data['status'] != '':
						try:
							print(f"{batsman : <50}{data['status'] : <55}{data['run'] : ^8}{data['balls'] : ^8}{data['4s'] : ^8}{data['6s'] : ^8}{round((data['run']/data['balls'])*100, 2) : ^12}", file=output)
						except ZeroDivisionError:
							print("Error while finding strike rate. Zero came in denominator")
				print(" ",file=output)
				#printing the extras of the innings
				print(f"{'Extras' : <50}{f'''{inns['extras']['wide']+inns['extras']['bye']+inns['extras']['nb']+inns['extras']['lb']+inns['extras']['p'] : >44}(b {inns['extras']['bye']},lb {inns['extras']['lb']},w {inns['extras']['wide']},nb {inns['extras']['nb']},p {inns['extras']['p']})''':>82}", file=output)
				print(" ",file=output)
				#printing the Total runs and wickets of the innings
				print(f"{'Total' : <50}{f'''{inns['run']} ({inns['wicket']} wkts, {over_number} Ov)''' : >79}", file=output)
				print(" ",file=output)
				#printing list of people who didnt bat
				if inns['did_not_bat']:
					print(f"{'Did not Bat' : <50}{', '.join(inns['did_not_bat']) : >44}", file=output)
				#printing fall of wicket details
				print("Fall of wicket", file=output)
				print(", ".join(inns['fall_of_wicket']), file=output)
				print(" ",file=output)

				#printing the bowling status
				#the below line prints the heading
				print(f"{'Bowler' : <50}{'' : <45}{'O' : ^7}{'M' : ^7}{'R' : ^7}{'W' : ^7}{'NB' : ^7}{'WD' : ^7}{'ECO' : ^12}", file=output)
				print(" ",file=output)
				#the below ones used for printing the bowling status of the bowlers. The runs spent, maiden over, noballs etc
				for bowler, data in inns['bowling'].items():
					if data['balls']:
						
						total_overs=data['balls']//6
						extra_balls=data['balls']%6
						overall_overs=str(total_overs)+'.'+str(extra_balls)
						try:
							print(f"{bowler : <50}{'' : <45}{overall_overs : ^7}{data['maiden'] : ^7}{data['run'] : ^7}{data['wicket'] : ^7}{data['nb'] : ^7}{data['wide'] : ^7}{round(data['run']/(total_overs+(extra_balls/6)),1) : ^12}", file=output)
						except ZeroDivisionError:
							print("Error while finding economy. The numerator contains zero")				
				print(" ",file=output)
				#printing the runs scored in powerplay
				print(f"{'Powerplays' : <50}{'Overs' : ^55}{'run' : >35}", file=output)
				print(" ",file=output)
				print(f"{'Mandatory' : <50}{'0.1-6' : ^55}{inns['powerplay']: >35}", file=output)
				print(" ",file=output)

	except FileNotFoundError:
		print("File you are trying to open doesnt not exist.")

from platform import python_version
ver = python_version()

if ver == "3.8.10":
	print("Correct Version Installed")
else:
	print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")
try:
	scorecard()	
except:
	print("The function scorecard does not exist")
#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))