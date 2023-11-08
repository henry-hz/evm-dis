/*
 * Copyright 2023 Franck Cassez
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software dis-
 * tributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */


include "../../../src/dafny/utils/StackElement.dfy"
include "../../../src/dafny/utils/State.dfy"
include "../../../src/dafny/utils/LinSegments.dfy"
include "../../../src/dafny/disassembler/disassembler.dfy"
include "../../../src/dafny/proofobjectbuilder/Splitter.dfy"
include "../../../src/dafny/utils/int.dfy"

/**
  * Test correct computation of next State for segments.
  * 
  */
module RuNSegTests {

  import opened OpcodeDecoder
  import opened EVMConstants
  import Int
  import opened State
  import opened StackElement
  import opened BinaryDecoder
  import opened Splitter

  //  Simple example
  method {:test} Test1()
  {
    {
      //  Push and JUMP
      var x := DisassembleU8([PUSH1, 0x0a, PUSH1, 0x08, PUSH1, 0x03, SWAP1, PUSH1, 0x13, JUMP] );
      expect |x| == 6;
      var y := SplitUpToTerminal(x, [], []);
      expect |y| == 1;
      expect y[0].JUMPSeg?;
      //    Run Segment exit false. Should be Error
      var s0 := DEFAULT_VALIDSTATE;
      var s' := y[0].Run(s0, false);
      expect s'.Error?;

      var s1 := y[0].Run(s0, true);
      expect s1.EState?;
      expect s1 == EState(0x13,  [Value(0x08), Value(0x03), Value(0x0a)]);
    }
  }

  /** POP then DUP1 */
  method {:test} {:verify true} Test4()
  {
    //  Linear segment
    var x := DisassembleU8([POP, DUP1]);
    expect |x| == 2;
    var y := SplitUpToTerminal(x, [], []);
    expect |y| == 1;
    expect y[0].CONTSeg?;
    //    Run Segment exit false. Should be Error
    var s0 := DEFAULT_VALIDSTATE;
    var s' := y[0].Run(s0, true);
    expect s'.Error?;

    //  Not enough stakc element
    var s1 := y[0].Run(s0, false);
    expect s'.Error?;

    //  Good
    var s2 := y[0].Run(s0.(stack := [Random(), Random()]), false);
    expect s2.EState?;
    expect s2 == EState(0x02, [Random(), Random()]);

    var s3 := y[0].Run(s0.(stack := [Random(), Random()]), true);
    expect s3.Error?;
  }

  /**   Run more than one segment
    *   max-return.bin program
    */
  method {:test} {:verify false} Test5()
  {
    //  Linear segment
    var x := DisassembleU8(
      [
        /* 00000000: */ PUSH1, 0x0a,
        /* 00000002: */ PUSH1, 0x08,
        /* 00000004: */ PUSH1, 0x03,
        /* 00000006: */ SWAP1,
        /* 00000007: */ PUSH1, 0x13,
        /* 00000009: */ JUMP,

        /* 0000000a: */ JUMPDEST,
        /* 0000000b: */ PUSH1, 0x40,
        /* 0000000d: */ MSTORE,
        /* 0000000e: */ PUSH1, 0x20,
        /* 00000010: */ PUSH1, 0x40,
        /* 00000012: */ RETURN,

        /* 00000013: */ JUMPDEST,
        /* 00000014: */ SWAP2,
        /* 00000015: */ SWAP1,
        /* 00000016: */ DUP1,
        /* 00000017: */ DUP4,
        /* 00000018: */ LT,
        /* 00000019: */ PUSH1, 0x1f,
        /* 0000001b: */ JUMPI,

        /* 0000001c: */ JUMPDEST,
        /* 0000001d: */ POP,
        /* 0000001e: */ JUMP,

        /* 0000001f: */ JUMPDEST,
        /* 00000020: */ SWAP1,
        /* 00000021: */ SWAP2,
        /* 00000022: */ POP,
        /* 00000023: */ SWAP1,
        /* 00000024: */ PUSH0,
        /* 00000025: */ PUSH1, 0x1c,
        /* 00000027: */ JUMP
      ]
    );
    expect |x| == 31;
    var y := SplitUpToTerminal(x, [], []);
    expect |y| == 5;
    expect y[0].JUMPSeg?;
    expect y[1].RETURNSeg?;
    expect y[2].JUMPISeg?;
    expect y[3].JUMPSeg?;
    expect y[4].JUMPSeg?;
    //    Run Segment 0, exit true (JUMP)
    var s0 := DEFAULT_VALIDSTATE;
    var s1 := y[0].Run(s0, true);
    expect s1.EState?;
    expect s1.pc == 0x13;

    //  y[2] starts at 0x13, and JUMPI
    expect s1.pc == y[2].StartAddress();
    var s2 := y[2].Run(s1, true);
    expect s2.EState?;
    expect s2.pc == 0x1f;
    expect s2.stack == [Value(0x3), Value(0xa), Value(0x8)];

    //  y[4] starts at 0x1f, and JUMP
    expect s2.pc == y[4].StartAddress();
    var s3 := y[4].Run(s2, true);
    expect s3.EState?;
    expect s3.pc == 0x1c;
    expect s3.stack == [Value(0x0), Value(0xa), Value(0x3)];

    //  y[3] starts at 0x1c, and JUMP
    expect s3.pc == y[3].StartAddress();
    var s4 := y[3].Run(s3, true);
    expect s4.EState?;
    expect s4.pc == 0xa;
    expect s4.stack == [Value(0x3)];

    //  y[1] starts at 0x0a, and RETURN
    expect s4.pc == y[1].StartAddress();
    var s5 := y[1].Run(s4, false);
    expect s5.EState?;
    //  We end up after RETURN.
    expect s5 == EState(0x12 + 1, [Value(64), Value(32), Random()]);

    //  Now test JUMPI false (we go directly to successor of JUMPI)
    //  y[2] starts at 0x13, and JUMPI
    expect s1.pc == y[2].StartAddress();
    var s2' := y[2].Run(s1, false);
    expect s2'.EState?;
    expect s2' == EState(0x1c,  [Value(0x3), Value(0xa), Value(0x8)]);

    //  y[3] starts at 0x1c, and JUMP
    expect s2'.pc == y[3].StartAddress();
    var s3' := y[3].Run(s2', true);
    expect s3'.EState?;
    expect s3' == EState(0x0a,  [Value(0x8)]);

    //  y[1] starts at 0x0a, and RETURN
    expect s3'.pc == y[1].StartAddress();
    var s4' := y[1].Run(s3', false);
    expect s4' == EState(0x12 + 1,  [Value(64), Value(32), Random()]);

  }

  method {:test} {:verify true} Test6()
  {
    //  Linear segment, from max-return.bin
    var x := DisassembleU8(
      [
        /* 00000000 */ PUSH1, 0x12,
        /* 00000002 */ PUSH1, 0x08,
        /* 00000004 */ PUSH1, 0x0e,
        /* 00000006 */ PUSH1, 0x03,
        /* 00000008 */ PUSH1, 0x0a,
        /* 0000000a */ SWAP3,
        /* 0000000b */ PUSH1, 0x1b,
        /* 0000000d */ JUMP,

        /* 0000000e */ JUMPDEST,
        /* 0000000f */ PUSH1, 0x1b,
        /* 00000011 */ JUMP,

        /* 00000012 */ JUMPDEST,
        /* 00000013 */ PUSH1, 0x40,
        /* 00000015 */ MSTORE,
        /* 00000016 */ PUSH1, 0x20,
        /* 00000018 */ PUSH1, 0x40,
        /* 0000001a */ RETURN,

        /* 0000001b */ JUMPDEST,
        /* 0000001c */ SWAP2,
        /* 0000001d */ SWAP1,
        /* 0000001e */ DUP1,
        /* 0000001f */ DUP4,
        /* 00000020 */ LT,
        /* 00000021 */ PUSH1, 0x27,
        /* 00000023 */ JUMPI,

        /* 00000024 */ JUMPDEST,
        /* 00000025 */ POP,
        /* 00000026 */ JUMP,

        /* 00000027 */ JUMPDEST,
        /* 00000028 */ SWAP1,
        /* 00000029 */ SWAP2,
        /* 0000002a */ POP,
        /* 0000002b */ SWAP1,
        /* 0000002c */ PUSH0,
        /* 0000002d */ PUSH1, 0x24,
        /* 0000002f */ JUMP
      ]
    );

    expect |x| == 36;
    var y := SplitUpToTerminal(x, [], []);
    expect |y| == 6;
    expect y[0].JUMPSeg?;
    expect y[1].JUMPSeg?;
    expect y[2].RETURNSeg?;
    expect y[3].JUMPISeg?;
    expect y[4].JUMPSeg?;
    expect y[5].JUMPSeg?;

    //    Run Segment 0, exit true (JUMP)
    var s0 := DEFAULT_VALIDSTATE;
    var s1 := y[0].Run(s0, true);
    expect s1.EState?;
    expect s1.pc == 0x1b;

    // y[3] starts at 0x1b, and is a JUMPI
    expect s1.pc == y[3].StartAddress();
    var s2 := y[3].Run(s1, false);
    expect s2.EState?;
    expect s2.pc == 0x24;

    // print s2.stack;
    expect s2.stack == [Value(3), Value(14), Value(8), Value(10), Value(18)];

    // y[4] starts at 0x24, and is a JUMP
    expect s2.pc == y[4].StartAddress();
    var s3 := y[4].Run(s2, true);

    expect |y[4].ins| == 2;
    var s3' := y[4].ins[0].NextState(s2);

    expect s3'.EState?;
    var s4' := y[4].ins[1].NextState(s3');
    print "s4:", s4', "\n";

    expect s4'.EState?;
    var s5' := y[4].lastIns.NextState(s4', true);
    print "s5:", s5', "\n";

    expect s3.EState?;
    expect s3.pc == y[1].StartAddress();

    var s4 := y[1].Run(s3, true);
    expect s4.EState?;
    expect s4.pc == y[3].StartAddress();

    // y[3] starts at 0x1b, and is a JUMPI
    expect s4.pc == y[3].StartAddress();
    var s5 := y[3].Run(s4, false);
    expect s5.EState?;
    expect s5.pc == 0x24;

    expect s5.pc == y[4].StartAddress();
    var s6 := y[4].Run(s5, true);

    expect s6.EState?;
    expect s6.pc == 0x12;
  }
}

