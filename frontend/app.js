const API_URL = "https://skylark-bi-agent-9jvn.onrender.com/api/agent/chat";

const welcome = document.getElementById("welcome");
const chat = document.getElementById("chat");
const loading = document.getElementById("loading");
const messageInput = document.getElementById("message-input");
const sendButton = document.getElementById("send-button");


// =========================================
// Send Message
// =========================================

async function sendMessage(message) {

    message = message.trim();

    if (!message) {
        return;
    }

    // Hide welcome screen after first message
    welcome.style.display = "none";

    // Display user's message
    addMessage(message, "user");

    // Clear input
    messageInput.value = "";

    // Show loading indicator
    loading.classList.remove("hidden");

    // Disable input while waiting
    setInputState(false);

    try {

        const response = await fetch(API_URL, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });


        if (!response.ok) {

            throw new Error(
                `Server returned ${response.status}`
            );

        }


        const data = await response.json();

        console.log("Agent response:", data);


        // Display agent response
        addMessage(
            data.answer || "I could not generate a response.",
            "assistant"
        );


    } catch (error) {

        console.error("Agent request failed:", error);

        addMessage(
            "Sorry, I couldn't connect to the BI agent. Please make sure the backend server is running.",
            "assistant"
        );

    } finally {

        // Hide loading indicator
        loading.classList.add("hidden");

        // Re-enable input
        setInputState(true);

        // Put cursor back in input
        messageInput.focus();
    }
}


// =========================================
// Add Message to Chat
// =========================================

function addMessage(text, sender) {

    const messageElement = document.createElement("div");

    messageElement.className = `message ${sender}`;


    const avatar = document.createElement("div");

    avatar.className = "message-avatar";

    avatar.textContent = sender === "user"
        ? "You"
        : "S";


    const content = document.createElement("div");

    content.className = "message-content";


    // Basic formatting for assistant responses
    if (sender === "assistant") {

        content.innerHTML = formatAssistantMessage(text);

    } else {

        // User messages should remain plain text
        content.textContent = text;

    }


    messageElement.appendChild(avatar);
    messageElement.appendChild(content);

    chat.appendChild(messageElement);


    // Scroll to latest message
    messageElement.scrollIntoView({
        behavior: "smooth",
        block: "nearest"
    });
}


// =========================================
// Basic Assistant Formatting
// =========================================

function formatAssistantMessage(text) {

    if (!text) {
        return "";
    }

    return marked.parse(text, {
        gfm: true,
        breaks: true
    });
}

// =========================================
// Input State
// =========================================

function setInputState(enabled) {

    messageInput.disabled = !enabled;
    sendButton.disabled = !enabled;

}


// =========================================
// Send Button
// =========================================

sendButton.addEventListener(
    "click",
    () => {

        sendMessage(
            messageInput.value
        );

    }
);


// =========================================
// Enter / Shift + Enter
// =========================================

messageInput.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage(
                messageInput.value
            );

        }

    }
);


// =========================================
// Suggested Questions
// =========================================

const suggestions =
    document.querySelectorAll(".suggestion");


suggestions.forEach(
    (button) => {

        button.addEventListener(
            "click",
            () => {

                const question =
                    button.dataset.question;

                sendMessage(question);

            }
        );

    }
);


// =========================================
// Auto Resize Textarea
// =========================================

messageInput.addEventListener(
    "input",
    () => {

        messageInput.style.height = "auto";

        messageInput.style.height =
            `${Math.min(
                messageInput.scrollHeight,
                120
            )}px`;

    }
);

// =========================================
// Backend Connection Status
// =========================================

async function checkBackendConnection() {

    const statusElement =
        document.querySelector(".connection-status");

    const statusDot =
        document.querySelector(".status-dot");

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/health"
        );

        if (!response.ok) {
            throw new Error("Backend unavailable");
        }

        const data = await response.json();

        if (data.status === "ok") {

            statusElement.querySelector("span:last-child")
                .textContent = "Connected";

            statusDot.style.backgroundColor = "#10b981";

        } else {

            throw new Error("Invalid health response");

        }

    } catch (error) {

        statusElement.querySelector("span:last-child")
            .textContent = "Backend offline";

        statusDot.style.backgroundColor = "#ef4444";

        console.error(
            "Backend connection check failed:",
            error
        );
    }
}

checkBackendConnection();