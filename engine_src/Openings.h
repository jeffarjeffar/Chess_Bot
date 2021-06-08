#ifndef OPENINGS_H_INCLUDED
#define OPENINGS_H_INCLUDED
#include <string>
#include <cstring>
#include <random>
#include <chrono>
#include <vector>

#include "State.h"

#define NUM_ALL 29
#define NUM_WHITE 5
#define NUM_BLACK 2

class opening
{
public:
	std::string name;
	std::vector <int> moves;

	opening(std::vector <std::string> vec)
	{
		name = vec[0];
		vec.erase(vec.begin());

		init_eval_info();
		state temp = state();
		for (auto move : vec)
		{
			int move_i = temp.parse_move(move);
			moves.push_back(move_i);
			temp.make_move(move_i);
		}
	}
};

std::vector <std::string> all[NUM_ALL] = {
	{"Queen's gambit declined, modern variation", "d4", "d5", "c4", "e6", "Nc3", "Nf6", "Bg5", "Be7", "e3", "O-O", "Nf3", "h6", "Bh4"}, 
	{"Tarrasach defense, two knights variation", "d4", "d5", "c4", "e6", "Nc3", "c5", "cxd5", "exd5", "Nf3", "Nc6", "g3"}, 
	{"Semi slav defense", "d4", "d5", "c4", "c6", "Nf3", "Nf6", "Nc3", "e6", "e3", "Nbd7", "Bd3", "dxc4", "Bxc4"}, 
	{"Ruy lopez, morphy defense, closed", "e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "Nf6", "0-0", "Be7", "Re1", "b5", "Bb3", "d6", "c3", "0-0", "d4"}, 
	{"Slav Defense: Modern, Alapin Variation, Czech Variation", "d4", "d5", "c4", "c6", "Nf3", "Nf6", "Nc3", "dxc4", "a4", "Bf5"}, 
	{"Slav Defense: Modern, Alapin Variation, Czech Variation", "d4", "d5", "c4", "c6", "Nf3", "Nf6", "Nc3", "dxc4", "e4", "b5", "Be2"}, 
	{"Slav Defense: Modern, Geller Gambit", "e4", "e5", "Nf3", "Nf6", "Nxe5", "d6", "Nf3", "Nxe4"}, 
	{"Pirc Defense : Classical Variation", "e4", "d6", "d4", "Nf6", "Nc3", "g6", "Nf3", "Bg7", "Bc4", "O-O", "O-O"}, 
	{"Semi Slav Defense", "d4", "d5", "c4", "e6", "Nc3", "c6", "Nf3", "Nf6", "Bg5", "h6"}, 
	{"Queen's gambit accepted", "d4", "d5", "c4", "dxc4", "e4", "Nf6", "e5", "Nd5", "Bxc4", "Nc6", "Nc3"}, 
	{"Queen's gambit accepted, McDonell defense", "d4", "d5", "c4", "dxc4", "e4", "e5", "Nf3", "exd4", "Bxc4", "Nc6", "O-O"}, 
	{"King's indian defense", "d4", "Nf6", "c4", "g6", "Nc3", "Bg7", "e4", "d6", "Nf3", "O-O", "Be2", "e5", "O-O", "Nc6", "d5", "Ne7"}, 
	{"Queen's Gambit Declined: Three Knights Variation", "d4", "Nf6", "c4", "e6", "Nf3", "d5", "Nc3"}, 
	{"Nimzo-Indian Defense", "d4", "Nf6", "c4", "e6", "Nc3", "Bb4", "e3"}, 
	{"Grunfeld defense", "d4", "Nf6", "c4", "g6", "Nc3", "d5", "cxd5", "Nxd5", "e4", "Nxc3", "bxc3"}, 
	{"Four Knights Game: Double Spanish Variation", "e4", "e5", "Nf3", "Nc6", "Bb5", "Nf6", "Nc3", "Bb4", "O-O", "O-O"}, 
	{"Sicilian defense: Sheveningen Variation", "e4", "c5", "Nf3", "d6", "d4", "cxd4", "Nxd4", "Nf6", "Nc3", "a6", "Be3", "e6", "Qd2", "Nd7", "f3", "b5", "a3", "Bb7", "0-0-0", "Rc8"}, 
	{"Silician defense: Sveshnikov Variation", "e4", "c5", "Nf3", "Nc6", "d4", "cxd4", "Nxd4", "Nf6", "Nc3", "e5", "Ndb5", "d6", "Nd5", "Nxd5", "exd5", "Ne7", "c4", "Nf5"}, 
	{"Silician defense: Lasker-Pelikan Variation", "e4", "c5", "Nf3", "Nc6", "d4", "cxd4", "Nxd4", "Nf6", "Nc3", "e5", "Ndb5", "a6", "Nd6+", "Bxd6", "Qxd6"},
	{"Sicilian defense: Open, Najdorf Variation", "e4", "c5", "Nf3", "d6", "d4", "cxd4", "Nxd4", "Nf6", "Nc3", "a6", "Bg5", "Nbd7", "Bc4", "Qb6", "Bb3", "e6", "Qd2", "Be7", "0-0-0", "Nc5"},
	{"Sicilian defense: Open, Najdorf Variation", "e4", "c5", "Nf3", "d6", "d4", "cxd4", "Nxd4", "Nf6", "Nc3", "a6", "Bg5", "Nbd7", "f4", "e6", "Qf3", "Qc7", "0-0-0", "Be7", "g4", "b5", "Bxf6", "Nxf6", "g5", "Nd7", "f5", "Bxg5", "Kb1", "Ne5", "Qh5"},
	{"Sicilian defense: Closed, traditional line", "e4", "c5", "Nc3", "Nc6", "Nf3", "e6", "d4"},
	{"Sicilian defense: Closed, fianchetto variation", "e4", "c5", "Nc3", "Nc6", "g3", "g6", "Bg2", "Bg7"},
	{"Sicilian defense: French variation", "e4", "c5", "Nf3", "e6", "d4", "cxd4", "Nxd4"},
	{"English Opening: Four Knights Variation", "c4", "e5", "Nc3", "Nf6", "Nf3", "Nc6", "g3"},
	{"English Opening: Four Knights Variation, quiet variation", "c4", "e5", "Nc3", "Nf6", "Nf3", "Nc6", "e3"},
	{"Giuoco Piano Game: Main Line", "e4", "e5", "Nf3", "Nc6", "Bc4", "Bc5", "c3", "Nf6", "d4", "exd4", "e5"},
	{"English Opening: King's English Variation", "c4", "e5", "g3", "Nf6", "Bg2", "d5", "cxd5", "Nxd5", "Nc3"},
	{"London System", "d4", "d5", "Nf3", "Nf6", "Bf4", "c5", "e3"}
};

std::vector <std::string> white[NUM_WHITE] = {
	{"French defense: Winnever variation", "e4", "e6", "d4", "d5", "Nc3", "Bb4", "e5"}, // petition to get rid of the french
	{"Ruy lopez, morphy defense, caro", "e4", "e5", "Nf3", "Nc6", "Bb5", "a6", "Ba4", "b5", "Bb3", "Nf6", "d4", "exd4", "e5", "Qe7", "O-O"}, // ruy lopez opening trap
	{"Stafford Refutation Line 1", "e4", "e5", "Nf3", "Nf6", "Nxe5", "Nc6", "Nxc6", "dxc6", "d3", "Bc5", "Be2", "h5", "c3", "Ng4", "d4", "Qh4", "g3", "Qf6", "f3", "h4", "Rg1"},
	{"Scandinavian Defense", "e4", "d5", "exd5", "Qxd5", "Nc3"},
	{"Stafford Refutation Line 2", "e4", "e5", "Nf3", "Nf6", "Nxe5", "Nc6", "Nxc6", "dxc6", "Nc3", "Bc5", "h3"}
};

std::vector <std::string> black[NUM_BLACK] = {
	{"Sodium attack", "Na3", "d5", "c4"},
	{"King's gambit", "e4", "e5", "f4", "exf4", "Nf3"},
};

std::vector<opening> openings, black_openings, white_openings;
// black openings are really good for black (engine will never play it as white)
// white openings are really good for white (engine will never play it as black)

void load_openings()
{
	for (int i = 0; i < NUM_ALL; i++) {
		openings.push_back(opening(all[i]));

		init_eval_info();
		state temp = state();
		for (int move : openings.back().moves) {
			temp.make_move(move);
			Bitstring hash = temp.get_hash();
			tt_exists[hash % TABLE_SIZE] = true;
			tt_depths[hash % TABLE_SIZE] = MAX_DEPTH;
			tt_evals[hash % TABLE_SIZE] = VALUE_ZERO;
			tt_hashes[hash % TABLE_SIZE] = hash;
		}
	}

	for (int i = 0; i < NUM_WHITE; i++)
		white_openings.push_back(opening(white[i]));
	for (int i = 0; i < NUM_BLACK; i++)
		black_openings.push_back(opening(black[i]));
}

void scramble_openings()
{
	std::mt19937 rnd(std::chrono::system_clock::now().time_since_epoch().count());
	for (int iter = 0; iter < (int)openings.size(); iter++)
		for (int ind = iter; ind < (int)openings.size() - 1; ind++)
			if (unsigned(rnd())&1)
				std::swap(openings[ind], openings[ind + 1]);
	for (int iter = 0; iter < (int) white_openings.size(); iter++)
		for (int ind = iter; ind < (int) white_openings.size() - 1; ind++)
			if (unsigned(rnd())&1)
				std::swap(white_openings[ind], white_openings[ind + 1]);
	for (int iter = 0; iter < (int) black_openings.size(); iter++)
		for (int ind = iter; ind < (int) black_openings.size() - 1; ind++)
			if (unsigned(rnd())&1)
				std::swap(black_openings[ind], black_openings[ind + 1]);
}

void remove_openings(int num_move, int move_i, bool computer_is_white) {
	for (int i = 0; i < openings.size(); i++)
	{
		if (openings[i].moves[num_move - 1] != move_i || openings[i].moves[num_move] == -1)
		{
			openings.erase(openings.begin() + i);
			i--;
		}
	}
	if (computer_is_white)
	{
		for (int i = 0; i < white_openings.size(); i++)
		{
			if (white_openings[i].moves[num_move - 1] != move_i || white_openings[i].moves[num_move] == -1)
			{
				white_openings.erase(white_openings.begin() + i);
				i--;
			}
		}
	}
	else
	{
		for (int i = 0; i < black_openings.size(); i++)
		{
			if (black_openings[i].moves[num_move - 1] != move_i || black_openings[i].moves[num_move] == -1)
			{
				black_openings.erase(black_openings.begin() + i);
				i--;
			}
		}
	}
}

#endif // !OPENINGS_H_INCLUDED
