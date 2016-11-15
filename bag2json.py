'''
This script saves each topic in a bagfile as a JSON file.

Accepts a filename as a required argument.

Usage (for one bag file):
	python bag2json.py filename.bag

Derived from Nick Speal's bag2csv code (www.speal.ca).

'''

import rosbag, sys, json
import time
import string
import os # for file management, to make a directory
import shutil # for file management, to copy files

global count

def process_input_args():
    # Verify correct input arguments: 1 or 2
    if (len(sys.argv) != 2):
        print "invalid number of arguments:   " + str(len(sys.argv))
        print "should be 2: 'bag2json.py' and 'bagName.bag'"
        sys.exit(1)
    else:
        listOfBagFiles = [sys.argv[1]]

    return listOfBagFiles


def process_bagfile(bagFile, num_bag_files):
    global count

    count += 1
    print "Reading file " + str(count) + " of " + str(num_bag_files) + ": " + bagFile
    
    # Access bag
    bag = rosbag.Bag(bagFile)
    bagContents = bag.read_messages()
    bagName = bag.filename

    # Create a new directory
    folder = string.rstrip(bagName, ".bag") + '_json'
    try:
        os.makedirs(folder)
    except:
        # Do nothing if it already exists
        pass
    # shutil.copyfile(bagName, folder + '/' + bagName)

    # Get list of topics from the bag
    listOfTopics = []
    for topic, msg, t in bagContents:
        if topic not in listOfTopics:
            listOfTopics.append(topic)

    for topicName in listOfTopics:
        save_bag_topic_as_json(bag, folder, topicName)

    bag.close()    

def get_indent_level(string):
    """Count number of leading indentations (double spaces) in a stringself.
    """
    return (len(string)- len(string.lstrip()) ) / 2

def msg_lines_to_dictionary(msg_list):
    # Parse line-by-line, using leading indentation to indicate
    # hierarchical organization
    
    # All of lines will be put into a single, hierarchical dictionary
    main_line_dict = {}

    # First, go through and make a mini-dictionary for each line
    mini_dict_list = []
    for line in msg_list:
        indent_level = get_indent_level(line)
        split_pair = line.split(':')
        mini_dict = {}

        mini_dict['name'] = split_pair[0].strip()
        if len(split_pair) > 1:
            mini_dict['value'] = split_pair[1].strip()
        else:
            value = ''
        mini_dict['level'] = indent_level
        mini_dict_list.append(mini_dict)

    # Now, get a JSON-style hierarchical dictionary version of the text
    json_dict = ttree_to_json_dict(mini_dict_list)

    return json_dict

# from http://stackoverflow.com/questions/17858404/creating-a-tree-deeply-nested-dict-from-an-indented-text-file-in-python
def ttree_to_json_dict(ttree,level=0):
    result = {}
    for i in range(0,len(ttree)):
        cn = ttree[i]
        try:
            nn  = ttree[i+1]
        except:
            nn = {'level':-1}

        # Edge cases
        if cn['level']>level:
            continue
        if cn['level']<level:
            return result

        # Recursion
        if nn['level']==level:
            dict_insert_or_append(result,cn['name'],cn['value'])
        elif nn['level']>level:
            rr = ttree_to_json_dict(ttree[i+1:], level=nn['level'])
            dict_insert_or_append(result,cn['name'],rr)
        else:
            dict_insert_or_append(result,cn['name'],cn['value'])
            return result
    return result

# from http://stackoverflow.com/questions/17858404/creating-a-tree-deeply-nested-dict-from-an-indented-text-file-in-python
def dict_insert_or_append(adict,key,val):
    """Insert a value in dict at key if one does not exist
    Otherwise, convert value to list and append
    """
    if key in adict:
        if type(adict[key]) != list:
            adict[key] = [adict[key]]
        adict[key].append(val)
    else:
        adict[key] = val


def save_bag_topic_as_json(bag, folder, topicName):
    # Create a new JSON file for each topic
    filename = folder + '/' + string.replace(topicName, '/', '_slash_') + '.json'
    print "Processing data for " + filename
    with open(filename, 'w+') as jsonfile:
        # filewriter = csv.writer(csvfile, delimiter = ',', lineterminator='\n')
        firstIteration = True   #allows header row
        msg_dictionaries = []
        for subtopic, msg, t in bag.read_messages(topicName):   # for each instant in time that has data for topicName
            # Parse data from this instant, which is of the form of multiple lines of "Name: value\n"
            #   - put it in the form of a list of 2-element lists
            msgString = str(msg)
            msgLines = string.split(msgString, '\n')
            
            msg_dictionary = msg_lines_to_dictionary(msgLines)
            msg_dictionaries.append(msg_dictionary)


        json_dict = {}
        json_dict['messages'] = msg_dictionaries

        json.dump(json_dict, jsonfile)

def main():
    global count

    count = 0
    
    listOfBagFiles = process_input_args()

    for bagFile in listOfBagFiles:
        process_bagfile(bagFile, len(listOfBagFiles))

    print "Done reading all " + str(len(listOfBagFiles)) + " bag file(s)."

if __name__ == '__main__':
    main()