
import os

#mnist_ticket_path = 'tickets/mnist/'
#fmnist_ticket_path = 'tickets/fmnist/'
#mnist_tickets = os.listdir(mnist_ticket_path)[0:4]
#fmnist_tickets = os.listdir(fmnist_ticket_path)[0:4]

 #python exp_fit_example.py --prune_type=lt --arch_type=fc1 --dataset=mnist --ticket_folders=tickets/mnist/A --output_folder=fitTest

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
            
            #print(result_path+ f)

"""
program = "python exp_fit_example.py --prune_type=lt --arch_type=fc1 --dataset="
param2 = " --ticket_folders="

#Merge=======================================
#----------MNIST----------
dataset = "mnist"
result_path = "test_results/merge/" + dataset + "/"

def check_path(path, fileName):
    if (os.path.isdir(path + fileName)): #check if we already ran this merge
        print("Skipping: ", fileName)
        return True 


p2 = permutations(mnist_tickets, 2)
for p in list(p2):
    if check_path(result_path, p[0] + p[1]):
        continue

    cmd = str(program + dataset + param2 + mnist_ticket_path + p[0] + "," + mnist_ticket_path + p[1] + " --output_folder=" + result_path + p[0] + p[1])
    os.system(cmd)
    print(cmd)


p3 = permutations(mnist_tickets, 3)
for p in list(p3):
    if check_path(result_path, p[0] + p[1] + p[2]):
        continue
    
    cmd = str(program + dataset + param2 + mnist_ticket_path + p[0] \
        + "," + mnist_ticket_path + p[1] \
        + "," + mnist_ticket_path + p[2] + " --output_folder=" + result_path + p[0] + p[1] + p[2])
    os.system(cmd)
    print(cmd)

p4 = [('A', 'B', 'C', 'D'), ('D','C','B','A')]
for p in list(p4):
    if check_path(result_path, p[0] + p[1] + p[2] + p[3]):
        continue

    cmd = str(program + dataset + param2 + mnist_ticket_path + p[0] \
        + "," + mnist_ticket_path + p[1] \
        + "," + mnist_ticket_path + p[2] \
        + "," + mnist_ticket_path + p[3] + " --output_folder=" + result_path + p[0] + p[1] + p[2] + p[3])
    os.system(cmd)
    print(cmd)


#FMNIST
dataset = "fashionmnist"
result_path = "test_results/merge/" + dataset + "/"

p2 = permutations(fmnist_tickets, 2)
for p in list(p2):
    if check_path(result_path, p[0] + p[1]):
        continue
    cmd = str(program + dataset + param2 + fmnist_ticket_path + p[0] + "," + fmnist_ticket_path + p[1] + " --output_folder=" + result_path + p[0] + p[1])
    print(cmd)
    os.system(cmd)

p3 = permutations(fmnist_tickets, 3)
for p in list(p3):
    if check_path(result_path, p[0] + p[1] + p[2]):
        continue
    cmd = str(program + dataset + param2 + fmnist_ticket_path + p[0] \
        + "," + fmnist_ticket_path + p[1] \
        + "," + fmnist_ticket_path + p[2] + " --output_folder=" + result_path + p[0] + p[1] + p[2])
    print(cmd)
    os.system(cmd)

p4 = [('A', 'B', 'C', 'D'), ('D','C','B','A')]
for p in list(p4):
    if check_path(result_path, p[0] + p[1] + p[2] + p[3]):
        continue
    cmd = str(program + dataset + param2 + fmnist_ticket_path + p[0] \
        + "," + fmnist_ticket_path + p[1] \
        + "," + fmnist_ticket_path + p[2] \
        + "," + fmnist_ticket_path + p[3] + " --output_folder=" + result_path + p[0] + p[1] + p[2] + p[3])
    print(cmd)
    os.system(cmd)


#Average=======================================
program = "python merge_tickets_avg.py --prune_type=lt --arch_type=fc1 --dataset="

#----------MNIST----------
dataset = "mnist"
result_path = "test_results/average/" + dataset + "/"

p2 = combinations(mnist_tickets, 2)
for p in list(p2):
    if check_path(result_path, p[0] + p[1]):
        continue
    cmd = str(program + dataset + param2 + mnist_ticket_path + p[0] + "," + mnist_ticket_path + p[1] + " --output_folder=" + result_path + p[0] + p[1])
    print(cmd)
    os.system(cmd)

p3 = combinations(mnist_tickets, 3)
for p in list(p3):
    if check_path(result_path, p[0] + p[1] + p[2]):
        continue
    cmd = str(program + dataset + param2 + mnist_ticket_path + p[0] \
        + "," + mnist_ticket_path + p[1] \
        + "," + mnist_ticket_path + p[2] + " --output_folder=" + result_path + p[0] + p[1] + p[2])
    print(cmd)
    os.system(cmd)

p = ('A', 'B', 'C', 'D')
if not check_path(result_path, p[0] + p[1] + p[2] + p[3]):
    cmd = str(program + dataset + param2 + mnist_ticket_path + p[0] \
        + "," + mnist_ticket_path + p[1] \
        + "," + mnist_ticket_path + p[2] \
        + "," + mnist_ticket_path + p[3] + " --output_folder=" + result_path + p[0] + p[1] + p[2] + p[3])
    print(cmd)
    os.system(cmd)

#----------FMNIST----------
dataset = "fashionmnist"
result_path = "test_results/average/" + dataset + "/"

p2 = combinations(fmnist_tickets, 2)
for p in list(p2):
    if check_path(result_path, p[0] + p[1]):
        continue
    cmd = str(program + dataset + param2 + fmnist_ticket_path + p[0] + "," + fmnist_ticket_path + p[1] + " --output_folder=" + result_path + p[0] + p[1])
    print(cmd)
    os.system(cmd)

p3 = combinations(fmnist_tickets, 3)
for p in list(p3):
    if check_path(result_path, p[0] + p[1] + p[2]):
        continue
    cmd = str(program + dataset + param2 + fmnist_ticket_path + p[0] \
        + "," + fmnist_ticket_path + p[1] \
        + "," + fmnist_ticket_path + p[2] + " --output_folder=" + result_path + p[0] + p[1] + p[2])
    print(cmd)
    os.system(cmd)

p = ('A', 'B', 'C', 'D')
if not check_path(result_path, p[0] + p[1] + p[2] + p[3]):
    cmd = str(program + dataset + param2 + fmnist_ticket_path + p[0] \
        + "," + fmnist_ticket_path + p[1] \
        + "," + fmnist_ticket_path + p[2] \
        + "," + fmnist_ticket_path + p[3] + " --output_folder=" + result_path + p[0] + p[1] + p[2] + p[3])
    print(cmd)
    os.system(cmd)

#Reference:
#After creating some tickets run the merging test:
#python merge_tickets.py --prune_type=lt --arch_type=fc1 --dataset=mnist --prune_percent=10 --end_iter=20 --ticket_folders=tickets/A,tickets/B --output_folder=merge_result

#Average merging test:
#python merge_tickets_avg.py --prune_type=lt --arch_type=fc1 --dataset=mnist --prune_percent=10 --end_iter=20 --ticket_folders=tickets/A,tickets/B --output_folder=merge_result_avg
"""