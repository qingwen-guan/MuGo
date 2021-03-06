import go
from sgf_wrapper import replay_sgf
import unittest

from utils import parse_kgs_coords as pc
from test_utils import GoPositionTestCase, load_board

JAPANESE_HANDICAP_SGF = "(;GM[1]FF[4]CA[UTF-8]AP[CGoban:3]ST[2]RU[Japanese]SZ[9]HA[2]KM[5.50]PW[test_white]PB[test_black]AB[gc][cg];W[ee];B[dg])"

CHINESE_HANDICAP_SGF = "(;GM[1]FF[4]CA[UTF-8]AP[CGoban:3]ST[2]RU[Chinese]SZ[9]HA[2]KM[5.50]PW[test_white]PB[test_black]RE[B+39.50];B[gc];B[cg];W[ee];B[gg];W[eg];B[ge];W[ce];B[ec];W[cc];B[dd];W[de];B[cd];W[bd];B[bc];W[bb];B[be];W[ac];B[bf];W[dh];B[ch];W[ci];B[bi];W[di];B[ah];W[gh];B[hh];W[fh];B[hg];W[gi];B[fg];W[dg];B[ei];W[cf];B[ef];W[ff];B[fe];W[bg];B[bh];W[af];B[ag];W[ae];B[ad];W[ae];B[ed];W[db];B[df];W[eb];B[fb];W[ea];B[fa])"


class TestSgfWrapper(GoPositionTestCase):
    def test_sgf_props(self):
        sgf_replayer = replay_sgf(CHINESE_HANDICAP_SGF)
        initial = next(sgf_replayer)
        self.assertEqual(initial.metadata.result, 'B+39.50')
        self.assertEqual(initial.metadata.board_size, 9)
        self.assertEqual(initial.position.komi, 5.5)

    def test_japanese_handicap_handling(self):
        intermediate_board = load_board('''
            .........
            .........
            ......X..
            .........
            ....O....
            .........
            ..X......
            .........
            .........
        ''')
        intermediate_position = go.Position(
            intermediate_board,
            n=1,
            komi=5.5,
            caps=(0, 0),
            recent=(pc('E5'),),
            to_play=go.BLACK,
        )
        final_board = load_board('''
            .........
            .........
            ......X..
            .........
            ....O....
            .........
            ..XX.....
            .........
            .........
        ''')
        final_position = go.Position(
            final_board,
            n=2,
            komi=5.5,
            caps=(0, 0),
            recent=(pc('E5'), pc('D3')),
            to_play=go.WHITE,
        )

        positions_w_context = list(replay_sgf(JAPANESE_HANDICAP_SGF))
        self.assertEqualPositions(intermediate_position, positions_w_context[1].position)
        self.assertEqualPositions(final_position, positions_w_context[-1].position)

    def test_chinese_handicap_handling(self):
        intermediate_board = load_board('''
            .........
            .........
            ......X..
            .........
            .........
            .........
            .........
            .........
            .........
        ''')
        intermediate_position = go.Position(
            intermediate_board,
            n=1,
            komi=5.5,
            caps=(0, 0),
            recent=(pc('G7'),),
            to_play=go.BLACK,
        )
        final_board = load_board('''
            ....OX...
            .O.OOX...
            O.O.X.X..
            .OXXX....
            OX...XX..
            .X.XXO...
            X.XOOXXX.
            XXXO.OOX.
            .XOOX.O..
        ''')
        final_position = go.Position(
            final_board,
            n=50,
            komi=5.5,
            caps=(7, 2),
            ko=None,
            recent=(pc('E9'), pc('F9')),
            to_play=go.WHITE
        )
        positions_w_context = list(replay_sgf(CHINESE_HANDICAP_SGF))
        self.assertEqualPositions(intermediate_position, positions_w_context[1].position)
        self.assertEqual(positions_w_context[1].next_move, pc('C3'))
        self.assertEqualPositions(final_position, positions_w_context[-1].position)
        self.assertFalse(positions_w_context[-1].is_usable())
        self.assertTrue(positions_w_context[-2].is_usable())

if __name__ == '__main__':
    unittest.main()