import React from "react";
import { Container } from "reactstrap";

import BootstrapTable from "react-bootstrap-table-next";
import filterFactory, { textFilter } from "react-bootstrap-table2-filter";
import paginationFactory from "react-bootstrap-table2-paginator";

class RestCall extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      results: [],
    };
  }

  callApi = () => {
    fetch("http://localhost:7777/list")
      .then((res) => res.json())
      // .then((data) => console.log(data))
      .then((data) =>
        this.setState({
          results: data.results,
        })
      );
  };

  componentDidMount() {
    this.callApi();
  }

  render() {
    const { results } = this.state;
    console.log(results);

    const columns = [
      {
        dataField: "id",
        text: "ID",
      },
      {
        dataField: "name",
        text: "Name",
      },
      {
        dataField: "content",
        text: "content",
      },
      {
        dataField: "created_at",
        text: "created_at",
      },
    ];

    return (
      <Container>
        <div>
          <BootstrapTable
            keyField="id"
            data={results}
            columns={columns}
            filter={filterFactory()}
            pagination={paginationFactory()}
          />
        </div>
      </Container>
    );
  }
}

export default RestCall;
