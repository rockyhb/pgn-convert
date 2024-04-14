import argparse
import chess.pgn
import chess.engine
import stockfish

parser = argparse.ArgumentParser(description='Convert PGNs')
parser.add_argument('pgn_file',type=open,help='PGN file to read from')
parser.add_argument('-o','--out',type=argparse.FileType('w', encoding='latin-1'),required=False,help='File to write result to')
parser.add_argument('-e','--event',required=True,help='Set event header')
parser.add_argument('-r','--round',type=int,required=True,help='Set round')
parser.add_argument('-w','--white',required=True,help='Set white player')
parser.add_argument('-b','--black',required=True,help='Set black player')
parser.add_argument('--engine',help='Set path to stockfish engine')
args = parser.parse_args()
print(args)

#pgn = open(args.pgn_file)

if args.engine:
    #engine = chess.engine.SimpleEngine.popen_uci(args.engine)
    engine = stockfish.Stockfish(args.engine)

no = 0
while True:
    game = chess.pgn.read_game(args.pgn_file)
    if not game:
        break
    game.headers["Event"] = args.event
    no=no+1
    game.headers["Round"] = str(args.round)+'.'+str(no)
    game.headers["White"] = args.white
    game.headers["Black"] = args.black
    if args.engine:
        #result = engine.play(game.board, chess.engine.Limit(time=1))
        engine.set_fen_position(game.board().fen())
        print(game.board().fen())
        best_move = engine.get_best_move_time(1000)
        print(best_move)
        top_moves = engine.get_top_moves(3)
        print(top_moves)
        print(game.turn())
        if game.turn():
            game.comment = '[%tqu "De","Weiß am Zug","","","'+best_move+'","",10]'
        else:
            game.comment = '[%tqu "De","Schwarz am Zug","","","'+best_move+'","",10]'
        game.add_variation(chess.Move.from_uci(best_move))
        #result = engine.play(game.board, chess.engine.Limit(time=1))
        #game.move(result.move)
    if args.out:
        print(game,file=args.out)
        print(file=args.out)

    print(game)
    print()


