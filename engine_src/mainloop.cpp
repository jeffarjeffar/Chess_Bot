﻿#include <ctime>

#include "Openings.h"
#include "options.h"
#include "Search.h"

void init_everything()
{
	init_table();
	curr_state = state();
	scramble_openings();
	load_openings();
	init_eval_info();
}

std::string read_fen() {
	std::string pos, turn, castle, ep, fiftymove, fullmove;
	std::cin >> pos >> turn >> castle >> ep >> fiftymove >> fullmove;
	return pos + " " + turn + " " + castle + " " + ep + " " + fiftymove + " " + fullmove;
}

int main()
{
	srand(time(NULL));
	set_default_options();
	std::string cmnd;
	while (cmnd != "exit")
	{
		init_everything();
		// std::cout << ">>>\n";
		std::cin >> cmnd;
		if (cmnd == "go")
		{
			std::string pos = read_fen();
			curr_state.load(pos);
			curr_state.print();
			std::cout << eval(curr_state, true) << std::endl;
			pii best_move = find_best_move(options["time_limit"], (Depth)options["depth_limit"]);
			if ((curr_state.to_move && best_move.first <= -RESIGN) || (!curr_state.to_move && best_move.first >= RESIGN))
			{
				std::cout << "COMPUTER PLAYED RESIGN" << std::endl;
				continue;
			}
			std::cout << "COMPUTER PLAYED " << curr_state.move_to_string(best_move.second) << std::endl
				<< "EVAL: " << (double)best_move.first / 100 << std::endl;
			curr_state.make_move(best_move.second);
			curr_state.print();
			std::cout << "GAME: " << curr_state.to_fen() << std::endl;
		} 
		else if (cmnd == "setoption") {
			std::string option_name;
			int value;
			std::cin >> option_name >> value;
			options[option_name] = value;
		} 
		else if (cmnd == "debug") {
			// std::string pos = read_fen();
			// curr_state.load(pos);
			// curr_state.print();
			// for (int p : curr_state.list_moves()) {
			// 	// std::cout << p.first << " " << p.second << std::endl;
			// 	std::cout << p << std::endl;
			// }
		}
		else if (cmnd == "quit")
		{
			break;
		}
		else
		{
			// std::cout << "COMMAND NOT RECOGNIZED\n";
		}
	}
	return 0;
}