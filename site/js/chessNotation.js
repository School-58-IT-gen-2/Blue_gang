let LETTER_TO_NUMBER = {
  a: 1,
  b: 2,
  c: 3,
  d: 4,
  e: 5,
  f: 6,
  g: 7,
  h: 8,
};

let NUMBER_TO_LETTER = {
  1: "a",
  2: "b",
  3: "c",
  4: "d",
  5: "e",
  6: "f",
  7: "g",
  8: "h",
};

const FIGURES_TO_NUMBERS = {
  0: "pawn",
  1: "rook",
  2: "bishop",
  3: "knight",
  4: "queen",
  5: "king",
};

const COLORS = {
  w: "white",
  b: "black",
};

function toChessNotation(x1, y1, x2, y2) {
  return NUMBER_TO_LETTER[x1] + y1 + "-" + NUMBER_TO_LETTER[x2] + y2;
}

function toNumberNotation(s) {
  return [
    LETTER_TO_NUMBER[s[0]],
    Number(s[1]),
    LETTER_TO_NUMBER[s[3]],
    Number(s[4]),
  ];
}

function decrypt(s) {
  let decrypted = [];
  for (let i = 0; i < s.length; i += 4) {
    decrypted.push([
      FIGURES_TO_NUMBERS[s[i]],
      COLORS[s[i + 1]],
      Number(s[i + 2]),
      Number(s[i + 3]),
    ]);
  }
  return decrypted;
}

export {
  LETTER_TO_NUMBER,
  NUMBER_TO_LETTER,
  toChessNotation,
  toNumberNotation,
  decrypt
};
