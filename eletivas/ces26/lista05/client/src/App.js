import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Customers from './components/customers';
import axios from 'axios';

class MyForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: '', idade:null};

    }

    myChangeHandler = (event) => {
        this.setState({[event.target.name]: event.target.value});
    }

    handleSubmit = (event) => {
        if (this.state.idade >= 18) {
            alert('Um nome foi enviado: ' + JSON.stringify(this.state));
            console.log('teste 2 ' + JSON.stringify(this.state))
            axios.post('/api/pessoas', this.state).then(
                response => {
                    console.log(response);
                }
            ).catch(function (error) {
                   console.log('teste 2 ' + error)
                });
        }else
            alert('Idade invalida');
        event.preventDefault();
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label>
                    Nome:
                    <input type="text" name='value' onChange={this.myChangeHandler} />
                </label>
                <label>
                    Idade:
                    <input type="number" name='idade' onChange={this.myChangeHandler} />
                </label>
                <input type="submit" value="Enviar" />
            </form>
        );
    }
}
class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">React Express Starter</h1>
        </header>
          <MyForm />
        <Customers />
      </div>
    );
  }
}

export default App;
