# Importing Libraries
import argparse
import copy
import os
import sys
import numpy as np
from tqdm import tqdm
import torchvision
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import os
import seaborn as sns
import pickle

# Custom Libraries
import utils

# Plotting Style
sns.set_style('darkgrid')

from scipy.optimize import curve_fit
    
# Main
def main(args, ITE=0):


    test = args.ticket_folders#args.ticket_folders.split(',')
    
    '''
    # Pruning
    # NOTE First Pruning Iteration is of No Compression
    bestacc = 0.0
    best_accuracy = 0
    ITERATION = 1#args.prune_iterations     #This was set to 1 here because we aren't doing any pruning just merging
    comp = np.zeros(ITERATION,float)
    bestacc = np.zeros(ITERATION,float)
    step = 0
    all_loss = np.zeros(args.end_iter,float)
    all_accuracy = np.zeros(args.end_iter,float)
    
    all_loss_plot = [np.zeros(args.end_iter,float)]
    all_accuracy_plot = [np.zeros(args.end_iter,float)]



        # Plotting Loss (Training), Accuracy (Testing), Iteration Curve
        #NOTE Loss is computed for every iteration while Accuracy is computed only for every {args.valid_freq} iterations. Therefore Accuracy saved is constant during the uncomputed iterations.
        #NOTE Normalized the accuracy to [0,100] for ease of plotting.
        plt.plot(np.arange(1,(args.end_iter)+1), 100*(all_loss - np.min(all_loss))/np.ptp(all_loss).astype(float), c="blue", label="Loss") 
        plt.plot(np.arange(1,(args.end_iter)+1), all_accuracy, c="red", label="Accuracy") 
        plt.title(f"Loss Vs Accuracy Vs Iterations ({args.dataset},{args.arch_type})") 
        plt.xlabel("Iterations") 
        plt.ylabel("Loss and Accuracy") 
        plt.legend() 
        plt.grid(color="gray") 
        ax = plt.gca()
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        utils.checkdir(f"{os.getcwd()}/{args.output_folder}/plots/lt/{args.arch_type}/{args.dataset}/")
        plt.savefig(f"{os.getcwd()}/{args.output_folder}/plots/lt/{args.arch_type}/{args.dataset}/{args.prune_type}_LossVsAccuracy_{comp1}.png", dpi=1200) 
        plt.close()

        # Dump Plot values
        utils.checkdir(f"{os.getcwd()}/{args.output_folder}/dumps/lt/{args.arch_type}/{args.dataset}/")
        all_loss.dump(f"{os.getcwd()}/{args.output_folder}/dumps/lt/{args.arch_type}/{args.dataset}/{args.prune_type}_all_loss_{comp1}.dat")
        all_accuracy.dump(f"{os.getcwd()}/{args.output_folder}/dumps/lt/{args.arch_type}/{args.dataset}/{args.prune_type}_all_accuracy_{comp1}.dat")
        
        
        # Making variables into 0
        best_accuracy = 0
        all_loss = np.zeros(args.end_iter,float)
        all_accuracy = np.zeros(args.end_iter,float)
        all_loss_plot.append(np.zeros(args.end_iter,float))
        all_accuracy_plot.append(np.zeros(args.end_iter,float))

    # Dumping Values for Plotting
    utils.checkdir(f"{os.getcwd()}/{args.output_folder}/dumps/lt/{args.arch_type}/{args.dataset}/")
    comp.dump(f"{os.getcwd()}/{args.output_folder}/dumps/lt/{args.arch_type}/{args.dataset}/{args.prune_type}_compression.dat")
    bestacc.dump(f"{os.getcwd()}/{args.output_folder}/dumps/lt/{args.arch_type}/{args.dataset}/{args.prune_type}_bestaccuracy.dat")
    '''

    #with open('lt_all_accuracy_11.1.dat', 'rb') as f:
    acc = np.load(f"{os.getcwd()}/{test}/dumps/lt/{args.arch_type}/{args.dataset}/{args.prune_type}_all_accuracy_11.1.dat", allow_pickle=True)

    x = np.arange(acc.size)
    
    print(x,acc)
    
    #Fit and plot from: https://stackoverflow.com/questions/21420792/exponential-curve-fitting-in-scipy/21421137
    
    def fit(x, acc):
        def func(x, a, b, c, d):
            return a*np.exp(-c*(x-b))+d

        popt, pcov = curve_fit(func, x, acc, [-1,1,4,95])
        print(popt)

        exp_rate = popt[2]
        print("Rate: ", exp_rate)

        plt.plot(x,acc)
        plt.plot(x,func(x,*popt))
        #plt.show()
        
        if '/' in test:
            utils.checkdir(f"{os.getcwd()}/{args.output_folder}/{test.rsplit('/',1)[0]}")
        else:
            utils.checkdir(f"{os.getcwd()}/{args.output_folder}")
        plt.savefig(f"{os.getcwd()}/{args.output_folder}/{test}.png")

        return exp_rate
    
    print(max(acc))
    return fit(x,acc), max(acc)#exp. rate, best acc.

    # Plotting
    '''
    a = np.arange(args.prune_iterations)
    plt.plot(a, bestacc, c="blue", label="Winning tickets") 
    plt.title(f"Test Accuracy vs Unpruned Weights Percentage ({args.dataset},{args.arch_type})") 
    plt.xlabel("Unpruned Weights Percentage") 
    plt.ylabel("test accuracy") 
    plt.xticks(a, comp, rotation ="vertical") 
    plt.ylim(0,100)
    plt.legend() 
    plt.grid(color="gray")
    plt.tight_layout()
    utils.checkdir(f"{os.getcwd()}/{args.run_folder}/plots/lt/{args.arch_type}/{args.dataset}/")
    plt.savefig(f"{os.getcwd()}/{args.run_folder}/plots/lt/{args.arch_type}/{args.dataset}/{args.prune_type}_AccuracyVsWeights.png", dpi=1200) 
    plt.close()      
    '''    

    ''' Might add overlayed plots later...
    plt.figure()
    for i in 
    plt.plot(a, bestacc, c="blue", label="Winning tickets") 
    plt.title(f"Test Accuracy vs Unpruned Weights Percentage ({args.dataset},{args.arch_type})") 
    plt.tight_layout()
    plt.xlabel("Unpruned Weights Percentage") 
    plt.ylabel("test accuracy") 
    '''
    
   

if __name__=="__main__":
       
    
    # Arguement Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--prune_type", default="lt", type=str, help="lt | reinit")
    parser.add_argument("--dataset", default="mnist", type=str, help="mnist | cifar10 | fashionmnist | cifar100")
    parser.add_argument("--arch_type", default="fc1", type=str, help="fc1 | lenet5 | alexnet | vgg16 | resnet18 | densenet121")
    parser.add_argument("--ticket_folders", default="A0", type=str, help="Set the folders to load tickets from. Seperate with commas.")
    parser.add_argument("--output_folder", default="merge_result", type=str, help="Set the folder to store results in.")

    
    args = parser.parse_args()

    

    utils.checkdir(f"{os.getcwd()}/{args.output_folder}/")
    sys.stdout = open(f"{os.getcwd()}/{args.output_folder}/output.txt", 'w') #Store output in a file instead

    # Looping Entire process
    #for i in range(0, 5):
    main(args, ITE=1)






