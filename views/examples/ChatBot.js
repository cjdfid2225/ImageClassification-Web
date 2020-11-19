import React from "react";

// reactstrap components
import {
  Container,
} from "reactstrap";

// core components

function ChatBot() {
  React.useEffect(() => {
    document.body.classList.add("login-page");
    document.body.classList.add("sidebar-collapse");
    document.documentElement.classList.remove("nav-open");
    window.scrollTo(0, 0);
    document.body.scrollTop = 0;
    return function cleanup() {
      document.body.classList.remove("login-page");
      document.body.classList.remove("sidebar-collapse");
    };
  });
  return (
    <>
      <div className="page-header clear-filter" filter-color="blue">
        <div
          className="page-header-image"
          style={{
            backgroundImage: "url(" + require("assets/img/login.jpg") + ")"
          }}
        ></div>
        <div className="content">
          <Container>
            <iframe allow="microphone;" width="350" height="700"
                src="https://console.dialogflow.com/api-client/demo/embedded/f29ee2fc-1146-4462-928f-164d1bb01c58">
            </iframe>
          </Container>
        </div>
      </div>
    </>
  );
}

export default ChatBot;
