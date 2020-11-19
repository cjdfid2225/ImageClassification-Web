import React from "react";

// reactstrap components
import { Container, Row, Col } from "reactstrap";

// core components


function Input_Images3_gets3({s3path}) {
  let pathString = s3path;
  return (
    <>
      <div>
        <Container>
          <Row>
          <Col lg="6" sm="12">
               <div>
                 <h2>input image</h2>
                <img
                  alt="..."
                  src={pathString}
                ></img>
              </div>
          </Col>
          </Row>
        </Container>
      </div>
    </>
  );
}

export default Input_Images3_gets3;
