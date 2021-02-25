a : bin/Eval_info.o bin/Evaluate.o bin/List_moves.o bin/mainloop.o bin/Make_move.o bin/Search_util.o bin/Search.o bin/State_constants.o bin/State_io.o bin/State_util.o bin/Transpose.o bin/Unmake_move.o
	g++ bin/Eval_info.o bin/Evaluate.o bin/List_moves.o bin/mainloop.o bin/Make_move.o bin/Search_util.o bin/Search.o bin/State_constants.o bin/State_io.o bin/State_util.o bin/Transpose.o bin/Unmake_move.o

bin/Eval_info.o :
	g++ -c Chess_Bot/engine/Eval_info.cpp -o bin/Eval_info.o

bin/Evaluate.o : Chess_Bot/engine/Evaluate.cpp Chess_Bot/engine/Evaluate.h
	g++ -c Chess_Bot/engine/Evaluate.cpp -o bin/Evaluate.o

bin/List_moves.o : Chess_Bot/engine/List_moves.cpp Chess_Bot/engine/State.h
	g++ -c Chess_Bot/engine/List_moves.cpp -o bin/List_moves.o

bin/mainloop.o : Chess_Bot/engine/mainloop.cpp Chess_Bot/engine/Engine.h Chess_Bot/engine/Bot_2_2.h
	g++ -c Chess_Bot/engine/mainloop.cpp -o bin/mainloop.o

bin/Make_move.o : Chess_Bot/engine/Make_move.cpp Chess_Bot/engine/State.h
	g++ -c Chess_Bot/engine/Make_move.cpp -o bin/Make_move.o

bin/Search_util.o : Chess_Bot/engine/Search_util.cpp Chess_Bot/engine/Search.h
	g++ -c Chess_Bot/engine/Search_util.cpp -o bin/Search_util.o

bin/Search.o : Chess_Bot/engine/Search.cpp Chess_Bot/engine/Search.h
	g++ -c Chess_Bot/engine/Search.cpp -o bin/Search.o

bin/State_constants.o : Chess_Bot/engine/State_constants.cpp Chess_Bot/engine/State.h
	g++ -c Chess_Bot/engine/State_constants.cpp -o bin/State_constants.o

bin/State_io.o : Chess_Bot/engine/State_io.cpp Chess_Bot/engine/State.h
	g++ -c Chess_Bot/engine/State_io.cpp -o bin/State_io.o

bin/State_util.o : Chess_Bot/engine/Search_util.cpp Chess_Bot/engine/State.h
	g++ -c Chess_Bot/engine/State_util.cpp -o bin/State_util.o

bin/Transpose.o : Chess_Bot/engine/Transpose.cpp Chess_Bot/engine/Transpose.h
	g++ -c Chess_Bot/engine/Transpose.cpp -o bin/Transpose.o

bin/Unmake_move.o : Chess_Bot/engine/Unmake_move.cpp Chess_Bot/engine/State.h
	g++ -c Chess_Bot/engine/Unmake_move.cpp -o bin/Unmake_move.o

clear : 
	rm a bin/Eval_info.o bin/Evaluate.o bin/List_moves.o bin/mainloop.o bin/Make_move.o bin/Search_util.o bin/Search.o bin/State_constants.o bin/State_io.o bin/State_util.o bin/Transpose.o bin/Unmake_move.o