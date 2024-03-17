from random import randint
from numpy import argwhere, zeros, array,tile,array_equal,arange,sort,unique
from numpy.random import choice, shuffle,randint,random
from pygame.time import delay
import sys

sys.setrecursionlimit(100000)


class Matrix():



    def __init__(self):    
        self.sudoko = zeros((9, 9), dtype='i')
        self.original_sudoku = None
        self.sudokos = []
        self.get_valid()    
        self.direction = "forward"




        self.cells_not_diag = {
            "cell2": [(3, 6), (0, 3)],  
            "cell3": [(6, 9), (0, 3)],
            "cell4": [(0, 3), (3, 6)],
            "cell6": [(6, 9), (3, 6)],
            "cell7": [(0, 3), (6, 9)],
            "cell8": [(3, 6), (6, 9)]

        }
        self.cells_diag = {

            "cell1": [(0, 3), (0, 3)],
            "cell5": [(3, 6), (3, 6)],
            "cell9": [(6, 9), (6, 9)]
        }

        self.invalid_at_index = {}
        self.valid_at_index = {}
        self.index = 0
        self.valid_indices = []
        self.counter = 0
        self.filled = None
        self.prev_sudoku_image = None
        self.dont_touch = []

    def set_value(self, index, value):
        self.sudoko[index] = value

    def check_value_valid(self, index, val, cell=None):
        invalid = 0
        # ROW WISE
        if sum(self.sudoko[index[0],:]==val)>=1: return invalid 

        # COL WISE
        if sum(self.sudoko[:,index[1]]==val)>=1: return invalid

        # BLOCK WISE
        block_index = array([index[0]//3,index[1]//3])
        block_start = 3*block_index
        block_mat = self.sudoko[block_start[0]:block_start[0]+3,block_start[1]:block_start[1]+3].flatten()

        if sum(block_mat==val)>=1: return invalid

        
        # gebrish

        # if cell:
        #     if not invalid:
        #         cell.wrong = 0
        #         cell.box_color = (210, 210, 210)

        #     else:
        #         cell.box_color = "red"
        #         cell.wrong = 1

        return (invalid == 0)

    def check_valid_sudoku(self):
        '''' returns either a list of [1] if true 
            or a list of [0, problem in (row,col,block),i]
                    '''''
        for i in range(9):
        #check rows
            if len(unique(self.sudoko[i,:]))!=9: return [0 ,0, i]
            
        #check cols
            elif len(unique(self.sudoko[:,i]))!=9: return [0, 1, i] 

        #check blocks
            row, col= (i//3)*3, (i%3)*3
            box = self.sudoko[row:row + 3, col:col + 3]           
            if len(unique(box)) != 9 :return [0, 2, i]

        return [1]

    # for user exp 
    def get_same_value(self, val):
        if val == 0:
            return []
        return argwhere(self.sudoko == val)

    def get_valid(self):
        self.valids = argwhere(self.sudoko == 0)

    def recursive_Gen(self, blocks):
        #stop condition
        if len(argwhere(self.sudoko == 0)) == 0:
            return
        
        square_index_key = str(self.valids[self.index])
        square_index_tuple = tuple(self.valids[self.index])
        no_value = True

        if not (square_index_key in self.invalid_at_index.keys()):
            self.invalid_at_index[f'{self.valids[self.index]}'] = []

        

        for i in choice(range(1, 10), 9, replace=False):
            if i in self.invalid_at_index[square_index_key]:
                continue        
            if self.check_value_valid(square_index_tuple, i):
                self.set_value(square_index_tuple, i)
                # this can be optimized by making the self.sudoku in the box class
                #=================
                blocks[self.valids[self.index][0]][self.valids[self.index][1]].value = i
                #=================
                self.invalid_at_index[square_index_key].append(i)
                no_value = False
                break
            
            else:
                
                self.invalid_at_index[square_index_key].append(i)
        # delay(50)

        if no_value:
            blocks[self.valids[self.index][0]][self.valids[self.index][1]].value = 0
            self.set_value(square_index_tuple, 0)
            self.invalid_at_index[square_index_key] = []
            self.index -= 1
            self.recursive_Gen(blocks)

        else:
            self.index += 1
            self.recursive_Gen(blocks)

    def generate_valids_at_index(self):
        # generates invalids at all valid indexes for fixed puzzle generation to reduce the state space

     
        self.get_valid()
        for valid in self.valids:
            square_index_tuple = str(valid)
            if not (square_index_tuple in self.valid_at_index.keys()):
                self.valid_at_index[f'{valid}'] = []
            for i in range(1,10):
                if self.check_value_valid(tuple(valid), i):
                    self.valid_at_index[square_index_tuple].append(i)


        return

    def generate_for_fixed(self, blocks):
          #stop condition
        if len(argwhere(self.sudoko == 0)) == 0:
            return
        
        
        square_index_key = str(self.valids[self.index])
        square_index_tuple = tuple(self.valids[self.index])
        no_value = True        
        if not (square_index_key in self.invalid_at_index.keys()):
            self.invalid_at_index[f'{self.valids[self.index]}'] = []
        # print(self.index)
        # print(self.valid_at_index[square_index_key])
        shuffle(self.valid_at_index[square_index_key])
        for i in self.valid_at_index[square_index_key]:
            if i in self.invalid_at_index[square_index_key]:
                continue
            if self.check_value_valid(square_index_tuple, i):
                self.invalid_at_index[square_index_key].append(i)
                self.set_value(square_index_tuple, i)
                # this can be optimized by making the self.sudoku in the box class
                #=================
                blocks[self.valids[self.index][0]][self.valids[self.index][1]].value = i
                #=================
                no_value = False
                break
            else:
                self.invalid_at_index[square_index_key].append(i)
        
        delay(90)

        if no_value:
            self.invalid_at_index[square_index_key]  = []
            # print(self.invalid_at_index[square_index_key])
            blocks[self.valids[self.index][0]][self.valids[self.index][1]].value = 0
            self.set_value(square_index_tuple, 0)
            self.index -= 1
            self.generate_for_fixed(blocks)

        else:
            # print(self.invalid_at_index[square_index_key])
            self.index += 1
            self.generate_for_fixed(blocks)
        
        
        
        pass

    def Generate(self, BLOCKS):
        self.recursive_Gen(BLOCKS)

    def refresh(self, blocks):
        for rowidx, row in enumerate(self.sudoko):
            for colidx, col in enumerate(row):
                blocks[rowidx][colidx].value = col
                    
    def reset(self,suduko=0):
        if suduko:
         self.sudoko = zeros((9, 9), dtype='i')
        self.get_valid()    
        self.invalid_at_index = {}
        self.valid_indices = []
        self.index = 0
        self.counter = 0



    def fill(self, BLOCKS):
    

        self.iterative_gen(BLOCKS)
        delay(100)
        self.generate_unique_sol_sudoku(BLOCKS)
        # self.generate_random_values(BLOCKS)
        # self.generate_with_fixed_values(BLOCKS)
        
        # self.iterative_gen_with_fixed(BLOCKS)
        return
        self.recursive_Gen(BLOCKS)
        self.original_sudoku = self.sudoko
        # check = self.check_valid_sudoku()
        # if check[0]:
        #     print("VALID")
        # else:
        #     print("not valid:",check[1:])
    
        

            
        # print(self.original_sudoku)
        self.k = 20
        # THE SHUFFLE IS FOR RANDOM REMOVING 
        shuffle(self.valids)
        for i in range(self.k):
            self.set_value(tuple(self.valids[i]), 0)
            BLOCKS[self.valids[i][0]][self.valids[i][1]].value = 0

    # Todo
    def Solve(self):
        pass

    def get_filled(self):
        self.filled = argwhere(self.sudoko != 0)
        
        pass


    def generate_with_fixed_values(self,BLOCKS):
        ''' generates a sudoku with a pre existing fixed values 
            we suppose that the the values that should be generated all resign in indices with values 0
                                    '''
        self.refresh(BLOCKS)
        
        
        
        
        import time 
        time.sleep(5)
        self.iterative_gen_with_fixed(BLOCKS)

        # time.sleep(2)
        # self.generate_unique_sol_sudoku(BLOCKS)


        
        pass


    def iterative_gen(self,blocks):

        while (len(argwhere(self.sudoko==0)) != 0):
            delay(40)
            square_index_key = str(self.valids[self.index])
            square_index_tuple = tuple(self.valids[self.index])
            no_value = True
            if not (square_index_key in self.invalid_at_index.keys()):
                self.invalid_at_index[f'{self.valids[self.index]}'] = []

            for i in choice(range(1,10),9,replace=False):
                if i in self.invalid_at_index[square_index_key]:
                    continue

                if self.check_value_valid(square_index_tuple,i):
                    self.set_value(square_index_tuple,i)
                    blocks[self.valids[self.index][0]][self.valids[self.index][1]].value = i
                    #=================
                    self.invalid_at_index[square_index_key].append(i)
                    no_value = False
                    break
                
                else:
                    self.invalid_at_index[square_index_key].append(i)

            if no_value:
                blocks[self.valids[self.index][0]][self.valids[self.index][1]].value = 0
                self.set_value(square_index_tuple, 0)
                self.invalid_at_index[square_index_key] = []
                self.index -= 1

            else:
                self.index += 1
            

            
    def generate_random_values(self,blocks):
        probability_zero = round(random(),1)
        non_zero_prob = (1 - probability_zero) / 9
        probabilities = [probability_zero] + [non_zero_prob] * 9
        self.sudoko =   choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], size=(9, 9), p=probabilities)
        self.refresh(blocks)
        return self.sudoko.flatten().tolist()
        


        pass



    def iterative_gen_with_fixed(self,blocks):
        self.generate_valids_at_index()
        
          
        while(len(argwhere(self.sudoko == 0)) != 0):

        
        
            square_index_key = str(self.valids[self.index])
            square_index_tuple = tuple(self.valids[self.index])
            no_value = True        
            if not (square_index_key in self.invalid_at_index.keys()):
                self.invalid_at_index[f'{self.valids[self.index]}'] = []

            v = self.valids.tolist()
            for i in self.dont_touch:
                if i in v:
                    v.remove(i)
            if len(v) == 0:
                break

      
            shuffle(self.valid_at_index[square_index_key])

            for i in self.valid_at_index[square_index_key]:
                if i in self.invalid_at_index[square_index_key]:
                    continue
                if self.check_value_valid(square_index_tuple, i):
                    self.invalid_at_index[square_index_key].append(i)
                    self.set_value(square_index_tuple, i)
                    # this can be optimized by making the self.sudoku in the box class
                    #=================
                    blocks[self.valids[self.index][0]][self.valids[self.index][1]].value = i
                    #=================
                    no_value = False
                    break
                else:
                    self.invalid_at_index[square_index_key].append(i)
            
            delay(2
            )

            if no_value:
                self.invalid_at_index[square_index_key]  = []
                # print(self.invalid_at_index[square_index_key])
                blocks[self.valids[self.index][0]][self.valids[self.index][1]].value = 0
                self.set_value(square_index_tuple, 0)
                self.index -= 1

            else:
                # print(self.invalid_at_index[square_index_key])
                self.index += 1

        self.original_sudoku = self.sudoko

    def generate_unique_sol_sudoku(self,blocks):

        options = argwhere(self.sudoko != 0).tolist()
        self.static_sudoku = self.sudoko.copy()
        self.prev_sudoku_image = self.sudoko.copy()

        while(len(options) !=0):
            rand = randint(0,len(options))
            index = options[rand]
            self.prev_sudoku_image[tuple(index)] = -435
            self.sudoko = self.prev_sudoku_image
            print(self.prev_sudoku_image)
            self.sudoko[tuple(index)] = 0 
            self.refresh(blocks)
            self.reset()
            # delay(700)
            self.iterative_gen_with_fixed(blocks)
            if array_equal(self.sudoko,self.static_sudoku):
                self.dont_touch.append(index)
            else:
                self.prev_sudoku_image[tuple(index)] =  self.sudoko[tuple(index)]  
                
                

                
            del options[rand]
        self.sudoko = self.prev_sudoku_image

        
        self.refresh(blocks)


        # check if the option can be removed 
        # in the case of generating options for each image -->
        # how to generate options for each image:
        #   
        ''' the general case we should make the options is the whole sudoku states (81)
        we need to start by removing each option if we can and moving to the next elements until all the options are done
        '''

        # if it can be remove it then retry on the next image of the sudoku 
        # if cant check the other option until there is no options yet then we have the unique sudoku



        # for index in self.filled:
        #     val = self.sudoko[tuple(index)]
        #     self.sudoko[tuple(index)] = 0 
        #     self.reset()
        #     self.get_valid()
        #     self.iterative_gen_with_fixed(blocks)
        #     if array_equal(self.sudoko,self.original_sudoku):
        #         # self.filled.remove(index)
        #         continue
        #     else:
        #         self.sudoko[tuple(index)]=val
        #         continue




    
    
        
            

            
            





