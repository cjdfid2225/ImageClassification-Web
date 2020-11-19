import React from "react";

// reactstrap components
import { Container } from "reactstrap";

// core components

function Kibana() {
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
      <div className="content">
        <iframe
          src="http://localhost:5601/goto/04873dff53c297c50d5fd1bf9864bf0a"
          height="1200"
          width="1600"
        ></iframe>
      </div>
    </>
  );
}

export default Kibana;
