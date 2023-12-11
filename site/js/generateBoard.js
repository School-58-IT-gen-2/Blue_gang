import { NUMBER_TO_LETTER, decrypt } from "/site/js/chessNotation.js";
import { clickHandler } from "/site/js/clickHandler.js";

function generateBoard() {
  const chessboard = document.getElementById("chessboard");
  const colors = ["white", "black"];

  for (let row = 8; row > 0; row--) {
    const rowElement = document.createElement("tr");
    for (let col = 1; col < 9; col++) {
      const cellElement = document.createElement("td");
      cellElement.className = colors[(row + col) % 2];
      cellElement.id = NUMBER_TO_LETTER[col] + row;
      cellElement.addEventListener("click", function () {
        clickHandler(cellElement.id);
      });
      rowElement.appendChild(cellElement);
    }
    chessboard.appendChild(rowElement);
  }
}

function setFigures(code) {
  if (code == null) {
    code =
      "w0w210w220w230w240w250w260w270w281w111w183w123w172w132w164w155w140b710b720b730b740b750b760b770b781b811b883b823b872b832b864b855b84";
  }
  const figures = decrypt(code);
  figures.forEach((figure) => {
    let cage = document.getElementById(NUMBER_TO_LETTER[figure[3]] + figure[2]);
    let imgElement = document.createElement("img");
    imgElement.src =
      "site/res/" + figure[1] + "_" + figure[0].toLowerCase() + ".png";

    imgElement.classList.add("figure-image");
    // Привязываем фигуру к клетке
    cage.appendChild(imgElement);
  });
}

export { generateBoard, setFigures };
