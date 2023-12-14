let socket = null;
let numOfMessages = 1;

function setSocket() {
  if (window.location.protocol === "https:") {
    socket = io.connect("https://chess.projectalpha.ru", { secure: true });
  } else {
    socket = io.connect("localhost:5000");
  }
}

async function sendMessage(type, message) {
  return new Promise((resolve, reject) => {
    const messageId = numOfMessages++;

    const handleServerMessage = (response) => {
      if (response.id === messageId) {
        resolve(response);
        socket.off("message_from_server", handleServerMessage);
      } else {
        return null;
      }
    };

    socket.on("message_from_server", handleServerMessage);

    socket.emit("message_from_client", {
      id: messageId,
      type: type,
      message: message,
    });

    const timeoutId = setTimeout(() => {
      reject(new Error("Timeout: No response from the server."));
      socket.off("message_from_server", handleServerMessage);
    }, 5000);
  });
}

export { socket, sendMessage, setSocket };
