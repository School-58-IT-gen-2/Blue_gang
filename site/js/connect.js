const socket = io.connect("https://" + document.domain + ":" + location.port, {secure: true});
let numOfMessages = 1;

async function sendMessage(type, message) {
  return new Promise((resolve, reject) => {
    const messageId = numOfMessages++;

    const handleServerMessage = (response) => {
      if (response.id === messageId) {
        resolve(response);
        socket.off("message_from_server", handleServerMessage);
      } else {
        return null;ч
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

export { socket, sendMessage };
