__author__ = 'c1n1c0'

key = 'YOUR_KEY';
cseID = 'YOUR_CSE_ID';

import os
clear = lambda: os.system('clear')
import json
from matplotlib import pyplot as plt
import numpy as np
from googleapiclient.discovery import build

from num2words import num2words

percents = np.arange(0, 101, 1)

def main():
	# Build a service object for interacting with the API. Visit
	# the Google APIs Console <http://code.google.com/apis/console>
	# to get an API key for your own application.
	service = build("customsearch", "v1", developerKey=key)

	# Initialize list with results
	results = []
	for percent in percents:
		clear()
		print('\n{} %'.format(percent))
		# Query in format "fifty one percent"
		queryStr = num2words(percent) + ' percent'
		# Query in format "51 percent
		queryNum = str(percent) + ' percent'


		resultQueryStr = service.cse().list(q=queryStr, cx=cseID).execute();
		resultQueryNum = service.cse().list(q=queryNum, cx=cseID).execute();
		#res_dict = json.loads(res)

		results.append( int((resultQueryStr['searchInformation']['totalResults'])) + int((resultQueryNum['searchInformation']['totalResults'])) )

	with plt.xkcd(0.4, 500, 100):

		fig = plt.figure()
		ax1 = fig.add_subplot(1, 1, 1)

		color1 = 'tab:blue'
		color2 = 'tab:red'
		ax1.set_xlabel('Percents')
		ax1.set_ylabel('Occurrence (%)', color=color1)

		ax2 = ax1.twinx()
		ax2.set_ylabel('Occurrence Self Accuracy (%)', color=color2)

		occurrence = np.array(results)
		occurrencePercentage = 100 * occurrence / np.sum(occurrence)

		occurenceSelfAccuracy = np.absolute( occurrencePercentage - percents) / percents

		ax1.bar(percents, occurrencePercentage)
		ax2.plot(percents, occurenceSelfAccuracy, 'r')
		
		ax1.spines['right'].set_color('none')
		ax1.spines['top'].set_color('none')
		ax1.xaxis.set_ticks_position('bottom')
		
		ax1.set_xticks(np.arange(0, 101, 10))
		ax1.set_xlim([-0.5, 100.5])
		
		ax1.set_ylim([0, 8])
		ax1.set_yticks(np.arange(0, 8.5, 0.5))

		ax2.set_ylim([0, 101])
		ax2.set_yticks(np.arange(0, 101, 10))

		plt.title("Percentages of Percents")

		plt.show()


if __name__ == '__main__':
	main()