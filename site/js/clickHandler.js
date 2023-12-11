import { sendMessage } from "/site/js/connect.js";
import { NUMBER_TO_LETTER } from "/site/js/chessNotation.js";
let selected = null;
let highlighted = [];

async function clickHandler(id) {
  if (selected == id){
    selected = null;
    removeHighlight();
  }
  else if (selected == null) {
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
    let color = moveResult.message.split(",")[0].toLowerCase();
    let name = moveResult.message.split(",")[1].toLowerCase().replace(" ", "");

    img.src = "site/res/" + color + "_" + name + ".png";
    img.classList.add("figure-image");

    document.getElementById(second).appendChild(img);

    sendMessage("get_move_color").then((moveColorResult) => {
      if (moveColorResult == 'white'){
        document.getElementById("nowMove").innerHTML = "Сейчас ход белых"
      }
      else if (moveColorResult == 'black'){
        document.getElementById("nowMove").innerHTML = "Сейчас ход черных"
      }
    })


    selected = null;
  });
}

export { clickHandler };
