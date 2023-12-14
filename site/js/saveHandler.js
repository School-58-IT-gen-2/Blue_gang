let data = "https://youtu.be/dQw4w9WgXcQ?si=T6PYXu7j8ImWt3SV";
// if (window.location.protocol === "https:") {
//   data = "https://chess.projectalpha.ru/game?id=" + id;
// } else {
//   data = "localhost:5000/game?id=" + id;
// }

let options = {
  text: data,
  width: 256,
  height: 256,
};

const qrCode = new QRCodeStyling({
  width: 400,
  height: 400,
  type: "svg",
  data: data,
  dotsOptions: {
    color: "#343434",
    type: "extra-rounded",
  },
  backgroundOptions: {
    color: "#e5e5e5",
  },
  imageOptions: {
    crossOrigin: "anonymous",
    margin: 20,
  },
});

qrCode.append(document.getElementById("qrDiv"));
