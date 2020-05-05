
import os
import argparse
import sys
import utils
import pickle
import numpy as np

#mnist_ticket_path = 'tickets/mnist/'
#fmnist_ticket_path = 'tickets/fmnist/'
#mnist_tickets = os.listdir(mnist_ticket_path)[0:4]
#fmnist_tickets = os.listdir(fmnist_ticket_path)[0:4]

 #python exp_fit_example.py --prune_type=lt --arch_type=fc1 --dataset=mnist --ticket_folders=tickets/mnist/A --output_folder=fitTest

if __name__ == "__main__":
    # Arguement Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", default="False", type=str, help="Recreate rates/accuracies True | False")
    parser.add_argument("--output_folder", default=None, type=str, help="Output destination")
    parser.add_argument("--dat_percent", default=None, type=str, help="Output destination")

    args = parser.parse_args()


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

    results = {}
    root = "eval_tickets"
    for dataSet in os.listdir(root):
        results[dataSet] = {}
        for ticket in os.listdir(f"{root}/{dataSet}"):
            results[dataSet][ticket] = {}
            with open(f"{root}/{dataSet}/{ticket}/output.txt") as f:
                tmp = f.read().rstrip()
                tmp = tmp.replace('(', '')
                tmp = tmp.replace(')', '')
                results[dataSet][ticket] = tmp
#                    results[dataSet][len(ticket)][ticket] = f.read().rstrip()

    if args.output_folder != None:
        utils.checkdir(f"{os.getcwd()}/{args.output_folder}/")
        sys.stdout = open(f"{os.getcwd()}/{args.output_folder}/output.txt", 'w') #Store output in a file instead
        pickle.dump(results, open(f"{os.getcwd()}/{args.output_folder}/results.pickle", 'wb'))

    for dataSet in results.keys():
        print(f"{dataSet}")
        for ticket in results[dataSet].keys():
            print(f"\t{ticket}")
            print(f"\t\t{results[dataSet][ticket]}")
            #for ticket in results[dataSet][ticketLength]:
            #    print(f"\t\t{ticket}")
                #print(f"\t\t\t\t{results[dataSet][ticketLength][ticket]}")
                
        print(f"\tAverage")
        c = []
        acc = []
        for v in results[dataSet].values():
            ctmp, acctmp = v.split(', ')
            c.append(float(ctmp))
            acc.append(float(acctmp))
        avg_c = np.mean(c)
        avg_acc = np.mean(acc)
        out = ", ".join([str(avg_c),str(avg_acc)])
        print(f"\t\t{out}")
        