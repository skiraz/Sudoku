import pygame
from matrix import Matrix
from box import square
from threading import Thread
from time import sleep 
import json




class Sudoku_Game():
    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.init()

        # window  
        self.width, self.height  = 540,540
        self.background_Color  = 'white'
        self.window  = pygame.display.set_mode((self.width,self.height))
        self.window.fill(self.background_Color)

        #input 
        self.numbers = str(list(range(1,10)))
        self.keypad  =  [f'[{i}]' for i in self.numbers]

        self.matrix  = Matrix()

        



        # grid Gui
        self.Block_Size = 60
        self.Blocks = [[square(self.window, (i*self.Block_Size, j*self.Block_Size), (self.Block_Size, self.Block_Size),
                  value=self.matrix.sudoko[i, j]) for i in range(9)] for j in range(9)]
       




        # game params
        self.run = True
        self.pos = 1
        self.blocks = []
        self.foucused  = None
        self.grey = (160)*3
        self.cond = False
        self.fps = 30


        #Threads
        self.Threads = {"filling_Thread": {"Thread": Thread(
        target=self.matrix.fill, args=[self.Blocks]), "status": 0}}

        # data generation
        self.generate_data = 0
        self.counter = 1
        self.image_name = "sudoku_"
        self.generated_data = {}
        self.generated_data["sudoku_images/sudoku_0.png"] = [0]*81
        
        


        pass
    


    def pos_to_index(self,pos):
        return (pos[0] // self.Block_Size, pos[1] // self.Block_Size)

    


    def draw_lines(self):
        for i in range(1, 3):
            pygame.draw.line(self.window, 'black', (i*3*60, 0), (i*3*60, self.height), (4))
            pygame.draw.line(self.window, 'black', (0, i*3*60), (self.width, i*3*60), (4))

    def draw(self):
        # draw boxes
        for row in self.Blocks:
            for col in row:
                col.draw()

        # draw lines
        for i in range(1, 3):
            pygame.draw.line(self.window, 'black', (i*3*60, 0),
                                (i*3*60, self.height), (4))
            pygame.draw.line(self.window, 'black', (0, i*3*60),
                                (self.width, i*3*60), (4))



    def on_click_change(self,pos):

        # COLOR AND VALUE


        if self.pos == -1:
            return
        self.pos = pos

        for block in self.blocks:
            if self.Blocks[block[0], block[1]].color != "white":
                self.Blocks[block[0], block[1]].color = "white"


        index = self.pos_to_index(pos)
        # mouse gets position inversed
        self.foucused = self.Blocks[index[1]][index[0]]
        blocks = self.matrix.get_same_value(self.foucused.value)
        if not len(self.blocks):

            self.foucused.border_color = (100, 100, 100)

        else:
            for block in self.blocks:
                self.Blocks[block[0], block[1]].border_color = (100, 100, 100)
        return
    
    def take_images_with_values(self,size = 0):
        if self.counter <= size:
            image_path = "sudoku_images_test/"+self.image_name+str(self.counter)+".png"
            values = self.matrix.generate_random_values(self.Blocks)
            self.generated_data[f"{image_path}"] = values
            self.draw()
            pygame.image.save(self.window,image_path)
            self.matrix.reset()
            self.counter+=1
            
        else:
            print("###################### END OF GENERATION #########################")
            with open("data.json", "w") as file:
                json.dump(self.generated_data, file,indent=2)
            self.generate_data = 1
            self.run = 0 

        
        
        

        

    def gameLoop(self):

        while(self.run):


            keys = pygame.key.get_pressed()
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    run = False
                    break
                # HANDLING INPUTS
                if event.type == pygame.KEYDOWN:
                    # CLOSE
                    if event.key == pygame.K_ESCAPE:
                        self.run = False
                        break
                    # DELETE
                    if event.key == pygame.K_BACKSPACE:
                        if self.foucused:
                            idx = self.pos_to_index(self.foucused.position)
                            self.matrix.set_value(idx, 0)
                            self.foucused.value = 0
                            self.foucused.box_color = self.grey
                            self.foucused.wrong = 0
                            self.pos = 1 

                    # INSERT
                    pressed = pygame.key.name(event.key)
                    if (pressed in self.numbers or pressed in self.keypad) & (self.pos != -1):
                        if self.foucused:
                            if len(pressed) > 1:
                                pressed = pressed[1]
                            pressed = int(pressed)
                            idx = self.pos_to_index(self.foucused.position)
                            self.foucused.value = pressed
                            if not self.matrix.check_value_valid(idx, pressed, self.foucused):
                                self.pos = -1
                            self.matrix.set_value(idx, pressed)

                    if (event.key == pygame.K_SPACE) and (not self.Threads["filling_Thread"]["status"]):
                        self.Threads["filling_Thread"]["Thread"].start()
                        self.Threads["filling_Thread"]["status"] = 1

        
            # movement
            if self.foucused:
                if keys[pygame.K_RIGHT]:
                    r, c = self.foucused.position
                    self.on_click_change((((r+self.Block_Size) % 540), c))
                if keys[pygame.K_LEFT]:
                    r, c = self.foucused.position
                    self.on_click_change((((r-self.Block_Size) % 540), c))
                if keys[pygame.K_UP]: 
                    r, c = self.foucused.position
                    self.on_click_change((r, ((c-self.Block_Size) % 540)))
                if keys[pygame.K_DOWN]:
                    r, c = self.foucused.position
                    self.on_click_change((r, ((c+self.Block_Size) % 540)))

            # MOUSE
            if (pygame.mouse.get_pressed()[0]):

                self.on_click_change(pygame.mouse.get_pos())

            
            self.clock.tick(self.fps)
            if self.generate_data:
                self.take_images_with_values(size  = 2)

            else: 
                self.draw()
            pygame.display.update()
            # data generation
            


            
      
            


        pygame.quit()




if __name__ =="__main__":
    game = Sudoku_Game()
    game.gameLoop()