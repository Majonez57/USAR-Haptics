import matplotlib.pyplot as plt


def extract_info(lin):

    parts = lin.split(": ")
    timestamp = float((parts[0])[1:-1])
    actor = parts[1].strip()
    detection = parts[2].strip()

    return timestamp, actor, detection

def getdecs(s='', group='A'):
    tot_per_detection = {
        "Fire":0,
        "Biohazard":0,
        "Low Oxygen":0,
        "Uninjured Person":0,
        "Injured Person":0,
        "Incapacitated":0,
        "Connection Lost":0,
        "Robot Error":0
    }

    corr_per_detection = {
        "Fire":0,
        "Biohazard":0,
        "Low Oxygen":0,
        "Uninjured Person":0,
        "Injured Person":0,
        "Incapacitated":0,
        "Connection Lost":0,
        "Robot Error":0
    }

    folder = 'patterns' if group == 'A' else 'locational'

    xs = []
    for i in range(0, 10):
        for j in range(0, 3):

            try:
                countdet(f"results/vest/{folder}/{group}{i}{s}_{j}.txt", tot_per_detection, corr_per_detection)
            except:
                print(f"Test {i}_{j} not found")
    
    return tot_per_detection, corr_per_detection

def countdet(filename, totals, corrects):
    with open(filename) as file:
        lines = file.read().splitlines()
    
    for i, lin in enumerate(lines):
        t, a, d = extract_info(lin)

        if "VEST" in a:
            c = 1
            totals[d] +=1

            if i+c >= len(lines):
                break
            
            nt, na, nd = extract_info(lines[i+c])

            while "VEST" not in na:
                if nd == d: #Detection is
                    corrects[nd] += 1
                    d = "" # Avoid repeat detections

                if i+c+1 >= len(lines):
                    break 
                c += 1
                nt, na, nd = extract_info(lines[i+c])               

# Provides scoring for each run
def score_run(filename, time=False):
    lines = []
    
    total = 0
    button_presses = 0
    correct = 0
    avg_correct_time = 0
    avg_time = 0
    with open(filename) as file:
        lines = file.read().splitlines()
    
    for i, lin in enumerate(lines):
        t, a, d = extract_info(lin)
        
        if "VEST" in a:
            first = True
            total += 1
            c = 1
            if i+c >= len(lines):
                break
            
            nt, na, nd = extract_info(lines[i+c])

            while "VEST" not in na:
                if first:
                    if 'A' in filename:
                        if nd == "Incapacitated" or nd == "Injured Person" or nd == "Low Oxygen":
                            avg_time += (nt - 2.5) - t
                        else:
                            avg_time += (nt - 2) - t
                    else:
                        avg_time += (nt-1) - t
                    first = False
                if nd == d: #Detection is
                    correct += 1
                    avg_correct_time += nt - t 
                    d = "" # Avoid repeat detections

                if i+c+1 >= len(lines):
                    break 
                c += 1
                nt, na, nd = extract_info(lines[i+c])
        else:
            button_presses += 1                
            
        
    if time:
        return (avg_time / total if total != 0 else 0,0)
    else:
        # print("TOTAL VEST:", total)
        # print("TOTAL SELECTIONS:", button_presses)
        # print("CORRECT SELECTIONS: ", correct)

        # print("CORRECTLY CLICKED %", round(correct/total, 4)*100)
        # print("CORRECT SELECTIONS %", round(correct/button_presses, 4)*100)
        # print("AVG_TIME: ", avg_correct_time)

        return (correct/total, correct/(button_presses+0.000001)) # Div 0 fix

def average(group='A', load=False):
    score = 0
    acc = 0
    testn = 0.000000001
    vals = []
    e = 'L' if load else ''
    folder = 'patterns' if group == 'A' else 'locational'
    for i in range(0, 9):
        parts = 0
        partn = 0
        for j in range(0, 3):
            if group == 'B' and i == 2:
                continue

            if load and j == 2:
               continue
            if False:
                pass
            else:
                try:
                    s, a = score_run(f"results/vest/{folder}/{group}{i}{e}_{j}.txt", True)
                    parts += s
                    partn += 1
                    
                    score += s
                    vals.append(round(s,2))
                    acc += a
                    testn += 1
                except:
                    print(f"Test {i}_{j} not found")
        #print(parts/partn)
    
    print(vals)
    print(f"AVERAGE SCORE {group}{e}: {round(score/testn, 6)*100}%")
    print(f"AVERAGE ACCURACY {group}{e}: {round(acc/testn, 6)*100}%")

def getScoreData(group='A', load=False):
    
    e = 'L' if load else ''
    folder = 'patterns' if group == 'A' else 'locational'
    xs = []
    for i in range(0, 9):
        for j in range(0, 3):

            if group == 'B' and i == 2:    
                continue

            if load and j == 2:
               continue
            try:
                s, a = score_run(f"results/vest/{folder}/{group}{i}{e}_{j}.txt", time=True)
                xs.append(s*1000)
            except:
                print(f"Test {i}_{j} not found")
    
    return xs


if __name__ == "__main__":
    pats =  ["Fire",
            "Biohazard",
            "Low Oxygen",
            "Uninjured Person",
            "Injured Person",
            "Incapacitated",
            "Connection Lost",
            "Robot Error"]

    # tots, corrs = getdecs('L')
    # plotsL = [(corrs[pats[x]] / tots[pats[x]])*100 for x in range(len(tots))]
    tots, corrs = getdecs('', 'B')
    plotsB = [(corrs[pats[x]] / tots[pats[x]])*100 for x in range(len(tots))]
    tots, corrs = getdecs('L', 'B')
    plotsBL = [(corrs[pats[x]] / tots[pats[x]])*100 for x in range(len(tots))]
    tots, corrs = getdecs('', 'A')
    plotsA = [(corrs[pats[x]] / tots[pats[x]])*100 for x in range(len(tots))]
    tots, corrs = getdecs('L', 'A')
    plotsAL = [(corrs[pats[x]] / tots[pats[x]])*100 for x in range(len(tots))]

    X_axis = range(len(pats)) 
    
    # plt.bar(X_axis, plotsB, 0.2, label = 'Advanced', color='gold') 
    # plt.bar([x +0.2 for x in X_axis], plotsBL, 0.2, label = 'Positional',color='lightgreen') 
    # plt.bar([x +0.4 for x in X_axis], plotsA, 0.2, label = 'Advanced', color='purple') 
    # plt.bar([x +0.6 for x in X_axis], plotsAL, 0.2, label = 'Positional',color='skyblue') 


    # plt.xticks(X_axis, pats) 
    # plt.xlabel("Pattern") 
    # plt.xticks(rotation=25)
    # plt.xlabel("% Accuracy") 
    # plt.legend() 
    # plt.grid(True, axis='y')
    # plt.show() 

    data = []
    data += [getScoreData('A', True)]
    data += [getScoreData('A', False)]
    data += [getScoreData('B', True)]
    data += [getScoreData('B', False)]

    print(data)

    # Define colors for each box
    colors = ['skyblue', 'purple', 'lightgreen', 'gold']
    labels = [ "Semantic \n (+Cognitive Load)", "Semantic", "Positional \n (+Cognitive Load)", "Positional"]

    f = plt.figure()
    f.set_figwidth(6)
    f.set_figheight(5)

    # Create boxplot with different colors
    box = plt.boxplot(data, vert=False, patch_artist=True, labels=labels, notch=True)

    # Set different colors for each box
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)

    plt.grid(True, axis='x')
    plt.xlabel("Delay (ms)")
    #plt.xlabel("Accuracy (%)")
    #plt.xticks(range(0,110, 10))
    plt.savefig('test.png', bbox_inches='tight')
    #print(score_run(f"results/vest/patterns/A6L_2.txt"))

    #average('A', False)
    #average('B', False)
    #average('A', True)
    #average('B', True)