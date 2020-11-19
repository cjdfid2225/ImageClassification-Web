/*eslint-disable*/
import React from "react";

// reactstrap components
import { Container } from "reactstrap";
// core components

function IndexHeader() {
  let pageHeader = React.createRef();

  React.useEffect(() => {
    if (window.innerWidth > 991) {
      const updateScroll = () => {
        let windowScrollTop = window.pageYOffset / 3;
        pageHeader.current.style.transform =
          "translate3d(0," + windowScrollTop + "px,0)";
      };
      window.addEventListener("scroll", updateScroll);
      return function cleanup() {
        window.removeEventListener("scroll", updateScroll);
      };
    }
  });

  return (
    <>
      <div className="page-header clear-filter" filter-color="white">
        <div
          className="page-header-image"
          style={{
            backgroundImage: "url(" + require("assets/img/background.jpg") + ")"
          }}
          ref={pageHeader}
        ></div>
        <Container>
          <div className="content-center brand">
            <img
              alt="..."
              className="n-logo"
              src={require("assets/img/now-logo1.png")}
            ></img>
            <h1 className="h1-seo">자가 영양 진단 사이트</h1>
            <h3>본인 식단을 스스로 영양분석 해보세요!</h3>
          </div>
          <h6 className="category category-absolute">
            Designed by{" "}
            <a href="http://infornet.korea.ac.kr/gb/index.php" target="_blank">
              <img
                alt="..."
                className="invision-logo"
                src={require("assets/img/now-logo1.png")}
              ></img>
            </a>
            . Coded by Team EN.D{" "}

            .
          </h6>
        </Container>
      </div>
    </>
  );
}

export default IndexHeader;
