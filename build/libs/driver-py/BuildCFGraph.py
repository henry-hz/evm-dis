import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_
import _dafny
import System_
import Int
import MiscTypes
import EVMConstants
import EVMOpcodes
import OpcodeDecoder
import Hex
import StackElement
import WeakPre
import State
import EVMToolTips
import Instructions
import BinaryDecoder
import LinSegments
import Splitter
import SegBuilder
import ProofObject
import PrettyIns
import PrettyPrinters
import ProofObjectBuilder
import ArgParser
import SeqOfSets
import PartitionMod
import Automata
import Minimiser
import CFGraph
import LoopResolver

# Module: BuildCFGraph

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def BuildCFGV4(xs, maxDepth, numSeg, s, seen, seenPCs, path):
        pat_let_tv2_ = xs
        pat_let_tv3_ = path
        pat_let_tv4_ = numSeg
        pat_let_tv5_ = path
        pat_let_tv6_ = xs
        pat_let_tv7_ = maxDepth
        pat_let_tv8_ = seen
        pat_let_tv9_ = seenPCs
        pat_let_tv10_ = path
        pat_let_tv11_ = path
        pat_let_tv12_ = numSeg
        pat_let_tv13_ = path
        pat_let_tv14_ = path
        pat_let_tv15_ = numSeg
        pat_let_tv16_ = path
        pat_let_tv17_ = xs
        pat_let_tv18_ = path
        pat_let_tv19_ = numSeg
        pat_let_tv20_ = path
        pat_let_tv21_ = xs
        pat_let_tv22_ = maxDepth
        pat_let_tv23_ = seen
        pat_let_tv24_ = seenPCs
        pat_let_tv25_ = path
        pat_let_tv26_ = seenPCs
        pat_let_tv27_ = path
        pat_let_tv28_ = numSeg
        pat_let_tv29_ = path
        pat_let_tv30_ = xs
        pat_let_tv31_ = maxDepth
        pat_let_tv32_ = seen
        pat_let_tv33_ = seenPCs
        pat_let_tv34_ = path
        pat_let_tv35_ = path
        pat_let_tv36_ = numSeg
        pat_let_tv37_ = xs
        pat_let_tv38_ = xs
        pat_let_tv39_ = seen
        pat_let_tv40_ = path
        pat_let_tv41_ = path
        pat_let_tv42_ = numSeg
        pat_let_tv43_ = path
        pat_let_tv44_ = path
        pat_let_tv45_ = numSeg
        pat_let_tv46_ = path
        if (not(((xs)[numSeg]).HasExit(False))) and (not(((xs)[numSeg]).HasExit(True))):
            return CFGraph.BoolCFGraph_BoolCFGraph(_dafny.SeqWithoutIsStrInference([]), 0)
        elif (maxDepth) == (0):
            return CFGraph.BoolCFGraph_BoolCFGraph(_dafny.SeqWithoutIsStrInference([CFGraph.BoolEdge_BoolEdge(CFGraph.CFGNode_CFGNode(path, MiscTypes.Option_Some(numSeg)), True, CFGraph.CFGNode_CFGNode(path, MiscTypes.Option_Some(numSeg)))]), (len(xs)) - (1))
        elif True:
            def iife37_(_pat_let18_0):
                def iife38_(d_978_leftSucc_):
                    def iife39_(_pat_let19_0):
                        def iife40_(d_979_nextSeg_):
                            def iife41_(_pat_let20_0):
                                def iife42_(d_980_src_):
                                    def iife43_(_pat_let21_0):
                                        def iife44_(d_981_tgt_):
                                            def iife45_(_pat_let22_0):
                                                def iife46_(d_982_gleft_):
                                                    return (d_982_gleft_).AddEdge(CFGraph.BoolEdge_BoolEdge(d_980_src_, False, d_981_tgt_))
                                                return iife46_(_pat_let22_0)
                                            return iife45_(default__.BuildCFGV4(pat_let_tv6_, (pat_let_tv7_) - (1), (d_979_nextSeg_).v, d_978_leftSucc_, (pat_let_tv8_) + (_dafny.SeqWithoutIsStrInference([d_981_tgt_])), (pat_let_tv9_) + (_dafny.SeqWithoutIsStrInference([(d_978_leftSucc_).PC()])), (pat_let_tv10_) + (_dafny.SeqWithoutIsStrInference([False]))))
                                        return iife44_(_pat_let21_0)
                                    return iife43_(CFGraph.CFGNode_CFGNode((pat_let_tv5_) + (_dafny.SeqWithoutIsStrInference([False])), d_979_nextSeg_))
                                return iife42_(_pat_let20_0)
                            return (iife41_(CFGraph.CFGNode_CFGNode(pat_let_tv3_, MiscTypes.Option_Some(pat_let_tv4_))) if (d_979_nextSeg_).is_Some else CFGraph.BoolCFGraph_BoolCFGraph(_dafny.SeqWithoutIsStrInference([CFGraph.BoolEdge_BoolEdge(CFGraph.CFGNode_CFGNode(pat_let_tv11_, MiscTypes.Option_Some(pat_let_tv12_)), False, CFGraph.CFGNode_CFGNode((pat_let_tv13_) + (_dafny.SeqWithoutIsStrInference([False])), MiscTypes.Option_None()))]), 0))
                        return iife40_(_pat_let19_0)
                    return (iife39_(LinSegments.default__.PCToSeg(pat_let_tv2_, (d_978_leftSucc_).PC(), 0)) if ((d_978_leftSucc_).is_EState) and (((d_978_leftSucc_).PC()) < (Int.default__.TWO__256)) else CFGraph.BoolCFGraph_BoolCFGraph(_dafny.SeqWithoutIsStrInference([CFGraph.BoolEdge_BoolEdge(CFGraph.CFGNode_CFGNode(pat_let_tv14_, MiscTypes.Option_Some(pat_let_tv15_)), False, CFGraph.CFGNode_CFGNode((pat_let_tv16_) + (_dafny.SeqWithoutIsStrInference([False])), MiscTypes.Option_None()))]), 0))
                return iife38_(_pat_let18_0)
            d_977_leftBranch_ = (iife37_(((xs)[numSeg]).Run(s, False)) if ((xs)[numSeg]).HasExit(False) else CFGraph.BoolCFGraph_BoolCFGraph(_dafny.SeqWithoutIsStrInference([]), 0))
            def iife47_(_pat_let23_0):
                def iife48_(d_984_rightSucc_):
                    def iife49_(_pat_let24_0):
                        def iife50_(d_985_nextSeg_):
                            def iife51_(_pat_let25_0):
                                def iife52_(d_986_src_):
                                    def iife53_(_pat_let26_0):
                                        def iife54_(d_987_tgt_):
                                            def iife55_(_pat_let27_0):
                                                def iife56_(d_988_gright_):
                                                    return (d_988_gright_).AddEdge(CFGraph.BoolEdge_BoolEdge(d_986_src_, True, d_987_tgt_))
                                                return iife56_(_pat_let27_0)
                                            return iife55_(default__.BuildCFGV4(pat_let_tv21_, (pat_let_tv22_) - (1), (d_985_nextSeg_).v, d_984_rightSucc_, (pat_let_tv23_) + (_dafny.SeqWithoutIsStrInference([d_987_tgt_])), (pat_let_tv24_) + (_dafny.SeqWithoutIsStrInference([(d_984_rightSucc_).PC()])), (pat_let_tv25_) + (_dafny.SeqWithoutIsStrInference([True]))))
                                        return iife54_(_pat_let26_0)
                                    return iife53_(CFGraph.CFGNode_CFGNode((pat_let_tv20_) + (_dafny.SeqWithoutIsStrInference([True])), d_985_nextSeg_))
                                return iife52_(_pat_let25_0)
                            def lambda59_(source71_):
                                if source71_.is_None:
                                    def iife57_(_pat_let28_0):
                                        def iife58_(d_989_src_):
                                            def iife59_(_pat_let29_0):
                                                def iife60_(d_990_tgt_):
                                                    def iife61_(_pat_let30_0):
                                                        def iife62_(d_991_gright_):
                                                            return (d_991_gright_).AddEdge(CFGraph.BoolEdge_BoolEdge(d_989_src_, True, d_990_tgt_))
                                                        return iife62_(_pat_let30_0)
                                                    return iife61_(default__.BuildCFGV4(pat_let_tv30_, (pat_let_tv31_) - (1), (d_985_nextSeg_).v, d_984_rightSucc_, (pat_let_tv32_) + (_dafny.SeqWithoutIsStrInference([d_990_tgt_])), (pat_let_tv33_) + (_dafny.SeqWithoutIsStrInference([(d_984_rightSucc_).PC()])), (pat_let_tv34_) + (_dafny.SeqWithoutIsStrInference([True]))))
                                                return iife60_(_pat_let29_0)
                                            return iife59_(CFGraph.CFGNode_CFGNode((pat_let_tv29_) + (_dafny.SeqWithoutIsStrInference([True])), d_985_nextSeg_))
                                        return iife58_(_pat_let28_0)
                                    return iife57_(CFGraph.CFGNode_CFGNode(pat_let_tv27_, MiscTypes.Option_Some(pat_let_tv28_)))
                                elif True:
                                    d_992___mcc_h0_ = source71_.v
                                    def iife63_(_pat_let31_0):
                                        def iife64_(d_993_prev_):
                                            return CFGraph.BoolCFGraph_BoolCFGraph(_dafny.SeqWithoutIsStrInference([CFGraph.BoolEdge_BoolEdge(CFGraph.CFGNode_CFGNode(pat_let_tv35_, MiscTypes.Option_Some(pat_let_tv36_)), True, d_993_prev_)]), len(pat_let_tv37_))
                                        return iife64_(_pat_let31_0)
                                    return iife63_(d_992___mcc_h0_)

                            return ((iife51_(CFGraph.CFGNode_CFGNode(pat_let_tv18_, MiscTypes.Option_Some(pat_let_tv19_))) if ((d_984_rightSucc_).PC()) not in (pat_let_tv26_) else lambda59_(LoopResolver.default__.SafeLoopFound(pat_let_tv38_, (d_984_rightSucc_).PC(), pat_let_tv39_, (pat_let_tv40_) + (_dafny.SeqWithoutIsStrInference([True]))))) if (d_985_nextSeg_).is_Some else CFGraph.BoolCFGraph_BoolCFGraph(_dafny.SeqWithoutIsStrInference([CFGraph.BoolEdge_BoolEdge(CFGraph.CFGNode_CFGNode(pat_let_tv41_, MiscTypes.Option_Some(pat_let_tv42_)), True, CFGraph.CFGNode_CFGNode((pat_let_tv43_) + (_dafny.SeqWithoutIsStrInference([True])), MiscTypes.Option_None()))]), 0))
                        return iife50_(_pat_let24_0)
                    return (iife49_(LinSegments.default__.PCToSeg(pat_let_tv17_, (d_984_rightSucc_).PC(), 0)) if ((d_984_rightSucc_).is_EState) and (((d_984_rightSucc_).PC()) < (Int.default__.TWO__256)) else CFGraph.BoolCFGraph_BoolCFGraph(_dafny.SeqWithoutIsStrInference([CFGraph.BoolEdge_BoolEdge(CFGraph.CFGNode_CFGNode(pat_let_tv44_, MiscTypes.Option_Some(pat_let_tv45_)), True, CFGraph.CFGNode_CFGNode((pat_let_tv46_) + (_dafny.SeqWithoutIsStrInference([True])), MiscTypes.Option_None()))]), 0))
                return iife48_(_pat_let23_0)
            d_983_rightBranch_ = (iife47_(((xs)[numSeg]).Run(s, True)) if ((xs)[numSeg]).HasExit(True) else CFGraph.BoolCFGraph_BoolCFGraph(_dafny.SeqWithoutIsStrInference([]), 0))
            return CFGraph.BoolCFGraph_BoolCFGraph(((d_977_leftBranch_).edges) + ((d_983_rightBranch_).edges), (len(xs)) - (1))

