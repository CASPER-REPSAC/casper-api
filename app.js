const express = require("express");
const session = require("express-session");
const app = express();

app.get('/',(req,res){
    res.send("Casper API Test");
});

app.listen("7777", ()=>{
    console.log("Server Start")
});