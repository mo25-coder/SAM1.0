const form = document.getElementById("chatForm");
const textarea = document.getElementById("user_input");
const chatBox = document.getElementById("chatContainer");

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const userInput = textarea.value.trim();
    if (!userInput) return;

    // Add user message
    const userMessage = `
        <div class="message">
            <div class="role">User</div>
            <div class="content">${userInput}</div>
        </div>
    `;
    chatBox.insertAdjacentHTML("beforeend", userMessage);

    textarea.value = "";

    // Add loading message
    const loading = document.createElement("div");
    loading.id = "loadingMessage";
    loading.classList.add("message");
    loading.innerHTML = `
        <div class="role">Assistant</div>
        <div class="content">⏳ Thinking...</div>
    `;
    chatBox.appendChild(loading);

    chatBox.scrollTop = chatBox.scrollHeight;

    // Send to backend
    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: userInput })
    });

    const data = await res.json();

    document.getElementById("loadingMessage").remove();

    const assistantMessage = `
        <div class="message">
            <div class="role">Assistant</div>
            <div class="content">${data.response}</div>
        </div>
    `;
    chatBox.insertAdjacentHTML("beforeend", assistantMessage);
    // chatBox.scrollTop = chatBox.scrollHeight;
    chatBox.scrollTo({
        top: chatBox.scrollHeight,
        behavior: "smooth"
    });
    
});

textarea.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        form.dispatchEvent(new Event("submit"));
    }
});
