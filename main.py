'''
Author: Zakariah Siyaji
Phone: 708-890-2864
Email: z.siyaji@gmail.com
'''
#!/usr/bin/python3
import os
import sys
import json

def readRequestJSON(inputFilename=None):
    
    """
    readRequestJSON reads the input file and loads the json object
    """
    
    #checking if file exists, then read the json file
    if os.path.exists(inputFilename):

        #opening file for reading
        with open(inputFilename) as jsonFile:

            #loading the json file
            dataObj = json.load(jsonFile)


        jsonFile.close()

        #return loaded object
        return dataObj

    else:
        print(f'{inputFilename} doesn\'t exist!')

        #return None if not found
        return None


def findEntryInList(updatedList,sID):
    """
    findEntryInList checks all entries in the list to see if it
    found the sID to return the entry. Otherwise, create a new dictionary and update the entry
    as subject_id with sID and return
    """

    #reading all entry in list, and finding sID in each entry
    for entries in updatedList:

        #if found, then return that dictionary
        if entries["subject_id"] == sID :
            return entries


    #if not found, then create new dictionary and update sID with subject_id
    #and return the dictionary
    newDict = dict()
    newDict["subject_id"] = sID
    newDict["body_weight"] = None
    newDict["race"] = None
    return newDict

def processJSON(dataObj):

    #creating a new list
    updatedList = list()

    #checking if json object has data_points key
    if 'data_points' in dataObj:

        #if found, then save entries to entryValues variable for processing
        entryValues = dataObj['data_points']

        #process each row entry  in the list
        for rows in entryValues:

            # first checking if rows has subject_id, then process it
            if "subject_id" in rows.keys():
                sID = rows["subject_id"]

                #finding the dictionary which has sID
                newDict = findEntryInList(updatedList,sID)

                #if data_point_type is race, then update in the entry
                if "data_point_type" in rows.keys() and rows["data_point_type"] == "race":
                    newDict["race"] =  rows["value"]

                #else data_point_type is body_weight, then update in the entry by converting it according to units type
                elif "data_point_type" in rows.keys() and rows["data_point_type"] == "body_weight":
                    #if lb, then multiply with 0.4535147
                    if rows["units"] == "lb":
                        newDict["body_weight"] =  "{:0.5f}" .format(int(rows["value"]) * 0.4535147)

                    #if ounces, then multiply with 0.0283495
                    elif rows["units"] == "oz":
                        newDict["body_weight"] =  "{:0.5f}" .format(int(rows["value"]) * 0.0283495)

                    #if kilograms, no conversion required
                    else:
                        newDict["body_weight"] = rows["value"]

                #add new dictionary to list
                updatedList.append(newDict)

    #creating new JSON object and add the list to subjects key
    newObj = {}

    #adding the subjects key into object and value as empty list
    newObj["subjects"] = updatedList

    return newObj


def writeResponseJSON(newObj,outputFilename):
    if os.path.exists(outputFilename):
        print(f'{outputFilename} already exists, overwriting!')

    with open(outputFilename,'w') as f:
        json.dump(newObj,f)
    f.close()


def main():

    #specifying the input filename
    inputFilename = 'request.json'

    #specifying the output filename
    outputFilename = 'response.json'

    #reading the json object from file
    dataObj = readRequestJSON(inputFilename)

    #if not found, then exit
    if dataObj == None:
        print("Exiting the algorithm!")

        sys.exit(-1)

    else:
        #processing the json object
        newObj = processJSON(dataObj)

        #display the new build json object
        print(json.dumps(newObj,indent=3))

        #write the processed JSON object to file
        writeResponseJSON(newObj,outputFilename)

if __name__ == "__main__":
    main()
