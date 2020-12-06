import React, { useState, useEffect, Component } from "react";
import { Redirect } from "react-router-dom";
import axios from "axios";
import Input_Images3_gets3 from "./Input_Images3_gets3.js";
// import Output_Images3_gets3 from "./Output_Images3_gets3.js";
import image_upload from "assets/img/new/image_default.png";

import Plot from 'react-plotly.js'; 



import {
  Button,
  Label,
  FormGroup,
  Input,
  InputGroupAddon,
  InputGroupText,
  InputGroup,
  Container,
  Row,
  Col,
} from "reactstrap";

class Image_upload extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedFile: null,
      input_s3path: image_upload,
      analysis_filename: null,
      user_id:"",
      user_age:"",
      user_sex:"",
      jsonRes1Data: [], 
      jsonRes1Layout: {},
      jsonRes2Data: [], 
      jsonRes2Layout: {}
    };

    console.log(props)

    this.handlePost = this.handlePost.bind(this);
    this.handleAnalysis = this.handleAnalysis.bind(this);

    this.testPost = this.testPost.bind(this);
  }

  handleFileInput(e) {
    this.setState({
      selectedFile: e.target.files[0],
    });
  }

  testPost() {
    console.log("2323")

    const data = {
      a : this.state.jsonRes1Data,
      b : this.state.jsonRes1Layout,
      c : this.props.match.params.user_id,
      d : this.props.match.params.user_age,
      e : this.props.match.params.user_sex,
      f: this.state.jsonRes2Data,
      g : this.state.jsonRes2Layout,
    }

    console.log("test",data)
    
    this.props.history.push('/profile-page/',data)
  }


  handlePost() {
    const formData = new FormData();
    formData.append("file", this.state.selectedFile);
    return axios
      .post("http://13.209.118.56:7777/api/upload", formData)
      .then((res) => {
        alert("성공");
        console.log(res.data.body);
        console.log(res.data.body.location);
        this.setState({
          input_s3path: res.data.body.location, 
          analysis_filename: res.data.body.key,
        });
      })
      .catch((err) => {
        alert("실패");
      });
  }

  handleAnalysis(props) {
    const url = "http://13.209.118.56:5000/process";
    console.log(this.state.selectedFile.name); 

    console.log(this.props.match.params.user_id)

    const data = {
      analysis_filename: this.state.analysis_filename,
      analysis_url: this.state.input_s3path, 
      analysis_id: this.props.match.params.user_id,
      analysis_age: this.props.match.params.user_age,
      analysis_sex: this.props.match.params.user_sex,
    };



    fetch(url, {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
        'Accept': 'application/json'
      },
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("test :", data);
        this.setState({
          jsonRes1Data: data.res1.data, 
          jsonRes1Layout: data.res1.layout,
          jsonRes2Data: data.res2.data, 
          jsonRes2Layout: data.res2.layout
        });
      });
         // this.setState({
        //   output_s3path: data.url,
        // });
  }

  render() {
    return (
      <>
      <div className="page-header clear-filter" filter-color="white">
        <div
          className="page-header-image"
          style={{
          backgroundImage: "url(" + require("assets/img/bg7.jpg") + ")"
          }}
        ></div>
          <Container>
            <h3 className="title">이미지 업로드</h3>
            <Row>
              <Col>
                <Input
                  type="file"
                  name="file"
                  onChange={(e) => this.handleFileInput(e)}
                />
              </Col>
            </Row>
            <Row>
              <Col>
                <Button color="info" type="button" onClick={this.handlePost}>
                  이미지 업로드
                </Button>
                <Button
                  color="info"
                  type="button"
                  onClick={this.handleAnalysis}
                >
                  분석하기
                </Button>
                <Button
                  color="info"
                  type="button"
                  onClick={this.testPost}
                >
                  누적 결과보기
                </Button>
              </Col>
            </Row>
            <Row>
              <Col md="6">
                <Input_Images3_gets3 s3path={this.state.input_s3path} />
              </Col>
              <Col md="6">
                <Plot
                  data={this.state.jsonRes1Data}
                  layout={this.state.jsonRes1Layout}
                />
              </Col>
              {/* <Col md="6">
                <Output_Images3_gets3 s3path={this.state.output_s3path} />
              </Col> */}
            </Row>
          </Container>
        </div>
    </>
    );
  }
}

export default Image_upload;
