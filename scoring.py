
def extract_info(lin):

    parts = lin.split(": ")
    timestamp = float((parts[0])[1:-1])
    actor = parts[1]
    detection = parts[2]

    return timestamp, actor, detection

# Provides scoring for each run
def score_run(filename):
    lines = []
    
    tot_per_detection = {
        "Fire":0,
        "Biohazard":0,
        "Low Oxygen":0,
        "Uninjured Person":0,
        "Injured Person":0,
        "Unconscious Person":0,
        "Connection Lost":0,
        "Robot Error":0
    }
    
    total = 0
    button_presses = 0
    correct = 0
    avg_correct_time = 0
    with open(filename) as file:
        lines = file.read().splitlines()
    
    for i, lin in enumerate(lines):
        t, a, d = extract_info(lin)
        if "VEST" in a:

            total += 1
            c = 1
            if i+c >= len(lines):
                break
            
            
            nt, na, nd = extract_info(lines[i+c])

            while "VEST" not in na:
                if nd == d: #Detection is registered
                    correct += 1
                    avg_correct_time += nt - t    
                
                if i+c+1 >= len(lines):
                    break 
                c += 1
                nt, na, nd = extract_info(lines[i+c])
        else:
            button_presses += 1                
            
        
    avg_correct_time /= correct
    print("TOTAL VEST:", total)
    print("TOTAL SELECTIONS:", button_presses)
    print("CORRECT SELECTIONS: ", correct)

    print("CORRECTLY CLICKED %", round(correct/total, 4)*100)
    print("CORRECT SELECTIONS %", round(correct/button_presses, 4)*100)
    print("AVG_TIME: ", avg_correct_time)

#score_run("results/vest/patterns/A0_0.txt")

score_run("results/vest/locational/B0L_2.txt")