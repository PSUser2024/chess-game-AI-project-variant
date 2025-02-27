from board.move import move
from pieces.nullpiece import nullpiece
from pieces.queen import queen
import random

class AI:

    global tp
    tp=[]


    def __init__(self):
        pass


    def evaluate(self,gametiles):
        min=100000
        count=0
        count2=0
        chuk=[]
        movex=move()
        tp.clear()
        xp=self.minimax(gametiles,3,-1000000000,1000000000,False)

        for zoom in tp:
            if zoom[4]<min:
                chuk.clear()
                chuk.append(zoom)
                min=zoom[4]
            if zoom[4]==min:
                chuk.append(zoom)
        fx=random.randrange(len(chuk))
        print(tp)
        return chuk[fx][0],chuk[fx][1],chuk[fx][2],chuk[fx][3]


    def reset(self,gametiles):
        for x in range(8):
            for y in range(8):
                if gametiles[x][y].pieceonTile.tostring()=='k' or gametiles[x][y].pieceonTile.tostring()=='r':
                    gametiles[x][y].pieceonTile.moved=False


    def updateposition(self,x,y):
        a=x*8
        b=a+y
        return b

    def checkmate(self,gametiles):
        movex=move()
        if movex.checkw(gametiles)[0]=='checked':
            array=movex.movesifcheckedw(gametiles)
            if len(array)==0:
                return True

        if movex.checkb(gametiles)[0]=='checked' :
            array=movex.movesifcheckedb(gametiles)
            if len(array)==0:
                return True

    def stalemate(self,gametiles,player):
        movex=move()
        if player==False:
            if movex.checkb(gametiles)[0]=='notchecked':
                check=False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1=movex.pinnedb(gametiles,moves1,y,x)
                            if len(lx1)==0:
                                continue
                            else:
                                check=True
                            if check==True:
                                break
                    if check==True:
                        break

                if check==False:
                    return True

        if player==True:
                if movex.checkw(gametiles)[0]=='notchecked':
                    check=False
                    for x in range(8):
                        for y in range(8):
                            if gametiles[y][x].pieceonTile.alliance=='White':
                                moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                                lx1=movex.pinnedw(gametiles,moves1,y,x)
                                if len(lx1)==0:
                                    continue
                                else:
                                    check=True
                                if check==True:
                                    break
                        if check==True:
                            break

                    if check==False:
                        return True






    def minimax(self,gametiles, depth,alpha , beta ,player):
        if depth==0 or self.checkmate(gametiles)==True or self.stalemate(gametiles,player)==True:
            return self.calculateb(gametiles)
        if not player:
            minEval=100000000
            kp,ks=self.eva(gametiles,player)
            for lk in kp:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.move(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,True)
                    if evalk<minEval and depth==3:
                        tp.clear()
                        tp.append(move)
                    if evalk==minEval and depth==3:
                        tp.append(move)
                    minEval=min(minEval,evalk)
                    beta=min(beta,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break

                if beta<=alpha:
                    break
            return minEval

        else:
            maxEval=-100000000
            kp,ks=self.eva(gametiles,player)
            for lk in ks:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.movew(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,False)
                    maxEval=max(maxEval,evalk)
                    alpha=max(alpha,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break
                if beta<=alpha:
                    break

            return maxEval



    def printboard(self,gametilles):
        count = 0
        for rows in range(8):
            for column in range(8):
                print('|', end=gametilles[rows][column].pieceonTile.tostring())
            print("|",end='\n')


    def checkeva(self,gametiles,moves):
        arr=[]
        for move in moves:
            lk=[[move[2],move[3]]]
            arr.append(self.calci(gametiles,move[0],move[1],lk))

        return arr



    def eva(self,gametiles,player):
        lx=[]
        moves=[]
        kp=[]
        ks=[]
        movex=move()
        for x in range(8):
            for y in range(8):
                    if gametiles[y][x].pieceonTile.alliance=='Black' and player==False:
                        if movex.checkb(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedb(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            kp=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='K'):
                                ax=movex.castlingb(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([0,6])
                                        if l=='qs':
                                            moves.append([0,2])
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            lx=movex.pinnedb(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        kp.append(self.calci(gametiles,y,x,moves))


                    if gametiles[y][x].pieceonTile.alliance=='White' and player==True:
                        if movex.checkw(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedw(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            ks=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if moves==None:
                            print(y)
                            print(x)
                            print(gametiles[y][x].pieceonTile.position)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='k'):
                                ax=movex.castlingw(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([7,6])
                                        if l=='qs':
                                            moves.append([7,2])
                        if gametiles[y][x].pieceonTile.alliance=='White':
                            lx=movex.pinnedw(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        ks.append(self.calci(gametiles,y,x,moves))

        return kp,ks



    def calci(self,gametiles,y,x,moves):
        arr=[]
        jk=object
        for move in moves:
            jk=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            mk=self.calculateb(gametiles)
            gametiles[y][x].pieceonTile=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=jk
            arr.append([y,x,move[0],move[1],mk])
        return arr


    def calculateb(self,gametiles):
        #Values and weights
        space_value             = 1
        pawn_value              = 100
        knight_value            = 350
        bishop_value            = 350
        rook_value              = 525
        queen_value             = 900
        king_value              = 10000
        king_move_per_space_val = 10
        king_on_back_file       = 50
        def_piece_val           = 0.75 
        atk_piece_percent_val   = 0.35
        check_val               = 400
        pawn_progression_val    = 20
        pawn_promo_val          = 10000
        checkmate_val           = 1000000
        
        back_file_opp           = 0
        back_file_us            = 7
       
        value=0
        for y in range(8):
            for x in range(8):
            #Adding or subtracting value for each type of piece on board
                if gametiles[y][x].pieceonTile.tostring()=='P':
                    value=value-pawn_value
                    #Add value if pawn in progressing down board
                    value=value - ((y - 1) * pawn_progression_val)

                if gametiles[y][x].pieceonTile.tostring()=='N':
                    value=value-knight_value

                if gametiles[y][x].pieceonTile.tostring()=='B':
                    value=value-bishop_value

                if gametiles[y][x].pieceonTile.tostring()=='R':
                    value=value-rook_value

                if gametiles[y][x].pieceonTile.tostring()=='Q':
                    value=value-queen_value
                    if y == back_file_us:
                        value=value-pawn_promo_val
                        
                if gametiles[y][x].pieceonTile.tostring()=='K':
                    value=value-king_value
                    #King spaces availible
                    value=value-(king_move_per_space_val * len(gametiles[y][x].pieceonTile.legalmoveb(gametiles)))
                    #Encourages King to stay in the back file
                    if y == back_file_us:
                        value=value-king_on_back_file

                if gametiles[y][x].pieceonTile.tostring()=='p':
                    value=value+pawn_value
                    #Add value if pawn in progressing down board    
                    value=value + ((back_file_us - 1 - y) * pawn_progression_val)
                if gametiles[y][x].pieceonTile.tostring()=='n':
                    value=value+knight_value

                if gametiles[y][x].pieceonTile.tostring()=='b':
                    value=value+bishop_value

                if gametiles[y][x].pieceonTile.tostring()=='r':
                    value=value+rook_value

                if gametiles[y][x].pieceonTile.tostring()=='q':
                    value=value+queen_value
                    #Add value if a pawn turns into a queen on last row
                    if y == back_file_opp:
                        value=value+pawn_promo_val
                        
                if gametiles[y][x].pieceonTile.tostring()=='k':
                    value=value+king_value
                    #King spaces availible
                    value=value + (100 * len(gametiles[y][x].pieceonTile.legalmoveb(gametiles)))
                    #Keeping King back
                    if y == back_file_opp:
                        value=value+king_on_back_file
                        
                #For each piece oppenent has in posession, give value for each attack and defense it has
                if (gametiles[y][x].pieceonTile.tostring() != '-') and (gametiles[y][x].pieceonTile.tostring().isupper()):
                    moves = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                    if moves != None:
                        for move in moves:
                            #Subtract value if the piece is taking up space
                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='-':
                                value=value-space_value
                            #Subtract value if the piece is guarding one of its own
                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='P':
                                value=value-(pawn_value * def_piece_val)

                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='N':
                                value=value-(knight_value * def_piece_val)

                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='B':
                                value=value-(bishop_value * def_piece_val)

                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='R':
                                value=value-(rook_value * def_piece_val)

                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='Q':
                                value=value-(queen_value * def_piece_val)

                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='K':
                                value=value-(king_value * def_piece_val)
                            #Subtract value if the piece is attacking opponent piece    
                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='p':
                                value=value-(pawn_value * atk_piece_percent_val)
                            
                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='n':
                                value=value-(knight_value * atk_piece_percent_val)

                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='b':
                                value=value-(bishop_value * atk_piece_percent_val)

                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='r':
                                value=value-(rook_value * atk_piece_percent_val)

                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='q':
                                value=value-(queen_value * atk_piece_percent_val)

                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='k':
                                value=value-check_val
                                
                if (gametiles[y][x].pieceonTile.tostring() != '-') and (gametiles[y][x].pieceonTile.tostring().islower()):
                    moves = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                    if moves != None:
                        for move in moves:
                            #Add value if the piece is taking up space
                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='-':
                                value=value+space_value
                            #Add value if the piece is attacking opponent piece    
                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='P':
                                value=value+(pawn_value * atk_piece_percent_val)
                                
                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='N':
                                value=value+(knight_value * atk_piece_percent_val)

                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='B':
                                value=value+(bishop_value * atk_piece_percent_val)

                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='R':
                                value=value+(rook_value * atk_piece_percent_val)

                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='Q':
                                value=value+(queen_value * atk_piece_percent_val)

                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='K':
                                value=value+check_val
                            #Add value if the piece is guarding one of its own
                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='p':
                                value=value+(pawn_value * def_piece_val)
                            
                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='n':
                                value=value+(knight_value * def_piece_val)

                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='b':
                                value=value+(bishop_value * def_piece_val)

                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='r':
                                value=value+(rook_value * def_piece_val)

                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='q':
                                value=value+(queen_value * def_piece_val)

                            if gametiles[move[0]][move[1]].pieceonTile.tostring()=='k':
                                value=value+(king_value * def_piece_val) 
        return int(value)


    def move(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='K' or gametiles[y][x].pieceonTile.tostring()=='R':
            gametiles[y][x].pieceonTile.moved=True

        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='P' and y+1==n and y==6:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='P':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('Black',self.updateposition(n,m))
                promotion=False

        return gametiles



    def revmove(self,gametiles,x,y,n,m,mts):
        if gametiles[x][y].pieceonTile.tostring()=='K':
            if m==y-2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[n][7].pieceonTile.moved=False

                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            elif m==y+2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(m,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[n][0].pieceonTile.moved=False
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts

            return gametiles

        if gametiles[x][y].pieceonTile.tostring()=='k':
            if m==y-2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            elif m==y+2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(n,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts


            return gametiles

        gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
        s=self.updateposition(n,m)
        gametiles[n][m].pieceonTile.position=s
        gametiles[x][y].pieceonTile=mts

        return gametiles



    def movew(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='k' or gametiles[y][x].pieceonTile.tostring()=='r':
            pass

        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='p' and y-1==n and y==1:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='p':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('White',self.updateposition(n,m))
                promotion=False

        return gametiles
























                        
