import os

import pandas as pd

def get_moves(my_file, move_dict):

    moves = False
    for line in my_file:
        if 'count' in line:
            count = int(line.strip().strip('|').split(':')[1])
            #print(count)
        
        if moves == True:
            if '+' not in line:
                move_line = line.strip().strip('|').split()
                move = ' '.join(move_line[:-1])
                percent = float(move_line[-1][:-1])/100
                total = round(count * percent)
                #print(move, percent, total)
        
            if move not in move_dict:
                move_dict[move] = total
            else:
                move_dict[move] += total

        if 'Moves' in line:
            moves = True
        if 'Other' in line:
            moves = False
        if '+' in line:
            moves = False     

    return move_dict
 
def main():

    data_dir = 'data/www.smogon.com/stats/2022-06/moveset'

    file_list = ['gen7anythinggoes-0.txt', 'gen8anythinggoes-0.txt',
                 'gen7ou-0.txt', 'gen8ou-0.txt', 
                 'gen7uu-0.txt', 'gen8uu-0.txt']
    
    move_dict = {}
    
    for f in file_list:
        curr_file = open(os.path.join(data_dir, f))
        
        move_dict = get_moves(curr_file, move_dict)

    del move_dict['Other']

    
    df_showdown = pd.DataFrame(move_dict.items(), columns=['Name', 'Count'])

    df_showdown['Name_UPPER'] = df_showdown.apply(lambda row: row['Name'].replace(' ', '').replace('-', '').upper(), axis=1)

    #print(df_showdown)

    df_unown = pd.read_csv('Unown_Move_Data - Metadata.csv')

    #print(df_unown)
    
    df = df_showdown.merge(df_unown, how='outer', left_on='Name_UPPER', right_on='Move')

    df = df.sort_values(by='Count', ascending=False)

    df.to_csv('Unown_Moves_Smogon_Stats.csv', index=False)

    print(df)

if __name__ == "__main__":
    main()
