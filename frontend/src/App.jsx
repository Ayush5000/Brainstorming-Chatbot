import { useState } from "react";
import "./App.css";
import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "https://brainstorming-chatbot.onrender.com";

function App() {

  const [messages, setMessages] = useState([]);

  const [input, setInput] = useState("");

  const [loading, setLoading] = useState(false);


  // =====================================================
  // PROFESSIONAL BRAINSTORMING STARTERS
  // =====================================================

  const suggestions = [
    {
      title: "Explore a Problem",
      prompt:
        "Student learning consistency"
    },
    {
      title: "Find Opportunities",
      prompt:
        "Problems people face when searching for internships"
    },
    {
      title: "Rethink a System",
      prompt:
        "How traditional college education could be improved"
    },
    {
      title: "Challenge the Status Quo",
      prompt:
        "The problem of people spending too much time deciding what to work on"
    },
    {
      title: "Discover Hidden Gaps",
      prompt:
        "Problems beginners face when learning programming"
    },
    {
      title: "Future Thinking",
      prompt:
        "How personal productivity could change with intelligent technology"
    }
  ];


  // =====================================================
  // SEND MESSAGE
  // =====================================================

  const sendMessage = async (customMessage = null) => {

    const text =
      customMessage !== null
        ? customMessage.trim()
        : input.trim();

    if (!text || loading) {
      return;
    }


    // ---------------------------------------------------
    // Preserve previous conversation
    // ---------------------------------------------------

    const currentHistory = messages.map((message) => ({
      role: message.role,
      content: message.content
    }));


    // ---------------------------------------------------
    // Add user message
    // ---------------------------------------------------

    const userMessage = {
      role: "user",
      content: text
    };

    setMessages((previous) => [
      ...previous,
      userMessage
    ]);

    setInput("");
    setLoading(true);


    try {

      // -------------------------------------------------
      // API REQUEST
      // -------------------------------------------------

      const API_URL = import.meta.env.VITE_API_URL || "https://brainstorming-chatbot.onrender.com";

const response = await fetch(`${API_URL}/chat`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    message: input,
    history: messages,
  }),
});


      if (!response.ok) {
        throw new Error("Backend error");
      }


      const data = await response.json();


      // -------------------------------------------------
      // Add assistant response
      // -------------------------------------------------

      const assistantMessage = {
        role: "assistant",
        content: data.reply
      };

      setMessages((previous) => [
        ...previous,
        assistantMessage
      ]);

    } catch (error) {

      console.error(error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            "Unable to connect to the brainstorming engine. Please make sure the FastAPI backend is running."
        }
      ]);

    } finally {

      setLoading(false);

    }
  };


  // =====================================================
  // ENTER TO SEND
  // =====================================================

  const handleKeyDown = (event) => {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      sendMessage();
    }
  };


  // =====================================================
  // CLEAR CHAT
  // =====================================================

  const clearChat = () => {

    if (loading) {
      return;
    }

    setMessages([]);

    setInput("");
  };


  // =====================================================
  // STARTER CLICK
  // =====================================================

  const handleSuggestion = (prompt) => {

    sendMessage(prompt);
  };


  // =====================================================
  // UI
  // =====================================================

  return (

    <div className="app">

      {/* =================================================
          BACKGROUND
      ================================================= */}

      <div className="background-glow glow-one"></div>

      <div className="background-glow glow-two"></div>


      {/* =================================================
          HEADER
      ================================================= */}

      <header className="header">

        <div className="brand">

          <div className="brand-icon">
            ✦
          </div>

          <div>

            <h1>
              Brainstorm
            </h1>

            <p>
              Professional thinking engine
            </p>

          </div>

        </div>


        <button
          className="clear-button"
          onClick={clearChat}
          disabled={
            messages.length === 0 ||
            loading
          }
        >
          Clear
        </button>

      </header>


      {/* =================================================
          MAIN CHAT
      ================================================= */}

      <main className="chat-container">


        {/* =================================================
            WELCOME
        ================================================= */}

        {messages.length === 0 && (

          <section className="welcome">

            <div className="welcome-icon">
              ✦
            </div>


            <h2>
              Think beyond the obvious.
            </h2>


            <p>
              Give me a topic, problem or opportunity.
              <br />
              I'll turn it into a structured professional brainstorm.
            </p>


            {/* =================================================
                STARTERS
            ================================================= */}

            <div className="suggestions">

              {suggestions.map(
                (suggestion, index) => (

                  <button
                    key={index}
                    className="suggestion-card"
                    onClick={() =>
                      handleSuggestion(
                        suggestion.prompt
                      )
                    }
                  >

                    <span className="suggestion-title">
                      {suggestion.title}
                    </span>


                    <span className="suggestion-text">
                      {suggestion.prompt}
                    </span>

                  </button>

                )
              )}

            </div>

          </section>

        )}


        {/* =================================================
            MESSAGES
        ================================================= */}

        {messages.length > 0 && (

          <section className="messages">

            {messages.map(
              (message, index) => (

                <div
                  key={index}
                  className={`message-row ${
                    message.role === "user"
                      ? "user-row"
                      : "assistant-row"
                  }`}
                >

                  <div
                    className={`message-bubble ${
                      message.role === "user"
                        ? "user-bubble"
                        : "assistant-bubble"
                    }`}
                  >

                    {message.content}

                  </div>

                </div>

              )
            )}


            {/* =================================================
                LOADING
            ================================================= */}

            {loading && (

              <div className="message-row assistant-row">

                <div className="message-bubble assistant-bubble typing">

                  <span></span>
                  <span></span>
                  <span></span>

                </div>

              </div>

            )}

          </section>

        )}

      </main>


      {/* =================================================
          INPUT
      ================================================= */}

      <footer className="input-area">

        <div className="input-wrapper">

          <textarea
            value={input}
            onChange={(event) =>
              setInput(event.target.value)
            }
            onKeyDown={handleKeyDown}
            placeholder="Enter a topic, problem or opportunity..."
            rows="1"
            disabled={loading}
          />


          <button
            className="send-button"
            onClick={() => sendMessage()}
            disabled={
              !input.trim() ||
              loading
            }
          >
            ↑
          </button>

        </div>


        <div className="input-hint">
          Enter to brainstorm · Shift + Enter for new line
        </div>

      </footer>

    </div>
  );
}


export default App;