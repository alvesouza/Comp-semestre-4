import React, { Component } from 'react';
import './customers.css';

class Customers extends Component {
  constructor() {
    super();
    this.state = {
      customers: []
    };
    this.mount = this.mount.bind(this)
  }

  mount() {
    console.log('React teste');
    fetch('/api/pessoas')
        .then(res => res.json())
        .then(customers => this.setState({customers}, () => console.log('Customers fetched...', customers)));
  }

  mount1() {
    fetch('/api/customers')
        .then(res => res.json())
        .then(customers => this.setState({customers}, () => console.log('Customers fetched...', customers)));
  }

  render() {
    return (
        // <Button
        //     variant="primary"
        //     disabled={isLoading}
        //     onClick={!isLoading ? handleClick : null}
        // >
        //   {isLoading ? 'Loading…' : 'Click to load'}
        // </Button>
      <div>
        <button onClick={this.mount}>oi</button>
        <ul>
        {this.state.customers.map(customer =>
          <li key={customer.id}>{customer.value} {customer.idade}</li>
        )}
        </ul>
      </div>
    );
  }
}

export default Customers;
