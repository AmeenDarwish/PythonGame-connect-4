



def selection_sort(lst):
	for i in range(len(lst)):
		min_index = i
		for j in range(i,len(lst)):
			if lst[j] < lst[min_index]:

				min_index = j

		lst[i], lst[min_index] = lst[min_index], lst[i]
	print(lst)
	return lst


lister_tester = [4,6,8,1,2,6,3,5,10,22,33,44,55,200,7]


def bubble_sort(lst):
	for i in range(len(lst)):
		swap =False
		for j in range(len(lst) - i - 1):
			if lst[j] > lst[j+1]:
				lst[j], lst[j+1] = lst[j+1] , lst[j]
				swap = True
		if not swap:
			break

def merge_sort(lst):
	if (len(lst)==0) or len(lst) == 1:
		return lst
	mid = int(len(lst)/2)
	first_half = merge_sort(lst[0:mid])
	second_half = merge_sort(lst[mid:])
	return merge_two_lists(first_half,second_half)

def merge_two_lists(list1,list2):
	output = []
	list1_i = 0
	list2_i = 0
	while list1_i < len(list1) and list2_i < len(list2):
		if (list1[list1_i]<list2[list2_i]):
			output.append(list1[list1_i])
			list1_i += 1
		else:
			output.append(list2[list2_i])
	if list1_i < len(list1):
		output = output + list1[list1_i:]
	if list2_i < len(list2):
		output = output + list2[list2_i:]
	return output
