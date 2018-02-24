import chess

# Maybe just try all sliding convolutions.
# Then I wouldnt get duplicates, and 3x2's would capture knight captures
CONVOLUTIONS = [(1,1),(2,2),(3,2),(2,3)]

def make_convolutions(square, width, height):
    # Convolutions are made a bit more complicated due to even sizes
    file_ = chess.square_file(square)
    rank_ = chess.square_rank(square)
    f_ranges, r_ranges = [], []
    for ranges, start, size in ((f_ranges, file_, width),
                                (r_ranges, rank_, height)):
        if size % 2 == 1:
            ranges.append(range(start-size//2, start+size//2+1))
        else:
            ranges.append(range(start-size//2, start+size//2))
            ranges.append(range(start-size//2+1, start+size//2+1))
    for f_range in f_ranges:
        for r_range in r_ranges:
            convolution = []
            for f in f_range:
                for r in r_range:
                    if f < 0 or f > 7 or r < 0 or r > 7:
                        convolution.append(None)
                    else: convolution.append(chess.square(f,r))
            yield convolution

convolutions = {square: [c for w, h in CONVOLUTIONS
                           for c in make_convolutions(square, w, h)]
                for square in chess.SQUARES}

def board_to_words(board):
    piece_map = board.piece_map()
    for square in piece_map.keys():
        for convolution in convolutions[square]:
            word = []
            for s in convolution:
                if s is None:
                    word.append('x')
                elif s in piece_map:
                    word.append(str(s)+piece_map[s].symbol())
                else:
                    word.append('-')
            yield ''.join(word)

def board_to_words2(board):
    piece_map = board.piece_map()
    for w, h in CONVOLUTIONS:
        for f1 in range(-1, 10-w):
            for r1 in range(-1, 10-h):
                word = ['_'.join(map(str,[w,h,f1,r1]))]
                for f in range(f1, f1+w):
                    for r in range(r1, r1+h):
                        if f < 0 or f > 7 or r < 0 or r > 7:
                            word.append('x')
                        else:
                            s = chess.square(f,r)
                            piece = piece_map.get(s, None)
                            if piece is None:
                                word.append('-')
                            else:
                                word.append(piece.symbol())
                yield ''.join(word)


