#!/usr/bin/env python

import spade
from bot.bot import *
from time import sleep
import sys

try:
    import psyco
    psyco.full()
except:
    print 'Psyco not found'
    
class Igrac( spade.Agent.Agent ):
    class TrazimIgru( spade.Behaviour.OneShotBehaviour ):
        def _process( self ):
            originDTM = DTM( {(1020, 651): (30, 193, 56), (408, 650): (30, 193, 56)} )
            origin = findDTM( originDTM, 0, 0, self.myAgent.sx, self.myAgent.sy )
            if origin:
                setOrigin( origin )
                self._exitcode = self.myAgent.P_IGRA_PRONADJENA
                return
            else:
                print 'Ne mogu pronaci igru!'
                sleep( 1 )
                self._exitcode = self.myAgent.P_NEMA_IGRE
                return
    
    class PokrecemIgru( spade.Behaviour.OneShotBehaviour ):
        def _process( self ):
            if self.myAgent.prvi:
                level = self.myAgent.razina
                sleep(1)
                mouseClick(710, 520, True)
                sleep(4)
                mouseClick( 880, 489, True )
                sleep(2)
                mouseClick( 610, 528, True )
                sleep(2)
                if level == "easy":
                    mouseClick( 725, 492, True )
                elif level == "medium":
                    mouseClick( 725, 546, True )
                elif level == "hard":
                    mouseClick( 725, 604, True )
                sleep(2)
                mouseClick( 721, 426, True )
                sleep(1)
                self.myAgent.prvi = False
                self._exitcode = self.myAgent.P_POCETAK_IGRE
                return
            else:
                self.myAgent.prvi = True      


    class IgramIgru( spade.Behaviour.OneShotBehaviour ):
        def _process( self ): 
            print "Igram!"
            self.myAgent.brojacPokusaja += 1
            area = getArea( 0, 0, self.myAgent.sx, self.myAgent.sy )
            flag = False
            level = self.myAgent.razina
            for y in range(415,597):
                if flag:
                    break
                for x in range( 534,912):
                    if area.getpixel( ( x, y ) ) in [ (255,255,255),(101,212,252)]:
                        if level == "easy":
                            mouseClick( x+20, y+30, True)
                        elif level == "medium":
                            mouseClick( x-20, y+30, True )
                        elif level == "hard":
                            mouseClick( x-30, y+30, True )
                        sleep(0.5)
                        flag = True
                        break
            if self.myAgent.brojacPokusaja > 27:
                self.myAgent.brojacPokusaja = 0
                self.myAgent.prviIgraj = False
                self._exitcode = self.myAgent.P_IGRAJ_PONOVNO
                return
            else:
                self._exitcode = self.myAgent.P_POCETAK_IGRE
                return
                
    class IgrajPonovno( spade.Behaviour.OneShotBehaviour ):
        def _process( self ):
            if self.myAgent.prviPonovno:
                self.myAgent.brojacRundi += 1
                if self.myAgent.brojacRundi == 3:
                    self._exitcode = self.myAgent.P_KRAJ_IGRE
                    return
                else:
                    sleep(1)
                    mouseClick(795, 579, True)          
                    sleep(0.5)
                    self.myAgent.prviPonovno = False
                    self._exitcode = self.myAgent.P_POCETAK_IGRE
                    return
            else:
                self.myAgent.prviPonovno = True

    class KrajIgre( spade.Behaviour.OneShotBehaviour ):
        def _process( self ):
            print 'Igra je zavrsena!'
            self.myAgent._kill()
            
    def _setup( self ):
        print "pocinje igra!"
        self.sx, self.sy = getScreenSize()
        self.brojacPokusaja = 0
        self.prvi = True
        self.prviIgraj = True
        self.prviPonovno = True
        self.brojacRundi = 0
        self.korak = 0
        self.razina = sys.argv[1]
        
        self.S_TRAZIM_IGRU = 1
        self.S_POKRECEM_IGRU = 2
        self.S_IGRAM_IGRU = 3
        self.S_IGRAJ_PONOVNO = 4
        self.S_ZAVRSI_IGRU = 5
        
        self.P_NEMA_IGRE = 100
        self.P_IGRA_PRONADJENA = 101
        self.P_POCETAK_IGRE = 102
        self.P_IGRAJ_PONOVNO = 103
        self.P_KRAJ_IGRE = 104
        
        p = spade.Behaviour.FSMBehaviour()
        p.registerFirstState( self.TrazimIgru(), self.S_TRAZIM_IGRU )
        p.registerState(self.PokrecemIgru(), self.S_POKRECEM_IGRU)
        p.registerState(self.IgramIgru(), self.S_IGRAM_IGRU)
        p.registerState(self.IgrajPonovno(), self.S_IGRAJ_PONOVNO)
        p.registerLastState(self.KrajIgre(), self.S_ZAVRSI_IGRU)
        
        p.registerTransition( self.S_TRAZIM_IGRU, self.S_TRAZIM_IGRU, self.P_NEMA_IGRE )
        p.registerTransition( self.S_TRAZIM_IGRU, self.S_POKRECEM_IGRU, self.P_IGRA_PRONADJENA )
        p.registerTransition(self.S_POKRECEM_IGRU, self.S_IGRAM_IGRU, self.P_POCETAK_IGRE)
        p.registerTransition(self.S_IGRAM_IGRU, self.S_IGRAM_IGRU, self.P_POCETAK_IGRE)
        p.registerTransition(self.S_IGRAM_IGRU, self.S_IGRAJ_PONOVNO, self.P_IGRAJ_PONOVNO)
        p.registerTransition(self.S_IGRAJ_PONOVNO, self.S_IGRAM_IGRU, self.P_POCETAK_IGRE)
        p.registerTransition(self.S_IGRAJ_PONOVNO, self.S_ZAVRSI_IGRU, self.P_KRAJ_IGRE)
        
        self.addBehaviour( p, None )
        
if __name__ == '__main__':
    a = Igrac( 'igrac@127.0.0.1', 'tajna' )
    a.start()