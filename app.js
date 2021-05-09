const express = require("express");
const session = require("express-session");
const app = express();

app.get('/', async(req,res)=>{
    res.send("Casper API Test");
});

app.listen("7777", async ()=>{ // adjust port number
    console.log("Server Start")
});