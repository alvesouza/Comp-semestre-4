// document.getElementById("demo").innerHTML = "<h1>Hello World!</h1>";
    // Pedro Alves de Souza Neto
    // Turma COMP21
var numElementos = 0;

function CreateElement(){
    numElementos++;
    var elemNova = document.createElement("p");
    elemNova.setAttribute("id","elemNovo" + numElementos);
    elemNova.innerHTML = "Elemento do DOM " + numElementos + "<br>";
    document.getElementById("demo").appendChild(elemNova);
}

function DeletaElement(){
    if (numElementos > 0) {
        document.getElementById("elemNovo" + numElementos).remove();
        numElementos--;  
    }
    
}

function alteraElementos(){
    var children = document.getElementById("demo").children;
    var matches;
    if(children.length == 0)
        CreateElement();
    for (const child of children) {
        matches = child.innerHTML.match(/\d+/g);

        if(matches.length > 1){
            child.innerHTML = "Elemento do DOM " + matches[0] +", alterado "+ (parseInt(matches[1])+1) +" vezes"+ "<br>";
        }else{
            child.innerHTML = "Elemento do DOM " + matches[0] +", alterado 1 vez"+ "<br>";
        }
    }
}

function corMudou(){
    return
}

function mudaCor(objeto){
    objeto.style = "background-color:"+document.getElementById("corEscolhida").value + ";";
}

function voltaCor(objeto){
    objeto.style = "background-color:rgb(57, 9, 230);";
}

function caiTexto(objeto, option = {intervalo:5, posFinalRelativa:110}) {
    var option = option||{};
    option.intervalo = option.intervalo||5;
    posFinalRelativa = option.posFinalRelativa||110;
    // console.log("Flag01");
    var posInicial = objeto.getBoundingClientRect().y;
    // console.log("Flag02 posInicial = " + posInicial);
    var aux = window.innerHeight;
    var pos= 100*posInicial/aux;
    posInicial = pos;
    var velocidade = (posFinalRelativa - pos)/(option.intervalo*1000);
    var time01 = Date.now();
    var time02;
    var dt;
    var id = setInterval(function() {
        time02 = Date.now();
        dt = time02 - time01;
        // console.log("Flag07 dt = " + dt);
        if (pos >= posFinalRelativa) {
            objeto.style.top = posInicial + "%"; 
            clearInterval(id);
        }  else {
            pos=pos+velocidade*dt; 
            // console.log("Flag09 objeto.style.top = " + objeto.style.top);
            objeto.style.top = pos + "%"; 
        }
        time01 = time02;
    }, 5);
    
}