# this is just an experiment:

Emanuel = [((0,1),(1,1)), ((1,1),(1,2)), ((1,2),(2,2)), ((2,2),(2,1)), ((2,1),(3,1)), ((3,1),(4,1)), ((3,1),(3,2)), ((3,2),(3,3)), ((3,3),(4,3)) ]
Hunter  = []
Chamin  = []
Kobi    = []

def test(player):
    longest_road = 0
    for i in player:
        temp_first_coord  = i[0]
        temp_second_coord = i[1]
        temp_in  = []
        temp_out = []

        for i in player:
            if (i[0] != temp_first_coord) and (i[1] != temp_second_coord):
                temp_in.append(i)

        print(temp_in)

        

test(Emanuel)