const express = require('express');
const cors = require('cors');
const bodyParser = require("body-parser");
const fs = require('fs');

const app = express();
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.get('/api/customers', cors(), (req, res) => {
  const customers = [
    {id: 1, firstName: 'John', lastName: 'Doe'},
    {id: 2, firstName: 'Brad', lastName: 'Traversy'},
    {id: 3, firstName: 'Mary', lastName: 'Swanson'},
    {id: 4, firstName: 'Broh', lastName: 'Swanson'},
  ];

  res.json(customers);
});
const util = require('util')



app.post('/api/pessoas', cors(), (req, res) => {
  // console.log('teste 1 ' + req);
  // console.log(util.inspect(req, {showHidden: false, depth: null}))
  console.log('teste ' + util.inspect(req.body, {showHidden: false, depth: null}));
  fs.readFile('pessoas.json', 'utf8', function readFileCallback(err, data){
    if (err){
      console.log('error:\n',err);
    } else {
      console.log('teste 01');
      obj = JSON.parse(data); //now it an object
      console.log('teste 02');
      console.log('teste ' + util.inspect(obj, {showHidden: false, depth: null}));
      obj.table.push(req.body); //add some data
      console.log('teste 03');
      console.log('teste ' + util.inspect(obj, {showHidden: false, depth: null}));
      json = JSON.stringify(obj); //convert it back to json
      console.log('teste 04');
      fs.writeFile('pessoas.json', json, function(err){
        if (err) throw err;
        console.log('The "data to append" was appended to file!');
      }); // write it back
    }});
  res.end("yes");
  return
});

const port = 5000;

app.listen(port, () => `Server running on port ${port}`);