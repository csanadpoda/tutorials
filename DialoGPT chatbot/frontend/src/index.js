import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ChatBot, { Loading } from 'react-simple-chatbot';
import { createRoot } from 'react-dom/client';


class DBPedia extends Component {
  constructor(props) {
    super(props);

    this.state = {
      loading: true,
      result: '',
      trigger: false,
    };

    this.triggetNext = this.triggetNext.bind(this);

  }

  componentWillMount() {
    const self = this;
    const { steps } = this.props;
    const search = steps.search.value;
    const query = search;

    const queryUrl = `http://localhost:5000/query`;

    const xhr = new XMLHttpRequest();

    xhr.addEventListener('readystatechange', readyStateChange);

    function readyStateChange() {
      if (this.readyState === 4) {
        const data = JSON.parse(this.responseText);
        const bindings = data.botResponse;
        self.setState({ loading: false, result: bindings });
      }
    }

    xhr.open("POST", queryUrl);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ "lastConversations": query }));
  }

  triggetNext() {
    this.setState({ trigger: true }, () => {
      this.props.triggerNextStep();
    });
  }

  render() {
    const { trigger, loading, result } = this.state;

    return (
      <div className="dbpedia">
        {loading ? <Loading /> : result}
        {
          !loading &&
          <div>
            {
              !trigger &&
              <button style={{
                display: "none"
              }}
                onClick={this.triggetNext()}
              ></button>
            }
          </div>
        }
      </div>
    );
  }
}

DBPedia.propTypes = {
  steps: PropTypes.object,
  triggerNextStep: PropTypes.func,
};

DBPedia.defaultProps = {
  steps: undefined,
  triggerNextStep: undefined,
};


const ExampleDBPedia = () => (
  <ChatBot
    steps={[
      {
        id: '1',
        message: 'Hi! I\'m DialoGPT. Type something to start chatting!',
        trigger: 'search',
      },
      {
        id: 'search',
        user: true,
        trigger: '3',
      },
      {
        id: '3',
        component: <DBPedia />,
        waitAction: true,
        asMessage: true,
        trigger: "search",
      },
    ]}
  />
);

export default ExampleDBPedia;

const container = document.getElementById('root');
const root = createRoot(container);
root.render(<ExampleDBPedia />);