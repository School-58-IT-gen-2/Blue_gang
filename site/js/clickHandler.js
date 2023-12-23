import { sendMessage } from "/site/js/connect.js";
import { NUMBER_TO_LETTER, toChessNotation } from "/site/js/chessNotation.js";
let selected = null;
let highlighted = [];
let moveColor = "white";
let numOfMoves = 0;

function setMoveColor(color) {
  moveColor = color;
  if (color == "white") {
    document.getElementById("nowMove").innerHTML = "Сейчас ход белых";
  } else if (color == "black") {
    document.getElementById("nowMove").innerHTML = "Сейчас ход черных";
  }
}

async function clickHandler(id) {
  if (selected == id) {
    selected = null;
    removeHighlight();
  } else if (selected == null) {
    sendMessage("get_color", id)
      .then((colorResult) => {
        sendMessage("get_move_color").then((moveColorResult) => {
          if (colorResult.message == moveColorResult.message) {
            selected = id;
            highlight(id);
          }
        });
      })
      .catch((error) => {
        console.error("Error:", error.message);
      });
  } else {
    if (highlighted.includes(id)) {
      move(selected, id);
    } else {
      sendMessage("get_color", id).then((colorResult) => {
        sendMessage("get_move_color").then((moveColorResult) => {
          if (colorResult.message == moveColorResult.message) {
            selected = id;
            removeHighlight();
            highlight(id);
          }
        });
      });
    }
  }
}

function highlight(id) {
  sendMessage("get_attack_positions", id).then((attackPositions) => {
    highlighted = attackPositions.message;
    attackPositions.message.forEach((position) => {
      console.log(position)
      document.getElementById(position).classList.add("attack_position");
    });
  });
}

function removeHighlight() {
  highlighted = [];
  for (let row = 8; row > 0; row--) {
    for (let col = 1; col < 9; col++) {
      document
        .getElementById(NUMBER_TO_LETTER[col] + row)
        .classList.remove("attack_position");
    }
  }
}

function move(first, second) {
  sendMessage("move", first + second).then((moveResult) => {
    removeHighlight();
    document
      .getElementById(first)
      .removeChild(
        document.getElementById(first).getElementsByTagName("img")[0]
      );

    if (
      document.getElementById(second).getElementsByTagName("img").length > 0
    ) {
      document
        .getElementById(second)
        .removeChild(
          document.getElementById(second).getElementsByTagName("img")[0]
        );
    }

    let img = document.createElement("img");
    console.log(moveResult)
    if (moveResult.message == "mate") {
      window.location.href = "/win";
    } else {
      let type = moveResult.message.split(",")[0]
      let color = moveResult.message.split(",")[1].toLowerCase();
      let name = moveResult.message
        .split(",")[2]
        .toLowerCase()
        .replace(" ", "");

      img.src = "site/res/" + color + "_" + name + ".png";
      console.log("site/res/" + color + "_" + name + ".png");
      img.classList.add("figure-image");

      document.getElementById(second).appendChild(img);

      console.log(moveResult)

      if (moveColor == "white") {
        setMoveColor("black");
      } else if (moveColor == "black") {
        setMoveColor("white");
      }

      addMove(first + "-" + second);

      selected = null;

      if (type == "mate"){
        window.location.href = "/win";
      }
      else {
        ai_move();
      }
    }
  });
}

function ai_move(){
  sendMessage("ai_move").then((moveResult) => {
    let img = document.createElement("img");
    let type = moveResult.message.split(",")[0]
    let color = moveResult.message.split(",")[1].toLowerCase();
    let name = moveResult.message
      .split(",")[2]
      .toLowerCase()
      .replace(" ", "");
    let move = moveResult.message.split(",")[3].toLowerCase();
    console.log(move)


    img.src = "site/res/" + color + "_" + name + ".png";
    console.log("site/res/" + color + "_" + name + ".png");
    img.classList.add("figure-image");

    document
      .getElementById(move[0] + move[1])
      .removeChild(
        document.getElementById(move[0] + move[1]).getElementsByTagName("img")[0]
      );

    document.getElementById(move[2] + move[3]).appendChild(img);
  })
}

function addMove(s) {
  let moves = document.getElementById("moves");
  let oneMove = document.createElement("text");
  numOfMoves++;
  oneMove.innerHTML = String(numOfMoves) + ". " + s + "<br>";
  moves.appendChild(oneMove);
}

export { clickHandler, setMoveColor, addMove };
