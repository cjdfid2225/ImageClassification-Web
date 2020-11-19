import React from 'react';
import ReactMarkdown from 'react-markdown';
import CodeBlock from './CodeBlock';
import test from './md/test2.md';

import {
    Container
  } from "reactstrap";


  class Markdown extends React.PureComponent {
    constructor(props) {
        super(props)
    
        this.state = { markdown: null }
      }
    
      componentWillMount() {
        fetch(test).then((response) => response.text()).then((text) => {
          this.setState({ markdown: text })
        })
      }
    
    render() {

      return (
        <Container>
          <ReactMarkdown
            source={this.state.markdown}
            renderers={{
              code: CodeBlock,
            }}
          />  
        </Container>
      );
    }
  }


export default Markdown;