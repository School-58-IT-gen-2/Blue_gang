#include "main.h"
#include <iostream>

#include <string>

using namespace std;


Figure::Figure(Board* initialBoard, string initialName, pair<int, int> initialPosition, string initialColor,
               string initialSymbol)
        : board(initialBoard), name(initialName), position(initialPosition), color(initialColor), symbol(initialSymbol) {
    board->put_figure(this);
}


void Figure::move(pair<int, int> new_position) {
    already_moved = true;
    position = new_position;
}

bool Figure::is_null(){
    return this->name == "null";
}

bool Figure::is_empty(pair<int, int> position) {
    if (position.first > 7 or position.second > 7 or position.first < 0 or position.second < 0){
        return false;
    }
    return (board->figure_by_position(position)->name == "null");
}

bool Figure::is_teammate(pair<int, int> position){
    return (this->color == board->figure_by_position(position)->color);
}

bool Figure::is_opponent(pair<int, int> position) {
    auto figure = board->figure_by_position(position);
    return (figure->color != this->color and not figure->is_null());
}

vector<pair<int, int>> Figure::available_moves() {
    return vector<pair<int, int>> {};
}

NullFigure::NullFigure(Board* initialBoard) :
Figure(initialBoard, "null", make_pair(-1, -1), "null", "0") {}

Pawn::Pawn(Board* initialBoard, pair<int, int> position, string color) :
Figure(initialBoard, "pawn", position, color, (color == "white") ? "P" : "p") {}

vector<pair<int, int>> Pawn::available_moves(){
    vector<pair<int, int>> moves {};
    int direction = (color == "white") ? -1 : 1;

    if (is_empty(make_pair(position.first + direction, position.second))){
        moves.push_back(make_pair(position.first + direction, position.second));
    }

    if ((position.first == 6 and color == "white") or (position.first == 1 and color == "black")){
        if (is_empty(make_pair(position.first + 2 * direction, position.second))){
            moves.push_back(make_pair(position.first + 2 * direction, position.second));
        }
    }

    if (is_opponent(make_pair(position.first + direction, position.second + 1))){
        moves.push_back(make_pair(position.first + direction, position.second + 1));
    }
    if (is_opponent(make_pair(position.first + direction, position.second - 1))){
        moves.push_back(make_pair(position.first + direction, position.second - 1));
    }
    return moves;
}


Rook::Rook(Board* initialBoard, pair<int, int> position, string color) :
        Figure(initialBoard, "rook", position, color, (color == "white") ? "R" : "r") {}

vector<pair<int, int>> Rook::available_moves(){
    vector<pair<int, int>> moves {};
    int i;

    i = 1;
    while (is_empty(make_pair(position.first + i, position.second))){
        moves.push_back(make_pair(position.first + i, position.second));
        i++;
    }
    if (is_opponent(make_pair(position.first + i, position.second))){
        moves.push_back(make_pair(position.first + i, position.second));
    }

    i = 1;
    while (is_empty(make_pair(position.first - i, position.second))){
        moves.push_back(make_pair(position.first - i, position.second));
        i++;
    }
    if (is_opponent(make_pair(position.first - i, position.second))){
        moves.push_back(make_pair(position.first - i, position.second));
    }

    i = 1;
    while (is_empty(make_pair(position.first, position.second + i))){
        moves.push_back(make_pair(position.first, position.second + i));
        i++;
    }
    if (is_opponent(make_pair(position.first, position.second + i))){
        moves.push_back(make_pair(position.first, position.second + i));
    }

    i = 1;
    while (is_empty(make_pair(position.first, position.second - i))){
        moves.push_back(make_pair(position.first, position.second - i));
        i++;
    }
    if (is_opponent(make_pair(position.first, position.second - i))){
        moves.push_back(make_pair(position.first, position.second - i));
    }

    return moves;

}

Knight::Knight(Board* initialBoard, pair<int, int> position, string color) :
        Figure(initialBoard, "knight", position, color, (color == "white") ? "N" : "n") {}

vector<pair<int, int>> Knight::available_moves(){
    vector<pair<int, int>> moves {};

    if (is_opponent(make_pair(position.first + 2, position.second + 1)) or
        is_empty(make_pair(position.first + 2, position.second + 1))){
        moves.push_back(make_pair(position.first + 2, position.second + 1));
    }
    if (is_opponent(make_pair(position.first + 2, position.second - 1)) or
        is_empty(make_pair(position.first + 2, position.second - 1))){
        moves.push_back(make_pair(position.first + 2, position.second - 1));
    }
    if (is_opponent(make_pair(position.first - 2, position.second + 1)) or
        is_empty(make_pair(position.first - 2, position.second + 1))){
        moves.push_back(make_pair(position.first - 2, position.second + 1));
    }
    if (is_opponent(make_pair(position.first - 2, position.second - 1)) or
        is_empty(make_pair(position.first - 2, position.second - 1))){
        moves.push_back(make_pair(position.first - 2, position.second - 1));
    }
    if (is_opponent(make_pair(position.first + 1, position.second + 2)) or
        is_empty(make_pair(position.first + 1, position.second + 2))){
        moves.push_back(make_pair(position.first + 1, position.second + 2));
    }
    if (is_opponent(make_pair(position.first + 1, position.second - 2)) or
        is_empty(make_pair(position.first + 1, position.second - 2))){
        moves.push_back(make_pair(position.first + 1, position.second - 2));
    }
    if (is_opponent(make_pair(position.first - 1, position.second + 2)) or
        is_empty(make_pair(position.first - 1, position.second + 2))){
        moves.push_back(make_pair(position.first - 1, position.second + 2));
    }
    if (is_opponent(make_pair(position.first - 1, position.second - 2)) or
        is_empty(make_pair(position.first - 1, position.second - 2))){
        moves.push_back(make_pair(position.first - 1, position.second - 2));
    }

    return moves;
}

Bishop::Bishop(Board* initialBoard, pair<int, int> position, string color) :
        Figure(initialBoard, "bishop", position, color, (color == "white") ? "B" : "b") {}

vector<pair<int, int>> Bishop::available_moves(){
    vector<pair<int, int>> moves {};
    int i;

    i = 1;
    while (is_empty(make_pair(position.first + i, position.second + i))){
        moves.push_back(make_pair(position.first + i, position.second + i));
        i++;
    }
    if (is_opponent(make_pair(position.first + i, position.second + i))){
        moves.push_back(make_pair(position.first + i, position.second + i));
    }

    i = 1;
    while (is_empty(make_pair(position.first + i, position.second - i))){
        moves.push_back(make_pair(position.first + i, position.second - i));
        i++;
    }
    if (is_opponent(make_pair(position.first + i, position.second - i))){
        moves.push_back(make_pair(position.first + i, position.second - i));
    }

    i = 1;
    while (is_empty(make_pair(position.first - i, position.second + i))){
        moves.push_back(make_pair(position.first - i, position.second + i));
        i++;
    }
    if (is_opponent(make_pair(position.first - i, position.second - i))){
        moves.push_back(make_pair(position.first - i, position.second - i));
    }

    return moves;
}

Queen::Queen(Board* initialBoard, pair<int, int> position, string color) :
        Figure(initialBoard, "queen", position, color, (color == "white") ? "Q" : "q") {}


vector<pair<int, int>> Queen::available_moves(){
    vector<pair<int, int>> moves {};
    int i;

    i = 1;
    while (is_empty(make_pair(position.first + i, position.second))){
        moves.push_back(make_pair(position.first + i, position.second));
        i++;
    }
    if (is_opponent(make_pair(position.first + i, position.second))){
        moves.push_back(make_pair(position.first + i, position.second));
    }

    i = 1;
    while (is_empty(make_pair(position.first - i, position.second))){
        moves.push_back(make_pair(position.first - i, position.second));
        i++;
    }
    if (is_opponent(make_pair(position.first - i, position.second))){
        moves.push_back(make_pair(position.first - i, position.second));
    }

    i = 1;
    while (is_empty(make_pair(position.first, position.second + i))){
        moves.push_back(make_pair(position.first, position.second + i));
        i++;
    }
    if (is_opponent(make_pair(position.first, position.second + i))){
        moves.push_back(make_pair(position.first, position.second + i));
    }

    i = 1;
    while (is_empty(make_pair(position.first, position.second - i))){
        moves.push_back(make_pair(position.first, position.second - i));
        i++;
    }
    if (is_opponent(make_pair(position.first, position.second - i))){
        moves.push_back(make_pair(position.first, position.second - i));
    }

    i = 1;
    while (is_empty(make_pair(position.first + i, position.second + i))){
        moves.push_back(make_pair(position.first + i, position.second + i));
        i++;
    }
    if (is_opponent(make_pair(position.first + i, position.second + i))){
        moves.push_back(make_pair(position.first + i, position.second + i));
    }

    i = 1;
    while (is_empty(make_pair(position.first + i, position.second - i))){
        moves.push_back(make_pair(position.first + i, position.second - i));
        i++;
    }
    if (is_opponent(make_pair(position.first + i, position.second - i))){
        moves.push_back(make_pair(position.first + i, position.second - i));
    }

    i = 1;
    while (is_empty(make_pair(position.first - i, position.second + i))){
        moves.push_back(make_pair(position.first - i, position.second + i));
        i++;
    }
    if (is_opponent(make_pair(position.first - i, position.second - i))){
        moves.push_back(make_pair(position.first - i, position.second - i));
    }

    return moves;
}

King::King(Board* initialBoard, pair<int, int> position, string color) :
        Figure(initialBoard, "king", position, color, (color == "white") ? "K" : "k") {}


vector<pair<int, int>> King::available_moves(){
    vector<pair<int, int>> moves {};

    if (is_opponent(make_pair(position.first + 1, position.second)) or
        is_empty(make_pair(position.first + 1, position.second))){
        moves.push_back(make_pair(position.first + 1, position.second));
    }
    if (is_opponent(make_pair(position.first - 1, position.second)) or
        is_empty(make_pair(position.first - 1, position.second))){
        moves.push_back(make_pair(position.first - 1, position.second));
    }
    if (is_opponent(make_pair(position.first, position.second + 1)) or
        is_empty(make_pair(position.first, position.second + 1))){
        moves.push_back(make_pair(position.first, position.second + 1));
    }
    if (is_opponent(make_pair(position.first + 1, position.second + 1)) or
        is_empty(make_pair(position.first + 1, position.second + 1))){
        moves.push_back(make_pair(position.first + 1, position.second + 1));
    }
    if (is_opponent(make_pair(position.first + 1, position.second - 1)) or
        is_empty(make_pair(position.first + 1, position.second - 1))){
        moves.push_back(make_pair(position.first + 1, position.second - 1));
    }
    if (is_opponent(make_pair(position.first - 1, position.second + 1)) or
        is_empty(make_pair(position.first - 1, position.second + 1))){
        moves.push_back(make_pair(position.first - 1, position.second + 1));
    }
    if (is_opponent(make_pair(position.first - 1, position.second - 1)) or
        is_empty(make_pair(position.first - 1, position.second - 1))){
        moves.push_back(make_pair(position.first - 1, position.second - 1));
    }


    return moves;
}
