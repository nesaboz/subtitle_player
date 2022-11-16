import datetime
import tkinter as tk
import pause

###### Inputs #######

OFFSET_SECONDS = 300
SRT_FILE = 'TopGunMaverick2022italian.srt'

#####################
groups = []
temp = []
with open(SRT_FILE, 'r') as f:
	lines = f.readlines()

for line in lines:
	if line != '\n':
		temp.append(line)
	else:
		groups.append(temp)
		temp = []

root = tk.Tk()

T = tk.Text(root, font=("Arial", 80, "normal"), insertofftime=0)
T.pack()


def find_start_end(string):
	start, end = string.split('-->')

	def conv(x):
		x = datetime.datetime.strptime(x.strip(), '%H:%M:%S,%f')
		return datetime.timedelta(hours=x.hour, minutes=x.minute, seconds=x.second, microseconds=x.microsecond)
	return conv(start), conv(end)


offset = datetime.timedelta(seconds=OFFSET_SECONDS)
started_subtitles = datetime.datetime.now() - offset


for group in groups:
	index = group[0]
	start, end = find_start_end(group[1])

	text = "".join(group[2:]).replace(r'{\an8}', '').replace(r'<i>', '"').replace(r'</i>', '"')
	pause.until(started_subtitles + start)

	T.insert('1.0', "".join(text))

	T.update_idletasks()
	T.update()
	pause.until(started_subtitles + end)
	T.delete('1.0', tk.END)
