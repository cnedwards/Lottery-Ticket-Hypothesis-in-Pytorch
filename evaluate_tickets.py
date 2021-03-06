#Used to automate the process of processing ticket results

import os
import argparse
import sys
import utils
import pickle
import numpy as np

if __name__ == "__main__":
    # Arguement Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", default="False", type=str, help="Recreate rates/accuracies True | False")
    parser.add_argument("--output_folder", default=None, type=str, help="Output destination")
    parser.add_argument("--dat_percent", default=None, type=str, help="Percent coverage version")

    args = parser.parse_args()

    #Extract and create result files if specified
    if args.generate == "True":
        if args.dat_percent == None:
            print("Please specify file version to evaluate.")
            exit()

        ticket_folders="tickets"
        for dataSet in os.listdir(ticket_folders):

            if "_" in dataSet: #Skip over extra data sets
                continue

            result_path = "eval_tickets/" + dataSet + "/"
            for f in os.listdir(ticket_folders+"/"+dataSet+"/"):
                ticket_path = ticket_folders + "/" + dataSet + "/" + f

                tmpData = dataSet 
                if tmpData== "fmnist":
                    tmpData = "fashionmnist"

                cmd = str("python exp_fit_example.py --prune_type=lt --arch_type=fc1 --dataset="+tmpData+" --ticket_folders="\
                    + ticket_path + " --output_folder="+result_path+f+" --dat_percent="+args.dat_percent)
                print(cmd)
                os.system(cmd)

    #Parse through results and create dictionary
    results = {}
    root = "eval_tickets"
    for dataSet in os.listdir(root):
        results[dataSet] = {}
        for ticket in os.listdir(f"{root}/{dataSet}"):

            if ticket[1:] not in results[dataSet].keys():
                results[dataSet][ticket[1:]] = {}

            results[dataSet][ticket[1:]][ticket] = {}

            with open(f"{root}/{dataSet}/{ticket}/output.txt") as f:
                tmp = f.read().rstrip()
                tmp = tmp.replace('(', '')
                tmp = tmp.replace(')', '')
                results[dataSet][ticket[1:]][ticket] = tmp

    if args.output_folder != None:
        utils.checkdir(f"{os.getcwd()}/{args.output_folder}/")
        sys.stdout = open(f"{os.getcwd()}/{args.output_folder}/output.txt", 'w') #Store output in a file instead
        pickle.dump(results, open(f"{os.getcwd()}/{args.output_folder}/results.pickle", 'wb'))

    #Output results
    for dataSet in results.keys():
        print(f"{dataSet}")
        for dataPercent in results[dataSet].keys():
            print(f"\t{dataPercent}")
            for ticket in results[dataSet][dataPercent].keys():
                print(f"\t\t{ticket}")
                print(f"\t\t\t{results[dataSet][dataPercent][ticket]}")
                
            print(f"\tAverage")
            c = []
            acc = []
            for v in results[dataSet][dataPercent].values():
                ctmp, acctmp = v.split(', ')
                c.append(float(ctmp))
                acc.append(float(acctmp))
            avg_c = np.mean(c)
            avg_acc = np.mean(acc)
            out = ", ".join([str(avg_c),str(avg_acc)])
            print(f"\t\t{out}")
        