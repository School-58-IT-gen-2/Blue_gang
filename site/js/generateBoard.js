import { NUMBER_TO_LETTER } from "/site/js/chessNotation.js";
import { clickHandler, setMoveColor, addMove } from "/site/js/clickHandler.js";

function generateBoard() {
  const chessboard = document.getElementById("chessboard");
  const colors = ["white", "black"];

  for (let row = 8; row > 0; row--) {
    const rowElement = document.createElement("tr");
    for (let col = 1; col < 9; col++) {
      const cellElement = document.createElement("td");
      cellElement.className = colors[(row + col + 1) % 2];
      cellElement.id = NUMBER_TO_LETTER[col] + row;
      cellElement.addEventListener("click", function () {
        clickHandler(cellElement.id);
      });
      rowElement.appendChild(cellElement);
    }
    chessboard.appendChild(rowElement);
  }
}

function loadData(code) {
  if (code == null) {
    code = "default";
  }

  let URLforRequest;

  if (window.location.protocol === "https:") {
    URLforRequest = "https://chess.projectalpha.ru";
  } else {
    URLforRequest = "http://127.0.0.1:5000";
  }

  fetch(URLforRequest + "/get_save/" + code)
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Ошибка: ${response.status}`);
      }

      return response.json();
    })
    .then((data) => {
      data = JSON.parse(data);
      setMoveColor(data.move_color);
      data.figures.forEach((figure) => {
        let cage = document.getElementById(figure.column + figure.row);
        let imgElement = document.createElement("img");
        imgElement.src =
          "site/res/" + figure.color + "_" + figure.name.toLowerCase() + ".png";
        imgElement.classList.add("figure-image");
        cage.appendChild(imgElement);
      });
      data.moves.forEach((element) => {
        addMove(element);
      });
    })
    .catch((error) => {
      console.error("Ошибка при запросе данных:", error);
    });
}

export { generateBoard, loadData };
