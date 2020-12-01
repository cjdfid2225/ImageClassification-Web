import React from "react";
import Plot from 'react-plotly.js'; 

// reactstrap components
import {
  Button,
  NavItem,
  NavLink,
  Nav,
  TabContent,
  TabPane,
  Container,
  Row,
  Col,
  UncontrolledTooltip
} from "reactstrap";

// core components
// import ExamplesNavbar from "components/Navbars/ExamplesNavbar.js";
import ProfilePageHeader from "components/Headers/ProfilePageHeader.js";
// import DefaultFooter from "components/Footers/DefaultFooter.js";



function ProfilePage({match}) {
  const {user_id,user_age,user_sex} = match.params
  const [pills, setPills] = React.useState("2");
  React.useEffect(() => {
    document.body.classList.add("profile-page");
    document.body.classList.add("sidebar-collapse");
    document.documentElement.classList.remove("nav-open");
    return function cleanup() {
      document.body.classList.remove("profile-page");
      document.body.classList.remove("sidebar-collapse");
    };
  });

  const butaction = () => {
    window.location.href = "/image_upload/"+user_id+"/"+user_age+"/"+user_sex
  }


  return (
    <>
      {/* <ExamplesNavbar /> */}
      <div className="wrapper">
        <ProfilePageHeader user_id={user_id} user_age={user_age} user_sex={user_sex} />
        <div className="section">
          <Container>
            <div className="button-container">
              <Button className="btn-round" color="info" size="lg" onClick={butaction}>
                사진 올리기
              </Button>
            </div>
            <h3 className="title">영양관리의 중요성</h3>
            <h5 className="description">
            균형 잡힌 식사는 우리나라 전통의 탑 모양으로 디자인 된 ‘식품구성탑’이라 일컫는 다섯 층의 식품군으로 잘 표현될 수 있다. 1층에 곡류 전분류, 2층에 채소 과일류, 3층에 고기 생선 달걀 콩류, 4층에 우유 유제품류, 5층에 유지 견과 당류로 구성되고, 각 층의 크기와 위치는 실제 식생활에서 차지하는 중요성과 양을 표현하고 있다. 가능한한 매 끼니에 다섯 식품군의 식품을 골고루 먹는 것이 좋다.
            또한 하루 식사량도 적당량 섭취하여야 한다. 우리 몸에 필요한 필수영양소는 결핍 되면 결핍증을 유발하고, 과잉 섭취하여도 건강에 유해할 수 있다.
            <br></br>  <br></br>
            건강을 위한 식사의 기본 원칙은 식품의 다양성과 영양학적 균형, 적정한 식사량이다.
            </h5>
            <Row>
              <Col className="ml-auto mr-auto" md="6">
                <h4 className="title text-center">나의 식단일지</h4>
                <div className="nav-align-center">
                  <Nav
                    className="nav-pills-info nav-pills-just-icons"
                    pills
                    role="tablist"
                  >
                    <NavItem>
                      <NavLink
                        className={pills === "1" ? "active" : ""}
                        href="#pablo"
                        onClick={e => {
                          e.preventDefault();
                          setPills("1");
                        }}
                      >
                        <i className="now-ui-icons design_image"></i>
                      </NavLink>
                    </NavItem>
                    <NavItem>
                      <NavLink
                        className={pills === "2" ? "active" : ""}
                        href="#pablo"
                        onClick={e => {
                          e.preventDefault();
                          setPills("2");
                        }}
                      >
                        <i className="now-ui-icons location_world"></i>
                      </NavLink>
                    </NavItem>
                    <NavItem>
                      <NavLink
                        className={pills === "3" ? "active" : ""}
                        href="#pablo"
                        onClick={e => {
                          e.preventDefault();
                          setPills("3");
                        }}
                      >
                        <i className="now-ui-icons sport_user-run"></i>
                      </NavLink>
                    </NavItem>
                  </Nav>
                </div>
              </Col>
              <TabContent className="gallery" activeTab={"pills" + pills}>
                <TabPane tabId="pills1">
                  <Col className="ml-auto mr-auto" md="10">
                    <Row className="collections">
                      <Col md="6">
                        <img
                          alt="..."
                          className="img-raised"
                          src={require("assets/img/bg1.jpg")}
                        ></img>
                        <img
                          alt="..."
                          className="img-raised"
                          src={require("assets/img/bg3.jpg")}
                        ></img>
                      </Col>
                      <Col md="6">
                        <img
                          alt="..."
                          className="img-raised"
                          src={require("assets/img/bg8.jpg")}
                        ></img>
                        <img
                          alt="..."
                          className="img-raised"
                          src={require("assets/img/bg7.jpg")}
                        ></img>
                      </Col>
                    </Row>
                  </Col>
                </TabPane>
                <TabPane tabId="pills2">
                  <Col className="ml-auto mr-auto" md="10">
                    <Row className="collections">
                      <Col md="6">
                        <img
                          alt="..."
                          className="img-raised"
                          src={require("assets/img/bg6.jpg")}
                        ></img>
                        <img
                          alt="..."
                          className="img-raised"
                          src={require("assets/img/bg11.jpg")}
                        ></img>
                      </Col>
                      <Col md="6">
                        <img
                          alt="..."
                          className="img-raised"
                          src={require("assets/img/bg7.jpg")}
                        ></img>
                        <img
                          alt="..."
                          className="img-raised"
                          src={require("assets/img/bg8.jpg")}
                        ></img>
                      </Col>
                    </Row>
                  </Col>
                </TabPane>
                <TabPane tabId="pills3">
                  <Col className="ml-auto mr-auto" md="10">
                    <Row className="collections">
                      <Col md="6">
                        <img
                          alt="..."
                          className="img-raised"
                          src={require("assets/img/bg3.jpg")}
                        ></img>
                        <img
                          alt="..."
                          className="img-raised"
                          src={require("assets/img/bg8.jpg")}
                        ></img>
                      </Col>
                      <Col md="6">
                        <img
                          alt="..."
                          className="img-raised"
                          src={require("assets/img/bg7.jpg")}
                        ></img>
                        <img
                          alt="..."
                          className="img-raised"
                          src={require("assets/img/bg6.jpg")}
                        ></img>
                      </Col>
                    </Row>
                  </Col>
                </TabPane>
              </TabContent>
            </Row>
          </Container>
        </div>
        {/* <DefaultFooter /> */}
      </div>
    </>
  );
}

export default ProfilePage;
