
import os
import argparse
import sys
import utils
import pickle

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

    args = parser.parse_args()

    if args.generate == "True":
        ticket_folders="test_results"
        for d in os.listdir(ticket_folders):
            #print(d)
            for v in os.listdir(ticket_folders+"/"+d):
                #print("\t",v)
                result_path = "eval_results/" + d + "/" + v + "/"
                for f in os.listdir(ticket_folders+"/"+d+"/"+v):
                    ticket_path = ticket_folders + "/" + d + "/" + v + "/" + f
                    cmd = str("python exp_fit_example.py --prune_type=lt --arch_type=fc1 --dataset="+v+" --ticket_folders="\
                        + ticket_path + " --output_folder="+result_path+f)
                    print(cmd)
                    os.system(cmd)

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
#                    results[expType][dataSet][len(ticket)][ticket] = f.read().rstrip()

    if args.output_folder != None:
        utils.checkdir(f"{os.getcwd()}/{args.output_folder}/")
        sys.stdout = open(f"{os.getcwd()}/{args.output_folder}/output.txt", 'w') #Store output in a file instead
        pickle.dump(results, open(f"{os.getcwd()}/{args.output_folder}/results.pickle", 'wb'))

    for expType in results.keys():
        print(expType)
        for dataSet in results[expType].keys():
            print(f"\t{dataSet}")
            for ticketLength in results[expType][dataSet].keys():
                print(f"\t\t{ticketLength}")
                for ticket in results[expType][dataSet][ticketLength].keys():
                    print(f"\t\t\t{ticket}")
                    print(f"\t\t\t\t{results[expType][dataSet][ticketLength][ticket]}")