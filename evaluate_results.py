#Used to automate the process of processing merged ticket results

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

    args = parser.parse_args()

    #Generate intermediate output files if needed
    if args.generate == "True":
        ticket_folders="test_results"
        for d in os.listdir(ticket_folders):
            for v in os.listdir(ticket_folders+"/"+d):
                result_path = "eval_results/" + d + "/" + v + "/"
                for f in os.listdir(ticket_folders+"/"+d+"/"+v):
                    ticket_path = ticket_folders + "/" + d + "/" + v + "/" + f
                    cmd = str("python exp_fit_example.py --prune_type=lt --arch_type=fc1 --dataset="+v+" --ticket_folders="\
                        + ticket_path + " --output_folder="+result_path+f)
                    print(cmd)
                    os.system(cmd)

    #Parse intermediate output files
    results = {}
    root = "eval_results"
    for expType in os.listdir(root):
        results[expType] = {}
        for dataSet in os.listdir(f"{root}/{expType}"):
            results[expType][dataSet] = {}
            for ticket in os.listdir(f"{root}/{expType}/{dataSet}"):

                if (len(ticket)) not in results[expType][dataSet].keys():
                    results[expType][dataSet][len(ticket)] = {}

                results[expType][dataSet][len(ticket)][ticket] = {}
                with open(f"{root}/{expType}/{dataSet}/{ticket}/output.txt") as f:
                    tmp = f.read().rstrip()
                    tmp = tmp.replace('(', '')
                    tmp = tmp.replace(')', '')
                    results[expType][dataSet][len(ticket)][ticket] = tmp

    #Output results
    if args.output_folder != None:
        utils.checkdir(f"{os.getcwd()}/{args.output_folder}/")
        sys.stdout = open(f"{os.getcwd()}/{args.output_folder}/output.txt", 'w') #Store output in a file instead
        pickle.dump(results, open(f"{os.getcwd()}/{args.output_folder}/results.pickle", 'wb'))

    for expType in results.keys():
        print(expType)
        for dataSet in results[expType].keys():
            print(f"\t{dataSet}")
            for ticketLength in results[expType][dataSet].keys():
                print(f"\t\t Ticket Length {ticketLength} : Trials {len(results[expType][dataSet][ticketLength].keys())}")
                for ticket in results[expType][dataSet][ticketLength].keys():
                    print(f"\t\t\t{ticket}")
                    print(f"\t\t\t\t{results[expType][dataSet][ticketLength][ticket]}")
                    
                print(f"\t\t\tAverage")
                c = []
                acc = []
                for v in results[expType][dataSet][ticketLength].values():
                    ctmp, acctmp = v.split(', ')
                    c.append(float(ctmp))
                    acc.append(float(acctmp))
                avg_c = np.mean(c)
                avg_acc = np.mean(acc)
                out = ", ".join([str(avg_c),str(avg_acc)])
                print(f"\t\t\t\t{out}")
                    