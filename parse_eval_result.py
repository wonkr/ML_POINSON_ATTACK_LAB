#!/usr/bin/python3
def avg(lst):
    return sum(lst) / len(lst)

def get_avg_test_accuracy(filename):
    f = open(filename, "r")
    lines = f.readlines()

    test_accuracy = []
    for line in lines:
        # get test accuracy
        if line.startswith("Final test accuracy "):
            accur = float(line.split("=")[1].strip().replace("%",""))
            test_accuracy.append(accur)
    f.close()

    return (avg(test_accuracy))

def get_avg_target_misclassified_accuracy(filename):
    f = open(filename, "r")
    lines = f.readlines()

    test_accuracy = []
    for line in lines:
        # get test accuracy
        if line.startswith("The target is now"):
            accur = float(line.split("[[")[1].split()[1].replace("]]",""))
            test_accuracy.append(accur)
    f.close()
    return (avg(test_accuracy))

def get_avg_poison_classified_accuracy(filename):
    f = open(filename, "r")
    lines = f.readlines()

    test_accuracy = []
    for line in lines:
        # get test accuracy
        if line.startswith("The poison is now"):
            accur = float(line.split("[[")[1].split()[1].replace("]]",""))
            test_accuracy.append(accur)
    f.close()
    return (avg(test_accuracy))

get_avg_poison_classified_accuracy("dog_and_cat_eval")
eval_list = ["dog_and_cat_eval",
             "mouse_and_cat_eval"]

# refer from colab execution result
# https://colab.research.google.com/drive/1xCFJ86tA8lo7_vThehxUmaT_Y4KisiIH#scrollTo=NcYG2H4ceXJP 
# https://colab.research.google.com/drive/10wnT0R-fNmGC_P0AB6ozKFtnPcJFtz4f#scrollTo=mm4-TofGACaJ
final_test_accuracy_before_poisoned = {
    "dog_and_cat_eval": 97.0,
    "mouse_and_cat_eval": 99.0
}
for eval in eval_list:
    print("=======",eval,"=======")
    print("# Final test accuracy")
    print("before poisoned : ", 
          final_test_accuracy_before_poisoned[eval])
    print("after poisoned : ",
          get_avg_test_accuracy(eval))
    print("avg poison classified accuracy : ",
          get_avg_poison_classified_accuracy(eval))
    print("avg target misclassified accuracy : ",
          get_avg_target_misclassified_accuracy(eval))
