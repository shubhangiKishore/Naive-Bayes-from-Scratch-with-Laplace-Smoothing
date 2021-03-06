'''
Project : naive_bayes_classifier, A python program to make a naive bayes classifier with laplace smoothing.
'''


#importing libaries 
import pandas as pd 
import numpy as np 



# function to calculate probabilities based on training data 
# input parameters are the features ('Outlook','Temp.','Humidity','Windy','Play')
def calc_prob(x1,x2,x3,x4, p_play):

	# conditional probability with laplace smoothing, probability of values given tennis is played
	play_x1 = df['freq_Outlook'][x1]['p_yes']
	play_x2 = df['freq_Temp.'][x2]['p_yes']
	play_x3 = df['freq_Humidity'][x3]['p_yes']
	play_x4 = df['freq_Windy'][x4]['p_yes']

	# probabilities of occurences of individual event 
	p_x1 = df['freq_Outlook'][x1]['p']
	p_x2 = df['freq_Temp.'][x2]['p']
	p_x3 = df['freq_Humidity'][x3]['p']
	p_x4  = df['freq_Windy'][x4]['p']

	p_intersection = float(p_x1 * p_x2 * p_x3 * p_x4)
	prob_numerator = float(play_x1 * play_x2 * play_x3 * play_x4 * p_play)

	return float(prob_numerator/p_intersection)



# function to assign class(Play/NO play) depending on the probability 
def assign_class(x):
	if x > 0.5:
		return 'Play_Tennis'
	return 'No_Tennis'

# function to output result by testing test cases stored in test.csv file 

def run_tests(p_play):
	test_df = pd.read_csv('test.csv', sep =  ',')
	test_set =  np.array(test_df)
	j = 1
	for test in test_set:
	    x1 = test[0]
	    x2 = test[1]
	    x3 = test[2]
	    x4 = test[3]
	    result = assign_class(calc_prob(x1,x2,x3,x4,p_play))
	    print "\n%d - Test case" %j
	    j = j+1
	    for i in test:
	    	print i
	    print "\nTo play or not to play: " + result




df = {}
#Read CSV file to a dataFrame 
tennis_df = pd.read_csv('Q2-tennis.csv', sep =  ',')
num_rows = len(tennis_df.index)


# Calculating the probability when play is yes 

play_df = tennis_df[tennis_df['Play']=='yes']
count_play_yes = play_df.count()
play_yes =  count_play_yes[0]
p_play = float (play_yes)/float (num_rows)


# Listing the factors that determine playing tennis 

features = list(tennis_df.columns.values)
features.remove('Play');

#iterating over features ('Outlook','Temp.','Humidity','Windy','Play')
for i in features :

	#listing unique values of the feature 
	feature_values = tennis_df[i].unique()
	num_features =  len(feature_values)
	#creating dataframes for each feature to store frequencies of different values it can take 
	df["freq_{}".format(i)] = pd.DataFrame(columns = feature_values, index = ['yes','no','total','p_yes','p_no','p'])


	# temporary dataframe to calculate number of occurences 
	temp_df = tennis_df[tennis_df['Play']=='yes']
	counter = temp_df.groupby([i]).size()
	valuesDict = {k:counter.ix[k] for k in counter.keys()}
	
	#updating values in frequency dataframe for ith feature 
	for val in df["freq_{}".format(i)].columns:
		count_yes = valuesDict[val]
		df["freq_{}".format(i)][val]['yes'] = count_yes 

	# finding total occurences of distinct values in features 
	counter2 = tennis_df.groupby([i]).size()
	valuesDict2 = {k2:counter2.ix[k2] for k2 in counter2.keys()}
	
	#updating values in frequency dataframe for ith feature
	for val in df["freq_{}".format(i)].columns:

		count_tot = valuesDict2[val]
		count_yes = df["freq_{}".format(i)][val]['yes']
		
		df["freq_{}".format(i)][val]['total'] = count_tot
		df["freq_{}".format(i)][val]['no'] = count_tot - count_yes
		df["freq_{}".format(i)][val]['p'] = float (count_tot)/ float(num_rows)
		
		# using laplace smoothing for conditional probability, alpha = 1 
		df["freq_{}".format(i)][val]['p_yes'] = float ((count_yes)+1)/ float((count_tot)*(num_features))
		df["freq_{}".format(i)][val]['p_no'] = float ((count_tot-count_yes)+1)/ float((count_tot)* (num_features))



# To view the frequency tables, Uncomment the line below 
#print df

# To run a sample case, uncomment the line below 
#print assign_class(calc_prob('sunny','hot','high','true ',p_play))
# function to test test cases and output the class ('play_tennis /no_tennis')
run_tests(p_play)

