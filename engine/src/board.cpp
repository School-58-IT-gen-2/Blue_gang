#include "main.h"

#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>
#include "../../dependencies/nlohmann/json/json-master/single_include/nlohmann/json.hpp"

using namespace std;
using json = nlohmann::json;


Figure* Board::figure_by_position(pair<int, int> position) {
    for (auto figure : figures) {
        if (figure->position == position) {
            return figure;
        }
    }
    return new NullFigure(this);
}

void Board::clear_null_figures() {
    figures.erase(remove_if(figures.begin(), figures.end(), [](Figure* figure) { return figure->name == "null"; }), figures.end());
}

void Board::print(){
    clear_null_figures();
    vector<vector<string>> board(8, vector<string>(8, "."));
    for (Figure* figure : figures) {
        board[figure->position.first][figure->position.second] = figure->symbol;
    }
    for (const auto &row : board) {
        for (const auto &cell : row) {
            cout << cell << ' ';
        }
        cout << '\n';
    }
}

void Board::info() {
    clear_null_figures();
    for (auto figure : figures) {
        cout << figure->name << " " << figure->color << " " << position_to_chess_notation(figure->position) << endl;
    }
}

void Board::change_turn(){
    if (this->turn == "white"){
        this->turn = "black";
    }
    else {
        this->turn = "white";
    }
}

void Board::kill(std::pair<int, int> position) {
    auto fig = figure_by_position(position);

    if (not fig->is_null()) {
        auto it = std::find(figures.begin(), figures.end(), fig);
        if (it != figures.end()) {
            delete *it;
            figures.erase(it);
        }
    }
}

string Board::move(pair<int, int> pos1, pair<int, int> pos2){
    if (turn == figure_by_position(pos1)->color){
        Figure* figure = figure_by_position(pos1);
        auto pawn = dynamic_cast<Pawn*>(figure);
        auto rook = dynamic_cast<Rook*>(figure);
        auto knight = dynamic_cast<Knight*>(figure);
        auto bishop = dynamic_cast<Bishop*>(figure);
        auto queen = dynamic_cast<Queen*>(figure);
        auto king = dynamic_cast<King*>(figure);


        if (pawn) {
            auto available_moves = pawn->available_moves();
            if (not available_moves.empty() and find(available_moves.begin(), available_moves.end(), pos2) != available_moves.end()) {
                pawn->move(pos2);
            } else {
                cout << "Invalid move" << endl;
            }
        }
        else if (rook) {
            auto available_moves = rook->available_moves();
            if (not available_moves.empty() and find(available_moves.begin(), available_moves.end(), pos2) != available_moves.end()) {
                rook->move(pos2);
            } else {
                cout << "Invalid move" << endl;
            }
        }
        else if (knight) {
            auto available_moves = knight->available_moves();
            if (not available_moves.empty() and find(available_moves.begin(), available_moves.end(), pos2) != available_moves.end()) {
                knight->move(pos2);
            } else {
                cout << "Invalid move" << endl;
            }
        }
        else if (bishop) {
            auto available_moves = bishop->available_moves();
            if (not available_moves.empty() and find(available_moves.begin(), available_moves.end(), pos2) != available_moves.end()) {
                bishop->move(pos2);
            } else {
                cout << "Invalid move" << endl;
            }
        }
        else if (queen) {
            auto available_moves = queen->available_moves();
            if (not available_moves.empty() and find(available_moves.begin(), available_moves.end(), pos2) != available_moves.end()) {
                queen->move(pos2);
            } else {
                cout << "Invalid move" << endl;
            }
        }
        else if (king) {
            auto available_moves = king->available_moves();
            if (not available_moves.empty() and find(available_moves.begin(), available_moves.end(), pos2) != available_moves.end()) {
                king->move(pos2);
            } else {
                cout << "Invalid move" << endl;
            }
        }
        else {
            cout << "Figure not found" << endl;
        }
        this->change_turn();
    }
    else{
        cout << "Not your turn" << endl;
    }
    return "moved";
}


void Board::put_figure(Figure* figure){
    figures.push_back(figure);
}

void Board::import_json(std::string path) {
    ifstream file(path);
    json data;
    Board& board = *this;
    file >> data;
    file.close();


    for (auto figure : data["figures"]){
        if (figure["name"] == "pawn"){
            Pawn* pawn = new Pawn(&board, board.position_to_number_notation(figure["position"]), figure["color"]);
        }
        else if (figure["name"] == "rook"){
            Rook* rook = new Rook(&board, board.position_to_number_notation(figure["position"]), figure["color"]);
        }
        else if (figure["name"] == "knight"){
            Knight* knight = new Knight(&board, board.position_to_number_notation(figure["position"]), figure["color"]);
        }
        else if (figure["name"] == "bishop"){
            Bishop* bishop = new Bishop(&board, board.position_to_number_notation(figure["position"]), figure["color"]);
        }
        else if (figure["name"] == "queen"){
            Queen* queen = new Queen(&board, board.position_to_number_notation(figure["position"]), figure["color"]);
        }
        else if (figure["name"] == "king"){
            King* king = new King(&board, board.position_to_number_notation(figure["position"]), figure["color"]);
        }
        else {
            cout << "Invalid figure name" << endl;
        }

    }
}

void Board::load_default_positions() {
    this->import_json("default_positions.json");
}

bool Board::is_empty(pair<int, int> position) {
    return figure_by_position(position)->name == "null";
}

string Board::position_to_chess_notation(pair<int, int> position) {
    string letters = "abcdefgh";
    string numbers = "87654321";
    return string(1, letters[position.second]) + string(1, numbers[position.first]);
}

string Board::move_to_chess_notation(pair<int, int> position1, pair<int, int> position2) {
    return position_to_chess_notation(position1) + position_to_chess_notation(position2);
}

string Board::move_to_chess_notation(pair<pair<int, int>, pair<int, int>> move) {
    return move_to_chess_notation(move.first, move.second);
}

pair<int, int> Board::position_to_number_notation(string notation) {
    string letters = "abcdefgh";
    string numbers = "87654321";
    return make_pair(numbers.find(notation[1]), letters.find(notation[0]));
}

pair<pair<int, int>, pair<int, int>> Board::move_to_number_notation(string notation1, string notation2) {
    return make_pair(position_to_number_notation(notation1), position_to_number_notation(notation2));
}