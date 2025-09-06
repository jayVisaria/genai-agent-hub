const chatHistory = document.getElementById("chat-history");
const messageInput = document.getElementById("message");
let history = [];

async function sendMessage() {
    const message = messageInput.value;
    messageInput.value = "";

    const userMessage = document.createElement("div");
    userMessage.classList.add("message", "user");
    userMessage.innerText = message;
    chatHistory.appendChild(userMessage);

    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, history }),
    });

    const result = await response.json();
    const agentMessage = document.createElement("div");
    agentMessage.classList.add("message", "agent");
    agentMessage.innerText = result.response;
    chatHistory.appendChild(agentMessage);

