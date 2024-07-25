import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import seaborn as sns
from experimental_trials.scoring import extract_info

# Example ground truth and predictions (replace with your actual data)
# These are just example arrays, replace them with your actual data.
# The arrays should contain the true labels and predicted labels.

labels = [
    "Fire",
    "Biohazard",
    "Low Oxygen",
    "Uninjured Person",
    "Injured Person",
    "Incapacitated",
    "Connection Lost",
    "Robot Error"
]

true_labels = np.random.randint(0, 8, size=1000)  # Example true labels
predicted_labels = np.random.randint(0, 8, size=1000)  # Example predicted labels

def getLabels(group='A', load=False):
    true = []
    reported = []
    e = 'L' if load else ''
    folder = 'patterns' if group == 'A' else 'locational'
    for i in range(0,10): #Participants
        for j in range(0,3): #Trials
            if group == 'B' and i == 2:
                continue
            if load and j == 2:
               continue
            else:
                try:
                    with open(f"results/vest/{folder}/{group}{i}{e}_{j}.txt") as file:
                        lines = file.read().splitlines() 
                        print(i,j)
                    for l, lin in enumerate(lines):
                        t, a, d = extract_info(lin) 
                        print("+", d)
                        if 'VEST' in a:
                            first = True
                            c = 1
                            if l+c >= len(lines):
                                break
                            
                            nt, na, nd = extract_info(lines[l+c])

                            while 'VEST' not in na:
                                if first:
                                    first = False
                                    
                                    true.append(labels.index(d))
                                    print(nd)
                                    reported.append(labels.index(nd))

                                if l+c+1 >= len(lines):
                                    break
                                c += 1
                                nt, na, nd = extract_info(lines[l+c])
                except:
                    print(f"Test {i}_{j} not found")
    
    return(true, reported)



print(true_labels)
print(predicted_labels)

# Create confusion matrix
true, reported = getLabels(group='A')
cm = confusion_matrix(true, reported)

# Plot confusion matrix
#plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='PuRd', xticklabels=labels, yticklabels=labels,cbar=False)
plt.xticks(rotation=25, ha='right')
plt.yticks(rotation=0, ha='right')
#plt.yticks([])
plt.subplots_adjust(bottom=0.26, right=1, left=0.245, top=0.945)
plt.savefig('conf1.png', bbox_inches='tight')
